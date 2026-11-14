'use strict';

/**
 * Phase 3 checks that need no API key, no database and no network.
 *
 *   node test-ai-session.js
 *
 * The point of P3 is that a free model cannot break a session: everything it
 * says is validated here, and every failure path has to end in a playable
 * deterministic script. These checks cover the acceptance tests from §19.3
 * (call budget, 429 → bank mode, no answer leaks) plus the protocol itself.
 */

const path = require('path');
const fs = require('fs');

const prompts = require('./pedagogy-prompts');
const createSessionAI = require('./session-ai');

const FRONTEND = path.join(__dirname, '..', 'veelearn-frontend');

let pass = 0;
const failures = [];
function ok(name, cond, detail) {
    if (cond) {
        pass += 1;
        return;
    }
    failures.push(detail ? `${name} — ${detail}` : name);
}

// --------------------------------------------------------- the one provider
// OpenRouter is retired: every AI call goes through Hack Club AI with gemma.
const chatClient = require('./ai-chat');
const hackclub = require('./hackclub-ai');

ok('the shared model is gemma on Hack Club', chatClient.DEFAULT_MODEL === 'google/gemma-4-26b-a4b-it:free', chatClient.DEFAULT_MODEL);
ok('the Hack Club client defaults to the same model', hackclub.DEFAULT_MODEL === 'google/gemma-4-26b-a4b-it:free', hackclub.DEFAULT_MODEL);
ok('the endpoint is Hack Club, not OpenRouter', /ai\.hackclub\.com/.test(fs.readFileSync(path.join(__dirname, 'hackclub-ai.js'), 'utf8')));
ok('no backend file still calls the OpenRouter API', !/openrouter\.ai/i.test(fs.readFileSync(path.join(__dirname, 'ai-chat.js'), 'utf8').replace(/^\s*\*.*$/gm, '')));

const savedHcKey = process.env.HACKCLUBAI_KEY;
process.env.HACKCLUBAI_KEY = ' hc-test-key ';
ok('the Hack Club key is read for the config checks', JSON.stringify(chatClient.getAiKeys()) === JSON.stringify(['hc-test-key']), JSON.stringify(chatClient.getAiKeys()));
if (savedHcKey === undefined) delete process.env.HACKCLUBAI_KEY;
else process.env.HACKCLUBAI_KEY = savedHcKey;

ok('a stale dots model in env falls back to gemma', (() => {
    const before = process.env.HACKCLUBAI_MODEL;
    process.env.HACKCLUBAI_MODEL = 'dots-studio/dots-3-note-preview:free';
    const model = hackclub.getHackClubModel();
    if (before === undefined) delete process.env.HACKCLUBAI_MODEL;
    else process.env.HACKCLUBAI_MODEL = before;
    return model === 'google/gemma-4-26b-a4b-it:free';
})());
ok('a deliberate model override still wins', (() => {
    const before = process.env.HACKCLUBAI_MODEL;
    process.env.HACKCLUBAI_MODEL = 'google/gemma-4-31b-it:free';
    const model = hackclub.getHackClubModel();
    if (before === undefined) delete process.env.HACKCLUBAI_MODEL;
    else process.env.HACKCLUBAI_MODEL = before;
    return model === 'google/gemma-4-31b-it:free';
})());

ok('no key means an empty list', (() => {
    const before = process.env.HACKCLUBAI_KEY;
    delete process.env.HACKCLUBAI_KEY;
    const list = chatClient.getAiKeys();
    if (before !== undefined) process.env.HACKCLUBAI_KEY = before;
    return list.length === 0;
})());

const savedModel = process.env.HACKCLUBAI_MODEL;
process.env.HACKCLUBAI_MODEL = 'google/other-model:free';
const candidateList = chatClient.getModelCandidates({ model: 'explicit/model' });
ok('an explicit model is tried first', candidateList[0] === 'explicit/model', candidateList.join(','));
ok('the env model and gemma are both candidates', candidateList.includes('google/other-model:free') && candidateList.includes('google/gemma-4-26b-a4b-it:free'));
if (savedModel === undefined) delete process.env.HACKCLUBAI_MODEL;
else process.env.HACKCLUBAI_MODEL = savedModel;

