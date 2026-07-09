const axios = require('axios');

const OPENROUTER_URL = 'https://openrouter.ai/api/v1/chat/completions';

function getOpenRouterKeys() {
    const raw = process.env.OPENROUTER_API_KEYS || '';
    const split = raw.split(',').map((k) => k.trim()).filter(Boolean);
    if (split.length) return split;
    const keys = [];
    for (let i = 1; i <= 8; i++) {
        const k = process.env[`OPENROUTER_KEY_${i}`];
        if (k && String(k).trim()) keys.push(String(k).trim());
    }
    return keys;
}

function shouldTryNextKey(status, err) {
    if (status === 401 || status === 429 || status >= 500) return true;
    if (err && (err.code === 'ECONNABORTED' || err.code === 'ETIMEDOUT' || err.code === 'ECONNRESET')) return true;
    return false;
}

/**
 * @param {Array<{ role: string, content: string }>} messages
 * @param {{ temperature?: number, max_tokens?: number }} [opts]
 * @returns {Promise<string>}
 */
async function openRouterChatCompletion(messages, opts = {}) {
    const keys = getOpenRouterKeys();
    if (!keys.length) {
        const err = new Error('OpenRouter API keys not configured');
        err.code = 'OPENROUTER_NOT_CONFIGURED';
        throw err;
    }

    const model = process.env.OPENROUTER_MODEL || 'google/gemini-2.5-flash:free';
    const temperature = opts.temperature ?? 0.35;
    const max_tokens = opts.max_tokens ?? 1024;
    const referer = process.env.OPENROUTER_SITE_URL || 'https://veelearn.org';
    const title = process.env.OPENROUTER_APP_TITLE || 'Veelearn Study Coach';

    let lastError;

    for (let i = 0; i < keys.length; i++) {
        const key = keys[i];
        try {
            const res = await axios.post(
                OPENROUTER_URL,
                { model, messages, temperature, max_tokens },
                {
                    headers: {
                        Authorization: `Bearer ${key}`,
                        'HTTP-Referer': referer,
                        'X-Title': title,
                        'Content-Type': 'application/json'
                    },
                    timeout: 45000,
                    validateStatus: () => true
                }
            );

            const status = res.status;
            if (shouldTryNextKey(status)) {
                lastError = new Error(`OpenRouter HTTP ${status}`);
                lastError.status = status;
                continue;
            }

            if (status === 400) {
                const err = new Error(`OpenRouter bad request: ${JSON.stringify(res.data).slice(0, 300)}`);
                err.status = 400;
                throw err;
            }

            if (status !== 200) {
                lastError = new Error(`OpenRouter HTTP ${status}`);
                lastError.status = status;
                lastError.data = res.data;
                continue;
            }

            const content = res.data?.choices?.[0]?.message?.content;
            if (typeof content !== 'string' || !content.trim()) {
                lastError = new Error('Empty OpenRouter response');
                continue;
            }

            return content.trim();
        } catch (e) {
            lastError = e;
            const st = e.response?.status;
            if (st && shouldTryNextKey(st, e)) continue;
            if (!e.response && shouldTryNextKey(0, e)) continue;
            if (e.response && !shouldTryNextKey(st, e)) throw e;
        }
    }

    const err = lastError || new Error('OpenRouter request failed');
    if (!err.code && err.message && err.message.includes('not configured')) err.code = 'OPENROUTER_NOT_CONFIGURED';
    throw err;
}

module.exports = { getOpenRouterKeys, openRouterChatCompletion };
