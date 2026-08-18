const axios = require('axios');

const HACKCLUB_URL = 'https://ai.hackclub.com/proxy/v1/chat/completions';
const DEFAULT_MODEL = 'dots-studio/dots-3-note-preview:free';
const DEFAULT_JSON_MODEL = 'qwen/qwen3-32b';
const DEFAULT_TIMEOUT_MS = 180000;

const JSON_MUST =
    '/no_think\nYou MUST use JSON. Reply with a single JSON object and nothing else. No markdown. No code fences. No explanation. Do not think out loud. The first character of your reply must be { and the last character must be }.';

function getHackClubKey() {
    return String(process.env.HACKCLUBAI_KEY || '').trim();
}

function getHackClubModel() {
    return String(process.env.HACKCLUBAI_MODEL || DEFAULT_MODEL).trim() || DEFAULT_MODEL;
}

function getHackClubJsonModel() {
    return String(process.env.HACKCLUBAI_JSON_MODEL || DEFAULT_JSON_MODEL).trim() || DEFAULT_JSON_MODEL;
}

function isReasoningPart(part) {
    const t = String(part?.type || '').toLowerCase();
    return t === 'reasoning' || t === 'thinking' || t === 'reason';
}

function flattenContent(content, opts = {}) {
    const includeReasoning = Boolean(opts.includeReasoning);
    if (content == null) return '';
    if (typeof content === 'string') return content;
    if (typeof content === 'number' || typeof content === 'boolean') return String(content);
    if (Array.isArray(content)) {
        return content
            .map((part) => {
                if (part && typeof part === 'object' && isReasoningPart(part) && !includeReasoning) return '';
                return flattenContent(part, opts);
            })
            .filter(Boolean)
            .join('\n');
    }
    if (typeof content === 'object') {
        if (!includeReasoning && isReasoningPart(content)) return '';
        if (typeof content.text === 'string') return content.text;
        if (typeof content.output_text === 'string') return content.output_text;
        if (typeof content.content === 'string') return content.content;
        if (content.parsed && typeof content.parsed === 'object') {
            try {
                return JSON.stringify(content.parsed);
            } catch (_) { /* ignore */ }
        }
        if (content.content) return flattenContent(content.content, opts);
        if (Array.isArray(content.parts)) return flattenContent(content.parts, opts);
    }
    return '';
}

function firstNonEmpty(parts) {
    for (const p of parts) {
        if (typeof p === 'string' && p.trim()) return p.trim();
    }
    return '';
}

function extractAssistantText(data) {
    const choice = data?.choices?.[0] || {};
    const msg = choice.message || choice.delta || {};
    if (msg.parsed && typeof msg.parsed === 'object') {
        try {
            return JSON.stringify(msg.parsed);
        } catch (_) { /* ignore */ }
    }
    const outputBits = [];
    if (Array.isArray(data?.output)) {
        for (const item of data.output) outputBits.push(flattenContent(item?.content));
    }
    const primary = firstNonEmpty([
        flattenContent(msg.content),
        flattenContent(choice.text),
        flattenContent(data?.output_text),
        ...outputBits
    ]);
    if (primary) return primary;
    return firstNonEmpty([
        flattenContent(msg.refusal),
        flattenContent(msg.reasoning_content, { includeReasoning: true }),
        flattenContent(msg.reasoning, { includeReasoning: true })
    ]);
}

function isFilePart(part) {
    return part && typeof part === 'object' && part.type === 'file' && part.file;
}

function isImagePart(part) {
    return part && typeof part === 'object' && part.type === 'image_url' && part.image_url;
}

function contentHasFiles(content) {
    return Array.isArray(content) && content.some(isFilePart);
}

function messagesHaveFiles(messages) {
    return (messages || []).some((m) => contentHasFiles(m?.content));
}

function appendJsonMust(text) {
    const t = String(text || '').trim();
    if (!t) return JSON_MUST;
    if (/MUST use JSON/i.test(t) && /first character/i.test(t)) return t;
    return `${t}\n\n${JSON_MUST}`;
}

/**
 * One user (or user+history) turn. Keeps PDF `file` parts and `image_url` parts.
 * JSON is forced in the text. Matches Hack Club image/PDF input docs.
 */
function toHackClubMessages(messages, { jsonMust = true } = {}) {
    const texts = [];
    const files = [];
    const images = [];
    const extraTurns = [];

    for (const m of messages || []) {
        const role = m?.role || 'user';
        const c = m?.content;
        if (role === 'assistant') {
            extraTurns.push({
                role: 'assistant',
                content: typeof c === 'string' ? c : flattenContent(c),
                ...(m.annotations ? { annotations: m.annotations } : {})
            });
            continue;
        }
        if (typeof c === 'string') {
            texts.push(role === 'system' ? `INSTRUCTIONS:\n${c}` : c);
            continue;
        }
        if (Array.isArray(c)) {
            for (const part of c) {
                if (!part || typeof part !== 'object') continue;
                if (part.type === 'text' && part.text) {
                    texts.push(role === 'system' ? `INSTRUCTIONS:\n${part.text}` : String(part.text));
                } else if (isFilePart(part) && files.length < 3) {
                    files.push({
                        type: 'file',
                        file: {
                            filename: String(part.file.filename || 'document.pdf').slice(0, 180),
                            file_data: part.file.file_data
                        }
                    });
                } else if (isImagePart(part) && images.length < 6) {
                    images.push({
                        type: 'image_url',
                        image_url: { url: part.image_url.url }
                    });
                }
            }
        }
    }

    const text = jsonMust ? appendJsonMust(texts.filter(Boolean).join('\n\n')) : texts.filter(Boolean).join('\n\n');
    const parts = [{ type: 'text', text }];
    for (const f of files) parts.push(f);
    for (const img of images) parts.push(img);

    const userMessage =
        files.length || images.length
            ? { role: 'user', content: parts }
            : { role: 'user', content: text };

    return { messages: [userMessage, ...extraTurns], userMessage };
}

