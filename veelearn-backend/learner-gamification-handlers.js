/**
 * Learner gamification: gems, streaks, avatar/store, display name, feedback.
 */

const STORE_SEED = [
    { item_id: 'theme_warm', item_type: 'theme', name: 'Warm', gem_cost: 0, asset_key: 'warm', description: 'Friendly cream & peach default' },
    { item_id: 'theme_blue', item_type: 'theme', name: 'Blue', gem_cost: 40, asset_key: 'blue', description: 'Calm sky blues' },
    { item_id: 'theme_red', item_type: 'theme', name: 'Red', gem_cost: 40, asset_key: 'red', description: 'Bold warm reds' },
    { item_id: 'theme_cool', item_type: 'theme', name: 'Cool', gem_cost: 50, asset_key: 'cool', description: 'Icy teal vibes' },
    { item_id: 'theme_happy', item_type: 'theme', name: 'Happy', gem_cost: 55, asset_key: 'happy', description: 'Sunny yellow smiles' },
    { item_id: 'theme_hacker', item_type: 'theme', name: 'Hacker', gem_cost: 80, asset_key: 'hacker', description: 'Terminal green glow' },
    { item_id: 'theme_superhero', item_type: 'theme', name: 'Superhero', gem_cost: 100, asset_key: 'superhero', description: 'Comic-book power colors' },
    { item_id: 'hat_blue', item_type: 'hat', name: 'Blue Cap', gem_cost: 25, asset_key: 'hat-blue', description: 'A comfy blue baseball cap' },
    { item_id: 'hat_crown', item_type: 'hat', name: 'Mini Crown', gem_cost: 60, asset_key: 'hat-crown', description: 'Feel like a learning champ' },
    { item_id: 'glasses_round', item_type: 'glasses', name: 'Round Glasses', gem_cost: 30, asset_key: 'glasses-round', description: 'Scholarly round frames' },
    { item_id: 'shirt_green', item_type: 'shirt', name: 'Green Hoodie', gem_cost: 35, asset_key: 'shirt-green', description: 'Cozy green hoodie' },
    { item_id: 'shirt_hero', item_type: 'shirt', name: 'Hero Tee', gem_cost: 45, asset_key: 'shirt-hero', description: 'Superhero stripe tee' },
    { item_id: 'cape_red', item_type: 'cape', name: 'Red Cape', gem_cost: 70, asset_key: 'cape-red', description: 'Whoosh into learning' },
    { item_id: 'acc_star', item_type: 'accessory', name: 'Star Badge', gem_cost: 20, asset_key: 'acc-star', description: 'A shiny star pin' }
];

const BASE_QUIZ_GEMS = 5;
const STREAK_CHECKIN_GEMS = 10;
const MAX_STREAK_MULT = 3;
const XP_PER_LEVEL = 100;

const XP_KINDS = {
    page: { xp: 8, gems: 0 },
    matching: { xp: 12, gems: 2 },
    step_reveal: { xp: 12, gems: 2 },
    unit: { xp: 50, gems: 15 },
    master: { xp: 100, gems: 30 },
    checkin: { xp: 15, gems: 0 }
};

const BADGE_CATALOG = [
    { id: 'first', label: 'First spark', how: 'Answer any quiz question correctly once.' },
    { id: 'streak3', label: '3-day streak', how: 'Check in on 3 different days in a row.' },
    { id: 'streak7', label: 'Week warrior', how: 'Keep a 7-day check-in streak.' },
    { id: 'quiz20', label: '20 correct', how: 'Get 20 quiz questions correct in total.' },
    { id: 'gems100', label: '100 gems earned', how: 'Earn 100 gems over your lifetime (spending does not reset this).' },
    { id: 'domain_master', label: 'Domain Master', how: 'Finish any unit in a Master Course.' },
    { id: 'zero_error', label: 'Zero-Error Streak', how: 'Get 5 quiz questions correct in a row.' },
    { id: 'stretch_champion', label: 'Stretch Champion', how: 'Answer 3 Stretch (SAT / Honors) questions correctly.' },
    { id: 'transformation_virtuoso', label: 'Transformation Virtuoso', how: 'Complete a functions / transformations unit, or finish your first unit.' }
];

