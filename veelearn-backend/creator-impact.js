'use strict';

/**
 * P4 — course-guided teaching.
 *
 * Three jobs, all deterministic and cheap enough to run on every publish:
 *
 *   1. Readiness gate (§15.3). Score a peer course on whether a session can be
 *      taught from it, auto-fix what can be fixed (split into units, map to
 *      skills), and tell the creator exactly what to improve. Gate, don't block:
 *      a course under 60 still gets sessions, in bank-led mode, at half hours.
 *
 *   2. The course plan (§15.2). Unit order, then prerequisites, then the
 *      creator's own questions before the shared bank. The unit's own text is
 *      what the tutor teaches from, so a session sounds like its author.
 *
 *   3. Teaching-impact hours (§15.4). Volunteer hours v2 pay for verified
 *      learning that happened without the creator present: per-session hours
 *      scaled by readiness, rating and mastery gain, behind gates that make a
 *      two-account farm worthless and caps that bound a nonprofit certificate
 *      programme. Every grant, paid or refused, is written to the ledger so the
 *      creator pane and the certificate both read the same rows.
 */

const WEIGHTS = { units: 30, skills: 25, questions: 25, prose: 15, sims: 5 };
const PROSE_MIN = 80;
const READY_PASS = 60;
const SESSION_HOURS = 0.25;
const COMPLETION_HOURS = 1;
const COMPLETION_MAX = 10;
const CAP_DAY = 3;
const CAP_WEEK = 20;
const CAP_COURSE = 200;
const MIN_LEARNERS = 2;
const MIN_MINUTES = 10;
const MIN_ITEMS = 3;
const FRAME_CHARS = 600;

const STOPWORDS = new Set([
    'the', 'and', 'for', 'with', 'that', 'this', 'from', 'into', 'your', 'you', 'are', 'was', 'were',
    'will', 'can', 'how', 'why', 'what', 'when', 'their', 'them', 'then', 'than', 'there', 'here',
    'unit', 'lesson', 'chapter', 'part', 'section', 'course', 'intro', 'introduction', 'summary',
    'practice', 'review', 'overview', 'using', 'use', 'used', 'about', 'more', 'most', 'some', 'such'
]);

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

function stripHtml(html) {
    return String(html || '')
        .replace(/<script[\s\S]*?<\/script>/gi, ' ')
        .replace(/<style[\s\S]*?<\/style>/gi, ' ')
        .replace(/<[^>]+>/g, ' ')
        .replace(/&nbsp;/gi, ' ')
        .replace(/&amp;/gi, '&')
        .replace(/&lt;/gi, '<')
        .replace(/&gt;/gi, '>')
        .replace(/&quot;/gi, '"')
        .replace(/\s+/g, ' ')
        .trim();
}

function tokensOf(text) {
    return new Set(
        String(text || '')
            .toLowerCase()
            .replace(/[^a-z0-9\s]/g, ' ')
            .split(/\s+/)
            .filter((w) => w.length >= 4 && !STOPWORDS.has(w) && !/^\d+$/.test(w))
    );
}

/**
 * Units, in the creator's order. <h2> is the unit boundary; a course with only
 * one <h2> (the "1 unit" course from the acceptance test) is split by <h3>, and
 * a course with neither is chunked by words so it still has teachable parts.
 */
function splitUnits(content) {
    const html = String(content || '');
    const byH2 = html.split(/<h2[^>]*>/i).filter((part) => part.trim());
    if (byH2.length >= 2) {
        return byH2.map((part, i) => {
            const raw = part.replace(/<\/h2>[\s\S]*$/i, '');
            const rest = part.slice(part.toLowerCase().indexOf('</h2>') + 5);
            const title = stripHtml(raw) || `Unit ${i + 1}`;
            const body = stripHtml(rest);
            return { ord: i, title: title.slice(0, 120), text: body, html: rest };
        });
    }

    const byH3 = html.split(/<h3[^>]*>/i).filter((part) => part.trim());
    if (byH3.length >= 2) {
        return byH3.map((part, i) => {
            const raw = part.replace(/<\/h3>[\s\S]*$/i, '');
            const rest = part.slice(part.toLowerCase().indexOf('</h3>') + 5);
            return {
                ord: i,
                title: (stripHtml(raw) || `Section ${i + 1}`).slice(0, 120),
                text: stripHtml(rest),
                html: rest
            };
        });
    }

    // A single section still has to become a teachable plan: paragraph blocks
    // are the natural boundaries, so a one-unit course auto-splits into parts.
    const heading = (html.match(/<h[12][^>]*>([\s\S]*?)<\/h[12]>/i) || [])[1];
    const baseTitle = (heading ? stripHtml(heading) : '') || 'Course';
    const body = stripHtml(html);
    if (!body) return [];

    const blocks = html
        .split(/<\/(?:p|li|div|blockquote|section)>|<br\s*\/?>/i)
        .map((block) => stripHtml(block))
        .filter((block) => block.length >= 40);
    if (blocks.length >= 2) {
        return blocks.slice(0, 8).map((text, i) => ({
            ord: i,
            title: `${baseTitle} · part ${i + 1}`.slice(0, 120),
            text,
            html: text
        }));
    }

    // Last resort: slice the prose so the plan always has more than one stop.
    const words = body.split(' ');
    const parts = words.length >= 60 ? Math.min(4, Math.max(2, Math.ceil(words.length / 120))) : 1;
    const size = Math.ceil(words.length / parts);
    const units = [];
    for (let i = 0; i < parts; i += 1) {
        const chunk = words.slice(i * size, (i + 1) * size).join(' ');
        if (!chunk.trim()) continue;
        units.push({ ord: units.length, title: parts === 1 ? baseTitle : `${baseTitle} · part ${units.length + 1}`, text: chunk, html: chunk });
    }
    return units;
}

