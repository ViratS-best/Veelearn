'use strict';

/**
 * Retention and the storage budget.
 *
 * The design sets a hard budget: Postgres working set under 300 MB, an alarm at
 * 240 MB and auto-tighten at 270 MB. Nothing here needs a nightly job runner —
 * one pass on boot plus a daily timer inside the same process is enough for a
 * single-instance API, and every window is generous enough that pruning is never
 * visible to a learner mid-session.
 *
 * Windows
 *   session_events     180 days   the audit trail of what happened in a session
 *   practice_attempts  365 days   per-question history (mastery keeps the summary)
 *   session_summaries  365 days   the text a learner sees after a session
 *   llm_cache           90 days   cached model output
 */

const WINDOWS = {
    session_events: 180,
    practice_attempts: 365,
    session_summaries: 365,
    llm_cache: 90
};

const ALARM_MB = 240;
const TIGHTEN_MB = 270;

async function dbSizeMb(query) {
    try {
        const rows = await query('SELECT pg_database_size(current_database()) AS bytes');
        const bytes = Number(rows[0] && rows[0].bytes);
        if (!Number.isFinite(bytes) || bytes <= 0) return null;
        return Math.round(bytes / 1048576);
    } catch (_) {
        return null;
    }
}

/**
 * One pruning pass.
 * @returns {Promise<{deleted:Object<string,number>, sizeMb:number|null}>}
 */
async function runRetention({ query, log } = {}) {
    const info = (log && log.info) || (() => {});
    const warn = (log && log.warn) || (() => {});
    const deleted = {};

    for (const [table, days] of Object.entries(WINDOWS)) {
        try {
            const res = await query(`DELETE FROM ${table} WHERE created_at < NOW() - INTERVAL '${days} days'`);
            const count = (res && res.affectedRows) || 0;
            deleted[table] = count;
        } catch (e) {
            // A table that does not exist yet is not an error worth waking anyone for.
            deleted[table] = -1;
        }
    }

    const sizeMb = await dbSizeMb(query);
    if (sizeMb != null) {
        if (sizeMb >= TIGHTEN_MB) {
            warn(`[retention] database is ${sizeMb} MB — over ${TIGHTEN_MB} MB, tightening windows`);
            // Tighten the cheapest-to-lose table first: cached model output.
            try {
                await query("DELETE FROM llm_cache WHERE created_at < NOW() - INTERVAL '30 days'");
            } catch (_) {
                /* nothing cached */
            }
        } else if (sizeMb >= ALARM_MB) {
            warn(`[retention] database is ${sizeMb} MB — over the ${ALARM_MB} MB alarm line`);
        } else {
            info(`[retention] database ${sizeMb} MB (budget ${ALARM_MB} MB)`);
        }
    }

    return { deleted, sizeMb };
}

/** Run once now, then daily for as long as the process lives. */
function scheduleRetention(deps, { hours = 24 } = {}) {
    const timer = setInterval(() => {
        runRetention(deps).catch(() => {});
    }, Math.max(1, hours) * 3600 * 1000);
    if (typeof timer.unref === 'function') timer.unref();
    return timer;
}

module.exports = { runRetention, scheduleRetention, dbSizeMb, WINDOWS, ALARM_MB, TIGHTEN_MB };
