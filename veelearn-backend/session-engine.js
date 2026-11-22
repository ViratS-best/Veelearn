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

/**
 * The lesson writer uses the product's model with reasoning off.
 *
 * A reasoning model's thinking is not content: the stream stayed silent for
 * about a hundred seconds and then the whole reply landed at once. Luna can be
 * told `effort: 'none'`, so the lesson is written as it streams instead of being
 * thought about first.
 */
const LESSON_MODEL = String(process.env.VEELEARN_LESSON_MODEL || '').trim() || 'openai/gpt-6-luna';
const LESSON_REASONING = /^openai\/gpt-6-luna/i.test(LESSON_MODEL) ? { effort: 'none' } : null;

/** Unit reviews must clear this share of their questions to move on. */
const REVIEW_PASS = 0.9;

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

/**
 * The hint ladder for one card: the authored hints first, then the first
 * concrete steps of the authored method. "Look again at what the question is
 * asking" is not a hint — every rung names something the learner can do next.
 * The final solution step is never added, because that is the answer.
 */
function hintLadder(raw) {
    const out = [];
    const push = (text) => {
        const line = String(text == null ? '' : text)
            .replace(/\s+/g, ' ')
            .trim();
        if (!line) return;
        if (out.some((hint) => hint.toLowerCase() === line.toLowerCase())) return;
        out.push(line);
    };
    for (const hint of parseJson(raw && raw.hints, [])) push(hint);
    const steps = parseJson(raw && raw.solution_steps, [])
        .map((step) =>
            String(step == null ? '' : step)
                .replace(/\s+/g, ' ')
                .trim()
        )
        .filter(Boolean);
    const usable = steps.slice(0, Math.max(0, steps.length - 1));
    for (const step of usable) {
        if (out.length >= 3) break;
        push(`${out.length ? 'Next step' : 'Start with this step'}: ${step}`);
    }
    return out;
}

/**
 * Some replies arrive as drafted sentences with word counts ("..." (11) = 26)
 * because the model did its arithmetic out loud. When that pattern shows up,
 * keep the finished sentences and drop the working.
 */
/**
 * A vague unit can make the model think out loud instead of teaching: "The user
 * wants me to teach…", "Let me plan the lesson". None of that belongs in front
 * of a learner, so it is removed here — line by line, keeping every real lesson
 * section instead of only the last paragraph (a lesson with worked examples has
 * many). A heading always counts as lesson text.
 */
const PLANNING_TELL =
    /(the user wants|the user is asking|the user asked|the learner wants|i need to teach|i should teach|i should interpret|given the ambiguity|the safest approach is|that actually makes sense|the most sensible interpretation|as an ai|these instructions|this prompt|the instructions say|word count|let me (?:think|plan|write|draft|work out))/i;

/**
 * A model that answers by quoting the brief back ("Structure plan: …", then the
 * template's own sentences) has not written a lesson. These lines are the brief's
 * words, never the learner's, so the whole paragraph is dropped.
 */
const BRIEF_ECHO =
    /(named in one line|two to four short paragraphs|state the example in its own sentence|slightly harder example worked the same way|the mistake learners usually make here|teach from the unit material|never use one of this unit|draw a picture with a small github-style|finish every sentence, every step|shape it exactly like this|the outline material covers|structure plan:|the final task gives)/i;

