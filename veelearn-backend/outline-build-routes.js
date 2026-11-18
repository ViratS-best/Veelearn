'use strict';

/**
 * Superadmin batch conversion of approved courses into outlines.
 *
 *   GET  /api/admin/outlines/progress          how much of the catalog is mapped
 *   POST /api/admin/outlines/build             build + save the next batch
 *
 * The builder lives in `outline-builder.js` and the map shape in `outline.js`,
 * so this route only loads rows, calls the builder and saves. Batches keep one
 * request short enough for the host's request timeout; the caller loops until
 * `remaining` is zero.
 */

const express = require('express');
const { aiChatCompletion } = require('./ai-chat');

// Fast, non-reasoning model: question writing needs an answer, not a monologue.
const FILL_MODEL = String(process.env.VEELEARN_OUTLINE_MODEL || '').trim() || 'google/gemini-3.5-flash-lite';
const FILL_MIN = 3;

function parseObject(text) {
    const raw = String(text || '').trim();
    if (!raw) return null;
    const fenced = /```(?:json)?\s*([\s\S]*?)```/i.exec(raw);
    const candidates = [fenced && fenced[1], raw].filter(Boolean);
    for (const source of candidates) {
        const src = source.trim();
        try {
            const value = JSON.parse(src);
            if (value && typeof value === 'object') return value;
        } catch (_) {
            /* scan for the first balanced object below */
        }
        const at = src.indexOf('{');
        if (at < 0) continue;
        let depth = 0;
        let inString = false;
        let escaped = false;
        for (let i = at; i < src.length; i += 1) {
            const ch = src[i];
            if (inString) {
                if (escaped) escaped = false;
                else if (ch === '\\') escaped = true;
                else if (ch === '"') inString = false;
                continue;
            }
            if (ch === '"') {
                inString = true;
                continue;
            }
            if (ch === '{') depth += 1;
            else if (ch === '}') {
                depth -= 1;
                if (depth === 0) {
                    try {
                        const value = JSON.parse(src.slice(at, i + 1));
                        if (value && typeof value === 'object') return value;
                    } catch (_) {
                        /* keep looking */
                    }
                    break;
                }
            }
        }
    }
    return null;
}

const normStem = (s) =>
    String(s || '')
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, ' ')
        .trim();

