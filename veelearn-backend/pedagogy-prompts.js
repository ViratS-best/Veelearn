'use strict';

/**
 * The teaching prompt, the action protocol and everything the server uses to
 * decide whether a model reply is allowed to reach the page.
 *
 * This module is pure data + pure functions on purpose: the validation here is
 * what makes a free model safe to put in front of a learner, so it must be
 * testable without a network, a database or an API key.
 *
 * The whitelists mirror the client players:
 *   primitives → assets in annotate.js (`global.Annotate`)
 *   presets    → SUPPORTED in board.js (the existing widget engine)
 * test-ai-session.js parses both frontend files and fails if they drift.
 */

/** The 12 annotation primitives, as the player names them. */
const PRIMITIVES = [
    'underline',
    'highlight',
    'circle',
    'ellipseLabel',
    'arrow',
    'curve',
    'strike',
    'box',
    'brace',
    'sweep',
    'stamp',
    'shake'
];

/** Spellings the design document and other models use. */
const PRIMITIVE_ALIASES = {
    'ellipse_label': 'ellipseLabel',
    'ellipse-with-label': 'ellipseLabel',
    'ellipse': 'ellipseLabel',
    'curved_pointer': 'curve',
    'curved-pointer': 'curve',
    'strikethrough': 'strike',
    'strike_through': 'strike',
    'underline_sweep': 'sweep',
    'underline-sweep': 'sweep'
};

/** Non-drawing script steps the player also understands. */
const CONTROL_STEPS = ['say', 'move', 'mood', 'board'];

/** Board presets the widget engine really mounts (board.js SUPPORTED). */
const PRESETS = [
    'number_line',
    'function_plot',
    'area_shade',
    'coordinate_plane',
    'geometry_board',
    'triangle_lab',
    'unit_circle',
    'parametric_plot',
    'inequality_region',
    'projectile'
];

/** Mascot moods, as mascot.js implements them. */
const MOODS = ['idle', 'happy', 'thinking', 'oops', 'talking', 'pointing', 'writing', 'cheer', 'sleepy'];

/** The mode ladder. The server counts; the model only proposes. */
const MODES = ['focus', 'funnel', 'teach', 'verify', 'celebrate'];
const NEXT_ACTIONS = ['reask', 'more', 'advance', 'teach', 'wrap'];

/**
 * Anchors a script may point at. Anything else is dropped: a script that
 * annotates a selector that is not on the page is worse than no annotation.
 */
const ANCHORS = [
    '[data-annotate=stem]',
    '[data-annotate=why]',
    '[data-annotate=solution]',
    '[data-annotate=solution-answer]',
    '[data-annotate=verdict]',
    '#sx-question-card',
    '#sx-hintbox',
    '#board',
    '#sx-options [data-key=A]',
    '#sx-options [data-key=B]',
    '#sx-options [data-key=C]',
    '#sx-options [data-key=D]'
];

const LIMITS = {
    script: 6,
    scriptHard: 12,
    say: 280,
    ask: 160,
    text: 80,
    turns: 6,
    summary: 400,
    maxAt: 12000
};

const SYSTEM_PROMPT = `You are the teaching voice inside a Veelearn practice session. Veelearn already graded the student's answer with an answer key. You never grade, never award progress and never decide what happens next: you say one short, specific thing and choose the annotation script the mascot draws while it talks.

WHAT YOU RECEIVE
- The question card: stem, options, tier. The correct option is deliberately withheld.
- The skill: name, level, prerequisites, common misconceptions.
- On a wrong answer: the option the student chose and the authored reason it is tempting.
- At most the last six turns of this session.

HOW TO TALK
- Warm, brief, specific. Two sentences at most, 280 characters total.
- Name the misconception in the first four words of a reteach ("You multiplied the exponents instead of adding them.").
- Praise the reasoning, never the child. Never say "Great job!".
- Never state, spell out, compute or hint at the final answer, and never name which option is correct.
- No markdown, no lists, no headings. Plain sentences.

HOW TO DRAW
- Emit a script of 1 to 6 steps. Fewer is better: one underline that lands beats five that flash past.
- "do" is one of: ${PRIMITIVES.join(', ')}, plus the control steps say, move, mood, board.
- "anchor" must be exactly one of: ${ANCHORS.join(' | ')}
- "text" must be a short phrase copied from the anchored element (a few words), or omitted to use the whole element.
- "at" is milliseconds from the start of the script and must increase.
- Use "board" only when the question card carries a visual preset, and pass that preset back unchanged.
- A "say" step may carry at most 140 characters; keep total narration to two bubbles.

MODES
focus (a question about their reasoning) → funnel (one narrowing hint) → teach (worked method) → verify (independent attempt). The server decides the mode and will override yours if it disagrees; report the mode you were asked for.

ANSWER WITH ONE JSON OBJECT AND NOTHING ELSE:
{"say":"...","mood":"thinking","mode":"funnel","script":[{"at":0,"do":"underline","anchor":"[data-annotate=stem]","text":"per week"}],"ask":{"text":"..."},"next":{"action":"reask"}}

"next.action" is a request, not an instruction: reask | more | advance | teach | wrap.`;