/** Lines that open with a note addressed to nobody but the model. */
const PLANNING_LEAD =
    /^(the user|the learner|i need to|i should|i'll|i will now|let me|we need to|okay,?\s+(?:so|let)|hmm\b|wait\b|given the ambiguity|the most sensible|plan:|draft:|outline of the lesson|thinking:)/i;

/** A friendly preamble a model adds before the lesson actually starts. */
const LESSON_PREAMBLE = /^(sure\b|certainly\b|of course\b|here(?:'s| is)\b|absolutely\b|great\b|okay\b|alright\b)/i;

function cleanLesson(text, opts) {
    let raw = String(text || '').trim();
    if (!raw) return '';

    // Chain-of-thought blocks a reasoning model may print into the content.
    raw = raw
        .replace(/<(?:thinking|thought|reasoning|scratchpad)>[\s\S]*?<\/(?:thinking|thought|reasoning|scratchpad)>/gi, ' ')
        .replace(/^\s*(?:thinking|planning|reasoning|analysis|scratchpad)\s*:[^\n]*(?:\n(?!\s*\n)[^\n]*)*/i, ' ')
        .trim();
    if (!raw) return '';

    const lines = raw.split(/\r?\n/);
    const kept = [];
    let dropping = false;
    for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed) {
            dropping = false;
            kept.push('');
            continue;
        }
        // A section heading is always the learner's text.
        if (/^#{1,4}\s/.test(trimmed)) {
            dropping = false;
            kept.push(trimmed);
            continue;
        }
        if (dropping) continue; // rest of the planning paragraph
        const meta =
            PLANNING_TELL.test(trimmed) ||
            BRIEF_ECHO.test(trimmed) ||
            (PLANNING_LEAD.test(trimmed) && /\b(i|me|we|the user|the learner)\b/i.test(trimmed.slice(0, 40)));
        if (meta) {
            dropping = true;
            continue;
        }
        kept.push(trimmed);
    }

    // A one-line greeting before the first heading is not part of the lesson.
    const firstHeading = kept.findIndex((l) => /^#{1,4}\s/.test(l));
    if (firstHeading > 0) {
        const before = kept.slice(0, firstHeading).filter(Boolean);
        if (before.length <= 2 && before.every((l) => LESSON_PREAMBLE.test(l) || PLANNING_TELL.test(l))) {
            kept.splice(0, firstHeading);
        }
    }

    let out = kept
        .join('\n')
        .replace(/\n{3,}/g, '\n\n')
        .trim();
    // The brief asks for the lesson to start at its first heading, so anything
    // before one is not the lesson: it is the brief quoted back, or a plan.
    const heading = out.search(/^#{2,3}\s+\S/m);
    if (heading > 0) out = out.slice(heading).trim();
    else if (heading < 0 && opts && opts.requireHeading) return '';
    return out.length >= 40 ? out : '';
}

function stripDrafting(text) {
    const raw = String(text || '');
    const quoted = raw.match(/"([^"]{8,})"\s*\(\d+\)/g) || [];
    if (quoted.length < 2) return raw;
    const kept = quoted
        .map((m) => m.replace(/"\s*\(\d+\)$/, '').replace(/^"/, '').trim())
        .filter(Boolean);
    return kept.length ? kept.join(' ') : raw;
}

function createSessionEngine({ query, qbank, log, chatStream, impact } = {}) {
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
                    f.correct_count, f.attempts, f.question_ids, f.review_pool, f.frame_md, f.unit_index, f.unit_label, f.started_at, f.completed_at,
                    s.name AS skill_name, s.code AS skill_code, s.track, s.intro_md
             FROM session_focus_items f
             JOIN skills s ON s.id = f.skill_id
             WHERE f.session_id = ?
             ORDER BY f.ord ASC`,
            [sessionId]
        );
    }

    /** A review waits until every skill in its unit is done. */
    function reviewBlocked(item, items) {
        if (!item || !Number(item.is_review)) return false;
        return items.some(
            (row) =>
                !Number(row.is_review) &&
                Number(row.unit_index || 0) === Number(item.unit_index || 0) &&
                row.status !== 'done'
        );
    }

    function currentItem(items, index) {
        const open = items.filter((i) => i.status === 'active' || i.status === 'pending');
        const active = open.find((i) => i.status === 'active');
        if (active && !reviewBlocked(active, items)) return active;
        // Walk the plan in the order the creator drew it. A ready review is only
        // current when it is the next open row, never by scanning ahead: skipping
        // to a later unit's review was why a fresh session opened at the end.
        for (const row of open) {
            if (!reviewBlocked(row, items)) return row;
        }
        // Blocked reviews only happen when their unit is already out of order; never
        // leave the learner without a card when work is still open.
        if (open.length) return open[0];
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

    /**
     * A review needs more cards than its unit's own list holds, or it asks the
     * same handful again. Top the pool up from the shared bank for the unit's
     * skills, and, when the bank has nothing new, have the model write more
     * MCQs from the same unit material. The pool is saved, so this runs once.
     */
    const toppingUp = new Map();
    async function topUpReviewPool(item, items, userId, { write = true } = {}) {
        const pool = parseJson(item.review_pool, []).map(Number).filter(Boolean);
        const need = Math.max(1, Number(item.target_dots || 18));
        if (pool.length >= need + 4) return pool;

        const key = `${item.id}|${pool.length}|${write ? 'w' : 'b'}`;
        const running = toppingUp.get(key);
        if (running) return running;

        const work = (async () => {
            const rows = items && items.length ? items : await focusItems(item.session_id);
            const skills = [
                ...new Set(
                    (rows || [])
                        .filter((row) => !Number(row.is_review) && Number(row.unit_index || 0) === Number(item.unit_index || 0))
                        .map((row) => Number(row.skill_id))
                        .filter(Boolean)
                )
            ];
            if (!skills.length) return pool;

            const marks = skills.map(() => '?').join(', ');
            try {
                const rows = await query(
                    `SELECT id FROM qbank_items
                     WHERE skill_id IN (${marks}) AND live = TRUE
                     ORDER BY tier ASC, calibration_p DESC, id ASC LIMIT 60`,
                    skills
                );
                for (const row of rows) {
                    const id = Number(row.id);
                    if (id && !pool.includes(id)) pool.push(id);
                }
            } catch (e) {
                info(`[session] review bank top-up skipped: ${e.message}`);
            }

            // Still short of a full review: the model writes fresh MCQs for the
            // same skills, so a review is not the same three cards again. This is
            // the slow half, so a caller that must answer immediately passes
            // `write: false` and lets it run while the learner reads the card.
            if (write && pool.length < need + 2) {
                try {
                    const writer = impact || require('./creator-impact')({ query, log });
                    if (writer && typeof writer.generateQuestionsForSkill === 'function') {
                        for (const skillId of skills) {
                            if (pool.length >= need + 4) break;
                            const made = await writer.generateQuestionsForSkill(skillId, {
                                count: 4,
                                avoid: pool.slice(0, 8)
                            });
                            for (const id of made || []) {
                                const n = Number(id);
                                if (n && !pool.includes(n)) pool.push(n);
                            }
                        }
                    }
                } catch (e) {
                    info(`[session] review question writing skipped: ${e.message}`);
                }
            }

            const trimmed = pool.slice(0, 60);
            try {
                await query('UPDATE session_focus_items SET review_pool = ? WHERE id = ?', [
                    JSON.stringify(trimmed),
                    item.id
                ]);
                item.review_pool = JSON.stringify(trimmed);
            } catch (e) {
                info(`[session] review pool save skipped: ${e.message}`);
            }
            return trimmed;
        })();

        toppingUp.set(key, work);
        const forget = () => setTimeout(() => toppingUp.delete(key), 5000);
        work.then(forget, forget);
        // A failed top-up must not break the review: the pool it had is still playable.
        return work.catch((e) => {
            info(`[session] review top-up failed: ${e.message}`);
            return pool;
        });
    }

    async function ensureQuestion(item, userId) {
        const ids = parseJson(item.question_ids, []).map(Number).filter(Boolean);
        if (ids.length) {
            // The list is the unit's own questions, not a record of what was asked,
            // so resuming a unit lands on a card the learner has not answered yet.
            // Returning the last entry re-asked the question they had just done.
            let asked = new Set();
            if (!Number(item.is_review)) {
                try {
                    const rows = await query(
                        'SELECT DISTINCT question_id FROM practice_attempts WHERE user_id = ? AND session_id = ?',
                        [userId, item.session_id]
                    );
                    asked = new Set(rows.map((r) => Number(r.question_id)).filter(Boolean));
                } catch (_) {
                    asked = new Set();
                }
            }
            const nextId = Number(item.is_review)
                ? ids[ids.length - 1]
                : ids.find((id) => !asked.has(Number(id))) || ids[ids.length - 1];
            const raw = await qbank.getRaw(nextId);
            if (raw) return qbank.toCard(raw);
        }
        // A review serves a card the learner has not met yet, from a pool wider
        // than the unit's own list — otherwise it is the same three questions again.
        if (Number(item.is_review)) {
            // Bank cards are one quick query; the model's fresh MCQs are written
            // while the learner reads this card, never before it appears.
            const pool = await topUpReviewPool(item, null, userId, { write: false });
            const served = ids.map(Number);
            const asked = new Set();
            try {
                const rows = await query(
                    'SELECT DISTINCT question_id FROM practice_attempts WHERE user_id = ? AND session_id = ?',
                    [userId, item.session_id]
                );
                for (const row of rows) asked.add(Number(row.question_id));
            } catch (_) {
                /* an empty set only costs freshness, never a card */
            }
            const open = (id) => !served.includes(Number(id));
            // A card the learner has not answered in this unit first; a re-ask
            // only when the widened pool is genuinely spent.
            const fresh = pool.find((id) => open(id) && !asked.has(Number(id))) || pool.find(open);
            if (fresh) {
                const raw = await qbank.getRaw(fresh);
                if (raw) {
                    const served = [...ids.map(Number), Number(fresh)];
                    await query('UPDATE session_focus_items SET question_ids = ? WHERE id = ?', [
                        JSON.stringify(served),
                        item.id
                    ]);
                    item.question_ids = JSON.stringify(served);
                    Promise.resolve(topUpReviewPool(item, null, userId)).catch(() => {});
                    return qbank.toCard(raw);
                }
            }
        }

        let picked = await qbank.pickUnserved({ skillId: item.skill_id, exclude: [] });
        if (!picked) picked = await qbank.pick({ skillId: item.skill_id, tier: 1, userId });
        if (!picked) {
            try {
                // Prefetch and the first render can race; one call per skill is enough.
                let pending = ensuring.get(Number(item.skill_id));
                if (!pending) {
                    const onDemand = impact || require('./creator-impact')({ query, log });
                    pending = onDemand.ensureQuestionsForSkill(item.skill_id).finally(() => {
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

    /** A readable summary of a bank diagram, for prompts that only read text. */
    function describeVisual(visual) {
        if (!visual || typeof visual !== 'object') return '';
        const bits = [];
        for (const key of ['alt', 'caption', 'description', 'title', 'label']) {
            if (visual[key]) bits.push(String(visual[key]));
        }
        if (!bits.length && typeof visual.svg === 'string') {
            const texts = (visual.svg.match(/<text[^>]*>([^<]{2,140})<\/text>/gi) || [])
                .slice(0, 8)
                .map((t) => t.replace(/<[^>]+>/g, '').trim())
                .filter(Boolean);
            if (texts.length) bits.push(texts.join(' / '));
        }
        if (visual.type) bits.unshift(String(visual.type));
        return bits.join(' · ').slice(0, 400);
    }

    /** The bank's diagram as something the vision model can actually look at. */
    function visualImage(visual) {
        if (!visual || typeof visual !== 'object') return null;
        const raw = visual.image || visual.image_url || visual.url || visual.src;
        if (typeof raw === 'string' && /^data:image\//.test(raw)) return raw;
        if (typeof raw === 'string' && /^https?:\/\//.test(raw)) return raw;
        if (typeof visual.svg === 'string' && /^\s*<svg/i.test(visual.svg)) {
            return 'data:image/svg+xml;base64,' + Buffer.from(visual.svg).toString('base64');
        }
        return null;
    }

    /**
     * A short lesson for the current unit, streamed token by token. The unit's own
     * text is the fallback, so even without a key the learner gets taught instead
     * of being handed another question.
     */
    async function teach(userId, sessionId, { onDelta, question } = {}) {
        const session = await sessionRow(userId, sessionId);
        if (!session) return { error: 404, message: 'Session not found' };
        const items = await focusItems(sessionId);
        const item = currentItem(items, session.item_index);
        if (!item) return { error: 409, message: 'That session has no current unit' };

        const rows = await query('SELECT name, intro_md, misconceptions FROM skills WHERE id = ? LIMIT 1', [item.skill_id]);
        // The focus item carries the unit's own words; the skill intro is the fallback.
        const unitText = String(item.frame_md || (rows[0] && rows[0].intro_md) || '')
            .replace(/\r\n/g, '\n')
            .replace(/[ \t]+/g, ' ')
            .replace(/\n{3,}/g, '\n\n')
            .trim();
        let misconceptions = [];
        try {
            const raw = rows[0] && rows[0].misconceptions;
            const parsed = typeof raw === 'string' ? JSON.parse(raw) : raw;
            misconceptions = Array.isArray(parsed) ? parsed.filter(Boolean).slice(0, 3) : [];
        } catch (_) {
            misconceptions = [];
        }
        const title = item.skill_name || (rows[0] && rows[0].name) || 'this unit';
        const frame = parseJson(session.turn_buffer, null);
        const asked = String(question || '').trim().slice(0, 400);

        // Asking needs the card in front of the learner: without it Vee answered a
        // generic question about the unit and never saw what the learner was on.
        let cardBlock = '';
        let cardImage = null;
        try {
            const qids = parseJson(item.question_ids, []);
            const onCard = qids.length ? await qbank.getRaw(qids[qids.length - 1]) : null;
            if (onCard) {
                const choices = parseJson(onCard.options, [])
                    .map((o) => `${o.k}. ${o.t}`)
                    .join('\n');
                const visual = parseJson(onCard.visual, null);
                let visualText = describeVisual(visual);
                // A diagram authored only as SVG has no alt text; hand the tutor the
                // geometry so it can still see what the learner is looking at.
                if (!visualText && visual && typeof visual.svg === 'string') {
                    visualText = ('inline svg: ' + visual.svg).replace(/\s+/g, ' ').slice(0, 600);
                }
                cardImage = visualImage(visual);
                cardBlock =
                    `The learner is looking at this question right now: ${String(onCard.stem || '').slice(0, 500)}\n` +
                    (choices ? `Choices:\n${choices.slice(0, 700)}\n` : '') +
                    (visualText ? `Its diagram shows: ${visualText}\n` : '') +
                    `This card is tier ${Number(onCard.tier) || 1} of 4.\n`;
            }
        } catch (_) {
            cardBlock = '';
        }
        const fallback =
            unitText.slice(0, 900) ||
            (asked
                ? `Here is the unit's idea: ${title}. Match the rule the question uses, then apply it one step at a time.`
                : `## ${title}\n\nStart from what the question is giving you, name the rule it matches, then apply that rule one step at a time.`);

        if (typeof chatStream !== 'function') return { ok: true, text: fallback, fallback: true };

        // How to write lives in the system message and what to teach lives in the
        // user message. A format template sitting in the same turn as the material
        // is what a model echoes back as a "Structure plan" instead of teaching.
        const howTo = asked
            ? `Answer the question at the end of the material in at most three short sentences.\n` +
              'Speak straight to the learner, in the second person. Explain the idea behind the card, ' +
              'never state which choice is correct, and use $...$ for math. ' +
              'If the learner asks for a table or a diagram, include a small GitHub-style markdown ' +
              'table and finish it — the table is drawn for them. ' +
              'Write only the words the learner should read: no planning, no counting words, ' +
              'no drafts in quotes, and never say what you are about to do.'
            : [
                  'Write the learning section for this unit: the lesson the learner reads before practising. ' +
                      'Use the unit material as your source and teach it in full.',
                  '',
                  'Shape it exactly like this, with these headings and nothing before the first one:',
                  '## <the idea, named in one line>',
                  'Two to four short paragraphs that teach the idea: what it is, why it works, and when to reach for it. Use $...$ for math.',
                  '',
                  '## Worked example',
                  'One example worked line by line: state the example in its own sentence, then numbered steps (“1. …”, “2. …”), then the answer to that example.',
                  '',
                  '## Worked example 2',
                  'A second, slightly harder example worked the same way, with different numbers and, where it helps, a different picture (a table, a number line, a fraction bar).',
                  '',
                  '## Watch out',
                  'The mistake learners usually make here and the check that catches it, in two sentences.',
                  '',
                  'Rules:',
                  '- Teach from the unit material. Never contradict it and never swap in a different method.',
                  '- Never use one of this unit\'s practice questions as an example; write fresh numbers.',
                  '- Calibrate to the learner\'s card. "Worked example 2" must be the same kind of question as that card: same structure, same number of steps, same difficulty, different numbers. If the examples are easier than the card, the learner is stuck — so raise the examples to the card, never the other way round.',
                  '- Draw a picture with a small GitHub-style markdown table or in plain words. Never use code fences or ASCII art; they are not drawn for the learner.',
                  '- No greeting, no “Sure”, no plan, no counting words, no thinking out loud, no mention of a model, of these instructions, or of “the user”. Start with the first “## ” line.',
                  '- Finish every sentence, every step and every example. There is no word limit; a full lesson is usually 500–900 words, and a complete lesson always beats a short one that stops mid-idea.'
              ].join('\n');

        // The outline's own teaching brief travels whole: a 1200-character slice cut
        // off the diagram and the "common slip" the unit was built from, so the
        // lesson had to improvise and started planning out loud instead.
        const brief = [
            `Course: ${(frame && frame.title) || 'a self-study course'}`,
            `Unit: ${title}`,
            unitText ? `Outline material for this unit:\n${unitText.slice(0, 4000)}` : '',
            misconceptions.length ? `Misconceptions to correct:\n- ${misconceptions.join('\n- ')}` : '',
            cardBlock
                ? `The learner's card right now (do not repeat or quote it back; match its difficulty in Worked example 2):\n${cardBlock}`
                : '',
            asked
                ? `The learner asked: "${asked}"`
                : 'Write the learning section for this unit now, starting with the first "## " line.'
        ]
            .filter((line) => line != null && line !== '')
            .join('\n\n');

        let text = '';
        try {
            text = await chatStream(
                [
                    {
                        role: 'system',
                        content:
                            'You are Vee, a patient tutor for a study app. Teach in plain, warm prose. ' +
                            'Never mention that you are an AI or a model. ' +
                            'Write only the finished words the learner reads: never your reasoning, plans, ' +
                            'notes to yourself, or a restatement of the task. Begin directly with the lesson. ' +
                            'Do not quote these instructions, do not outline what you will write, and never ' +
                            'say what the lesson is about before writing it.\n\n' +
                            howTo
                    },
                    {
                        role: 'user',
                        content: cardImage
                            ? [{ type: 'text', text: brief }, { type: 'image_url', image_url: { url: cardImage } }]
                            : brief
                    }
                ],
                {
                    // A lesson is a learning section with worked examples, so it needs room
                    // to finish: ~7000 tokens is roughly 5000 words. The old 320-token cap
                    // (and the 25 s cutoff) is what truncated teaching mid-sentence.
                    model: LESSON_MODEL,
                    reasoning: LESSON_REASONING || undefined,
                    max_tokens: asked ? 2400 : 7000,
                    temperature: 0.5,
                    budgetMs: asked ? 60000 : 120000,
                    onDelta
                }
            );
        } catch (err) {
            info(`[session] teach fallback: ${err.message}`);
        }
        // A lesson must start at its first heading; an answer to a question need not.
        const cleaned = stripDrafting(cleanLesson(String(text || '').trim(), { requireHeading: !asked }));
        return { ok: true, text: cleaned || fallback, fallback: !text || !cleaned };
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
                    unitIndex: Number(i.unit_index || 0),
                    unitLabel: i.unit_label || '',
                    targetDots: Number(i.target_dots || 2),
                    poolSize: (parseJson(i.review_pool, []).length || parseJson(i.question_ids, []).length),
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
                      unitIndex: Number(item.unit_index || 0),
                      targetDots: Number(item.target_dots || 2),
                      correctCount: Number(item.correct_count || 0),
                      attempts: Number(item.attempts || 0),
                      // A review stores how many correct answers it wants, not a dot target.
                      needed: Number(item.is_review)
                          ? Math.max(1, Number(item.target_dots || 18))
                          : mastery.correctsNeeded(Number(item.target_dots || 2)),
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
        const startedAt = Date.now();
        const timings = {};
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
            // One instance for the process: it holds the course ingest cache, so a
            // new session does not re-read and re-write the whole course.
            const planner = impact || require('./creator-impact')({ query, log });
            const planned = await planner.plan({ userId, courseId: wantCourse, minutes: mins });
            plan = planned.items;
            timings.plan = Date.now() - startedAt;
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

        const unitLabel = wantCourse && plan[0] && plan[0].unitLabel ? String(plan[0].unitLabel).slice(0, 150) : null;
        const goalText = wantCourse
            ? unitLabel || `Close ${plan.length} topic${plan.length === 1 ? '' : 's'} in this course`
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
        timings.sessionRow = Date.now() - startedAt;
        const sessionId = inserted.insertId || (await latestSessionId(userId));
        if (!sessionId) throw new Error('Could not create session');

        for (let i = 0; i < plan.length; i += 1) {
            const p = plan[i];
            // A course unit can arrive with its creator's questions already chosen.
            const seeded = Array.isArray(p.questionIds) ? p.questionIds.filter(Boolean) : [];
            const q = seeded.length ? null : await qbank.pick({ skillId: p.skillId, tier: p.startTier || 1, userId });
            const frameDigest = p.frame && p.frame.digest ? String(p.frame.digest) : null;
            await query(
                `INSERT INTO session_focus_items
                    (session_id, skill_id, ord, is_review, target_dots, status, correct_count, attempts, question_ids, review_pool, frame_md, unit_index, unit_label)
                 VALUES (?, ?, ?, ?, ?, 'pending', 0, 0, ?, ?, ?, ?, ?)`,
                [
                    sessionId,
                    p.skillId,
                    i,
                    p.isReview ? 1 : 0,
                    p.targetDots,
                    JSON.stringify(p.isReview ? [] : seeded.length ? seeded.map(Number) : q ? [Number(q.id)] : []),
                    p.isReview && seeded.length ? JSON.stringify(seeded.map(Number)) : null,
                    frameDigest,
                    Number(p.unitIndex || 0),
                    p.unitLabel ? String(p.unitLabel).slice(0, 150) : null
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
        timings.state = Date.now() - startedAt;
        return { ...fresh, resumed: false, timings };
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
        // A review item deliberately mixes the unit's skills, so its questions do not
        // have to belong to the review's own synthetic skill.
        if (!raw || (!Number(item.is_review) && Number(raw.skill_id) !== Number(item.skill_id))) {
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
        // A review item stores the number of correct answers it wants (about 90% of
        // its pool) rather than a dot target, so it can ask for ~18 of 20.
        const need = Number(item.is_review)
            ? Math.max(1, Number(item.target_dots || 18))
            : mastery.correctsNeeded(Number(item.target_dots || 2));
        const correctCount = Number(item.correct_count || 0) + (correct ? 1 : 0);
        const attempts = Number(item.attempts || 0) + 1;
        let itemDone = correct && correctCount >= need;

        let next = 'retry';
        let nextQuestion = null;

        // Cards the learner has actually answered in this session. `question_ids`
        // is the unit's own question list (an outline unit seeds three of them), so
        // it cannot be used to decide what was already served.
        let asked = null;
        const answeredCards = async () => {
            if (asked) return asked;
            const rows = await query(
                'SELECT DISTINCT question_id FROM practice_attempts WHERE user_id = ? AND session_id = ?',
                [userId, sessionId]
            );
            asked = new Set(rows.map((r) => Number(r.question_id)).filter(Boolean));
            asked.add(Number(raw.id));
            return asked;
        };

        if (correct) {
            if (itemDone) {
                next = 'advance';
            } else if (Number(item.is_review)) {
                // A review walks its own pool, so twenty correct answers mean twenty
                // different questions instead of one skill on repeat.
                const storedPool = parseJson(item.review_pool, []).map(Number);
                const pool = storedPool.length ? storedPool : parseJson(item.question_ids, []).map(Number);
                const answered = await answeredCards();
                const isOpen = (id) => !servedIds.includes(Number(id));
                let unserved = pool.filter((id) => isOpen(id) && !answered.has(Number(id)));
                if (!unserved.length) {
                    // Every card in the pool has been served: widen it from the bank
                    // now, and ask the model for more while the learner works, so
                    // the next card is fresh without this answer waiting on a model.
                    const grown = await topUpReviewPool(item, items, userId, { write: false });
                    unserved = grown.filter((id) => isOpen(id) && !answered.has(Number(id)));
                    Promise.resolve(topUpReviewPool(item, items, userId)).catch(() => {});
                }
                if (!unserved.length) unserved = pool.filter(isOpen);
                if (unserved.length) {
                    const rawNext = await qbank.getRaw(unserved[0]);
                    nextQuestion = rawNext ? qbank.toCard(rawNext) : null;
                }
                if (nextQuestion) {
                    next = 'more';
                } else if (correctCount < need) {
                    // Every pool card has been seen but the bar is not met yet, so
                    // re-ask one rather than ending the review early or deadlocking.
                    const again = pool.find((id) => Number(id) !== Number(raw.id));
                    const rawAgain = again ? await qbank.getRaw(again) : null;
                    nextQuestion = rawAgain ? qbank.toCard(rawAgain) : null;
                    next = nextQuestion ? 'more' : 'retry';
                } else {
                    // The pool is spent and the bar is met: score it against 90%.
                    itemDone = true;
                    next = 'advance';
                }
            } else {
                next = 'more';
                // Only the cards the learner actually answered are off the table, so
                // the unit keeps going for the three corrects it asks for instead of
                // closing as soon as its seeded list runs out.
                const seen = await answeredCards();
                const pending = parseJson(item.question_ids, [])
                    .map(Number)
                    .filter((id) => id && !seen.has(id));
                let nextRaw = pending.length ? await qbank.getRaw(pending[0]) : null;
                if (!nextRaw) {
                    const tier = Math.min(4, Number(raw.tier) + 1);
                    nextRaw = await qbank.pick({ skillId: raw.skill_id, tier, userId });
                    if (nextRaw && seen.has(Number(nextRaw.id))) nextRaw = null;
                }
                if (!nextRaw) {
                    nextRaw = await qbank.pickUnserved({ skillId: raw.skill_id, exclude: [...seen] });
                }
                // Only an empty skill ends the unit: never loop the same card at the
                // learner just because the plan's list was mistaken for served cards.
                if (nextRaw) nextQuestion = nextRaw;
                else {
                    itemDone = true;
                    next = 'advance';
                }
            }
        } else if (attempts >= 2) {
            // Taught once already — hand back a variant one tier easier.
            next = 'variant';
            nextQuestion = await qbank.pick({ skillId: raw.skill_id, tier: Math.max(1, Number(raw.tier) - 1), userId });
        }

        // The 90% gate. Passing closes any review left over from an earlier failure;
        // failing puts the unit's skills back and re-queues exactly one review,
        // reusing a pending one instead of stacking a fresh card each time.
        let reviewRetry = false;
        if (correct && itemDone && Number(item.is_review)) {
            const accuracy = attempts ? correctCount / attempts : 1;
            const unitIndex = Number(item.unit_index || 0);
            if (accuracy < REVIEW_PASS) {
                reviewRetry = true;
                next = 'review';
                try {
                    await query(
                        `UPDATE session_focus_items
                         SET status = 'pending', correct_count = 0, attempts = 0, completed_at = NULL
                         WHERE session_id = ? AND unit_index = ? AND is_review = 0`,
                        [sessionId, unitIndex]
                    );
                    const pending = await query(
                        `SELECT id FROM session_focus_items
                         WHERE session_id = ? AND unit_index = ? AND is_review = 1 AND id <> ?
                           AND status IN ('pending', 'active')
                         ORDER BY ord ASC LIMIT 1`,
                        [sessionId, unitIndex, item.id]
                    );
                    if (pending.length) {
                        await query(
                            `UPDATE session_focus_items
                             SET status = 'pending', correct_count = 0, attempts = 0, completed_at = NULL
                             WHERE id = ?`,
                            [pending[0].id]
                        );
                    } else {
                        const maxRows = await query(
                            'SELECT COALESCE(MAX(ord), 0) AS m FROM session_focus_items WHERE session_id = ?',
                            [sessionId]
                        );
                        const nextOrd = Number(maxRows[0] && maxRows[0].m ? maxRows[0].m : 0) + 1;
                        // A retake draws from the whole unit again, not only the cards the
                        // failed attempt happened to serve, and asks for 90% of that pool.
                        const unitRows = await query(
                            `SELECT question_ids FROM session_focus_items
                             WHERE session_id = ? AND unit_index = ? AND is_review = 0
                             ORDER BY ord ASC`,
                            [sessionId, unitIndex]
                        );
                        let retakePool = [];
                        for (const row of unitRows) {
                            for (const qid of parseJson(row.question_ids, [])) {
                                if (!retakePool.includes(Number(qid))) retakePool.push(Number(qid));
                            }
                        }
                        retakePool = retakePool.slice(0, 20);
                        if (!retakePool.length) retakePool = parseJson(item.question_ids, []).map(Number);
                        const retakeTarget = Math.max(
                            1,
                            Math.min(retakePool.length, Math.ceil(retakePool.length * REVIEW_PASS))
                        );
                        await query(
                            `INSERT INTO session_focus_items
                                (session_id, skill_id, ord, is_review, target_dots, status, correct_count, attempts, question_ids, review_pool, frame_md, unit_index, unit_label)
                             VALUES (?, ?, ?, 1, ?, 'pending', 0, 0, ?, ?, ?, ?, ?)`,
                            [
                                sessionId,
                                item.skill_id,
                                nextOrd,
                                retakeTarget,
                                JSON.stringify([]),
                                JSON.stringify(retakePool),
                                item.frame_md,
                                unitIndex,
                                item.unit_label || null
                            ]
                        );
                    }
                    info(`[session] unit ${unitIndex} review failed at ${Math.round(accuracy * 100)}% — skills reset`);
                } catch (err) {
                    info(`[session] review reset skipped: ${err.message}`);
                }
            } else {
                // A passed unit must not leave a duplicate review card behind.
                try {
                    await query(
                        `UPDATE session_focus_items
                         SET status = 'done', completed_at = COALESCE(completed_at, NOW())
                         WHERE session_id = ? AND unit_index = ? AND is_review = 1 AND id <> ?
                           AND status IN ('pending', 'active')`,
                        [sessionId, unitIndex, item.id]
                    );
                } catch (err) {
                    info(`[session] stale review cleanup skipped: ${err.message}`);
                }
            }
        }

        if (nextQuestion && !Number(item.is_review) && (await answeredCards()).has(Number(nextQuestion.id))) {
            // Never hand back a card this learner already answered; a review's own
            // re-ask is deliberate and stays as it is.
            nextQuestion = await qbank.pickUnserved({ skillId: raw.skill_id, exclude: [...(await answeredCards())] });
        }
        const questionIds = nextQuestion
            ? [...new Set([...servedIds, Number(nextQuestion.id)])]
            : servedIds;

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
        const hintsForCard = hintLadder(raw);

        return {
            ok: true,
            verdict: correct ? 'correct' : 'incorrect',
            correct,
            // Released only now, never before grading:
            why: correct ? '' : qbank.whyFor(raw, given),
            selected: selectedOption ? selectedOption.t : '',
            hint: correct
                ? ''
                : String(hintsForCard[Math.min(hintsUsed, Math.max(0, hintsForCard.length - 1))] || ''),
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
            trace: {
                need,
                correctCount,
                attempts,
                served: servedIds.length,
                reviewPool: parseJson(item.review_pool, []).length,
                itemDone
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
        const hints = hintLadder(raw);
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
module.exports.cleanLesson = cleanLesson;
module.exports.parseJson = parseJson;
module.exports.hintLadder = hintLadder;