module.exports = function createOutlineBuildRoutes({ query, authenticateToken, log }) {
    const router = express.Router();
    const createOutlines = require('./outline');
    const outlines = createOutlines({ query, log });
    const builder = require('./outline-builder');

    const isAdmin = (req) => req.user && req.user.role === 'superadmin';
    const isStub = (course) => String(course.content || '').length < 1000;

    router.get('/api/admin/outlines/progress', authenticateToken, async (req, res) => {
        if (!isAdmin(req)) return res.status(403).json({ success: false, message: 'Superadmin only' });
        try {
            const rows = await query(
                `SELECT c.id, c.title, LENGTH(c.content) AS content_length,
                        (SELECT COUNT(*) FROM course_outlines o WHERE o.course_id = c.id) AS mapped
                 FROM courses c WHERE c.status = 'approved' ORDER BY c.id`
            );
            const mapped = rows.filter((r) => Number(r.mapped) > 0);
            let stats = null;
            if (String(req.query.deep || '') === '1') {
                stats = { units: 0, skills: 0, questions: 0, emptySkills: 0, thinSkills: 0, thinCourses: [] };
                for (const row of mapped) {
                    const outline = await outlines.load(row.id);
                    if (!outline) continue;
                    const s = builder.stats(outline);
                    stats.units += s.units;
                    stats.skills += s.skills;
                    stats.questions += s.questions;
                    stats.emptySkills += s.emptySkills;
                    stats.thinSkills += s.thinSkills;
                    if (s.thinSkills) stats.thinCourses.push({ id: Number(row.id), title: row.title, thin: s.thinSkills, empty: s.emptySkills });
                }
            }
            res.json({
                success: true,
                data: {
                    approved: rows.length,
                    mapped: mapped.length,
                    missing: rows.length - mapped.length,
                    stubs: rows.filter((r) => Number(r.content_length || 0) < 1000).length,
                    stats,
                    courses: rows.map((r) => ({
                        id: Number(r.id),
                        title: r.title,
                        stub: Number(r.content_length || 0) < 1000,
                        mapped: Number(r.mapped) > 0
                    }))
                }
            });
        } catch (err) {
            res.status(500).json({ success: false, message: 'Could not read progress', error: err.message });
        }
    });

    router.post('/api/admin/outlines/build', authenticateToken, async (req, res) => {
        if (!isAdmin(req)) return res.status(403).json({ success: false, message: 'Superadmin only' });
        const body = req.body || {};
        const force = Boolean(body.force);
        const mode = body.mode === 'stubs' ? 'stubs' : 'courses';
        const limit = Math.min(25, Math.max(1, Number(body.limit) || 8));

        try {
            const all = await query(
                `SELECT c.id, c.title, c.description, c.content, c.grade_level,
                        (SELECT COUNT(*) FROM course_outlines o WHERE o.course_id = c.id) AS mapped
                 FROM courses c WHERE c.status = 'approved' ORDER BY c.id`
            );
            const stubRows = all.filter(isStub);
            let targets = mode === 'stubs' ? stubRows : all.filter((c) => !isStub(c));
            if (!force) targets = targets.filter((c) => !Number(c.mapped));
            if (Array.isArray(body.ids) && body.ids.length) {
                const wanted = new Set(body.ids.map(Number));
                targets = targets.filter((c) => wanted.has(Number(c.id)));
            }

            const batch = targets.slice(0, limit);
            const remaining = Math.max(0, targets.length - batch.length);

            // Sibling assembly needs the unit courses and their questions; only
            // load that catalog when a stub is actually in this batch.
            let siblingPool = null;
            const needsSiblings = batch.some(isStub);
            if (needsSiblings) {
                const support = await query(
                    `SELECT id, title, content, description, grade_level FROM courses
                     WHERE status = 'approved' AND LENGTH(content) > 1000 ORDER BY id`
                );
                const ids = support.map((r) => Number(r.id));
                const qrows = ids.length
                    ? await query(
                          `SELECT course_id, question_text, options, correct_answer, explanation
                           FROM course_questions WHERE course_id IN (${ids.map(() => '?').join(',')})
                           ORDER BY course_id, order_index, id`,
                          ids
                      )
                    : [];
                const byCourse = new Map();
                for (const q of qrows) {
                    const key = Number(q.course_id);
                    if (!byCourse.has(key)) byCourse.set(key, []);
                    byCourse.get(key).push(q);
                }
                siblingPool = support.map((s) => ({ ...s, questions: byCourse.get(Number(s.id)) || [] }));
            }

            const built = [];
            const failed = [];
            for (const course of batch) {
                try {
                    const questions = await query(
                        `SELECT question_text, options, correct_answer, explanation
                         FROM course_questions WHERE course_id = ? ORDER BY order_index, id`,
                        [course.id]
                    );
                    const shaped = { ...course, questions };
                    let outline = builder.outlineForCourse(shaped);
                    let how = 'course';
                    if ((!outline || outline.units.length < 2) && siblingPool) {
                        const assembled = builder.assembleFromSiblings(shaped, siblingPool);
                        if (assembled) {
                            outline = assembled;
                            how = 'siblings';
                        }
                    }
                    if (!outline || !outline.units.length) {
                        failed.push({ id: Number(course.id), title: course.title, reason: 'no usable structure' });
                        continue;
                    }
                    const saveable = siblingPool ? outline : outline;
                    const saved = await outlines.save(course.id, saveable);
                    const stats = builder.stats(saved);
                    built.push({ id: Number(course.id), title: course.title, how, ...stats });
                    if (log && log.info) log.info(`[outline.build] ${course.id} ${course.title}: ${stats.skills} skills, ${stats.questions} questions`);
                } catch (err) {
                    failed.push({ id: Number(course.id), title: course.title, reason: err.message });
                    if (log && log.warn) log.warn(`[outline.build] ${course.id} failed: ${err.message}`);
                }
            }

            res.json({
                success: true,
                data: {
                    mode,
                    built,
                    failed,
                    remaining,
                    done: targets.length - remaining
                }
            });
        } catch (err) {
            res.status(500).json({ success: false, message: 'Could not build outlines', error: err.message });
        }
    });

    /**
     * Ask the model for the questions a skill is missing.
     *
     * Only gaps are generated (skills below three questions), so the course's
     * own authored questions always win. Every generated item is validated: four
     * options, an answer letter that exists, and no duplicate stem.
     */
    router.post('/api/admin/outlines/fill', authenticateToken, async (req, res) => {
        if (!isAdmin(req)) return res.status(403).json({ success: false, message: 'Superadmin only' });
        const body = req.body || {};
        const limit = Math.min(6, Math.max(1, Number(body.limit) || 2));
        const ids = Array.isArray(body.ids) ? body.ids.map(Number).filter(Boolean) : [];
        const afterId = Number(body.afterId) || 0;

        try {
            const all = await query(
                `SELECT id, title, grade_level FROM courses WHERE status = 'approved' ORDER BY id`
            );
            const pool = ids.length ? all.filter((c) => ids.includes(Number(c.id))) : all;
            // Courses that still have a skill below the three-question floor.
            const work = [];
            for (const course of pool) {
                const outline = await outlines.load(course.id);
                if (!outline || !outline.units.length) continue;
                const gaps = [];
                for (const unit of outline.units) {
                    for (const skill of unit.skills) {
                        if (skill.questions.length < FILL_MIN) {
                            gaps.push({
                                skill,
                                need: FILL_MIN - skill.questions.length,
                                existing: skill.questions.map((q) => q.stem).slice(0, 3)
                            });
                        }
                    }
                }
                if (gaps.length) work.push({ course, outline, gaps });
            }
            // A cursor keeps progress stable while courses drop out of the list.
            const ahead = work.filter((w) => Number(w.course.id) > afterId);
            const batch = ahead.slice(0, limit);

            const filled = [];
            const failed = [];
            for (const item of batch) {
                const { course, outline, gaps } = item;
                // A short list keeps the reply inside the token budget; a course
                // with many thin skills comes back on a later pass.
                const list = gaps
                    .slice(0, 5)
                    .map(
                        (g, i) =>
                            `${i + 1}. ${g.skill.name} — need ${g.need}. Teaching brief: ${String(g.skill.teach || '').slice(0, 380)}` +
                            (g.existing.length ? ` Existing stems (do not repeat): ${g.existing.join(' | ')}` : '')
                    )
                    .join('\n');
                const messages = [
                    {
                        role: 'system',
                        content:
                            'You write original multiple-choice questions for Veelearn, an adaptive tutor. ' +
                            'Never copy a textbook, contest or exam question. Each question has exactly four options, ' +
                            'one correct answer, three plausible distractors aimed at common slips, a one-sentence hint, ' +
                            'and a short explanation of why the answer is right. Vary the correct letter. ' +
                            'Match the course level and keep the wording plain. ' +
                            'Return ONLY JSON: {"questions":[{"skill":"exact skill name","stem":"...","options":["...","...","...","..."],"answer":"A","hint":"...","why":"..."}]}'
                    },
                    {
                        role: 'user',
                        content:
                            `Course: ${course.title}${course.grade_level ? ` (grade ${course.grade_level})` : ''}.\n` +
                            `Write the missing questions for these skills:\n${list}`
                    }
                ];
                try {
                    const ask = async (extra) =>
                        aiChatCompletion(extra ? messages.concat([{ role: 'user', content: extra }]) : messages, {
                            model: FILL_MODEL,
                            max_tokens: 5000,
                            temperature: extra ? 0.3 : 0.5,
                            budgetMs: 120000,
                            jsonMust: true
                        });
                    let text = await ask('');
                    let parsed = parseObject(text);
                    if (!parsed) {
                        // One compact retry: a reasoning model can answer with prose.
                        text = await ask('Return ONLY the JSON object {"questions":[...]}. No prose, no fences.');
                        parsed = parseObject(text);
                    }
                    if (!parsed) {
                        // A second model occasionally reads the constraint better.
                        try {
                            text = await aiChatCompletion(messages, {
                                model: 'google/gemma-4-26b-a4b-it',
                                max_tokens: 4000,
                                temperature: 0.2,
                                budgetMs: 120000,
                                jsonMust: true
                            });
                            parsed = parseObject(text);
                        } catch (_) {
                            /* keep the earlier failure */
                        }
                    }
                    if (!parsed) {
                        failed.push({ id: Number(course.id), reason: 'unparseable reply' });
                        continue;
                    }
                    const rows = Array.isArray(parsed.questions)
                        ? parsed.questions
                        : Array.isArray(parsed)
                          ? parsed
                          : Array.isArray(parsed.items)
                            ? parsed.items
                            : [];

                    const byName = new Map();
                    for (const unit of outline.units) {
                        for (const skill of unit.skills) byName.set(normStem(skill.name), skill);
                    }
                    const asked = gaps.slice(0, 5).map((g) => g.skill);
                    /** Exact name, then word overlap, then the first skill still short. */
                    const pickSkill = (label) => {
                        const key = normStem(label);
                        const exact = byName.get(key);
                        if (exact && exact.questions.length < FILL_MIN) return exact;
                        const labelTokens = builder.tokenSet(label);
                        let best = null;
                        let bestScore = 0;
                        for (const candidate of asked) {
                            if (candidate.questions.length >= FILL_MIN) continue;
                            const score = builder.overlap(labelTokens, builder.tokenSet(candidate.name));
                            if (score > bestScore) {
                                bestScore = score;
                                best = candidate;
                            }
                        }
                        if (best) return best;
                        return asked.find((s) => s.questions.length < FILL_MIN) || null;
                    };
                    let added = 0;
                    for (const raw of rows) {
                        if (!raw || typeof raw !== 'object') continue;
                        const skill = pickSkill(raw.skill || raw.skillName || raw.topic || '');
                        if (!skill || skill.questions.length >= FILL_MIN) continue;
                        const options = (Array.isArray(raw.options)
                            ? raw.options
                            : Array.isArray(raw.choices)
                              ? raw.choices
                              : Array.isArray(raw.answers)
                                ? raw.answers
                                : []
                        )
                            .map((o, i) => ({
                                k: 'ABCD'[i],
                                t: String(o && typeof o === 'object' ? o.t || o.text || o.label || '' : o || '')
                                    .trim()
                                    .slice(0, 300)
                            }))
                            .filter((o) => o.t);
                        if (options.length !== 4) continue;
                        const wanted = String(raw.answer != null ? raw.answer : raw.correct || '')
                            .trim()
                            .toLowerCase()
                            .replace(/^([a-d])\s*[).:-]\s+/, '$1')
                            .replace(/^option\s+/i, '');
                        let index = options.findIndex((o) => o.t.toLowerCase() === wanted);
                        if (index < 0 && /^[a-d]$/.test(wanted)) index = 'abcd'.indexOf(wanted);
                        if (index < 0 && /^[0-3]$/.test(wanted)) index = Number(wanted);
                        if (index < 0) continue;
                        const stem = String(raw.stem || raw.question || raw.prompt || '').trim().slice(0, 1200);
                        if (stem.length < 12) continue;
                        if (skill.questions.some((q) => normStem(q.stem) === normStem(stem))) continue;
                        skill.questions.push({
                            id: `ai${skill.questions.length + 1}`,
                            stem,
                            options,
                            answer: options[index].k,
                            hint: String(raw.hint || '').trim().slice(0, 400),
                            why: String(raw.why || raw.explanation || '').trim().slice(0, 700),
                            visual: null,
                            bankId: null,
                            source: 'authored',
                            attribution: ''
                        });
                        added += 1;
                    }
                    if (!added) {
                        failed.push({ id: Number(course.id), reason: 'no valid questions in reply' });
                        continue;
                    }
                    const saved = await outlines.save(course.id, outline);
                    filled.push({ id: Number(course.id), title: course.title, added, ...builder.stats(saved) });
                    if (log && log.info) log.info(`[outline.fill] ${course.id}: +${added} questions`);
                } catch (err) {
                    failed.push({ id: Number(course.id), reason: err.message });
                    if (log && log.warn) log.warn(`[outline.fill] ${course.id} failed: ${err.message}`);
                }
            }

            const lastId = batch.length ? Number(batch[batch.length - 1].course.id) : afterId;
            res.json({
                success: true,
                data: {
                    filled,
                    failed,
                    processed: batch.length,
                    total: ahead.length,
                    nextId: lastId,
                    remaining: Math.max(0, ahead.length - batch.length)
                }
            });
        } catch (err) {
            res.status(500).json({ success: false, message: 'Could not fill outlines', error: err.message });
        }
    });

    return router;
};
