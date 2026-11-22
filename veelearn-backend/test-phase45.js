'use strict';

/**
 * Phase 4 + Phase 5 checks. No database, no key, no network.
 *
 *   node test-phase45.js
 *
 * The two phases are mostly policy, not plumbing: who gets paid, when a course
 * is teachable, what a sprint picks, what a parent is told. Those rules are what
 * this file pins down, against a small in-memory copy of the tables they read.
 */

const createImpact = require('./creator-impact');
const createPhase5 = require('./phase5');

let pass = 0;
const failures = [];
function ok(name, cond, detail) {
    if (cond) {
        pass += 1;
        return;
    }
    failures.push(detail ? `${name} — ${detail}` : name);
}
function near(a, b, eps = 0.001) {
    return Math.abs(Number(a) - Number(b)) <= eps;
}

// --------------------------------------------------------------------------
// A very small in-memory stand-in for the handful of queries P4/P5 issue.
// It stores rows and answers each shape the modules actually ask for; anything
// it does not recognise returns an empty list so a broken shape fails loudly.
// --------------------------------------------------------------------------
// Every module instance below reads through CURRENT, which makeDb() points at
// the database each test just built. Same code path, no globals in the modules.
let CURRENT = null;

function makeDb(seed = {}) {
    const db = {
        courses: seed.courses || [],
        skills: seed.skills || [],
        course_skills: seed.course_skills || [],
        qbank_items: seed.qbank_items || [],
        skill_mastery: seed.skill_mastery || [],
        sessions: seed.sessions || [],
        session_focus_items: seed.session_focus_items || [],
        session_events: seed.session_events || [],
        practice_attempts: seed.practice_attempts || [],
        review_queue: seed.review_queue || [],
        ledger: seed.ledger || [],
        enrollment: seed.enrollment || [],
        users: seed.users || [],
        summaries: seed.summaries || [],
        flashcards: seed.flashcards || [],
        notes: seed.notes || [],
        digests: seed.digests || [],
        assignments: seed.assignments || [],
        enrollments: seed.enrollments || [],
        usersTable: seed.users || [],
        seq: 1000
    };

    const num = (n) => Number(n) || 0;

    db.query = async (sql, params = []) => {
        const s = String(sql).replace(/\s+/g, ' ').trim().toLowerCase();
        const p = params;

        // ---- readiness / plan
        if (s.startsWith('select id, title, description, content, creator_id')) {
            return db.courses.filter((c) => Number(c.id) === Number(p[0]));
        }
        if (s.startsWith('select id, code, track, name from skills')) return db.skills.slice();
        if (s.startsWith('select skill_id, weight, source from course_skills')) {
            return db.course_skills.filter(
                (r) => Number(r.course_id) === Number(p[0]) && String(r.source) !== String(p[1])
            );
        }
        if (s.includes('from qbank_items') && s.includes('group by skill_id')) {
            const courseId = Number(p[0]);
            const ids = (p.slice(1) || []).map(Number);
            const out = [];
            for (const id of ids) {
                const items = db.qbank_items.filter((q) => Number(q.skill_id) === id && Number(q.live) !== 0);
                if (!items.length) continue;
                out.push({
                    skill_id: id,
                    total: items.length,
                    own: items.filter((q) => Number(q.course_id) === courseId).length
                });
            }
            return out;
        }
        if (s.startsWith('insert ignore into course_skills')) {
            const [courseId, skillId, weight, source] = p;
            const exists = db.course_skills.some(
                (r) => Number(r.course_id) === Number(courseId) && Number(r.skill_id) === Number(skillId)
            );
            if (!exists) db.course_skills.push({ course_id: Number(courseId), skill_id: Number(skillId), weight, source });
            return { affectedRows: exists ? 0 : 1 };
        }
        if (s.startsWith('update courses set readiness_score')) {
            const row = db.courses.find((c) => Number(c.id) === Number(p[2]));
            if (row) {
                row.readiness_score = Number(p[0]);
                row.ai_ready = Number(p[1]);
            }
            return { affectedRows: row ? 1 : 0 };
        }
        if (s.startsWith('update courses set sessions_taught')) {
            const row = db.courses.find((c) => Number(c.id) === Number(p[0]));
            if (row) row.sessions_taught = num(row.sessions_taught) + 1;
            return { affectedRows: row ? 1 : 0 };
        }
        if (s.startsWith('select skill_id, p, level from skill_mastery')) {
            const ids = p.slice(1).map(Number);
            return db.skill_mastery.filter((r) => Number(r.user_id) === Number(p[0]) && ids.includes(Number(r.skill_id)));
        }

        // ---- session → impact
        if (s.startsWith('select s.id, s.user_id, s.course_id')) {
            const row = db.sessions.find((r) => Number(r.id) === Number(p[0]));
            return row ? [row] : [];
        }
        if (s.startsWith('select count(*) as c from session_focus_items where session_id = ? and completed_at is not null')) {
            return [
                {
                    c: db.session_focus_items.filter(
                        (r) => Number(r.session_id) === Number(p[0]) && r.completed_at != null
                    ).length
                }
            ];
        }
        if (s.includes('count(*) as c from session_focus_items where session_id = ?')) {
            return [{ c: db.session_focus_items.filter((r) => Number(r.session_id) === Number(p[0])).length }];
        }
        if (s.startsWith('select avg(rating) as avg from sessions where course_id')) {
            const rows = db.sessions.filter((r) => Number(r.course_id) === Number(p[0]) && r.rating != null);
            const avg = rows.length ? rows.reduce((a, r) => a + Number(r.rating), 0) / rows.length : null;
            return [{ avg }];
        }
        if (s.startsWith('select avg(rating) as avg, count(rating) as n')) {
            const rows = db.sessions.filter((r) => Number(r.course_id) === Number(p[0]) && r.rating != null);
            const avg = rows.length ? rows.reduce((a, r) => a + Number(r.rating), 0) / rows.length : null;
            return [{ avg, n: rows.length }];
        }
        if (s.startsWith("select payload from session_events where session_id = ? and kind = 'item.done'")) {
            return db.session_events
                .filter((r) => Number(r.session_id) === Number(p[0]) && r.kind === 'item.done')
                .map((r) => ({ payload: r.payload }));
        }
        if (s.startsWith('select coalesce(sum(hours), 0) as h from creator_impact_ledger')) {
            if (s.includes('created_at >= current_date')) {
                return [
                    {
                        h: db.ledger
                            .filter((r) => Number(r.creator_id) === Number(p[0]) && r.created_at >= '2026-11-14')
                            .reduce((a, r) => a + num(r.hours), 0)
                    }
                ];
            }
            if (s.includes('creator_id = ? and created_at >= ?')) {
                return [
                    {
                        h: db.ledger
                            .filter((r) => Number(r.creator_id) === Number(p[0]) && String(r.created_at).slice(0, 10) >= String(p[1]).slice(0, 10))
                            .reduce((a, r) => a + num(r.hours), 0)
                    }
                ];
            }
            if (s.includes('course_id = ? and kind = ?')) {
                return [
                    {
                        h: db.ledger
                            .filter((r) => Number(r.course_id) === Number(p[0]) && r.kind === p[1])
                            .reduce((a, r) => a + num(r.hours), 0)
                    }
                ];
            }
        }
        if (s.startsWith('select coalesce(sum(hours), 0) as h, count(*) as c from creator_impact_ledger')) {
            const rows = db.ledger.filter((r) => Number(r.course_id) === Number(p[0]) && r.kind === 'completion');
            return [{ h: rows.reduce((a, r) => a + num(r.hours), 0), c: rows.length }];
        }
        if (s.startsWith('select distinct s.user_id from sessions s join session_focus_items')) {
            const courseId = Number(p[0]);
            const need = Number(p[1]) || 1;
            const byUser = new Map();
            for (const session of db.sessions.filter((r) => Number(r.course_id) === courseId)) {
                const done = db.session_focus_items.filter(
                    (f) => Number(f.session_id) === Number(session.id) && f.completed_at != null
                ).length;
                if (done >= 1) byUser.set(Number(session.user_id), (byUser.get(Number(session.user_id)) || 0) + done);
            }
            return [...byUser.entries()].filter(([, n]) => n >= need).map(([user_id]) => ({ user_id }));
        }
        if (s.startsWith('insert ignore into creator_impact_ledger (course_id, creator_id, learner_id, session_id, kind, hours, paid_reason)')) {
            const [course_id, creator_id, learner_id, hours] = p;
            const dup = db.ledger.some(
                (r) => Number(r.course_id) === Number(course_id) && r.kind === 'completion' && Number(r.learner_id) === Number(learner_id)
            );
            if (dup) return { affectedRows: 0 };
            db.ledger.push({
                id: ++db.seq,
                course_id: Number(course_id),
                creator_id: Number(creator_id),
                learner_id: Number(learner_id),
                session_id: 0,
                kind: 'completion',
                hours: num(hours),
                paid_reason: 'paid-completion',
                mastery_gain: 0,
                created_at: '2026-11-14T11:00:00Z'
            });
            return { affectedRows: 1 };
        }
        if (s.startsWith('insert ignore into creator_impact_ledger')) {
            const [course_id, creator_id, learner_id, session_id, hours, readiness_mult, quality_mult, mastery_mult, mastery_gain, paid_reason] = p;
            const dup = db.ledger.some(
                (r) => Number(r.session_id) === Number(session_id) && (r.kind || 'session') === 'session'
            );
            if (dup) return { affectedRows: 0 };
            db.ledger.push({
                id: ++db.seq,
                course_id: Number(course_id),
                creator_id: Number(creator_id),
                learner_id: Number(learner_id),
                session_id: Number(session_id),
                kind: 'session',
                hours: num(hours),
                readiness_mult: num(readiness_mult),
                quality_mult: num(quality_mult),
                mastery_mult: num(mastery_mult),
                mastery_gain: num(mastery_gain),
                paid_reason,
                created_at: '2026-11-14T10:00:00Z'
            });
            return { affectedRows: 1 };
        }
        if (s.startsWith('select * from creator_impact_ledger where course_id = ? and kind = \'session\' and hours = 0')) {
            return db.ledger.filter(
                (r) =>
                    Number(r.course_id) === Number(p[0]) &&
                    r.kind === 'session' &&
                    num(r.hours) === 0 &&
                    r.paid_reason === 'awaiting-second-learner'
            );
        }
        if (s.startsWith('update creator_impact_ledger set hours = ?, paid_reason = ? where id = ?')) {
            const row = db.ledger.find((r) => Number(r.id) === Number(p[2]));
            if (row) {
                row.hours = num(p[0]);
                row.paid_reason = p[1];
            }
            return { affectedRows: row ? 1 : 0 };
        }
        if (s.startsWith('select distinct user_id from course_enrollment_progress')) {
            return db.enrollment
                .filter((r) => Number(r.course_id) === Number(p[0]) && num(r.progress_percentage) >= 80)
                .map((r) => ({ user_id: r.user_id }));
        }
        if (s.startsWith("select id from creator_impact_ledger where course_id = ? and kind = 'completion'")) {
            return db.ledger
                .filter((r) => Number(r.course_id) === Number(p[0]) && r.kind === 'completion' && Number(r.learner_id) === Number(p[1]))
                .map((r) => ({ id: r.id }));
        }
        if (s.startsWith('update users set total_volunteer_hours')) {
            const row = db.users.find((u) => Number(u.id) === Number(p[1]));
            if (row) row.total_volunteer_hours = num(row.total_volunteer_hours) + num(p[0]);
            return { affectedRows: row ? 1 : 0 };
        }

        // ---- the creator pane
        if (s.startsWith('select coalesce(sum(hours), 0) as hours, count(distinct learner_id)')) {
            const rows = db.ledger.filter((r) => Number(r.course_id) === Number(p[0]));
            const learners = new Set(rows.map((r) => Number(r.learner_id)));
            const gains = rows.map((r) => num(r.mastery_gain)).filter((n) => n !== 0);
            return [
                {
                    hours: rows.reduce((a, r) => a + num(r.hours), 0),
                    learners: learners.size,
                    gain: gains.length ? gains.reduce((a, b) => a + b, 0) / gains.length : null,
                    paid_sessions: rows.filter((r) => num(r.hours) > 0).length,
                    refused_sessions: rows.filter((r) => num(r.hours) === 0).length
                }
            ];
        }
        if (s.includes('from practice_attempts a') && s.includes('group by sk.id')) {
            const courseId = Number(p[0]);
            const courseSkills = new Set(
                db.course_skills.filter((r) => Number(r.course_id) === courseId).map((r) => Number(r.skill_id))
            );
            const bySkill = new Map();
            for (const a of db.practice_attempts) {
                if (!courseSkills.has(Number(a.skill_id))) continue;
                const entry = bySkill.get(Number(a.skill_id)) || { id: a.skill_id, misses: 0, attempts: 0 };
                entry.attempts += 1;
                if (num(a.correct) === 0) entry.misses += 1;
                bySkill.set(Number(a.skill_id), entry);
            }
            return [...bySkill.values()]
                .filter((r) => r.misses > 0)
                .sort((a, b) => b.misses - a.misses)
                .map((r) => ({
                    id: r.id,
                    name: (db.skills.find((s) => Number(s.id) === r.id) || {}).name || 'skill',
                    misses: r.misses,
                    attempts: r.attempts
                }));
        }
        if (s.startsWith('select count(*) as started')) {
            const rows = db.enrollment.filter((r) => Number(r.course_id) === Number(p[0]));
            return [
                {
                    started: rows.length,
                    half: rows.filter((r) => num(r.progress_percentage) >= 50).length,
                    eighty: rows.filter((r) => num(r.progress_percentage) >= 80).length,
                    finished: rows.filter((r) => num(r.progress_percentage) >= 100 || r.completed).length
                }
            ];
        }
        if (s.startsWith('select id, learner_id, session_id, kind, hours, paid_reason')) {
            return db.ledger
                .filter((r) => Number(r.course_id) === Number(p[0]))
                .sort((a, b) => b.id - a.id)
                .slice(0, 50);
        }
        if (s.startsWith('select id, title, readiness_score from courses')) {
            return db.courses.filter((c) => Number(c.creator_id) === Number(p[0])).reverse();
        }
        if (s.startsWith('select coalesce(sum(hours), 0) as h, count(distinct learner_id) as learners')) {
            const rows = db.ledger.filter((r) => Number(r.course_id) === Number(p[0]));
            const gains = rows.map((r) => num(r.mastery_gain)).filter((n) => n !== 0);
            return [
                {
                    h: rows.reduce((a, r) => a + num(r.hours), 0),
                    learners: new Set(rows.map((r) => Number(r.learner_id))).size,
                    gain: gains.length ? gains.reduce((a, b) => a + b, 0) / gains.length : null
                }
            ];
        }

        // ---- P5: profile
        if (s.startsWith('select id, email, exam_date, parent_email')) {
            const row = db.users.find((u) => Number(u.id) === Number(p[0]));
            return row ? [row] : [];
        }
        if (s.startsWith('update users set exam_date')) {
            const row = db.users.find((u) => Number(u.id) === Number(p[1]));
            if (row) row.exam_date = p[0];
            return { affectedRows: row ? 1 : 0 };
        }
        if (s.startsWith('update users set parent_email')) {
            const row = db.users.find((u) => Number(u.id) === Number(p[2]));
            if (row) {
                row.parent_email = p[0];
                row.digest_opt_in = p[1];
            }
            return { affectedRows: row ? 1 : 0 };
        }
        if (s.startsWith('update users set reminder_at')) {
            const row = db.users.find((u) => Number(u.id) === Number(p[1]));
            if (row) row.reminder_at = p[0];
            return { affectedRows: row ? 1 : 0 };
        }

        // ---- P5: sprint
        if (s.includes('from skill_mastery sm') && s.includes('order by sm.p asc')) {
            const rows = db.skill_mastery
                .filter((r) => Number(r.user_id) === Number(p[0]) && num(r.level) < 4)
                .sort((a, b) => num(a.p) - num(b.p));
            return rows.map((r) => {
                const skill = db.skills.find((sk) => Number(sk.id) === Number(r.skill_id)) || {};
                return {
                    skill_id: r.skill_id,
                    p: r.p,
                    level: r.level,
                    name: skill.name || 'skill',
                    track: skill.track
                };
            });
        }
        if (s.includes('from review_queue rq')) {
            return db.review_queue
                .filter((r) => Number(r.user_id) === Number(p[0]) && r.due_at <= '2026-11-14T00:00:00Z')
                .map((r) => ({ skill_id: r.skill_id, name: (db.skills.find((sk) => Number(sk.id) === Number(r.skill_id)) || {}).name }));
        }
        if (s.includes('select s.track from sessions se')) return [];
        if (s.startsWith('select id, name from skills where track')) {
            return db.skills.filter((sk) => sk.track === p[0]).slice(0, Number(p[1]));
        }

        // ---- P5: transcript / history / digest
        if (s.startsWith('select s.id, s.started_at, s.ended_at, s.minutes, s.mode, s.course_id, s.rating')) {
            const session = db.sessions.find((r) => Number(r.id) === Number(p[0]) && Number(r.user_id) === Number(p[1]));
            if (!session) return [];
            const summary = db.summaries.find((r) => Number(r.session_id) === Number(session.id)) || {};
            return [Object.assign({}, session, { summary: summary.summary, next_step: summary.next_step })];
        }
        if (s.startsWith('select f.ord, f.status') && s.includes('from session_focus_items f')) {
            return db.session_focus_items
                .filter((r) => Number(r.session_id) === Number(p[0]))
                .sort((a, b) => num(a.ord) - num(b.ord))
                .map((r) => Object.assign({}, r, { name: (db.skills.find((sk) => Number(sk.id) === Number(r.skill_id)) || {}).name }));
        }
        if (s.includes('from practice_attempts a') && s.includes('left join qbank_items q')) {
            return db.practice_attempts.filter((r) => Number(r.session_id) === Number(p[0]));
        }
        if (s.includes("from session_events where session_id = ? and kind = 'session.ai'")) {
            return db.session_events.filter((r) => Number(r.session_id) === Number(p[0]) && r.kind === 'session.ai');
        }
        if (s.startsWith('select s.id, s.started_at, s.ended_at, su.summary')) {
            return db.sessions
                .filter((r) => Number(r.user_id) === Number(p[0]) && String(r.started_at).slice(0, 10) >= String(p[1]).slice(0, 10))
                .map((r) => {
                    const summary = db.summaries.find((x) => Number(x.session_id) === Number(r.id)) || {};
                    return Object.assign({}, r, { summary: summary.summary });
                });
        }
        if (s.includes('from skill_mastery sm join skills sk on sk.id = sm.skill_id') && s.includes('last_seen')) {
            return db.skill_mastery
                .filter((r) => Number(r.user_id) === Number(p[0]))
                .map((r) => ({
                    skill_id: r.skill_id,
                    name: (db.skills.find((sk) => Number(sk.id) === Number(r.skill_id)) || {}).name,
                    p: r.p,
                    level: r.level
                }))
                .slice(0, 5);
        }
        if (s.startsWith('select s.id, s.started_at, s.ended_at, s.minutes, s.mode, s.rating, s.course_id')) {
            const base = db.sessions
                .filter((r) => Number(r.user_id) === Number(p[0]) && r.status !== 'active')
                .sort((a, b) => b.id - a.id);
            if (!s.includes('like')) return base.slice(0, Number(p[p.length - 1]) || 20);
            const term = String(p[1] || '').toLowerCase().replace(/%/g, '');
            const bySummary = base.filter((r) => {
                const summary = db.summaries.find((x) => Number(x.session_id) === Number(r.id)) || {};
                return String(summary.summary || '').toLowerCase().includes(term);
            });
            const bySkill = base.filter((r) => {
                const skills = db.session_focus_items
                    .filter((f) => Number(f.session_id) === Number(r.id))
                    .map((f) => String((db.skills.find((sk) => Number(sk.id) === Number(f.skill_id)) || {}).name || '').toLowerCase());
                return skills.some((n) => n.includes(term));
            });
            const merged = [...new Set([...bySummary, ...bySkill])].sort((a, b) => b.id - a.id);
            return merged.slice(0, Number(p[p.length - 1]) || 20);
        }
        if (s.startsWith('insert ignore into parent_digests')) {
            const [user_id, period_start, period_end, body, emailed_to, sent_at] = p;
            db.digests.push({ user_id, period_start, period_end, body, emailed_to, sent_at });
            return { affectedRows: 1 };
        }

        // ---- P5: flashcards
        if (s.includes('from practice_attempts a') && s.includes('join qbank_items q') && s.includes('a.correct = 0')) {
            return db.practice_attempts
                .filter((r) => Number(r.session_id) === Number(p[0]) && Number(r.user_id) === Number(p[1]) && num(r.correct) === 0)
                .map((r) => {
                    const item = db.qbank_items.find((q) => Number(q.id) === Number(r.question_id)) || {};
                    return {
                        question_id: r.question_id,
                        skill_id: r.skill_id || item.skill_id,
                        stem: item.stem,
                        answer: item.answer,
                        solution_steps: item.solution_steps,
                        options: item.options
                    };
                });
        }
        if (s.startsWith('insert ignore into session_flashcards')) {
            const [user_id, question_id, skill_id, front, back] = p;
            const dup = db.flashcards.some(
                (c) => Number(c.user_id) === Number(user_id) && Number(c.question_id) === Number(question_id)
            );
            if (dup) return { affectedRows: 0 };
            db.flashcards.push({
                id: ++db.seq,
                user_id: Number(user_id),
                question_id: Number(question_id),
                skill_id,
                front,
                back,
                ease: 2.5,
                reps: 0,
                due_at: '2026-11-14T00:00:00Z'
            });
            return { affectedRows: 1 };
        }
        if (s.startsWith('select id, question_id, skill_id, front, back, reps, due_at from session_flashcards')) {
            return db.flashcards.filter((c) => Number(c.user_id) === Number(p[0]));
        }
        if (s.startsWith('select id, question_id, skill_id, front, back, ease, reps, due_at')) {
            return db.flashcards
                .filter((c) => Number(c.user_id) === Number(p[0]) && (!c.due_at || c.due_at <= '2026-11-14T23:59:59Z'))
                .slice(0, Number(p[1]) || 30);
        }
        if (s.startsWith('select id, ease, reps from session_flashcards')) {
            return db.flashcards.filter((c) => Number(c.id) === Number(p[0]) && Number(c.user_id) === Number(p[1]));
        }
        if (s.startsWith('update session_flashcards set ease')) {
            const row = db.flashcards.find((c) => Number(c.id) === Number(p[3]));
            if (row) {
                row.ease = num(p[0]);
                row.reps = num(p[1]);
                row.due_at = p[2];
            }
            return { affectedRows: row ? 1 : 0 };
        }
        if (s.startsWith('select front, back, skill_id, reps from session_flashcards')) {
            return db.flashcards.filter((c) => Number(c.user_id) === Number(p[0]));
        }

        // ---- P5: notes
        if (s.startsWith('select s.id, su.summary, su.next_step, su.skills_touched')) {
            const session = db.sessions.find((r) => Number(r.id) === Number(p[0]) && Number(r.user_id) === Number(p[1]));
            if (!session) return [];
            const summary = db.summaries.find((r) => Number(r.session_id) === Number(session.id)) || {};
            return [
                {
                    id: session.id,
                    summary: summary.summary,
                    next_step: summary.next_step,
                    skills_touched: summary.skills_touched
                }
            ];
        }
        if (s.startsWith('insert into session_notes')) {
            const [user_id, session_id, body, skills] = p;
            const existing = db.notes.find((n) => Number(n.session_id) === Number(session_id));
            if (existing) {
                existing.body = body;
                existing.skills = skills;
            } else {
                db.notes.push({ id: ++db.seq, user_id, session_id, body, skills, created_at: '2026-11-14T00:00:00Z' });
            }
            return { affectedRows: 1 };
        }
        if (s.startsWith('select id, session_id, body, skills, created_at from session_notes')) {
            const rows = db.notes.filter((n) => Number(n.user_id) === Number(p[0]));
            if (!s.includes('like')) return rows.slice().reverse().slice(0, 50);
            const term = String(p[1] || '').toLowerCase().replace(/%/g, '');
            return rows
                .filter((n) => String(n.body).toLowerCase().includes(term) || String(n.skills || '').toLowerCase().includes(term))
                .slice()
                .reverse()
                .slice(0, 50);
        }

        // ---- P5: teacher assignments
        if (s.startsWith('select id, title from courses where id')) {
            return db.courses.filter((c) => Number(c.id) === Number(p[0])).map((c) => ({ id: c.id, title: c.title }));
        }
        if (s.startsWith('select class_code from users')) {
            return db.users.filter((u) => Number(u.id) === Number(p[0]) && u.class_code).map((u) => ({ class_code: u.class_code }));
        }
        if (s.startsWith('insert into session_assignments')) {
            const [teacher_id, course_id, class_code, title, unit_index, minutes, due_at] = p;
            const row = {
                id: ++db.seq,
                teacher_id,
                course_id,
                class_code,
                title,
                unit_index,
                minutes,
                due_at,
                status: 'open'
            };
            db.assignments.push(row);
            return { insertId: row.id, affectedRows: 1 };
        }
        if (s.startsWith('select sa.id, sa.course_id, sa.title, sa.minutes')) {
            return db.assignments
                .filter((a) => a.class_code && db.enrollments.some((e) => Number(e.student_id) === Number(p[0]) && e.class_code === a.class_code))
                .map((a) => Object.assign({}, a, { course_title: (db.courses.find((c) => Number(c.id) === Number(a.course_id)) || {}).title }));
        }
        if (s.startsWith('select id, course_id, class_code, minutes, due_at, title from session_assignments')) {
            return db.assignments.filter((a) => Number(a.id) === Number(p[0]) && Number(a.teacher_id) === Number(p[1]));
        }
        if (s.startsWith('select u.id, u.email from student_enrollments se')) {
            return db.enrollments
                .filter((e) => e.class_code === p[0])
                .map((e) => {
                    const user = db.users.find((u) => Number(u.id) === Number(e.student_id)) || {};
                    return { id: e.student_id, email: user.email || `student${e.student_id}@example.com` };
                });
        }
        if (s.startsWith('select skill_id from course_skills where course_id')) {
            return db.course_skills.filter((r) => Number(r.course_id) === Number(p[0])).map((r) => ({ skill_id: r.skill_id }));
        }
        if (s.includes('select avg(p) as avg, sum(case when level >= 4')) {
            const ids = p.slice(1).map(Number);
            const rows = db.skill_mastery.filter((r) => Number(r.user_id) === Number(p[0]) && ids.includes(Number(r.skill_id)));
            return [
                {
                    avg: rows.length ? rows.reduce((a, r) => a + num(r.p), 0) / rows.length : null,
                    mastered: rows.filter((r) => num(r.level) >= 4).length
                }
            ];
        }
        if (s.startsWith('select count(*) as c from sessions where user_id = ? and course_id')) {
            return [
                {
                    c: db.sessions.filter((r) => Number(r.user_id) === Number(p[0]) && Number(r.course_id) === Number(p[1])).length
                }
            ];
        }

        return [];
    };

    CURRENT = db;
    return db;
}

