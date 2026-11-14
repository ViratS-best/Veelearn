'use strict';

/**
 * P5 — the quality-of-life layer: exam sprint, teacher-assigned sessions, the
 * parent digest, flashcards, read-aloud support, session history and notes.
 *
 * Everything here is a read or a small write over data the session engine
 * already records. Nothing in this file needs a model: the digest and the
 * transcript are written from the ledger of what actually happened, which is
 * also what makes them trustworthy enough to email a parent.
 */

const DAY = 24 * 60 * 60 * 1000;
const EXAM_WINDOW_DAYS = 45;
const SPRINT_ITEMS = 6;

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

function isoDate(d) {
    return new Date(d).toISOString().slice(0, 10);
}

function daysBetween(a, b) {
    return Math.ceil((new Date(b).getTime() - new Date(a).getTime()) / DAY);
}

function csvCell(value) {
    const text = String(value == null ? '' : value).replace(/\s+/g, ' ').trim();
    return `"${text.replace(/"/g, '""')}"`;
}

function createPhase5({ query, log, sendEmail } = {}) {
    const info = (log && log.info) || (() => {});

    async function userRow(userId) {
        const rows = await query(
            'SELECT id, email, exam_date, parent_email, digest_opt_in, reminder_at FROM users WHERE id = ? LIMIT 1',
            [userId]
        );
        return rows[0] || null;
    }

    // ------------------------------------------------------------- exam sprint
    async function setExam({ userId, date }) {
        const value = date ? isoDate(date) : null;
        if (value && Number.isNaN(new Date(value).getTime())) {
            const err = new Error('That exam date is not a date');
            err.status = 400;
            throw err;
        }
        await query('UPDATE users SET exam_date = ? WHERE id = ?', [value, userId]);
        return examStatus(userId);
    }

    async function examStatus(userId) {
        const user = await userRow(userId);
        if (!user) {
            const err = new Error('User not found');
            err.status = 404;
            throw err;
        }
        if (!user.exam_date) return { examDate: null, daysLeft: null, sprintAvailable: false, offer: null };
        const daysLeft = daysBetween(new Date(), user.exam_date);
        const sprintAvailable = daysLeft >= 0 && daysLeft <= EXAM_WINDOW_DAYS;
        return {
            examDate: isoDate(user.exam_date),
            daysLeft,
            sprintAvailable,
            offer: sprintAvailable
                ? `Exam in ${daysLeft} day${daysLeft === 1 ? '' : 's'} — a ${SPRINT_ITEMS}-item sprint targets your weakest skills.`
                : null
        };
    }

    /**
     * The sprint plan (§16.3): the weakest skills, one due review, and a mixed
     * finish. Six items, shorter teach text, timed — the engine replays it
     * exactly like a focus plan, only the planner differs.
     */
    async function sprintPlan({ userId }) {
        const weak = await query(
            `SELECT sm.skill_id, sm.p, sm.level, sk.name, sk.track
             FROM skill_mastery sm
             JOIN skills sk ON sk.id = sm.skill_id
             WHERE sm.user_id = ? AND sm.level < 4
             ORDER BY sm.p ASC, sm.last_seen ASC
             LIMIT 12`,
            [userId]
        );
        const due = await query(
            `SELECT rq.skill_id, sk.name
             FROM review_queue rq
             JOIN skills sk ON sk.id = rq.skill_id
             WHERE rq.user_id = ? AND rq.due_at <= NOW()
             ORDER BY rq.due_at ASC LIMIT 3`,
            [userId]
        );

        const picks = [];
        const seen = new Set();
        for (const row of due.slice(0, 1)) {
            const id = Number(row.skill_id);
            if (seen.has(id)) continue;
            seen.add(id);
            picks.push({ skillId: id, skillName: row.name, isReview: 1, targetDots: 2, startTier: 3 });
        }
        for (const row of weak) {
            if (picks.length >= SPRINT_ITEMS) break;
            const id = Number(row.skill_id);
            if (seen.has(id)) continue;
            seen.add(id);
            picks.push({
                skillId: id,
                skillName: row.name,
                isReview: 0,
                targetDots: 2,
                startTier: Number(row.level) >= 2 ? 3 : 1
            });
        }

        // A sprint is always six stops: top up from the learner's own track so a
        // new learner with two measured skills still gets a full plan.
        if (picks.length < SPRINT_ITEMS) {
            const trackRows = await query(
                `SELECT s.track FROM sessions se
                 JOIN session_focus_items f ON f.session_id = se.id
                 JOIN skills s ON s.id = f.skill_id
                 WHERE se.user_id = ? ORDER BY se.id DESC LIMIT 1`,
                [userId]
            );
            const chosen = trackRows[0]?.track || weak[0]?.track || 'math.g8';
            const extra = await query(
                'SELECT id, name FROM skills WHERE track = ? ORDER BY order_index ASC LIMIT ?',
                [chosen, SPRINT_ITEMS * 2]
            );
            for (const row of extra) {
                if (picks.length >= SPRINT_ITEMS) break;
                const id = Number(row.id);
                if (seen.has(id)) continue;
                seen.add(id);
                picks.push({ skillId: id, skillName: row.name, isReview: 0, targetDots: 2, startTier: 1 });
            }
        }
        if (!picks.length) return { items: [], reason: 'no-skills' };

        return {
            items: picks.slice(0, SPRINT_ITEMS).map((p, i) => Object.assign({ ord: i }, p)),
            count: Math.min(SPRINT_ITEMS, picks.length),
            minutes: 25
        };
    }

    // -------------------------------------------------------------- transcript
    /** Markdown evidence a teacher or a parent can read without the app. */
    async function transcript({ userId, sessionId }) {
        const rows = await query(
            `SELECT s.id, s.started_at, s.ended_at, s.minutes, s.mode, s.course_id, s.rating,
                    su.summary, su.next_step
             FROM sessions s
             LEFT JOIN session_summaries su ON su.session_id = s.id
             WHERE s.id = ? AND s.user_id = ? LIMIT 1`,
            [sessionId, userId]
        );
        const session = rows[0];
        if (!session) {
            const err = new Error('Session not found');
            err.status = 404;
            throw err;
        }

        const items = await query(
            `SELECT f.ord, f.status, f.attempts, f.correct_count, sk.name
             FROM session_focus_items f
             JOIN skills sk ON sk.id = f.skill_id
             WHERE f.session_id = ? ORDER BY f.ord ASC`,
            [sessionId]
        );
        const answers = await query(
            `SELECT a.question_id, a.correct, a.answer_given, a.ms_taken, a.created_at, q.stem, q.answer
             FROM practice_attempts a
             LEFT JOIN qbank_items q ON q.id = a.question_id
             WHERE a.session_id = ? ORDER BY a.id ASC`,
            [sessionId]
        );
        const events = await query(
            "SELECT kind, payload, created_at FROM session_events WHERE session_id = ? AND kind = 'session.ai' ORDER BY id ASC",
            [sessionId]
        );

        const started = session.started_at ? new Date(session.started_at) : new Date();
        const minutes = session.ended_at
            ? Math.max(1, Math.round((new Date(session.ended_at) - started) / 60000))
            : Number(session.minutes || 0);

        const lines = [];
        lines.push(`# Veelearn session — ${isoDate(started)}`);
        lines.push('');
        lines.push(`- Mode: ${session.mode || 'focus'}`);
        lines.push(`- Length: ${minutes} min`);
        if (session.rating) lines.push(`- Learner rating: ${session.rating}/5`);
        lines.push('');
        if (session.summary) {
            lines.push(`**Summary.** ${session.summary}`);
            lines.push('');
        }
        lines.push('## Skills worked');
        for (const item of items) {
            const state = item.status === 'done' ? 'done' : item.status || 'pending';
            lines.push(`- ${item.name} — ${state}, ${Number(item.attempts || 0)} attempt(s)`);
        }
        if (answers.length) {
            lines.push('');
            lines.push('## Answers');
            for (const a of answers) {
                const verdict = Number(a.correct) === 1 ? 'correct' : 'wrong';
                const stem = String(a.stem || `Question ${a.question_id}`).replace(/\s+/g, ' ').slice(0, 140);
                lines.push(`- ${verdict} — ${stem}`);
            }
        }
        if (events.length) {
            lines.push('');
            lines.push('## AI explanations');
            for (const e of events) {
                const payload = parseJson(e.payload, {}) || {};
                if (payload.say) lines.push(`- ${String(payload.say).replace(/\s+/g, ' ')}`);
            }
        }
        lines.push('');
        if (session.next_step) {
            lines.push(`**Next step.** ${session.next_step}`);
            lines.push('');
        }
        lines.push('_Generated from the session ledger; no transcript of the chat itself is stored._');

        return {
            sessionId: Number(sessionId),
            markdown: lines.join('\n'),
            filename: `veelearn-session-${sessionId}.md`
        };
    }

    // -------------------------------------------------------------- flashcards
    /** Every wrong answer can become a card (QoL 9); export is Anki-ready CSV. */
    async function flashcardsFromSession({ userId, sessionId, questionIds }) {
        const wanted = Array.isArray(questionIds) && questionIds.length ? questionIds.map(Number) : null;
        const misses = await query(
            `SELECT a.question_id, a.skill_id, q.stem, q.answer, q.solution_steps, q.options
             FROM practice_attempts a
             JOIN qbank_items q ON q.id = a.question_id
             WHERE a.session_id = ? AND a.user_id = ? AND a.correct = 0`,
            [sessionId, userId]
        );
        const created = [];
        for (const row of misses) {
            const questionId = Number(row.question_id);
            if (wanted && !wanted.includes(questionId)) continue;
            const steps = parseJson(row.solution_steps, []) || [];
            const back = steps.length ? String(steps[steps.length - 1]) : String(row.answer);
            try {
                const res = await query(
                    `INSERT IGNORE INTO session_flashcards (user_id, question_id, skill_id, front, back, source, due_at)
                     VALUES (?, ?, ?, ?, ?, 'miss', NOW())`,
                    [
                        userId,
                        questionId,
                        row.skill_id || null,
                        String(row.stem || '').slice(0, 900),
                        String(back).slice(0, 900)
                    ]
                );
                const header = Array.isArray(res) ? res[0] : res;
                // INSERT IGNORE reports zero rows when the card already exists,
                // so "created" stays honest on a second pass over the misses.
                if ((header && header.affectedRows ? header.affectedRows : 0) > 0) created.push(questionId);
            } catch (e) {
                info(`[phase5] card skipped: ${e.message}`);
            }
        }
        const cards = await query(
            'SELECT id, question_id, skill_id, front, back, reps, due_at FROM session_flashcards WHERE user_id = ? ORDER BY due_at ASC LIMIT 100',
            [userId]
        );
        return { created: created.length, questionIds: created, cards };
    }

    async function dueCards({ userId, limit }) {
        const cap = Math.min(100, Math.max(1, parseInt(limit, 10) || 30));
        const rows = await query(
            `SELECT id, question_id, skill_id, front, back, ease, reps, due_at
             FROM session_flashcards WHERE user_id = ? AND (due_at IS NULL OR due_at <= NOW())
             ORDER BY due_at ASC LIMIT ?`,
            [userId, cap]
        );
        return { cards: rows, due: rows.length };
    }

    /** SM-2 lite, same shape as the review queue: good pushes the card out. */
    async function reviewCard({ userId, cardId, grade }) {
        const rows = await query('SELECT id, ease, reps FROM session_flashcards WHERE id = ? AND user_id = ? LIMIT 1', [
            cardId,
            userId
        ]);
        const card = rows[0];
        if (!card) {
            const err = new Error('Card not found');
            err.status = 404;
            throw err;
        }
        const g = Math.min(3, Math.max(0, parseInt(grade, 10) || 0));
        const ease = Math.max(1.3, Number(card.ease || 2.5) + (g === 3 ? 0.1 : g === 0 ? -0.2 : 0));
        const reps = Number(card.reps || 0) + 1;
        const days = g === 0 ? 1 : g === 1 ? 3 : Math.round(ease * reps);
        const dueAt = new Date(Date.now() + days * DAY).toISOString();
        await query('UPDATE session_flashcards SET ease = ?, reps = ?, due_at = ? WHERE id = ?', [ease, reps, dueAt, cardId]);
        return { id: Number(cardId), ease, reps, dueAt, days };
    }

    async function cardsCsv(userId) {
        const rows = await query(
            'SELECT front, back, skill_id, reps FROM session_flashcards WHERE user_id = ? ORDER BY id ASC',
            [userId]
        );
        const lines = ['front,back,tags'];
        for (const row of rows) {
            lines.push([csvCell(row.front), csvCell(row.back), csvCell(`veelearn skill:${row.skill_id || 'none'}`)].join(','));
        }
        return { csv: lines.join('\n'), count: rows.length };
    }

    // ------------------------------------------------------------------- notes
    /** The session summary doubles as a note, searchable later (QoL 10). */
    async function saveNote({ userId, sessionId }) {
        const rows = await query(
            `SELECT s.id, su.summary, su.next_step, su.skills_touched
             FROM sessions s LEFT JOIN session_summaries su ON su.session_id = s.id
             WHERE s.id = ? AND s.user_id = ? LIMIT 1`,
            [sessionId, userId]
        );
        const session = rows[0];
        if (!session) {
            const err = new Error('Session not found');
            err.status = 404;
            throw err;
        }
        if (!session.summary) {
            const err = new Error('That session has no summary yet');
            err.status = 409;
            throw err;
        }
        const skills = String(session.skills_touched || '').slice(0, 400);
        const body = `## ${isoDate(Date.now())} — session #${session.id}\n\n${session.summary}${
            session.next_step ? `\n\n**Next:** ${session.next_step}` : ''
        }`;
        await query(
            `INSERT INTO session_notes (user_id, session_id, body, skills) VALUES (?, ?, ?, ?)
             ON CONFLICT (session_id) DO UPDATE SET body = EXCLUDED.body, skills = EXCLUDED.skills`,
            [userId, session.id, body, skills]
        );
        return { sessionId: Number(session.id), body, skills };
    }

    async function notes({ userId, q }) {
        const term = String(q || '').trim();
        const rows = term
            ? await query(
                  'SELECT id, session_id, body, skills, created_at FROM session_notes WHERE user_id = ? AND (body LIKE ? OR skills LIKE ?) ORDER BY id DESC LIMIT 50',
                  [userId, `%${term}%`, `%${term}%`]
              )
            : await query(
                  'SELECT id, session_id, body, skills, created_at FROM session_notes WHERE user_id = ? ORDER BY id DESC LIMIT 50',
                  [userId]
              );
        return { notes: rows, count: rows.length };
    }

    // ----------------------------------------------------------------- digest
    async function setDigest({ userId, parentEmail, optIn }) {
        const email = String(parentEmail || '').trim();
        if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
            const err = new Error('That parent email does not look right');
            err.status = 400;
            throw err;
        }
        await query('UPDATE users SET parent_email = ?, digest_opt_in = ? WHERE id = ?', [
            email || null,
            optIn ? 1 : 0,
            userId
        ]);
        return { parentEmail: email || null, optIn: Boolean(optIn) };
    }

    /**
     * One email a week (QoL 25). The body is built from the ledger, stored so a
     * parent can be shown exactly what was sent, and only sent when the learner
     * opted in and an address exists.
     */
    async function digest({ userId, send = false, now = Date.now() } = {}) {
        const user = await userRow(userId);
        if (!user) {
            const err = new Error('User not found');
            err.status = 404;
            throw err;
        }
        const from = new Date(now - 7 * DAY).toISOString().slice(0, 10);
        const rows = await query(
            `SELECT s.id, s.started_at, s.ended_at, su.summary
             FROM sessions s LEFT JOIN session_summaries su ON su.session_id = s.id
             WHERE s.user_id = ? AND s.started_at >= ? ORDER BY s.id DESC`,
            [userId, from]
        );
        const gains = await query(
            `SELECT sm.skill_id, sk.name, sm.p, sm.level
             FROM skill_mastery sm JOIN skills sk ON sk.id = sm.skill_id
             WHERE sm.user_id = ? AND sm.last_seen >= ?
             ORDER BY sm.p DESC LIMIT 5`,
            [userId, from]
        );
        const minutes = rows.reduce((sum, r) => {
            const start = new Date(r.started_at || now).getTime();
            const end = r.ended_at ? new Date(r.ended_at).getTime() : start;
            return sum + Math.max(0, Math.round((end - start) / 60000));
        }, 0);

        const body = [
            `Veelearn weekly digest for ${user.email}`,
            '',
            `Sessions: ${rows.length}`,
            `Minutes practised: ${minutes}`,
            `Skills touched: ${gains.length}`,
            '',
            gains.length ? 'Strongest skills right now:' : 'No skills measured yet this week.',
            ...gains.map((g) => `- ${g.name} (level ${g.level}, mastery ${Math.round(Number(g.p || 0) * 100)}%)`),
            '',
            rows.find((r) => r.summary) ? `Latest note: ${rows.find((r) => r.summary).summary}` : ''
        ]
            .filter((line) => line !== '')
            .join('\n');

        const periodStart = from;
        const emailedTo = user.digest_opt_in && user.parent_email ? user.parent_email : null;
        let sent = false;
        if (send && emailedTo && typeof sendEmail === 'function') {
            try {
                await sendEmail({
                    to: emailedTo,
                    subject: `Veelearn: ${rows.length} session${rows.length === 1 ? '' : 's'} this week`,
                    html: `<pre style="font:14px/1.6 system-ui,sans-serif;white-space:pre-wrap">${body
                        .replace(/&/g, '&amp;')
                        .replace(/</g, '&lt;')}</pre>`
                });
                sent = true;
            } catch (e) {
                info(`[phase5] digest email failed: ${e.message}`);
            }
        }

        try {
            await query(
                `INSERT INTO parent_digests (user_id, period_start, period_end, body, emailed_to, sent_at)
                 VALUES (?, ?, ?, ?, ?, ?)
                 ON CONFLICT (user_id, period_start) DO UPDATE SET body = EXCLUDED.body, emailed_to = EXCLUDED.emailed_to, sent_at = EXCLUDED.sent_at`,
                [userId, periodStart, isoDate(now), body, emailedTo, sent ? new Date().toISOString() : null]
            );
        } catch (e) {
            info(`[phase5] digest store skipped: ${e.message}`);
        }

        return { body, sessions: rows.length, minutes, emailedTo, sent };
    }

    // ------------------------------------------------- teacher assignments
    /** "A 20-minute session on Unit 3, due Friday" (QoL 24). */
    async function assignSession({ teacherId, courseId, classCode, minutes, dueAt, unitIndex, title }) {
        const course = await query('SELECT id, title FROM courses WHERE id = ? LIMIT 1', [courseId]);
        if (!course.length) {
            const err = new Error('Course not found');
            err.status = 404;
            throw err;
        }
        let code = String(classCode || '').trim() || null;
        if (!code) {
            const mine = await query(
                'SELECT class_code FROM users WHERE id = ? AND class_code IS NOT NULL LIMIT 1',
                [teacherId]
            );
            code = mine[0]?.class_code || null;
        }
        const mins = Math.min(90, Math.max(5, parseInt(minutes, 10) || 20));
        const due = dueAt ? new Date(dueAt) : null;
        const inserted = await query(
            `INSERT INTO session_assignments (teacher_id, course_id, class_code, title, unit_index, minutes, due_at, status)
             VALUES (?, ?, ?, ?, ?, ?, ?, 'open')`,
            [
                teacherId,
                courseId,
                code,
                String(title || course[0].title).slice(0, 160),
                Math.max(0, parseInt(unitIndex, 10) || 0),
                mins,
                due ? due.toISOString() : null
            ]
        );
        const id = inserted.insertId || inserted[0]?.id || null;
        return { id, courseId: Number(courseId), classCode: code, minutes: mins, dueAt: due ? due.toISOString() : null };
    }

    async function assignmentsForStudent({ userId }) {
        const rows = await query(
            `SELECT sa.id, sa.course_id, sa.title, sa.minutes, sa.due_at, sa.unit_index, c.title AS course_title
             FROM session_assignments sa
             JOIN courses c ON c.id = sa.course_id
             WHERE sa.status = 'open'
               AND sa.class_code IS NOT NULL
               AND sa.class_code IN (SELECT class_code FROM student_enrollments WHERE student_id = ?)
             ORDER BY (sa.due_at IS NULL), sa.due_at ASC, sa.id DESC`,
            [userId]
        );
        return { assignments: rows, count: rows.length };
    }

    /** The teacher's own list, so mastery is reachable after a page reload. */
    async function assignmentsForTeacher({ teacherId }) {
        const rows = await query(
            `SELECT sa.id, sa.course_id, sa.title, sa.minutes, sa.due_at, sa.unit_index, sa.class_code,
                    c.title AS course_title
             FROM session_assignments sa
             JOIN courses c ON c.id = sa.course_id
             WHERE sa.teacher_id = ?
             ORDER BY sa.id DESC LIMIT 50`,
            [teacherId]
        );
        return { assignments: rows, count: rows.length };
    }

    /** Per-student mastery for one assignment (the teacher's view). */
    async function teacherMastery({ teacherId, assignmentId }) {
        const rows = await query(
            'SELECT id, course_id, class_code, minutes, due_at, title FROM session_assignments WHERE id = ? AND teacher_id = ? LIMIT 1',
            [assignmentId, teacherId]
        );
        const assignment = rows[0];
        if (!assignment) {
            const err = new Error('Assignment not found');
            err.status = 404;
            throw err;
        }
        const students = await query(
            `SELECT u.id, u.email FROM student_enrollments se
             JOIN users u ON u.id = se.student_id
             WHERE se.class_code = ? ORDER BY u.email ASC`,
            [assignment.class_code]
        );
        const skillRows = await query('SELECT skill_id FROM course_skills WHERE course_id = ?', [assignment.course_id]);
        const skillIds = skillRows.map((r) => Number(r.skill_id));
        const out = [];
        for (const student of students) {
            let mastered = 0;
            let avg = 0;
            if (skillIds.length) {
                const placeholders = skillIds.map(() => '?').join(', ');
                const m = await query(
                    `SELECT AVG(p) AS avg, SUM(CASE WHEN level >= 4 THEN 1 ELSE 0 END) AS mastered
                     FROM skill_mastery WHERE user_id = ? AND skill_id IN (${placeholders})`,
                    [student.id, ...skillIds]
                );
                avg = Number(m[0]?.avg || 0);
                mastered = Number(m[0]?.mastered || 0);
            }
            const done = await query(
                'SELECT COUNT(*) AS c FROM sessions WHERE user_id = ? AND course_id = ?',
                [student.id, assignment.course_id]
            );
            out.push({
                studentId: Number(student.id),
                email: student.email,
                mastery: Math.round(avg * 100),
                masteredSkills: mastered,
                skillsTracked: skillIds.length,
                sessions: Number(done[0]?.c || 0)
            });
        }
        return {
            assignment: {
                id: Number(assignment.id),
                title: assignment.title,
                courseId: Number(assignment.course_id),
                classCode: assignment.class_code,
                minutes: Number(assignment.minutes || 20),
                dueAt: assignment.due_at
            },
            students: out
        };
    }

    // ---------------------------------------------------------------- history
    /** The Sessions pane (QoL 26): past sessions, searchable by skill. */
    async function history({ userId, q, limit }) {
        const cap = Math.min(50, Math.max(1, parseInt(limit, 10) || 20));
        const term = String(q || '').trim();
        const base = `SELECT s.id, s.started_at, s.ended_at, s.minutes, s.mode, s.rating, s.course_id,
                             su.summary, su.next_step
                      FROM sessions s
                      LEFT JOIN session_summaries su ON su.session_id = s.id
                      WHERE s.user_id = ? AND s.status <> 'active'`;
        let rows;
        if (term) {
            rows = await query(
                `${base}
                 AND (su.summary LIKE ? OR s.id IN (
                     SELECT f.session_id FROM session_focus_items f
                     JOIN skills sk ON sk.id = f.skill_id
                     WHERE sk.name LIKE ?))
                 ORDER BY s.id DESC LIMIT ?`,
                [userId, `%${term}%`, `%${term}%`, cap]
            );
        } else {
            rows = await query(`${base} ORDER BY s.id DESC LIMIT ?`, [userId, cap]);
        }
        return {
            sessions: rows.map((r) => ({
                id: Number(r.id),
                startedAt: r.started_at,
                minutes: Number(r.minutes || 0),
                mode: r.mode,
                rating: r.rating,
                courseId: r.course_id ? Number(r.course_id) : null,
                summary: r.summary,
                nextStep: r.next_step
            })),
            count: rows.length
        };
    }

    async function setReminder({ userId, at }) {
        const value = at ? new Date(at) : null;
        if (value && Number.isNaN(value.getTime())) {
            const err = new Error('That reminder time is not a date');
            err.status = 400;
            throw err;
        }
        await query('UPDATE users SET reminder_at = ? WHERE id = ?', [value ? value.toISOString() : null, userId]);
        return { reminderAt: value ? value.toISOString() : null };
    }

    return {
        setExam,
        examStatus,
        sprintPlan,
        transcript,
        flashcardsFromSession,
        dueCards,
        reviewCard,
        cardsCsv,
        saveNote,
        notes,
        setDigest,
        digest,
        assignSession,
        assignmentsForTeacher,
        assignmentsForStudent,
        teacherMastery,
        history,
        setReminder
    };
}

module.exports = createPhase5;
module.exports.SPRINT_ITEMS = SPRINT_ITEMS;
module.exports.EXAM_WINDOW_DAYS = EXAM_WINDOW_DAYS;
module.exports.csvCell = csvCell;
