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

function todayUTC() {
    return new Date().toISOString().slice(0, 10);
}

function yesterdayUTC() {
    const d = new Date();
    d.setUTCDate(d.getUTCDate() - 1);
    return d.toISOString().slice(0, 10);
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
                    last_active_date, avatar_config, dashboard_theme, role
             FROM users WHERE id = ? LIMIT 1`,
            [userId]
        );
        return rows[0] || null;
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
            return apiResponse(res, 200, 'OK', {
                displayName: displayNameFromUser(row),
                email: row.email,
                gems: row.gems || 0,
                currentStreak: row.current_streak || 0,
                longestStreak: row.longest_streak || 0,
                lastActiveDate: row.last_active_date,
                avatarConfig: parseAvatarConfig(row.avatar_config),
                dashboardTheme: row.dashboard_theme || 'warm',
                inventory: inv.map((i) => i.item_id),
                quizCorrect: stats.correct,
                quizTotal: stats.total,
                streakMultiplier: streakMultiplier(row.current_streak || 0)
            });
        },

        async checkin(req, res) {
            const userId = req.user.id;
            const row = await getProfileRow(userId);
            if (!row) return apiResponse(res, 404, 'User not found');

            const today = todayUTC();
            const last = row.last_active_date
                ? String(row.last_active_date).slice(0, 10)
                : null;

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

            await query(
                `UPDATE users SET gems = ?, current_streak = ?, longest_streak = ?, last_active_date = ?
                 WHERE id = ?`,
                [newGems, current, longest, today, userId]
            );

            return apiResponse(res, 200, 'Streak updated', {
                gems: newGems,
                currentStreak: current,
                longestStreak: longest,
                gemsAwarded,
                alreadyCheckedIn: false,
                streakMultiplier: streakMultiplier(current)
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

            const row = await getProfileRow(userId);
            const mult = streakMultiplier(row?.current_streak || 0);
            const gemsAwarded = BASE_QUIZ_GEMS * mult;
            const newGems = (row?.gems || 0) + gemsAwarded;

            await query('UPDATE users SET gems = ? WHERE id = ?', [newGems, userId]);
            await query(
                'UPDATE user_quiz_attempts SET gems_awarded = 1 WHERE user_id = ? AND question_id = ?',
                [userId, questionId]
            );

            return apiResponse(res, 200, 'Gems awarded', {
                gems: newGems,
                gemsAwarded,
                multiplier: mult,
                alreadyRewarded: false
            });
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

module.exports = { createLearnerGamificationHandlers, STORE_SEED, streakMultiplier };
