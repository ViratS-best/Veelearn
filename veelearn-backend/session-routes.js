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
const createCreatorImpact = require('./creator-impact');
const createPhase5 = require('./phase5');

function createSessionRoutes({
    query,
    apiResponse,
    log,
    chat,
    qbank: injectedQBank,
    impact: injectedImpact,
    phase5: injectedPhase5,
    sendEmail
} = {}) {
    const qbank = injectedQBank || createQBank({ query });
    // P4/P5 surfaces. Both are injectable so their tests stay offline.
    const impact = injectedImpact || createCreatorImpact({ query, log });
    const engine = createSessionEngine({
        query,
        qbank,
        log,
        impact,
        // Streaming is only wired when the caller did not inject its own client
        // (tests pass a fake `chat`, which has no stream variant).
        chatStream: chat ? null : require('./ai-chat').aiChatCompletionStream
    });
    // `chat` is injectable so the AI loop can be tested without a key.
    const ai = createSessionAI({ query, qbank, chat, log });
    const p5 = injectedPhase5 || createPhase5({ query, log, sendEmail });

    function fail(res, e, fallbackMessage) {
        const status = e && e.status ? e.status : 500;
        if (status >= 500) console.error('[session]', e);
        return apiResponse(res, status, (e && e.message) || fallbackMessage);
    }

    function sessionIdFrom(req) {
        return parseInt(req.params.sessionId || req.params.id, 10);
    }

    function courseIdFrom(req) {
        return parseInt(req.params.courseId || req.body?.courseId || req.query.courseId, 10);
    }

    /** Readiness and impact are the creator's own pane (admins may look too). */
    async function mayManageCourse(user, courseId) {
        if (!user || !courseId) return false;
        if (user.role === 'admin' || user.role === 'superadmin' || user.is_admin) return true;
        const rows = await query('SELECT creator_id FROM courses WHERE id = ? LIMIT 1', [courseId]);
        return rows.length > 0 && Number(rows[0].creator_id) === Number(user.id);
    }

    return {
        qbank,
        engine,
        ai,
        impact,
        p5,

        /** POST /api/session/start { minutes, track, courseId, intent } */
        async start(req, res) {
            try {
                const data = await engine.start(req.user.id, {
                    minutes: req.body?.minutes,
                    track: req.body?.track,
                    courseId: req.body?.courseId,
                    intent: req.body?.intent,
                    mode: req.body?.mode
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
                const sessions = await engine.history(req.user.id, { limit: req.query.limit, q: req.query.q });
                // The dashboard's Sessions pane lists everything, active first, so
                // a learner can pick a specific session back up.
                const status = String(req.query.status || 'all');
                const filtered =
                    status === 'active' || status === 'completed'
                        ? sessions.filter((row) => row.status === status)
                        : sessions;
                return apiResponse(res, 200, 'OK', { sessions: filtered, count: filtered.length });
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

        /**
         * POST /api/session/:sessionId/teach
         * Server-sent events: a short lesson for the current unit, typed live.
         */
        async teach(req, res) {
            const id = sessionIdFrom(req);
            res.writeHead(200, {
                'Content-Type': 'text/event-stream; charset=utf-8',
                'Cache-Control': 'no-cache, no-transform',
                Connection: 'keep-alive',
                'X-Accel-Buffering': 'no'
            });
            const send = (event, data) => {
                try {
                    res.write(`event: ${event}\ndata: ${JSON.stringify(data)}\n\n`);
                } catch (_) {
                    /* client went away */
                }
            };
            try {
                const out = await engine.teach(req.user.id, id, {
                    onDelta: (t) => send('delta', { t }),
                    question: req.body && req.body.question,
                    // "Teach me this step" and "Show me a similar example" are asks with
                    // a preset question; "Explain it again" asks for a fresh lesson.
                    askMode: req.body && req.body.askMode,
                    fresh: !!(req.body && req.body.fresh)
                });
                if (out.error) send('error', { message: out.message });
                else send('done', { text: out.text, fallback: out.fallback });
            } catch (e) {
                send('error', { message: (e && e.message) || 'Could not teach this unit' });
            }
            res.end();
        },

        /** POST /api/session/:sessionId/extend { minutes } */
        async extend(req, res) {
            try {
                const out = await engine.extend(req.user.id, sessionIdFrom(req), req.body?.minutes);
                if (out.error) return apiResponse(res, out.error, out.message);
                return apiResponse(res, 200, 'Session extended', out);
            } catch (e) {
                return fail(res, e, 'Could not extend the session');
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
         * POST /api/session/:sessionId/board { questionId, ask }
         *
         * The board is generated per question: a preset with real parameters or a
         * small canvas scene the learner can move. A failure returns the authored
         * method, never an unrelated stock graph.
         */
        async board(req, res) {
            try {
                const out = await ai.boardScene({
                    userId: req.user.id,
                    sessionId: sessionIdFrom(req),
                    questionId: req.body?.questionId,
                    ask: req.body?.ask
                });
                if (out.ok === false) return apiResponse(res, out.error || 400, out.message || 'Could not draw that');
                return apiResponse(res, 200, 'Board scene', out);
            } catch (e) {
                return fail(res, e, 'Could not draw that');
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
                const sessionId = sessionIdFrom(req);
                // The plan's unit text is what makes a session sound like the
                // course's author, so it travels with every turn (§15.2).
                let courseFrame = null;
                try {
                    const rows = await query('SELECT turn_buffer FROM sessions WHERE id = ? LIMIT 1', [sessionId]);
                    const raw = rows[0] && rows[0].turn_buffer;
                    if (raw) courseFrame = typeof raw === 'object' ? raw : JSON.parse(String(raw));
                } catch (_) {
                    courseFrame = null;
                }
                const out = await ai.turn({
                    userId: req.user.id,
                    sessionId,
                    course: courseFrame,
                    kind: req.body?.kind,
                    questionId: req.body?.questionId,
                    distractor: req.body?.distractor,
                    attempts: req.body?.attempts,
                    correct: req.body?.correct,
                    itemsDone: req.body?.itemsDone,
                    turns: req.body?.turns,
                    summary: req.body?.summary,
                    learnerPrefs: req.body?.learnerPrefs,
                    course: courseFrame
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


        // ------------------------------------------------------------- P4
        /** GET/POST /api/session/course/:courseId/readiness */
        async readiness(req, res) {
            try {
                const courseId = courseIdFrom(req);
                const allowed = await mayManageCourse(req.user, courseId);
                if (!allowed) return apiResponse(res, 403, 'Only the course creator can see readiness');
                const data = await impact.readiness(courseId, { persist: true });
                return apiResponse(res, 200, 'OK', data);
            } catch (e) {
                return fail(res, e, 'Could not score that course');
            }
        },

        /** GET /api/course/:courseId/impact — the creator pane (§15.5) */
        async courseImpact(req, res) {
            try {
                const courseId = courseIdFrom(req);
                const allowed = await mayManageCourse(req.user, courseId);
                if (!allowed) return apiResponse(res, 403, 'Only the course creator can see impact');
                return apiResponse(res, 200, 'OK', await impact.impact(courseId));
            } catch (e) {
                return fail(res, e, 'Could not load teaching impact');
            }
        },

        /** GET /api/creator/impact — every course the creator owns */
        async creatorImpact(req, res) {
            try {
                return apiResponse(res, 200, 'OK', await impact.summaryForCreator(req.user.id));
            } catch (e) {
                return fail(res, e, 'Could not load your impact');
            }
        },

        // ------------------------------------------------------------- P5
        /** GET/POST /api/profile/exam { date } */
        async exam(req, res) {
            try {
                if (req.method === 'GET') return apiResponse(res, 200, 'OK', await p5.examStatus(req.user.id));
                const data = await p5.setExam({ userId: req.user.id, date: req.body?.date });
                return apiResponse(res, 200, 'Exam date saved', data);
            } catch (e) {
                return fail(res, e, 'Could not save the exam date');
            }
        },

        /** GET /api/session/:sessionId/transcript */
        async transcript(req, res) {
            try {
                const data = await p5.transcript({ userId: req.user.id, sessionId: sessionIdFrom(req) });
                return apiResponse(res, 200, 'OK', data);
            } catch (e) {
                return fail(res, e, 'Could not write the transcript');
            }
        },

        /** POST /api/session/:sessionId/flashcards { questionIds } */
        async makeCards(req, res) {
            try {
                const data = await p5.flashcardsFromSession({
                    userId: req.user.id,
                    sessionId: sessionIdFrom(req),
                    questionIds: req.body?.questionIds
                });
                return apiResponse(res, 200, `${data.created} card(s) saved`, data);
            } catch (e) {
                return fail(res, e, 'Could not build flashcards');
            }
        },

        /** GET /api/flashcards?limit= */
        async cards(req, res) {
            try {
                return apiResponse(res, 200, 'OK', await p5.dueCards({ userId: req.user.id, limit: req.query.limit }));
            } catch (e) {
                return fail(res, e, 'Could not load flashcards');
            }
        },

        /** POST /api/flashcards/:cardId/review { grade } */
        async reviewCard(req, res) {
            try {
                const data = await p5.reviewCard({
                    userId: req.user.id,
                    cardId: parseInt(req.params.cardId, 10),
                    grade: req.body?.grade
                });
                return apiResponse(res, 200, 'Card scheduled', data);
            } catch (e) {
                return fail(res, e, 'Could not schedule that card');
            }
        },

        /** GET /api/flashcards/export.csv — Anki-ready */
        async cardsCsv(req, res) {
            try {
                const data = await p5.cardsCsv(req.user.id);
                if (typeof res.setHeader === 'function') {
                    res.setHeader('Content-Type', 'text/csv; charset=utf-8');
                    res.setHeader('Content-Disposition', 'attachment; filename="veelearn-flashcards.csv"');
                }
                if (typeof res.send === 'function') return res.send(data.csv);
                return apiResponse(res, 200, 'OK', data);
            } catch (e) {
                return fail(res, e, 'Could not export flashcards');
            }
        },

        /** POST /api/session/:sessionId/note */
        async saveNote(req, res) {
            try {
                const data = await p5.saveNote({ userId: req.user.id, sessionId: sessionIdFrom(req) });
                return apiResponse(res, 200, 'Note saved', data);
            } catch (e) {
                return fail(res, e, 'Could not save that note');
            }
        },

        /** GET /api/notes?q= */
        async notes(req, res) {
            try {
                return apiResponse(res, 200, 'OK', await p5.notes({ userId: req.user.id, q: req.query.q }));
            } catch (e) {
                return fail(res, e, 'Could not load your notes');
            }
        },

        /** GET/POST /api/profile/digest — opt in, preview, or send once */
        async digest(req, res) {
            try {
                if (req.method === 'POST') {
                    const data = await p5.setDigest({
                        userId: req.user.id,
                        parentEmail: req.body?.parentEmail,
                        optIn: req.body?.optIn
                    });
                    return apiResponse(res, 200, 'Digest settings saved', data);
                }
                const send = String(req.query.send || '') === '1';
                const data = await p5.digest({ userId: req.user.id, send });
                return apiResponse(res, 200, 'OK', data);
            } catch (e) {
                return fail(res, e, 'Could not build the digest');
            }
        },

        /** POST /api/profile/reminder { at } */
        async reminder(req, res) {
            try {
                const data = await p5.setReminder({ userId: req.user.id, at: req.body?.at });
                return apiResponse(res, 200, 'Reminder saved', data);
            } catch (e) {
                return fail(res, e, 'Could not save the reminder');
            }
        },

        /** POST /api/teacher/assign-session { courseId, minutes, dueAt, unitIndex } */
        async assignSession(req, res) {
            try {
                const data = await p5.assignSession({
                    teacherId: req.user.id,
                    courseId: courseIdFrom(req),
                    classCode: req.body?.classCode,
                    minutes: req.body?.minutes,
                    dueAt: req.body?.dueAt,
                    unitIndex: req.body?.unitIndex,
                    title: req.body?.title
                });
                return apiResponse(res, 201, 'Session assigned', data);
            } catch (e) {
                return fail(res, e, 'Could not assign that session');
            }
        },

        /** GET /api/student/session-assignments */
        async studentAssignments(req, res) {
            try {
                return apiResponse(res, 200, 'OK', await p5.assignmentsForStudent({ userId: req.user.id }));
            } catch (e) {
                return fail(res, e, 'Could not load your assignments');
            }
        },

        /** GET /api/teacher/session-assignment/:assignmentId */
        async teacherMastery(req, res) {
            try {
                const data = await p5.teacherMastery({
                    teacherId: req.user.id,
                    assignmentId: parseInt(req.params.assignmentId, 10)
                });
                return apiResponse(res, 200, 'OK', data);
            } catch (e) {
                return fail(res, e, 'Could not load mastery for that assignment');
            }
        },

        /** POST /api/session/:sessionId/rate { rating } */
        async rate(req, res) {
            try {
                const out = await engine.rate(req.user.id, sessionIdFrom(req), { rating: req.body?.rating });
                if (out.error) return apiResponse(res, out.error, out.message);
                return apiResponse(res, 200, 'Thanks for rating', out);
            } catch (e) {
                return fail(res, e, 'Could not save the rating');
            }
        },

        /** GET /api/teacher/session-assignments */
        async teacherAssignments(req, res) {
            try {
                return apiResponse(res, 200, 'OK', await p5.assignmentsForTeacher({ teacherId: req.user.id }));
            } catch (e) {
                return fail(res, e, 'Could not load your assignments');
            }
        },

        /** POST /api/session/:sessionId/end { reason, rating } */
        async end(req, res) {
            try {
                const sessionId = sessionIdFrom(req);
                const out = await engine.end(req.user.id, sessionId, {
                    reason: req.body?.reason,
                    rating: req.body?.rating
                });
                if (out.error) return apiResponse(res, out.error, out.message);
                // Volunteer hours are paid at the end of a course session, after
                // the learner's rating and the mastery gains exist (§15.4).
                let placement = null;
                try {
                    placement = await impact.record({ sessionId });
                } catch (e) {
                    (log && log.warn ? log.warn : console.warn)(`[session] impact skipped: ${e.message}`);
                }
                return apiResponse(res, 200, 'Session saved', placement ? { ...out, impact: placement } : out);
            } catch (e) {
                return fail(res, e, 'Could not save the session');
            }
        }
    };
}

module.exports = createSessionRoutes;