const TASKS = {
    teach:
        'Write the two-sentence teaching intro for this item, then the script that draws the one relationship that matters. Do not give the answer.',
    reteach:
        'The student has now missed this item twice. Name the misconception in the first four words, then draw the method: box the worked steps (if they are on the page) or arrow the key phrase, and point at the board when a diagram helps.',
    explain_again:
        'The student asked you to explain it differently. Use a different example or a different representation from the script you already played, and keep it to two sentences.',
    ask: 'The student asked a question of their own. Answer it in two sentences without revealing this item\'s answer, then draw one underline if a phrase in the card deserves it.',
    summary: 'Write two sentences for the end of the session: what moved forward, and exactly what to do next time. No celebration language.'
};

/** Normalise a primitive name the model may have spelled differently. */
function normalizePrimitive(name) {
    const raw = String(name == null ? '' : name).trim();
    if (!raw) return '';
    if (PRIMITIVES.includes(raw)) return raw;
    const lower = raw.replace(/\s+/g, '');
    if (PRIMITIVES.includes(lower)) return lower;
    const alias = PRIMITIVE_ALIASES[lower] || PRIMITIVE_ALIASES[raw.toLowerCase()];
    return alias || '';
}

function clampText(value, limit) {
    const text = String(value == null ? '' : value)
        .replace(/\s+/g, ' ')
        .trim();
    if (!text) return '';
    if (text.length <= limit) return text;
    const cut = text.lastIndexOf(' ', limit);
    return `${text.slice(0, cut > limit * 0.6 ? cut : limit).trim()}…`;
}

/** A two-sentence safe say, from the authored reason — never from the key. */
function safeSay(why, fallback) {
    const source = String(why || '').trim();
    if (!source) return fallback;
    const sentences = source.split(/(?<=[.!?])\s+/).slice(0, 2).join(' ');
    return clampText(sentences, LIMITS.say);
}

/**
 * Deterministic script used when the model is unavailable, rate-limited, slow
 * or caught leaking. It is the same choreography the page used before P3, so a
 * fallback looks intentional rather than broken.
 */
function templateFallback({ mode, question, why, solution, distractor, say } = {}) {
    const optionKey = String(distractor || '').toUpperCase();
    const optionAnchor = /^[ABCD]$/.test(optionKey) ? `#sx-options [data-key=${optionKey}]` : '';
    const script = [];
    const teach = mode === 'teach' || mode === 'verify';

    if (optionAnchor && !teach) {
        script.push({ at: 0, do: 'circle', anchor: optionAnchor });
    } else if (optionAnchor) {
        script.push({ at: 0, do: 'strike', anchor: optionAnchor });
    }

    if (teach && solution && Array.isArray(solution.steps) && solution.steps.length) {
        script.push({ at: 300, do: 'box', anchor: '[data-annotate=solution]' });
        script.push({ at: 700, do: 'arrow', anchor: '[data-annotate=solution-answer]' });
    } else {
        script.push({ at: 320, do: 'curve', anchor: '[data-annotate=why]' });
        const phrase = safeSay(why, '');
        if (phrase) {
            const firstSentence = phrase.split(/(?<=[.!?])\s+/)[0] || '';
            const words = firstSentence.replace(/[.!?]+$/, '').split(' ').slice(0, 6).join(' ');
            if (words.length >= 8) {
                script.push({ at: 520, do: 'underline', anchor: '[data-annotate=why]', text: words });
            }
        }
    }

    const line = say || safeSay(why, teach ? 'Here is the method, step by step. Read the steps, then try the easier one.' : 'Look again at what the question is asking before you choose.');

    return {
        say: clampText(line, LIMITS.say),
        mood: teach ? 'thinking' : 'oops',
        mode: MODES.includes(mode) ? mode : 'funnel',
        script,
        ask: null,
        next: { action: teach ? 'teach' : 'reask' },
        fallback: true
    };
}

