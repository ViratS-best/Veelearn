'use strict';

/**
 * Outline + question-bank endpoints for the creator and the session planner.
 *
 *   POST /api/outlines                         start a map (no course body)
 *   POST /api/outlines/:courseId/submit        send the map for superadmin review
 *   GET  /api/courses/:courseId/outline        the saved map (creator or learner)
 *   PUT  /api/courses/:courseId/outline        creator saves the map
 *   GET  /api/question-bank/search?q=...       questions (with diagrams) to pull in
 */

const express = require('express');
const courseQuality = require('./course-quality');
const embeddings = require('./embeddings');

module.exports = function createOutlineRoutes({ query, authenticateToken, writeLimiter, log }) {
    const router = express.Router();
    const createOutlines = require('./outline');
    const outlines = createOutlines({ query, log });
    embeddings.configure({ query, log });

    const cleanTitle = (v) => String(v == null ? '' : v).replace(/\s+/g, ' ').trim().slice(0, 160);

    /**
     * An outline is the thing a creator makes. There is no course body to write:
     * the row exists so the map, the sessions built from it and the review queue
     * all hang off one id, and it starts as a private draft.
     */
    router.post('/api/outlines', authenticateToken, writeLimiter, async (req, res) => {
        try {
            const body = req.body || {};
            const title = cleanTitle(body.title);
            if (!title) return res.status(400).json({ success: false, message: 'Give the outline a title first' });
            // "a", "test", "Outline Test 1794761977545": these used to be saved and
            // then recommended to learners. Refuse them at the door.
            if (courseQuality.isTestTitle(title)) {
                return res.status(400).json({
                    success: false,
                    message: 'Give the outline a real title — a placeholder like "test" or "a" cannot be published.'
                });
            }
            const description = String(body.description || '').trim().slice(0, 600);
            const rawGrade = Number(body.gradeLevel != null ? body.gradeLevel : body.grade_level);
            const gradeLevel = Number.isFinite(rawGrade) && rawGrade >= 1 && rawGrade <= 13 ? Math.round(rawGrade) : null;

            const created = await query(
                `INSERT INTO courses (title, description, content, blocks, creator_id, status, creation_time, grade_level, course_type)
                 VALUES (?, ?, '', '[]', ?, 'draft', 0, ?, 'single')`,
                [title, description, req.user.id, gradeLevel]
            );
            const courseId = Number((created && created.insertId) || 0);
            if (!courseId) throw new Error('the outline row was not created');
            try {
                await query('INSERT INTO course_outlines (course_id, outline_json) VALUES (?, ?)', [
                    courseId,
                    JSON.stringify({ version: 1, units: [] })
                ]);
            } catch (err) {
                // The map is created lazily by the first save if this insert loses a race.
                if (log && log.warn) log.warn(`[outline] empty map not pre-created: ${err.message}`);
            }
            res.status(201).json({
                success: true,
                message: 'Outline created',
                data: { id: courseId, title, description, status: 'draft' }
            });
        } catch (err) {
            res.status(500).json({ success: false, message: 'Could not create the outline', error: err.message });
        }
    });

    /**
     * Submission is the only gate: the same review queue and the same approve /
     * reject endpoint a course used, so a superadmin sees an outline exactly
     * where they used to see a course.
     */
    router.post('/api/outlines/:courseId/submit', authenticateToken, writeLimiter, async (req, res) => {
        try {
            const courseId = Number(req.params.courseId);
            const rows = await query('SELECT id, creator_id, status FROM courses WHERE id = ? LIMIT 1', [courseId]);
            if (!rows.length) return res.status(404).json({ success: false, message: 'Outline not found' });
            if (Number(rows[0].creator_id) !== Number(req.user.id)) {
                return res.status(403).json({ success: false, message: 'You can only submit your own outline' });
            }
            const status = String(rows[0].status || 'draft');
            if (status === 'pending') return res.status(400).json({ success: false, message: 'This outline is already waiting for review' });
            if (status === 'approved') return res.status(400).json({ success: false, message: 'This outline is already approved' });

            const outline = (await outlines.load(courseId)) || { units: [] };
            const units = Array.isArray(outline.units) ? outline.units.length : 0;
            const skills = outlines.skillCount(outline);
            const questions = outlines.questionCount(outline);
            if (!units) return res.status(400).json({ success: false, message: 'Add at least one unit page before submitting' });
            if (!skills) return res.status(400).json({ success: false, message: 'Add at least one skill circle before submitting' });
            if (questions < 3) {
                return res.status(400).json({ success: false, message: 'Put at least three questions in the map before submitting' });
            }

            await query("UPDATE courses SET status = 'pending', feedback = NULL WHERE id = ?", [courseId]);
            res.json({
                success: true,
                message: 'Outline submitted for approval',
                data: { status: 'pending', units, skills, questions }
            });
        } catch (err) {
            res.status(500).json({ success: false, message: 'Could not submit the outline', error: err.message });
        }
    });

    router.get('/api/courses/:courseId/outline', authenticateToken, async (req, res) => {
        try {
            const courseId = Number(req.params.courseId);
            const rows = await query('SELECT id, creator_id, title, status, feedback FROM courses WHERE id = ? LIMIT 1', [courseId]);
            if (!rows.length) return res.status(404).json({ success: false, message: 'Course not found' });
            const outline = (await outlines.load(courseId)) || { version: 1, units: [] };
            res.json({
                success: true,
                data: {
                    courseId,
                    title: rows[0].title,
                    // Review state travels with the map, so the creator can see a
                    // rejection reason without opening the dashboard.
                    status: String(rows[0].status || 'draft'),
                    feedback: rows[0].feedback || '',
                    canEdit: Number(rows[0].creator_id) === Number(req.user.id),
                    outline,
                    skills: outlines.skillCount(outline),
                    questions: outlines.questionCount(outline)
                }
            });
        } catch (err) {
            res.status(500).json({ success: false, message: 'Could not load the outline', error: err.message });
        }
    });

    router.put('/api/courses/:courseId/outline', authenticateToken, writeLimiter, async (req, res) => {
        try {
            const courseId = Number(req.params.courseId);
            const rows = await query('SELECT id, creator_id FROM courses WHERE id = ? LIMIT 1', [courseId]);
            if (!rows.length) return res.status(404).json({ success: false, message: 'Course not found' });
            if (Number(rows[0].creator_id) !== Number(req.user.id)) {
                return res.status(403).json({ success: false, message: 'You can only edit your own outline' });
            }
            // Volunteer hours are granted by the existing course save path; this
            // endpoint only stores the map, so the creator ledger stays untouched.
            const saved = await outlines.save(courseId, req.body && req.body.outline ? req.body.outline : req.body);
            res.json({
                success: true,
                message: 'Outline saved',
                data: { outline: saved, skills: outlines.skillCount(saved), questions: outlines.questionCount(saved) }
            });
        } catch (err) {
            res.status(500).json({ success: false, message: 'Could not save the outline', error: err.message });
        }
    });

    router.get('/api/question-bank/search', authenticateToken, async (req, res) => {
        try {
            const q = String(req.query.q || '').trim();
            const limit = Math.min(30, Math.max(1, parseInt(req.query.limit, 10) || 12));
            // Postgres LIKE is case-sensitive, so "stars" would miss "Stars
            // are". Lower both sides (portable across MySQL and Postgres).
            const like = `%${q.replace(/[%_]/g, '').toLowerCase()}%`;
            const columns = `q.id, q.stem, q.options, q.answer, q.hints, q.solution_steps, q.visual,
                             q.source, q.attribution, s.name AS skill_name`;

            let rows = null;
            let semantic = false;
            if (q) {
                const vector = await embeddings.embedQuery(q).catch(() => null);
                if (vector) {
                    try {
                        // Two candidate sets: the nearest 150 vectors and the 150
                        // keyword hits. The outer score is what the user sees.
                        rows = await query(
                            `WITH vec AS (
                                 SELECT id, (1 - (embedding <=> ?::${embeddings.state.column})) AS sim
                                   FROM qbank_items
                                  WHERE live = 1 AND embedding IS NOT NULL
                                  ORDER BY embedding <=> ?::${embeddings.state.column}
                                  LIMIT 150
                             ), kw AS (
                                 SELECT q.id
                                   FROM qbank_items q
                                   LEFT JOIN skills s ON s.id = q.skill_id
                                  WHERE q.live = 1 AND (LOWER(q.stem) LIKE ? OR LOWER(s.name) LIKE ?)
                                  LIMIT 150
                             )
                             SELECT ${columns},
                                    COALESCE(v.sim, 0) AS similarity,
                                    CASE WHEN k.id IS NULL THEN 0 ELSE 1 END AS keyword_hit,
                                    (COALESCE(v.sim, 0) * 0.72 +
                                     (CASE WHEN k.id IS NULL THEN 0 ELSE 1 END) * 0.28) AS score
                               FROM qbank_items q
                               LEFT JOIN skills s ON s.id = q.skill_id
                               LEFT JOIN vec v ON v.id = q.id
                               LEFT JOIN kw k ON k.id = q.id
                              WHERE q.live = 1 AND (v.id IS NOT NULL OR k.id IS NOT NULL)
                              ORDER BY score DESC, q.id DESC
                              LIMIT ?`,
                            [vector, vector, like, like, limit]
                        );
                        semantic = true;
                    } catch (err) {
                        if (log && log.warn) log.warn(`[qbank] hybrid search fell back: ${err.message}`);
                        rows = null;
                    }
                }
            }

            if (!rows) {
                const params = [];
                let where = 'WHERE q.live = 1';
                if (q) {
                    where += ' AND (LOWER(q.stem) LIKE ? OR LOWER(s.name) LIKE ?)';
                    params.push(like, like);
                }
                rows = await query(
                    `SELECT ${columns}
                     FROM qbank_items q
                     LEFT JOIN skills s ON s.id = q.skill_id
                     ${where}
                     ORDER BY q.id DESC
                     LIMIT ${limit}`,
                    params
                );
            }
            const data = rows.map((row) => {
                const parse = (v, f) => {
                    if (v == null) return f;
                    if (typeof v === 'object') return v;
                    try {
                        return JSON.parse(String(v));
                    } catch (_) {
                        return f;
                    }
                };
                return {
                    id: Number(row.id),
                    skill: row.skill_name || '',
                    stem: row.stem,
                    options: parse(row.options, []).map((o) => ({ k: o.k, t: o.t })),
                    answer: row.answer,
                    hint: (parse(row.hints, []) || [])[0] || '',
                    why: (parse(row.solution_steps, []) || [])[0] || '',
                    visual: parse(row.visual, null),
                    // Provenance, so a creator can see where a pulled question
                    // came from before they put it in their outline.
                    source: row.source || 'authored',
                    attribution: row.attribution || '',
                    // Present only on the hybrid path; the picker ignores them.
                    similarity: row.similarity == null ? null : Number(Number(row.similarity).toFixed(4)),
                    match: semantic ? (Number(row.keyword_hit) ? 'semantic+keyword' : 'semantic') : 'keyword'
                };
            });
            res.json({ success: true, data, semantic });
        } catch (err) {
            res.status(500).json({ success: false, message: 'Question bank unavailable', error: err.message });
        }
    });

    return router;
};
