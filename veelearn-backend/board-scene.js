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

const MAX_CODE = 4000;
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

const SYSTEM_PROMPT = `You draw on Veelearn's teaching board while a tutor explains one question. You receive the question card (the correct option is withheld), the skill and the authored method. Make the idea visible and touchable — this is the part a paragraph cannot do.

Reply in EXACTLY this plain-text format — no JSON, no preamble:
TITLE: <a specific title, at most 60 characters>
STEPS:
- <one short step>
- <another step>
CONTROLS:
- a | Shade | 0 | 4 | 0.1 | 1
CODE:
function draw(ctx, W, H, S, t) { ... }
Every header sits on its own line. STEPS and CONTROLS use "- " bullets; CONTROLS lines are key | label | min | max | step | value. CODE is the last section and runs to the end of the reply; do not wrap it in fence markers. Omit PRESET/PARAMS unless you use a preset, and omit the CODE section only when you do use one.

DRAW WITH CODE (preferred):
- "code" is exactly one function: function draw(ctx, W, H, S, t) { ... }
- ctx is a canvas 2D context, W and H are pixels, S holds your slider values by key, t is seconds since the board opened.
- Animate from t only. Draw the actual quantities in THIS question with its numbers and labels.
- Vector shapes only: lines, arcs, rectangles, polygons, text, gradients. No images, no external fonts.
- Label what matters with ctx.fillText (axis names, the value being changed, the point the question asks about).
- Palette: ${PALETTE}. The canvas is white; a pale panel is fine, a full-bleed dark background is not.
- Keep it under 90 lines, compact, with no comments, and never draw a stock parabola unless the question is actually about that parabola.
- Forbidden (the scene will be rejected): document, window, parent, fetch, XMLHttpRequest, WebSocket, eval, new Function, import, localStorage, cookies, location, postMessage, timers, alerts.

OR USE A PRESET:
- Only when the generic engine is genuinely the better drawing, set "preset" to one of: ${prompts.PRESETS.join(', ')} and put numbers in "params". Leave "code" as "".

CONTROLS:
- 1 to 3 sliders at most. Each key is read in draw through S.key and must visibly change something.
- min/max/step/value are numbers; keep the span under 1000.
- Omit controls entirely when a slider would not teach anything.

STEPS:
- 0 to 3 short sentences (<= 140 characters each) that walk the method beside the drawing.
- Plain words, no markdown, never state or hint at the answer.

TITLE: at most 60 characters, specific to this question ("Halving the bar", not "Diagram").`;

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

/**
 * The plain-text scene protocol.
 *
 * Canvas code carries newlines and quotes, which is exactly what a model fails
 * to escape inside a JSON string. Headers plus a CODE section let the code
 * travel verbatim, so the scene is parsed instead of salvaged.
 */
function parseSceneText(text) {
    const src = String(text || '').replace(/\r\n/g, '\n').trim();
    if (!src) return null;
    // Some models answer in JSON anyway; let the caller try that separately.
    if (/^\s*\{/.test(src)) return null;

    const HEADER = /^(TITLE|STEPS|CONTROLS|PRESET|PARAMS|CODE)\s*:\s*(.*)$/i;
    const scene = { title: '', steps: [], controls: [], preset: '', params: {}, code: '' };
    const controlLines = [];
    let paramsRaw = '';
    let mode = null;
    const codeLines = [];

    for (const rawLine of src.split('\n')) {
        const line = rawLine.replace(/\s+$/, '');
        const head = HEADER.exec(line.trim());
        if (head) {
            mode = head[1].toLowerCase();
            const rest = head[2] ? head[2].trim() : '';
            if (mode === 'title') scene.title = rest;
            else if (mode === 'preset') scene.preset = rest;
            else if (mode === 'params') paramsRaw = rest;
            else if (mode === 'code' && rest) codeLines.push(rest);
            continue;
        }
        if (mode === 'steps') {
            const item = line.replace(/^\s*[-*•]\s*/, '').trim();
            if (item) scene.steps.push(item);
        } else if (mode === 'controls') {
            const item = line.replace(/^\s*[-*•]\s*/, '').trim();
            if (item) controlLines.push(item);
        } else if (mode === 'code') {
            if (/^```/.test(line.trim())) continue;
            codeLines.push(line);
        }
    }

    scene.code = codeLines.join('\n').trim();
    scene.params = numberPair(paramsRaw);
    scene.controls = controlLines
        .map((item) => {
            const bits = item.split('|').map((b) => b.trim());
            if (bits.length < 6) return null;
            return {
                key: bits[0],
                label: bits[1],
                min: Number(bits[2]),
                max: Number(bits[3]),
                step: Number(bits[4]),
                value: Number(bits[5])
            };
        })
        .filter(Boolean);

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
