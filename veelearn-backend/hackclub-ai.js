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

/**
 * Chat completion via Hack Club AI (OpenAI-compatible proxy).
 * `messages[].content` may be a string or a multimodal array (text / image_url / file).
 * @param {Array} messages
 * @param {{ temperature?: number, max_tokens?: number, model?: string, timeoutMs?: number }} [opts]
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
    const body = {
        model,
        messages,
        temperature: opts.temperature ?? 0.35,
        max_tokens: opts.max_tokens ?? 8192
    };

    try {
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

        if (res.status === 429) {
            const err = new Error('Hack Club AI rate limited');
            err.code = 'HACKCLUB_RATE_LIMITED';
            err.status = 429;
            throw err;
        }
        if (res.status < 200 || res.status >= 300) {
            const msg =
                res.data?.error?.message ||
                res.data?.message ||
                `Hack Club AI HTTP ${res.status}`;
            const err = new Error(typeof msg === 'string' ? msg : 'Hack Club AI request failed');
            err.code = 'HACKCLUB_ERROR';
            err.status = res.status;
            throw err;
        }

        const content = res.data?.choices?.[0]?.message?.content;
        if (!content || typeof content !== 'string') {
            const err = new Error('Hack Club AI returned an empty response');
            err.code = 'HACKCLUB_EMPTY';
            throw err;
        }
        return content;
    } catch (e) {
        if (e.code && String(e.code).startsWith('HACKCLUB_')) throw e;
        const err = new Error(e.message || 'Hack Club AI request failed');
        err.code = e.code === 'ECONNABORTED' ? 'HACKCLUB_TIMEOUT' : 'HACKCLUB_ERROR';
        err.status = e.response?.status;
        throw err;
    }
}

module.exports = {
    hackClubChatCompletion,
    getHackClubKey,
    getHackClubModel,
    DEFAULT_MODEL
};
