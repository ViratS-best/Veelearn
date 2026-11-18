'use strict';

/**
 * Superadmin endpoints for the semantic question bank.
 *
 *   GET  /api/admin/qbank/embed/progress
 *   POST /api/admin/qbank/embed/backfill {afterId, limit, mode}
 *   POST /api/admin/qbank/embed/sync     {afterId, limit}
 *   POST /api/admin/qbank/embed/index
 *   POST /api/admin/qbank/embed/search   {q}
 *
 * Backfill is cursor-based (`afterId`) and resumable, so a caller loops until
 * `remaining` is zero without holding one request open for 50,000 rows.
 */

const express = require('express');

module.exports = function createSemanticRoutes({ query, authenticateToken, log }) {
    const router = express.Router();
    const embeddings = require('./embeddings');
    embeddings.configure({ query, log });

    const admin = (req, res) => {
        if (!req.user || req.user.role !== 'superadmin') {
            res.status(403).json({ success: false, message: 'Superadmin only' });
            return false;
        }
        return true;
    };

    router.get('/api/admin/qbank/embed/progress', authenticateToken, async (req, res) => {
        if (!admin(req, res)) return;
        try {
            const data = await embeddings.progress();
            res.json({ success: true, data });
        } catch (err) {
            res.status(500).json({ success: false, message: 'Could not read embedding progress', error: err.message });
        }
    });

    router.post('/api/admin/qbank/embed/backfill', authenticateToken, async (req, res) => {
        if (!admin(req, res)) return;
        try {
            const body = req.body || {};
            const data = await embeddings.backfill({
                afterId: Number(body.afterId) || 0,
                limit: Number(body.limit) || 192,
                mode: body.mode === 'stale' ? 'stale' : 'missing'
            });
            res.json({ success: data.ok !== false, data });
        } catch (err) {
            res.status(500).json({ success: false, message: 'Backfill failed', error: err.message });
        }
    });

    router.post('/api/admin/qbank/embed/sync', authenticateToken, async (req, res) => {
        if (!admin(req, res)) return;
        try {
            const body = req.body || {};
            const data = await embeddings.backfill({
                afterId: Number(body.afterId) || 0,
                limit: Number(body.limit) || 128,
                mode: 'stale'
            });
            res.json({ success: data.ok !== false, data });
        } catch (err) {
            res.status(500).json({ success: false, message: 'Sync failed', error: err.message });
        }
    });

    router.post('/api/admin/qbank/embed/index', authenticateToken, async (req, res) => {
        if (!admin(req, res)) return;
        try {
            const data = await embeddings.ensureIndex();
            res.json({ success: data.ok !== false, data });
        } catch (err) {
            res.status(500).json({ success: false, message: 'Index build failed', error: err.message });
        }
    });

    /** Diagnostic: does a phrase find the right questions, and how fast? */
    router.post('/api/admin/qbank/embed/search', authenticateToken, async (req, res) => {
        if (!admin(req, res)) return;
        try {
            const q = String((req.body && req.body.q) || '').trim();
            if (!q) return res.status(400).json({ success: false, message: 'Give the test a query' });
            const started = Date.now();
            const vector = await embeddings.embedQuery(q);
            if (!vector) {
                return res.json({ success: true, data: { query: q, semantic: false, results: [] } });
            }
            const column = embeddings.state.column;
            const rows = await query(
                `SELECT q.id, q.stem, s.name AS skill_name,
                        (1 - (q.embedding <=> ?::${column})) AS similarity
                   FROM qbank_items q LEFT JOIN skills s ON s.id = q.skill_id
                  WHERE q.live = 1 AND q.embedding IS NOT NULL
                  ORDER BY q.embedding <=> ?::${column}
                  LIMIT 8`,
                [vector, vector]
            );
            res.json({
                success: true,
                data: {
                    query: q,
                    semantic: true,
                    ms: Date.now() - started,
                    results: rows.map((r) => ({
                        id: Number(r.id),
                        skill: r.skill_name || '',
                        stem: String(r.stem || '').slice(0, 160),
                        similarity: Number(Number(r.similarity || 0).toFixed(4))
                    }))
                }
            });
        } catch (err) {
            res.status(500).json({ success: false, message: 'Semantic search failed', error: err.message });
        }
    });

    return router;
};
