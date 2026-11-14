'use strict';

/**
 * PostgreSQL compatibility layer for the Veelearn API.
 *
 * The application was written against `mysql2`. Instead of rewriting 240+ call
 * sites, this module exposes the same small surface (`db.query(sql, params, cb)`
 * and a promise helper) backed by a single `pg.Pool` capped at PG_POOL_MAX
 * connections (20 by default, matching the Aiven connection limit).
 *
 * Pooling model: every query checks a connection out of the pool, runs, and
 * returns it immediately. Waiting requests queue in the pool instead of opening
 * new connections, so hundreds of concurrent users share the same 20 sockets.
 *
 * It also translates the MySQL-flavoured SQL the codebase uses:
 *   ?          -> $1, $2, ...   (quote-aware)
 *   IFNULL     -> COALESCE
 *   CURDATE()  -> CURRENT_DATE
 *   YEAR(x)    -> EXTRACT(YEAR FROM x)
 *   MONTH(x)   -> EXTRACT(MONTH FROM x)
 *   DATEDIFF(a,b) -> (a::date - b::date)
 *   TRUE/FALSE -> 1/0            (boolean-ish columns are smallint)
 *   INSERT IGNORE ... -> INSERT ... ON CONFLICT DO NOTHING
 *   ON DUPLICATE KEY UPDATE .. VALUES(col) -> ON CONFLICT (uniquecols) DO UPDATE SET .. EXCLUDED.col
 *   AUTO_INCREMENT / ENUM / LONGTEXT / ON UPDATE CURRENT_TIMESTAMP in DDL
 *
 * Result shapes mirror mysql2: SELECT resolves to an array of rows, writes
 * resolve to { insertId, affectedRows }.
 */

const { Pool, types } = require('pg');

// ---------------------------------------------------------------------------
// Result type parsers - keep values looking like mysql2's `dateStrings: true`
// ---------------------------------------------------------------------------
types.setTypeParser(20, (v) => parseInt(v, 10)); // bigint (COUNT(*)) -> number
types.setTypeParser(1114, (v) => v); // timestamp without tz -> string
types.setTypeParser(1184, (v) => v); // timestamptz -> string
types.setTypeParser(1082, (v) => v); // date -> string
types.setTypeParser(1083, (v) => v); // time -> string
types.setTypeParser(114, (v) => v); // json  -> raw string (callers JSON.parse)
types.setTypeParser(3802, (v) => v); // jsonb -> raw string (callers JSON.parse)
types.setTypeParser(1700, (v) => v); // numeric -> string (MySQL DECIMAL behaviour)

// ---------------------------------------------------------------------------
// Pool
// ---------------------------------------------------------------------------
// Aiven PostgreSQL reports max_connections = 20 with superuser_reserved_connections = 3,
// so an ordinary role can only ever hold 17 sockets. Cap the pool at 15 by default:
// that leaves room for psql/console sessions and avoids "too many clients already"
// during a burst. Override with PG_POOL_MAX if the plan limit changes.
const PG_MAX = Number(process.env.PG_POOL_MAX || 15);
const PG_IDLE_MS = Number(process.env.PG_POOL_IDLE_MS || 30000);
const PG_CONNECT_MS = Number(process.env.PG_POOL_CONNECT_MS || 15000);

const ca = (process.env.PGSSL_CA || process.env.DB_SSL_CA || '').replace(/\\n/g, '\n').trim();

const pool = new Pool({
    host: process.env.PGHOST,
    port: Number(process.env.PGPORT || 5432),
    user: process.env.PGUSER,
    password: process.env.PGPASSWORD,
    database: process.env.PG_DATABASE || process.env.PGDATABASE || 'defaultdb',
    max: PG_MAX,
    idleTimeoutMillis: PG_IDLE_MS,
    connectionTimeoutMillis: PG_CONNECT_MS,
    keepAlive: true,
    application_name: 'veelearn-api',
    ssl: ca ? { ca, rejectUnauthorized: false } : { rejectUnauthorized: false },
});

