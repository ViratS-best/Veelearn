'use strict';

/**
 * Schema + seed for AI learning sessions (Phase 1).
 *
 * Everything here is additive: the 40+ existing tables are untouched. The DDL is
 * written in the same MySQL-flavoured dialect the rest of server.js uses, because
 * `db.js` rewrites it for Postgres (SERIAL, TEXT, SMALLINT booleans, UNIQUE keys).
 *
 * JSON-shaped columns are LONGTEXT on purpose — same convention as
 * `courses.blocks` and `courses.gamification_json`, and it avoids json/jsonb
 * casting differences between the two dialects.
 */

const fs = require('fs');
const path = require('path');

const SEED_PATH = path.join(__dirname, 'seed', 'session_seed.json');

const TABLES = [
    `CREATE TABLE IF NOT EXISTS skills (
        id INT AUTO_INCREMENT PRIMARY KEY,
        code VARCHAR(64) NOT NULL,
        track VARCHAR(48) NOT NULL,
        name VARCHAR(160) NOT NULL,
        grade_band SMALLINT,
        prereq_id INT NULL,
        order_index INT DEFAULT 0,
        dot_target SMALLINT DEFAULT 2,
        intro_md LONGTEXT NULL,
        misconceptions LONGTEXT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE KEY uniq_skill_code (code),
        INDEX idx_skill_track (track, order_index)
    )`,

    `CREATE TABLE IF NOT EXISTS skill_edges (
        id INT AUTO_INCREMENT PRIMARY KEY,
        from_skill INT NOT NULL,
        to_skill INT NOT NULL,
        kind VARCHAR(16) DEFAULT 'requires',
        UNIQUE KEY uniq_skill_edge (from_skill, to_skill)
    )`,

    `CREATE TABLE IF NOT EXISTS qbank_items (
        id INT AUTO_INCREMENT PRIMARY KEY,
        skill_id INT NOT NULL,
        tier SMALLINT NOT NULL DEFAULT 1,
        qtype VARCHAR(16) DEFAULT 'mcq',
        stem LONGTEXT NOT NULL,
        stem_hash CHAR(64) NOT NULL,
        options LONGTEXT NULL,
        answer VARCHAR(64) NOT NULL,
        hints LONGTEXT NULL,
        solution_steps LONGTEXT NULL,
        visual LONGTEXT NULL,
        source VARCHAR(16) DEFAULT 'authored',
        attribution VARCHAR(200) NULL,
        course_id INT NULL,
        calibration_p REAL DEFAULT 0.5,
        seen_count INT DEFAULT 0,
        live SMALLINT DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE KEY uniq_qbank_hash (stem_hash),
        INDEX idx_qbank_pick (skill_id, tier, calibration_p)
    )`,

    `CREATE TABLE IF NOT EXISTS course_skills (
        id INT AUTO_INCREMENT PRIMARY KEY,
        course_id INT NOT NULL,
        skill_id INT NOT NULL,
        weight REAL DEFAULT 1,
        source VARCHAR(12) DEFAULT 'auto',
        UNIQUE KEY uniq_course_skill (course_id, skill_id)
    )`,

    `CREATE TABLE IF NOT EXISTS sessions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        course_id INT NULL,
        mode VARCHAR(16) DEFAULT 'focus',
        intent_text LONGTEXT NULL,
        minutes SMALLINT DEFAULT 20,
        goal_text VARCHAR(160) NULL,
        status VARCHAR(12) DEFAULT 'active',
        item_index SMALLINT DEFAULT 0,
        turn_buffer LONGTEXT NULL,
        xp_awarded INT DEFAULT 0,
        gems_awarded INT DEFAULT 0,
        started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_active_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        ended_at TIMESTAMP NULL,
        INDEX idx_sessions_user (user_id, status, last_active_at)
    )`,

    `CREATE TABLE IF NOT EXISTS session_focus_items (
        id INT AUTO_INCREMENT PRIMARY KEY,
        session_id INT NOT NULL,
        skill_id INT NOT NULL,
        ord SMALLINT NOT NULL DEFAULT 0,
        is_review SMALLINT DEFAULT 0,
        target_dots SMALLINT DEFAULT 2,
        status VARCHAR(12) DEFAULT 'pending',
        correct_count SMALLINT DEFAULT 0,
        attempts SMALLINT DEFAULT 0,
        question_ids LONGTEXT NULL,
        started_at TIMESTAMP NULL,
        completed_at TIMESTAMP NULL,
        UNIQUE KEY uniq_focus_item (session_id, ord),
        INDEX idx_focus_session (session_id, status)
    )`,

    `CREATE TABLE IF NOT EXISTS session_events (
        id INT AUTO_INCREMENT PRIMARY KEY,
        session_id INT NOT NULL,
        seq INT NOT NULL DEFAULT 0,
        kind VARCHAR(24) NOT NULL,
        skill_id INT NULL,
        question_id INT NULL,
        payload LONGTEXT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_events_session (session_id, seq),
        INDEX idx_events_created (created_at)
    )`,

    `CREATE TABLE IF NOT EXISTS practice_attempts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        question_id INT NOT NULL,
        skill_id INT NOT NULL,
        session_id INT NULL,
        correct SMALLINT DEFAULT 0,
        hints SMALLINT DEFAULT 0,
        assistance SMALLINT DEFAULT 0,
        ms_taken INT NULL,
        answer_given VARCHAR(64) NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_attempts_unseen (user_id, question_id),
        INDEX idx_attempts_skill (user_id, skill_id, created_at)
    )`,

    `CREATE TABLE IF NOT EXISTS skill_mastery (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        skill_id INT NOT NULL,
        p REAL DEFAULT 0,
        level SMALLINT DEFAULT 0,
        ease REAL DEFAULT 2.5,
        seen SMALLINT DEFAULT 0,
        correct SMALLINT DEFAULT 0,
        last_seen TIMESTAMP NULL,
        last_level_up_at TIMESTAMP NULL,
        UNIQUE KEY uniq_mastery (user_id, skill_id)
    )`,

    `CREATE TABLE IF NOT EXISTS review_queue (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        skill_id INT NOT NULL,
        due_at TIMESTAMP NOT NULL,
        ease REAL DEFAULT 2.5,
        reps SMALLINT DEFAULT 0,
        verify_independently SMALLINT DEFAULT 0,
        avoided SMALLINT DEFAULT 0,
        UNIQUE KEY uniq_review (user_id, skill_id),
        INDEX idx_review_due (user_id, due_at)
    )`,

    `CREATE TABLE IF NOT EXISTS session_summaries (
        id INT AUTO_INCREMENT PRIMARY KEY,
        session_id INT NOT NULL,
        user_id INT NOT NULL,
        summary VARCHAR(600) NOT NULL,
        skills_touched LONGTEXT NULL,
        next_step VARCHAR(200) NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE KEY uniq_summary_session (session_id)
    )`,

    `CREATE TABLE IF NOT EXISTS skill_pool (
        id INT AUTO_INCREMENT PRIMARY KEY,
        skill_id INT NOT NULL,
        tier SMALLINT NOT NULL,
        live_count INT DEFAULT 0,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE KEY uniq_skill_pool (skill_id, tier)
    )`,

    `CREATE TABLE IF NOT EXISTS llm_cache (
        id INT AUTO_INCREMENT PRIMARY KEY,
        cache_key CHAR(64) NOT NULL,
        kind VARCHAR(16) NOT NULL,
        body LONGTEXT NULL,
        model VARCHAR(64) NULL,
        hits INT DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE KEY uniq_llm_cache (cache_key)
    )`
];