function readinessMultiplier(score) {
    return score >= READY_PASS ? 1 : 0.5;
}

function qualityMultiplier(avgRating) {
    if (!Number.isFinite(avgRating) || avgRating <= 0) return 1;
    if (avgRating >= 4) return 1.2;
    if (avgRating < 3) return 0.6;
    return 1;
}

function masteryMultiplier(avgGain) {
    if (!Number.isFinite(avgGain)) return 1;
    if (avgGain >= 0.5) return 1.2;
    if (avgGain < 0.2) return 0.5;
    return 1;
}

function round2(n) {
    return Math.round((Number(n) || 0) * 100) / 100;
}

function createCreatorImpact({ query, log } = {}) {
    const info = (log && log.info) || (() => {});

    async function loadCourse(courseId) {
        const rows = await query(
            `SELECT id, title, description, content, creator_id, status, readiness_score, sessions_taught, grade_level
             FROM courses WHERE id = ? LIMIT 1`,
            [courseId]
        );
        return rows[0] || null;
    }

    /**
     * Score a course for session-readiness, persisting the mapping so the next
     * call is cheap and the editor can show what was auto-filled (§15.3).
     */
    async function readiness(courseId, { persist = true } = {}) {
        const course = await loadCourse(courseId);
        if (!course) {
            const err = new Error('Course not found');
            err.status = 404;
            throw err;
        }

        const units = splitUnits(course.content);
        const allSkills = await query('SELECT id, code, track, name FROM skills ORDER BY track ASC, order_index ASC');

        // An explicit creator mapping always wins over the keyword pass.
        const explicit = await query(
            'SELECT skill_id, weight, source FROM course_skills WHERE course_id = ? AND source <> ?',
            [courseId, 'auto']
        );
        const mapped = new Map(explicit.map((r) => [Number(r.skill_id), { source: r.source || 'creator' }]));

        const unitSkillIndex = [];
        for (const unit of units) {
            const unitTokens = tokensOf(`${unit.title} ${unit.text}`);
            const scored = [];
            for (const skill of allSkills) {
                if (mapped.has(Number(skill.id))) continue;
                const nameTokens = tokensOf(`${skill.name} ${skill.code.replace(/[._]/g, ' ')}`);
                let hits = 0;
                for (const t of nameTokens) if (unitTokens.has(t)) hits += 1;
                if (hits) scored.push({ skill, hits });
            }
            scored.sort((a, b) => b.hits - a.hits);
            for (const hit of scored.slice(0, 2)) {
                if (!mapped.has(Number(hit.skill.id))) mapped.set(Number(hit.skill.id), { source: 'auto' });
            }
            unitSkillIndex.push(scored.slice(0, 2).map((h) => Number(h.skill.id)));
        }

        const skillIds = [...mapped.keys()];
        let questionRows = [];
        if (skillIds.length) {
            const placeholders = skillIds.map(() => '?').join(', ');
            questionRows = await query(
                `SELECT skill_id,
                        COUNT(*) AS total,
                        SUM(CASE WHEN course_id = ? THEN 1 ELSE 0 END) AS own
                 FROM qbank_items WHERE live = 1 AND skill_id IN (${placeholders})
                 GROUP BY skill_id`,
                [courseId, ...skillIds]
            );
        }
        const perSkill = new Map(
            questionRows.map((r) => [Number(r.skill_id), { total: Number(r.total || 0), own: Number(r.own || 0) }])
        );
        const covered = skillIds.filter((id) => (perSkill.get(id)?.total || 0) > 0);
        const filled = skillIds.filter((id) => (perSkill.get(id)?.own || 0) === 0 && (perSkill.get(id)?.total || 0) > 0);

        const thinSections = units.filter((u) => u.text.length < PROSE_MIN).map((u) => u.title);
        const simEmbeds = (String(course.content || '').match(/data-sim(?:ulator)?-id=/gi) || []).length;
        const brokenSims = (String(course.content || '').match(/data-sim(?:ulator)?-id=["']\s*["']/gi) || []).length;

        const checks = [
            {
                id: 'units',
                label: 'Has at least 2 teachable units',
                weight: WEIGHTS.units,
                pass: units.length >= 2,
                detail: `${units.length} unit(s)`,
                fix: units.length >= 2 ? null : 'Add <h2> headings, or let the auto-split run.'
            },
            {
                id: 'skills',
                label: 'Maps to at least 3 skills',
                weight: WEIGHTS.skills,
                pass: skillIds.length >= 3,
                detail: `${skillIds.length} skill(s) mapped`,
                fix: skillIds.length >= 3 ? null : 'Name the concepts in your unit headings; the mapper matches skill names.'
            },
            {
                id: 'questions',
                label: 'Every mapped skill has a question',
                weight: WEIGHTS.questions,
                pass: skillIds.length > 0 && covered.length === skillIds.length,
                detail: `${covered.length}/${skillIds.length} skills have items`,
                fix: covered.length === skillIds.length ? null : 'Add your own questions, or let the bank fill the gap (labelled in the session).'
            },
            {
                id: 'prose',
                label: 'Explanations are at least 80 characters',
                weight: WEIGHTS.prose,
                pass: units.length > 0 && thinSections.length === 0,
                detail: thinSections.length ? `too thin: ${thinSections.slice(0, 3).join(', ')}` : 'all sections have prose',
                fix: thinSections.length ? `Write a few sentences in: ${thinSections.slice(0, 3).join(', ')}.` : null
            },
            {
                id: 'sims',
                label: 'No broken simulator embeds',
                weight: WEIGHTS.sims,
                pass: brokenSims === 0,
                detail: simEmbeds ? `${simEmbeds} embed(s), ${brokenSims} broken` : 'no embeds',
                fix: brokenSims ? 'Re-insert the simulator; the session falls back to bank-led until it loads.' : null
            }
        ];

        const score = checks.reduce((sum, c) => sum + (c.pass ? c.weight : 0), 0);
        const passed = score >= READY_PASS;

        if (persist) {
            for (const skillId of skillIds) {
                try {
                    await query(
                        'INSERT IGNORE INTO course_skills (course_id, skill_id, weight, source) VALUES (?, ?, ?, ?)',
                        [courseId, skillId, 1, mapped.get(skillId)?.source || 'auto']
                    );
                } catch (e) {
                    info(`[impact] mapping skipped for course ${courseId}: ${e.message}`);
                }
            }
            try {
                await query('UPDATE courses SET readiness_score = ?, ai_ready = ? WHERE id = ?', [
                    score,
                    passed ? 1 : 0,
                    courseId
                ]);
            } catch (_) {
                /* ai_ready may be absent on an unmigrated database */
            }
        }

        return {
            courseId: Number(courseId),
            title: course.title,
            score,
            passed,
            bankLed: !passed,
            multiplier: readinessMultiplier(score),
            checks,
            units: units.map((u) => ({ ord: u.ord, title: u.title, characters: u.text.length })),
            skills: skillIds.map((id) => {
                const skill = allSkills.find((s) => Number(s.id) === id);
                const counts = perSkill.get(id) || { total: 0, own: 0 };
                return {
                    id,
                    name: skill ? skill.name : `Skill ${id}`,
                    code: skill ? skill.code : null,
                    questions: counts.total,
                    own: counts.own,
                    source: mapped.get(id)?.source || 'auto'
                };
            }),
            filled
        };
    }

    /** The unit's own words, short enough to fit the tutor's prompt budget. */
    function frameFor(unit) {
        const text = String(unit?.text || '').replace(/\s+/g, ' ').trim();
        if (!text) return null;
        return {
            unit: unit.ord,
            title: unit.title,
            digest: text.slice(0, FRAME_CHARS),
            truncated: text.length > FRAME_CHARS
        };
    }

    const LETTERS = 'ABCDEFGH';

    function optionKey(options, correct) {
        const want = String(correct || '').replace(/\s+/g, ' ').trim().toLowerCase();
        if (!want) return null;
        for (const opt of options) {
            if (opt.t.replace(/\s+/g, ' ').trim().toLowerCase() === want) return opt.k;
        }
        // Already a key letter?
        if (want.length === 1 && LETTERS.toLowerCase().includes(want)) {
            const key = want.toUpperCase();
            return options.some((o) => o.k === key) ? key : null;
        }
        return null;
    }

    /**
     * A course whose subject is not in the shared skill bank (AP Calculus, for
     * example) still has its creator's quiz questions. Those are real graded
     * items with answer keys, so they become the practice bank for this course:
     * one synthetic skill per unit, questions ingested into qbank_items once
     * (stem_hash makes it idempotent), and one focus item per unit that carries
     * all of that unit's questions.
     */
    async function ingestCourseQuestions(course, units) {
        let rows;
        try {
            rows = await query(
                `SELECT id, question_text, question_type, options, correct_answer, explanation, difficulty
                 FROM course_questions WHERE course_id = ? ORDER BY order_index, id`,
                [course.id]
            );
        } catch (err) {
            log(`[creator-impact] course_questions unavailable: ${err.message}`);
            return [];
        }
        if (!rows || !rows.length) return [];

        const list = units && units.length ? units : [{ ord: 0, title: course.title, text: '' }];
        const buckets = list.map(() => []);
        const parsed = [];
        rows.forEach((q, i) => {
            let rawOptions = q.options;
            if (typeof rawOptions === 'string') {
                try {
                    rawOptions = JSON.parse(rawOptions);
                } catch (_) {
                    rawOptions = [];
                }
            }
            const options = Array.isArray(rawOptions)
                ? rawOptions.map((o, k) => ({ k: LETTERS[k], t: String(o == null ? '' : o).trim(), why: '' }))
                : [];
            const answer = optionKey(options, q.correct_answer);
            if (!answer) return; // no comparable key: never ship an ungradeable item
            const tier = String(q.difficulty || '').toLowerCase() === 'hard' ? 3
                : String(q.difficulty || '').toLowerCase() === 'medium' ? 2 : 1;
            const stem = String(q.question_text || '').trim();
            if (!stem) return;
            const unitIndex = Math.min(list.length - 1, Math.floor((i * list.length) / rows.length));
            parsed.push({ q, options, answer, tier, stem, unitIndex, explanation: q.explanation || null });
        });
        if (!parsed.length) return [];

        // One synthetic skill per unit so mastery and the focus list stay readable.
        for (const unit of list) {
            const code = `course.${course.id}.u${unit.ord}`;
            await query(
                `INSERT IGNORE INTO skills (code, track, name, grade_band, order_index, dot_target, intro_md, misconceptions)
                 VALUES (?, 'course', ?, ?, ?, 2, ?, '[]')`,
                [
                    code,
                    String(unit.title || course.title).slice(0, 160),
                    course.grade_level != null ? Number(course.grade_level) : null,
                    unit.ord,
                    String(unit.text || '').slice(0, FRAME_CHARS) || null
                ]
            );
        }
        const skillRows = await query(
            `SELECT id, code FROM skills WHERE code LIKE ?`,
            [`course.${course.id}.u%`]
        );
        const skillByCode = new Map(skillRows.map((r) => [r.code, Number(r.id)]));

        const crypto = require('crypto');
        for (const item of parsed) {
            const skillId = skillByCode.get(`course.${course.id}.u${item.unitIndex}`);
            if (!skillId) continue;
            const stemHash = crypto.createHash('sha256').update(item.stem).digest('hex');
            await query(
                `INSERT IGNORE INTO qbank_items
                    (skill_id, tier, qtype, stem, stem_hash, options, answer, hints, solution_steps, source, course_id, live)
                 VALUES (?, ?, 'mcq', ?, ?, ?, ?, NULL, ?, 'course', ?, 1)`,
                [
                    skillId,
                    item.tier,
                    item.stem,
                    stemHash,
                    JSON.stringify(item.options),
                    item.answer,
                    JSON.stringify(item.explanation ? [item.explanation] : []),
                    Number(course.id)
                ]
            );
            const idRow = await query('SELECT id FROM qbank_items WHERE stem_hash = ? LIMIT 1', [stemHash]);
            const questionId = idRow && idRow[0] ? Number(idRow[0].id) : null;
            if (questionId) buckets[item.unitIndex].push({ questionId, tier: item.tier });
        }

        const items = [];
        buckets.forEach((bucket, unitIndex) => {
            if (!bucket.length) return;
            const unit = list[unitIndex];
            items.push({
                ord: items.length,
                skillId: skillByCode.get(`course.${course.id}.u${unit.ord}`),
                skillName: String(unit.title || course.title),
                isReview: 0,
                targetDots: 2,
                startTier: Math.min(...bucket.map((b) => b.tier)),
                unitIndex: unit.ord,
                frame: frameFor(unit),
                // Seed only the first card: the engine serves the last id in the
                // array, then picks the next unseen question for this skill itself.
                questionIds: [bucket[0].questionId]
            });
        });
        return items;
    }

    /**
     * Course plan (§15.2): unit order first, then the weakest skills inside a
     * unit, capped by the time budget the learner picked.
     */
    async function plan({ userId, courseId, minutes }) {
        const course = await loadCourse(courseId);
        if (!course) {
            const err = new Error('Course not found');
            err.status = 404;
            throw err;
        }
        const report = await readiness(courseId, { persist: true });
        const units = splitUnits(course.content);
        const unitSkills = new Map();
        for (const unit of units) {
            const tokens = tokensOf(`${unit.title} ${unit.text}`);
            for (const skill of report.skills) {
                const nameTokens = tokensOf(skill.name);
                let hits = 0;
                for (const t of nameTokens) if (tokens.has(t)) hits += 1;
                if (!hits) continue;
                const prev = unitSkills.get(skill.id);
                if (!prev || hits > prev.hits) unitSkills.set(skill.id, { hits, unit });
            }
        }

        const mastery = require('./mastery');
        const count = Math.max(1, mastery.itemsForMinutes(minutes || 20));
        let masteryRows = [];
        if (report.skills.length) {
            const placeholders = report.skills.map(() => '?').join(', ');
            masteryRows = await query(
                `SELECT skill_id, p, level FROM skill_mastery WHERE user_id = ? AND skill_id IN (${placeholders})`,
                [userId, ...report.skills.map((s) => s.id)]
            );
        }
        const masteryMap = new Map(masteryRows.map((r) => [Number(r.skill_id), { p: Number(r.p || 0), level: Number(r.level || 0) }]));

        // Unit order is the creator's, but inside a unit the weakest skill leads.
        const ordered = report.skills
            .map((skill) => {
                const hit = unitSkills.get(skill.id);
                const m = masteryMap.get(skill.id) || { p: 0, level: 0 };
                return { skill, unitOrd: hit ? hit.unit.ord : 99, unit: hit ? hit.unit : null, p: m.p, level: m.level };
            })
            .filter((row) => !hitIsMastered(row))
            .sort((a, b) => (a.unitOrd - b.unitOrd) || (a.p - b.p));

        let items = ordered.slice(0, count).map((row, i) => ({
            ord: i,
            skillId: row.skill.id,
            skillName: row.skill.name,
            isReview: 0,
            targetDots: 2,
            startTier: row.level >= 2 ? 3 : row.level >= 1 ? 2 : 1,
            unitIndex: row.unit ? row.unit.ord : 0,
            frame: frameFor(row.unit)
        }));

        // The shared bank has no skills for this subject (AP Calculus, say), but
        // the creator's own graded questions still make a real session.
        if (!items.length) {
            items = (await ingestCourseQuestions(course, units)).slice(0, count);
        }

        return { course, report, items };
    }

    function hitIsMastered(row) {
        return row.level >= 4;
    }

    /**
     * Volunteer hours v2, per §15.4. Idempotent per (session, kind) because the
     * ledger has a unique key on it; a refusal is recorded too, so the creator
     * pane can explain a zero.
     */
    async function record({ sessionId, endedAt } = {}) {
        const rows = await query(
            `SELECT s.id, s.user_id, s.course_id, s.mode, s.minutes, s.started_at, s.ended_at, s.rating,
                    s.course_id AS cid
             FROM sessions s WHERE s.id = ? LIMIT 1`,
            [sessionId]
        );
        const session = rows[0];
        if (!session || !session.course_id) return { paid: false, reason: 'no-course', hours: 0 };

        const course = await loadCourse(session.course_id);
        if (!course) return { paid: false, reason: 'no-course', hours: 0 };
        const creatorId = Number(course.creator_id || 0);
        const learnerId = Number(session.user_id);

        // ---- gates that are pure refusals (§15.4 anti-gaming table) --------
        if (!creatorId) {
            return await writeLedger({ course, creatorId: 0, learnerId, sessionId, hours: 0, reason: 'no-creator' });
        }
        if (creatorId === learnerId) {
            return await writeLedger({ course, creatorId, learnerId, sessionId, hours: 0, reason: 'creator-is-learner' });
        }

        const started = new Date(session.started_at || Date.now()).getTime();
        const ended = new Date(session.ended_at || endedAt || Date.now()).getTime();
        const minutes = Math.max(0, Math.round((ended - started) / 60000));
        const itemRows = await query(
            'SELECT COUNT(*) AS c FROM session_focus_items WHERE session_id = ? AND completed_at IS NOT NULL',
            [sessionId]
        );
        const itemsDone = Number(itemRows[0]?.c || 0);
        if (minutes < MIN_MINUTES || itemsDone < MIN_ITEMS) {
            return await writeLedger({
                course,
                creatorId,
                learnerId,
                sessionId,
                hours: 0,
                reason: minutes < MIN_MINUTES ? 'too-short' : 'too-few-items',
                masteryGain: 0
            });
        }

        // ---- multipliers ---------------------------------------------------
        const report = await readiness(course.id, { persist: false });
        const ratingRows = await query(
            'SELECT AVG(rating) AS avg FROM sessions WHERE course_id = ? AND rating IS NOT NULL',
            [course.id]
        );
        const avgRating = Number(ratingRows[0]?.avg || 0);
        const gainRows = await query(
            "SELECT payload FROM session_events WHERE session_id = ? AND kind = 'item.done'",
            [sessionId]
        );
        const gains = gainRows
            .map((row) => parseJson(row.payload, null))
            .filter((p) => p && p.dotsAfter != null && p.dotsBefore != null)
            .map((p) => Number(p.dotsAfter) - Number(p.dotsBefore))
            .filter((n) => Number.isFinite(n));
        const avgGain = gains.length ? gains.reduce((a, b) => a + b, 0) / gains.length : 0;

        const readinessMult = report.multiplier;
        const qualityMult = qualityMultiplier(avgRating);
        const masteryMult = masteryMultiplier(avgGain);
        let hours = SESSION_HOURS * readinessMult * qualityMult * masteryMult;

        // ---- caps ----------------------------------------------------------
        const capped = await capRemaining(creatorId, course.id);
        if (hours > capped.remaining) hours = Math.max(0, capped.remaining);
        if (hours <= 0) {
            return await writeLedger({
                course,
                creatorId,
                learnerId,
                sessionId,
                hours: 0,
                reason: capped.reason || 'capped',
                readinessMult,
                qualityMult,
                masteryMult,
                masteryGain: avgGain
            });
        }

        // ---- the 2-distinct-learners gate, paid retroactively ---------------
        const learners = await eligibleLearners(course.id);
        if (learners.size < MIN_LEARNERS) {
            const written = await writeLedger({
                course,
                creatorId,
                learnerId,
                sessionId,
                hours: 0,
                reason: 'awaiting-second-learner',
                readinessMult,
                qualityMult,
                masteryMult,
                masteryGain: avgGain
            });
            return Object.assign(written, { pendingLearners: MIN_LEARNERS - learners.size });
        }

        const written = await writeLedger({
            course,
            creatorId,
            learnerId,
            sessionId,
            hours: round2(hours),
            reason: 'paid',
            readinessMult,
            qualityMult,
            masteryMult,
            masteryGain: avgGain
        });

        const backfilled = await backfill(course, creatorId);

        // ---- completion bonus ---------------------------------------------
        const completion = await awardCompletion(course, creatorId);

        try {
            await query('UPDATE courses SET sessions_taught = COALESCE(sessions_taught, 0) + 1 WHERE id = ?', [course.id]);
        } catch (_) {
            /* column added by the session schema; absent only on a cold DB */
        }

        return Object.assign(written, { backfilled, completion });
    }

    /** Learners with a session that met the minute/item bar, distinct. */
    async function eligibleLearners(courseId) {
        const rows = await query(
            `SELECT DISTINCT s.user_id
             FROM sessions s
             JOIN session_focus_items f ON f.session_id = s.id AND f.completed_at IS NOT NULL
             WHERE s.course_id = ? AND s.user_id IS NOT NULL
             GROUP BY s.user_id
             HAVING COUNT(*) >= ?`,
            [courseId, MIN_ITEMS]
        );
        return new Set(rows.map((r) => Number(r.user_id)));
    }

    async function capRemaining(creatorId, courseId) {
        const day = await query(
            'SELECT COALESCE(SUM(hours), 0) AS h FROM creator_impact_ledger WHERE creator_id = ? AND created_at >= CURRENT_DATE',
            [creatorId]
        );
        const weekStart = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString().slice(0, 10);
        const week = await query(
            'SELECT COALESCE(SUM(hours), 0) AS h FROM creator_impact_ledger WHERE creator_id = ? AND created_at >= ?',
            [creatorId, weekStart]
        );
        const course = await query(
            'SELECT COALESCE(SUM(hours), 0) AS h FROM creator_impact_ledger WHERE course_id = ? AND kind = ?',
            [courseId, 'session']
        );
        const left = Math.min(
            CAP_DAY - Number(day[0]?.h || 0),
            CAP_WEEK - Number(week[0]?.h || 0),
            CAP_COURSE - Number(course[0]?.h || 0)
        );
        const remaining = Math.max(0, round2(left));
        return { remaining, reason: remaining <= 0 ? 'capped' : null };
    }

    async function writeLedger({ course, creatorId, learnerId, sessionId, hours, reason, readinessMult = 1, qualityMult = 1, masteryMult = 1, masteryGain = 0 }) {
        let inserted = false;
        try {
            const res = await query(
                `INSERT IGNORE INTO creator_impact_ledger
                    (course_id, creator_id, learner_id, session_id, kind, hours, readiness_mult, quality_mult, mastery_mult, mastery_gain, paid_reason)
                 VALUES (?, ?, ?, ?, 'session', ?, ?, ?, ?, ?, ?)`,
                [course.id, creatorId, learnerId, sessionId, round2(hours), readinessMult, qualityMult, masteryMult, masteryGain, reason]
            );
            const header = Array.isArray(res) ? res[0] : res;
            inserted = (header && header.affectedRows ? header.affectedRows : 0) > 0;
        } catch (e) {
            info(`[impact] ledger write failed: ${e.message}`);
            return { paid: false, reason: 'ledger-error', hours: 0 };
        }
        // The ledger's unique key is what makes this idempotent: if the row was
        // already there, this session has been settled and must not pay again.
        if (!inserted) return { paid: false, reason: 'already-settled', hours: 0, sessionId };
        if (hours > 0) await addUserHours(creatorId, hours);
        return { paid: hours > 0, reason, hours: round2(hours), sessionId };
    }

    /** Sessions refused only because the second learner had not arrived yet. */
    async function backfill(course, creatorId) {
        const pending = await query(
            `SELECT * FROM creator_impact_ledger
             WHERE course_id = ? AND kind = 'session' AND hours = 0 AND paid_reason = 'awaiting-second-learner'`,
            [course.id]
        );
        let paid = 0;
        for (const row of pending) {
            const room = await capRemaining(creatorId, course.id);
            if (room.remaining <= 0) break;
            let hours = SESSION_HOURS * Number(row.readiness_mult || 1) * Number(row.quality_mult || 1) * Number(row.mastery_mult || 1);
            hours = Math.min(hours, room.remaining);
            await query('UPDATE creator_impact_ledger SET hours = ?, paid_reason = ? WHERE id = ?', [
                round2(hours),
                'paid-backfill',
                row.id
            ]);
            await addUserHours(creatorId, hours);
            paid += 1;
        }
        return paid;
    }

    /** One hour per distinct learner who reached 80% of the course, max 10. */
    async function awardCompletion(course, creatorId) {
        const rows = await query(
            `SELECT DISTINCT user_id FROM course_enrollment_progress
             WHERE course_id = ? AND progress_percentage >= 80`,
            [course.id]
        );
        const already = await query(
            "SELECT COALESCE(SUM(hours), 0) AS h, COUNT(*) AS c FROM creator_impact_ledger WHERE course_id = ? AND kind = 'completion'",
            [course.id]
        );
        let granted = Number(already[0]?.c || 0);
        let hours = 0;
        for (const row of rows) {
            if (granted >= COMPLETION_MAX) break;
            const learnerId = Number(row.user_id);
            if (learnerId === creatorId) continue;
            const existing = await query(
                "SELECT id FROM creator_impact_ledger WHERE course_id = ? AND kind = 'completion' AND learner_id = ? LIMIT 1",
                [course.id, learnerId]
            );
            if (existing.length) continue;
            const room = await capRemaining(creatorId, course.id);
            const pay = Math.min(COMPLETION_HOURS, room.remaining);
            if (pay <= 0) break;
            await query(
                `INSERT IGNORE INTO creator_impact_ledger
                    (course_id, creator_id, learner_id, session_id, kind, hours, paid_reason)
                 VALUES (?, ?, ?, 0, 'completion', ?, 'paid-completion')`,
                [course.id, creatorId, learnerId, round2(pay)]
            );
            await addUserHours(creatorId, pay);
            granted += 1;
            hours += pay;
        }
        return round2(hours);
    }

    async function addUserHours(userId, hours) {
        if (!(hours > 0)) return;
        try {
            await query('UPDATE users SET total_volunteer_hours = COALESCE(total_volunteer_hours, 0) + ? WHERE id = ?', [
                round2(hours),
                userId
            ]);
        } catch (e) {
            info(`[impact] hours update skipped: ${e.message}`);
        }
    }

    /** The creator pane (§15.5): the ledger, the funnel and where learners stall. */
    async function impact(courseId) {
        const course = await loadCourse(courseId);
        if (!course) {
            const err = new Error('Course not found');
            err.status = 404;
            throw err;
        }
        const totals = await query(
            `SELECT COALESCE(SUM(hours), 0) AS hours,
                    COUNT(DISTINCT learner_id) AS learners,
                    AVG(NULLIF(mastery_gain, 0)) AS gain,
                    SUM(CASE WHEN hours > 0 THEN 1 ELSE 0 END) AS paid_sessions,
                    SUM(CASE WHEN hours = 0 THEN 1 ELSE 0 END) AS refused_sessions
             FROM creator_impact_ledger WHERE course_id = ?`,
            [courseId]
        );
        const ratingRows = await query(
            'SELECT AVG(rating) AS avg, COUNT(rating) AS n FROM sessions WHERE course_id = ? AND rating IS NOT NULL',
            [courseId]
        );
        const stuck = await query(
            `SELECT sk.id, sk.name,
                    SUM(CASE WHEN a.correct = 0 THEN 1 ELSE 0 END) AS misses,
                    COUNT(*) AS attempts
             FROM practice_attempts a
             JOIN skills sk ON sk.id = a.skill_id
             JOIN course_skills cs ON cs.skill_id = a.skill_id AND cs.course_id = ?
             GROUP BY sk.id, sk.name
             HAVING SUM(CASE WHEN a.correct = 0 THEN 1 ELSE 0 END) > 0
             ORDER BY misses DESC LIMIT 5`,
            [courseId]
        );
        const funnelRows = await query(
            `SELECT
                COUNT(*) AS started,
                SUM(CASE WHEN progress_percentage >= 50 THEN 1 ELSE 0 END) AS half,
                SUM(CASE WHEN progress_percentage >= 80 THEN 1 ELSE 0 END) AS eighty,
                SUM(CASE WHEN completed = TRUE OR progress_percentage >= 100 THEN 1 ELSE 0 END) AS finished
             FROM course_enrollment_progress WHERE course_id = ?`,
            [courseId]
        );
        const ledger = await query(
            `SELECT id, learner_id, session_id, kind, hours, paid_reason, mastery_gain, created_at
             FROM creator_impact_ledger WHERE course_id = ? ORDER BY id DESC LIMIT 50`,
            [courseId]
        );

        const t = totals[0] || {};
        return {
            courseId: Number(courseId),
            title: course.title,
            learners: Number(t.learners || 0),
            hours: round2(t.hours || 0),
            avgGain: round2(t.gain || 0),
            rating: round2(ratingRows[0]?.avg || 0),
            ratingCount: Number(ratingRows[0]?.n || 0),
            paidSessions: Number(t.paid_sessions || 0),
            refusedSessions: Number(t.refused_sessions || 0),
            stuck: stuck.map((r) => ({
                skillId: Number(r.id),
                name: r.name,
                misses: Number(r.misses || 0),
                attempts: Number(r.attempts || 0)
            })),
            funnel: {
                started: Number(funnelRows[0]?.started || 0),
                half: Number(funnelRows[0]?.half || 0),
                eighty: Number(funnelRows[0]?.eighty || 0),
                finished: Number(funnelRows[0]?.finished || 0)
            },
            ledger: ledger.map((r) => ({
                id: Number(r.id),
                learnerId: Number(r.learner_id),
                sessionId: Number(r.session_id),
                kind: r.kind,
                hours: round2(r.hours),
                reason: r.paid_reason,
                masteryGain: round2(r.mastery_gain),
                createdAt: r.created_at
            }))
        };
    }

    /** Every course a creator owns, with the numbers the dashboard shows. */
    async function summaryForCreator(creatorId) {
        const courses = await query(
            'SELECT id, title, readiness_score FROM courses WHERE creator_id = ? ORDER BY id DESC LIMIT 50',
            [creatorId]
        );
        const out = [];
        let hours = 0;
        for (const course of courses) {
            const rows = await query(
                `SELECT COALESCE(SUM(hours), 0) AS h, COUNT(DISTINCT learner_id) AS learners, AVG(NULLIF(mastery_gain, 0)) AS gain
                 FROM creator_impact_ledger WHERE course_id = ?`,
                [course.id]
            );
            const row = rows[0] || {};
            hours += Number(row.h || 0);
            out.push({
                courseId: Number(course.id),
                title: course.title,
                readiness: Number(course.readiness_score || 0),
                learners: Number(row.learners || 0),
                hours: round2(row.h || 0),
                avgGain: round2(row.gain || 0)
            });
        }
        return { courses: out, hours: round2(hours) };
    }

    return { readiness, plan, impact, record, summaryForCreator, splitUnits, frameFor };
}

module.exports = createCreatorImpact;
module.exports.splitUnits = splitUnits;
module.exports.stripHtml = stripHtml;
module.exports.WEIGHTS = WEIGHTS;
module.exports.READY_PASS = READY_PASS;
module.exports.constants = {
    SESSION_HOURS,
    COMPLETION_HOURS,
    COMPLETION_MAX,
    CAP_DAY,
    CAP_WEEK,
    CAP_COURSE,
    MIN_LEARNERS,
    MIN_MINUTES,
    MIN_ITEMS
};
