/**
 * Simulator Studio AI Help: OpenRouter-backed Scratch block builder with wait_for_user gates.
 */

const ALLOWED_ACTION_TYPES = new Set([
    'message',
    'select_target',
    'ensure_sprite',
    'add_block',
    'add_stack',
    'draw_asset',
    'wait_for_user',
    'set_sprite_props',
    'done'
]);

const KNOWN_BLOCK_TYPES = new Set([
    'motion_movesteps', 'motion_turnright', 'motion_turnleft', 'motion_goto', 'motion_gotoxy',
    'motion_glideto', 'motion_glidesecstoxy', 'motion_pointindirection', 'motion_pointtowards',
    'motion_changexby', 'motion_setx', 'motion_changeyby', 'motion_sety', 'motion_ifonedgebounce',
    'motion_setrotationstyle', 'motion_xposition', 'motion_yposition', 'motion_direction',
    'looks_sayforsecs', 'looks_say', 'looks_thinkforsecs', 'looks_think', 'looks_switchcostumeto',
    'looks_nextcostume', 'looks_switchbackdropto', 'looks_changesizeby', 'looks_setsizeto',
    'looks_changeeffectby', 'looks_seteffectto', 'looks_cleargraphiceffects', 'looks_show', 'looks_hide',
    'looks_gotofrontback', 'looks_goforwardbackwardlayers', 'looks_costumenumbername', 'looks_size',
    'sound_play', 'sound_playuntildone', 'sound_stopallsounds', 'sound_changevolumeby', 'sound_setvolumeto', 'sound_volume',
    'event_whenflagclicked', 'event_whenkeypressed', 'event_whenthisspriteclicked',
    'event_whenbackdropswitchesto', 'event_whenbroadcastreceived', 'event_broadcast', 'event_broadcastandwait',
    'control_wait', 'control_repeat', 'control_forever', 'control_if', 'control_if_else',
    'control_wait_until', 'control_repeat_until', 'control_stop', 'control_create_clone_of',
    'control_start_as_clone', 'control_delete_this_clone',
    'sensing_touchingobject', 'sensing_touchingcolor', 'sensing_distanceto', 'sensing_askandwait',
    'sensing_answer', 'sensing_keypressed', 'sensing_mousedown', 'sensing_mousex', 'sensing_mousey',
    'sensing_setdragmode', 'sensing_loudness', 'sensing_timer', 'sensing_resettimer',
    'operator_add', 'operator_subtract', 'operator_multiply', 'operator_divide', 'operator_random',
    'operator_lt', 'operator_equals', 'operator_gt', 'operator_and', 'operator_or', 'operator_not',
    'operator_join', 'operator_letter_of', 'operator_length', 'operator_contains', 'operator_mod',
    'operator_round', 'operator_mathop',
    'data_variable', 'data_setvariableto', 'data_changevariableby', 'data_showvariable', 'data_hidevariable',
    'math_number', 'text', 'text_broadcast'
]);

const SIM_SYSTEM = `You are VeeLearn's Scratch Simulator Studio assistant.
You build COMPLETE, RUNNABLE Scratch-style simulations yourself — assets AND blocks. Never ask the user to upload images.

CRITICAL OUTPUT FORMAT:
1) First: ONE short human status line (under 25 words). No JSON on this line. Example: Building a bouncing particle lab…
2) Next line exactly: VEELEARN_SIM_ACTIONS_JSON:
3) Immediately after: a single JSON array of action objects (no markdown fences).
4) After the JSON, optionally one more short line.

ASSET RULES (mandatory):
- NEVER emit wait_for_user for backdrop/costume/sound. Draw everything with draw_asset.
- draw_asset payload: {"kind":"backdrop"|"costume","name":"...","target":"stage"|spriteName,"bg":"#0f172a","replace":true,"shapes":[...]}
- Shape types: rect, roundedRect, circle, sphere, ellipse, trapezoid, triangle, line, polygon, text.
- Shape fields examples:
  {"shape":"rect","x":40,"y":280,"w":400,"h":40,"fill":"#6b4423"}
  {"shape":"sphere","x":64,"y":64,"r":40,"fill":"#22c55e","highlight":"#bbf7d0","shade":"#14532d"}
  {"shape":"ellipse","x":64,"y":70,"rx":28,"ry":40,"fill":"#a78bfa"}
  {"shape":"trapezoid","x":240,"y":200,"wTop":60,"wBottom":120,"h":40,"fill":"#64748b"}
  {"shape":"line","x1":40,"y1":40,"x2":440,"y2":40,"stroke":"#94a3b8","lineWidth":2}
  {"shape":"text","x":20,"y":30,"text":"Lab","fill":"#e2e8f0","font":"bold 18px sans-serif"}
- Backdrop canvas is 480x360. Costume canvas defaults ~128x128 (center at 64,64). Stretch/deform with rx/ry, w/h, rotate.
- First create backdrops and costumes with draw_asset, THEN add scripts.

BLOCK RULES (mandatory — make the ACTUAL working sim):
- Never invent block types. Use real types only.
- Every sprite that should run needs a COMPLETE stack: event_whenflagclicked -> control_forever (or repeat) -> motion/looks/sensing inside SUBSTACK.
- Emit ONE add_block per block. After a hat, next block connectToPrevious:true.
- After control_forever / control_repeat / control_if, the NEXT statement MUST use "into":"SUBSTACK" (or SUBSTACK2 for else).
- Blocks after the first inside a C-block: connectToPrevious:true (no into) so they stack inside the C-block.
- Prefer 12–40 actions for rich sims (multi-sprite). Do not stop after 3 blocks.
- For complex requests (double-slit, many controls): keep EACH draw_asset under 10 shapes and finish a complete JSON array. Prefer two shorter complete replies over one truncated mega-JSON.
- Use ensure_sprite for named roles (Emitter, Particle, Detector, etc.), set_sprite_props for x/y/size, looks_hide on templates used only as clones when needed.
- For physics/graphs: use motion + variables (data_setvariableto / data_changevariableby / data_showvariable) and looks_say for simple readouts if needed.
- End with {"type":"done","payload":{"message":"Press the green flag to try it!"}}.

Example (particle bouncing + lab backdrop):
Building a lab particle bounce…
VEELEARN_SIM_ACTIONS_JSON:
[{"type":"message","payload":{"text":"Building a lab particle bounce…"}},{"type":"draw_asset","payload":{"kind":"backdrop","name":"lab","bg":"#0b1220","shapes":[{"shape":"rect","x":0,"y":300,"w":480,"h":60,"fill":"#334155"},{"shape":"rect","x":60,"y":250,"w":360,"h":20,"fill":"#78716c"},{"shape":"circle","x":80,"y":40,"r":6,"fill":"#f8fafc"},{"shape":"circle","x":140,"y":40,"r":6,"fill":"#f8fafc"},{"shape":"circle","x":200,"y":40,"r":6,"fill":"#f8fafc"}]}},{"type":"ensure_sprite","payload":{"name":"Particle"}},{"type":"draw_asset","payload":{"kind":"costume","name":"dot","target":"Particle","shapes":[{"shape":"sphere","x":64,"y":64,"r":28,"fill":"#38bdf8","highlight":"#e0f2fe","shade":"#075985"}]}},{"type":"set_sprite_props","payload":{"x":-180,"y":0,"size":60}},{"type":"add_block","payload":{"type":"event_whenflagclicked","newStack":true}},{"type":"add_block","payload":{"type":"control_forever","connectToPrevious":true}},{"type":"add_block","payload":{"type":"motion_movesteps","inputs":{"STEPS":8},"connectToPrevious":true,"into":"SUBSTACK"}},{"type":"add_block","payload":{"type":"motion_ifonedgebounce","connectToPrevious":true}},{"type":"done","payload":{"message":"Done — press ▶!"}}]
Done — press ▶!`;

