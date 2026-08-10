/**
 * Simulator Studio AI Help: OpenRouter-backed Scratch block builder with wait_for_user gates.
 */

const ALLOWED_ACTION_TYPES = new Set([
    'message',
    'select_target',
    'ensure_sprite',
    'add_block',
    'add_stack',
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
You build working Scratch-style simulations by emitting structured actions the studio executes one-by-one.

CRITICAL OUTPUT FORMAT:
1) First line exactly: VEELEARN_SIM_ACTIONS_JSON:
2) Immediately after: a single JSON array of action objects (no markdown fences).
3) After the JSON, optionally a short human reply (under 40 words).

Rules:
- Never invent block types. Use only real types like event_whenflagclicked, motion_movesteps, control_forever, looks_say, etc.
- Prefer simple working stacks: start with event_whenflagclicked (or a key hat), then motion/looks/control.
- Emit ONE add_block per block so the user sees them appear. Set connectToPrevious:true for stacked statements after a hat.
- For numeric inputs use payload.inputs like {"STEPS": 10}. For text use {"MESSAGE": "Hello"}. For dropdown fields use payload.fields like {"KEY_OPTION": "space"}.
- When the user must upload a custom backdrop, costume, or sound, emit wait_for_user BEFORE blocks that need that asset:
  {"type":"wait_for_user","payload":{"need":"backdrop"|"costume"|"sound","message":"Please upload ..."}}
- Use select_target with payload.target "stage" or a sprite name/id before wait_for_user for costumes vs backdrops.
- Use ensure_sprite if you need an extra sprite: {"type":"ensure_sprite","payload":{"name":"Cat"}}.
- set_sprite_props: optional x,y,size,direction,visible.
- End with {"type":"done","payload":{"message":"Press the green flag to try it!"}} when finished.
- On continue after wait_for_user, finish remaining logic; do not re-ask for the same asset unless still missing.
- Keep stacks under ~25 blocks unless the user asks for more.
- Do not clear existing blocks unless the user asks to rebuild from scratch.

Example (walk left-right):
VEELEARN_SIM_ACTIONS_JSON:
[{"type":"message","payload":{"text":"Building a left-right walker…"}},{"type":"select_target","payload":{"target":"Sprite1"}},{"type":"add_block","payload":{"type":"event_whenflagclicked","newStack":true}},{"type":"add_block","payload":{"type":"control_forever","connectToPrevious":true}},{"type":"add_block","payload":{"type":"motion_movesteps","inputs":{"STEPS":10},"connectToPrevious":true,"into":"SUBSTACK"}},{"type":"add_block","payload":{"type":"motion_ifonedgebounce","connectToPrevious":true}},{"type":"done","payload":{"message":"Done — press ▶ to run!"}}]
Short reply here.`;

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

function extractActionsAndReply(raw) {
    const text = String(raw || '');
    const marker = 'VEELEARN_SIM_ACTIONS_JSON:';
    const idx = text.indexOf(marker);
    let jsonPart = '';
    let reply = '';
    if (idx >= 0) {
        const after = text.slice(idx + marker.length).trim();
        const arrStart = after.indexOf('[');
        if (arrStart >= 0) {
            let depth = 0;
            let end = -1;
            for (let i = arrStart; i < after.length; i++) {
                const c = after[i];
                if (c === '[') depth++;
                else if (c === ']') {
                    depth--;
                    if (depth === 0) {
                        end = i;
                        break;
                    }
                }
            }
            if (end >= 0) {
                jsonPart = after.slice(arrStart, end + 1);
                reply = after.slice(end + 1).trim();
            } else {
                jsonPart = after.slice(arrStart);
            }
        }
    } else {
        reply = text.trim();
    }

    let actions = [];
    if (jsonPart) {
        try {
            actions = JSON.parse(repairJsonStringEscapes(jsonPart));
        } catch (e) {
            try {
                // Truncation salvage: close open brackets
                let salvage = repairJsonStringEscapes(jsonPart);
                const open = (salvage.match(/\[/g) || []).length;
                const close = (salvage.match(/\]/g) || []).length;
                for (let i = 0; i < open - close; i++) salvage += ']';
                const lastObj = salvage.lastIndexOf('}');
                if (lastObj > 0) salvage = salvage.slice(0, lastObj + 1) + ']';
                actions = JSON.parse(salvage);
            } catch (_) {
                actions = [];
            }
        }
    }
    if (!Array.isArray(actions)) actions = [];
    return { actions, reply: String(reply || '').slice(0, 2000) };
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
        } else if (type === 'wait_for_user') {
            let need = String(payload.need || '').toLowerCase();
            if (!['backdrop', 'costume', 'sound'].includes(need)) need = 'costume';
            out.push({
                type,
                payload: {
                    need,
                    message: String(payload.message || `Please add a ${need}.`).slice(0, 500)
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

        if (out.length >= 60) break;
    }
    return out;
}

module.exports = function createAiSimulatorHelpHandlers({ openRouterChatCompletion, apiResponse, getOpenRouterKeys }) {
    return {
        async help(req, res) {
            const userId = req.user?.id;
            if (!userId) return apiResponse(res, 401, 'Authentication required');

            const keys = typeof getOpenRouterKeys === 'function' ? getOpenRouterKeys() : [];
            if (!keys.length) {
                return apiResponse(res, 503, 'AI is not configured (missing OpenRouter keys).');
            }

            const message = String(req.body?.message || '').trim().slice(0, 8000);
            const isContinue = !!req.body?.continue;
            const lastNeed = String(req.body?.lastNeed || '').slice(0, 40);
            const projectSummary = String(req.body?.projectSummary || '').slice(0, 4000);
            const history = Array.isArray(req.body?.history) ? req.body.history.slice(-12) : [];

            if (!message && !isContinue) {
                return apiResponse(res, 400, 'Message required');
            }

            const userContent = [
                isContinue
                    ? `CONTINUE after the user completed: ${lastNeed || 'asset upload'}. Finish remaining setup. Do not re-request the same asset.`
                    : `User request: ${message}`,
                projectSummary ? `\nCurrent project summary:\n${projectSummary}` : '',
                '\nEmit VEELEARN_SIM_ACTIONS_JSON: then actions.'
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

            let raw = '';
            try {
                raw = await openRouterChatCompletion(messages, {
                    temperature: 0.4,
                    max_tokens: 3500,
                    budgetMs: 45000,
                    timeoutMs: 55000
                });
            } catch (e) {
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

            const parsed = extractActionsAndReply(raw);
            const actions = validateActions(parsed.actions);
            let reply = parsed.reply;
            if (!actions.length && !reply) {
                reply = 'I could not build that yet. Try a simpler request like “make a sprite bounce side to side”.';
            }

            return apiResponse(res, 200, 'OK', {
                reply,
                actions,
                rawPreview: String(raw).slice(0, 500)
            });
        }
    };
};