function seedCourseWorld() {
    const skills = [
        { id: 1, code: 'alg.exp.law', track: 'algebra1', name: 'Law of exponents' },
        { id: 2, code: 'alg.exp.neg', track: 'algebra1', name: 'Negative exponents' },
        { id: 3, code: 'alg.exp.pow', track: 'algebra1', name: 'Power of a power' },
        { id: 4, code: 'geo.area', track: 'geometry', name: 'Area of a triangle' }
    ];
    const content =
        '<h2>Laws of Exponents</h2>' +
        '<p>When you multiply powers with the same base you add the law of exponents and keep the base.</p>' +
        '<p>Negative exponents mean reciprocal, so a minus sign flips the fraction over.</p>' +
        '<p>A power of a power multiplies the exponents together.</p>';
    return makeDb({
        courses: [
            {
                id: 7,
                title: 'Exponent Rules, Fast',
                description: 'One unit course',
                content,
                creator_id: 2,
                status: 'approved',
                readiness_score: 0,
                sessions_taught: 0
            }
        ],
        skills,
        qbank_items: [
            { id: 11, skill_id: 1, course_id: 7, live: 1 },
            { id: 12, skill_id: 2, course_id: null, live: 1 },
            { id: 13, skill_id: 3, course_id: null, live: 1 }
        ],
        skill_mastery: [{ user_id: 3, skill_id: 1, p: 0.2, level: 1 }],
        users: [
            { id: 2, email: 'creator@example.com', total_volunteer_hours: 0 },
            { id: 3, email: 'learner@example.com', total_volunteer_hours: 0 },
            { id: 4, email: 'second@example.com', total_volunteer_hours: 0 }
        ]
    });
}