function xpLevel(xp) {
    return Math.floor(Math.max(0, parseInt(xp, 10) || 0) / XP_PER_LEVEL) + 1;
}

/** Calendar day as YYYY-MM-DD (UTC — Render servers run UTC). */
function calendarDayUTC(offsetDays = 0) {
    const d = new Date();
    d.setUTCDate(d.getUTCDate() + offsetDays);
    return d.toISOString().slice(0, 10);
}

function todayUTC() {
    return calendarDayUTC(0);
}

function yesterdayUTC() {
    return calendarDayUTC(-1);
}

/**
 * Normalize mysql2 DATE / DATETIME / string into YYYY-MM-DD.
 * Without dateStrings, mysql2 returns DATE as a Date object and
 * String(date).slice(0,10) becomes "Wed Jul 23" — breaking same-day checks.
 */
function normalizeSqlDate(value) {
    if (value == null || value === '') return null;
    if (typeof value === 'string') {
        const m = value.match(/^(\d{4}-\d{2}-\d{2})/);
        return m ? m[1] : null;
    }
    if (value instanceof Date && !Number.isNaN(value.getTime())) {
        // Prefer UTC ISO (matches todayUTC). Also try local Y-M-D if they differ
        // by timezone — for DATE-only values at local midnight in US zones,
        // local components match the stored calendar day more reliably.
        const pad = (n) => String(n).padStart(2, '0');
        const local = `${value.getFullYear()}-${pad(value.getMonth() + 1)}-${pad(value.getDate())}`;
        const utc = value.toISOString().slice(0, 10);
        // If either equals today/yesterday we'll compare against todayUTC later;
        // prefer local calendar day for DATE columns (mysql2 default mapping).
        return local;
    }
    try {
        const s = String(value);
        const m = s.match(/^(\d{4}-\d{2}-\d{2})/);
        if (m) return m[1];
    } catch (_) { /* ignore */ }
    return null;
}

function streakMultiplier(currentStreak) {
    const s = Math.max(1, parseInt(currentStreak, 10) || 1);
    return Math.min(MAX_STREAK_MULT, 1 + Math.floor((s - 1) / 3));
}

function parseAvatarConfig(raw) {
    if (!raw) return { skin: 'default', hat: null, glasses: null, shirt: null, cape: null, accessory: null };
    if (typeof raw === 'object') return raw;
    try {
        return JSON.parse(raw);
    } catch (_) {
        return { skin: 'default', hat: null, glasses: null, shirt: null, cape: null, accessory: null };
    }
}

function displayNameFromUser(row) {
    if (row.display_name && String(row.display_name).trim()) return String(row.display_name).trim();
    if (row.name && String(row.name).trim()) return String(row.name).trim();
    const email = row.email || '';
    return email.includes('@') ? email.split('@')[0] : (email || 'Learner');
}