// Prose callers must not be told to answer in JSON; the session scripts must.
const prosePacking = hackclub.toHackClubMessages([{ role: 'system', content: 'You are a tutor.' }, { role: 'user', content: 'help' }], { jsonMust: false });
const jsonPacking = hackclub.toHackClubMessages([{ role: 'user', content: 'give me a script' }], { jsonMust: true });
ok('prose mode does not force JSON', !/MUST use JSON/i.test(JSON.stringify(prosePacking.messages)));
ok('json mode does force JSON', /MUST use JSON/i.test(JSON.stringify(jsonPacking.messages)));
ok('system text survives as instructions', /INSTRUCTIONS/.test(JSON.stringify(prosePacking.messages)));

// ------------------------------------------------------------ frontend parity
const annotateSrc = fs.readFileSync(path.join(FRONTEND, 'annotate.js'), 'utf8');
const apiBlock = annotateSrc.slice(annotateSrc.indexOf('  const api = {'));
const playerNames = [...apiBlock.slice(0, apiBlock.indexOf('};')).matchAll(/^\s{4}(\w+),?$/gm)].map((m) => m[1]);
const helpers = ['attach', 'clear', 'play', 'labelOf', 'isReduced', 'count', 'MAX_LIVE'];
const playerPrimitives = playerNames.filter((n) => !helpers.includes(n));

ok('the player exposes 12 drawing primitives', playerPrimitives.length === 12, playerPrimitives.join(','));
ok(
    'the server whitelist is exactly the player vocabulary',
    playerPrimitives.length === prompts.PRIMITIVES.length && playerPrimitives.every((p) => prompts.PRIMITIVES.includes(p)),
    `${playerPrimitives.join(',')} vs ${prompts.PRIMITIVES.join(',')}`
);

const boardSrc = fs.readFileSync(path.join(FRONTEND, 'board.js'), 'utf8');
const supportedBlock = boardSrc.slice(boardSrc.indexOf('const SUPPORTED = ['), boardSrc.indexOf('];', boardSrc.indexOf('const SUPPORTED = [')));
const boardPresets = [...supportedBlock.matchAll(/'([a-z0-9_]+)'/g)].map((m) => m[1]);
ok('the board advertises its presets', boardPresets.length >= 10, String(boardPresets.length));
ok(
    'the prompt preset list matches the board',
    boardPresets.length === prompts.PRESETS.length && boardPresets.every((p) => prompts.PRESETS.includes(p)),
    `${boardPresets.join(',')} vs ${prompts.PRESETS.join(',')}`
);

const mascotSrc = fs.readFileSync(path.join(FRONTEND, 'mascot.js'), 'utf8');
const mouthBlock = mascotSrc.slice(mascotSrc.indexOf('const MOUTH'), mascotSrc.indexOf('};', mascotSrc.indexOf('const MOUTH')));
const mouthKeys = [...mouthBlock.matchAll(/^\s{4}(\w+):/gm)].map((m) => m[1]);
ok('the rig implements every mood the protocol allows', prompts.MOODS.every((m) => mouthKeys.includes(m)), mouthKeys.join(','));
ok('the protocol has no mood the rig cannot draw', prompts.MOODS.length === mouthKeys.length, `${prompts.MOODS.length} vs ${mouthKeys.length}`);

