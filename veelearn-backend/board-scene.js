'use strict';

/**
 * The board scene: what Vee draws when a learner asks to be shown.
 *
 * The model used to be limited to a widget preset, so every board without one
 * fell back to a stock `y = a·x²` plot, unrelated to the question. This module
 * lets the model write a small canvas scene instead — `draw(ctx, W, H, S, t)` —
 * with sliders the learner can move. The code is untrusted, so it is validated
 * here (length, banned APIs, one `draw` function) and runs in a sandboxed
 * iframe on the page, with no DOM, network or storage access.
 *
 * The same module builds the prompt, validates the reply, and produces the
 * deterministic fallback (the question's own method, never a fake graph).
 */

const prompts = require('./pedagogy-prompts');

const MAX_CODE = 6000;
const MAX_CONTROLS = 3;
const MAX_STEPS = 3;

/** Anything that could reach outside the drawing surface. */
const BANNED = [
    [/\bfetch\s*\(/, 'network access'],
    [/\bXMLHttpRequest\b/, 'network access'],
    [/\bWebSocket\b/, 'network access'],
    [/\bimportScripts\b/, 'worker access'],
    [/\bnew\s+Worker\s*\(/, 'worker access'],
    [/\bimport\s*\(/, 'dynamic import'],
    [/\beval\s*\(/, 'eval'],
    [/\bnew\s+Function\b/, 'Function constructor'],
    [/\bdocument\b/, 'DOM access'],
    [/\bwindow\b/, 'DOM access'],
    [/\bparent\b/, 'frame access'],
    [/\blocalStorage\b/, 'storage access'],
    [/\bsessionStorage\b/, 'storage access'],
    [/\bcookie\b/, 'cookie access'],
    [/\blocation\b/, 'navigation'],
    [/\bpostMessage\b/, 'messaging'],
    [/<[a-z!/]/i, 'markup'],
    [/[\u2028\u2029]/, 'line separators']
];

const PALETTE = 'ink #26221f, accent #ea580c, green #15803d, blue #2563eb, muted #a8a29e, pale #f6efe6';

const SYSTEM_PROMPT = `You write one small interactive canvas drawing for a Veelearn question. You get the question card (the answer is withheld), the skill and the authored method.

Output EXACTLY these three things and nothing else. No preamble, no plan, no explanation, no markdown fences.
You may think silently, but never write the thinking: no reasoning, no notes to yourself, no draft, no "Let me…", no restating the task. The reply starts with TITLE: and ends with the closing brace of draw().

1) TITLE: <specific title, at most 60 characters>
2) CONTROLS: key | label | min | max | step | value, key | label | ...   (1 to 3 sliders, never empty)
3) JavaScript beginning with: function draw(ctx, W, H, S, t) { ... }

The JavaScript is the answer, so start it immediately after the CONTROLS line. Never describe the drawing in words.

THE DRAWING
- ctx is a canvas 2D context, W and H are pixels, S holds slider values (S.a), t is seconds since the board opened.
- Draw the actual quantities in THIS question with its numbers, not a generic graph.
- Animate from t only: shapes, arrows, parts that fill or move.
- A 3D idea is welcome: project the points yourself onto this 2D canvas (isometric or simple perspective) and rotate them from S and t. No WebGL.
- Vector shapes and text only. Label what matters with ctx.fillText.
- Palette: ${PALETTE}. White canvas.
- Under 140 lines, no comments.
- Never use: document, window, parent, fetch, XMLHttpRequest, eval, new Function, import, localStorage, location, postMessage, alerts, images, timers.

CONTROLS
- One line, key | label | min | max | step | value, groups separated by commas. Always at least one.
- Each key must visibly change the drawing through S.key, so the learner can move it and watch the answer follow.
- Pick a quantity the question is actually about: a coefficient, the slope, the intercept, an angle, a length, the point itself. If the card gives fixed numbers, let the learner drag that number and redraw the result.

Only if a stock diagram is genuinely the better drawing, output instead:
PRESET: <one of ${prompts.PRESETS.join(', ')}>
PARAMS: key=value, key=value`;

function clampText(value, max) {
    const text = String(value == null ? '' : value)
        .replace(/\s+/g, ' ')
        .trim();
    if (!text) return '';
    if (text.length <= max) return text;
    return `${text.slice(0, max - 1).trim()}…`;
}

function plainParams(raw) {
    if (!raw || typeof raw !== 'object' || Array.isArray(raw)) return {};
    const out = {};
    let n = 0;
    for (const [key, value] of Object.entries(raw)) {
        if (n >= 12) break;
        if (!/^[a-z][a-z0-9_]{0,23}$/i.test(key)) continue;
        if (typeof value === 'number' && Number.isFinite(value)) out[key] = value;
        else if (typeof value === 'string') out[key] = clampText(value, 60);
        else if (Array.isArray(value) && value.length <= 12 && value.every((v) => typeof v === 'number')) {
            out[key] = value.slice(0, 12);
        } else continue;
        n += 1;
    }
    return out;
}

function plainControls(raw) {
    if (!Array.isArray(raw)) return [];
    const seen = new Set();
    const out = [];
    for (const item of raw.slice(0, MAX_CONTROLS)) {
        if (!item || typeof item !== 'object') continue;
        const key = String(item.key || '').trim();
        if (!/^[a-z][a-z0-9_]{0,15}$/i.test(key) || seen.has(key)) continue;
        const min = Number(item.min);
        const max = Number(item.max);
        if (!Number.isFinite(min) || !Number.isFinite(max) || max <= min || max - min > 1000) continue;
        let step = Number(item.step);
        if (!Number.isFinite(step) || step <= 0) step = (max - min) / 100;
        const value = Number.isFinite(Number(item.value)) ? Math.min(max, Math.max(min, Number(item.value))) : min;
        seen.add(key);
        out.push({
            key,
            label: clampText(item.label, 32) || key,
            min,
            max,
            step,
            value
        });
    }
    return out;
}

function validCode(raw) {
    let code = typeof raw === 'string' ? raw.trim() : '';
    const dropped = [];
    if (!code) return { code: '', dropped };
    if (code.length > MAX_CODE) return { code: '', dropped: ['code too long'] };
    const blocked = BANNED.find(([re]) => re.test(code));
    if (blocked) return { code: '', dropped: [`code blocked: ${blocked[1]}`] };
    if (!/function\s+draw\s*\(/.test(code)) return { code: '', dropped: ['no draw function'] };
    // The code is injected into an inline script: it must never close the tag
    // or start a new one, even if it slipped past the markup check.
    code = code.replace(/<\//g, '<\\/');
    return { code, dropped };
}

function numberPair(raw) {
    if (!raw) return {};
    const out = {};
    String(raw)
        .split(/[,;]\s*/)
        .forEach((pair) => {
            const m = /^\s*([a-z][a-z0-9_]{0,23})\s*[=:]\s*(-?\d+(?:\.\d+)?)\s*$/i.exec(pair);
            if (m) out[m[1]] = Number(m[2]);
        });
    return out;
}

function parseControlLine(item) {
    const bits = String(item || '')
        .split('|')
        .map((b) => b.trim());
    if (bits.length < 6) return null;
    return {
        key: bits[0],
        label: bits[1],
        min: Number(bits[2]),
        max: Number(bits[3]),
        step: Number(bits[4]),
        value: Number(bits[5])
    };
}

/**
 * Take the draw function alone, closing brace included. Prose after the code
 * (an explanation, a second draft) must not travel into the sandbox.
 */
function sliceDrawFunction(src) {
    const at = src.search(/function\s+draw\s*\(/);
    if (at < 0) return '';
    const open = src.indexOf('{', at);
    if (open < 0) return '';
    let depth = 0;
    let quote = null;
    let escaped = false;
    for (let i = open; i < src.length; i += 1) {
        const ch = src[i];
        if (quote) {
            if (escaped) escaped = false;
            else if (ch === '\\') escaped = true;
            else if (ch === quote) quote = null;
            continue;
        }
        if (ch === '"' || ch === "'" || ch === '`') {
            quote = ch;
            continue;
        }
        if (ch === '/' && src[i + 1] === '/') {
            const nl = src.indexOf('\n', i);
            i = nl < 0 ? src.length : nl;
            continue;
        }
        if (ch === '/' && src[i + 1] === '*') {
            const end = src.indexOf('*/', i + 2);
            i = end < 0 ? src.length : end + 1;
            continue;
        }
        if (ch === '{') depth += 1;
        else if (ch === '}') {
            depth -= 1;
            if (depth === 0) return src.slice(at, i + 1).trim();
        }
    }
    return src.slice(at).trim();
}

/**
 * The plain-text scene protocol.
 *
 * Canvas code carries newlines and quotes, which is exactly what a model fails
 * to escape inside a JSON string, so the code is taken verbatim from the first
 * `function draw` to the end of the reply. A model that chats first still works:
 * the TITLE and CONTROLS lines are found anywhere, and the prose is ignored.
 */
function parseSceneText(text) {
    const src = String(text || '').replace(/\r\n/g, '\n').trim();
    if (!src) return null;
    // Some models answer in JSON anyway; let the caller try that separately.
    if (/^\s*\{/.test(src)) return null;

    const scene = { title: '', steps: [], controls: [], preset: '', params: {}, code: '' };
    const CONTROL = /^\s*(-\s*)?(TITLE|STEPS?|CONTROLS?|PRESET|PARAMS|CODE)\s*:\s*(.*)$/i;
    const MODE = {
        title: 'title',
        step: 'steps',
        steps: 'steps',
        control: 'controls',
        controls: 'controls',
        preset: 'preset',
        params: 'params',
        code: 'code'
    };
    const codeLines = [];
    let mode = null;
    let inCode = false;

    for (const rawLine of src.split('\n')) {
        const line = rawLine.replace(/\s+$/, '');
        const head = inCode ? null : CONTROL.exec(line);
        if (head) {
            mode = MODE[head[2].toLowerCase()] || null;
            const rest = (head[3] || '').trim();
            if (mode === 'title' && rest && !scene.title) scene.title = rest.replace(/^["'`]|["'`]$/g, '');
            else if (mode === 'preset' && rest) scene.preset = rest.split(/\s+/)[0];
            else if (mode === 'params' && rest) scene.params = Object.assign(scene.params, numberPair(rest));
            else if (mode === 'controls' && rest) {
                rest.split(/\s*,\s*/)
                    .map(parseControlLine)
                    .filter(Boolean)
                    .forEach((control) => scene.controls.push(control));
            } else if (mode === 'code' && rest) {
                inCode = true;
                codeLines.push(rest);
            }
            continue;
        }

        // Code starts at the first draw function even if the model forgot the
        // CODE header; everything from there is taken verbatim.
        if (!inCode && /function\s+draw\s*\(/.test(line)) {
            inCode = true;
            mode = 'code';
        }
        if (inCode) {
            if (/^\s*```/.test(line)) continue;
            codeLines.push(line);
            continue;
        }
        if (mode === 'steps') {
            const item = line.replace(/^\s*[-*•]\s*/, '').trim();
            if (item && !/^```/.test(item)) scene.steps.push(item);
        } else if (mode === 'controls') {
            const item = line.replace(/^\s*[-*•]\s*/, '').trim();
            if (item) {
                item.split(/\s*,\s*/)
                    .map(parseControlLine)
                    .filter(Boolean)
                    .forEach((control) => scene.controls.push(control));
            }
        }
    }

    scene.steps = scene.steps.slice(0, MAX_STEPS);
    const joined = codeLines.join('\n').trim();
    // Trailing prose after the function is dropped, so only the drawing is sent.
    scene.code = joined ? sliceDrawFunction(joined) || joined : '';
    if (!scene.title && !scene.steps.length && !scene.code && !scene.preset) return null;
    return scene;
}

function sanitizeScene(raw) {
    const dropped = [];
    if (!raw || typeof raw !== 'object') return { scene: null, dropped: ['not an object'] };

    const title = clampText(raw.title, 60) || 'On the board';
    const steps = (Array.isArray(raw.steps) ? raw.steps : [])
        .slice(0, MAX_STEPS)
        .map((s) => clampText(s, 140))
        .filter(Boolean);

    const wanted = String(raw.preset || '').trim();
    const preset = prompts.PRESETS.includes(wanted) ? wanted : '';
    if (wanted && !preset) dropped.push(`unknown preset: ${wanted}`);

    const params = plainParams(raw.params);
    const controls = plainControls(raw.controls);
    const codeVerdict = validCode(raw.code);
    if (codeVerdict.dropped.length) dropped.push(...codeVerdict.dropped);

    if (!steps.length && !preset && !codeVerdict.code) return { scene: null, dropped };

    return {
        scene: {
            title,
            steps,
            preset,
            params,
            controls,
            code: codeVerdict.code
        },
        dropped
    };
}

/**
 * What the board shows when the model is unavailable: the authored method and,
 * if the card arrived with a diagram, that diagram. Never an invented graph.
 */
function fallbackScene({ question, skill, solution, hint } = {}) {
    const steps = (solution && Array.isArray(solution.steps) ? solution.steps : [])
        .slice(0, MAX_STEPS)
        .map((s) => clampText(s, 140))
        .filter(Boolean);
    if (!steps.length && hint) steps.push(clampText(hint, 140));

    const visual = question && question.visual && typeof question.visual === 'object' ? question.visual : {};
    const preset = prompts.PRESETS.includes(String(visual.preset || '')) ? String(visual.preset) : '';

    return {
        ok: true,
        fallback: true,
        dropped: [],
        scene: {
            title: (skill && skill.name) || 'On the board',
            steps,
            preset,
            params: preset && visual.params && typeof visual.params === 'object' ? visual.params : {},
            controls: [],
            code: ''
        }
    };
}

function buildMessages({ question, skill, solution, ask } = {}) {
    const card = question || {};
    const options = Array.isArray(card.options) ? card.options : [];
    const lines = [
        'QUESTION CARD (the correct option is withheld; do not guess it)',
        String(card.stem || '').slice(0, 900),
        options.map((o) => `${String(o.k || '').toUpperCase()}) ${String(o.t || '')}`).join('\n'),
        card.visual && card.visual.preset ? `The card already shows a "${card.visual.preset}" diagram.` : ''
    ].filter(Boolean);

    if (skill && skill.name) {
        const bits = [`Skill: ${skill.name}`];
        if (skill.grade_band) bits.push(`Grade band: ${skill.grade_band}`);
        const miscon = Array.isArray(skill.misconceptions) ? skill.misconceptions.filter(Boolean).slice(0, 3) : [];
        if (miscon.length) bits.push(`Watch for: ${miscon.join('; ')}`);
        lines.push(bits.join('\n'));
    }
    if (solution && Array.isArray(solution.steps) && solution.steps.length) {
        lines.push(`THE AUTHORED METHOD (use it; do not state the final answer)\n${solution.steps.slice(0, 5).join('\n')}`);
    }
    if (ask) lines.push(`THE LEARNER ASKED: ${clampText(ask, 300)}`);

    return [
        { role: 'system', content: SYSTEM_PROMPT },
        { role: 'system', content: lines.join('\n\n') },
        { role: 'user', content: 'Design the board scene for this question in the plain-text format above.' }
    ];
}

module.exports = {
    BANNED,
    MAX_CODE,
    MAX_CONTROLS,
    MAX_STEPS,
    SYSTEM_PROMPT,
    buildMessages,
    clampText,
    fallbackScene,
    numberPair,
    parseSceneText,
    sanitizeScene
};
