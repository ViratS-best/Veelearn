'use strict';

/**
 * Semantic search for the question bank.
 *
 * Embeddings come from the same Hack Club AI account as every other model call:
 * `POST https://ai.hackclub.com/proxy/v1/embeddings` with
 * `openai/text-embedding-3-small` at 512 dimensions. Vectors are stored in
 * `qbank_items.embedding` as `halfvec(512)` (half the bytes of `vector`), with an
 * HNSW cosine index for nearest-neighbour search.
 *
 * `embedding_hash` is the fingerprint of the exact text that was embedded, so a
 * question that is edited (stem, skill, answer) is detected as stale and
 * re-embedded instead of silently keeping an old vector.
 *
 * Everything degrades to keyword search: if the extension, the key or the
 * network is unavailable, `embedQuery` returns null and the caller keeps its
 * existing SQL path.
 */

const crypto = require('crypto');
const hackclub = require('./hackclub-ai');

const EMBED_MODEL = String(process.env.VEELEARN_EMBED_MODEL || '').trim() || 'cohere/embed-5-fast';
const EMBED_DIMS = Number(process.env.VEELEARN_EMBED_DIMS || 512);
const EMBED_URL = String(
    process.env.HACKCLUBAI_EMBEDDINGS_URL || 'https://ai.hackclub.com/proxy/v1/embeddings'
).trim();
const MAX_TEXT = 2000;
const BATCH = Math.max(1, Math.min(96, Number(process.env.VEELEARN_EMBED_BATCH || 50)));

let ctx = { query: null, log: null };
const state = {
    checked: false,
    ready: false,
    column: 'halfvec(512)',
    halfvec: true,
    extension: '',
    error: '',
    lastIndexAt: 0
};
const queryCache = new Map();
const queue = new Set();
let queueTimer = null;
let draining = false;
let autoTimer = null;

function configure({ query, log } = {}) {
    if (query) ctx.query = query;
    if (log) ctx.log = log;
    return api;
}

const info = (m) => ctx.log && ctx.log.info && ctx.log.info(m);
const warn = (m) => ctx.log && ctx.log.warn && ctx.log.warn(m);

function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}

/* ------------------------------------------------------------------ schema */

let lastSchemaTry = 0;

async function ensureSchema() {
    if (!ctx.query) return state;
    if (state.checked && state.ready) return state;
    // A missing extension will not appear between two requests; retry every
    // five minutes instead of on every search.
    if (state.checked && Date.now() - lastSchemaTry < 5 * 60 * 1000) return state;
    state.checked = true;
    lastSchemaTry = Date.now();
    try {
        await ctx.query('CREATE EXTENSION IF NOT EXISTS vector');
    } catch (err) {
        state.error = `pgvector unavailable: ${err.message}`;
        state.ready = false;
        warn(`[embeddings] ${state.error}`);
        return state;
    }

    try {
        const ext = await ctx.query(`SELECT extversion FROM pg_extension WHERE extname = 'vector' LIMIT 1`);
        state.extension = (ext[0] && ext[0].extversion) || '';
    } catch (_) {
        state.extension = '';
    }

    // halfvec arrived in pgvector 0.7; an older install still gets vectors, just
    // at float4 storage.
    try {
        await ctx.query('ALTER TABLE qbank_items ADD COLUMN IF NOT EXISTS embedding halfvec(512)');
        state.column = 'halfvec(512)';
        state.halfvec = true;
    } catch (err) {
        warn(`[embeddings] halfvec unavailable (${err.message}); using vector(512)`);
        try {
            await ctx.query('ALTER TABLE qbank_items ADD COLUMN IF NOT EXISTS embedding vector(512)');
            state.column = 'vector(512)';
            state.halfvec = false;
        } catch (err2) {
            state.error = `embedding column unavailable: ${err2.message}`;
            state.ready = false;
            return state;
        }
    }

    try {
        await ctx.query('ALTER TABLE qbank_items ADD COLUMN IF NOT EXISTS embedding_hash TEXT');
    } catch (err) {
        state.error = `embedding_hash unavailable: ${err.message}`;
        state.ready = false;
        return state;
    }

    state.ready = true;
    info(`[embeddings] ready: pgvector ${state.extension || 'unknown'}, ${state.column}`);
    return state;
}

/** Bulk-loading 48k rows is several times faster without index maintenance. */
async function dropIndex() {
    await ensureSchema();
    if (!state.ready) return { ok: false, error: state.error };
    try {
        await ctx.query('DROP INDEX IF EXISTS qbank_items_embedding_hnsw');
        return { ok: true, dropped: 'qbank_items_embedding_hnsw' };
    } catch (err) {
        return { ok: false, error: err.message };
    }
}