function fileParserPlugin(engine) {
    return {
        id: 'file-parser',
        pdf: { engine: engine || 'native' }
    };
}

function withFileContext(newMessages, fileContext) {
    if (!fileContext?.userMessage || !fileContext?.annotations) {
        return toHackClubMessages(newMessages);
    }
    const follow = toHackClubMessages(newMessages);
    const followUser = follow.userMessage;
    const followContent =
        typeof followUser.content === 'string'
            ? followUser.content
            : flattenContent((followUser.content || []).filter((p) => p.type === 'text'));
    return {
        messages: [
            fileContext.userMessage,
            {
                role: 'assistant',
                content: fileContext.content || '',
                annotations: fileContext.annotations
            },
            { role: 'user', content: appendJsonMust(followContent) }
        ],
        userMessage: fileContext.userMessage
    };
}

async function postChat(body, timeoutMs) {
    const key = getHackClubKey();
    return axios.post(HACKCLUB_URL, body, {
        headers: {
            Authorization: `Bearer ${key}`,
            'Content-Type': 'application/json'
        },
        timeout: timeoutMs,
        maxBodyLength: Infinity,
        maxContentLength: Infinity,
        validateStatus: () => true
    });
}

/**
 * Hack Club chat completions. Documented fields: model, messages, temperature, max_tokens.
 * PDFs use plugins file-parser (native → pdf-text → mistral-ocr). JSON is forced in the user text.
 */
async function hackClubChatCompletion(messages, opts = {}) {
    const key = getHackClubKey();
    if (!key) {
        const err = new Error('Hack Club AI is not configured');
        err.code = 'HACKCLUB_NOT_CONFIGURED';
        throw err;
    }

    const model = opts.model || getHackClubModel();
    const packed = opts.fileContext?.annotations
        ? withFileContext(messages, opts.fileContext)
        : toHackClubMessages(messages);
    const hcMessages = packed.messages;
    const hasFiles = messagesHaveFiles(hcMessages) && !opts.fileContext?.annotations;
    const maxTokens = opts.max_tokens ?? 8192;
    const timeoutMs = opts.timeoutMs ?? (hasFiles ? 240000 : DEFAULT_TIMEOUT_MS);

    const engines = hasFiles
        ? [opts.pdfEngine || 'native', 'pdf-text', 'mistral-ocr']
        : [null];
    const seen = new Set();
    const engineList = engines.filter((e) => {
        const k = e || 'none';
        if (seen.has(k)) return false;
        seen.add(k);
        return true;
    });

    let lastError;
    for (const engine of engineList) {
        const body = {
            model,
            messages: hcMessages,
            temperature: opts.temperature ?? 0.1,
            max_tokens: maxTokens
        };
        if (hasFiles && engine) {
            body.plugins = [fileParserPlugin(engine)];
        }

        try {
            const res = await postChat(body, timeoutMs);
            if (res.status === 429) {
                const err = new Error('Hack Club AI rate limited');
                err.code = 'HACKCLUB_RATE_LIMITED';
                err.status = 429;
                throw err;
            }
            if (res.status === 400) {
                lastError = Object.assign(
                    new Error(res.data?.error?.message || res.data?.message || 'Hack Club AI HTTP 400'),
                    { code: 'HACKCLUB_ERROR', status: 400 }
                );
                continue;
            }
            if (res.status < 200 || res.status >= 300) {
                const msg = res.data?.error?.message || res.data?.message || `Hack Club AI HTTP ${res.status}`;
                lastError = Object.assign(new Error(typeof msg === 'string' ? msg : 'Hack Club AI request failed'), {
                    code: 'HACKCLUB_ERROR',
                    status: res.status
                });
                continue;
            }

            const choice = res.data?.choices?.[0] || {};
            const msg = choice.message || {};
            const content = extractAssistantText(res.data);
            if (content) {
                return {
                    content,
                    annotations: msg.annotations || null,
                    userMessage: packed.userMessage,
                    finishReason: choice.finish_reason || null
                };
            }

            const parseErr = res.data?.error?.message || null;
            console.warn('[hackclub] empty content', {
                status: res.status,
                finish: choice.finish_reason,
                engine,
                contentType: msg.content == null ? 'null' : typeof msg.content,
                msgKeys: Object.keys(msg).slice(0, 12),
                error: parseErr
            });
            lastError = Object.assign(
                new Error(parseErr || 'Hack Club AI returned an empty response'),
                { code: parseErr && /timed out/i.test(parseErr) ? 'HACKCLUB_TIMEOUT' : 'HACKCLUB_EMPTY' }
            );
        } catch (e) {
            if (e.code === 'HACKCLUB_RATE_LIMITED' || e.code === 'HACKCLUB_NOT_CONFIGURED') throw e;
            if (e.code && String(e.code).startsWith('HACKCLUB_')) {
                lastError = e;
                continue;
            }
            lastError = Object.assign(new Error(e.message || 'Hack Club AI request failed'), {
                code: e.code === 'ECONNABORTED' ? 'HACKCLUB_TIMEOUT' : 'HACKCLUB_ERROR',
                status: e.response?.status
            });
        }
    }

    throw lastError || Object.assign(new Error('Hack Club AI returned an empty response'), { code: 'HACKCLUB_EMPTY' });
}

module.exports = {
    hackClubChatCompletion,
    extractAssistantText,
    toHackClubMessages,
    getHackClubKey,
    getHackClubModel,
    getHackClubJsonModel,
    JSON_MUST,
    DEFAULT_MODEL,
    DEFAULT_JSON_MODEL
};
