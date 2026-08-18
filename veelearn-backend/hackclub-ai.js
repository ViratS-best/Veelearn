const axios = require('axios');

const HACKCLUB_URL = 'https://ai.hackclub.com/proxy/v1/chat/completions';
const DEFAULT_MODEL = 'dots-studio/dots-3-note-preview:free';
const DEFAULT_TIMEOUT_MS = 120000;

function getHackClubKey() {
    return String(process.env.HACKCLUBAI_KEY || '').trim();
}

function getHackClubModel() {
    return String(process.env.HACKCLUBAI_MODEL || DEFAULT_MODEL).trim() || DEFAULT_MODEL;
}

function flattenContent(content) {
    if (content == null) return '';
    if (typeof content === 'string') return content;
    if (typeof content === 'number' || typeof content === 'boolean') return String(content);
    if (Array.isArray(content)) {
        return content.map(flattenContent).filter(Boolean).join('\n');
    }
    if (typeof content === 'object') {
        if (typeof content.text === 'string') return content.text;
        if (typeof content.output_text === 'string') return content.output_text;
        if (typeof content.content === 'string') return content.content;
        if (content.parsed && typeof content.parsed === 'object') {
            try {
                return JSON.stringify(content.parsed);
            } catch (_) { /* ignore */ }
        }
        if (content.content) return flattenContent(content.content);
        if (Array.isArray(content.parts)) return flattenContent(content.parts);
    }
    return '';
}

function extractAssistantText(data) {
    const choice = data?.choices?.[0] || {};
    const msg = choice.message || choice.delta || {};
    const chunks = [
        flattenContent(msg.content),
        flattenContent(msg.reasoning_content),
        flattenContent(msg.reasoning),
        flattenContent(choice.text),
        flattenContent(data?.output_text)
    ];
    if (msg.parsed && typeof msg.parsed === 'object') {
        try {
            chunks.push(JSON.stringify(msg.parsed));
        } catch (_) { /* ignore */ }
    }
    if (Array.isArray(data?.output)) {
        for (const item of data.output) chunks.push(flattenContent(item?.content));
    }
    return chunks.filter((p) => typeof p === 'string' && p.trim()).join('\n').trim();
}

function diagnostic(data, status) {
    const choice = data?.choices?.[0] || {};
    const msg = choice.message || {};
    return {
        status,
        finish: choice.finish_reason || choice.native_finish_reason || data?.finish_reason,
        contentType: msg.content == null ? 'null' : Array.isArray(msg.content) ? 'array' : typeof msg.content,
        msgKeys: msg && typeof msg === 'object' ? Object.keys(msg).slice(0, 12) : [],
        error: data?.error?.message || null
    };
}

/**
 * Chat completion via Hack Club AI (OpenAI-compatible proxy).
 * `messages[].content` may be a string or a multimodal array (text / image_url / file).
 * @param {Array} messages
 * @param {{ temperature?: number, max_tokens?: number, model?: string, timeoutMs?: number, json?: boolean }} [opts]
 * @returns {Promise<string>}
 */
async function hackClubChatCompletion(messages, opts = {}) {
    const key = getHackClubKey();
    if (!key) {
        const err = new Error('Hack Club AI is not configured');
        err.code = 'HACKCLUB_NOT_CONFIGURED';
        throw err;
    }

    const model = opts.model || getHackClubModel();

    const postOnce = async (body) => {
        const res = await axios.post(HACKCLUB_URL, body, {
            headers: {
                Authorization: `Bearer ${key}`,
                'Content-Type': 'application/json'
            },
            timeout: opts.timeoutMs ?? DEFAULT_TIMEOUT_MS,
            maxBodyLength: Infinity,
            maxContentLength: Infinity,
            validateStatus: () => true
        });
        return res;
    };

    const base = {
        model,
        messages,
        temperature: opts.temperature ?? 0.2,
        max_tokens: opts.max_tokens ?? 4096
    };

    const attempts = [];
    if (opts.json !== false) {
        attempts.push({
            ...base,
            response_format: { type: 'json_object' },
            reasoning: { exclude: true },
            include_reasoning: false
        });
    }
    attempts.push({
        ...base,
        reasoning: { exclude: true },
        include_reasoning: false
    });
    attempts.push({ ...base });

    let lastError;
    for (let i = 0; i < attempts.length; i++) {
        const body = attempts[i];
        try {
            const res = await postOnce(body);

            if (res.status === 429) {
                const err = new Error('Hack Club AI rate limited');
                err.code = 'HACKCLUB_RATE_LIMITED';
                err.status = 429;
                throw err;
            }

            // Unknown fields (response_format / reasoning) — try a simpler body
            if (res.status === 400 && i < attempts.length - 1) {
                console.warn('[hackclub] HTTP 400, retrying simpler body', res.data?.error?.message || res.data?.message || '');
                continue;
            }

            if (res.status < 200 || res.status >= 300) {
                const msg =
                    res.data?.error?.message ||
                    res.data?.message ||
                    `Hack Club AI HTTP ${res.status}`;
                const err = new Error(typeof msg === 'string' ? msg : 'Hack Club AI request failed');
                err.code = 'HACKCLUB_ERROR';
                err.status = res.status;
                lastError = err;
                continue;
            }

            const content = extractAssistantText(res.data);
            if (content) return content;

            console.warn('[hackclub] empty content', diagnostic(res.data, res.status));
            lastError = Object.assign(new Error('Hack Club AI returned an empty response'), {
                code: 'HACKCLUB_EMPTY'
            });
        } catch (e) {
            if (e.code === 'HACKCLUB_RATE_LIMITED' || e.code === 'HACKCLUB_NOT_CONFIGURED') throw e;
            if (e.code && String(e.code).startsWith('HACKCLUB_')) {
                lastError = e;
                continue;
            }
            const err = new Error(e.message || 'Hack Club AI request failed');
            err.code = e.code === 'ECONNABORTED' ? 'HACKCLUB_TIMEOUT' : 'HACKCLUB_ERROR';
            err.status = e.response?.status;
            lastError = err;
        }
    }

    throw lastError || Object.assign(new Error('Hack Club AI returned an empty response'), { code: 'HACKCLUB_EMPTY' });
}

module.exports = {
    hackClubChatCompletion,
    extractAssistantText,
    getHackClubKey,
    getHackClubModel,
    DEFAULT_MODEL
};