// db.js strips MySQL-style INDEX lines from CREATE TABLE, so hot indexes are
// created explicitly (Postgres syntax, which passes through untouched).
const INDEXES = [
    'CREATE INDEX IF NOT EXISTS idx_skills_track ON skills (track, order_index)',
    'CREATE INDEX IF NOT EXISTS idx_qbank_pick2 ON qbank_items (skill_id, tier, calibration_p)',
    'CREATE INDEX IF NOT EXISTS idx_sessions_user2 ON sessions (user_id, status, last_active_at)',
    'CREATE INDEX IF NOT EXISTS idx_focus_items ON session_focus_items (session_id, status)',
    'CREATE INDEX IF NOT EXISTS idx_events_session2 ON session_events (session_id, seq)',
    'CREATE INDEX IF NOT EXISTS idx_attempts_unseen2 ON practice_attempts (user_id, question_id)',
    'CREATE INDEX IF NOT EXISTS idx_review_due2 ON review_queue (user_id, due_at)'
];

const ALTERS = [
    'ALTER TABLE courses ADD COLUMN IF NOT EXISTS ai_ready SMALLINT DEFAULT 0',
    'ALTER TABLE courses ADD COLUMN IF NOT EXISTS sessions_taught INT DEFAULT 0',
    "ALTER TABLE user_learning_profile ADD COLUMN IF NOT EXISTS prefs LONGTEXT NULL"
];

function loadSeed() {
    if (!fs.existsSync(SEED_PATH)) return null;
    try {
        return JSON.parse(fs.readFileSync(SEED_PATH, 'utf8'));
    } catch (e) {
        return { __error: e.message };
    }
}

/**
 * Create the tables. Safe to call on every boot.
 * @returns {Promise<{ok:boolean, created:number, errors:string[]}>}
 */
async function ensureSessionSchema({ query, log } = {}) {
    const info = (log && log.info) || (() => {});
    const warn = (log && log.warn) || ((m) => console.warn(m));
    const errors = [];
    let created = 0;

    for (const ddl of TABLES) {
        try {
            await query(ddl);
            created += 1;
        } catch (e) {
            errors.push(String(e.message || e));
            warn(`[session-schema] table failed: ${e.message}`);
        }
    }

    for (const idx of INDEXES) {
        try {
            await query(idx);
        } catch (e) {
            if (!/already exists|duplicate/i.test(String(e.message || e))) {
                errors.push(String(e.message || e));
            }
        }
    }

    for (const alter of ALTERS) {
        try {
            await query(alter);
        } catch (e) {
            // Adding a column twice is the normal case on Postgres without
            // IF NOT EXISTS support on older servers; not fatal.
            if (!/already exists|duplicate/i.test(String(e.message || e))) {
                errors.push(String(e.message || e));
            }
        }
    }

    if (!errors.length) info(`[session-schema] ${created} tables ready`);
    return { ok: errors.length === 0, created, errors };
}