async function ensureIndex() {
    await ensureSchema();
    if (!state.ready) return { ok: false, error: state.error };
    const ops = state.halfvec ? 'halfvec_cosine_ops' : 'vector_cosine_ops';
    try {
        await ctx.query(
            `CREATE INDEX IF NOT EXISTS qbank_items_embedding_hnsw
             ON qbank_items USING hnsw (embedding ${ops})`
        );
        state.lastIndexAt = Date.now();
        return { ok: true, index: 'qbank_items_embedding_hnsw' };
    } catch (err) {
        return { ok: false, error: err.message };
    }
}

/* -------------------------------------------------------------- embeddings */

function getKey() {
    try {
        return hackclub.getHackClubKey();
    } catch (_) {
        return '';
    }
}

function toVectorLiteral(vector) {
    return `[${vector.map((n) => Number(n.toFixed(6))).join(',')}]`;
}

function normaliseVector(vector) {
    let v = vector.slice(0, EMBED_DIMS);
    if (v.length < EMBED_DIMS) return null;
    const norm = Math.sqrt(v.reduce((n, x) => n + x * x, 0)) || 1;
    v = v.map((x) => x / norm);
    return v;
}

async function requestEmbeddings(texts, { withDimensions = true, model = EMBED_MODEL } = {}) {
    const key = getKey();
    if (!key) throw Object.assign(new Error('Hack Club AI is not configured'), { code: 'EMBED_NO_KEY' });
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 30000);
    try {
        const body = { model, input: texts };
        if (withDimensions) body.dimensions = EMBED_DIMS;
        const res = await fetch(EMBED_URL, {
            method: 'POST',
            headers: {
                authorization: `Bearer ${key}`,
                'content-type': 'application/json'
            },
            body: JSON.stringify(body),
            signal: controller.signal
        });
        const data = await res.json().catch(() => null);
        if (!res.ok) {
            const message = (data && (data.error?.message || data.message)) || `HTTP ${res.status}`;
            const err = new Error(message);
            err.status = res.status;
            err.body = data;
            throw err;
        }
        const rows = Array.isArray(data && data.data) ? data.data : [];
        const vectors = rows.map((row) => (Array.isArray(row.embedding) ? row.embedding : null));
        if (vectors.length !== texts.length || vectors.some((v) => !v || !v.length)) {
            throw new Error('the embeddings response was incomplete');
        }
        return vectors.map((v) => {
            const n = normaliseVector(v);
            if (!n) throw new Error(`expected ${EMBED_DIMS} dimensions, got ${v.length}`);
            return n;
        });
    } finally {
        clearTimeout(timer);
    }
}

/**
 * Embed many strings. A proxy that rejects `dimensions` is retried without it and
 * the vector is truncated + renormalised (Matryoshka truncation for the v3
 * models), so the column stays 512 wide either way.
 */
async function embedBatch(chunk, model = EMBED_MODEL) {
    for (let attempt = 0; attempt < 4; attempt += 1) {
        try {
            try {
                return await requestEmbeddings(chunk, { model });
            } catch (err) {
                if (err.status === 400 && /dimension/i.test(String(err.message))) {
                    return await requestEmbeddings(chunk, { withDimensions: false });
                }
                throw err;
            }
        } catch (err) {
            const retryable = err.status === 429 || (err.status >= 500 && err.status < 600) || err.name === 'AbortError';
            if (!retryable || attempt === 3) throw err;
            await sleep(1200 * (attempt + 1));
        }
    }
    return [];
}

async function embedTexts(texts) {
    const list = (texts || []).map((t) => String(t || '').slice(0, MAX_TEXT));
    if (!list.length) return [];
    const starts = [];
    for (let i = 0; i < list.length; i += BATCH) starts.push(i);
    const out = new Array(list.length);
    let next = 0;
    // Several requests in flight: the proxy's latency, not the row writes, is the
    // bottleneck for a 48k backfill. Order is preserved through `starts`.
    const width = Math.max(1, Math.min(8, Number(process.env.VEELEARN_EMBED_CONCURRENCY || 6)));
    const worker = async () => {
        while (next < starts.length) {
            const start = starts[next++];
            const vectors = await embedBatch(list.slice(start, start + BATCH));
            vectors.forEach((vector, k) => {
                out[start + k] = vector;
            });
        }
    };
    await Promise.all(Array.from({ length: Math.min(width, starts.length) }, worker));
    return out;
}

/**
 * Try a candidate model without writing anything: lets a model switch be
 * verified before the bank is re-embedded into a different vector space.
 */