function normalizeShape(s) {
    if (!s || typeof s !== 'object') return null;
    const shape = String(s.shape || s.type || '').toLowerCase().slice(0, 32);
    if (!shape) return null;
    const out = { shape };
    const copyNum = (keys) => {
        for (const k of keys) {
            if (s[k] != null && !Number.isNaN(Number(s[k]))) out[k] = Number(s[k]);
        }
    };
    const copyStr = (keys) => {
        for (const k of keys) {
            if (s[k] != null) out[k] = String(s[k]).slice(0, 80);
        }
    };
    copyNum(['x', 'y', 'w', 'h', 'r', 'rx', 'ry', 'wTop', 'wBottom', 'x1', 'y1', 'x2', 'y2', 'rotate', 'opacity', 'lineWidth', 'width', 'height', 'radius', 'top', 'bottom']);
    copyStr(['fill', 'color', 'stroke', 'bg', 'highlight', 'shade', 'font', 'text']);
    if (Array.isArray(s.points)) {
        out.points = s.points.slice(0, 24).map((p) => {
            if (Array.isArray(p)) return [Number(p[0]) || 0, Number(p[1]) || 0];
            return { x: Number(p.x) || 0, y: Number(p.y) || 0 };
        });
    }
    return out;
}

function repairJsonStringEscapes(input) {
    const s = String(input || '');
    let out = '';
    let inString = false;
    let escaped = false;
    for (let i = 0; i < s.length; i++) {
        const ch = s[i];
        if (!inString) {
            if (ch === '"') inString = true;
            out += ch;
            continue;
        }
        if (escaped) {
            out += ch;
            escaped = false;
            continue;
        }
        if (ch === '\\') {
            const next = s[i + 1];
            if (next == null) {
                out += '\\\\';
                continue;
            }
            if ('"\\/'.includes(next)) {
                out += ch;
                escaped = true;
                continue;
            }
            if (next === 'u' && /^[0-9a-fA-F]{4}/.test(s.slice(i + 2, i + 6))) {
                out += ch;
                escaped = true;
                continue;
            }
            if ('bfnrt'.includes(next)) {
                const after = s[i + 2];
                if (after && /[a-zA-Z]/.test(after)) {
                    out += '\\\\';
                    continue;
                }
                out += ch;
                escaped = true;
                continue;
            }
            out += '\\\\';
            continue;
        }
        if (ch === '"') {
            inString = false;
            out += ch;
            continue;
        }
        out += ch;
    }
    return out;
}

