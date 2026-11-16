'use strict';

/**
 * Outline + question-bank endpoints for the creator and the session planner.
 *
 *   GET  /api/courses/:courseId/outline        the saved map (creator or learner)
 *   PUT  /api/courses/:courseId/outline        creator saves the map
 *   GET  /api/question-bank/search?q=...       questions (with diagrams) to pull in
 */

const express = require('express');

module.exports = function createOutlineRoutes({ query, authenticateToken, writeLimiter, log }) {
    const router = express.Router();
    const createOutlines = require('./outline');
    const outlines = createOutlines({ query, log });

    router.get('/api/courses/:courseId/outline', authenticateToken, async (req, res) => {
        try {
            const courseId = Number(req.params.courseId);
            const rows = await query('SELECT id, creator_id, title FROM courses WHERE id = ? LIMIT 1', [courseId]);
            if (!rows.length) return res.status(404).json({ success: false, message: 'Course not found' });
            const outline = (await outlines.load(courseId)) || { version: 1, units: [] };
            res.json({
                success: true,
                data: {
                    courseId,
                    title: rows[0].title,
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
            const params = [];
            let where = 'WHERE q.live = 1';
            if (q) {
                where += ' AND (q.stem LIKE ? OR s.name LIKE ?)';
                const like = `%${q.replace(/[%_]/g, '')}%`;
                params.push(like, like);
            }
            const rows = await query(
                `SELECT q.id, q.stem, q.options, q.answer, q.hints, q.solution_steps, q.visual,
                        q.source, q.attribution, s.name AS skill_name
                 FROM qbank_items q
                 LEFT JOIN skills s ON s.id = q.skill_id
                 ${where}
                 ORDER BY q.id DESC
                 LIMIT ${limit}`,
                params
            );
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
                    attribution: row.attribution || ''
                };
            });
            res.json({ success: true, data });
        } catch (err) {
            res.status(500).json({ success: false, message: 'Question bank unavailable', error: err.message });
        }
    });

    return router;
};
