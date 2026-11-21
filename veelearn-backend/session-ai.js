'use strict';

/**
 * The AI loop for learning sessions (design §9).
 *
 * Division of labour, enforced here rather than promised in a prompt:
 *   server — grades, counts the ladder, decides mode/next, validates the reply,
 *            caps spend, caches, and falls back to a deterministic script
 *   model  — proposes one line of prose and a whitelisted annotation script
 *
 * A model reply can therefore be wrong, slow, malformed or leaking and the
 * session still behaves: `turn()` always resolves with something playable.
 */

const crypto = require('crypto');
const prompts = require('./pedagogy-prompts');

const CAPS = {
    /** Design budget for a clean 20-minute session. */
    cleanSession: 9,
    /** Hard per-session ceiling, whatever the learner does. */
    perSession: 15,
    /** Free-form questions per session. */
    askPerSession: 6,
    /** LRU entries kept in memory (~1.3 KB each → well under the 12 MB budget). */
    cacheEntries: 500,
    /**
     * A slow answer inside a session is worse than a template one — but the page
     * plays the template immediately, so a late model reply is an upgrade, not a
     * wait. OpenRouter's free router measured 5 / 25 / 13 s on the live deploy,
     * so the budget is generous and overridable.
     */
    budgetMs: Number(process.env.SESSION_AI_BUDGET_MS) || 18000,
    summaryBudgetMs: Number(process.env.SESSION_SUMMARY_BUDGET_MS) || 9000,
    /** A scene is drawn once per question and cached, so it can afford a moment. */
    boardBudgetMs: Number(process.env.SESSION_BOARD_BUDGET_MS) || 24000,
    /** A fallback is deterministic; remember it briefly instead of stalling again. */
    fallbackTtlMs: 5 * 60 * 1000,
    maxTokens: 700
};

const AI_KINDS = ['teach', 'reteach', 'explain_again', 'ask', 'summary'];