/**
 * Load seed/session_seed.json into skills + qbank_items.
 * Idempotent: uses INSERT IGNORE (ON CONFLICT DO NOTHING) and skips entirely
 * once the skill tree exists.
 */
async function seedSessionData({ query, log } = {}) {
    const info = (log && log.info) || (() => {});
    const warn = (log && log.warn) || ((m) => console.warn(m));

    // Materialised counts first: planning uses them to skip skills that have no
    // live item at any tier, and it must stay correct after items are added.
    try {
        await query(
            `INSERT INTO skill_pool (skill_id, tier, live_count)
             SELECT skill_id, tier, COUNT(*) FROM qbank_items WHERE live = 1
             GROUP BY skill_id, tier
             ON CONFLICT (skill_id, tier)
             DO UPDATE SET live_count = EXCLUDED.live_count, updated_at = NOW()`
        );
    } catch (e) {
        warn(`[session-seed] skill pool refresh skipped: ${e.message}`);
    }

    const existing = await query('SELECT COUNT(*) AS c FROM skills');
    const skillCount = Number(existing[0]?.c || 0);
    if (skillCount > 0) {
        const qcount = await query('SELECT COUNT(*) AS c FROM qbank_items');
        info(`[session-seed] already seeded: ${skillCount} skills, ${Number(qcount[0]?.c || 0)} questions`);
        return { seeded: false, skills: skillCount, questions: Number(qcount[0]?.c || 0) };
    }

    const seed = loadSeed();
    if (!seed) {
        warn('[session-seed] no seed/session_seed.json found — run: python build_session_seed.py');
        return { seeded: false, skills: 0, questions: 0 };
    }
    if (seed.__error) {
        warn(`[session-seed] seed file is not valid JSON: ${seed.__error}`);
        return { seeded: false, skills: 0, questions: 0 };
    }

    // ---- skills ---------------------------------------------------------
    for (const s of seed.skills || []) {
        await query(
            `INSERT IGNORE INTO skills (code, track, name, grade_band, order_index, dot_target, intro_md, misconceptions)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
            [
                s.code,
                s.track,
                s.name,
                s.grade_band != null ? s.grade_band : null,
                s.order || 0,
                s.dot_target || 2,
                s.intro_md || null,
                JSON.stringify(s.misconceptions || [])
            ]
        );
    }

    // ---- prerequisite links (needs ids) ---------------------------------
    const idRows = await query('SELECT id, code, prereq_id FROM skills');
    const byCode = new Map(idRows.map((r) => [r.code, Number(r.id)]));
    for (const s of seed.skills || []) {
        if (!s.prereq) continue;
        const selfId = byCode.get(s.code);
        const prereqId = byCode.get(s.prereq);
        if (!selfId || !prereqId) continue;
        await query('UPDATE skills SET prereq_id = ? WHERE id = ?', [prereqId, selfId]);
        try {
            await query('INSERT IGNORE INTO skill_edges (from_skill, to_skill, kind) VALUES (?, ?, ?)', [
                prereqId,
                selfId,
                'requires'
            ]);
        } catch (_) {
            /* edge is informational */
        }
    }

    // ---- questions -------------------------------------------------------
    let inserted = 0;
    const questions = seed.questions || [];
    const CHUNK = 20;
    for (let i = 0; i < questions.length; i += CHUNK) {
        const chunk = questions.slice(i, i + CHUNK).filter((q) => byCode.has(q.skill));
        if (!chunk.length) continue;
        const values = [];
        const params = [];
        for (const q of chunk) {
            values.push('(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)');
            params.push(
                byCode.get(q.skill),
                q.tier,
                q.qtype || 'mcq',
                q.stem,
                q.stem_hash,
                JSON.stringify(q.options || []),
                String(q.answer),
                JSON.stringify(q.hints || []),
                JSON.stringify(q.steps || []),
                q.visual ? JSON.stringify(q.visual) : null,
                q.source || 'authored'
            );
        }
        await query(
            `INSERT IGNORE INTO qbank_items
                (skill_id, tier, qtype, stem, stem_hash, options, answer, hints, solution_steps, visual, source)
             VALUES ${values.join(', ')}`,
            params
        );
        inserted += chunk.length;
    }

    info(`[session-seed] seeded ${byCode.size} skills and ${inserted} questions`);
    return { seeded: true, skills: byCode.size, questions: inserted };
}

module.exports = { ensureSessionSchema, seedSessionData, TABLES, SEED_PATH };
