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
const readline = require('readline');
const zlib = require('zlib');

const SEED_PATH = path.join(__dirname, 'seed', 'session_seed.json');
// The bulk bank (open datasets + generated practice) is far too large for the
// curated seed: it ships gzipped, one JSON question per line, and is loaded once
// per version by importOpenBank() after boot.
const BANK_PATH = path.join(__dirname, 'seed', 'open_bank.jsonl.gz');
const BANK_META_PATH = path.join(__dirname, 'seed', 'open_bank_meta.json');

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

    `CREATE TABLE IF NOT EXISTS bank_imports (
        version VARCHAR(32) NOT NULL PRIMARY KEY,
        source_count INT DEFAULT 0,
        item_count INT DEFAULT 0,
        meta LONGTEXT NULL,
        imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )`,

    `CREATE TABLE IF NOT EXISTS course_outlines (
        course_id INT PRIMARY KEY,
        outline_json LONGTEXT NULL,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
        review_pool LONGTEXT NULL,
        frame_md LONGTEXT NULL,

        unit_index SMALLINT DEFAULT 0,
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
    )`,

    // ---- P4: teaching impact ledger (volunteer hours v2) ------------------
    `CREATE TABLE IF NOT EXISTS creator_impact_ledger (
        id INT AUTO_INCREMENT PRIMARY KEY,
        course_id INT NOT NULL,
        creator_id INT NOT NULL,
        learner_id INT NOT NULL,
        session_id INT NOT NULL,
        kind VARCHAR(16) DEFAULT 'session',
        hours REAL DEFAULT 0,
        readiness_mult REAL DEFAULT 1,
        quality_mult REAL DEFAULT 1,
        mastery_mult REAL DEFAULT 1,
        mastery_gain REAL DEFAULT 0,
        paid_reason VARCHAR(40) NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE KEY uniq_impact_grant (session_id, kind),
        INDEX idx_impact_course (course_id, created_at),
        INDEX idx_impact_creator (creator_id, created_at)
    )`,

    // ---- P5: flashcards from misses, auto notes, digests, assignments -----
    `CREATE TABLE IF NOT EXISTS session_flashcards (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        question_id INT NULL,
        skill_id INT NULL,
        front LONGTEXT NOT NULL,
        back LONGTEXT NOT NULL,
        source VARCHAR(16) DEFAULT 'miss',
        ease REAL DEFAULT 2.5,
        reps SMALLINT DEFAULT 0,
        due_at TIMESTAMP NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE KEY uniq_card_question (user_id, question_id),
        INDEX idx_cards_due (user_id, due_at)
    )`,

    `CREATE TABLE IF NOT EXISTS session_notes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        session_id INT NULL,
        body LONGTEXT NOT NULL,
        skills VARCHAR(400) NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE KEY uniq_note_session (session_id),
        INDEX idx_notes_user (user_id, created_at)
    )`,

    `CREATE TABLE IF NOT EXISTS parent_digests (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        period_start DATE NOT NULL,
        period_end DATE NOT NULL,
        body LONGTEXT NOT NULL,
        emailed_to VARCHAR(190) NULL,
        sent_at TIMESTAMP NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE KEY uniq_digest_period (user_id, period_start)
    )`,

    `CREATE TABLE IF NOT EXISTS session_assignments (
        id INT AUTO_INCREMENT PRIMARY KEY,
        teacher_id INT NOT NULL,
        course_id INT NOT NULL,
        class_code VARCHAR(12) NULL,
        title VARCHAR(160) NULL,
        unit_index SMALLINT DEFAULT 0,
        minutes SMALLINT DEFAULT 20,
        due_at TIMESTAMP NULL,
        status VARCHAR(12) DEFAULT 'open',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_assign_teacher (teacher_id, created_at),
        INDEX idx_assign_class (class_code, status)
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
    'CREATE INDEX IF NOT EXISTS idx_review_due2 ON review_queue (user_id, due_at)',
    'CREATE INDEX IF NOT EXISTS idx_cards_due2 ON session_flashcards (user_id, due_at)',
    'CREATE INDEX IF NOT EXISTS idx_impact_course2 ON creator_impact_ledger (course_id, created_at)'
];

const ALTERS = [
    'ALTER TABLE courses ADD COLUMN IF NOT EXISTS ai_ready SMALLINT DEFAULT 0',
    'ALTER TABLE courses ADD COLUMN IF NOT EXISTS sessions_taught INT DEFAULT 0',
    'ALTER TABLE courses ADD COLUMN IF NOT EXISTS readiness_score SMALLINT DEFAULT 0',
    'ALTER TABLE courses ADD COLUMN IF NOT EXISTS readiness_json LONGTEXT NULL',
    'ALTER TABLE session_focus_items ADD COLUMN IF NOT EXISTS frame_md LONGTEXT NULL',
    'ALTER TABLE session_focus_items ADD COLUMN IF NOT EXISTS review_pool LONGTEXT NULL',

    'ALTER TABLE session_focus_items ADD COLUMN IF NOT EXISTS unit_index SMALLINT DEFAULT 0',
    'ALTER TABLE sessions ADD COLUMN IF NOT EXISTS rating SMALLINT NULL',
    'ALTER TABLE sessions ADD COLUMN IF NOT EXISTS sprint SMALLINT DEFAULT 0',
    'ALTER TABLE users ADD COLUMN IF NOT EXISTS exam_date DATE NULL',
    'ALTER TABLE users ADD COLUMN IF NOT EXISTS parent_email VARCHAR(190) NULL',
    'ALTER TABLE users ADD COLUMN IF NOT EXISTS digest_opt_in SMALLINT DEFAULT 0',
    'ALTER TABLE users ADD COLUMN IF NOT EXISTS reminder_at TIMESTAMP NULL',
    "ALTER TABLE user_learning_profile ADD COLUMN IF NOT EXISTS prefs LONGTEXT NULL",
    // Provenance columns, for databases created before they were in CREATE TABLE.
    "ALTER TABLE qbank_items ADD COLUMN IF NOT EXISTS source VARCHAR(16) DEFAULT 'authored'",
    "ALTER TABLE qbank_items ADD COLUMN IF NOT EXISTS attribution VARCHAR(200) NULL"
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
 * Idempotent and incremental: INSERT IGNORE (ON CONFLICT DO NOTHING) against
 * `skills.code` and `qbank_items.stem_hash`, so a boot adds only the skills and
 * questions that are new to the database. That is how new banks (exam subjects,
 * extra authoring passes) reach a database that was seeded months ago.
 */
async function seedSessionData({ query, log } = {}) {
    const info = (log && log.info) || (() => {});
    const warn = (log && log.warn) || ((m) => console.warn(m));

    // Refresh the materialised pool after the inserts (below): planning skips
    // skills whose live_count is zero, so a new skill must be counted in the same
    // boot that created it.
    const refreshPool = async () => {
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
    };

    // Growth, not just first boot: the bank gains skills and questions over time
    // (new subjects, authoring passes), so every boot re-runs the inserts. Both
    // tables have the unique keys that make this a no-op for rows already there
    // (`skills.code`, `qbank_items.stem_hash`).
    const seed = loadSeed();
    if (!seed) {
        warn('[session-seed] no seed/session_seed.json found — run: python build_session_seed.py');
        return { seeded: false, skills: 0, questions: 0 };
    }
    if (seed.__error) {
        warn(`[session-seed] seed file is not valid JSON: ${seed.__error}`);
        return { seeded: false, skills: 0, questions: 0 };
    }

    const countRows = async (sql) => {
        try {
            const rows = await query(sql);
            return Number(rows[0]?.c || 0);
        } catch (_) {
            return 0;
        }
    };
    const skillsBefore = await countRows('SELECT COUNT(*) AS c FROM skills');
    const itemsBefore = await countRows('SELECT COUNT(*) AS c FROM qbank_items');

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
            values.push('(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)');
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
                q.source || 'authored',
                // Provenance travels with the row: which work it came from and
                // under which licence, or 'Veelearn original' for our own items.
                q.attribution || null
            );
        }
        await query(
            `INSERT IGNORE INTO qbank_items
                (skill_id, tier, qtype, stem, stem_hash, options, answer, hints, solution_steps, visual, source, attribution)
             VALUES ${values.join(', ')}`,
            params
        );
        inserted += chunk.length;
    }

    // Existing rows keep their id (INSERT IGNORE skips them), so a diagram or a
    // licence line added to a question later would never reach a database that
    // was seeded before it. Refresh those columns for the seeded rows only;
    // stem_hash identifies a seed row, so creator content is untouched.
    let refreshed = 0;
    for (const q of questions) {
        if (!q.stem_hash || (!q.visual && !q.attribution)) continue;
        try {
            await query('UPDATE qbank_items SET visual = ?, attribution = ?, source = ? WHERE stem_hash = ?', [
                q.visual ? JSON.stringify(q.visual) : null,
                q.attribution || null,
                q.source || 'authored',
                q.stem_hash
            ]);
            refreshed += 1;
        } catch (err) {
            warn(`[session-seed] media refresh skipped: ${err.message}`);
            break;
        }
    }

    await refreshPool();

    const skillsAfter = await countRows('SELECT COUNT(*) AS c FROM skills');
    const itemsAfter = await countRows('SELECT COUNT(*) AS c FROM qbank_items');
    const addedSkills = Math.max(0, skillsAfter - skillsBefore);
    const addedItems = Math.max(0, itemsAfter - itemsBefore);
    info(
        `[session-seed] ${skillsAfter} skills, ${itemsAfter} questions ` +
            `(added ${addedSkills} skills, ${addedItems} questions from ${inserted} seed rows)`
    );
    return {
        seeded: addedSkills + addedItems > 0,
        skills: skillsAfter,
        questions: itemsAfter,
        added: { skills: addedSkills, questions: addedItems }
    };
}

/**
 * Import seed/open_bank.jsonl.gz into qbank_items, once per bank version.
 *
 * The curated seed stays small; the bulk bank (openly licensed datasets plus the
 * generated practice families) is ~47k rows, so it is streamed in batches of 250
 * and guarded by `bank_imports`. A crash mid-import is safe: INSERT IGNORE makes a
 * re-run add only what is missing, and the version is recorded after the stream
 * finishes. `skill_pool` is refreshed once at the end rather than per row.
 *
 * Every row carries its own `source` and `attribution`, so the licence line that
 * provenance.js shows in the UI is the same one the loader wrote.
 */
async function importOpenBank({ query, log, batchSize = 250 } = {}) {
    const info = (log && log.info) || (() => {});
    const warn = (log && log.warn) || ((m) => console.warn(m));

    let meta;
    try {
        meta = JSON.parse(fs.readFileSync(BANK_META_PATH, 'utf8'));
    } catch (e) {
        warn(`[open-bank] no usable ${path.basename(BANK_META_PATH)} (${e.message}) — run: python tools/build_open_bank.py`);
        return { imported: false, reason: 'no-meta' };
    }
    if (!fs.existsSync(BANK_PATH)) {
        warn('[open-bank] no seed/open_bank.jsonl.gz — run: python tools/build_open_bank.py');
        return { imported: false, reason: 'no-bank' };
    }

    let done;
    try {
        done = await query('SELECT version FROM bank_imports WHERE version = ?', [meta.version]);
    } catch (e) {
        // Without the guard table every boot would re-stream the whole bank.
        warn(`[open-bank] could not check bank_imports: ${e.message}`);
        return { imported: false, reason: 'no-table' };
    }
    if (done && done.length) {
        return { imported: false, version: meta.version, already: true };
    }

    const skillRows = await query('SELECT id, code FROM skills');
    const byCode = new Map(skillRows.map((r) => [r.code, Number(r.id)]));
    const wanted = new Set(Object.keys(meta.bySkill || {}));
    if (![...wanted].some((code) => byCode.has(code))) {
        warn('[open-bank] none of the bank skills exist yet; leaving the import for the next boot');
        return { imported: false, reason: 'no-skills' };
    }

    const started = Date.now();
    let rows = 0;
    let inserted = 0;
    let unknownSkill = 0;
    let batch = [];

    const flush = async () => {
        if (!batch.length) return;
        const values = [];
        const params = [];
        for (const q of batch) {
            values.push('(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)');
            params.push(
                q.skill_id,
                q.tier,
                'mcq',
                q.stem,
                q.stem_hash,
                q.options,
                q.answer,
                q.hints,
                q.steps,
                null,
                q.source,
                q.attribution
            );
        }
        await query(
            `INSERT IGNORE INTO qbank_items
                (skill_id, tier, qtype, stem, stem_hash, options, answer, hints, solution_steps, visual, source, attribution)
             VALUES ${values.join(', ')}`,
            params
        );
        inserted += batch.length;
        batch = [];
    };

    const stream = fs.createReadStream(BANK_PATH).pipe(zlib.createGunzip());
    const lines = readline.createInterface({ input: stream, crlfDelay: Infinity });
    for await (const line of lines) {
        if (!line.trim()) continue;
        let item;
        try {
            item = JSON.parse(line);
        } catch (e) {
            continue;
        }
        rows += 1;
        const skillId = byCode.get(item.skill);
        if (!skillId) {
            unknownSkill += 1;
            continue;
        }
        batch.push({
            skill_id: skillId,
            tier: item.tier || 1,
            stem: item.stem,
            stem_hash: item.stem_hash,
            options: JSON.stringify(item.options || []),
            answer: String(item.answer),
            hints: JSON.stringify(item.hints || []),
            steps: JSON.stringify(item.steps || []),
            source: item.source || 'authored',
            attribution: item.attribution || null
        });
        if (batch.length >= batchSize) await flush();
    }
    await flush();

    if (!inserted) {
        warn(`[open-bank] nothing importable in ${meta.version} (${rows} rows, ${unknownSkill} unknown skills)`);
        return { imported: false, version: meta.version, rows };
    }

    try {
        await query(
            `INSERT INTO skill_pool (skill_id, tier, live_count)
             SELECT skill_id, tier, COUNT(*) FROM qbank_items WHERE live = 1
             GROUP BY skill_id, tier
             ON CONFLICT (skill_id, tier)
             DO UPDATE SET live_count = EXCLUDED.live_count, updated_at = NOW()`
        );
    } catch (e) {
        warn(`[open-bank] skill pool refresh skipped: ${e.message}`);
    }

    try {
        await query('INSERT INTO bank_imports (version, source_count, item_count, meta) VALUES (?, ?, ?, ?)', [
            meta.version,
            Object.keys(meta.bySource || {}).length,
            meta.total || inserted,
            JSON.stringify({ builtAt: meta.builtAt, bySource: meta.bySource, datasets: meta.datasets })
        ]);
    } catch (e) {
        // Not fatal: rows are in, and INSERT IGNORE makes the next boot harmless.
        warn(`[open-bank] could not record version ${meta.version}: ${e.message}`);
    }

    info(
        `[open-bank] imported ${inserted} of ${rows} rows for version ${meta.version} ` +
            `in ${Math.round((Date.now() - started) / 1000)}s` +
            (unknownSkill ? ` (${unknownSkill} rows belong to skills this seed does not have)` : '')
    );
    return { imported: true, version: meta.version, rows, inserted, unknownSkill };
}

module.exports = { ensureSessionSchema, seedSessionData, importOpenBank, TABLES, SEED_PATH, BANK_PATH };
