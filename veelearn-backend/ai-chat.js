'use strict';

/**
 * RETIRED PROVIDER — OpenRouter is no longer used anywhere in Veelearn.
 *
 * Every AI call now goes through Hack Club AI
 * (https://ai.hackclub.com/proxy/v1/chat/completions), the same client the
 * notes → master-course pipeline already uses (`./hackclub-ai.js`): one key,
 * `file` parts for PDFs, JSON forced when the caller asks for it.
 *
 * It exposes one shape — `aiChatCompletion(messages, opts) -> string` — and a
 * streaming variant that reads the proxy's OpenAI-compatible SSE frames. The
 * tutor, editor help, simulator help, session AI and calendar parsing all
 * receive these functions as parameters, so every caller shares one provider,
 * one key and one model. Error codes are generic (`AI_RATE_LIMITED`, ...) and
 * map onto the 429 / 503 / 504 responses the handlers already send.
 *
 * Callers that want structured output pass `{ jsonMust: true }`; the default is
 * prose, because forcing JSON on the tutor would break its reply.
 */

const axios = require('axios');
const hackclub = require('./hackclub-ai');

const HACKCLUB_URL = 'https://ai.hackclub.com/proxy/v1/chat/completions';

/** The model the whole product now uses: fast, free, and available on Hack Club. */
const DEFAULT_MODEL = 'google/gemma-4-26b-a4b-it:free';
const DEFAULT_TIMEOUT_MS = 60000;
const MAX_RETRY_DELAY_MS = 800;