function parseJsonLoose(text) {
    if (!text || typeof text !== 'string') return null;
    const s = text.replace(/```(?:json)?/gi, '').trim();
    const wanted = ['say', 'script', 'mood', 'ask', 'next', 'questions'];

    // Walk every balanced object/array in the reply, ignoring braces inside
    // strings. A chatty model often says a sentence first, or emits two objects;
    // taking the outermost first slice missed the real one.
    const candidates = [];
    const stack = [];
    let inString = false;
    let escaped = false;
    for (let i = 0; i < s.length; i += 1) {
        const ch = s[i];
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
        if (ch === '{' || ch === '[') {
            stack.push({ ch, at: i });
            continue;
        }
        if ((ch === '}' || ch === ']') && stack.length) {
            const open = stack.pop();
            if ((open.ch === '{' && ch === '}') || (open.ch === '[' && ch === ']')) {
                if (!stack.length) candidates.push(s.slice(open.at, i + 1));
            }
        }
    }

    const parsed = [];
    for (const c of candidates) {
        try {
            parsed.push(JSON.parse(c));
        } catch (_) {
            /* not JSON, keep looking */
        }
    }
    if (!parsed.length) {
        try {
            parsed.push(JSON.parse(s.slice(s.search(/[[{]/))));
        } catch (_) {
            return null;
        }
    }

    const flat = parsed.flatMap((p) => (Array.isArray(p) ? p : [p]));
    const best = flat.find((p) => p && typeof p === 'object' && wanted.some((k) => k in p));
    return best || flat.find((p) => p && typeof p === 'object') || null;
}

/** Numbers in a string, ignoring option letters and footnote-ish noise. */
function numbersIn(text) {
    const out = [];
    const re = /-?\d+(?:\.\d+)?/g;
    let m;
    while ((m = re.exec(String(text || ''))) !== null) out.push(Number(m[0]));
    return out;
}

/**
 * Answer-leak guard (design §9.6). Rejects a line that states the key, names
 * the correct option as correct, echoes the correct option's text, or contains
 * a number within 0.5% of a numeric answer.
 */
function leaksAnswer(say, raw) {
    const text = String(say || '');
    if (!text.trim() || !raw) return false;

    const key = raw.answer != null ? String(raw.answer).trim() : '';
    if (!key) return false;

    // "the answer is C" / "option C is correct" / "C is right"
    if (/^[A-Da-d]$/.test(key) && new RegExp(`\\b(?:answer|correct|right|option)\\b[^.]{0,24}\\b${key}\\b`, 'i').test(text)) {
        return true;
    }

    // Numeric answer within 0.5%
    const wanted = Number(key);
    if (Number.isFinite(wanted)) {
        const tolerance = Math.max(Math.abs(wanted) * 0.005, 1e-9);
        if (numbersIn(text).some((n) => Math.abs(n - wanted) <= tolerance)) return true;
    }

    // Echoing the correct option's wording
    let options = [];
    try {
        options = typeof raw.options === 'string' ? JSON.parse(raw.options) : raw.options || [];
    } catch (_) {
        options = [];
    }
    const correct = (Array.isArray(options) ? options : []).find(
        (o) => String(o.k || '').toUpperCase() === key.toUpperCase()
    );
    const correctText = correct && correct.t ? String(correct.t).trim() : '';
    if (correctText.length >= 12 && text.toLowerCase().includes(correctText.toLowerCase())) return true;

    return false;
}

/**
 * Validate one model reply into a script the player can execute.
 * Everything unknown is dropped, not repaired: a script that points at a
 * selector which is not on the page is worse than no annotation at all.
 */
function validateAction(action, { mode, hasSolution } = {}) {
    const dropped = [];
    if (!action || typeof action !== 'object') return { action: null, dropped: ['no object'] };

    const say = prompts.clampText(action.say, prompts.LIMITS.say);
    const mood = prompts.MOODS.includes(String(action.mood || '').trim()) ? String(action.mood).trim() : 'thinking';
    const proposedMode = String(action.mode || '').trim().toLowerCase();
    const resolvedMode = prompts.MODES.includes(proposedMode) ? proposedMode : mode || 'funnel';

    const rawScript = Array.isArray(action.script) ? action.script : [];
    const script = [];
    let lastAt = -1;

    for (const step of rawScript) {
        if (!step || typeof step !== 'object') {
            dropped.push('step is not an object');
            continue;
        }
        const rawDo = String(step.do || step.action || '').trim();
        const doName = prompts.normalizePrimitive(rawDo) || (prompts.CONTROL_STEPS.includes(rawDo) ? rawDo : '');
        if (!doName) {
            dropped.push(`unknown primitive: ${rawDo || '(empty)'}`);
            continue;
        }

        if (doName === 'board') {
            const preset = String(step.preset || '').trim();
            if (!prompts.PRESETS.includes(preset)) {
                dropped.push(`unknown preset: ${preset || '(empty)'}`);
                continue;
            }
            const at = Math.max(lastAt + 1, Math.min(prompts.LIMITS.maxAt, Math.max(0, Number(step.at) || 0)));
            lastAt = at;
            const params = step.params && typeof step.params === 'object' ? step.params : {};
            script.push({ at, do: 'board', preset, params });
        } else if (doName === 'say') {
            const text = prompts.clampText(step.text, 140);
            if (!text) {
                dropped.push('empty say step');
                continue;
            }
            const at = Math.max(lastAt + 1, Math.min(prompts.LIMITS.maxAt, Math.max(0, Number(step.at) || 0)));
            lastAt = at;
            script.push({ at, do: 'say', text });
        } else if (doName === 'move') {
            const anchor = String(step.anchor || step.to || '').trim();
            if (!prompts.ANCHORS.includes(anchor)) {
                dropped.push(`unknown anchor: ${anchor || '(empty)'}`);
                continue;
            }
            const at = Math.max(lastAt + 1, Math.min(prompts.LIMITS.maxAt, Math.max(0, Number(step.at) || 0)));
            lastAt = at;
            script.push({ at, do: 'move', to: anchor });
        } else if (doName === 'mood') {
            const nextMood = String(step.mood || '').trim();
            if (!prompts.MOODS.includes(nextMood)) {
                dropped.push(`unknown mood: ${nextMood || '(empty)'}`);
                continue;
            }
            const at = Math.max(lastAt + 1, Math.min(prompts.LIMITS.maxAt, Math.max(0, Number(step.at) || 0)));
            lastAt = at;
            script.push({ at, do: 'mood', mood: nextMood });
        } else {
            const anchor = String(step.anchor || '').trim();
            if (!prompts.ANCHORS.includes(anchor)) {
                dropped.push(`unknown anchor: ${anchor || '(empty)'}`);
                continue;
            }
            if (/solution/.test(anchor) && !hasSolution) {
                dropped.push(`anchor not on the page yet: ${anchor}`);
                continue;
            }
            const at = Math.max(lastAt + 1, Math.min(prompts.LIMITS.maxAt, Math.max(0, Number(step.at) || 0)));
            lastAt = at;
            const entry = { at, do: doName, anchor };
            const text = prompts.clampText(step.text, prompts.LIMITS.text);
            if (text) entry.text = text;
            if (doName === 'ellipseLabel') {
                const label = prompts.clampText(step.label, 24);
                if (label) entry.label = label;
            }
            if (doName === 'stamp') entry.mark = step.mark === 'x' || step.mark === '✗' ? 'x' : 'v';
            const ms = Number(step.ms);
            if (Number.isFinite(ms) && ms > 0) entry.ms = Math.min(2000, ms);
            script.push(entry);
        }
    }

    // The player caps live strokes at 12 anyway; do it here so the budget holds.
    const drawing = script.filter((s) => !prompts.CONTROL_STEPS.includes(s.do));
    if (drawing.length > prompts.LIMITS.scriptHard) {
        dropped.push('script too long');
    }

    const askText = action.ask && typeof action.ask === 'object' ? prompts.clampText(action.ask.text, prompts.LIMITS.ask) : '';
    const nextAction = action.next && typeof action.next === 'object' ? String(action.next.action || '').trim().toLowerCase() : '';

    const trimmed = script.slice(0, prompts.LIMITS.scriptHard);
    if (!say && !trimmed.length) return { action: null, dropped };

    return {
        action: {
            say,
            mood,
            mode: resolvedMode,
            script: trimmed,
            ask: askText ? { text: askText } : null,
            next: prompts.NEXT_ACTIONS.includes(nextAction) ? { action: nextAction } : null
        },
        dropped
    };
}

/**
 * The server's ladder. The model reports; this function decides.
 * wrong #1 → funnel · wrong #2 → teach · correct → celebrate.
 */
function decideMode({ attempts = 0, correct = false, requested } = {}) {
    if (correct) return { mode: 'celebrate', overridden: requested ? requested !== 'celebrate' : false };
    const n = Number(attempts) || 0;
    const mode = n >= 2 ? 'teach' : n === 1 ? 'funnel' : 'focus';
    return { mode, overridden: !!requested && requested !== mode };
}

/** `next` is a request the server may refuse. */
function decideNext({ requested, correct, attempts = 0, itemsDone = false } = {}) {
    const n = Number(attempts) || 0;
    const want = String(requested || '').toLowerCase();
    if (!correct) {
        if (n >= 2) return { action: 'teach', overridden: want !== 'teach' };
        return { action: 'reask', overridden: want !== 'reask' };
    }
    if (itemsDone) return { action: 'advance', overridden: want !== 'advance' };
    if (want === 'more' || want === 'advance' || want === 'wrap') return { action: want, overridden: false };
    return { action: 'more', overridden: want !== 'more' };
}

// Board scenes want a coder, not a talker, and a reasoning model spends the
// answer's budget thinking. The board pins Luna (the standard id, not the
// expensive `:nitro` route) with reasoning off.
const BOARD_MODEL = String(process.env.VEELEARN_BOARD_MODEL || '').trim() || 'openai/gpt-6-luna';
const BOARD_REASONING = /^openai\/gpt-6-luna/i.test(BOARD_MODEL) ? { effort: 'none' } : null;

function createSessionAI({ query, qbank, chat, log } = {}) {
    const info = (log && log.info) || (() => {});
    const cache = new Map();
    const local = { calls: new Map(), events: [] };

    if (typeof chat !== 'function') {
        // Lazily resolve the shared multi-key client so tests never need one.
        const client = require('./ai-chat');
        chat = (messages, opts) => client.aiChatCompletion(messages, opts);
    }
    if (typeof qbank !== 'function' && (!qbank || !qbank.getRaw)) {
        qbank = require('./qbank')({ query });
    }

    function cacheKey({ skillId, questionId, distractor, mode, kind, courseId }) {
        return crypto
            .createHash('sha256')
            .update(`${skillId}|${questionId}|${distractor || ''}|${mode || ''}|${kind || ''}|${courseId || ''}`)
            .digest('hex');
    }

    function cacheGet(key) {
        const hit = cache.get(key);
        if (!hit) return null;
        if (hit.expiresAt && hit.expiresAt < Date.now()) {
            cache.delete(key);
            return null;
        }
        // Refresh recency for the LRU trim.
        cache.delete(key);
        cache.set(key, hit);
        return hit;
    }

    function cacheSet(key, value, ttlMs) {
        const entry = ttlMs ? Object.assign({}, value, { expiresAt: Date.now() + ttlMs }) : value;
        cache.set(key, entry);
        while (cache.size > CAPS.cacheEntries) {
            const oldest = cache.keys().next().value;
            cache.delete(oldest);
        }
    }

    async function countCalls(sessionId) {
        if (typeof query === 'function') {
            try {
                const rows = await query(
                    `SELECT COUNT(*) AS c FROM session_events WHERE session_id = ? AND kind = 'ai'`,
                    [sessionId]
                );
                return Number(rows[0]?.c || 0);
            } catch (e) {
                info(`[session.ai] count skipped: ${e.message}`);
            }
        }
        return local.calls.get(Number(sessionId)) || 0;
    }

    async function recordTurn(sessionId, { kind, skillId, questionId, payload }) {
        local.calls.set(Number(sessionId), (local.calls.get(Number(sessionId)) || 0) + 1);
        local.events.push({ sessionId, kind, questionId, payload });
        if (typeof query !== 'function') return;
        try {
            const seqRows = await query(
                'SELECT COALESCE(MAX(seq), 0) + 1 AS s FROM session_events WHERE session_id = ?',
                [sessionId]
            );
            const seq = Number(seqRows[0]?.s || 1);
            await query(
                'INSERT INTO session_events (session_id, seq, kind, skill_id, question_id, payload) VALUES (?, ?, ?, ?, ?, ?)',
                [sessionId, seq, 'ai', skillId || null, questionId || null, JSON.stringify(payload).slice(0, 2000)]
            );
        } catch (e) {
            info(`[session.ai] event skipped: ${e.message}`);
        }
    }

    function skillContext(skill, masteryRow) {
        if (!skill) return null;
        let miscon = [];
        try {
            miscon = typeof skill.misconceptions === 'string' ? JSON.parse(skill.misconceptions) : skill.misconceptions || [];
        } catch (_) {
            miscon = [];
        }
        return {
            name: skill.name,
            code: skill.code,
            grade_band: skill.grade_band,
            level: masteryRow && masteryRow.level != null ? Number(masteryRow.level) : 0,
            misconceptions: Array.isArray(miscon) ? miscon : []
        };
    }

    /**
     * One AI turn. Always resolves: on any failure it returns a deterministic
     * script flagged `fallback: true`, and `bankMode: true` when the cause was
     * rate limiting or a missing key (the session keeps working either way).
     */
    async function turn({ userId, sessionId, kind = 'reteach', questionId, distractor, attempts = 0, correct = false, itemsDone = false, turns, summary, learnerPrefs, course = null } = {}) {
        const safeKind = AI_KINDS.includes(kind) && kind !== 'summary' ? kind : 'reteach';
        if (!questionId) {
            return { ok: false, error: 400, message: 'questionId is required' };
        }

        const raw = await qbank.getRaw(questionId);
        if (!raw) return { ok: false, error: 404, message: 'Question not found' };

        // Scope: this endpoint can only decorate a question that is part of the
        // caller's own session. Otherwise it would be a way to probe any item.
        if (typeof query === 'function' && userId && sessionId) {
            // Matching only `f.skill_id` rejected every review card: its question
            // belongs to one of the unit's skills, not to the review item itself.
            const owned = await query(
                `SELECT f.skill_id, f.question_ids, f.review_pool
                   FROM session_focus_items f
                   JOIN sessions s ON s.id = f.session_id
                  WHERE f.session_id = ? AND s.user_id = ?`,
                [sessionId, userId]
            );
            const list = (value) => {
                try {
                    const parsed = typeof value === 'string' ? JSON.parse(value) : value;
                    return Array.isArray(parsed) ? parsed.map(Number) : [];
                } catch (_) {
                    return [];
                }
            };
            const qid = Number(raw.id);
            const member = owned.some(
                (row) =>
                    Number(row.skill_id) === Number(raw.skill_id) ||
                    list(row.question_ids).includes(qid) ||
                    list(row.review_pool).includes(qid)
            );
            if (!member) return { ok: false, error: 404, message: 'That question is not part of this session' };
        }

        const skill = await qbank.getSkill(raw.skill_id);

        let masteryRow = null;
        if (typeof query === 'function' && userId) {
            try {
                const rows = await query('SELECT level FROM skill_mastery WHERE user_id = ? AND skill_id = ? LIMIT 1', [
                    userId,
                    raw.skill_id
                ]);
                masteryRow = rows[0] || null;
            } catch (_) {
                masteryRow = null;
            }
        }

        const ladder = decideMode({ attempts, correct, requested: safeKind === 'reteach' && attempts >= 2 ? 'teach' : undefined });
        const mode = ladder.mode;
        const card = qbank.toCard(raw);
        const why = qbank.whyFor(raw, distractor);
        const solution = raw.solution_steps ? qbank.solutionFor(raw) : null;
        const callCount = await countCalls(sessionId);

        const fallbackFor = (reason, extra) => {
            const generated = Object.assign(
                prompts.templateFallback({ mode, question: card, why, solution, distractor }),
                {
                    ok: true,
                    cached: false,
                    bankMode: reason === 'rate' || reason === 'unconfigured' || reason === 'timeout',
                    reason,
                    aiCalls: callCount
                },
                extra || {}
            );
            return generated;
        };

        // 1. Spend guard: over the ceiling, never call the model again.
        if (callCount >= CAPS.perSession) {
            await recordTurn(sessionId, { kind: safeKind, skillId: raw.skill_id, questionId: raw.id, payload: { kind: safeKind, capped: true, mode } });
            return fallbackFor('capped');
        }
        if (safeKind === 'ask') {
            const asks = local.events.filter((e) => e.sessionId === Number(sessionId) && e.kind === 'ask').length;
            if (asks >= CAPS.askPerSession) return fallbackFor('ask_capped');
        }

        // 2. Cache: the second learner of a question costs nothing.
        const key = cacheKey({ skillId: raw.skill_id, questionId: raw.id, distractor, mode, kind: safeKind });
        const hit = cacheGet(key);
        if (hit) {
            // A cache hit costs nothing, so it must not consume the call budget.
            local.events.push({ sessionId: Number(sessionId), kind: safeKind, cached: true });
            return Object.assign({}, hit, { ok: true, cached: true, aiCalls: callCount });
        }

        const messages = prompts.buildMessages({
            kind: safeKind,
            question: card,
            skill: skillContext(skill, masteryRow),
            brief: learnerPrefs ? `Learner preferences: ${String(learnerPrefs).slice(0, 180)}` : '',
            turns,
            summary,
            distractor,
            why,
            mode,
            course
        });

        const started = Date.now();
        let reply = null;
        let usedModel = null;
        let failure = null;

        // 3. Two parse attempts, then the template. A 12 s budget, not 35 s.
        for (let attempt = 0; attempt < 2 && !reply; attempt++) {
            try {
                const nudge =
                    attempt === 0
                        ? messages
                        : messages.concat([
                              {
                                  role: 'user',
                                  content: 'Your previous reply was not valid JSON. Reply with ONE JSON object only, no prose, no code fence.'
                              }
                          ]);
                const text = await chat(nudge, {
                    max_tokens: CAPS.maxTokens,
                    temperature: 0.4,
                    budgetMs: CAPS.budgetMs,
                    jsonMust: true,
                    onModel: (m) => {
                        usedModel = m;
                    }
                });
                if (!usedModel) usedModel = 'hackclub';
                const parsed = parseJsonLoose(text);
                if (!parsed) {
                    failure = 'parse';
                    continue;
                }
                const validated = validateAction(parsed, { mode, hasSolution: !!(solution && solution.steps && solution.steps.length) });
                if (!validated.action) {
                    failure = 'invalid';
                    continue;
                }
                reply = validated.action;
                if (validated.dropped.length) info(`[session.ai] dropped ${validated.dropped.length} script step(s): ${validated.dropped.slice(0, 3).join('; ')}`);
            } catch (e) {
                const code = e && e.code;
                const text = String((e && e.message) || '');
                failure =
                    code === 'AI_RATE_LIMITED' || e.status === 429
                        ? 'rate'
                        : code === 'AI_NOT_CONFIGURED'
                          ? 'unconfigured'
                          : code === 'AI_TIMEOUT' || /budget|timeout|ECONNABORTED|ETIMEDOUT/i.test(text)
                            ? 'timeout'
                            : 'error';
                info(`[session.ai] ${failure}: ${e && e.message}`);
                break; // no second parse attempt for transport failures
            }
        }

        if (!reply) {
            await recordTurn(sessionId, {
                kind: safeKind,
                skillId: raw.skill_id,
                questionId: raw.id,
                payload: { kind: safeKind, mode, fallback: true, reason: failure || 'unknown', ms: Date.now() - started }
            });
            const fallback = fallbackFor(failure || 'unknown');
            fallback.aiCalls = callCount + 1;
            // Cache it: asking the same question again should not stall again.
            cacheSet(key, fallback, CAPS.fallbackTtlMs);
            return fallback;
        }

        // 4. Guardrails: the reply may not leak the key, whatever the prompt said.
        let sanitized = false;
        if (leaksAnswer(reply.say, raw)) {
            sanitized = true;
            reply.say = prompts.safeSay(why, 'Look at what the question is asking, then at the step where your method stopped matching it.');
            info('[session.ai] reply sanitised: it stated the answer');
        }
        if (why && reply.say && reply.say.toLowerCase().includes(String(raw.answer || '').toLowerCase()) && String(raw.answer || '').length >= 2) {
            sanitized = true;
            reply.say = prompts.safeSay(why, reply.say);
        }

        // 5. The server owns the ladder and the next step.
        const next = decideNext({ requested: reply.next ? reply.next.action : '', correct, attempts, itemsDone });
        const result = {
            ok: true,
            say: reply.say,
            mood: reply.mood,
            mode: ladder.mode,
            script: reply.script,
            ask: reply.ask,
            next,
            cached: false,
            fallback: false,
            bankMode: false,
            sanitized,
            modeOverridden: ladder.overridden,
            model: usedModel,
            ms: Date.now() - started,
            aiCalls: callCount + 1
        };

        cacheSet(key, result);
        await recordTurn(sessionId, {
            kind: safeKind,
            skillId: raw.skill_id,
            questionId: raw.id,
            payload: {
                kind: safeKind,
                mode: ladder.mode,
                model: usedModel,
                ms: result.ms,
                cached: false,
                fallback: false,
                steps: result.script.length,
                sanitized
            }
        });

        return result;
    }

    /** One call at the end of a session; template text is the fallback. */
    async function summary({ sessionId, payload = {} } = {}) {
        const template = String(payload.summary || '').trim();
        const callCount = await countCalls(sessionId);
        if (callCount >= CAPS.perSession || !template) {
            return { ok: true, line: template, fallback: true, cached: false, aiCalls: callCount };
        }
        const key = cacheKey({ skillId: 0, questionId: 0, distractor: '', mode: 'summary', kind: 'summary' });
        const messages = [
            { role: 'system', content: prompts.SYSTEM_PROMPT },
            {
                role: 'system',
                content: [
                    'SESSION FACTS (already computed by the server; do not invent numbers)',
                    template,
                    payload.nextStep ? `Server's next step: ${payload.nextStep}` : '',
                    `Items moved: ${Number(payload.done) || 0} of ${Number(payload.total) || 0}`,
                    `Minutes: ${Number(payload.minutes) || 0}`
                ]
                    .filter(Boolean)
                    .join('\n')
            },
            { role: 'user', content: prompts.TASKS.summary + ' Reply as {"say":"..."}.' }
        ];

        try {
            const text = await chat(messages, {
                max_tokens: 160,
                temperature: 0.4,
                budgetMs: Number(payload.budgetMs) || CAPS.summaryBudgetMs,
                jsonMust: true
            });
            const parsed = parseJsonLoose(text);
            const line = prompts.clampText(parsed && parsed.say ? parsed.say : text, 320);
            if (!line) return { ok: true, line: template, fallback: true, cached: false, aiCalls: callCount };
            cacheSet(key, line);
            await recordTurn(sessionId, { kind: 'summary', payload: { kind: 'summary', ms: 0, chars: line.length } });
            return { ok: true, line, fallback: false, cached: false, aiCalls: callCount + 1 };
        } catch (e) {
            return {
                ok: true,
                line: template,
                fallback: true,
                cached: false,
                bankMode: e && (e.code === 'AI_RATE_LIMITED' || e.status === 429),
                aiCalls: callCount
            };
        }
    }

    /**
     * A board scene for one question. The model writes a small canvas scene; the
     * validator only lets a safe one through, and any failure returns the
     * authored method rather than an unrelated stock graph.
     */
    const boardCache = new Map();
    /** Plain-text first (code travels verbatim), JSON only if the model ignored it. */
    function sanitizeBoardReply(sceneModule, text) {
        return sceneModule.parseSceneText(text) || parseJsonLoose(text);
    }
    async function boardScene({ userId, sessionId, questionId, ask } = {}) {
        if (!questionId) return { ok: false, error: 400, message: 'questionId is required' };
        const raw = await qbank.getRaw(questionId);
        if (!raw) return { ok: false, error: 404, message: 'Question not found' };

        if (typeof query === 'function' && userId && sessionId) {
            // Matching only `f.skill_id` rejected every review card: its question
            // belongs to one of the unit's skills, not to the review item itself.
            const owned = await query(
                `SELECT f.skill_id, f.question_ids, f.review_pool
                   FROM session_focus_items f
                   JOIN sessions s ON s.id = f.session_id
                  WHERE f.session_id = ? AND s.user_id = ?`,
                [sessionId, userId]
            );
            const list = (value) => {
                try {
                    const parsed = typeof value === 'string' ? JSON.parse(value) : value;
                    return Array.isArray(parsed) ? parsed.map(Number) : [];
                } catch (_) {
                    return [];
                }
            };
            const qid = Number(raw.id);
            const member = owned.some(
                (row) =>
                    Number(row.skill_id) === Number(raw.skill_id) ||
                    list(row.question_ids).includes(qid) ||
                    list(row.review_pool).includes(qid)
            );
            if (!member) return { ok: false, error: 404, message: 'That question is not part of this session' };
        }

        const key = `${raw.id}|${String(ask || '').slice(0, 120)}`.toLowerCase();
        const cached = boardCache.get(key);
        if (cached && cached.expiresAt > Date.now()) return Object.assign({}, cached.value, { cached: true });
        if (boardCache.size > 300) boardCache.clear();

        const skill = await qbank.getSkill(raw.skill_id);
        const card = qbank.toCard(raw);
        const solution = raw.solution_steps ? qbank.solutionFor(raw) : null;
        let hint = '';
        try {
            hint = typeof qbank.hintFor === 'function' ? qbank.hintFor(raw, 0) || '' : '';
        } catch (_) {
            hint = '';
        }
        const sceneModule = require('./board-scene');

        let scene = null;
        let dropped = [];
        let lastText = '';
        let lastError = '';
        let usedModel = BOARD_MODEL;
        const messages = sceneModule.buildMessages({ question: card, skill, solution, ask });
        // A scene carries code, so a truncated reply is the common failure. Two
        // attempts: the second asks for a shorter, compact object.
        for (let attempt = 0; attempt < 2 && !scene; attempt += 1) {
            const nudge =
                attempt === 0
                    ? messages
                    : messages.concat([
                          {
                              role: 'user',
                              content:
                                  'Your previous reply did not follow the format. Reply again with TITLE, CONTROLS and the JavaScript only. No prose, no reasoning, no markdown fences.'
                          }
                      ]);
            try {
                const text = await chat(nudge, {
                    model: BOARD_MODEL,
                    reasoning: BOARD_REASONING || undefined,
                    max_tokens: attempt === 0 ? 2600 : 2200,
                    temperature: attempt === 0 ? 0.45 : 0.3,
                    budgetMs: CAPS.boardBudgetMs,
                    // The scene protocol is plain text on purpose: code with
                    // newlines and quotes cannot survive a JSON string.
                    jsonMust: false,
                    onModel: (model) => {
                        if (model) usedModel = String(model);
                    }
                });
                lastText = text == null ? `(null ${typeof text})` : `${typeof text}:${String(text).length}`;
                const verdict = sceneModule.sanitizeScene(sanitizeBoardReply(sceneModule, text));
                dropped = verdict.dropped;
                scene = verdict.scene;
                if (!scene) info(`[session.ai] board reply ${attempt + 1} unusable: ${String(text || '').slice(0, 160)}`);
            } catch (e) {
                lastError = (e && (e.code || e.message)) || String(e);
                info(`[session.ai] board scene unavailable: ${lastError}`);
                break; // a transport failure will not improve on a retry
            }
        }
        if (!scene && dropped.length) info(`[session.ai] board scene rejected: ${dropped.slice(0, 3).join('; ')}`);
        // A scene may arrive with code only: pair it with the authored method so
        // the board still reads like a worked example.
        if (scene && !scene.steps.length) {
            scene.steps = (solution && Array.isArray(solution.steps) ? solution.steps : [])
                .slice(0, 3)
                .map((step) => sceneModule.clampText(step, 140))
                .filter(Boolean);
            if (!scene.steps.length && hint) scene.steps = [sceneModule.clampText(hint, 140)];
        }
        // The model that actually answered, so a fallback inside the chain is visible.
        if (scene) scene.model = usedModel;

        if (!scene) {
            const fallback = sceneModule.fallbackScene({ question: card, skill, solution, hint });
            fallback.dropped = lastError ? dropped.concat([`error: ${lastError}`]) : dropped;
            boardCache.set(key, { value: fallback, expiresAt: Date.now() + CAPS.fallbackTtlMs });
            return fallback;
        }

        const out = { ok: true, fallback: false, cached: false, dropped, scene };
        boardCache.set(key, { value: out, expiresAt: Date.now() + 15 * 60 * 1000 });
        await recordTurn(sessionId, {
            kind: 'board',
            skillId: raw.skill_id,
            questionId: raw.id,
            payload: { kind: 'board', code: scene.code ? scene.code.length : 0, preset: scene.preset || null }
        });
        return out;
    }

    return {
        CAPS,
        boardScene,
        counts: () => ({ entries: cache.size, calls: Object.fromEntries(local.calls) }),
        decideMode,
        decideNext,
        leaksAnswer,
        summary,
        turn,
        validateAction,
        _cacheKey: cacheKey,
        _cacheClear: () => cache.clear()
    };
}

module.exports = createSessionAI;
module.exports.CAPS = CAPS;
module.exports.decideMode = decideMode;
module.exports.decideNext = decideNext;
module.exports.leaksAnswer = leaksAnswer;
module.exports.validateAction = validateAction;
module.exports.parseJsonLoose = parseJsonLoose;
