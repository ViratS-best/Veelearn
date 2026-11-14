'use strict';

/**
 * HTTP handlers for AI learning sessions.
 *
 * Thin by design: parse, delegate to session-engine, shape the response with the
 * standard `{ success, message, data }` envelope every other route uses.
 */

const createSessionEngine = require('./session-engine');
const createQBank = require('./qbank');
const createSessionAI = require('./session-ai');

function createSessionRoutes({ query, apiResponse, log, chat, qbank: injectedQBank } = {}) {
    const qbank = injectedQBank || createQBank({ query });
    const engine = createSessionEngine({ query, qbank, log });
    // `chat` is injectable so the AI loop can be tested without a key.
    const ai = createSessionAI({ query, qbank, chat, log });

    function fail(res, e, fallbackMessage) {
        const status = e && e.status ? e.status : 500;
        if (status >= 500) console.error('[session]', e);
        return apiResponse(res, status, (e && e.message) || fallbackMessage);
    }

    function sessionIdFrom(req) {
        return parseInt(req.params.sessionId || req.params.id, 10);
    }

    return {
        qbank,
        engine,
        ai,

        /** POST /api/session/start { minutes, track, courseId, intent } */
        async start(req, res) {
            try {
                const data = await engine.start(req.user.id, {
                    minutes: req.body?.minutes,
                    track: req.body?.track,
                    courseId: req.body?.courseId,
                    intent: req.body?.intent
                });
                return apiResponse(res, 200, data.resumed ? 'Session resumed' : 'Session started', data);
            } catch (e) {
                return fail(res, e, 'Could not start a session');
            }
        },

        /** GET /api/session/active — resume card */
        async active(req, res) {
            try {
                return apiResponse(res, 200, 'OK', await engine.active(req.user.id));
            } catch (e) {
                return fail(res, e, 'Could not load your session');
            }
        },

        /** GET /api/session/history */
        async history(req, res) {
            try {
                const data = await engine.history(req.user.id, { limit: req.query.limit });
                return apiResponse(res, 200, 'OK', data);
            } catch (e) {
                return fail(res, e, 'Could not load session history');
            }
        },

        /** GET /api/skills/map?track= */
        async map(req, res) {
            try {
                const data = await engine.mapFor(req.user.id, req.query.track);
                return apiResponse(res, 200, 'OK', data);
            } catch (e) {
                return fail(res, e, 'Could not load the learning map');
            }
        },

        /** GET /api/session/:sessionId */
        async get(req, res) {
            try {
                const data = await engine.state(req.user.id, sessionIdFrom(req));
                if (!data) return apiResponse(res, 404, 'Session not found');
                return apiResponse(res, 200, 'OK', data);
            } catch (e) {
                return fail(res, e, 'Could not load the session');
            }
        },

        /** POST /api/session/:sessionId/answer */
        async answer(req, res) {
            try {
                const out = await engine.answer(req.user.id, sessionIdFrom(req), {
                    itemId: req.body?.itemId,
                    questionId: req.body?.questionId,
                    answer: req.body?.answer,
                    ms: req.body?.ms,
                    hints: req.body?.hints
                });
                if (out.error) return apiResponse(res, out.error, out.message);
                return apiResponse(res, 200, out.correct ? 'Correct' : 'Not quite', out);
            } catch (e) {
                return fail(res, e, 'Could not grade that answer');
            }
        },

        /** POST /api/session/:sessionId/hint */
        async hint(req, res) {
            try {
                const out = await engine.hint(req.user.id, sessionIdFrom(req), {
                    questionId: req.body?.questionId
                });
                if (out.error) return apiResponse(res, out.error, out.message);
                return apiResponse(res, 200, 'OK', out);
            } catch (e) {
                return fail(res, e, 'Could not load a hint');
            }
        },

        /** POST /api/session/:sessionId/skip */
        async skip(req, res) {
            try {
                const out = await engine.skip(req.user.id, sessionIdFrom(req), { itemId: req.body?.itemId });
                if (out.error) return apiResponse(res, out.error, out.message);
                return apiResponse(res, 200, 'Item deferred', out);
            } catch (e) {
                return fail(res, e, 'Could not skip that item');
            }
        },

        /**
         * POST /api/session/:sessionId/ai { kind, questionId, distractor, attempts, correct }
         *
         * The model proposes a line and a script; this route returns something
         * playable even when it is rate-limited, slow or malformed.
         */
        async aiTurn(req, res) {
            try {
                const out = await ai.turn({
                    userId: req.user.id,
                    sessionId: sessionIdFrom(req),
                    kind: req.body?.kind,
                    questionId: req.body?.questionId,
                    distractor: req.body?.distractor,
                    attempts: req.body?.attempts,
                    correct: req.body?.correct,
                    itemsDone: req.body?.itemsDone,
                    turns: req.body?.turns,
                    summary: req.body?.summary,
                    learnerPrefs: req.body?.learnerPrefs
                });
                if (out.error && !out.ok) return apiResponse(res, out.error, out.message);
                return apiResponse(res, 200, 'OK', out);
            } catch (e) {
                return fail(res, e, 'Could not prepare an explanation');
            }
        },

        /**
         * POST /api/session/:sessionId/summary
         *
         * One model sentence for the end screen, requested after /end has already
         * answered so the ending never waits on a slow free model.
         */
        async summary(req, res) {
            try {
                const rows = await query(
                    `SELECT su.summary AS summary, su.next_step AS next_step
                     FROM session_summaries su
                     JOIN sessions s ON s.id = su.session_id
                     WHERE su.session_id = ? AND s.user_id = ? LIMIT 1`,
                    [sessionIdFrom(req), req.user.id]
                );
                if (!rows.length) return apiResponse(res, 404, 'Session summary not found');
                const out = await ai.summary({
                    sessionId: sessionIdFrom(req),
                    payload: {
                        summary: rows[0].summary,
                        nextStep: rows[0].next_step,
                        budgetMs: req.body?.budgetMs
                    }
                });
                return apiResponse(res, 200, 'OK', out);
            } catch (e) {
                return fail(res, e, 'Could not write a summary line');
            }
        },

        /** POST /api/session/:sessionId/end { reason } */
        async end(req, res) {
            try {
                const out = await engine.end(req.user.id, sessionIdFrom(req), { reason: req.body?.reason });
                if (out.error) return apiResponse(res, out.error, out.message);
                return apiResponse(res, 200, 'Session saved', out);
            } catch (e) {
                return fail(res, e, 'Could not save the session');
            }
        }
    };
}

module.exports = createSessionRoutes;
