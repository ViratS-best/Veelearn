'use strict';

/**
 * Question bank access for AI sessions.
 *
 * Selection only — questions are authored/generated offline by
 * `build_session_seed.py` and verified before they reach the database, so a
 * session never waits on content generation.
 *
 * Security note: `toCard()` is the only shape that reaches the browser and it
 * deliberately omits `answer` and every distractor `why`. Those are released by
 * the session engine after grading.
 */

function parseJson(value, fallback) {
    if (value == null) return fallback;
    if (typeof value === 'object') return value;
    try {
        const parsed = JSON.parse(String(value));
        return parsed == null ? fallback : parsed;
    } catch (_) {
        return fallback;
    }
}

function createQBank({ query }) {
    /**
     * Client-safe question card. No answer key, no distractor rationales.
     */
    function toCard(row) {
        if (!row) return null;
        const options = parseJson(row.options, []).map((o) => ({ k: o.k, t: o.t }));
        return {
            id: Number(row.id),
            skillId: Number(row.skill_id),
            tier: Number(row.tier),
            type: row.qtype || 'mcq',
            stem: row.stem,
            options,
            hints: parseJson(row.hints, []),
            visual: parseJson(row.visual, null)
        };
    }

    /** Full row, server-side only. */
    async function getRaw(questionId) {
        const rows = await query(
            `SELECT id, skill_id, tier, qtype, stem, options, answer, hints, solution_steps, visual, live
             FROM qbank_items WHERE id = ? LIMIT 1`,
            [questionId]
        );
        return rows[0] || null;
    }

    /** Distractor-specific explanation, released only after a wrong answer. */
    function whyFor(row, answerKey) {
        const options = parseJson(row?.options, []);
        const hit = options.find((o) => String(o.k).toUpperCase() === String(answerKey).toUpperCase());
        return hit && hit.why ? String(hit.why) : '';
    }

    function solutionFor(row) {
        return {
            steps: parseJson(row?.solution_steps, []),
            answer: row?.answer != null ? String(row.answer) : ''
        };
    }

    /**
     * Pick one question for (skill, tier, learner), preferring ones this learner
     * has never attempted, then the best-calibrated item.
     */
    async function pick({ skillId, tier, userId }) {
        const t = Math.min(4, Math.max(1, parseInt(tier, 10) || 1));
        const unseenFirst = `
            SELECT q.id, q.skill_id, q.tier, q.qtype, q.stem, q.options, q.answer,
                   q.hints, q.solution_steps, q.visual
            FROM qbank_items q
            WHERE q.skill_id = ? AND q.tier = ? AND q.live = TRUE
              AND NOT EXISTS (
                  SELECT 1 FROM practice_attempts a
                  WHERE a.user_id = ? AND a.question_id = q.id AND a.correct = TRUE
              )
            ORDER BY q.calibration_p DESC, q.id ASC
            LIMIT 1`;

        let rows = await query(unseenFirst, [skillId, t, userId]);
        if (!rows.length) {
            // Any item at this tier, seen or not.
            rows = await query(
                `SELECT id, skill_id, tier, qtype, stem, options, answer, hints, solution_steps, visual
                 FROM qbank_items
                 WHERE skill_id = ? AND tier = ? AND live = TRUE
                 ORDER BY calibration_p DESC, id ASC
                 LIMIT 1`,
                [skillId, t]
            );
        }
        if (!rows.length) {
            // Tier may be missing for a young skill — walk down, then up.
            const order = t > 1 ? [t - 1, t + 1, 2, 1, 3, 4] : [2, 3, 4];
            for (const alt of order) {
                if (alt < 1 || alt > 4) continue;
                rows = await query(
                    `SELECT id, skill_id, tier, qtype, stem, options, answer, hints, solution_steps, visual
                     FROM qbank_items
                     WHERE skill_id = ? AND tier = ? AND live = TRUE
                     ORDER BY calibration_p DESC, id ASC
                     LIMIT 1`,
                    [skillId, alt]
                );
                if (rows.length) break;
            }
        }
        return rows[0] || null;
    }

    async function listSkills(track) {
        return query(
            `SELECT id, code, track, name, grade_band, prereq_id, order_index, intro_md, misconceptions, dot_target
             FROM skills ${track ? 'WHERE track = ?' : ''}
             ORDER BY track ASC, order_index ASC`,
            track ? [track] : []
        );
    }

    async function getSkill(skillId) {
        const rows = await query(
            'SELECT id, code, track, name, intro_md, misconceptions, dot_target, order_index FROM skills WHERE id = ? LIMIT 1',
            [skillId]
        );
        return rows[0] || null;
    }

    async function getSkillByCode(code) {
        const rows = await query('SELECT id, code, track, name, dot_target FROM skills WHERE code = ? LIMIT 1', [code]);
        return rows[0] || null;
    }

    async function tracks() {
        return query(
            `SELECT track, COUNT(*) AS skills, MIN(order_index) AS ord
             FROM skills GROUP BY track ORDER BY ord ASC`
        );
    }

    async function countForSkill(skillId) {
        const rows = await query('SELECT COUNT(*) AS c FROM qbank_items WHERE skill_id = ? AND live = TRUE', [skillId]);
        return rows[0]?.c || 0;
    }

    return {
        countForSkill,
        getRaw,
        getSkill,
        getSkillByCode,
        listSkills,
        pick,
        solutionFor,
        toCard,
        tracks,
        whyFor
    };
}

module.exports = createQBank;
module.exports.parseJson = parseJson;
