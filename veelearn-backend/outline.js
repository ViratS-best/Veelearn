'use strict';

/**
 * Course outlines.
 *
 * A creator no longer writes a course body: they draw a map. Each unit is a
 * page, each skill is a circle on that page, and each skill carries a short
 * teaching brief plus its own questions (written or pulled from the bank, with
 * diagrams). This module is the one place that reads that map, so the creator
 * API and the session planner agree on its shape.
 *
 * Shape (version 1):
 * {
 *   version: 1,
 *   units: [{
 *     id, title, summary,
 *     skills: [{
 *       id, name, teach,
 *       questions: [{ id, stem, hint, why, visual, options:[{k,t}], answer }]
 *     }]
 *   }]
 * }
 */

const FRAME_CHARS = 900;
const LETTERS = 'ABCDEFGH';
const REVIEW_MIN = 4;
const REVIEW_TARGET_RATIO = 0.9;

function parseJson(value, fallback) {
    if (value == null) return fallback;
    if (typeof value === 'object') return value;
    try {
        const parsed = JSON.parse(String(value));
        return parsed == null ? fallback : parsed;
    } catch (_) {
        return fallback;
    }
}

function text(value, max) {
    return String(value == null ? '' : value)
        .replace(/\r\n/g, '\n')
        .trim()
        .slice(0, max);
}

function normaliseQuestion(q, index) {
    const options = (Array.isArray(q?.options) ? q.options : [])
        .map((o, i) => {
            const t = text(typeof o === 'string' ? o : o?.t, 600);
            if (!t) return null;
            const k = text(o?.k, 1) || LETTERS[i];
            return { k: String(k).toUpperCase().slice(0, 1), t };
        })
        .filter(Boolean)
        .slice(0, 6);
    if (!options.length) return null;
    const answer = text(q?.answer, 1).toUpperCase();
    const key = options.some((o) => o.k === answer) ? answer : options[0].k;
    const stem = text(q?.stem, 1200);
    if (!stem) return null;
    return {
        id: text(q?.id, 40) || `q${index + 1}`,
        stem,
        options,
        answer: key,
        hint: text(q?.hint, 400),
        why: text(q?.why, 700),
        visual: q?.visual && typeof q.visual === 'object' ? q.visual : null,
        bankId: q?.bankId ? Number(q.bankId) : null
    };
}

/** Trim, de-duplicate and number an incoming outline. */
function normalise(raw) {
    const unitsIn = Array.isArray(raw?.units) ? raw.units : [];
    const units = unitsIn
        .slice(0, 24)
        .map((u, ui) => {
            const skillsIn = Array.isArray(u?.skills) ? u.skills : [];
            const skills = skillsIn
                .slice(0, 24)
                .map((s, si) => {
                    const name = text(s?.name, 160);
                    if (!name) return null;
                    const questions = (Array.isArray(s?.questions) ? s.questions : [])
                        .slice(0, 40)
                        .map(normaliseQuestion)
                        .filter(Boolean);
                    return {
                        id: text(s?.id, 40) || `u${ui + 1}s${si + 1}`,
                        name,
                        teach: text(s?.teach, 1600),
                        questions
                    };
                })
                .filter(Boolean);
            const title = text(u?.title, 160);
            if (!title) return null;
            return {
                id: text(u?.id, 40) || `u${ui + 1}`,
                title,
                summary: text(u?.summary, 600),
                skills
            };
        })
        .filter(Boolean)
        .slice(0, 24);
    return { version: 1, units, updatedAt: new Date().toISOString() };
}

function skillCount(outline) {
    return (outline?.units || []).reduce((n, u) => n + (u.skills?.length || 0), 0);
}

function questionCount(outline) {
    return (outline?.units || []).reduce(
        (n, u) => n + (u.skills || []).reduce((m, s) => m + (s.questions?.length || 0), 0),
        0
    );
}