function createLearnerGamificationHandlers({ query, apiResponse, sendEmail }) {
    async function ensureStoreSeeded() {
        const rows = await query('SELECT COUNT(*) AS c FROM store_items');
        if ((rows[0]?.c || 0) > 0) return;
        for (const item of STORE_SEED) {
            await query(
                `INSERT INTO store_items (item_id, item_type, name, description, gem_cost, asset_key)
                 VALUES (?, ?, ?, ?, ?, ?)
                 ON DUPLICATE KEY UPDATE name = VALUES(name), gem_cost = VALUES(gem_cost)`,
                [item.item_id, item.item_type, item.name, item.description, item.gem_cost, item.asset_key]
            );
        }
        // Free warm theme for everyone is granted on first profile fetch
    }

    async function grantFreeDefaults(userId) {
        await query(
            `INSERT IGNORE INTO user_inventory (user_id, item_id) VALUES (?, 'theme_warm')`,
            [userId]
        );
    }

    async function getProfileRow(userId) {
        const rows = await query(
            `SELECT id, email, name, display_name, gems, current_streak, longest_streak,
                    last_active_date, avatar_config, dashboard_theme, role,
                    xp, lifetime_gems, current_correct_streak, best_correct_streak
             FROM users WHERE id = ? LIMIT 1`,
            [userId]
        );
        return rows[0] || null;
    }

    async function getBadges(userId) {
        try {
            return await query('SELECT badge_id, earned_at FROM user_badges WHERE user_id = ?', [userId]);
        } catch (_) {
            return [];
        }
    }

    async function grantBadge(userId, badgeId) {
        try {
            const result = await query(
                'INSERT IGNORE INTO user_badges (user_id, badge_id) VALUES (?, ?)',
                [userId, badgeId]
            );
            const header = Array.isArray(result) ? result[0] : result;
            return (header?.affectedRows || 0) > 0;
        } catch (_) {
            return false;
        }
    }

    async function evaluateBadges(userId, extras) {
        const row = await getProfileRow(userId);
        const stats = await quizStats(userId);
        const owned = new Set((await getBadges(userId)).map((b) => b.badge_id));
        const unlocked = [];
        const tryGrant = async (id) => {
            if (owned.has(id)) return;
            if (await grantBadge(userId, id)) {
                owned.add(id);
                const meta = BADGE_CATALOG.find((b) => b.id === id);
                unlocked.push({ id, label: meta ? meta.label : id });
            }
        };

        if ((stats.correct || 0) >= 1) await tryGrant('first');
        if ((row?.current_streak || 0) >= 3 || (row?.longest_streak || 0) >= 3) await tryGrant('streak3');
        if ((row?.longest_streak || 0) >= 7) await tryGrant('streak7');
        if ((stats.correct || 0) >= 20) await tryGrant('quiz20');
        if ((row?.lifetime_gems || 0) >= 100) await tryGrant('gems100');
        if ((row?.best_correct_streak || 0) >= 5 || (row?.current_correct_streak || 0) >= 5) {
            await tryGrant('zero_error');
        }
        if (extras?.unitComplete) await tryGrant('domain_master');
        const title = String(extras?.unitTitle || '');
        if (extras?.unitComplete && /function|transform/i.test(title)) {
            await tryGrant('transformation_virtuoso');
        } else if (extras?.unitComplete && extras?.firstUnitFallback) {
            await tryGrant('transformation_virtuoso');
        }
        if (extras?.stretchCorrectCount >= 3) await tryGrant('stretch_champion');
        return unlocked;
    }

    async function stretchCorrectCount(userId) {
        try {
            const rows = await query(
                `SELECT COUNT(*) AS c FROM user_quiz_attempts uqa
                 JOIN course_questions cq ON cq.id = uqa.question_id
                 WHERE uqa.user_id = ? AND uqa.is_correct = 1 AND cq.difficulty = 'stretch'`,
                [userId]
            );
            return rows[0]?.c || 0;
        } catch (_) {
            return 0;
        }
    }

    async function awardEvent(userId, eventKey, xp, gems, extras) {
        const key = String(eventKey || '').slice(0, 191);
        if (!key) return { xpAwarded: 0, gemsAwarded: 0, alreadyRewarded: true, newBadges: [] };
        let inserted = false;
        try {
            const result = await query(
                'INSERT IGNORE INTO user_xp_events (user_id, event_key, xp, gems) VALUES (?, ?, ?, ?)',
                [userId, key, xp || 0, gems || 0]
            );
            const header = Array.isArray(result) ? result[0] : result;
            inserted = (header?.affectedRows || 0) > 0;
        } catch (e) {
            console.error('awardEvent insert:', e.message);
            return { xpAwarded: 0, gemsAwarded: 0, alreadyRewarded: true, newBadges: [] };
        }
        if (!inserted) {
            const row = await getProfileRow(userId);
            return {
                xpAwarded: 0,
                gemsAwarded: 0,
                alreadyRewarded: true,
                xp: row?.xp || 0,
                gems: row?.gems || 0,
                level: xpLevel(row?.xp || 0),
                newBadges: []
            };
        }
        await query(
            `UPDATE users SET xp = COALESCE(xp,0) + ?, gems = COALESCE(gems,0) + ?,
                    lifetime_gems = COALESCE(lifetime_gems,0) + ?
             WHERE id = ?`,
            [xp || 0, gems || 0, gems || 0, userId]
        );
        const newBadges = await evaluateBadges(userId, extras || {});
        const row = await getProfileRow(userId);
        return {
            xpAwarded: xp || 0,
            gemsAwarded: gems || 0,
            alreadyRewarded: false,
            xp: row?.xp || 0,
            gems: row?.gems || 0,
            level: xpLevel(row?.xp || 0),
            newBadges
        };
    }

    async function getInventory(userId) {
        return query('SELECT item_id, acquired_at FROM user_inventory WHERE user_id = ?', [userId]);
    }

    async function quizStats(userId) {
        const rows = await query(
            `SELECT COUNT(*) AS total,
                    SUM(CASE WHEN is_correct = 1 THEN 1 ELSE 0 END) AS correct
             FROM user_quiz_attempts WHERE user_id = ?`,
            [userId]
        );
        return {
            total: rows[0]?.total || 0,
            correct: rows[0]?.correct || 0
        };
    }

    async function applyQuizReward(userId, questionId, isCorrect, difficulty) {
        if (!isCorrect) {
            await query('UPDATE users SET current_correct_streak = 0 WHERE id = ?', [userId]);
            const row = await getProfileRow(userId);
            return {
                xpAwarded: 0,
                gemsAwarded: 0,
                xp: row?.xp || 0,
                gems: row?.gems || 0,
                level: xpLevel(row?.xp || 0),
                newBadges: []
            };
        }
        const row = await getProfileRow(userId);
        const streak = (row?.current_correct_streak || 0) + 1;
        await query(
            `UPDATE users SET current_correct_streak = ?,
                    best_correct_streak = GREATEST(COALESCE(best_correct_streak,0), ?)
             WHERE id = ?`,
            [streak, streak, userId]
        );
        const isStretch = String(difficulty || '') === 'stretch';
        const mult = streakMultiplier(row?.current_streak || 0);
        let gems = BASE_QUIZ_GEMS * mult;
        if (isStretch) gems *= 2;
        const xpAmt = isStretch ? 25 : 10;
        const stretchCount = await stretchCorrectCount(userId);
        const awarded = await awardEvent(userId, `quiz:${questionId}`, xpAmt, gems, {
            stretchCorrectCount: stretchCount
        });
        try {
            await query(
                'UPDATE user_quiz_attempts SET gems_awarded = 1 WHERE user_id = ? AND question_id = ?',
                [userId, questionId]
            );
        } catch (_) { /* column may not exist yet */ }
        return awarded;
    }

    return {
        async ensureReady() {
            await ensureStoreSeeded();
        },

        async profile(req, res) {
            const userId = req.user.id;
            await grantFreeDefaults(userId);
            const row = await getProfileRow(userId);
            if (!row) return apiResponse(res, 404, 'User not found');
            const inv = await getInventory(userId);
            const stats = await quizStats(userId);
            const badges = await getBadges(userId);
            const owned = new Set(badges.map((b) => b.badge_id));
            return apiResponse(res, 200, 'OK', {
                id: row.id,
                displayName: displayNameFromUser(row),
                email: row.email,
                gems: row.gems || 0,
                lifetimeGems: row.lifetime_gems || 0,
                xp: row.xp || 0,
                level: xpLevel(row.xp || 0),
                currentStreak: row.current_streak || 0,
                longestStreak: row.longest_streak || 0,
                lastActiveDate: row.last_active_date,
                avatarConfig: parseAvatarConfig(row.avatar_config),
                dashboardTheme: row.dashboard_theme || 'warm',
                inventory: inv.map((i) => i.item_id),
                quizCorrect: stats.correct,
                quizTotal: stats.total,
                streakMultiplier: streakMultiplier(row.current_streak || 0),
                badges: BADGE_CATALOG.map((b) => ({
                    id: b.id,
                    label: b.label,
                    how: b.how || '',
                    earned: owned.has(b.id)
                }))
            });
        },

        async checkin(req, res) {
            const userId = req.user.id;
            const row = await getProfileRow(userId);
            if (!row) return apiResponse(res, 404, 'User not found');

            const today = todayUTC();
            const last = normalizeSqlDate(row.last_active_date);

            if (last === today) {
                return apiResponse(res, 200, 'Already checked in today', {
                    gems: row.gems || 0,
                    currentStreak: row.current_streak || 0,
                    longestStreak: row.longest_streak || 0,
                    gemsAwarded: 0,
                    alreadyCheckedIn: true
                });
            }

            let current = row.current_streak || 0;
            if (last === yesterdayUTC()) {
                current += 1;
            } else {
                current = 1;
            }
            const longest = Math.max(row.longest_streak || 0, current);
            const gemsAwarded = STREAK_CHECKIN_GEMS * streakMultiplier(current);
            const newGems = (row.gems || 0) + gemsAwarded;

            // Atomic guard: only award if still not checked in today (stops refresh races)
            const result = await query(
                `UPDATE users SET gems = ?, lifetime_gems = COALESCE(lifetime_gems,0) + ?,
                        current_streak = ?, longest_streak = ?, last_active_date = ?
                 WHERE id = ? AND (last_active_date IS NULL OR last_active_date < ?)`,
                [newGems, gemsAwarded, current, longest, today, userId, today]
            );

            const header = Array.isArray(result) ? result[0] : result;
            const affected = header?.affectedRows ?? 0;
            if (!affected) {
                const fresh = await getProfileRow(userId);
                return apiResponse(res, 200, 'Already checked in today', {
                    gems: fresh?.gems || 0,
                    currentStreak: fresh?.current_streak || 0,
                    longestStreak: fresh?.longest_streak || 0,
                    gemsAwarded: 0,
                    alreadyCheckedIn: true
                });
            }

            const xpResult = await awardEvent(userId, `checkin:${today}`, XP_KINDS.checkin.xp, 0);
            const badges = await evaluateBadges(userId, {});
            return apiResponse(res, 200, 'Streak updated', {
                gems: newGems,
                currentStreak: current,
                longestStreak: longest,
                gemsAwarded,
                xpAwarded: xpResult.xpAwarded || 0,
                xp: xpResult.xp,
                level: xpResult.level,
                alreadyCheckedIn: false,
                streakMultiplier: streakMultiplier(current),
                newBadges: badges
            });
        },

        async rewardQuiz(req, res) {
            const userId = req.user.id;
            const questionId = parseInt(req.body?.questionId, 10);
            if (!questionId || Number.isNaN(questionId)) {
                return apiResponse(res, 400, 'questionId required');
            }

            const attempt = await query(
                `SELECT id, is_correct, gems_awarded FROM user_quiz_attempts
                 WHERE user_id = ? AND question_id = ? LIMIT 1`,
                [userId, questionId]
            );
            if (!attempt.length) {
                return apiResponse(res, 400, 'No quiz attempt found');
            }
            if (!attempt[0].is_correct) {
                return apiResponse(res, 400, 'Answer was not correct');
            }
            if (attempt[0].gems_awarded) {
                const row = await getProfileRow(userId);
                return apiResponse(res, 200, 'Already rewarded', {
                    gems: row?.gems || 0,
                    gemsAwarded: 0,
                    alreadyRewarded: true
                });
            }

            const qRows = await query('SELECT difficulty FROM course_questions WHERE id = ? LIMIT 1', [questionId]);
            const awarded = await applyQuizReward(userId, questionId, true, qRows[0]?.difficulty);
            await query(
                'UPDATE user_quiz_attempts SET gems_awarded = 1 WHERE user_id = ? AND question_id = ?',
                [userId, questionId]
            );

            return apiResponse(res, 200, 'Gems awarded', {
                gems: awarded.gems,
                gemsAwarded: awarded.gemsAwarded,
                xpAwarded: awarded.xpAwarded,
                xp: awarded.xp,
                level: awarded.level,
                multiplier: streakMultiplier((await getProfileRow(userId))?.current_streak || 0),
                alreadyRewarded: awarded.alreadyRewarded,
                newBadges: awarded.newBadges
            });
        },

        async applyQuizReward(userId, questionId, isCorrect, difficulty) {
            return applyQuizReward(userId, questionId, isCorrect, difficulty);
        },

        async awardForUnit(userId, unitId, unitTitle, allComplete, parentCourseId) {
            const unitAward = await awardEvent(userId, `unit:${unitId}`, XP_KINDS.unit.xp, XP_KINDS.unit.gems, {
                unitComplete: true,
                unitTitle: unitTitle || '',
                firstUnitFallback: true
            });
            let masterAward = { xpAwarded: 0, gemsAwarded: 0, newBadges: [] };
            if (allComplete && parentCourseId) {
                masterAward = await awardEvent(
                    userId,
                    `master:${parentCourseId}`,
                    XP_KINDS.master.xp,
                    XP_KINDS.master.gems,
                    { unitComplete: true, unitTitle: unitTitle || '' }
                );
            }
            return {
                xpAwarded: (unitAward.xpAwarded || 0) + (masterAward.xpAwarded || 0),
                gemsAwarded: (unitAward.gemsAwarded || 0) + (masterAward.gemsAwarded || 0),
                xp: masterAward.xp || unitAward.xp,
                gems: masterAward.gems || unitAward.gems,
                level: masterAward.level || unitAward.level,
                newBadges: [...(unitAward.newBadges || []), ...(masterAward.newBadges || [])]
            };
        },

        async awardXp(req, res) {
            const kind = String(req.body?.kind || '');
            const amounts = XP_KINDS[kind];
            if (!amounts) return apiResponse(res, 400, 'Invalid kind');
            const userId = req.user.id;
            const courseId = parseInt(req.body?.courseId, 10) || 0;
            const pageIndex = parseInt(req.body?.pageIndex, 10);
            const blockId = String(req.body?.blockId || '').slice(0, 80);
            const unitId = parseInt(req.body?.unitId, 10) || 0;
            let key = '';
            if (kind === 'page') key = `page:${courseId}:${Number.isNaN(pageIndex) ? 0 : pageIndex}`;
            else if (kind === 'matching') key = `matching:${courseId}:${blockId}`;
            else if (kind === 'step_reveal') key = `step:${courseId}:${blockId}`;
            else if (kind === 'unit') key = `unit:${unitId}`;
            else if (kind === 'master') key = `master:${courseId}`;
            else if (kind === 'checkin') key = `checkin:${todayUTC()}`;
            else return apiResponse(res, 400, 'Invalid kind');
            const extras = {
                unitComplete: kind === 'unit' || kind === 'master',
                unitTitle: String(req.body?.unitTitle || '')
            };
            const result = await awardEvent(userId, key, amounts.xp, amounts.gems, extras);
            return apiResponse(res, 200, 'OK', result);
        },

        async getBossState(req, res) {
            const userId = req.user.id;
            const courseId = parseInt(req.params.courseId, 10);
            if (!courseId) return apiResponse(res, 400, 'courseId required');
            let rows = [];
            try {
                rows = await query(
                    'SELECT hearts, unlocked_json FROM user_boss_state WHERE user_id = ? AND course_id = ? LIMIT 1',
                    [userId, courseId]
                );
            } catch (_) {
                rows = [];
            }
            if (!rows.length) {
                return apiResponse(res, 200, 'OK', {
                    hearts: 3,
                    unlocked: { easy: true, medium: false, hard: false }
                });
            }
            let unlocked = { easy: true, medium: false, hard: false };
            try {
                unlocked = Object.assign(unlocked, JSON.parse(rows[0].unlocked_json || '{}'));
            } catch (_) { /* keep defaults */ }
            return apiResponse(res, 200, 'OK', { hearts: rows[0].hearts, unlocked });
        },

        async saveBossState(req, res) {
            const userId = req.user.id;
            const courseId = parseInt(req.params.courseId, 10);
            if (!courseId) return apiResponse(res, 400, 'courseId required');
            const hearts = Math.max(0, Math.min(3, parseInt(req.body?.hearts, 10)));
            const unlocked = JSON.stringify(req.body?.unlocked || {});
            await query(
                `INSERT INTO user_boss_state (user_id, course_id, hearts, unlocked_json)
                 VALUES (?, ?, ?, ?)
                 ON DUPLICATE KEY UPDATE hearts = VALUES(hearts), unlocked_json = VALUES(unlocked_json)`,
                [userId, courseId, Number.isNaN(hearts) ? 3 : hearts, unlocked]
            );
            return apiResponse(res, 200, 'Saved');
        },

        async storeCatalog(req, res) {
            await ensureStoreSeeded();
            const userId = req.user.id;
            await grantFreeDefaults(userId);
            const items = await query(
                `SELECT item_id, item_type, name, description, gem_cost, asset_key FROM store_items ORDER BY gem_cost ASC, name ASC`
            );
            const inv = await getInventory(userId);
            const owned = new Set(inv.map((i) => i.item_id));
            const row = await getProfileRow(userId);
            return apiResponse(res, 200, 'OK', {
                gems: row?.gems || 0,
                items: items.map((it) => ({
                    ...it,
                    owned: owned.has(it.item_id)
                }))
            });
        },

        async purchase(req, res) {
            const userId = req.user.id;
            const itemId = String(req.body?.itemId || '').trim();
            if (!itemId) return apiResponse(res, 400, 'itemId required');

            const items = await query('SELECT * FROM store_items WHERE item_id = ? LIMIT 1', [itemId]);
            if (!items.length) return apiResponse(res, 404, 'Item not found');
            const item = items[0];

            const owned = await query(
                'SELECT id FROM user_inventory WHERE user_id = ? AND item_id = ? LIMIT 1',
                [userId, itemId]
            );
            if (owned.length) {
                return apiResponse(res, 400, 'Already owned');
            }

            const row = await getProfileRow(userId);
            const cost = item.gem_cost || 0;
            if ((row?.gems || 0) < cost) {
                return apiResponse(res, 400, 'Not enough gems');
            }

            await query('UPDATE users SET gems = gems - ? WHERE id = ? AND gems >= ?', [cost, userId, cost]);
            await query('INSERT INTO user_inventory (user_id, item_id) VALUES (?, ?)', [userId, itemId]);

            const updated = await getProfileRow(userId);
            return apiResponse(res, 200, 'Purchased', {
                gems: updated?.gems || 0,
                itemId
            });
        },

        async equip(req, res) {
            const userId = req.user.id;
            const { slot, itemId, theme } = req.body || {};

            if (theme) {
                const themeItem = `theme_${String(theme)}`;
                const owned = await query(
                    'SELECT id FROM user_inventory WHERE user_id = ? AND item_id = ? LIMIT 1',
                    [userId, themeItem]
                );
                if (!owned.length && theme !== 'warm') {
                    return apiResponse(res, 403, 'Theme not owned');
                }
                await query('UPDATE users SET dashboard_theme = ? WHERE id = ?', [String(theme), userId]);
                return apiResponse(res, 200, 'Theme equipped', { dashboardTheme: String(theme) });
            }

            const allowedSlots = ['hat', 'glasses', 'shirt', 'cape', 'accessory'];
            if (!allowedSlots.includes(slot)) {
                return apiResponse(res, 400, 'Invalid slot');
            }

            const row = await getProfileRow(userId);
            const cfg = parseAvatarConfig(row?.avatar_config);

            if (itemId === null || itemId === '' || itemId === undefined) {
                cfg[slot] = null;
            } else {
                const id = String(itemId);
                const owned = await query(
                    'SELECT id FROM user_inventory WHERE user_id = ? AND item_id = ? LIMIT 1',
                    [userId, id]
                );
                if (!owned.length) return apiResponse(res, 403, 'Item not owned');
                cfg[slot] = id;
            }

            await query('UPDATE users SET avatar_config = ? WHERE id = ?', [JSON.stringify(cfg), userId]);
            return apiResponse(res, 200, 'Equipped', { avatarConfig: cfg });
        },

        async updateSettings(req, res) {
            const userId = req.user.id;
            const displayName = String(req.body?.displayName || '').trim().slice(0, 80);
            if (!displayName) return apiResponse(res, 400, 'displayName required');
            await query(
                "UPDATE users SET display_name = ?, name = COALESCE(NULLIF(name, ''), ?) WHERE id = ?",
                [displayName, displayName, userId]
            );
            return apiResponse(res, 200, 'Saved', { displayName });
        },

        async feedback(req, res) {
            const userId = req.user.id;
            const message = String(req.body?.message || '').trim().slice(0, 4000);
            if (!message || message.length < 5) {
                return apiResponse(res, 400, 'Please write a bit more feedback');
            }

            const row = await getProfileRow(userId);
            let emailed = 0;
            try {
                if (typeof sendEmail === 'function') {
                    await sendEmail(
                        'viratsuper6@gmail.com',
                        `Veelearn feedback from ${displayNameFromUser(row)}`,
                        `<p><strong>From:</strong> ${row?.email || userId} (${displayNameFromUser(row)})</p>
                         <p><strong>Message:</strong></p>
                         <pre style="white-space:pre-wrap;font-family:sans-serif;">${String(message)
                             .replace(/&/g, '&amp;')
                             .replace(/</g, '&lt;')
                             .replace(/>/g, '&gt;')}</pre>`
                    );
                    emailed = 1;
                }
            } catch (err) {
                console.error('Feedback email failed:', err.message);
            }

            await query(
                'INSERT INTO user_feedback (user_id, message, emailed) VALUES (?, ?, ?)',
                [userId, message, emailed]
            );

            return apiResponse(res, 200, emailed ? 'Thanks! Feedback sent.' : 'Thanks! Feedback saved.', {
                emailed: !!emailed
            });
        },

        async listFeedback(req, res) {
            // Superadmin-only inbox helper (optional append; does not change existing panels)
            if (req.user.role !== 'superadmin') {
                return apiResponse(res, 403, 'Forbidden');
            }
            const rows = await query(
                `SELECT f.id, f.message, f.created_at, f.emailed, u.email,
                        COALESCE(NULLIF(u.display_name,''), NULLIF(u.name,''), SUBSTRING_INDEX(u.email,'@',1)) AS display_name
                 FROM user_feedback f
                 JOIN users u ON u.id = f.user_id
                 ORDER BY f.created_at DESC
                 LIMIT 100`
            );
            return apiResponse(res, 200, 'OK', rows);
        }
    };
}

module.exports = { createLearnerGamificationHandlers, STORE_SEED, streakMultiplier, xpLevel, BADGE_CATALOG };