async function probe({ model, text } = {}) {
    const use = String(model || '').trim() || EMBED_MODEL;
    const started = Date.now();
    try {
        const [vector] = await requestEmbeddings([String(text || '').slice(0, MAX_TEXT) || 'test'], { model: use });
        return { ok: true, model: use, dims: vector.length, requested: EMBED_DIMS, ms: Date.now() - started };
    } catch (err) {
        return { ok: false, model: use, error: err.message, status: err.status || null, ms: Date.now() - started };
    }
}

/** Text that is embedded: question, its topic and its answer. */
function questionText(row) {
    const stem = String(row.stem || '').replace(/\s+/g, ' ').trim();
    if (!stem) return '';
    let options = row.options;
    if (typeof options === 'string') {
        try {
            options = JSON.parse(options);
        } catch (_) {
            options = [];
        }
    }
    const key = String(row.answer == null ? '' : row.answer).trim().toUpperCase();
    const hit = Array.isArray(options) ? options.find((o) => String(o && o.k).toUpperCase() === key) : null;
    const answerText = hit && hit.t ? String(hit.t).replace(/\s+/g, ' ').trim() : '';
    const topic = [row.skill_name || row.skill || '', row.track || ''].filter(Boolean).join(' · ');
    return [
        stem,
        topic ? `Topic: ${topic}` : '',
        answerText ? `Answer: ${answerText}` : ''
    ]
        .filter(Boolean)
        .join('\n')
        .slice(0, MAX_TEXT);
}

function hashText(text) {
    return crypto.createHash('sha256').update(`${EMBED_MODEL}|${EMBED_DIMS}|${text}`).digest('hex');
}

function toHalfVecParam(vector) {
    return toVectorLiteral(vector);
}

/* --------------------------------------------------------------- querying */

async function embedQuery(text) {
    const q = String(text || '').trim();
    if (!q) return null;
    // No key means no network call, which keeps tests and local keyword-only
    // setups fast.
    if (!getKey()) return null;
    const cacheKey = q.toLowerCase();
    const cached = queryCache.get(cacheKey);
    if (cached && cached.expiresAt > Date.now()) return cached.value;
    await ensureSchema();
    if (!state.ready) return null;
    try {
        const [vector] = await embedTexts([q]);
        if (!vector) return null;
        const value = toVectorLiteral(vector);
        queryCache.set(cacheKey, { value, expiresAt: Date.now() + 60 * 60 * 1000 });
        if (queryCache.size > 250) {
            const oldest = queryCache.keys().next().value;
            queryCache.delete(oldest);
        }
        return value;
    } catch (err) {
        warn(`[embeddings] query failed: ${err.message}`);
        return null;
    }
}

/* --------------------------------------------------------------- backfill */

async function rowsPage({ afterId = 0, limit = 128, mode = 'missing' } = {}) {
    const cols = `q.id, q.stem, q.options, q.answer, q.embedding_hash, s.name AS skill_name, s.track`;
    const from = `FROM qbank_items q LEFT JOIN skills s ON s.id = q.skill_id`;
    if (mode === 'stale') {
        return ctx.query(
            `SELECT ${cols} ${from}
             WHERE q.live = 1 AND q.id > ? AND q.embedding IS NOT NULL
             ORDER BY q.id ASC LIMIT ?`,
            [afterId, limit]
        );
    }
    return ctx.query(
        `SELECT ${cols} ${from}
         WHERE q.live = 1 AND q.id > ? AND (q.embedding IS NULL OR q.embedding_hash IS NULL)
         ORDER BY q.id ASC LIMIT ?`,
        [afterId, limit]
    );
}

async function writeEmbeddings(rows) {
    const prepared = [];
    for (const row of rows) {
        const text = questionText(row);
        if (!text) continue;
        prepared.push({ row, text, hash: hashText(text) });
    }
    if (!prepared.length) return 0;
    const vectors = await embedTexts(prepared.map((p) => p.text));
    let written = 0;
    // One UPDATE per row: the vector is a halfvec literal, and keeping the cast
    // on a single parameter avoids the integer/halfvec ambiguity of VALUES.
    for (let i = 0; i < prepared.length; i += 1) {
        const { row, hash } = prepared[i];
        const vector = vectors[i];
        if (!vector) continue;
        await ctx.query(
            `UPDATE qbank_items SET embedding = ?::${state.column}, embedding_hash = ? WHERE id = ?`,
            [toHalfVecParam(vector), hash, Number(row.id)]
        );
        written += 1;
    }
    return written;
}