/**
 * Turn the map into session items, in exactly the order it was drawn.
 *
 * Every outline skill gets a synthetic bank skill so the existing engine can
 * grade, schedule reviews and record mastery without a second code path. The
 * questions are copied into qbank_items (stem_hash keeps it idempotent), and the
 * teaching brief travels as the card's frame.
 */
function createOutlines({ query, log } = {}) {
    const warn = (m) => {
        if (log && log.warn) log.warn(m);
    };

    async function load(courseId) {
        const rows = await query('SELECT outline_json FROM course_outlines WHERE course_id = ? LIMIT 1', [courseId]);
        return rows.length ? normalise(parseJson(rows[0].outline_json, null)) : null;
    }

    async function save(courseId, outline) {
        const clean = normalise(outline);
        const payload = JSON.stringify(clean);
        // UPDATE-then-INSERT keeps this working on both MySQL and Postgres.
        const updated = await query('UPDATE course_outlines SET outline_json = ?, updated_at = CURRENT_TIMESTAMP WHERE course_id = ?', [
            payload,
            courseId
        ]);
        const header = Array.isArray(updated) ? updated[0] : updated;
        const changed = Number((header && (header.affectedRows ?? header.rowCount)) || 0);
        if (!changed) {
            await query('INSERT INTO course_outlines (course_id, outline_json) VALUES (?, ?)', [courseId, payload]);
        }
        return clean;
    }

    async function ensureSkill(course, code, name, intro) {
        await query(
            `INSERT IGNORE INTO skills (code, track, name, grade_band, order_index, dot_target, intro_md, misconceptions)
             VALUES (?, 'course', ?, ?, 0, 2, ?, '[]')`,
            [code, name, course.grade_level != null ? Number(course.grade_level) : null, intro || null]
        );
        await query('UPDATE skills SET name = ?, intro_md = ? WHERE code = ?', [name, intro || null, code]);
        const rows = await query('SELECT id FROM skills WHERE code = ? LIMIT 1', [code]);
        return rows[0] ? Number(rows[0].id) : null;
    }

    const crypto = require('crypto');

    /** Insert the skill's questions once; return their bank ids in creator order. */
    async function ensureQuestions(skillId, courseId, questions) {
        const prepared = questions.map((q) => ({
            q,
            hash: crypto.createHash('sha256').update(`${courseId}|${q.stem}`).digest('hex')
        }));
        if (!prepared.length) return [];

        const hashes = prepared.map((p) => p.hash);
        const marks = hashes.map(() => '?').join(', ');
        let known = [];
        try {
            known = await query(`SELECT id, stem_hash FROM qbank_items WHERE stem_hash IN (${marks})`, hashes);
        } catch (_) {
            known = [];
        }
        const idByHash = new Map(known.map((r) => [String(r.stem_hash), Number(r.id)]));
        const missing = prepared.filter((p) => !idByHash.has(p.hash));

        for (let i = 0; i < missing.length; i += 30) {
            const chunk = missing.slice(i, i + 30);
            const values = chunk.map(() => `(?, 1, 'mcq', ?, ?, ?, ?, ?, ?, ?, 'course', ?, 1)`).join(', ');
            const params = [];
            chunk.forEach(({ q, hash }) => {
                params.push(
                    skillId,
                    q.stem.slice(0, 2000),
                    hash,
                    JSON.stringify(q.options),
                    q.answer,
                    JSON.stringify(q.hint ? [q.hint] : []),
                    JSON.stringify(q.why ? [q.why] : []),
                    q.visual ? JSON.stringify(q.visual) : null,
                    Number(courseId)
                );
            });
            try {
                await query(
                    `INSERT IGNORE INTO qbank_items
                        (skill_id, tier, qtype, stem, stem_hash, options, answer, hints, solution_steps, visual, source, course_id, live)
                     VALUES ${values}`,
                    params
                );
            } catch (err) {
                warn(`[outline] question batch skipped: ${err.message}`);
            }
        }

        if (missing.length) {
            try {
                const fresh = await query(`SELECT id, stem_hash FROM qbank_items WHERE stem_hash IN (${marks})`, hashes);
                fresh.forEach((r) => idByHash.set(String(r.stem_hash), Number(r.id)));
            } catch (_) {
                /* keep the ids we already had */
            }
        }
        return prepared.map((p) => idByHash.get(p.hash)).filter(Boolean);
    }

    /**
     * The plan for an outline course: each skill in drawing order, followed by a
     * review of the whole unit. Returns [] when the course has no usable outline.
     */
    async function planFromOutline(course, { maxItems } = {}) {
        const outline = await load(course.id);
        if (!outline || !outline.units.length) return [];

        const items = [];
        let ord = 0;
        for (const unit of outline.units) {
            const unitQuestions = [];
            const unitSkills = [];
            for (let si = 0; si < unit.skills.length; si += 1) {
                const skill = unit.skills[si];
                const code = `course.${course.id}.o${unit.id}.${skill.id}`.slice(0, 120);
                const brief =
                    `${skill.name}\n\n${skill.teach || ''}`.trim() ||
                    `${skill.name}: teach the idea, then let the learner practise it.`;
                const skillId = await ensureSkill(course, code, skill.name.slice(0, 160), brief.slice(0, FRAME_CHARS));
                if (!skillId) continue;
                const ids = await ensureQuestions(skillId, course.id, skill.questions);
                unitSkills.push({ skillId, name: skill.name, ids });
                unitQuestions.push(...ids);
                if (maxItems && items.length >= maxItems) break;
                if (!ids.length) continue;
                items.push({
                    ord: ord++,
                    skillId,
                    skillName: skill.name,
                    isReview: 0,
                    // Three to five questions per skill, exactly as the learner asked.
                    targetDots: ids.length >= 4 ? 3 : 2,
                    startTier: 1,
                    unitIndex: outline.units.indexOf(unit) + 1,
                    unitLabel: `Unit ${outline.units.indexOf(unit) + 1}: ${unit.title}`,
                    frame: {
                        unit: outline.units.indexOf(unit) + 1,
                        title: skill.name,
                        digest: brief.slice(0, FRAME_CHARS),
                        truncated: brief.length > FRAME_CHARS
                    },
                    questionIds: ids.slice(0, 5)
                });
            }

            // End-of-unit review: the unit's questions, and a 90% bar to clear it.
            const pool = [...new Set(unitQuestions)].slice(0, 20);
            if (pool.length >= REVIEW_MIN && unitSkills.length) {
                const reviewCode = `course.${course.id}.rv${unit.id}`.slice(0, 120);
                const reviewName = `Review: ${unit.title}`;
                const reviewBrief =
                    `Review of ${unit.title}. The learner is checked on every skill in this unit. ` +
                    `Pass mark: ${Math.round(REVIEW_TARGET_RATIO * 100)}%. Skills missed go back into the plan.`;
                const reviewSkillId = await ensureSkill(course, reviewCode, reviewName.slice(0, 160), reviewBrief);
                if (reviewSkillId) {
                    const ids = await ensureQuestions(reviewSkillId, course.id, []);
                    const all = [...new Set([...pool, ...ids])];
                    items.push({
                        ord: ord++,
                        skillId: reviewSkillId,
                        skillName: reviewName,
                        isReview: 1,
                        targetDots: Math.max(2, Math.ceil(all.length * REVIEW_TARGET_RATIO)),
                        startTier: 1,
                        unitIndex: outline.units.indexOf(unit) + 1,
                        unitLabel: `Unit ${outline.units.indexOf(unit) + 1}: ${unit.title} review`,
                        frame: {
                            unit: outline.units.indexOf(unit) + 1,
                            title: reviewName,
                            digest: reviewBrief.slice(0, FRAME_CHARS),
                            truncated: false
                        },
                        questionIds: all.slice(0, 20),
                        reviewOf: unit.id
                    });
                }
            }
        }
        return items;
    }

    return { load, save, planFromOutline, normalise, skillCount, questionCount };
}

module.exports = createOutlines;
module.exports.normalise = normalise;
module.exports.skillCount = skillCount;
module.exports.questionCount = questionCount;