function sanitizeModelId(m) {
    if (typeof m !== 'string') return '';
    return m
        .trim()
        .replace(/^["']+|["']+$/g, '')
        .replace(/\s+/g, '');
}

/** The single Hack Club key, expressed as a list because callers check `.length`. */
function getAiKeys() {
    const key = hackclub.getHackClubKey();
    return key ? [key] : [];
}

/** Model order: explicit ask → env → the gemma default → any fallbacks in env. */
function getModelCandidates(opts = {}) {
    const list = [];
    const push = (m) => {
        const v = sanitizeModelId(m);
        if (v && !list.includes(v)) list.push(v);
    };
    push(opts.model);
    push(process.env.HACKCLUBAI_MODEL);
    push(DEFAULT_MODEL);
    for (const m of String(process.env.HACKCLUBAI_FALLBACK_MODELS || '').split(',')) push(m);
    return list;
}

/** Hack Club error codes → the codes the handlers already branch on. */
function adaptError(e) {
    const code = String((e && e.code) || '');
    const status = e && e.status;
    const err = new Error((e && e.message) || 'Hack Club AI request failed');
    if (code === 'HACKCLUB_NOT_CONFIGURED') {
        err.code = 'AI_NOT_CONFIGURED';
        return err;
    }
    if (code === 'HACKCLUB_RATE_LIMITED' || status === 429) {
        err.code = 'AI_RATE_LIMITED';
        err.status = 429;
        return err;
    }
    if (code === 'HACKCLUB_TIMEOUT' || code === 'ECONNABORTED') {
        err.code = 'AI_TIMEOUT';
        err.status = 504;
        return err;
    }
    if (code === 'HACKCLUB_EMPTY') {
        err.code = 'AI_MODEL_UNAVAILABLE';
        err.status = 502;
        return err;
    }
    if (status === 400 || status === 404 || code === 'HACKCLUB_ERROR') {
        err.code = 'AI_MODEL_UNAVAILABLE';
        err.status = status || 502;
        return err;
    }
    err.code = 'AI_ERROR';
    err.status = status || 502;
    return err;
}

function isFatal(e) {
    const code = String((e && e.code) || '');
    return code === 'HACKCLUB_NOT_CONFIGURED' || code === 'HACKCLUB_RATE_LIMITED';
}

function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * Chat completion. Returns the reply text, exactly like the OpenRouter version
 * did, so no caller has to change.
 *
 * @param {Array<{role: string, content: any}>} messages
 * @param {{ model?: string, temperature?: number, max_tokens?: number,
 *           budgetMs?: number, timeoutMs?: number, jsonMust?: boolean }} [opts]
 * @returns {Promise<string>}
 */
async function aiChatCompletion(messages, opts = {}) {
    const key = hackclub.getHackClubKey();
    if (!key) {
        const err = new Error('Hack Club AI is not configured (HACKCLUBAI_KEY)');
        err.code = 'AI_NOT_CONFIGURED';
        throw err;
    }

    const models = getModelCandidates(opts);
    const timeoutMs = Number(opts.timeoutMs) || Number(opts.budgetMs) || DEFAULT_TIMEOUT_MS;
    let lastError = null;

    for (const model of models) {
        try {
            const out = await hackclub.hackClubChatCompletion(messages, {
                model,
                temperature: opts.temperature ?? 0.35,
                max_tokens: opts.max_tokens ?? 1024,
                timeoutMs,
                jsonMust: opts.jsonMust === true,
                fileContext: opts.fileContext
            });
            const content = typeof out === 'string' ? out : out && out.content;
            if (typeof content === 'string' && content.trim()) return content.trim();
            lastError = Object.assign(new Error('Hack Club AI returned an empty response'), { code: 'HACKCLUB_EMPTY' });
        } catch (e) {
            lastError = e;
            if (isFatal(e)) throw adaptError(e);
            // A different model may answer where this one failed.
        }
    }

    throw adaptError(lastError || Object.assign(new Error('Hack Club AI request failed'), { code: 'HACKCLUB_ERROR' }));
}

/**
 * Streaming completion. The Hack Club proxy is OpenAI-compatible, so this reads
 * the same SSE frames the old client did; if the proxy answers with plain JSON
 * (or no deltas at all) the one-shot call is replayed as a single delta, which
 * keeps streaming endpoints working rather than failing.
 *
 * @param {Array<{role: string, content: any}>} messages
 * @param {{ onDelta?: (chunk: string) => void }} [opts]
 * @returns {Promise<string>} full content
 */
async function aiChatCompletionStream(messages, opts = {}) {
    const key = hackclub.getHackClubKey();
    if (!key) {
        const err = new Error('Hack Club AI is not configured (HACKCLUBAI_KEY)');
        err.code = 'AI_NOT_CONFIGURED';
        throw err;
    }

    const onDelta = typeof opts.onDelta === 'function' ? opts.onDelta : null;
    const model = getModelCandidates(opts)[0];
    const packed = hackclub.toHackClubMessages(messages, { jsonMust: opts.jsonMust === true });
    const timeoutMs = Number(opts.timeoutMs) || Number(opts.budgetMs) || DEFAULT_TIMEOUT_MS;

    try {
        const res = await axios.post(
            HACKCLUB_URL,
            {
                model,
                messages: packed.messages,
                temperature: opts.temperature ?? 0.35,
                max_tokens: opts.max_tokens ?? 1024,
                stream: true
            },
            {
                headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
                timeout: timeoutMs,
                responseType: 'stream',
                validateStatus: () => true,
                maxBodyLength: Infinity,
                maxContentLength: Infinity
            }
        );

        if (res.status === 429) {
            const err = new Error('Hack Club AI rate limited');
            err.code = 'HACKCLUB_RATE_LIMITED';
            throw err;
        }
        if (res.status < 200 || res.status >= 300) {
            try {
                res.data.destroy?.();
            } catch (_) {
                /* ignore */
            }
            const err = new Error(`Hack Club AI HTTP ${res.status}`);
            err.code = 'HACKCLUB_ERROR';
            err.status = res.status;
            throw err;
        }

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
                        const delta = json?.choices?.[0]?.delta?.content ?? json?.choices?.[0]?.message?.content;
                        if (typeof delta === 'string' && delta) {
                            full += delta;
                            if (onDelta) {
                                try {
                                    onDelta(delta);
                                } catch (_) {
                                    /* the caller's writer failed; keep reading */
                                }
                            }
                        }
                    } catch (_) {
                        /* not a JSON frame */
                    }
                }
            });
            res.data.on('end', resolve);
            res.data.on('error', reject);
        });

        if (full.trim()) return full.trim();
    } catch (e) {
        if (isFatal(e)) throw adaptError(e);
        await sleep(MAX_RETRY_DELAY_MS);
    }

    // No usable stream: replay the one-shot answer so the endpoint still works.
    const text = await aiChatCompletion(messages, opts);
    if (onDelta && text) {
        try {
            onDelta(text);
        } catch (_) {
            /* ignore */
        }
    }
    return text;
}

module.exports = {
    DEFAULT_MODEL,
    getModelCandidates,
    getAiKeys,
    aiChatCompletion,
    aiChatCompletionStream,
    sanitizeModelId
};