/**
 * Assemble the ~2k-token input described in the design: system prompt, brief,
 * skill context, question card, last turns, rolling summary.
 *
 * Security: the answer key is never accepted here. `question` must be the
 * client-safe card (qbank.toCard), and `why` is the authored distractor
 * rationale, which is released only after grading.
 */
function buildMessages({ kind = 'reteach', question, skill, brief, turns, summary, distractor, why, mode } = {}) {
    if (!question || !question.stem) {
        throw Object.assign(new Error('A question card is required'), { status: 400 });
    }

    const block = [];
    if (brief) block.push(String(brief).slice(0, 600));
    if (skill) {
        const bits = [`Skill: ${skill.name || skill.code || 'this skill'}`];
        if (skill.level != null) bits.push(`Current level: ${skill.level} of 4 dots`);
        if (skill.grade_band) bits.push(`Grade band: ${skill.grade_band}`);
        if (skill.prereq) bits.push(`Prerequisite: ${skill.prereq}`);
        const miscon = Array.isArray(skill.misconceptions) ? skill.misconceptions.filter(Boolean).slice(0, 4) : [];
        if (miscon.length) bits.push(`Common misconceptions:${'\n'}- ${miscon.join('\n- ')}`);
        block.push(bits.join('\n'));
    }

    const options = Array.isArray(question.options) ? question.options : [];
    const optionLines = options.map((o) => `${String(o.k || '').toUpperCase()}) ${String(o.t || '')}`).join('\n');
    block.push(
        [
            'QUESTION CARD (the correct option is withheld; do not guess it)',
            String(question.stem || '').slice(0, 900),
            optionLines,
            `Tier: ${Number(question.tier) || 1} of 4`,
            question.visual && question.visual.preset ? `Visual on the card: preset "${question.visual.preset}"` : ''
        ]
            .filter(Boolean)
            .join('\n')
    );

    if (mode) block.push(`Mode the server has set: ${mode}`);

    const lastTurns = [];
    if (Array.isArray(turns)) {
        for (const t of turns.slice(-LIMITS.turns)) {
            const text = clampText(t && t.text, 300);
            if (!text) continue;
            lastTurns.push(`${t.role === 'user' ? 'Student' : 'You'} said: ${text}`);
        }
    }
    if (lastTurns.length) block.push(`LAST TURNS\n${lastTurns.join('\n')}`);
    if (summary) block.push(`EARLIER IN THIS SESSION\n${clampText(summary, LIMITS.summary)}`);

    if (distractor) {
        const chosen = options.find((o) => String(o.k || '').toUpperCase() === String(distractor).toUpperCase());
        block.push(
            [
                'THE STUDENT CHOSE',
                chosen ? `${String(chosen.k).toUpperCase()}) ${chosen.t}` : String(distractor),
                why ? `Why that is tempting (authored): ${clampText(why, 320)}` : ''
            ]
                .filter(Boolean)
                .join('\n')
        );
    }

    return [
        { role: 'system', content: SYSTEM_PROMPT },
        { role: 'system', content: block.join('\n\n') },
        { role: 'user', content: TASKS[kind] || TASKS.reteach }
    ];
}

module.exports = {
    ANCHORS,
    CONTROL_STEPS,
    LIMITS,
    MODES,
    MOODS,
    NEXT_ACTIONS,
    PRESETS,
    PRIMITIVES,
    PRIMITIVE_ALIASES,
    SYSTEM_PROMPT,
    TASKS,
    buildMessages,
    clampText,
    normalizePrimitive,
    safeSay,
    templateFallback
};