pool.on('error', (err) => {
    console.error('[pg pool] idle client error:', err.message);
});

const stats = { queries: 0, errors: 0, slow: 0 };

// MySQL error codes the application already branches on -> PostgreSQL SQLSTATE.
const PgErrorAsMysql = {
    '23505': 'ER_DUP_ENTRY',
    '23503': 'ER_NO_REFERENCED_ROW_2',
    '23502': 'ER_BAD_NULL_ERROR',
    '42703': 'ER_BAD_FIELD_ERROR',
    '42P01': 'ER_NO_SUCH_TABLE',
    '22001': 'ER_DATA_TOO_LONG',
    '22P02': 'ER_TRUNCATED_WRONG_VALUE',
    '40001': 'ER_LOCK_DEADLOCK',
    '40P01': 'ER_LOCK_DEADLOCK',
};

function withMysqlErrorCode(err) {
    if (!err) return err;
    if (!err.pgCode) err.pgCode = err.code;
    if (PgErrorAsMysql[err.code]) err.code = PgErrorAsMysql[err.code];
    return err;
}

// ---------------------------------------------------------------------------
// Schema metadata: primary key + unique index columns per table.
// Used to turn `ON DUPLICATE KEY UPDATE` into a real `ON CONFLICT (...)`.
// ---------------------------------------------------------------------------
let metaPromise = null;