// ------------------------------------------------------------------- fixtures
const ALGEBRA = {
    id: 501,
    skill_id: 7,
    tier: 2,
    qtype: 'mcq',
    stem: 'Solve 2x + 5 > 17. Which step keeps the inequality true?',
    options: JSON.stringify([
        { k: 'A', t: 'Subtract 5 from both sides, then divide both sides by 2', why: '' },
        { k: 'B', t: 'Subtract 5 from both sides, then multiply both sides by 2', why: 'You multiplied where you should have divided.' },
        { k: 'C', t: 'Divide both sides by 2 first, then subtract 5', why: 'Dividing first hides the constant you need.' },
        { k: 'D', t: 'Add 5 to both sides, then divide both sides by 2', why: 'Adding the constant instead of subtracting it.' }
    ]),
    answer: 'A',
    hints: JSON.stringify(['What is the inverse of adding 5?']),
    solution_steps: JSON.stringify(['2x + 5 > 17', '2x > 12', 'x > 6']),
    visual: null
};

const NUMERIC = {
    id: 502,
    skill_id: 7,
    tier: 1,
    qtype: 'mcq',
    qtype: 'numeric',
    stem: 'Solve 2x = 14.',
    options: JSON.stringify([
        { k: 'A', t: 'x = 7', why: '' },
        { k: 'B', t: 'x = 28', why: 'You multiplied instead of dividing.' },
        { k: 'C', t: 'x = 12', why: 'You subtracted 2 instead of dividing by 2.' },
        { k: 'D', t: 'x = 9', why: 'You added 2 instead of dividing by 2.' }
    ]),
    answer: '7',
    hints: JSON.stringify(['What is the inverse of multiplying by 2?']),
    solution_steps: JSON.stringify(['2x = 14', 'x = 7']),
    visual: null
};

function makeQBank(rows) {
    const table = new Map(rows.map((r) => [r.id, r]));
    return {
        getRaw: async (id) => table.get(Number(id)) || null,
        getSkill: async (id) => ({ id, code: 'ALG.INEQ', name: 'Solving inequalities', grade_band: '6-8', misconceptions: JSON.stringify(['flips the inequality when it should not']) }),
        toCard: (row) => ({
            id: row.id,
            skillId: row.skill_id,
            tier: row.tier,
            type: row.qtype,
            stem: row.stem,
            options: JSON.parse(row.options).map((o) => ({ k: o.k, t: o.t })),
            hints: JSON.parse(row.hints),
            visual: null
        }),
        whyFor: (row, key) => {
            const hit = JSON.parse(row.options).find((o) => String(o.k).toUpperCase() === String(key || '').toUpperCase());
            return hit && hit.why ? hit.why : '';
        },
        solutionFor: (row) => ({ steps: JSON.parse(row.solution_steps), answer: String(row.answer) })
    };
}

function makeDb() {
    const events = [];
    return {
        events,
        query: async (sql, params) => {
            if (/COUNT\(\*\)/i.test(sql) && /session_events/i.test(sql)) return [{ c: events.length }];
            if (/MAX\(seq\)/i.test(sql)) return [{ s: events.length + 1 }];
            if (/INSERT INTO session_events/i.test(sql)) {
                events.push(params);
                return { affectedRows: 1 };
            }
            if (/session_focus_items/i.test(sql)) return [{ id: 1 }];
            if (/skill_mastery/i.test(sql)) return [{ level: 2 }];
            return [];
        }
    };
}

let chatCalls = 0;
function scriptedChat(replies) {
    chatCalls = 0;
    const queue = Array.isArray(replies) ? replies.slice() : [];
    return async () => {
        chatCalls += 1;
        const next = queue.length > 1 ? queue.shift() : queue[0];
        if (next instanceof Error) throw next;
        return typeof next === 'string' ? next : JSON.stringify(next);
    };
}

function aiWith(chat, rows = [ALGEBRA, NUMERIC]) {
    const db = makeDb();
    const ai = createSessionAI({ query: db.query, qbank: makeQBank(rows), chat });
    return { ai, db };
}

// The player must understand every step the validator can emit.
const controlPlayed = ['say', 'move', 'mood', 'board'].every((name) =>
    new RegExp(`action === '${name}'`).test(annotateSrc)
);
ok('the player handles every control step the validator emits', controlPlayed);
ok(
    'every primitive the validator emits is a player function',
    prompts.PRIMITIVES.every((p) => playerNames.includes(p)),
    prompts.PRIMITIVES.filter((p) => !playerNames.includes(p)).join(',')
);

