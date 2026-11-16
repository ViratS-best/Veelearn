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
            visual: parseJson(row.visual, null),
            // Where the question came from, so a session can say so in plain
            // language. Not sensitive: it is the same line the creator saw.
            source: row.source || 'authored',
            attribution: row.attribution || ''
        };
    }

    const LETTERS = ['A', 'B', 'C', 'D', 'E', 'F'];

    /**
     * Deterministic Fisher-Yates. Seeded by the question id so the same row keeps
     * the same order across requests, which is what makes the repair idempotent.
     */
    function shuffledOptions(options, seed) {
        const list = options.slice();
        let s = (Number(seed) || 1) % 4294967296;
        const rand = () => {
            s = (s * 1103515245 + 12345) % 2147483648;
            return s / 2147483648;
        };
        for (let i = list.length - 1; i > 0; i -= 1) {
            const j = Math.floor(rand() * (i + 1));
            const tmp = list[i];
            list[i] = list[j];
            list[j] = tmp;
        }
        return list;
    }

    /**
     * Full row, server-side only.
     *
     * A bank built from creator quizzes tends to put the correct choice first, so
     * every card read "the answer is A". The first time such a row is served its
     * options are shuffled and the key rewritten; every later read is consistent.
     */
    async function getRaw(questionId) {
        const rows = await query(
            `SELECT id, skill_id, tier, qtype, stem, options, answer, hints, solution_steps, visual, live,
                    source, attribution
             FROM qbank_items WHERE id = ? LIMIT 1`,
            [questionId]
        );
        const row = rows[0];
        if (!row) return null;
        const options = parseJson(row.options, []);
        const key = String(row.answer == null ? '' : row.answer).trim().toUpperCase();
        if (Array.isArray(options) && options.length >= 3 && options[0] && options[0].k === key) {
            const mixed = shuffledOptions(options, row.id);
            const correctText = (options.find((o) => o.k === key) || {}).t;
            // A shuffle that happens to leave the key first is exactly the bug the
            // learner reported, so move it off the first slot on purpose.
            let at = mixed.findIndex((o) => o.t === correctText);
            if (at === 0) {
                const moveTo = 1 + (Number(row.id) % (mixed.length - 1));
                const tmp = mixed[0];
                mixed[0] = mixed[moveTo];
                mixed[moveTo] = tmp;
                at = moveTo;
            }
            const remapped = mixed.map((o, i) => Object.assign({}, o, { k: LETTERS[i] }));
            const newKey = remapped[at] ? remapped[at].k : LETTERS[0];
            try {
                await query('UPDATE qbank_items SET options = ?, answer = ? WHERE id = ?', [
                    JSON.stringify(remapped),
                    newKey,
                    row.id
                ]);
                row.options = remapped;
                row.answer = newKey;
            } catch (_) {
                /* serving an unshuffled row beats failing the card */
            }
        }
        return row;
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
                   q.hints, q.solution_steps, q.visual, q.source, q.attribution
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
                `SELECT id, skill_id, tier, qtype, stem, options, answer, hints, solution_steps, visual,
                        source, attribution
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
                    `SELECT id, skill_id, tier, qtype, stem, options, answer, hints, solution_steps, visual,
                            source, attribution
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

    /**
     * The next card for a skill that has not been served in this session yet.
     * Course-seeded units can be small, and qbank.pick can legitimately hand
     * back the card that was just answered; this keeps the learner moving.
     */
    async function pickUnserved({ skillId, exclude }) {
        const ids = (exclude || []).map(Number).filter((n) => n > 0);
        const notIn = ids.length ? `AND q.id NOT IN (${ids.map(() => '?').join(',')})` : '';
        const rows = await query(
            `SELECT q.id, q.skill_id, q.tier, q.qtype, q.stem, q.options, q.answer,
                    q.hints, q.solution_steps, q.visual, q.source, q.attribution
             FROM qbank_items q
             WHERE q.skill_id = ? AND q.live = TRUE ${notIn}
             ORDER BY q.tier ASC, q.calibration_p DESC, q.id ASC
             LIMIT 1`,
            [skillId, ...ids]
        );
        return rows[0] || null;
    }

    return {
        countForSkill,
        getRaw,
        getSkill,
        getSkillByCode,
        listSkills,
        pick,
        pickUnserved,
        solutionFor,
        toCard,
        shuffledOptions,
        tracks,
        whyFor
    };
}

module.exports = createQBank;
module.exports.parseJson = parseJson;