function ensureMeta() {
    if (!metaPromise) {
        metaPromise = pool
            .query(
                `SELECT t.relname AS tbl,
                        i.indisprimary AS is_pk,
                        (SELECT array_agg(a.attname::text ORDER BY k.ord)
                           FROM unnest(i.indkey) WITH ORDINALITY AS k(attnum, ord)
                           JOIN pg_attribute a ON a.attrelid = t.oid AND a.attnum = k.attnum)::text[] AS cols
                   FROM pg_index i
                   JOIN pg_class t ON t.oid = i.indrelid
                   JOIN pg_namespace n ON n.oid = t.relnamespace
                  WHERE i.indisunique AND n.nspname = current_schema()`
            )
            .then(({ rows }) => {
                const meta = new Map();
                for (const row of rows) {
                    const raw = Array.isArray(row.cols)
                        ? row.cols
                        : String(row.cols || '')
                              .replace(/^\{|\}$/g, '')
                              .split(',');
                    const cols = raw.map((c) => String(c).replace(/"/g, '').trim()).filter(Boolean);
                    if (!cols.length) continue;
                    const entry = meta.get(row.tbl) || { pk: null, uniques: [] };
                    if (row.is_pk) entry.pk = cols;
                    else entry.uniques.push(cols);
                    meta.set(row.tbl, entry);
                }
                return meta;
            })
            .catch((err) => {
                console.error('[pg] could not load schema metadata:', err.message);
                metaPromise = null;
                return new Map();
            });
    }
    return metaPromise;
}

// ---------------------------------------------------------------------------
// SQL translation helpers
// ---------------------------------------------------------------------------

/** Run `fn` on the parts of the SQL that are not inside quotes. */
function mapOutsideQuotes(sql, fn) {
    let out = '';
    let buf = '';
    let quote = null;
    for (let i = 0; i < sql.length; i += 1) {
        const ch = sql[i];
        if (quote) {
            out += ch;
            if (ch === '\\' && quote === "'") {
                out += sql[i + 1] || '';
                i += 1;
            } else if (ch === quote) {
                if (sql[i + 1] === quote) {
                    out += sql[i + 1];
                    i += 1;
                } else {
                    quote = null;
                }
            }
            continue;
        }
        if (ch === "'" || ch === '"' || ch === '`') {
            if (buf) {
                out += fn(buf);
                buf = '';
            }
            quote = ch === '`' ? '"' : ch;
            out += quote;
            continue;
        }
        buf += ch;
    }
    if (buf) out += fn(buf);
    return out;
}

function rewriteScalars(sql) {
    let text = mapOutsideQuotes(sql, (chunk) =>
        chunk
            .replace(/\bIFNULL\s*\(/gi, 'COALESCE(')
            .replace(/\bCURDATE\s*\(\s*\)/gi, 'CURRENT_DATE')
            .replace(/\bDATABASE\s*\(\s*\)/gi, 'current_schema()')
            .replace(/\bYEAR\s*\(([\w.]+)\)/gi, 'EXTRACT(YEAR FROM $1)')
            .replace(/\bMONTH\s*\(([\w.]+)\)/gi, 'EXTRACT(MONTH FROM $1)')
            .replace(/\bDATEDIFF\s*\(\s*NOW\s*\(\s*\)\s*,\s*([\w.]+)\s*\)/gi, '(CURRENT_DATE - $1::date)')
            .replace(/\bDATEDIFF\s*\(\s*([\w.]+)\s*,\s*([\w.]+)\s*\)/gi, '($1::date - $2::date)')
            .replace(/\bSUBSTRING_INDEX\s*\(([^,]+),([^,]+),([^)]+)\)/gi, 'split_part($1,$2,$3)')
            .replace(/\bTRUE\b/gi, '1')
            .replace(/\bFALSE\b/gi, '0')
    );
    return text;
}

function rewriteDdl(sql) {
    let text = sql;
    text = text.replace(/\b(INT|INTEGER)\s+AUTO_INCREMENT\s+PRIMARY\s+KEY\b/gi, 'SERIAL PRIMARY KEY');
    text = text.replace(/\bBIGINT\s+AUTO_INCREMENT\s+PRIMARY\s+KEY\b/gi, 'BIGSERIAL PRIMARY KEY');
    text = text.replace(/\bAUTO_INCREMENT\b/gi, '');
    text = text.replace(/\b(LONG|MEDIUM|TINY)TEXT\b/gi, 'TEXT');
    text = text.replace(/\bENUM\s*\([^)]*\)/gi, 'TEXT');
    text = text.replace(/\bTINYINT\s*\(\s*1\s*\)/gi, 'SMALLINT');
    text = text.replace(/\bTINYINT\b/gi, 'SMALLINT');
    text = text.replace(/\bMEDIUMINT\b/gi, 'INTEGER');
    text = text.replace(/\bDATETIME\b/gi, 'TIMESTAMP');
    text = text.replace(/\bDOUBLE\b/gi, 'DOUBLE PRECISION');
    text = text.replace(/\bUNSIGNED\b/gi, '');
    text = text.replace(/\bBOOLEAN\b/gi, 'SMALLINT');
    text = text.replace(/\bDEFAULT\s+FALSE\b/gi, 'DEFAULT 0');
    text = text.replace(/\bDEFAULT\s+TRUE\b/gi, 'DEFAULT 1');
    text = text.replace(/\s+ON\s+UPDATE\s+CURRENT_TIMESTAMP\b/gi, '');
    // UNIQUE KEY name (a, b) -> CONSTRAINT "name" UNIQUE (a, b)
    text = text.replace(
        /\bUNIQUE\s+(?:KEY|INDEX)\s+(\w+)\s*\(([^)]*)\)/gi,
        'CONSTRAINT "$1" UNIQUE ($2)'
    );
    // plain MySQL secondary index definitions are not valid inside CREATE TABLE
    text = text.replace(/,\s*(?:INDEX|KEY)\s+\w+\s*\([^)]*\)/gi, '');
    text = text.replace(/\b(?:INDEX|KEY)\s+\w+\s*\([^)]*\)/gi, '');
    text = text.replace(/\bENGINE\s*=\s*\w+/gi, '');
    text = text.replace(/\bDEFAULT\s+CHARSET\s*=\s*\w+/gi, '');
    text = text.replace(/\bCOLLATE\s*=\s*\w+/gi, '');
    // MODIFY COLUMN x TYPE NOT NULL DEFAULT ... -> ALTER COLUMN x TYPE TYPE
    // (PostgreSQL does not accept NOT NULL / DEFAULT inside a TYPE clause)
    text = text.replace(/\bMODIFY\s+COLUMN\s+(\w+)\s+([^,;]+)/gi, (m, col, def) => {
        const cleaned = def
            .replace(/\bNOT\s+NULL\b/gi, '')
            .replace(/\bDEFAULT\s+(?:'(?:[^']|'')*'|[^\s,;]+)/gi, '')
            .trim();
        return `ALTER COLUMN ${col} TYPE ${cleaned}`;
    });
    text = text.replace(/\s+AFTER\s+\w+/gi, '');
    text = text.replace(/\s+FIRST\b/gi, '');
    text = text.replace(/\bDATABASE\s*\(\s*\)/gi, 'current_schema()');
    return text;
}