async function backfill({ afterId = 0, limit = 128, mode = 'missing' } = {}) {
    await ensureSchema();
    if (!state.ready) return { ok: false, error: state.error, embedded: 0, nextId: afterId, remaining: 0 };
    const pageSize = Math.max(1, Math.min(512, Number(limit) || 128));
    const rows = await rowsPage({ afterId: Number(afterId) || 0, limit: pageSize, mode });
    let toEmbed = rows;
    if (mode === 'stale') {
        toEmbed = rows.filter((row) => hashText(questionText(row)) !== String(row.embedding_hash || ''));
    }
    const embedded = await writeEmbeddings(toEmbed);
    const nextId = rows.length ? Number(rows[rows.length - 1].id) : Number(afterId) || 0;
    const counts = await progress();
    return {
        ok: true,
        mode,
        scanned: rows.length,
        embedded,
        skipped: rows.length - toEmbed.length,
        nextId,
        remaining: counts.missing,
        total: counts.total
    };
}

async function progress() {
    await ensureSchema();
    let total = 0;
    let embedded = 0;
    let missing = 0;
    if (ctx.query) {
        try {
            const rows = await ctx.query(
                `SELECT COUNT(*) AS total,
                        COUNT(embedding) AS embedded,
                        COUNT(*) FILTER (WHERE embedding IS NULL) AS missing
                   FROM qbank_items WHERE live = 1`
            );
            const row = rows[0] || {};
            total = Number(row.total || 0);
            embedded = Number(row.embedded || 0);
            missing = Number(row.missing || 0);
        } catch (err) {
            state.error = err.message;
        }
    }
    return {
        total,
        embedded,
        missing,
        model: EMBED_MODEL,
        dims: EMBED_DIMS,
        column: state.column,
        extension: state.extension,
        ready: state.ready,
        error: state.error
    };
}

/* ------------------------------------------------- created / edited rows */

/**
 * Queue question ids for an immediate embedding. The drain runs in the
 * background, so a creator saving an outline never waits on the embeddings API.
 */
function queueQuestions(ids) {
    for (const id of ids || []) {
        const n = Number(id);
        if (n > 0) queue.add(n);
    }
    if (!queue.size || queueTimer) return queue.size;
    queueTimer = setTimeout(() => {
        queueTimer = null;
        drain().catch((err) => warn(`[embeddings] queue drain failed: ${err.message}`));
    }, 800);
    if (queueTimer.unref) queueTimer.unref();
    return queue.size;
}

async function drain() {
    if (draining || !ctx.query) return 0;
    draining = true;
    let written = 0;
    try {
        await ensureSchema();
        if (!state.ready) return 0;
        const ids = [...queue].slice(0, 32);
        ids.forEach((id) => queue.delete(id));
        if (!ids.length) return 0;
        const rows = await ctx.query(
            `SELECT q.id, q.stem, q.options, q.answer, q.embedding_hash, s.name AS skill_name, s.track
               FROM qbank_items q LEFT JOIN skills s ON s.id = q.skill_id
              WHERE q.id IN (${ids.map(() => '?').join(',')}) AND q.live = 1`,
            ids
        );
        written = await writeEmbeddings(rows);
        if (queue.size) queueQuestions([]); // schedule the next batch
    } catch (err) {
        warn(`[embeddings] ${err.message}`);
    } finally {
        draining = false;
    }
    return written;
}

/**
 * Periodic drift sweep: catches seed inserts, bulk edits and anything written by
 * a path that does not call `queueQuestions`. It is small per tick so it never
 * competes with a session.
 */
function startAutoSync({ intervalMs = 10 * 60 * 1000, perTick = 64 } = {}) {
    if (autoTimer) return autoTimer;
    autoTimer = setInterval(async () => {
        try {
            await ensureSchema();
            if (!state.ready) return;
            const counts = await progress();
            if (!counts.missing) return;
            const page = await backfill({ afterId: 0, limit: perTick, mode: 'missing' });
            if (page.embedded) info(`[embeddings] auto-sync embedded ${page.embedded}, ${page.remaining} left`);
        } catch (err) {
            warn(`[embeddings] auto-sync failed: ${err.message}`);
        }
    }, intervalMs);
    if (autoTimer.unref) autoTimer.unref();
    return autoTimer;
}

const api = {
    EMBED_DIMS,
    EMBED_MODEL,
    backfill,
    configure,
    drain,
    dropIndex,
    probe,
    embedQuery,
    embedTexts,
    ensureIndex,
    ensureSchema,
    hashText,
    progress,
    queueQuestions,
    questionText,
    startAutoSync,
    state,
    toVectorLiteral
};

module.exports = api;