// ------------------------------------------------------------- prompt safety
const card = makeQBank([ALGEBRA]).toCard(ALGEBRA);
const messages = prompts.buildMessages({
    kind: 'reteach',
    question: card,
    skill: { name: 'Solving inequalities', level: 2, misconceptions: ['flips the inequality'] },
    distractor: 'B'
});
const promptText = JSON.stringify(messages);
ok('the prompt is three messages', messages.length === 3);
ok('the prompt never carries the answer key', !promptText.includes('"answer"') && !/answer\s*[:=]\s*"?A"?/i.test(promptText), promptText.slice(0, 120));
ok('the prompt keeps the stem', promptText.includes('2x + 5 > 17'));
ok('the prompt keeps the options', promptText.includes('multiply both sides by 2'));
ok('the prompt carries the chosen distractor and its authored reason', promptText.includes('THE STUDENT CHOSE') && promptText.includes('You multiplied'));
ok('the prompt names the skill', promptText.includes('Solving inequalities'));
ok('the system prompt forbids revealing the answer', /never state, spell out, compute or hint at the final answer/i.test(prompts.SYSTEM_PROMPT));
ok('the system prompt lists the whitelist', prompts.PRIMITIVES.every((p) => prompts.SYSTEM_PROMPT.includes(p)));
ok('the system prompt demands one JSON object', /ONE JSON OBJECT/.test(prompts.SYSTEM_PROMPT));
ok('a missing card is rejected', (() => {
    try {
        prompts.buildMessages({ kind: 'reteach', question: null });
        return false;
    } catch (e) {
        return e.status === 400;
    }
})());

// --------------------------------------------------------------- the protocol
const good = prompts.templateFallback({ mode: 'funnel', question: card, why: ALGEBRA_answer(), distractor: 'B' });
function ALGEBRA_answer() {
    return JSON.parse(ALGEBRA.options).find((o) => o.k === 'B').why;
}
ok('the template sanitises to 6 steps or fewer', good.script.length <= prompts.LIMITS.scriptHard);
ok('the template only uses playable anchors', good.script.every((s) => prompts.ANCHORS.includes(s.anchor || '#board')));
ok('the template names the misconception first', /^You multiplied/.test(good.say), good.say);
ok('the template is under the say cap', good.say.length <= prompts.LIMITS.say);
ok('the template is flagged', good.fallback === true);

const validated = createSessionAI.validateAction(
    {
        say: '  You   multiplied where you should have divided.  ',
        mood: 'oops',
        mode: 'funnel',
        script: [
            { at: 0, do: 'circle', anchor: '#sx-options [data-key=B]' },
            { at: 200, do: 'curved_pointer', anchor: '[data-annotate=why]' },
            { at: 400, do: 'laser', anchor: '[data-annotate=why]' },
            { at: 500, do: 'underline', anchor: '#sx-nope' },
            { at: 600, do: 'board', preset: 'holo_deck' },
            { at: 700, do: 'board', preset: 'number_line', params: { elements: [] } },
            { at: 800, do: 'mood', mood: 'chartreuse' },
            { at: 900, do: 'say', text: 'Look at the step where you multiplied.' }
        ],
        ask: { text: 'Which step flipped it?' },
        next: { action: 'advance' }
    },
    { mode: 'funnel', hasSolution: false }
).action;