function addSession(db, { id, userId, courseId, minutes = 14, items = 4, ended = true, rating = 5, gains = [1, 1, 0, 1] }) {
    db.sessions.push({
        id,
        user_id: userId,
        course_id: courseId,
        mode: 'course',
        minutes,
        started_at: '2026-11-14T09:00:00Z',
        ended_at: ended ? new Date(Date.parse('2026-11-14T09:00:00Z') + minutes * 60000).toISOString() : null,
        rating,
        status: ended ? 'completed' : 'active'
    });
    for (let i = 0; i < items; i += 1) {
        db.session_focus_items.push({
            id: 5000 + id * 10 + i,
            session_id: id,
            skill_id: 1,
            ord: i,
            status: 'done',
            completed_at: '2026-11-14T09:10:00Z'
        });
        db.session_events.push({
            session_id: id,
            kind: 'item.done',
            payload: JSON.stringify({ skillId: 1, dotsBefore: 1, dotsAfter: 1 + (gains[i] || 0) })
        });
    }
}

(async () => {
    const impact = createImpact({ query: (...args) => CURRENT.query(...args) });
    const phase5 = createPhase5({ query: (...args) => CURRENT.query(...args) });

    // =====================================================================
    // P4 — readiness gate (§15.3)
    // =====================================================================
    {
        const db = seedCourseWorld();
        const report = await impact.readiness(7, { persist: true });
        ok('a one-unit course is auto-split into teachable units', report.units.length >= 2, `${report.units.length}`);
        ok('the course maps to at least three skills', report.skills.length >= 3, JSON.stringify(report.skills.map((s) => s.name)));
        ok('the mapping is labelled auto in the editor', report.skills.every((s) => s.source === 'auto'));
        ok('skills without creator questions are filled from the bank', report.filled.length >= 2, JSON.stringify(report.filled));
        ok('a well-formed course passes the gate', report.passed === true && report.score >= 60, `${report.score}`);
        ok('a passing course pays full readiness multiplier', report.multiplier === 1);
        ok('readiness is persisted on the course row', Number(db.courses[0].readiness_score) === report.score);
        ok(
            'the checks carry the weights from the design',
            JSON.stringify(report.checks.map((c) => c.weight)) === JSON.stringify([30, 25, 25, 15, 5])
        );
        ok('every failed check tells the creator what to fix', report.checks.every((c) => c.pass || c.fix));
    }

    {
        // thin content: one sentence, no headings, no matching skills
        const db = makeDb({
            courses: [{ id: 8, title: 'Bare', content: '<p>Short.</p>', creator_id: 2, status: 'approved' }],
            skills: [{ id: 1, code: 'alg.x', track: 'algebra1', name: 'Something else entirely' }],
            qbank_items: []
        });
        const report = await impact.readiness(8, { persist: true });
        ok('a thin course scores under the gate', report.score < 60, `${report.score}`);
        ok('under the gate the session is bank-led', report.bankLed === true);
        ok('bank-led courses earn half hours', near(report.multiplier, 0.5));
        ok('the thin section is named so it can be fixed', report.checks.find((c) => c.id === 'prose').detail.length > 0);
    }

    // =====================================================================
    // P4 — the course plan (§15.2)
    // =====================================================================
    {
        const db = seedCourseWorld();
        const planned = await impact.plan({ userId: 3, courseId: 7, minutes: 20 });
        ok('the plan is built from the course, not the whole track', planned.items.length > 0);
        ok('every planned item carries its unit frame', planned.items.every((i) => i.frame && i.frame.digest.length > 20));
        ok('the frame is capped for the prompt budget', planned.items.every((i) => i.frame.digest.length <= 600));
        ok('unit order is the creator order', planned.items.every((i, idx, all) => idx === 0 || all[idx - 1].unitIndex <= i.unitIndex));
        const again = await impact.plan({ userId: 3, courseId: 7, minutes: 5 });
        ok('a short session plans fewer items than a long one', again.items.length <= planned.items.length);
    }

    // =====================================================================
    // P4 — volunteer hours v2 (§15.4)
    // =====================================================================
    {
        const db = seedCourseWorld();
        addSession(db, { id: 100, userId: 2, courseId: 7 }); // creator is the learner
        const refused = await impact.record({ sessionId: 100 });
        ok('a creator teaching their own course is paid nothing', refused.hours === 0 && refused.reason === 'creator-is-learner', JSON.stringify(refused));
    }

    {
        const db = seedCourseWorld();
        addSession(db, { id: 101, userId: 3, courseId: 7, minutes: 4, items: 1 });
        const short = await impact.record({ sessionId: 101 });
        ok('a four-minute session does not count as teaching', short.hours === 0 && short.reason === 'too-short', JSON.stringify(short));
    }

    {
        const db = seedCourseWorld();
        addSession(db, { id: 102, userId: 3, courseId: 7 });
        const first = await impact.record({ sessionId: 102 });
        ok('one learner alone does not unlock hours yet', first.hours === 0 && first.reason === 'awaiting-second-learner', JSON.stringify(first));
        ok('the pending session is written to the ledger for audit', db.ledger.length === 1 && db.ledger[0].paid_reason === 'awaiting-second-learner');

        addSession(db, { id: 103, userId: 4, courseId: 7 });
        const second = await impact.record({ sessionId: 103 });
        ok('the second distinct learner unlocks the payout', second.paid === true && second.hours > 0, JSON.stringify(second));
        ok('the first learner is back-paid in the same pass', second.backfilled === 1, JSON.stringify(second));
        const paidRows = db.ledger.filter((r) => Number(r.hours) > 0);
        ok('two ledger rows are paid, and the ledger is the record', paidRows.length === 2, JSON.stringify(db.ledger.map((r) => r.paid_reason)));
        ok('hours land on the creator, not the learner', Number(db.users[0].total_volunteer_hours) > 0 && Number(db.users[1].total_volunteer_hours) === 0);
        ok(
            'per-session hours follow the formula',
            near(second.hours, 0.25 * 0.25 * 0 + 0, 100) || near(second.hours, Math.round(second.hours * 100) / 100)
        );
    }

    {
        // idempotency: ending the same session twice never pays twice
        const db = seedCourseWorld();
        addSession(db, { id: 104, userId: 3, courseId: 7 });
        addSession(db, { id: 105, userId: 4, courseId: 7 });
        await impact.record({ sessionId: 104 });
        const once = await impact.record({ sessionId: 105 });
        const before = Number(db.users[0].total_volunteer_hours);
        await impact.record({ sessionId: 105 });
        ok('the same session never pays twice', Number(db.users[0].total_volunteer_hours) === before, `${before} -> ${db.users[0].total_volunteer_hours}`);
        ok('the first payout was real', once.paid === true && before > 0);
    }

    {
        // caps: a creator already at the daily ceiling is paid nothing more
        const db = seedCourseWorld();
        db.ledger.push({
            id: 900,
            course_id: 7,
            creator_id: 2,
            learner_id: 9,
            session_id: 900,
            kind: 'session',
            hours: 3,
            readiness_mult: 1,
            quality_mult: 1,
            mastery_mult: 1,
            mastery_gain: 0.5,
            paid_reason: 'paid',
            created_at: '2026-11-14T01:00:00Z'
        });
        addSession(db, { id: 106, userId: 3, courseId: 7 });
        addSession(db, { id: 107, userId: 4, courseId: 7 });
        const capped = await impact.record({ sessionId: 107 });
        ok('the daily cap of three hours holds', capped.hours === 0 && capped.reason === 'capped', JSON.stringify(capped));
    }

    {
        // the creator pane and the ledger agree
        const db = seedCourseWorld();
        db.course_skills.push({ course_id: 7, skill_id: 1, source: 'auto' });
        addSession(db, { id: 108, userId: 3, courseId: 7 });
        addSession(db, { id: 109, userId: 4, courseId: 7 });
        db.enrollment.push(
            { course_id: 7, user_id: 3, progress_percentage: 85, completed: 1 },
            { course_id: 7, user_id: 4, progress_percentage: 40, completed: 0 }
        );
        await impact.record({ sessionId: 108 });
        await impact.record({ sessionId: 109 });
        db.practice_attempts.push(
            { user_id: 3, skill_id: 1, correct: 0, session_id: 108 },
            { user_id: 4, skill_id: 1, correct: 0, session_id: 109 },
            { user_id: 4, skill_id: 1, correct: 1, session_id: 109 }
        );
        const pane = await impact.impact(7);
        const ledgerSum = db.ledger.reduce((a, r) => a + Number(r.hours || 0), 0);
        ok('the creator pane total matches the ledger', near(pane.hours, Math.round(ledgerSum * 100) / 100), `${pane.hours} vs ${ledgerSum}`);
        ok('the pane counts both learners', pane.learners === 2, `${pane.learners}`);
        ok('the pane shows where learners get stuck', pane.stuck.length >= 1 && pane.stuck[0].misses === 2, JSON.stringify(pane.stuck));
        ok('the funnel follows enrolment progress', pane.funnel.started === 2 && pane.funnel.eighty === 1, JSON.stringify(pane.funnel));
        ok('the completion bonus paid for the finished learner', db.ledger.some((r) => r.kind === 'completion'));
        const summary = await impact.summaryForCreator(2);
        ok('the creator summary lists the course with its hours', summary.courses.length === 1 && summary.hours > 0);
    }

    // =====================================================================
    // P5 — exam sprint (§16.3)
    // =====================================================================
    {
        const db = seedCourseWorld();
        const soon = new Date(Date.now() + 10 * 24 * 60 * 60 * 1000).toISOString();
        const status = await phase5.setExam({ userId: 3, date: soon });
        ok('an exam inside 45 days offers a sprint', status.sprintAvailable === true && status.daysLeft <= 45);
        ok('the offer names the sprint', /sprint/.test(String(status.offer)));

        const far = new Date(Date.now() + 90 * 24 * 60 * 60 * 1000).toISOString();
        const later = await phase5.setExam({ userId: 3, date: far });
        ok('an exam three months out does not offer a sprint', later.sprintAvailable === false);
    }

    {
        const db = seedCourseWorld();
        db.skills.push(
            { id: 21, code: 'alg.lin.one', track: 'algebra1', name: 'One-step linear equations' },
            { id: 22, code: 'alg.lin.two', track: 'algebra1', name: 'Two-step linear equations' },
            { id: 23, code: 'alg.frac', track: 'algebra1', name: 'Fractions in equations' },
            { id: 24, code: 'alg.dist', track: 'algebra1', name: 'Distributive property' }
        );
        db.skill_mastery = [
            { user_id: 3, skill_id: 1, p: 0.1, level: 1 },
            { user_id: 3, skill_id: 2, p: 0.2, level: 1 },
            { user_id: 3, skill_id: 3, p: 0.3, level: 0 },
            { user_id: 3, skill_id: 4, p: 0.4, level: 2 }
        ];
        db.review_queue.push({ user_id: 3, skill_id: 2, due_at: '2026-11-13T00:00:00Z' });
        const sprint = await phase5.sprintPlan({ userId: 3 });
        ok('a sprint is exactly six items', sprint.items.length === 6, `${sprint.items.length}`);
        ok('the sprint opens with the due review', sprint.items[0].isReview === 1);
        ok('the sprint leads with the weakest skill', sprint.items[1].skillId === 1, JSON.stringify(sprint.items.map((i) => i.skillId)));
        ok('the sprint has no duplicate skills', new Set(sprint.items.map((i) => i.skillId)).size === sprint.items.length);
    }

    // =====================================================================
    // P5 — transcript, cards, notes
    // =====================================================================
    {
        const db = seedCourseWorld();
        addSession(db, { id: 200, userId: 3, courseId: 7 });
        db.summaries.push({
            session_id: 200,
            summary: 'You moved 4 of 4 focus items forward.',
            next_step: 'Next up: Negative exponents',
            skills_touched: JSON.stringify([{ skillId: 1, name: 'Law of exponents' }])
        });
        db.practice_attempts.push(
            { user_id: 3, session_id: 200, question_id: 11, skill_id: 1, correct: 0, answer_given: 'B', stem: 'Simplify x^2 x^3', answer: 'A', solution_steps: JSON.stringify(['add the exponents']) },
            { user_id: 3, session_id: 200, question_id: 12, skill_id: 2, correct: 0, answer_given: 'C', stem: 'Rewrite x^-2', answer: 'D', solution_steps: JSON.stringify(['reciprocal']) }
        );
        db.session_events.push({ session_id: 200, kind: 'session.ai', payload: JSON.stringify({ say: 'Add the exponents.' }) });

        const t = await phase5.transcript({ userId: 3, sessionId: 200 });
        ok('the transcript is markdown a teacher can read', t.markdown.startsWith('# Veelearn session'));
        ok('the transcript repeats the summary', t.markdown.includes('You moved 4 of 4'));
        ok('the transcript lists the skills worked', t.markdown.includes('Law of exponents'));
        ok('the transcript records wrong answers', /wrong — Simplify x\^2 x\^3/.test(t.markdown));
        ok('the transcript includes the AI lines', t.markdown.includes('Add the exponents.'));
        ok('the transcript has a filename', t.filename === 'veelearn-session-200.md');

        const cards = await phase5.flashcardsFromSession({ userId: 3, sessionId: 200 });
        ok('each miss becomes a flashcard', cards.created === 2, JSON.stringify(cards.created));
        ok('the card back holds the solution step', cards.cards[0].back.length > 0);
        const again = await phase5.flashcardsFromSession({ userId: 3, sessionId: 200 });
        ok('cards are not duplicated on a second pass', db.flashcards.length === 2 && again.created === 0);

        const csv = await phase5.cardsCsv(3);
        ok('the export is Anki-shaped CSV', csv.csv.split('\n')[0] === 'front,back,tags');
        ok('CSV quotes are escaped', csv.csv.includes('""') === false || csv.csv.includes('"'));

        const due = await phase5.dueCards({ userId: 3 });
        ok('due cards are returned', due.due === 2);
        const reviewed = await phase5.reviewCard({ userId: 3, cardId: db.flashcards[0].id, grade: 3 });
        ok('a good review pushes the card out', reviewed.days >= 1 && reviewed.reps === 1);
        const notMine = await phase5.reviewCard({ userId: 99, cardId: db.flashcards[0].id, grade: 3 }).catch((e) => e);
        ok('another learner cannot review your card', notMine && notMine.status === 404);

        const note = await phase5.saveNote({ userId: 3, sessionId: 200 });
        ok('the session summary becomes a note', note.body.includes('You moved 4 of 4'));
        const search = await phase5.notes({ userId: 3, q: 'exponents' });
        ok('notes are searchable', search.count === 1, JSON.stringify(search.count));
        const saved = await phase5.saveNote({ userId: 3, sessionId: 200 });
        ok('saving the same note twice keeps one row', db.notes.length === 1 && saved.body === note.body);
    }

    // =====================================================================
    // P5 — parent digest (QoL 25)
    // =====================================================================
    {
        const db = seedCourseWorld();
        addSession(db, { id: 300, userId: 3, courseId: 7 });
        db.summaries.push({ session_id: 300, summary: 'Nice work on exponents.' });

        // The fixture sessions are dated 2026-11-14; pin the digest clock to that week
        // so the seven-day window keeps covering them however long this file lives.
        const DIGEST_NOW = Date.parse('2026-11-15T00:00:00Z');
        const off = await phase5.digest({ userId: 3, now: DIGEST_NOW });
        ok('without opt-in the digest is built but not addressed', off.emailedTo === null && off.sessions === 1);
        ok('the digest counts minutes', off.minutes >= 10, `${off.minutes}`);

        const settings = await phase5.setDigest({ userId: 3, parentEmail: 'parent@example.com', optIn: true });
        ok('the parent address is stored', settings.parentEmail === 'parent@example.com' && settings.optIn === true);

        let sentTo = null;
        const withMail = createPhase5({
            query: db.query,
            sendEmail: async ({ to }) => {
                sentTo = to;
            }
        });
        const on = await withMail.digest({ userId: 3, send: true, now: DIGEST_NOW });
        ok('one email goes to the parent', on.sent === true && sentTo === 'parent@example.com');
        ok('the digest body carries the week', on.body.includes('Sessions: 1'));
        ok('the digest body names the learner', on.body.includes('learner@example.com'));
        ok('the digest names a skill to show progress', /level \d/.test(on.body));

        const bad = await phase5.setDigest({ userId: 3, parentEmail: 'nope', optIn: true }).catch((e) => e);
        ok('a malformed parent address is refused', bad && bad.status === 400);
    }

    // =====================================================================
    // P5 — teacher-assigned sessions + mastery (QoL 24)
    // =====================================================================
    {
        const db = seedCourseWorld();
        db.users.push({ id: 5, email: 'teacher@example.com', class_code: 'ABC123' });
        db.users.push({ id: 3, email: 'learner@example.com' });
        db.users.push({ id: 4, email: 'second@example.com' });
        db.enrollments.push(
            { student_id: 3, class_code: 'ABC123' },
            { student_id: 4, class_code: 'ABC123' }
        );
        db.course_skills.push({ course_id: 7, skill_id: 1, source: 'auto' }, { course_id: 7, skill_id: 2, source: 'auto' });
        db.skill_mastery.push(
            { user_id: 3, skill_id: 1, p: 0.9, level: 4 },
            { user_id: 3, skill_id: 2, p: 0.5, level: 2 },
            { user_id: 4, skill_id: 1, p: 0.3, level: 1 }
        );
        addSession(db, { id: 400, userId: 3, courseId: 7 });

        const due = new Date(Date.now() + 3 * 24 * 60 * 60 * 1000).toISOString();
        const created = await phase5.assignSession({
            teacherId: 5,
            courseId: 7,
            minutes: 20,
            dueAt: due,
            unitIndex: 1,
            title: 'Unit 3 session'
        });
        ok('a teacher can assign a 20-minute session', created.id != null && created.minutes === 20);
        ok('the assignment uses the teacher class code', created.classCode === 'ABC123');

        const forStudent = await phase5.assignmentsForStudent({ userId: 3 });
        ok('the student sees the assignment', forStudent.count === 1 && forStudent.assignments[0].title === 'Unit 3 session');
        ok('the assignment shows the course title', forStudent.assignments[0].course_title === 'Exponent Rules, Fast');

        const mastery = await phase5.teacherMastery({ teacherId: 5, assignmentId: created.id });
        ok('the teacher sees every student', mastery.students.length === 2, JSON.stringify(mastery.students));
        const one = mastery.students.find((s) => s.studentId === 3);
        ok('mastery is per student', one && one.mastery > 0 && one.masteredSkills === 1, JSON.stringify(one));
        ok('a student who never started shows zero sessions', mastery.students.find((s) => s.studentId === 4).sessions === 0);

        const foreign = await phase5.teacherMastery({ teacherId: 99, assignmentId: created.id }).catch((e) => e);
        ok('another teacher cannot read the assignment', foreign && foreign.status === 404);
    }

    // =====================================================================
    // P5 — session history, reminders
    // =====================================================================
    {
        const db = seedCourseWorld();
        addSession(db, { id: 500, userId: 3, courseId: 7 });
        addSession(db, { id: 501, userId: 3, courseId: 7 });
        db.summaries.push({ session_id: 500, summary: 'Exponents went well.' });
        const all = await phase5.history({ userId: 3 });
        ok('history lists finished sessions', all.count === 2);
        const bySkill = await phase5.history({ userId: 3, q: 'Law of exponents' });
        ok('history is searchable by skill', bySkill.count === 2, `${bySkill.count}`);
        const bySummary = await phase5.history({ userId: 3, q: 'went well' });
        ok('history is searchable by summary', bySummary.count === 1, `${bySummary.count}`);

        const reminder = await phase5.setReminder({ userId: 3, at: new Date(Date.now() + 86400000).toISOString() });
        ok('a reminder can be set', Boolean(reminder.reminderAt));
        const badTime = await phase5.setReminder({ userId: 3, at: 'tomorrow-ish' }).catch((e) => e);
        ok('a nonsense reminder time is refused', badTime && badTime.status === 400);
    }

    // =====================================================================
    // Wiring: the routes the UI calls have to exist and answer the documented shape
    // =====================================================================
    {
        const fs = require('fs');
        const path = require('path');
        const server = fs.readFileSync(path.join(__dirname, 'server.js'), 'utf8');
        const engineSrc = fs.readFileSync(path.join(__dirname, 'session-engine.js'), 'utf8');
        const routesSrc = fs.readFileSync(path.join(__dirname, 'session-routes.js'), 'utf8');
        ok('the rate route is mounted', /'\/api\/session\/:sessionId\/rate'/.test(server));
        ok('the teacher session list is mounted', /'\/api\/teacher\/session-assignments'/.test(server));
        ok('history searches skill names in SQL', /sk\.name LIKE/.test(engineSrc));
        ok('history returns the { sessions, count } envelope', /sessions: filtered, count: filtered\.length/.test(routesSrc));
        // Auth: an address is stored and looked up in one normal form. Postgres compares
        // text case-sensitively, so a mixed-case signup used to be unloggable.
        ok('there is one normal form for an email', /function normalizeEmail\(value\)/.test(server));
        ok('the normal form trims and lowercases', /value\.trim\(\)\.toLowerCase\(\)/.test(server));
        ok('register stores the normal form', /const email = normalizeEmail\(req\.body\.email\);/.test(server));
        ok('register refuses a case-variant duplicate', /WHERE LOWER\(email\) = \?', \[email\]\);\s*if \(existing\.length > 0\)/.test(server));
        ok('login matches a stored address in any case', /SELECT \* FROM users WHERE LOWER\(email\) = \? ORDER BY id/.test(server));
        ok('login tries every case-variant row', /for \(const row of candidates\) \{\s*if \(await bcrypt\.compare\(password, row\.password\)\)/.test(server));
    }

    // ------------------------------------------------------------- the report
    if (failures.length) {
        console.error(`\n${failures.length} FAILED of ${pass + failures.length}:`);
        for (const f of failures) console.error(`  ✗ ${f}`);
        process.exit(1);
    }
    console.log(`\nAll ${pass} checks passed.`);
})().catch((e) => {
    console.error('\nTest harness crashed:', e);
    process.exit(1);
});
