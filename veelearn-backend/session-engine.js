'use strict';

/**
 * Session engine: plans a focus list, serves one question at a time, grades
 * deterministically from the bank's answer key, updates mastery and schedules
 * reviews.
 *
 * Phase 1 has no model in the loop — by design. The graded loop, mastery maths
 * and rewards must be correct and fast before an LLM is allowed near it. The
 * engine's response shapes already match what the AI will later decorate
 * (`say`, `script`, `mood`), so Phase 3 only adds fields.
 */

const mastery = require('./mastery');

const TRACK_FALLBACK = 'math.g8';

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

function createSessionEngine({ query, qbank, log, chatStream } = {}) {
    const info = (log && log.info) || (() => {});

    // ---------------------------------------------------------------- rewards
    /**
     * Award XP/gems through the existing ledger so the sidebar, store and
     * achievements all keep working. Idempotent by event_key.
     */
    async function award(userId, eventKey, reward) {
        const xp = reward.xp || 0;
        const gems = reward.gems || 0;
        let inserted = false;
        try {
            const res = await query(
                'INSERT IGNORE INTO user_xp_events (user_id, event_key, xp, gems) VALUES (?, ?, ?, ?)',
                [userId, String(eventKey).slice(0, 191), xp, gems]
            );
            const header = Array.isArray(res) ? res[0] : res;
            inserted = (header?.affectedRows || 0) > 0;
        } catch (e) {
            info(`[session] award skipped: ${e.message}`);
            return { xpAwarded: 0, gemsAwarded: 0 };
        }
        if (!inserted) return { xpAwarded: 0, gemsAwarded: 0 };

        try {
            await query(
                `UPDATE users SET xp = COALESCE(xp,0) + ?, gems = COALESCE(gems,0) + ?,
                        lifetime_gems = COALESCE(lifetime_gems,0) + ?
                 WHERE id = ?`,
                [xp, gems, gems, userId]
            );
        } catch (e) {
            // lifetime_gems may not exist on very old databases.
            await query('UPDATE users SET xp = COALESCE(xp,0) + ?, gems = COALESCE(gems,0) + ? WHERE id = ?', [
                xp,
                gems,
                userId
            ]);
        }
        return { xpAwarded: xp, gemsAwarded: gems };
    }

    async function rewardTotals(userId) {
        const rows = await query('SELECT xp, gems FROM users WHERE id = ? LIMIT 1', [userId]);
        return { xp: Number(rows[0]?.xp || 0), gems: Number(rows[0]?.gems || 0) };
    }

    // -------------------------------------------------------------- planning
    async function resolveTrack(userId, requested) {
        const wanted = String(requested || '').trim();
        if (wanted) {
            const known = await query('SELECT track FROM skills WHERE track = ? LIMIT 1', [wanted]);
            if (known.length) return wanted;
        }

        const last = await query(
            `SELECT s.track
             FROM sessions se
             JOIN session_focus_items f ON f.session_id = se.id
             JOIN skills s ON s.id = f.skill_id
             WHERE se.user_id = ?
             ORDER BY se.id DESC LIMIT 1`,
            [userId]
        );
        if (last.length && last[0].track) return last[0].track;

        try {
            const prof = await query('SELECT prefs FROM user_learning_profile WHERE user_id = ? LIMIT 1', [userId]);
            const prefs = parseJson(prof[0]?.prefs, {}) || {};
            const grade = parseInt(prefs.declared_grade, 10);
            if (!Number.isNaN(grade)) {
                if (grade <= 8) return 'math.g8';
                if (grade <= 10) return 'algebra1';
                if (grade <= 12) return 'sat.math';
            }
        } catch (_) {
            /* prefs column may be missing */
        }
        return TRACK_FALLBACK;
    }

    /**
     * Focus list: due reviews first, then the weakest unlocked skills, with
     * prerequisites respected. Pure SQL + rules, so it is instant.
     */
    async function planFocus(userId, { track, minutes }) {
        const items = mastery.itemsForMinutes(minutes);
        const skills = await qbank.listSkills(track);
        if (!skills.length) return [];

        const masteryRows = await query(
            'SELECT skill_id, p, level, ease, last_seen FROM skill_mastery WHERE user_id = ?',
            [userId]
        );
        const mById = new Map(masteryRows.map((r) => [Number(r.skill_id), r]));

        const dueRows = await query(
            `SELECT r.skill_id
             FROM review_queue r
             JOIN skills s ON s.id = r.skill_id
             WHERE r.user_id = ? AND s.track = ? AND r.due_at <= NOW()
             ORDER BY r.due_at ASC LIMIT 3`,
            [userId, track]
        );
        const dueIds = dueRows.map((r) => Number(r.skill_id));

        const byId = new Map(skills.map((s) => [Number(s.id), s]));
        const levelOf = (id) => Number(mById.get(Number(id))?.level || 0);

        // Never plan a focus item we cannot serve. A stale or empty pool must not
        // dead-end a session, so fall back to the unfiltered list.
        let servable = null;
        try {
            const pool = await query('SELECT DISTINCT skill_id FROM skill_pool WHERE live_count > 0');
            if (pool.length) servable = new Set(pool.map((r) => Number(r.skill_id)));
        } catch (_) {
            servable = null;
        }
        const canServe = (id) => !servable || servable.has(Number(id));

        const plan = [];
        for (const id of dueIds) {
            const s = byId.get(id);
            if (s && canServe(id) && plan.length < items) plan.push({ skill: s, isReview: true });
        }

        const candidates = skills
            .filter((s) => !dueIds.includes(Number(s.id)))
            .filter((s) => canServe(s.id))
            .filter((s) => {
                const pre = s.prereq_id ? byId.get(Number(s.prereq_id)) : null;
                if (!pre) return true;
                return levelOf(pre.id) >= 1;
            })
            .sort((a, b) => {
                const la = levelOf(a.id);
                const lb = levelOf(b.id);
                if (la !== lb) return la - lb;
                return Number(a.order_index || 0) - Number(b.order_index || 0);
            });

        for (const s of candidates) {
            if (plan.length >= items) break;
            plan.push({ skill: s, isReview: false });
        }

        // Everything mastered and nothing due: recycle the highest-order skills.
        if (!plan.length) {
            for (const s of skills.slice(-items)) plan.push({ skill: s, isReview: true });
        }

        return plan.map((p) => {
            const m = mById.get(Number(p.skill.id));
            return {
                skillId: Number(p.skill.id),
                skill: p.skill,
                isReview: p.isReview,
                targetDots: Math.min(4, Number(p.skill.dot_target || 2)),
                level: Number(m?.level || 0),
                startTier: Math.min(4, Math.max(1, Number(m?.level || 0) + 1))
            };
        });
    }

    // ---------------------------------------------------------------- session
    async function sessionRow(userId, sessionId) {
        const rows = await query(
            `SELECT id, user_id, course_id, mode, minutes, goal_text, status, item_index,
                    xp_awarded, gems_awarded, started_at, ended_at, last_active_at,
                    turn_buffer, sprint, rating,
                    GREATEST(0, CAST(EXTRACT(EPOCH FROM (NOW() - started_at)) AS INTEGER)) AS elapsed_s
             FROM sessions WHERE id = ? AND user_id = ? LIMIT 1`,
            [sessionId, userId]
        );
        return rows[0] || null;
    }

    async function focusItems(sessionId) {
        return query(
            `SELECT f.id, f.session_id, f.skill_id, f.ord, f.is_review, f.target_dots, f.status,
                    f.correct_count, f.attempts, f.question_ids, f.started_at, f.completed_at,
                    s.name AS skill_name, s.code AS skill_code, s.track, s.intro_md
             FROM session_focus_items f
             JOIN skills s ON s.id = f.skill_id
             WHERE f.session_id = ?
             ORDER BY f.ord ASC`,
            [sessionId]
        );
    }

    function currentItem(items, index) {
        const active = items.find((i) => i.status === 'active');
        if (active) return active;
        const pending = items.find((i) => i.status === 'pending');
        if (pending) return pending;
        const byIndex = items[Number(index)];
        return byIndex && byIndex.status !== 'deferred' ? byIndex : null;
    }

    async function mapFor(userId, track) {
        const skills = await qbank.listSkills(track || null);
        const rows = await query('SELECT skill_id, p, level FROM skill_mastery WHERE user_id = ?', [userId]);
        const mById = new Map(rows.map((r) => [Number(r.skill_id), r]));
        const byTrack = new Map();
        for (const s of skills) {
            const t = s.track;
            if (!byTrack.has(t)) byTrack.set(t, []);
            const m = mById.get(Number(s.id));
            const level = Number(m?.level || 0);
            byTrack.get(t).push({
                id: Number(s.id),
                code: s.code,
                name: s.name,
                level,
                dots: mastery.dots(level),
                dotTarget: Number(s.dot_target || 2)
            });
        }
        const out = [];
        for (const [t, list] of byTrack.entries()) {
            const avg = list.length ? list.reduce((sum, s) => sum + s.level, 0) / (list.length * 4) : 0;
            out.push({ track: t, percent: Math.round(avg * 100), skills: list });
        }
        return out;
    }

    /**
     * The card the learner is about to see — always a real one.
     *
     * Course units no longer arrive with questions written ahead of time. When a
     * unit has nothing servable, the AI writes its questions at this exact moment
     * and they are stored, so the next visit is instant.
     */
    const ensuring = new Map();

    async function ensureQuestion(item, userId) {
        const ids = parseJson(item.question_ids, []);
        const lastId = ids.length ? ids[ids.length - 1] : null;
        if (lastId) {
            const raw = await qbank.getRaw(lastId);
            if (raw) return qbank.toCard(raw);
        }

        let picked = await qbank.pickUnserved({ skillId: item.skill_id, exclude: [] });
        if (!picked) picked = await qbank.pick({ skillId: item.skill_id, tier: 1, userId });
        if (!picked) {
            try {
                // Prefetch and the first render can race; one call per skill is enough.
                let pending = ensuring.get(Number(item.skill_id));
                if (!pending) {
                    const impact = require('./creator-impact')({ query, log });
                    pending = impact.ensureQuestionsForSkill(item.skill_id).finally(() => {
                        setTimeout(() => ensuring.delete(Number(item.skill_id)), 5000);
                    });
                    ensuring.set(Number(item.skill_id), pending);
                }
                const made = await pending;
                if (made && made.length) picked = await qbank.getRaw(made[0]);
            } catch (err) {
                info(`[session] on-demand questions skipped: ${err.message}`);
            }
        }
        if (!picked) return null;

        await query('UPDATE session_focus_items SET question_ids = ? WHERE id = ?', [
            JSON.stringify([Number(picked.id)]),
            item.id
        ]);
        return qbank.toCard(picked);
    }

    /**
     * A short lesson for the current unit, streamed token by token. The unit's own
     * text is the fallback, so even without a key the learner gets taught instead
     * of being handed another question.
     */
    async function teach(userId, sessionId, { onDelta } = {}) {
        const session = await sessionRow(userId, sessionId);
        if (!session) return { error: 404, message: 'Session not found' };
        const items = await focusItems(sessionId);
        const item = currentItem(items, session.item_index);
        if (!item) return { error: 409, message: 'That session has no current unit' };

        const rows = await query('SELECT name, intro_md FROM skills WHERE id = ? LIMIT 1', [item.skill_id]);
        const unitText = String((rows[0] && rows[0].intro_md) || '').replace(/\s+/g, ' ').trim();
        const title = item.skill_name || (rows[0] && rows[0].name) || 'this unit';
        const frame = parseJson(session.turn_buffer, null);
        const fallback =
            unitText.slice(0, 900) ||
            `In ${title}, start from what the question is giving you, name the rule it matches, then apply that rule one step at a time.`;

        if (typeof chatStream !== 'function') return { ok: true, text: fallback, fallback: true };

        let text = '';
        try {
            text = await chatStream(
                [
                    {
                        role: 'system',
                        content:
                            'You are Vee, a patient tutor for a study app. Teach in plain, warm prose. ' +
                            'Never mention that you are an AI or a model.'
                    },
                    {
                        role: 'user',
                        content:
                            `Course: ${(frame && frame.title) || 'a self-study course'}\n` +
                            `Unit: ${title}\n` +
                            (unitText ? `Unit material: ${unitText.slice(0, 1200)}\n` : '') +
                            '\nTeach this unit in under 120 words: the one idea, why it works, and a tiny worked example. ' +
                            'Do not ask a question and do not give the answer to any practice question. Use $...$ for math.'
                    }
                ],
                { max_tokens: 300, temperature: 0.5, budgetMs: 25000, onDelta }
            );
        } catch (err) {
            info(`[session] teach fallback: ${err.message}`);
        }
        return { ok: true, text: String(text || fallback).trim(), fallback: !text };
    }

    /** More time on the clock, without losing the plan. */
    async function extend(userId, sessionId, minutes) {
        const session = await sessionRow(userId, sessionId);
        if (!session) return { error: 404, message: 'Session not found' };
        if (session.status !== 'active') return { error: 409, message: 'This session is not active' };
        const add = Math.max(1, Math.min(60, parseInt(minutes, 10) || 10));
        await query('UPDATE sessions SET minutes = minutes + ?, last_active_at = NOW() WHERE id = ?', [add, sessionId]);
        return { ok: true, added: add, state: await state(userId, sessionId) };
    }

    async function state(userId, sessionId, { ensure = true } = {}) {
        const session = await sessionRow(userId, sessionId);
        if (!session) return null;
        const items = await focusItems(sessionId);
        const item = currentItem(items, session.item_index);
        const remainingMs = Math.max(0, Number(session.minutes || 20) * 60000 - Number(session.elapsed_s || 0) * 1000);

        let question = null;
        if (item && session.status === 'active' && ensure) {
            question = await ensureQuestion(item, userId);
        }

        const summaryRows = await query('SELECT summary, next_step FROM session_summaries WHERE session_id = ? LIMIT 1', [
            sessionId
        ]);

        const masteryRows = await query('SELECT skill_id, level FROM skill_mastery WHERE user_id = ?', [userId]);
        const levelById = new Map(masteryRows.map((r) => [Number(r.skill_id), Number(r.level || 0)]));

        const done = items.filter((i) => i.status === 'done').length;
        const track = items[0]?.track || null;

        return {
            session: {
                id: Number(session.id),
                status: session.status,
                minutes: Number(session.minutes || 20),
                goal: session.goal_text || '',
                itemIndex: Number(session.item_index || 0),
                track,
                mode: session.mode || 'focus',
                remainingMs,
                elapsedMs: Number(session.elapsed_s || 0) * 1000,
                xpAwarded: Number(session.xp_awarded || 0),
                gemsAwarded: Number(session.gems_awarded || 0)
            },
            focus: items.map((i) => {
                const level = levelById.get(Number(i.skill_id)) || 0;
                return {
                    id: Number(i.id),
                    skillId: Number(i.skill_id),
                    name: i.skill_name,
                    code: i.skill_code,
                    ord: Number(i.ord),
                    status: i.status,
                    isReview: !!Number(i.is_review),
                    targetDots: Number(i.target_dots || 2),
                    correctCount: Number(i.correct_count || 0),
                    dots: mastery.dots(level),
                    level
                };
            }),
            item: item
                ? {
                      id: Number(item.id),
                      skillId: Number(item.skill_id),
                      code: item.skill_code,
                      name: item.skill_name,
                      intro: item.intro_md || '',
                      isReview: !!Number(item.is_review),
                      targetDots: Number(item.target_dots || 2),
                      correctCount: Number(item.correct_count || 0),
                      attempts: Number(item.attempts || 0),
                      needed: mastery.correctsNeeded(Number(item.target_dots || 2)),
                      dots: mastery.dots(levelById.get(Number(item.skill_id)) || 0)
                  }
                : null,
            question,
            course: parseJson(session.turn_buffer, null),
            sprint: !!Number(session.sprint || 0),
            map: await mapFor(userId, track),
            summary: summaryRows[0] ? { text: summaryRows[0].summary, nextStep: summaryRows[0].next_step } : null,
            progress: { done, total: items.length }
        };
    }

    async function start(userId, { minutes, track, courseId, intent, mode } = {}) {
        const mins = mastery.clamp(minutes || 20, 5, 90);
        const wantCourse = courseId ? Number(courseId) : null;
        const wantSprint = String(mode || '') === 'sprint';

        // Reuse an in-flight session for the same course (or track) so a refresh
        // or a back-navigation never loses the plan.
        if (wantCourse) {
            const activeCourse = await query(
                "SELECT id FROM sessions WHERE user_id = ? AND status = 'active' AND course_id = ? ORDER BY id DESC LIMIT 1",
                [userId, wantCourse]
            );
            if (activeCourse.length) {
                const existing = await state(userId, activeCourse[0].id, { ensure: false });
                // Resume even when the current unit has not written its card yet:
                // the page prefetches it, and starting a second session would lose
                // the plan the learner already has.
                if (existing) return { ...existing, resumed: true };
            }
        }

        const chosenTrack = wantCourse ? null : await resolveTrack(userId, track);

        if (!wantCourse) {
            const activeRows = await query(
                `SELECT se.id FROM sessions se
                 JOIN session_focus_items f ON f.session_id = se.id
                 JOIN skills s ON s.id = f.skill_id
                 WHERE se.user_id = ? AND se.status = 'active' AND s.track = ?
                 ORDER BY se.id DESC LIMIT 1`,
                [userId, chosenTrack]
            );
            if (activeRows.length) {
                const existing = await state(userId, activeRows[0].id);
                if (existing && existing.question) return { ...existing, resumed: true };
            }
        }

        // Three planners, one shape. A course session follows the creator's
        // units (§15.2); a sprint follows the exam plan (§16.3); the default
        // stays the generic focus list.
        let plan = [];
        let courseFrame = null;
        let sprint = 0;
        if (wantCourse) {
            const createImpact = require('./creator-impact');
            const planned = await createImpact({ query, log }).plan({ userId, courseId: wantCourse, minutes: mins });
            plan = planned.items;
            courseFrame = {
                courseId: wantCourse,
                title: planned.course.title,
                readiness: planned.report.score,
                bankLed: planned.report.bankLed,
                units: planned.report.units
            };
        } else if (wantSprint) {
            const createPhase5 = require('./phase5');
            const planned = await createPhase5({ query, log }).sprintPlan({ userId });
            plan = planned.items || [];
            sprint = 1;
            if (!plan.length) plan = await planFocus(userId, { track: chosenTrack, minutes: mins });
        } else {
            plan = await planFocus(userId, { track: chosenTrack, minutes: mins });
        }
        if (!plan.length) {
            const err = new Error(
                wantCourse
                    ? 'This course has no practice questions yet — its creator needs to add quiz questions.'
                    : 'No practice material for this track yet'
            );
            err.status = 503;
            throw err;
        }

        const goalText = wantCourse
            ? `Finish ${plan.length} unit${plan.length === 1 ? '' : 's'} of this course`
            : wantSprint
              ? 'Six items to your exam'
              : mins <= 10
                ? 'Close two gaps'
                : mins <= 20
                  ? `Move ${Math.min(3, plan.length)} skills up a level`
                  : 'Half a unit';

        const sessionMode = wantCourse ? 'course' : wantSprint ? 'sprint' : 'focus';
        const inserted = await query(
            `INSERT INTO sessions (user_id, course_id, mode, intent_text, minutes, goal_text, status, item_index, sprint, turn_buffer)
             VALUES (?, ?, ?, ?, ?, ?, 'active', 0, ?, ?)`,
            [
                userId,
                wantCourse || null,
                sessionMode,
                intent ? String(intent).slice(0, 500) : null,
                mins,
                goalText,
                sprint,
                courseFrame ? JSON.stringify(courseFrame) : null
            ]
        );
        const sessionId = inserted.insertId || (await latestSessionId(userId));
        if (!sessionId) throw new Error('Could not create session');

        for (let i = 0; i < plan.length; i += 1) {
            const p = plan[i];
            // A course unit can arrive with its creator's questions already chosen.
            const seeded = Array.isArray(p.questionIds) ? p.questionIds.filter(Boolean) : [];
            const q = seeded.length ? null : await qbank.pick({ skillId: p.skillId, tier: p.startTier || 1, userId });
            await query(
                `INSERT INTO session_focus_items
                    (session_id, skill_id, ord, is_review, target_dots, status, correct_count, attempts, question_ids)
                 VALUES (?, ?, ?, ?, ?, 'pending', 0, 0, ?)`,
                [
                    sessionId,
                    p.skillId,
                    i,
                    p.isReview ? 1 : 0,
                    p.targetDots,
                    JSON.stringify(seeded.length ? seeded.map(Number) : q ? [Number(q.id)] : [])
                ]
            );
        }
        await logEvent(sessionId, 0, 'start', null, null, {
            track: chosenTrack,
            minutes: mins,
            mode: sessionMode,
            courseId: wantCourse || null
        });

        // No generation here: opening a session must not wait on the model.
        const fresh = await state(userId, sessionId, { ensure: false });
        return { ...fresh, resumed: false };
    }

    async function latestSessionId(userId) {
        const rows = await query('SELECT id FROM sessions WHERE user_id = ? ORDER BY id DESC LIMIT 1', [userId]);
        return rows[0]?.id || null;
    }

    async function logEvent(sessionId, seq, kind, skillId, questionId, payload) {
        try {
            await query(
                'INSERT INTO session_events (session_id, seq, kind, skill_id, question_id, payload) VALUES (?, ?, ?, ?, ?, ?)',
                [
                    sessionId,
                    Number(seq) || 0,
                    kind,
                    skillId || null,
                    questionId || null,
                    payload ? JSON.stringify(payload).slice(0, 4000) : null
                ]
            );
        } catch (e) {
            info(`[session] event log skipped: ${e.message}`);
        }
    }

    async function nextSeq(sessionId) {
        const rows = await query('SELECT COALESCE(MAX(seq), 0) AS s FROM session_events WHERE session_id = ?', [sessionId]);
        return Number(rows[0]?.s || 0) + 1;
    }

    // ------------------------------------------------------------- mastery io
    async function applyMastery(userId, skillId, { correct, tier, assistance }) {
        const rows = await query(
            'SELECT p, level, ease, seen, correct, last_seen FROM skill_mastery WHERE user_id = ? AND skill_id = ? LIMIT 1',
            [userId, skillId]
        );
        const before = rows[0] || { p: 0, level: 0, ease: 2.5, seen: 0, correct: 0 };
        const res = mastery.applyAttempt({ p: before.p, correct, tier, assistance });
        const levelAfter = mastery.levelFromP(res.p);
        const levelUp = levelAfter > Number(before.level || 0);

        if (rows[0]) {
            await query(
                `UPDATE skill_mastery
                 SET p = ?, level = ?, seen = COALESCE(seen,0) + 1, correct = COALESCE(correct,0) + ?,
                     last_seen = NOW()${levelUp ? ', last_level_up_at = NOW()' : ''}
                 WHERE user_id = ? AND skill_id = ?`,
                [res.p, levelAfter, correct ? 1 : 0, userId, skillId]
            );
        } else {
            await query(
                `INSERT INTO skill_mastery (user_id, skill_id, p, level, ease, seen, correct, last_seen, last_level_up_at)
                 VALUES (?, ?, ?, ?, ?, 1, ?, NOW(), ?)`,
                [userId, skillId, res.p, levelAfter, 2.5, correct ? 1 : 0, levelUp ? new Date().toISOString() : null]
            );
        }

        // ---- review scheduling
        const review = mastery.nextReview({
            level: levelAfter,
            ease: Number(before.ease || 2.5),
            correct,
            reps: Number(before.seen || 0)
        });
        const dueAt = new Date(Date.now() + review.intervalDays * 86400000).toISOString();
        try {
            const existing = await query('SELECT id FROM review_queue WHERE user_id = ? AND skill_id = ? LIMIT 1', [
                userId,
                skillId
            ]);
            const verify = assistance >= 2 ? 1 : 0;
            if (existing.length) {
                await query(
                    'UPDATE review_queue SET due_at = ?, ease = ?, reps = ?, verify_independently = ? WHERE id = ?',
                    [dueAt, review.ease, review.reps, verify, existing[0].id]
                );
            } else {
                await query(
                    `INSERT INTO review_queue (user_id, skill_id, due_at, ease, reps, verify_independently)
                     VALUES (?, ?, ?, ?, ?, ?)`,
                    [userId, skillId, dueAt, review.ease, review.reps, verify]
                );
            }
        } catch (e) {
            info(`[session] review schedule skipped: ${e.message}`);
        }

        return {
            p: res.p,
            delta: res.delta,
            assistance: res.assistance,
            levelBefore: Number(before.level || 0),
            levelAfter,
            levelUp,
            dots: mastery.dots(levelAfter),
            nextReviewDays: review.intervalDays
        };
    }

    // ----------------------------------------------------------------- answer
    async function answer(userId, sessionId, { itemId, questionId, answer, ms, hints } = {}) {
        const session = await sessionRow(userId, sessionId);
        if (!session) return { error: 404, message: 'Session not found' };
        if (session.status !== 'active') return { error: 409, message: 'This session is not active' };

        const items = await focusItems(sessionId);
        const item = items.find((i) => Number(i.id) === Number(itemId));
        if (!item) return { error: 400, message: 'That focus item is not part of this session' };
        if (item.status !== 'pending' && item.status !== 'active') {
            return { error: 409, message: 'That focus item is already done' };
        }

        const raw = await qbank.getRaw(questionId);
        if (!raw || Number(raw.skill_id) !== Number(item.skill_id)) {
            return { error: 400, message: 'Unknown question for this skill' };
        }
        const servedIds = parseJson(item.question_ids, []).map(Number);
        if (!servedIds.includes(Number(raw.id))) {
            return { error: 409, message: 'That question is not the one being asked' };
        }

        const priorRows = await query(
            'SELECT COUNT(*) AS c FROM practice_attempts WHERE user_id = ? AND session_id = ? AND question_id = ?',
            [userId, sessionId, raw.id]
        );
        const priorAttempts = Number(priorRows[0]?.c || 0);

        const hintRows = await query(
            "SELECT COUNT(*) AS c FROM session_events WHERE session_id = ? AND kind = 'hint' AND question_id = ?",
            [sessionId, raw.id]
        );
        const hintsUsed = Math.max(Number(hintRows[0]?.c || 0), Math.min(3, Number(hints) || 0));
        // Hints count, and so does a retry: if this card was already answered, the
        // learner has seen an explanation, so the next correct is worth less.
        const assistance = hintsUsed >= 2 ? 2 : hintsUsed >= 1 || priorAttempts > 0 ? 1 : 0;

        const given = String(answer == null ? '' : answer).trim().toUpperCase().replace(/\s+/g, '');
        const expected = String(raw.answer || '').trim().toUpperCase().replace(/\s+/g, '');
        const correct = given !== '' && given === expected;

        await query(
            `INSERT INTO practice_attempts
                (user_id, question_id, skill_id, session_id, correct, hints, assistance, ms_taken, answer_given)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`,
            [userId, raw.id, raw.skill_id, sessionId, correct ? 1 : 0, hintsUsed, assistance, Math.min(600000, Number(ms) || 0), given.slice(0, 64)]
        );

        const m = await applyMastery(userId, raw.skill_id, { correct, tier: raw.tier, assistance });

        // ---- item progression
        const need = mastery.correctsNeeded(Number(item.target_dots || 2));
        const correctCount = Number(item.correct_count || 0) + (correct ? 1 : 0);
        const attempts = Number(item.attempts || 0) + 1;
        let itemDone = correct && correctCount >= need;

        let next = 'retry';
        let nextQuestion = null;

        if (correct) {
            if (itemDone) {
                next = 'advance';
            } else {
                next = 'more';
                const tier = Math.min(4, Number(raw.tier) + 1);
                nextQuestion = await qbank.pick({ skillId: raw.skill_id, tier, userId });
                if (!nextQuestion || parseJson(item.question_ids, []).map(Number).includes(Number(nextQuestion.id))) {
                    nextQuestion = await qbank.pickUnserved({
                        skillId: raw.skill_id,
                        exclude: parseJson(item.question_ids, [])
                    });
                    // Nothing new in this skill: the unit is finished, don't loop the
                    // same card at the learner.
                    if (!nextQuestion) {
                        itemDone = true;
                        next = 'advance';
                    }
                }
            }
        } else if (attempts >= 2) {
            // Taught once already — hand back a variant one tier easier.
            next = 'variant';
            nextQuestion = await qbank.pick({ skillId: raw.skill_id, tier: Math.max(1, Number(raw.tier) - 1), userId });
        }

        if (nextQuestion && servedIds.includes(Number(nextQuestion.id))) {
            // Never re-serve the same card; fall back to any other item.
            nextQuestion = await qbank.pick({ skillId: raw.skill_id, tier: Math.min(4, Number(raw.tier) + 1), userId });
        }
        const questionIds = nextQuestion ? [...servedIds, Number(nextQuestion.id)] : servedIds;

        await query(
            `UPDATE session_focus_items
             SET correct_count = ?, attempts = ?, status = ?, question_ids = ?,
                 started_at = COALESCE(started_at, NOW()),
                 completed_at = ${itemDone ? 'NOW()' : 'completed_at'}
             WHERE id = ?`,
            [correctCount, attempts, itemDone ? 'done' : 'active', JSON.stringify(questionIds), item.id]
        );

        // ---- rewards
        let reward = { xpAwarded: 0, gemsAwarded: 0 };
        if (correct) {
            const r = await award(userId, `session:${sessionId}:q:${raw.id}`, mastery.REWARDS.correct);
            reward = { xpAwarded: r.xpAwarded, gemsAwarded: r.gemsAwarded };
        }
        let itemReward = { xpAwarded: 0, gemsAwarded: 0 };
        if (itemDone) {
            itemReward = await award(userId, `session:${sessionId}:item:${item.id}`, mastery.REWARDS.item);
        }

        const seq = await nextSeq(sessionId);
        await logEvent(sessionId, seq, 'answer', raw.skill_id, raw.id, {
            correct,
            tier: Number(raw.tier),
            hints: hintsUsed,
            assistance,
            verdict: correct ? 'correct' : 'incorrect',
            next
        });

        if (itemDone) {
            await query('UPDATE sessions SET item_index = item_index + 1, last_active_at = NOW() WHERE id = ?', [sessionId]);
        } else {
            await query('UPDATE sessions SET last_active_at = NOW() WHERE id = ?', [sessionId]);
        }

        const selectedOption = parseJson(raw.options, []).find(
            (o) => String(o.k).toUpperCase() === given
        );

        const showSolution = !correct && attempts >= 2;
        const nextCard = nextQuestion ? qbank.toCard(nextQuestion) : null;

        return {
            ok: true,
            verdict: correct ? 'correct' : 'incorrect',
            correct,
            // Released only now, never before grading:
            why: correct ? '' : qbank.whyFor(raw, given),
            selected: selectedOption ? selectedOption.t : '',
            hint: correct ? '' : String(parseJson(raw.hints, [])[Math.min(hintsUsed, parseJson(raw.hints, []).length - 1)] || ''),
            solution: showSolution ? qbank.solutionFor(raw) : null,
            next,
            question: nextCard,
            item: {
                id: Number(item.id),
                skillId: Number(raw.skill_id),
                name: item.skill_name,
                correctCount,
                attempts,
                needed: need,
                done: itemDone
            },
            mastery: m,
            reward: {
                xp: reward.xpAwarded + itemReward.xpAwarded,
                gems: reward.gemsAwarded + itemReward.gemsAwarded
            },
            totals: await rewardTotals(userId)
        };
    }

    // ------------------------------------------------------------------- hint
    async function hint(userId, sessionId, { questionId } = {}) {
        const session = await sessionRow(userId, sessionId);
        if (!session) return { error: 404, message: 'Session not found' };
        if (session.status !== 'active') return { error: 409, message: 'This session is not active' };

        const raw = await qbank.getRaw(questionId);
        if (!raw) return { error: 400, message: 'Unknown question' };

        const rows = await query(
            "SELECT COUNT(*) AS c FROM session_events WHERE session_id = ? AND kind = 'hint' AND question_id = ?",
            [sessionId, raw.id]
        );
        const used = Number(rows[0]?.c || 0);
        const hints = parseJson(raw.hints, []);
        if (used >= hints.length) {
            return { ok: true, hint: hints[hints.length - 1] || '', level: used, exhausted: true };
        }

        const seq = await nextSeq(sessionId);
        await logEvent(sessionId, seq, 'hint', raw.skill_id, raw.id, { level: used + 1 });

        return { ok: true, hint: hints[used], level: used + 1, exhausted: used + 1 >= hints.length };
    }

    // ------------------------------------------------------------------- skip
    async function skip(userId, sessionId, { itemId } = {}) {
        const session = await sessionRow(userId, sessionId);
        if (!session) return { error: 404, message: 'Session not found' };
        const items = await focusItems(sessionId);
        const item = items.find((i) => Number(i.id) === Number(itemId));
        if (!item) return { error: 400, message: 'Unknown focus item' };

        await query("UPDATE session_focus_items SET status = 'deferred' WHERE id = ?", [item.id]);
        const seq = await nextSeq(sessionId);
        await logEvent(sessionId, seq, 'skip', item.skill_id, null, { itemId: Number(item.id) });
        await query('UPDATE sessions SET item_index = item_index + 1, last_active_at = NOW() WHERE id = ?', [sessionId]);

        const done = items.filter((i) => i.status === 'done').length;
        const pending = items.filter((i) => i.status === 'pending' || i.status === 'active').length - 1;
        return { ok: true, remaining: Math.max(0, pending), done, total: items.length, state: await state(userId, sessionId) };
    }

    // -------------------------------------------------------------------- end
    async function end(userId, sessionId, { reason, rating } = {}) {
        const session = await sessionRow(userId, sessionId);
        if (!session) return { error: 404, message: 'Session not found' };
        if (session.status === 'completed') {
            const s = await state(userId, sessionId);
            return { ok: true, alreadyEnded: true, state: s };
        }

        const items = await focusItems(sessionId);
        const done = items.filter((i) => i.status === 'done');
        const touched = items.filter((i) => i.status === 'done' || i.status === 'deferred' || i.status === 'active');
        const minutes = Math.round(Number(session.elapsed_s || 0) / 60);
        const reachedGoal = done.length >= items.length || (reason === 'goal' && done.length > 0);

        let goalReward = { xpAwarded: 0, gemsAwarded: 0 };
        if (done.length > 0) {
            goalReward = await award(userId, `session:${sessionId}:goal`, mastery.REWARDS.goal);
        }

        const names = done.map((i) => i.skill_name);
        const summary =
            done.length === 0
                ? `You looked at ${touched.length} topic${touched.length === 1 ? '' : 's'} but didn't finish a focus item. That's fine — pick up here next time.`
                : `You moved ${done.length} of ${items.length} focus item${items.length === 1 ? '' : 's'} forward${
                      names.length ? `: ${names.slice(0, 3).join(', ')}` : ''
                  }. ${minutes} minute${minutes === 1 ? '' : 's'} of focused practice.`;

        const nextRows = await query(
            `SELECT s.name FROM review_queue r JOIN skills s ON s.id = r.skill_id
             WHERE r.user_id = ? ORDER BY r.due_at ASC LIMIT 1`,
            [userId]
        );
        const nextStep = nextRows[0]?.name ? `Next up: ${nextRows[0].name}` : 'Start a new session when you are ready.';

        try {
            await query(
                `INSERT IGNORE INTO session_summaries (session_id, user_id, summary, skills_touched, next_step)
                 VALUES (?, ?, ?, ?, ?)`,
                [
                    sessionId,
                    userId,
                    summary.slice(0, 600),
                    JSON.stringify(done.map((i) => ({ skillId: Number(i.skill_id), name: i.skill_name }))),
                    nextStep.slice(0, 200)
                ]
            );
        } catch (e) {
            info(`[session] summary insert skipped: ${e.message}`);
        }

        const stars = parseInt(rating, 10);
        await query(
            `UPDATE sessions
             SET status = 'completed', ended_at = NOW(), last_active_at = NOW(),
                 xp_awarded = xp_awarded + ?, gems_awarded = gems_awarded + ?,
                 rating = COALESCE(?, rating)
             WHERE id = ?`,
            [
                goalReward.xpAwarded,
                goalReward.gemsAwarded,
                Number.isFinite(stars) && stars >= 1 && stars <= 5 ? stars : null,
                sessionId
            ]
        );
        await logEvent(sessionId, await nextSeq(sessionId), 'end', null, null, {
            reason: reason || (reachedGoal ? 'goal' : 'quit'),
            done: done.length,
            total: items.length,
            rating: Number.isFinite(stars) ? stars : null
        });

        return {
            ok: true,
            reachedGoal,
            summary,
            nextStep,
            done: done.length,
            total: items.length,
            minutes,
            reward: { xp: goalReward.xpAwarded, gems: goalReward.gemsAwarded },
            totals: await rewardTotals(userId),
            state: await state(userId, sessionId)
        };
    }

    /** Stars live on the session so the creator's quality multiplier can read them. */
    async function rate(userId, sessionId, { rating } = {}) {
        const stars = parseInt(rating, 10);
        if (!Number.isFinite(stars) || stars < 1 || stars > 5) {
            return { error: 400, message: 'Rate this session from 1 to 5' };
        }
        const rows = await query('SELECT id FROM sessions WHERE id = ? AND user_id = ? LIMIT 1', [sessionId, userId]);
        if (!rows.length) return { error: 404, message: 'Session not found' };
        await query('UPDATE sessions SET rating = ? WHERE id = ?', [stars, sessionId]);
        await logEvent(sessionId, await nextSeq(sessionId), 'session.rate', null, null, { rating: stars });
        return { ok: true, rating: stars };
    }

    async function active(userId) {
        const rows = await query(
            "SELECT id FROM sessions WHERE user_id = ? AND status = 'active' ORDER BY id DESC LIMIT 1",
            [userId]
        );
        if (!rows.length) return { session: null };
        const s = await state(userId, rows[0].id);
        if (!s) return { session: null };
        return {
            session: s.session,
            item: s.item,
            progress: s.progress,
            resumeLabel: s.item ? `${s.item.name} · item ${s.progress.done + 1} of ${s.progress.total}` : ''
        };
    }

    async function history(userId, { limit, q } = {}) {
        const n = mastery.clamp(limit || 20, 1, 50);
        const term = String(q || '').trim();
        const base = `SELECT se.id, se.minutes, se.status, se.started_at, se.ended_at, se.xp_awarded,
                             se.mode, se.rating, se.course_id, se.goal_text, su.summary, su.next_step
                      FROM sessions se
                      LEFT JOIN session_summaries su ON su.session_id = se.id
                      WHERE se.user_id = ?`;
        // QoL 26: the Sessions pane searches skills and summaries, not just dates.
        const rows = term
            ? await query(
                  `${base} AND (su.summary LIKE ? OR se.id IN (
                        SELECT f.session_id FROM session_focus_items f
                        JOIN skills sk ON sk.id = f.skill_id
                        WHERE sk.name LIKE ?))
                   ORDER BY se.id DESC LIMIT ?`,
                  [userId, `%${term}%`, `%${term}%`, n]
              )
            : await query(`${base} ORDER BY se.id DESC LIMIT ?`, [userId, n]);
        return rows.map((r) => ({
            id: Number(r.id),
            minutes: Number(r.minutes || 0),
            status: r.status,
            mode: r.mode || 'focus',
            goal: r.goal_text || '',
            rating: r.rating != null ? Number(r.rating) : null,
            courseId: r.course_id != null ? Number(r.course_id) : null,
            startedAt: r.started_at,
            endedAt: r.ended_at,
            xp: Number(r.xp_awarded || 0),
            summary: r.summary || '',
            nextStep: r.next_step || ''
        }));
    }

    return { active, answer, end, extend, hint, history, mapFor, rate, skip, start, state, teach };
}

module.exports = createSessionEngine;
module.exports.parseJson = parseJson;