ok('say whitespace is normalised', validated.say === 'You multiplied where you should have divided.', validated.say);
ok('a snake_case primitive alias is accepted', validated.script.some((s) => s.do === 'curve'));
ok('an unknown primitive is dropped', !validated.script.some((s) => s.do === 'laser'));
ok('an unknown anchor is dropped', !validated.script.some((s) => s.anchor === '#sx-nope'));
ok('an unknown preset is dropped', !validated.script.some((s) => s.preset === 'holo_deck'));
ok('a whitelisted preset survives', validated.script.some((s) => s.do === 'board' && s.preset === 'number_line'));
ok('an unknown mood is dropped', !validated.script.some((s) => s.mood === 'chartreuse'));
ok('steps stay ordered in time', validated.script.every((s, i, a) => i === 0 || s.at > a[i - 1].at));
ok('the script keeps its say step', validated.script.some((s) => s.do === 'say'));
ok('the ask is capped and kept', validated.ask && validated.ask.text === 'Which step flipped it?');

const offscreen = createSessionAI.validateAction(
    { say: 'Look at the steps.', script: [{ at: 0, do: 'box', anchor: '[data-annotate=solution]' }] },
    { mode: 'funnel', hasSolution: false }
).action;
ok('an annotation on a card that is not on screen is dropped', offscreen.script.length === 0);

const capped = createSessionAI.validateAction(
    {
        say: 'x'.repeat(600),
        script: Array.from({ length: 20 }, (_, i) => ({ at: i * 10, do: 'underline', anchor: '[data-annotate=stem]' }))
    },
    { mode: 'funnel', hasSolution: false }
).action;
ok('the say is capped', capped.say.length <= prompts.LIMITS.say + 1, String(capped.say.length));
ok('the script is capped at 12 strokes', capped.script.length === prompts.LIMITS.scriptHard, String(capped.script.length));

ok('an empty action is rejected', createSessionAI.validateAction({ say: '', script: [] }).action === null);

// ------------------------------------------------------------ the leak guard
ok('"the answer is A" is a leak', createSessionAI.leaksAnswer('The answer is A, so divide both sides.', ALGEBRA));
ok('naming the correct option is a leak', createSessionAI.leaksAnswer('Option A is the correct one.', ALGEBRA));
ok('echoing the correct option text is a leak', createSessionAI.leaksAnswer('Subtract 5 from both sides, then divide both sides by 2.', ALGEBRA));
ok('a numeric answer is a leak', createSessionAI.leaksAnswer('So x = 7.', NUMERIC));
ok('a number within 0.5% is a leak', createSessionAI.leaksAnswer('About 7.02, near enough.', NUMERIC));
ok('an unrelated number is not a leak', !createSessionAI.leaksAnswer('You had two steps and stopped after the first.', NUMERIC));
ok('naming the misconception is not a leak', !createSessionAI.leaksAnswer('You multiplied where you should have divided.', ALGEBRA));

// ----------------------------------------------------------------- the ladder
ok('first miss is funnel', createSessionAI.decideMode({ attempts: 1 }).mode === 'funnel');
ok('second miss is teach', createSessionAI.decideMode({ attempts: 2 }).mode === 'teach');
ok('a correct answer is celebrate', createSessionAI.decideMode({ attempts: 1, correct: true }).mode === 'celebrate');
ok('the server overrides a wrong mode request', createSessionAI.decideMode({ attempts: 2, requested: 'funnel' }).overridden === true);
ok('a wrong answer may not advance', createSessionAI.decideNext({ requested: 'advance', correct: false, attempts: 1 }).action === 'reask');
ok('two misses force teach', createSessionAI.decideNext({ requested: 'reask', correct: false, attempts: 2 }).action === 'teach');
ok('a correct answer may advance', createSessionAI.decideNext({ requested: 'advance', correct: true, attempts: 1 }).action === 'advance');
ok('a finished item advances even if the model asks to stay', createSessionAI.decideNext({ requested: 'more', correct: true, itemsDone: true }).action === 'advance');