function rewritePlaceholders(sql) {
    let out = '';
    let n = 0;
    let quote = null;
    for (let i = 0; i < sql.length; i += 1) {
        const ch = sql[i];
        if (quote) {
            out += ch;
            if (ch === '\\' && quote === "'") {
                out += sql[i + 1] || '';
                i += 1;
            } else if (ch === quote) {
                if (sql[i + 1] === quote) {
                    out += sql[i + 1];
                    i += 1;
                } else {
                    quote = null;
                }
            }
            continue;
        }
        if (ch === "'" || ch === '"') {
            quote = ch;
            out += ch;
            continue;
        }
        if (ch === '?' && !/\$[0-9]/.test(sql.slice(i, i + 2))) {
            n += 1;
            out += `$${n}`;
            continue;
        }
        out += ch;
    }
    return out;
}

function insertTarget(sql) {
    const m = /^\s*INSERT\s+(?:IGNORE\s+)?INTO\s+"?([a-z_][a-z0-9_]*)"?\s*(?:\(([^)]*)\))?/i.exec(sql);
    if (!m) return null;
    return {
        table: m[1].toLowerCase(),
        columns: m[2]
            ? m[2]
                  .split(',')
                  .map((c) => c.trim().replace(/"/g, '').toLowerCase())
                  .filter(Boolean)
            : null,
    };
}

async function rewriteOnDuplicate(sql) {
    const target = insertTarget(sql);
    if (!target) return sql;
    const meta = await ensureMeta();
    const entry = meta.get(target.table);
    const cols = target.columns || [];

    let conflictCols = null;
    if (entry) {
        const candidates = entry.uniques.filter((u) => u.every((c) => cols.includes(c)));
        if (candidates.length) {
            candidates.sort((a, b) => a.length - b.length);
            conflictCols = candidates[0];
        } else if (entry.pk && entry.pk.every((c) => cols.includes(c))) {
            conflictCols = entry.pk;
        } else {
            conflictCols = entry.pk;
        }
    }
    if (!conflictCols || !conflictCols.length) conflictCols = ['id'];

    const conflict = conflictCols.map((c) => `"${c}"`).join(', ');
    const idx = sql.search(/ON\s+DUPLICATE\s+KEY\s+UPDATE/i);
    const head = sql.slice(0, idx);
    let updates = sql.slice(idx).replace(/ON\s+DUPLICATE\s+KEY\s+UPDATE/i, '').trim();
    updates = updates.replace(/VALUES\s*\(\s*([\w.]+)\s*\)/gi, 'EXCLUDED."$1"');
    return `${head}ON CONFLICT (${conflict}) DO UPDATE SET ${updates}`;
}

async function toPostgres(sql) {
    let text = String(sql);
    const isDdl = /^\s*(CREATE|ALTER|DROP)\s+(TABLE|INDEX|VIEW|DATABASE)\b/i.test(text);
    if (isDdl) text = rewriteDdl(text);
    // Runs before quote splitting because the separator itself is a quoted string.
    text = text.replace(
        /\bSUBSTRING_INDEX\s*\(\s*([\w.]+)\s*,\s*'([^']*)'\s*,\s*(-?\d+)\s*\)/gi,
        "split_part($1, '$2', $3)"
    );
    text = rewriteScalars(text);

    if (/^\s*INSERT\s+IGNORE\b/i.test(text)) {
        text = text.replace(/^\s*INSERT\s+IGNORE/i, 'INSERT') + ' ON CONFLICT DO NOTHING';
    }
    if (/ON\s+DUPLICATE\s+KEY/i.test(text)) {
        text = await rewriteOnDuplicate(text);
    }
    return rewritePlaceholders(text);
}

