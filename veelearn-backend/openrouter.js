const axios = require('axios');

const OPENROUTER_URL = 'https://openrouter.ai/api/v1/chat/completions';
/** Retries on the same key when it is the only key left; otherwise rotate immediately on 429. */
const MAX_RETRIES_SOLE_KEY = 2;
const BASE_RETRY_DELAY_MS = 800;
/** Stay under typical reverse-proxy idle timeouts when possible; section mode may use a higher budget. */
const DEFAULT_BUDGET_MS = 35000;
const DEFAULT_TIMEOUT_MS = 45000;

/** Last-resort router that picks any available free model. */
const FREE_ROUTER = 'openrouter/free';

function sanitizeModelId(m) {
    if (typeof m !== 'string') return '';
    return m
        .trim()
        .replace(/^["']+|["']+$/g, '')
        .replace(/\s+/g, '');
}

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

function getModelCandidates(opts = {}) {
    const list = [];
    const push = (m) => {
        const v = sanitizeModelId(m);
        if (v && !list.includes(v)) list.push(v);
    };

    push(opts.model);
    push(process.env.OPENROUTER_MODEL || 'google/gemma-4-31b-it:free');

    const fallbacks = (process.env.OPENROUTER_FALLBACK_MODELS || '').split(',');
    for (const m of fallbacks) push(m);

    push('google/gemma-4-31b-it:free');
    push('google/gemma-4-26b-a4b-it:free');
    push('openai/gpt-oss-20b:free');
    push(FREE_ROUTER);

    return list;
}

function shouldTryNextKey(status, err) {
    if (status === 401 || status === 429 || status >= 500) return true;
    if (err && (err.code === 'ECONNABORTED' || err.code === 'ETIMEDOUT' || err.code === 'ECONNRESET')) return true;
    return false;
}

function shouldSkipModel(status) {
    return status === 404 || status === 400;
}

function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}

function commonHeaders(key, referer, title) {
    return {
        Authorization: `Bearer ${key}`,
        'HTTP-Referer': referer,
        'X-Title': title,
        'Content-Type': 'application/json'
    };
}

/**
 * @param {Array<{ role: string, content: string }>} messages
 * @param {{ temperature?: number, max_tokens?: number, model?: string, budgetMs?: number }} [opts]
 * @returns {Promise<string>}
 */
async function openRouterChatCompletion(messages, opts = {}) {
    const keys = getOpenRouterKeys();
    if (!keys.length) {
        const err = new Error('OpenRouter API keys not configured');
        err.code = 'OPENROUTER_NOT_CONFIGURED';
        throw err;
    }

    const models = getModelCandidates(opts);
    const temperature = opts.temperature ?? 0.35;
    const max_tokens = opts.max_tokens ?? 1024;
    const referer = process.env.OPENROUTER_SITE_URL || 'https://veelearn.org';
    const title = process.env.OPENROUTER_APP_TITLE || 'Veelearn Study Coach';
    const budgetMs = opts.budgetMs ?? DEFAULT_BUDGET_MS;
    const started = Date.now();

    let lastError;
    let sawOnly429 = true;
    let sawModelUnavailable = false;

    console.log(`[OpenRouter] Trying models: ${models.join(' → ')}`);

    modelLoop: for (const model of models) {
        for (let i = 0; i < keys.length; i++) {
            if (Date.now() - started > budgetMs) {
                const err = new Error('OpenRouter request budget exceeded');
                err.code = sawOnly429 ? 'OPENROUTER_RATE_LIMITED' : 'OPENROUTER_TIMEOUT';
                err.status = sawOnly429 ? 429 : 504;
                throw err;
            }

            const key = keys[i];
            const remainingKeys = keys.length - i;
            const isLastModel = models.indexOf(model) === models.length - 1;
            const maxAttempts = remainingKeys === 1 && isLastModel ? MAX_RETRIES_SOLE_KEY : 0;

            for (let attempt = 0; attempt <= maxAttempts; attempt++) {
                try {
                    const res = await axios.post(
                        OPENROUTER_URL,
                        { model, messages, temperature, max_tokens },
                        {
                            headers: commonHeaders(key, referer, title),
                            timeout: opts.timeoutMs || DEFAULT_TIMEOUT_MS,
                            validateStatus: () => true
                        }
                    );

                    const status = res.status;

                    if (status === 429) {
                        lastError = new Error(`OpenRouter HTTP 429 (rate limited) model=${model}`);
                        lastError.status = 429;
                        lastError.code = 'OPENROUTER_RATE_LIMITED';
                        if (attempt < maxAttempts) {
                            await sleep(BASE_RETRY_DELAY_MS * Math.pow(2, attempt));
                            continue;
                        }
                        break;
                    }

                    if (shouldSkipModel(status)) {
                        sawOnly429 = false;
                        sawModelUnavailable = true;
                        const detail = JSON.stringify(res.data || {}).slice(0, 240);
                        lastError = new Error(`OpenRouter HTTP ${status} model=${model} ${detail}`);
                        lastError.status = status;
                        lastError.code = 'OPENROUTER_MODEL_UNAVAILABLE';
                        console.warn(`[OpenRouter] Skipping model ${model}: HTTP ${status}`);
                        continue modelLoop;
                    }

                    sawOnly429 = false;

                    if (shouldTryNextKey(status)) {
                        lastError = new Error(`OpenRouter HTTP ${status} model=${model}`);
                        lastError.status = status;
                        break;
                    }

                    if (status !== 200) {
                        lastError = new Error(`OpenRouter HTTP ${status} model=${model}`);
                        lastError.status = status;
                        lastError.data = res.data;
                        break;
                    }

                    const content = res.data?.choices?.[0]?.message?.content;
                    if (typeof content !== 'string' || !content.trim()) {
                        lastError = new Error(`Empty OpenRouter response model=${model}`);
                        break;
                    }

                    console.log(`[OpenRouter] Success with model=${model}`);
                    return content.trim();
                } catch (e) {
                    sawOnly429 = false;
                    lastError = e;
                    const st = e.response?.status;
                    if (st === 429) {
                        lastError.code = 'OPENROUTER_RATE_LIMITED';
                        lastError.status = 429;
                        sawOnly429 = true;
                        break;
                    }
                    if (shouldSkipModel(st)) {
                        sawModelUnavailable = true;
                        lastError.code = 'OPENROUTER_MODEL_UNAVAILABLE';
                        lastError.status = st;
                        continue modelLoop;
                    }
                    if (st && shouldTryNextKey(st, e)) break;
                    if (!e.response && shouldTryNextKey(0, e)) break;
                    if (e.response && !shouldTryNextKey(st, e)) throw e;
                    break;
                }
            }
        }
    }

    const err = lastError || new Error('OpenRouter request failed');
    if (!err.code && err.message && err.message.includes('not configured')) {
        err.code = 'OPENROUTER_NOT_CONFIGURED';
    }
    if (!err.code && (err.status === 429 || /429|rate limited/i.test(err.message || ''))) {
        err.code = 'OPENROUTER_RATE_LIMITED';
        err.status = 429;
    }
    if (!err.code && (sawModelUnavailable || err.status === 404)) {
        err.code = 'OPENROUTER_MODEL_UNAVAILABLE';
        err.status = 404;
    }
    throw err;
}

/**
 * Stream OpenRouter chat completions. Invokes onDelta(textChunk) for each piece.
 * @returns {Promise<string>} full content
 */
async function openRouterChatCompletionStream(messages, opts = {}) {
    const keys = getOpenRouterKeys();
    if (!keys.length) {
        const err = new Error('OpenRouter API keys not configured');
        err.code = 'OPENROUTER_NOT_CONFIGURED';
        throw err;
    }

    const models = getModelCandidates(opts);
    const temperature = opts.temperature ?? 0.35;
    const max_tokens = opts.max_tokens ?? 1024;
    const referer = process.env.OPENROUTER_SITE_URL || 'https://veelearn.org';
    const title = process.env.OPENROUTER_APP_TITLE || 'Veelearn Study Coach';
    const budgetMs = opts.budgetMs ?? DEFAULT_BUDGET_MS;
    const onDelta = typeof opts.onDelta === 'function' ? opts.onDelta : null;
    const started = Date.now();

    let lastError;
    let sawOnly429 = true;
    let sawModelUnavailable = false;

    console.log(`[OpenRouter stream] Trying models: ${models.join(' → ')}`);

    modelLoop: for (const model of models) {
        for (let i = 0; i < keys.length; i++) {
            if (Date.now() - started > budgetMs) {
                const err = new Error('OpenRouter request budget exceeded');
                err.code = sawOnly429 ? 'OPENROUTER_RATE_LIMITED' : 'OPENROUTER_TIMEOUT';
                err.status = sawOnly429 ? 429 : 504;
                throw err;
            }

            const key = keys[i];

            try {
                const res = await axios.post(
                    OPENROUTER_URL,
                    { model, messages, temperature, max_tokens, stream: true },
                    {
                        headers: commonHeaders(key, referer, title),
                        timeout: opts.timeoutMs || 90000,
                        responseType: 'stream',
                        validateStatus: () => true
                    }
                );

                const status = res.status;
                if (status === 429) {
                    lastError = new Error(`OpenRouter HTTP 429 (rate limited) model=${model}`);
                    lastError.status = 429;
                    lastError.code = 'OPENROUTER_RATE_LIMITED';
                    sawOnly429 = true;
                    try {
                        res.data.destroy?.();
                    } catch (_) { /* ignore */ }
                    continue;
                }
                if (shouldSkipModel(status)) {
                    sawOnly429 = false;
                    sawModelUnavailable = true;
                    lastError = new Error(`OpenRouter HTTP ${status} model=${model}`);
                    lastError.status = status;
                    lastError.code = 'OPENROUTER_MODEL_UNAVAILABLE';
                    try {
                        res.data.destroy?.();
                    } catch (_) { /* ignore */ }
                    continue modelLoop;
                }
                if (status !== 200) {
                    sawOnly429 = false;
                    lastError = new Error(`OpenRouter HTTP ${status} model=${model}`);
                    lastError.status = status;
                    try {
                        res.data.destroy?.();
                    } catch (_) { /* ignore */ }
                    if (shouldTryNextKey(status)) continue;
                    break;
                }

                sawOnly429 = false;
                let full = '';
                let buffer = '';

                await new Promise((resolve, reject) => {
                    res.data.on('data', (chunk) => {
                        buffer += chunk.toString('utf8');
                        const parts = buffer.split('\n');
                        buffer = parts.pop() || '';
                        for (const line of parts) {
                            const trimmed = line.trim();
                            if (!trimmed || trimmed.startsWith(':')) continue;
                            if (!trimmed.startsWith('data:')) continue;
                            const payload = trimmed.slice(5).trim();
                            if (payload === '[DONE]') continue;
                            try {
                                const json = JSON.parse(payload);
                                const delta = json?.choices?.[0]?.delta?.content;
                                if (typeof delta === 'string' && delta) {
                                    full += delta;
                                    if (onDelta) {
                                        try {
                                            onDelta(delta);
                                        } catch (_) { /* ignore */ }
                                    }
                                }
                            } catch (_) {
                                /* ignore */
                            }
                        }
                    });
                    res.data.on('end', resolve);
                    res.data.on('error', reject);
                });

                if (!full.trim()) {
                    lastError = new Error(`Empty OpenRouter stream model=${model}`);
                    continue;
                }

                console.log(`[OpenRouter stream] Success with model=${model}`);
                return full.trim();
            } catch (e) {
                sawOnly429 = false;
                lastError = e;
                const st = e.response?.status;
                if (st === 429) {
                    lastError.code = 'OPENROUTER_RATE_LIMITED';
                    lastError.status = 429;
                    sawOnly429 = true;
                    continue;
                }
                if (shouldSkipModel(st)) {
                    sawModelUnavailable = true;
                    lastError.code = 'OPENROUTER_MODEL_UNAVAILABLE';
                    lastError.status = st;
                    continue modelLoop;
                }
                if (st && shouldTryNextKey(st, e)) continue;
                if (!e.response && shouldTryNextKey(0, e)) continue;
            }
        }
    }

    const err = lastError || new Error('OpenRouter stream failed');
    if (!err.code && err.message && err.message.includes('not configured')) {
        err.code = 'OPENROUTER_NOT_CONFIGURED';
    }
    if (!err.code && (err.status === 429 || /429|rate limited/i.test(err.message || ''))) {
        err.code = 'OPENROUTER_RATE_LIMITED';
        err.status = 429;
    }
    if (!err.code && (sawModelUnavailable || err.status === 404)) {
        err.code = 'OPENROUTER_MODEL_UNAVAILABLE';
        err.status = 404;
    }
    throw err;
}

module.exports = {
    getOpenRouterKeys,
    openRouterChatCompletion,
    openRouterChatCompletionStream,
    getModelCandidates,
    sanitizeModelId
};