// ------------------------------------------------------------ the AI turn
(async () => {
    const modelReply = {
        say: 'You multiplied where you should have divided, so the inequality flipped the wrong way.',
        mood: 'oops',
        mode: 'funnel',
        script: [
            { at: 0, do: 'circle', anchor: '#sx-options [data-key=B]' },
            { at: 300, do: 'underline', anchor: '[data-annotate=why]', text: 'should have divided' }
        ],
        ask: { text: 'Which step flipped it?' },
        next: { action: 'reask' }
    };

    const { ai } = aiWith(scriptedChat([modelReply]));
    const first = await ai.turn({ userId: 3, sessionId: 90, kind: 'reteach', questionId: 501, distractor: 'B', attempts: 1 });
    ok('a valid reply is accepted', first.ok && !first.fallback, JSON.stringify(first).slice(0, 120));
    ok('the model line is kept', /You multiplied/.test(first.say));
    ok('the script survives validation', first.script.length === 2);
    ok('the server decides the mode', first.mode === 'funnel');
    ok('the first call is not cached', first.cached === false);
    ok('one call is counted', first.aiCalls === 1);
    ok('one chat request was made', chatCalls === 1);

    const second = await ai.turn({ userId: 3, sessionId: 90, kind: 'reteach', questionId: 501, distractor: 'B', attempts: 1 });
    ok('the same turn is served from cache', second.cached === true);
    ok('a cached turn costs no call', chatCalls === 1, String(chatCalls));
    ok('the cached payload is identical', second.say === first.say && second.script.length === first.script.length);
    ok('a cached turn costs no budget', second.aiCalls === 1, String(second.aiCalls));

    // A different distractor is a different cache entry.
    const other = await ai.turn({ userId: 3, sessionId: 90, kind: 'reteach', questionId: 501, distractor: 'C', attempts: 1 });
    ok('a different misconception is not served from cache', other.cached === false && chatCalls === 2);

    // ---- 429 storm: bank mode, still playable
    const rate = Object.assign(new Error('rate limited'), { code: 'AI_RATE_LIMITED', status: 429 });
    const storm = aiWith(scriptedChat([rate]));
    const degraded = await storm.ai.turn({ userId: 3, sessionId: 91, kind: 'reteach', questionId: 501, distractor: 'B', attempts: 2 });
    ok('a 429 still answers', degraded.ok === true);
    ok('a 429 degrades to bank mode', degraded.bankMode === true);
    ok('a 429 returns the template script', degraded.fallback === true && degraded.script.length > 0);
    ok('the degraded script is playable', degraded.script.every((s) => prompts.ANCHORS.includes(s.anchor || '#board')));
    ok('the degraded turn is one chat attempt', chatCalls === 1, String(chatCalls));
    ok('the degraded mode is still the server ladder', degraded.mode === 'teach');

    // ---- a fallback is cached: the same question must not stall twice
    const degradedAgain = await storm.ai.turn({ userId: 3, sessionId: 91, kind: 'reteach', questionId: 501, distractor: 'B', attempts: 2 });
    ok('a fallback is served from cache next time', degradedAgain.cached === true);
    ok('a cached fallback costs no transport call', chatCalls === 1, String(chatCalls));
    ok('a cached fallback still looks the same', degradedAgain.say === degraded.say);

    // ---- a budget overrun is reported as a timeout, not an unknown error
    const slow = Object.assign(new Error('OpenRouter request budget exceeded'), { code: 'AI_TIMEOUT', status: 504 });
    const timedOut = aiWith(scriptedChat([slow]));
    const timeoutTurn = await timedOut.ai.turn({ userId: 3, sessionId: 103, kind: 'reteach', questionId: 501, distractor: 'D', attempts: 2 });
    ok('a slow model is a timeout', timeoutTurn.fallback === true && timeoutTurn.reason === 'timeout', timeoutTurn.reason);
    ok('a timeout counts as bank mode', timeoutTurn.bankMode === true);
    ok('a timeout still returns a playable script', timeoutTurn.script.length > 0);
    ok('a timeout reports the call it spent', timeoutTurn.aiCalls === 1, String(timeoutTurn.aiCalls));

    // ---- no key at all
    const noKey = aiWith(scriptedChat([Object.assign(new Error('nope'), { code: 'AI_NOT_CONFIGURED' })]));
    const unconfigured = await noKey.ai.turn({ userId: 3, sessionId: 92, kind: 'reteach', questionId: 501, distractor: 'B' });
    ok('a missing key is bank mode, not an error', unconfigured.ok === true && unconfigured.bankMode === true);

    // ---- garbage twice, then the template
    const garbage = aiWith(scriptedChat(['I think the learner should divide first.', 'Still not JSON, sorry.']));
    const parsedTwice = await garbage.ai.turn({ userId: 3, sessionId: 93, kind: 'reteach', questionId: 501, distractor: 'C' });
    ok('two bad replies fall back', parsedTwice.fallback === true && parsedTwice.reason === 'parse');
    ok('two parse attempts were made', chatCalls === 2, String(chatCalls));

    // ---- a fenced, chatty reply is still parsed
    const fenced = aiWith(scriptedChat(['Here you go:\n```json\n' + JSON.stringify(modelReply) + '\n```']));
    const fencedOut = await fenced.ai.turn({ userId: 3, sessionId: 94, kind: 'reteach', questionId: 501, distractor: 'B' });
    ok('a fenced reply is parsed', fencedOut.ok && !fencedOut.fallback, fencedOut.reason || '');

    // ---- the model leaks the answer: prose is replaced, the script is kept
    const leaky = aiWith(
        scriptedChat([
            {
                say: 'The answer is A, so divide both sides by 2.',
                mood: 'happy',
                mode: 'funnel',
                script: [{ at: 0, do: 'underline', anchor: '[data-annotate=why]' }]
            }
        ])
    );
    const guarded = await leaky.ai.turn({ userId: 3, sessionId: 95, kind: 'reteach', questionId: 501, distractor: 'B' });
    ok('a leaked answer is caught', guarded.sanitized === true);
    ok('the leaked line is replaced', !/answer is A/i.test(guarded.say), guarded.say);
    ok('the safe line still names the misconception', /multiplied|divide/i.test(guarded.say));
    ok('the script survives the leak', guarded.script.length === 1);

    // ---- numeric answers are guarded too
    const numericLeak = aiWith(
        scriptedChat([{ say: 'x = 7, because you halve 14.', mood: 'happy', mode: 'teach', script: [] }])
    );
    const numeric = await numericLeak.ai.turn({ userId: 3, sessionId: 96, kind: 'reteach', questionId: 502, distractor: 'B', attempts: 2 });
    ok('a numeric leak is caught', numeric.sanitized === true, numeric.say);
    ok('the numeric answer is gone', !/\b7\b/.test(numeric.say), numeric.say);

    // ---- the call budget
    const budget = aiWith(scriptedChat([modelReply]));
    let last = null;
    for (let i = 0; i <= createSessionAI.CAPS.perSession; i++) {
        last = await budget.ai.turn({ userId: 3, sessionId: 97, kind: 'explain_again', questionId: 501, distractor: `X${i}`, attempts: 1 });
    }
    ok('the per-session ceiling is enforced', last.fallback === true && last.reason === 'capped', JSON.stringify(last).slice(0, 90));
    ok('the model is not called past the ceiling', chatCalls === createSessionAI.CAPS.perSession, String(chatCalls));

    const asks = aiWith(scriptedChat([modelReply]));
    let askOut = null;
    for (let i = 0; i < createSessionAI.CAPS.askPerSession + 1; i++) {
        askOut = await asks.ai.turn({ userId: 3, sessionId: 102, kind: 'ask', questionId: 501, distractor: '', attempts: 1 });
    }
    ok('free-form questions are capped per session', askOut.fallback === true && askOut.reason === 'ask_capped', JSON.stringify(askOut).slice(0, 80));
    ok('the ceiling is 15 calls', createSessionAI.CAPS.perSession === 15);
    ok('the clean-session budget is 9', createSessionAI.CAPS.cleanSession <= 9);

    // A clean 20-minute session: one reteach per tested item, no repeats.
    const clean = aiWith(scriptedChat([modelReply]));
    let cleanCalls = 0;
    for (let i = 0; i < 5; i++) {
        const out = await clean.ai.turn({ userId: 3, sessionId: 98, kind: 'reteach', questionId: 501, distractor: ['B', 'C', 'D', 'B', 'C'][i], attempts: 2 });
        cleanCalls = out.aiCalls;
    }
    ok('a clean session stays inside the AI budget', cleanCalls <= createSessionAI.CAPS.cleanSession, String(cleanCalls));

    // ---- the summary
    const summaryAI = aiWith(scriptedChat([{ say: 'You fixed the inequality flip. Next time, name the inverse operation first.' }]));
    const summary = await summaryAI.ai.summary({ sessionId: 99, payload: { summary: 'You moved 1 of 2 items forward.', done: 1, total: 2, minutes: 9 } });
    ok('the summary is generated once', summary.ok && !summary.fallback && /inverse operation/.test(summary.line));
    const summaryFail = aiWith(scriptedChat([rate]));
    const fallbackSummary = await summaryFail.ai.summary({ sessionId: 100, payload: { summary: 'You moved 1 of 2 items forward.' } });
    ok('a failed summary falls back to the stored text', fallbackSummary.fallback === true && fallbackSummary.line === 'You moved 1 of 2 items forward.');

    // ---- scope: a question outside the learner's session is refused
    const db = makeDb();
    const scoped = createSessionAI({
        query: async (sql, params) => {
            if (/session_focus_items/i.test(sql)) return [];
            return db.query(sql, params);
        },
        qbank: makeQBank([ALGEBRA]),
        chat: scriptedChat([modelReply])
    });
    const denied = await scoped.turn({ userId: 3, sessionId: 101, kind: 'reteach', questionId: 501, distractor: 'B' });
    ok('a question outside the session is refused', denied.ok === false && denied.error === 404, JSON.stringify(denied));
    ok('a refused turn makes no model call', chatCalls === 0);

    // ---- the HTTP layer exposes the same guard rails
    const createRoutes = require('./session-routes');
    const apiResponse = (res, status, message, data) => {
        res.out = { status, message, data };
        return res.out;
    };
    const routesDb = makeDb();
    const routes = createRoutes({
        query: routesDb.query,
        qbank: makeQBank([ALGEBRA, NUMERIC]),
        apiResponse,
        log: { info() {} },
        chat: scriptedChat([modelReply])
    });
    ok('the routes expose the AI loop', typeof routes.ai.turn === 'function');
    ok('the routes keep the engine', typeof routes.engine.answer === 'function');
    ok('the routes expose a non-blocking summary', typeof routes.summary === 'function');

    const noSummary = {};
    await routes.summary({ user: { id: 3 }, params: { sessionId: 4242 }, body: {} }, noSummary);
    ok('a missing session summary is a 404', noSummary.out && noSummary.out.status === 404, JSON.stringify(noSummary.out).slice(0, 80));

    const resStub = {};
    await routes.aiTurn(
        { user: { id: 3 }, params: { sessionId: 110 }, body: { kind: 'reteach', questionId: 501, distractor: 'B', attempts: 1 } },
        resStub
    );
    ok('the ai route answers 200', resStub.out && resStub.out.status === 200, JSON.stringify(resStub.out).slice(0, 100));
    ok('the ai route returns a script the client can play', Array.isArray(resStub.out.data.script) && resStub.out.data.script.length > 0);
    ok('the ai route never returns the answer key', !/\"answer\"/.test(JSON.stringify(resStub.out.data)));

    const notFound = {};
    await routes.aiTurn({ user: { id: 3 }, params: { sessionId: 111 }, body: { questionId: 999999 } }, notFound);
    ok('an unknown question is a 404', notFound.out && notFound.out.status === 404, JSON.stringify(notFound.out).slice(0, 80));

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