function extractJsonArray(text) {
    const s = String(text || '');
    // Prefer marker, then fenced ```json, then first top-level array that looks like actions
    const marker = 'VEELEARN_SIM_ACTIONS_JSON:';
    let searchFrom = 0;
    const mi = s.indexOf(marker);
    if (mi >= 0) searchFrom = mi + marker.length;

    const fence = s.indexOf('```', searchFrom);
    let slice = s.slice(searchFrom);
    if (fence >= 0 && (mi < 0 || fence > mi)) {
        const afterFence = s.slice(fence + 3).replace(/^json\s*/i, '');
        const endFence = afterFence.indexOf('```');
        if (endFence >= 0) slice = afterFence.slice(0, endFence);
        else slice = afterFence;
    }

    const arrStart = slice.indexOf('[');
    if (arrStart < 0) return { jsonPart: '', reply: s.trim() };

    let depth = 0;
    let inString = false;
    let escaped = false;
    let end = -1;
    for (let i = arrStart; i < slice.length; i++) {
        const c = slice[i];
        if (inString) {
            if (escaped) {
                escaped = false;
            } else if (c === '\\') {
                escaped = true;
            } else if (c === '"') {
                inString = false;
            }
            continue;
        }
        if (c === '"') {
            inString = true;
            continue;
        }
        if (c === '[') depth++;
        else if (c === ']') {
            depth--;
            if (depth === 0) {
                end = i;
                break;
            }
        }
    }

    if (end < 0) {
        return { jsonPart: slice.slice(arrStart), reply: '' };
    }
    const jsonPart = slice.slice(arrStart, end + 1);
    // Reply = text before marker/array + text after array (excluding fences)
    let reply = '';
    if (mi >= 0) {
        reply = (s.slice(0, mi) + ' ' + slice.slice(end + 1)).replace(/```/g, '').trim();
    } else {
        reply = (s.slice(0, searchFrom + arrStart) + ' ' + slice.slice(end + 1)).replace(/```/g, '').trim();
        // If reply still looks like JSON, drop it
        if (/^\s*[\[{]/.test(reply)) reply = '';
    }
    return { jsonPart, reply };
}

function extractActionsAndReply(raw) {
    const text = String(raw || '');
    const { jsonPart, reply } = extractJsonArray(text);

    let actions = [];
    if (jsonPart) {
        try {
            actions = JSON.parse(repairJsonStringEscapes(jsonPart));
        } catch (e) {
            actions = salvageCompleteActionObjects(jsonPart);
            if (actions.length) {
                console.warn(
                    `[sim-ai] salvaged ${actions.length} complete action(s) from truncated JSON`
                );
            }
        }
    }
    if (!Array.isArray(actions)) actions = [];
    // Filter noise: only objects with type
    actions = actions.filter((a) => a && typeof a === 'object' && a.type);
    return { actions, reply: String(reply || '').slice(0, 2000), truncated: !!(jsonPart && !String(jsonPart).trim().endsWith(']')) };
}

/**
 * Recover complete top-level action objects from a truncated JSON array.
 * Unlike slicing at the last "}," this respects nested shapes arrays.
 */
function salvageCompleteActionObjects(jsonPart) {
    const repaired = repairJsonStringEscapes(String(jsonPart || ''));
    try {
        const parsed = JSON.parse(repaired);
        if (Array.isArray(parsed)) return parsed;
    } catch (_) { /* fall through */ }

    const s = repaired.trim();
    const start = s.indexOf('[');
    if (start < 0) return [];

    const objects = [];
    let i = start + 1;
    while (i < s.length) {
        while (i < s.length && /[\s,]/.test(s[i])) i++;
        if (i >= s.length || s[i] === ']') break;
        if (s[i] !== '{') break;

        let depth = 0;
        let inString = false;
        let escaped = false;
        const objStart = i;
        let objEnd = -1;
        for (; i < s.length; i++) {
            const c = s[i];
            if (inString) {
                if (escaped) escaped = false;
                else if (c === '\\') escaped = true;
                else if (c === '"') inString = false;
                continue;
            }
            if (c === '"') {
                inString = true;
                continue;
            }
            if (c === '{') depth++;
            else if (c === '}') {
                depth--;
                if (depth === 0) {
                    objEnd = i;
                    i++;
                    break;
                }
            }
        }
        if (objEnd < 0) break;
        const chunk = s.slice(objStart, objEnd + 1);
        try {
            objects.push(JSON.parse(chunk));
        } catch (_) {
            try {
                objects.push(JSON.parse(repairJsonStringEscapes(chunk)));
            } catch (__) { /* skip broken object */ }
        }
    }
    return objects;
}

function isComplexSimRequest(message) {
    const m = String(message || '');
    if (m.length > 900) return true;
    const hits = [
        /double[\s-]?slit/i,
        /interference/i,
        /wave[\s-]?function/i,
        /wavelength/i,
        /particle\s+vs\.?\s+wave/i,
        /detector\s+screen/i,
        /interactive\s+controls/i,
        /slider/i,
        /clone/i,
        /intensity\s+graph/i
    ].filter((re) => re.test(m));
    return hits.length >= 2;
}

function isDoubleSlitRequest(message) {
    return /double[\s-]?slit|young'?s\s+experiment|interference\s+fringe/i.test(String(message || ''));
}

/** Guaranteed runnable starter when the model returns prose only. */
function fallbackBounceActions(userMessage) {
    const topic = String(userMessage || 'simulation').slice(0, 80);
    return [
        { type: 'message', payload: { text: `Building a working starter for “${topic}” (model skipped actions — using fallback).` } },
        {
            type: 'draw_asset',
            payload: {
                kind: 'backdrop',
                name: 'lab',
                bg: '#0b1220',
                replace: true,
                shapes: [
                    { shape: 'rect', x: 0, y: 0, w: 480, h: 360, fill: '#0b1220' },
                    { shape: 'rect', x: 30, y: 290, w: 420, h: 40, fill: '#57534e' },
                    { shape: 'rect', x: 220, y: 80, w: 18, h: 160, fill: '#94a3b8' },
                    { shape: 'rect', x: 218, y: 120, w: 22, h: 28, fill: '#0b1220' },
                    { shape: 'rect', x: 218, y: 180, w: 22, h: 28, fill: '#0b1220' },
                    { shape: 'rect', x: 420, y: 60, w: 12, h: 220, fill: '#e2e8f0' },
                    { shape: 'circle', x: 80, y: 40, r: 5, fill: '#f8fafc' },
                    { shape: 'circle', x: 120, y: 40, r: 5, fill: '#f8fafc' },
                    { shape: 'circle', x: 160, y: 40, r: 5, fill: '#f8fafc' }
                ]
            }
        },
        { type: 'ensure_sprite', payload: { name: 'Emitter' } },
        {
            type: 'draw_asset',
            payload: {
                kind: 'costume',
                name: 'emitter',
                target: 'Emitter',
                replace: true,
                shapes: [{ shape: 'trapezoid', x: 64, y: 40, wTop: 20, wBottom: 70, h: 50, fill: '#f59e0b' }]
            }
        },
        { type: 'set_sprite_props', payload: { x: -180, y: 0, size: 70 } },
        { type: 'ensure_sprite', payload: { name: 'Particle' } },
        {
            type: 'draw_asset',
            payload: {
                kind: 'costume',
                name: 'particle',
                target: 'Particle',
                replace: true,
                shapes: [{ shape: 'sphere', x: 64, y: 64, r: 22, fill: '#38bdf8', highlight: '#e0f2fe', shade: '#075985' }]
            }
        },
        { type: 'set_sprite_props', payload: { x: -140, y: 0, size: 45 } },
        { type: 'select_target', payload: { target: 'Particle' } },
        { type: 'add_block', payload: { type: 'event_whenflagclicked', newStack: true } },
        { type: 'add_block', payload: { type: 'motion_gotoxy', inputs: { X: -140, Y: 0 }, connectToPrevious: true } },
        { type: 'add_block', payload: { type: 'motion_pointindirection', inputs: { DIRECTION: 90 }, connectToPrevious: true } },
        { type: 'add_block', payload: { type: 'control_forever', connectToPrevious: true } },
        { type: 'add_block', payload: { type: 'motion_movesteps', inputs: { STEPS: 8 }, connectToPrevious: true, into: 'SUBSTACK' } },
        { type: 'add_block', payload: { type: 'motion_ifonedgebounce', connectToPrevious: true } },
        { type: 'add_block', payload: { type: 'control_wait', inputs: { DURATION: 0.05 }, connectToPrevious: true } },
        {
            type: 'done',
            payload: {
                message: 'Starter placed (Emitter + Particle bounce). Press ▶ — then ask me to expand the full double-slit logic.'
            }
        }
    ];
}

/**
 * Richer double-slit starter used when the model truncates / fails on that topic.
 * Approximates interference with dual slit paths + detector hits (Scratch-friendly).
 */
function fallbackDoubleSlitActions() {
    return [
        {
            type: 'message',
            payload: {
                text: 'Building a double-slit lab: barrier, two slits, emitter clones, detector hits, and mode variables.'
            }
        },
        {
            type: 'draw_asset',
            payload: {
                kind: 'backdrop',
                name: 'double_slit_lab',
                bg: '#020617',
                replace: true,
                shapes: [
                    { shape: 'rect', x: 0, y: 0, w: 480, h: 360, fill: '#020617' },
                    { shape: 'rect', x: 0, y: 320, w: 480, h: 40, fill: '#1e293b' },
                    { shape: 'rect', x: 210, y: 20, w: 18, h: 320, fill: '#64748b' },
                    { shape: 'rect', x: 210, y: 110, w: 18, h: 28, fill: '#020617' },
                    { shape: 'rect', x: 210, y: 210, w: 18, h: 28, fill: '#020617' },
                    { shape: 'rect', x: 450, y: 20, w: 14, h: 300, fill: '#0f172a' },
                    { shape: 'rect', x: 452, y: 20, w: 10, h: 300, fill: '#111827' },
                    { shape: 'text', x: 12, y: 24, text: 'Double-Slit Lab', fill: '#e2e8f0', font: 'bold 14px sans-serif' },
                    { shape: 'text', x: 12, y: 44, text: 'mode · wavelength · observe · rate', fill: '#94a3b8', font: '11px sans-serif' },
                    { shape: 'circle', x: 40, y: 60, r: 2, fill: '#f8fafc' },
                    { shape: 'circle', x: 70, y: 55, r: 2, fill: '#f8fafc' },
                    { shape: 'circle', x: 100, y: 62, r: 2, fill: '#f8fafc' }
                ]
            }
        },
        { type: 'ensure_sprite', payload: { name: 'Emitter' } },
        {
            type: 'draw_asset',
            payload: {
                kind: 'costume',
                name: 'emitter',
                target: 'Emitter',
                replace: true,
                shapes: [{ shape: 'trapezoid', x: 64, y: 48, wTop: 18, wBottom: 64, h: 44, fill: '#f59e0b' }]
            }
        },
        { type: 'set_sprite_props', payload: { name: 'Emitter', x: -200, y: 0, size: 80 } },
        { type: 'ensure_sprite', payload: { name: 'Photon' } },
        {
            type: 'draw_asset',
            payload: {
                kind: 'costume',
                name: 'photon',
                target: 'Photon',
                replace: true,
                shapes: [
                    { shape: 'sphere', x: 64, y: 64, r: 18, fill: '#22d3ee', highlight: '#ecfeff', shade: '#0e7490' }
                ]
            }
        },
        { type: 'set_sprite_props', payload: { name: 'Photon', x: -160, y: 0, size: 35, visible: false } },
        { type: 'ensure_sprite', payload: { name: 'Hit' } },
        {
            type: 'draw_asset',
            payload: {
                kind: 'costume',
                name: 'hit',
                target: 'Hit',
                replace: true,
                shapes: [{ shape: 'circle', x: 64, y: 64, r: 6, fill: '#a78bfa' }]
            }
        },
        { type: 'set_sprite_props', payload: { name: 'Hit', x: 200, y: 0, size: 20, visible: false } },
        { type: 'ensure_sprite', payload: { name: 'UI' } },
        {
            type: 'draw_asset',
            payload: {
                kind: 'costume',
                name: 'ui_panel',
                target: 'UI',
                replace: true,
                shapes: [
                    { shape: 'rect', x: 8, y: 8, w: 112, h: 100, fill: '#1e293b' },
                    { shape: 'text', x: 16, y: 28, text: 'Click: toggle', fill: '#e2e8f0', font: 'bold 12px sans-serif' },
                    { shape: 'text', x: 16, y: 48, text: 'observe ON/OFF', fill: '#94a3b8', font: '11px sans-serif' },
                    { shape: 'text', x: 16, y: 68, text: '(wave collapse)', fill: '#38bdf8', font: '11px sans-serif' }
                ]
            }
        },
        { type: 'set_sprite_props', payload: { name: 'UI', x: -180, y: 120, size: 90 } },

        // Emitter: init vars + spawn Photon clones
        { type: 'select_target', payload: { target: 'Emitter' } },
        { type: 'add_block', payload: { type: 'event_whenflagclicked', newStack: true } },
        {
            type: 'add_block',
            payload: {
                type: 'data_setvariableto',
                fields: { VARIABLE: 'mode' },
                inputs: { VALUE: 'particle' },
                connectToPrevious: true
            }
        },
        {
            type: 'add_block',
            payload: {
                type: 'data_setvariableto',
                fields: { VARIABLE: 'wavelength' },
                inputs: { VALUE: 550 },
                connectToPrevious: true
            }
        },
        {
            type: 'add_block',
            payload: {
                type: 'data_setvariableto',
                fields: { VARIABLE: 'slitGap' },
                inputs: { VALUE: 40 },
                connectToPrevious: true
            }
        },
        {
            type: 'add_block',
            payload: {
                type: 'data_setvariableto',
                fields: { VARIABLE: 'observe' },
                inputs: { VALUE: 0 },
                connectToPrevious: true
            }
        },
        {
            type: 'add_block',
            payload: {
                type: 'data_setvariableto',
                fields: { VARIABLE: 'rate' },
                inputs: { VALUE: 4 },
                connectToPrevious: true
            }
        },
        { type: 'add_block', payload: { type: 'data_showvariable', fields: { VARIABLE: 'mode' }, connectToPrevious: true } },
        { type: 'add_block', payload: { type: 'data_showvariable', fields: { VARIABLE: 'wavelength' }, connectToPrevious: true } },
        { type: 'add_block', payload: { type: 'data_showvariable', fields: { VARIABLE: 'observe' }, connectToPrevious: true } },
        { type: 'add_block', payload: { type: 'data_showvariable', fields: { VARIABLE: 'rate' }, connectToPrevious: true } },
        { type: 'add_block', payload: { type: 'control_forever', connectToPrevious: true } },
        {
            type: 'add_block',
            payload: {
                type: 'control_create_clone_of',
                fields: { CLONE_OPTION: 'Photon' },
                connectToPrevious: true,
                into: 'SUBSTACK'
            }
        },
        { type: 'add_block', payload: { type: 'control_wait', inputs: { DURATION: 0.2 }, connectToPrevious: true } },

        // Photon clone: go through upper/lower slit toward detector, stamp Hit, delete
        { type: 'select_target', payload: { target: 'Photon' } },
        { type: 'add_block', payload: { type: 'control_start_as_clone', newStack: true } },
        { type: 'add_block', payload: { type: 'looks_show', connectToPrevious: true } },
        { type: 'add_block', payload: { type: 'motion_gotoxy', inputs: { X: -160, Y: 0 }, connectToPrevious: true } },
        {
            type: 'add_block',
            payload: {
                type: 'data_setvariableto',
                fields: { VARIABLE: 'pathY' },
                inputs: { VALUE: 40 },
                connectToPrevious: true
            }
        },
        { type: 'add_block', payload: { type: 'motion_gotoxy', inputs: { X: -40, Y: 40 }, connectToPrevious: true } },
        { type: 'add_block', payload: { type: 'control_repeat', inputs: { TIMES: 28 }, connectToPrevious: true } },
        {
            type: 'add_block',
            payload: {
                type: 'motion_changexby',
                inputs: { DX: 8 },
                connectToPrevious: true,
                into: 'SUBSTACK'
            }
        },
        { type: 'add_block', payload: { type: 'control_wait', inputs: { DURATION: 0.03 }, connectToPrevious: true } },
        { type: 'add_block', payload: { type: 'motion_gotoxy', inputs: { X: 200, Y: 40 }, connectToPrevious: true } },
        {
            type: 'add_block',
            payload: {
                type: 'control_create_clone_of',
                fields: { CLONE_OPTION: 'Hit' },
                connectToPrevious: true
            }
        },
        { type: 'add_block', payload: { type: 'control_delete_this_clone', connectToPrevious: true } },

        // Hit clone: appear at detector and stay
        { type: 'select_target', payload: { target: 'Hit' } },
        { type: 'add_block', payload: { type: 'control_start_as_clone', newStack: true } },
        { type: 'add_block', payload: { type: 'looks_show', connectToPrevious: true } },
        { type: 'add_block', payload: { type: 'motion_gotoxy', inputs: { X: 200, Y: 40 }, connectToPrevious: true } },
        { type: 'add_block', payload: { type: 'looks_setsizeto', inputs: { SIZE: 40 }, connectToPrevious: true } },

        // UI click toggles observe 0/1
        { type: 'select_target', payload: { target: 'UI' } },
        { type: 'add_block', payload: { type: 'event_whenthisspriteclicked', newStack: true } },
        {
            type: 'add_block',
            payload: {
                type: 'data_changevariableby',
                fields: { VARIABLE: 'observe' },
                inputs: { VALUE: 1 },
                connectToPrevious: true
            }
        },
        {
            type: 'add_block',
            payload: {
                type: 'looks_sayforsecs',
                inputs: { MESSAGE: 'observe toggled (collapse toward single band)', SECS: 2 },
                connectToPrevious: true
            }
        },

        {
            type: 'done',
            payload: {
                message:
                    'Double-slit lab placed: slits, emitter clones, detector hits, and observe toggle. Press ▶ — then ask to add wave mode, wavelength color, or a live intensity graph.'
            }
        }
    ];
}

function pickFallbackActions(message) {
    if (isDoubleSlitRequest(message)) return fallbackDoubleSlitActions();
    return fallbackBounceActions(message || 'simulation');
}

function normalizeInputs(inputs) {
    if (!inputs || typeof inputs !== 'object') return {};
    const out = {};
    for (const [k, v] of Object.entries(inputs)) {
        if (v == null) continue;
        if (typeof v === 'number' || typeof v === 'string' || typeof v === 'boolean') {
            out[String(k).slice(0, 64)] = v;
        }
    }
    return out;
}

function normalizeFields(fields) {
    if (!fields || typeof fields !== 'object') return {};
    const out = {};
    for (const [k, v] of Object.entries(fields)) {
        if (v == null) continue;
        out[String(k).slice(0, 64)] = String(v).slice(0, 500);
    }
    return out;
}

function validateActions(rawActions) {
    const out = [];
    for (const a of rawActions) {
        if (!a || typeof a !== 'object') continue;
        const type = String(a.type || '').trim();
        if (!ALLOWED_ACTION_TYPES.has(type)) continue;
        const payload = a.payload && typeof a.payload === 'object' ? a.payload : {};

        if (type === 'message') {
            const text = String(payload.text || payload.message || '').slice(0, 1000).trim();
            if (!text) continue;
            out.push({ type, payload: { text } });
        } else if (type === 'select_target') {
            const target = String(payload.target || payload.id || payload.name || 'Sprite1').slice(0, 120);
            out.push({ type, payload: { target } });
        } else if (type === 'ensure_sprite') {
            out.push({
                type,
                payload: { name: String(payload.name || 'Sprite').slice(0, 80) }
            });
        } else if (type === 'add_block') {
            const blockType = String(payload.type || payload.blockType || '').trim();
            if (!KNOWN_BLOCK_TYPES.has(blockType)) continue;
            out.push({
                type,
                payload: {
                    type: blockType,
                    inputs: normalizeInputs(payload.inputs),
                    fields: normalizeFields(payload.fields),
                    connectToPrevious: payload.connectToPrevious !== false,
                    newStack: !!payload.newStack,
                    into: payload.into ? String(payload.into).slice(0, 64) : null,
                    x: typeof payload.x === 'number' ? payload.x : undefined,
                    y: typeof payload.y === 'number' ? payload.y : undefined
                }
            });
        } else if (type === 'add_stack') {
            const blocks = Array.isArray(payload.blocks) ? payload.blocks.slice(0, 40) : [];
            const normalized = [];
            for (const b of blocks) {
                const bt = String(b.type || b.blockType || '').trim();
                if (!KNOWN_BLOCK_TYPES.has(bt)) continue;
                normalized.push({
                    type: bt,
                    inputs: normalizeInputs(b.inputs),
                    fields: normalizeFields(b.fields),
                    connectToPrevious: b.connectToPrevious !== false,
                    newStack: !!b.newStack,
                    into: b.into ? String(b.into).slice(0, 64) : null
                });
            }
            if (!normalized.length) continue;
            out.push({ type, payload: { blocks: normalized } });
        } else if (type === 'draw_asset') {
            const kindRaw = String(payload.kind || 'costume').toLowerCase();
            const kind = kindRaw === 'backdrop' || kindRaw === 'background' ? 'backdrop' : 'costume';
            const shapes = Array.isArray(payload.shapes)
                ? payload.shapes.map(normalizeShape).filter(Boolean).slice(0, 80)
                : [];
            if (!shapes.length) continue;
            out.push({
                type,
                payload: {
                    kind,
                    name: String(payload.name || kind).slice(0, 80),
                    target: payload.target ? String(payload.target).slice(0, 120) : kind === 'backdrop' ? 'stage' : undefined,
                    bg: payload.bg ? String(payload.bg).slice(0, 40) : undefined,
                    width: typeof payload.width === 'number' ? payload.width : undefined,
                    height: typeof payload.height === 'number' ? payload.height : undefined,
                    replace: payload.replace !== false,
                    shapes
                }
            });
        } else if (type === 'wait_for_user') {
            // Convert legacy wait_for_user asset requests into procedural draw_asset
            let need = String(payload.need || '').toLowerCase();
            if (need === 'sound') {
                // No procedural audio — skip silently (AI should not wait)
                continue;
            }
            if (need !== 'backdrop') need = 'costume';
            const isBackdrop = need === 'backdrop';
            const shapes = isBackdrop
                ? [
                      { shape: 'rect', x: 0, y: 0, w: 480, h: 360, fill: '#0f172a' },
                      { shape: 'rect', x: 40, y: 280, w: 400, h: 50, fill: '#57534e' },
                      { shape: 'circle', x: 100, y: 50, r: 5, fill: '#f8fafc' },
                      { shape: 'circle', x: 160, y: 50, r: 5, fill: '#f8fafc' },
                      { shape: 'circle', x: 220, y: 50, r: 5, fill: '#f8fafc' },
                      { shape: 'circle', x: 280, y: 50, r: 5, fill: '#f8fafc' }
                  ]
                : [
                      { shape: 'sphere', x: 64, y: 64, r: 36, fill: '#38bdf8', highlight: '#e0f2fe', shade: '#0c4a6e' }
                  ];
            out.push({
                type: 'draw_asset',
                payload: {
                    kind: isBackdrop ? 'backdrop' : 'costume',
                    name: isBackdrop ? 'auto-lab' : 'auto-sprite',
                    target: isBackdrop ? 'stage' : undefined,
                    bg: isBackdrop ? '#0f172a' : undefined,
                    replace: true,
                    shapes
                }
            });
        } else if (type === 'set_sprite_props') {
            const props = {};
            if (typeof payload.x === 'number') props.x = payload.x;
            if (typeof payload.y === 'number') props.y = payload.y;
            if (typeof payload.size === 'number') props.size = payload.size;
            if (typeof payload.direction === 'number') props.direction = payload.direction;
            if (typeof payload.visible === 'boolean') props.visible = payload.visible;
            if (payload.name) props.name = String(payload.name).slice(0, 80);
            out.push({ type, payload: props });
        } else if (type === 'done') {
            out.push({
                type,
                payload: { message: String(payload.message || 'Done!').slice(0, 300) }
            });
        }

        if (out.length >= 140) break;
    }
    return out;
}

function buildMessages(reqBody, phaseInfo) {
    const message = String(reqBody?.message || '').trim().slice(0, 8000);
    const isContinue = !!reqBody?.continue;
    const lastNeed = String(reqBody?.lastNeed || '').slice(0, 40);
    const projectSummary = String(reqBody?.projectSummary || '').slice(0, 4000);
    const history = Array.isArray(reqBody?.history) ? reqBody.history.slice(-12) : [];
    const complex = isComplexSimRequest(message) || isDoubleSlitRequest(message);
    const phase = phaseInfo?.phase || 1;
    const totalPhases = phaseInfo?.totalPhases || (complex ? 2 : 1);

    let phaseHint = '';
    if (complex && totalPhases > 1) {
        if (phase === 1) {
            phaseHint = [
                `\nPHASE ${phase}/${totalPhases} — SCENE + SPRITES ONLY (compact).`,
                'Emit at most 28 actions. Prefer 4–8 shapes per draw_asset (not dozens).',
                'Include: backdrop with barrier+2 slits+detector, Emitter + Photon + Hit sprites/costumes, set_sprite_props, variables via data_setvariableto (mode, wavelength, observe, rate), Emitter forever create_clone_of Photon.',
                'End with done. Photon clone path scripts come in the next phase.'
            ].join('\n');
        } else {
            phaseHint = [
                `\nPHASE ${phase}/${totalPhases} — SCRIPTS + CONTROLS ONLY.`,
                'Do NOT redraw the whole backdrop unless needed. Prefer add_block / ensure_sprite / set_sprite_props.',
                'Add Photon when-I-start-as-a-clone stacks (upper+lower slit paths), Hit clones on detector, UI click toggles for observe/mode.',
                'Use clones. Keep JSON compact. End with done.'
            ].join('\n');
        }
    }

    const userContent = [
        isContinue
            ? `CONTINUE after the user completed: ${lastNeed || 'previous build'}. Finish remaining setup for the original request. Prefer scripts/controls if the scene already exists.`
            : `User request: ${message}`,
        projectSummary ? `\nCurrent project summary:\n${projectSummary}` : '',
        phaseHint,
        '\nStart with a short human status line, then VEELEARN_SIM_ACTIONS_JSON: then actions.',
        complex
            ? '\nIMPORTANT: Keep each draw_asset under 10 shapes. Prefer many small actions over one huge truncated JSON.'
            : ''
    ].join('');

    const messages = [
        { role: 'system', content: SIM_SYSTEM },
        ...history
            .filter((h) => h && (h.role === 'user' || h.role === 'assistant') && h.content)
            .map((h) => ({
                role: h.role,
                content: String(h.content).slice(0, 4000)
            })),
        { role: 'user', content: userContent }
    ];

    return { message, isContinue, messages, complex, phase, totalPhases };
}

function countBlockActions(actions) {
    return (actions || []).filter((a) => a && (a.type === 'add_block' || a.type === 'add_stack')).length;
}

function finalizeSimResult(raw, message, opts) {
    const options = opts || {};
    let parsed = extractActionsAndReply(raw);
    let actions = validateActions(parsed.actions);
    let reply = parsed.reply;
    let usedFallback = false;
    let salvaged = !!parsed.truncated && actions.length > 0;

    if (!actions.length) {
        usedFallback = true;
        actions = validateActions(pickFallbackActions(message || 'simulation'));
        reply =
            reply ||
            (isDoubleSlitRequest(message)
                ? 'The model response was truncated, so I placed a fuller double-slit lab starter you can expand.'
                : 'The model did not return build actions, so I placed a working starter simulation you can expand.');
    }

    if (!reply) {
        reply = usedFallback
            ? 'Starter simulation placed. Press ▶ to run.'
            : salvaged
              ? `Recovered ${actions.length} actions from a truncated model reply — applying what we got.`
              : `Placing ${actions.length} studio actions…`;
    }

    const needsContinue =
        options.needsContinue === true ||
        (options.complex && !usedFallback && countBlockActions(actions) < 8) ||
        (salvaged && countBlockActions(actions) < 6);

    return {
        reply,
        actions,
        actionCount: actions.length,
        usedFallback,
        salvaged,
        needsContinue: !!needsContinue,
        rawPreview: String(raw || '').slice(0, 1200)
    };
}

function openRouterErrorResponse(apiResponse, res, e) {
    console.error('ai simulator help openrouter:', e.message);
    if (e.code === 'OPENROUTER_NOT_CONFIGURED') {
        return apiResponse(res, 503, 'AI is not configured (missing OpenRouter keys).');
    }
    if (e.code === 'OPENROUTER_RATE_LIMITED' || e.status === 429) {
        return apiResponse(
            res,
            429,
            'AI is temporarily rate-limited. Please wait about a minute and try again.'
        );
    }
    return apiResponse(res, 502, e.message || 'AI service failed');
}

function sseWrite(res, event, data) {
    if (res.writableEnded) return;
    res.write(`event: ${event}\ndata: ${JSON.stringify(data)}\n\n`);
    if (typeof res.flush === 'function') {
        try {
            res.flush();
        } catch (_) { /* ignore */ }
    }
}

module.exports = function createAiSimulatorHelpHandlers({
    openRouterChatCompletion,
    openRouterChatCompletionStream,
    apiResponse,
    getOpenRouterKeys
}) {
    return {
        async help(req, res) {
            const userId = req.user?.id;
            if (!userId) return apiResponse(res, 401, 'Authentication required');

            const keys = typeof getOpenRouterKeys === 'function' ? getOpenRouterKeys() : [];
            if (!keys.length) {
                return apiResponse(res, 503, 'AI is not configured (missing OpenRouter keys).');
            }

            const { message, isContinue, messages, complex } = buildMessages(req.body, {
                phase: 1,
                totalPhases: 1
            });
            if (!message && !isContinue) {
                return apiResponse(res, 400, 'Message required');
            }

            let raw = '';
            try {
                raw = await openRouterChatCompletion(messages, {
                    temperature: 0.25,
                    max_tokens: complex ? 7000 : 5000,
                    budgetMs: 40000,
                    timeoutMs: 45000
                });
            } catch (e) {
                return openRouterErrorResponse(apiResponse, res, e);
            }

            let actions = validateActions(extractActionsAndReply(raw).actions);

            if (!actions.length) {
                console.warn('[sim-ai] zero actions on first pass; short retry. preview:', String(raw).slice(0, 240));
                try {
                    raw = await openRouterChatCompletion(
                        [
                            { role: 'system', content: SIM_SYSTEM },
                            {
                                role: 'user',
                                content: [
                                    'CRITICAL RETRY: Your previous reply had NO executable actions (or only truncated JSON).',
                                    'Start with one short status line, then:',
                                    'VEELEARN_SIM_ACTIONS_JSON:',
                                    'Keep under 25 compact actions. Max 8 shapes per draw_asset.',
                                    `User request: ${message || 'continue'}`
                                ].join('\n')
                            }
                        ],
                        { temperature: 0.1, max_tokens: 5000, budgetMs: 28000, timeoutMs: 30000 }
                    );
                } catch (retryErr) {
                    console.warn('[sim-ai] retry failed:', retryErr.message);
                }
            }

            return apiResponse(res, 200, 'OK', finalizeSimResult(raw, message, { complex }));
        },

        async helpStream(req, res) {
            const userId = req.user?.id;
            if (!userId) {
                return apiResponse(res, 401, 'Authentication required');
            }

            const keys = typeof getOpenRouterKeys === 'function' ? getOpenRouterKeys() : [];
            if (!keys.length) {
                return apiResponse(res, 503, 'AI is not configured (missing OpenRouter keys).');
            }

            const streamFn =
                typeof openRouterChatCompletionStream === 'function'
                    ? openRouterChatCompletionStream
                    : null;
            if (!streamFn) {
                return apiResponse(res, 501, 'Streaming not available on this server build.');
            }

            const first = buildMessages(req.body, { phase: 1, totalPhases: 1 });
            const { message, isContinue, complex } = first;
            if (!message && !isContinue) {
                return apiResponse(res, 400, 'Message required');
            }

            const totalPhases = complex && !isContinue ? 2 : 1;

            res.status(200);
            res.setHeader('Content-Type', 'text/event-stream; charset=utf-8');
            res.setHeader('Cache-Control', 'no-cache, no-transform');
            res.setHeader('Connection', 'keep-alive');
            res.setHeader('X-Accel-Buffering', 'no');
            if (typeof res.flushHeaders === 'function') res.flushHeaders();

            const keepAlive = setInterval(() => {
                if (res.writableEnded) return;
                try {
                    res.write(': keepalive\n\n');
                    if (typeof res.flush === 'function') res.flush();
                } catch (_) { /* ignore */ }
            }, 8000);

            const cleanup = () => {
                clearInterval(keepAlive);
            };

            req.on('close', cleanup);

            const streamOnce = async (messages, phaseLabel) => {
                sseWrite(res, 'status', { phase: phaseLabel });
                let suppressJson = false;
                let lineBuf = '';
                let rawOut = '';

                rawOut = await streamFn(messages, {
                    temperature: 0.25,
                    max_tokens: 7500,
                    budgetMs: 95000,
                    timeoutMs: 95000,
                    onDelta: (delta) => {
                        if (suppressJson) return;
                        lineBuf += delta;
                        const marker = 'VEELEARN_SIM_ACTIONS_JSON:';
                        const mi = lineBuf.indexOf(marker);
                        if (mi >= 0) {
                            const before = lineBuf.slice(0, mi);
                            if (before) sseWrite(res, 'token', { text: before });
                            suppressJson = true;
                            lineBuf = '';
                            return;
                        }
                        if (lineBuf.length > 48 && !marker.startsWith(lineBuf.trim().slice(0, 12))) {
                            const flushLen = Math.max(0, lineBuf.length - 40);
                            if (flushLen > 0) {
                                sseWrite(res, 'token', { text: lineBuf.slice(0, flushLen) });
                                lineBuf = lineBuf.slice(flushLen);
                            }
                        }
                    }
                });

                if (!suppressJson && lineBuf) {
                    sseWrite(res, 'token', { text: lineBuf });
                }
                return rawOut;
            };

            try {
                let mergedActions = [];
                let lastReply = '';
                let rawCombined = '';
                let usedFallback = false;
                let salvaged = false;

                for (let phase = 1; phase <= totalPhases; phase++) {
                    const built = buildMessages(req.body, { phase, totalPhases });
                    // Tell phase 2 what phase 1 already emitted
                    if (phase > 1 && mergedActions.length) {
                        const summary = mergedActions
                            .slice(0, 40)
                            .map((a) => a.type + (a.payload?.name ? `:${a.payload.name}` : a.payload?.type ? `:${a.payload.type}` : ''))
                            .join(', ');
                        built.messages.push({
                            role: 'user',
                            content: `Already applied in earlier phase (do not redo assets unless broken): ${summary}`
                        });
                    }

                    const raw = await streamOnce(built.messages, `generating-${phase}/${totalPhases}`);
                    rawCombined += (rawCombined ? '\n---\n' : '') + raw;
                    const parsed = extractActionsAndReply(raw);
                    const phaseActions = validateActions(parsed.actions);
                    if (parsed.reply) lastReply = parsed.reply;
                    if (parsed.truncated && phaseActions.length) salvaged = true;

                    if (!phaseActions.length) {
                        console.warn(
                            `[sim-ai stream] phase ${phase} zero actions. preview:`,
                            String(raw).slice(0, 240)
                        );
                        // Only fall back if phase 1 produced nothing
                        if (phase === 1 && !mergedActions.length) {
                            usedFallback = true;
                            mergedActions = validateActions(pickFallbackActions(message || 'simulation'));
                            lastReply =
                                lastReply ||
                                (isDoubleSlitRequest(message)
                                    ? 'Model JSON was truncated — placed a fuller double-slit lab. Press ▶, then Continue to refine.'
                                    : 'Model returned no actions — placed a starter. Press ▶, then Continue to expand.');
                            break;
                        }
                    } else {
                        mergedActions = mergedActions.concat(phaseActions);
                        if (mergedActions.length > 140) {
                            mergedActions = mergedActions.slice(0, 140);
                        }
                    }

                    // If phase 1 already has rich scripts, skip phase 2
                    if (phase === 1 && totalPhases > 1 && countBlockActions(phaseActions) >= 12) {
                        break;
                    }
                }

                if (!mergedActions.length) {
                    usedFallback = true;
                    mergedActions = validateActions(pickFallbackActions(message || 'simulation'));
                }

                if (!lastReply) {
                    lastReply = usedFallback
                        ? 'Starter simulation placed. Press ▶ to run.'
                        : salvaged
                          ? `Recovered and applied ${mergedActions.length} actions (model output was truncated).`
                          : `Placing ${mergedActions.length} studio actions…`;
                }

                const needsContinue =
                    !usedFallback &&
                    (salvaged || (complex && countBlockActions(mergedActions) < 10));

                sseWrite(res, 'result', {
                    reply: lastReply,
                    actions: mergedActions,
                    actionCount: mergedActions.length,
                    usedFallback,
                    salvaged,
                    needsContinue,
                    rawPreview: String(rawCombined).slice(0, 1200)
                });
            } catch (e) {
                console.error('ai simulator help stream:', e.message);
                const code =
                    e.code === 'OPENROUTER_NOT_CONFIGURED'
                        ? 503
                        : e.code === 'OPENROUTER_RATE_LIMITED' || e.status === 429
                          ? 429
                          : 502;
                sseWrite(res, 'error', {
                    status: code,
                    message:
                        code === 429
                            ? 'AI is temporarily rate-limited. Please wait about a minute and try again.'
                            : e.message || 'AI service failed'
                });
            } finally {
                cleanup();
                if (!res.writableEnded) res.end();
            }
        }
    };
};