function isWrite(text) {
    return /^\s*(INSERT|UPDATE|DELETE)\b/i.test(text);
}

async function runQuery(sql, params = []) {
    const started = Date.now();
    let text;
    try {
        text = await toPostgres(sql);
    } catch (err) {
        stats.errors += 1;
        throw withMysqlErrorCode(err);
    }

    let finalText = text;
    let returningCol = null;
    if (/^\s*INSERT\b/i.test(text) && !/\bRETURNING\b/i.test(text)) {
        const target = insertTarget(text);
        if (target) {
            const meta = await ensureMeta();
            const pk = meta.get(target.table)?.pk;
            if (pk && pk.length === 1) {
                finalText = `${text} RETURNING "${pk[0]}"`;
                returningCol = pk[0];
            }
        }
    }

    // mysql2 converts JS booleans to 1/0 for tinyint/smallint columns; pg would send
    // a real boolean and fail against smallint, so normalise here.
    // mysql2 converts JS booleans to 1/0 for smallint columns; pg would send a real
    // boolean and the insert would fail, so normalise params here.
    const values = (Array.isArray(params) ? params : []).map((v) => {
        if (v === true) return 1;
        if (v === false) return 0;
        if (v === undefined) return null;
        return v;
    });

    try {
        const result = await pool.query(finalText, values);
        stats.queries += 1;
        const ms = Date.now() - started;
        if (ms > 2000) stats.slow += 1;
        if (isWrite(text)) {
            const header = { affectedRows: result.rowCount, insertId: 0, rows: result.rows };
            if (returningCol && result.rows[0]) header.insertId = result.rows[0][returningCol];
            return header;
        }
        return result.rows;
    } catch (err) {
        stats.errors += 1;
        withMysqlErrorCode(err);
        err.sql = finalText;
        throw err;
    }
}

/** mysql2-style `db.query(sql, [params], cb)`; returns a promise when no callback. */
function queryCompat(sql, params, cb) {
    let values = params;
    let callback = cb;
    if (typeof params === 'function') {
        callback = params;
        values = [];
    }
    const promise = runQuery(sql, values || []);
    if (typeof callback === 'function') {
        promise.then((result) => callback(null, result), (err) => callback(err));
        return undefined;
    }
    return promise;
}

const db = {
    query: queryCompat,
    // mysql2 helpers occasionally used by callers
    escape: (value) => `'${String(value).replace(/'/g, "''")}'`,
    pool,
};

const query = (sql, params = []) => runQuery(sql, params);

async function healthCheck() {
    const started = Date.now();
    await pool.query('SELECT 1');
    return { ok: true, ms: Date.now() - started };
}

function poolStatus() {
    return {
        max: PG_MAX,
        total: pool.totalCount,
        idle: pool.idleCount,
        waiting: pool.waitingCount,
        queries: stats.queries,
        errors: stats.errors,
        slowQueries: stats.slow,
    };
}

async function close() {
    await pool.end();
}

module.exports = { db, query, pool, healthCheck, poolStatus, close, toPostgres };
