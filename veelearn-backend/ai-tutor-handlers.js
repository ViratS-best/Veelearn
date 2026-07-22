/**
 * Study coach: OpenRouter-backed chat with Socratic constraints and validated recommendations.
 */

const SOCRATIC_SYSTEM = `You are a study coach for Veelearn. Your job is to help students learn, not to do their work.

Rules (strict):
- Never give final numeric answers, final multiple-choice answers, or copy-paste solutions.
- Never provide complete code that solves an assignment; at most a tiny illustrative snippet with placeholders, or describe the algorithm in words.
- Give at most ONE clear next step: a question to ask themselves, a hint about which concept to review, or how to set up the problem (e.g. "label what is known/unknown").
- If they demand the answer, briefly refuse and offer a learning step instead.
- Keep responses concise (under 200 words unless they ask for more detail on the method).
- After your coaching reply, you MAY suggest up to 3 courses from the AVAILABLE_COURSES list the user is not enrolled in. If you do, add a new line exactly:
VEELEARN_RECOMMEND_JSON:
followed by a single JSON array like [{"courseId":123,"title":"Exact title from list","reason":"one short sentence"}]. Use only courseIds that appear in AVAILABLE_COURSES. If you have no recommendation, omit the VEELEARN_RECOMMEND_JSON line entirely.`;

function guardSocraticReply(text) {
    if (!text || typeof text !== 'string') return text;
    const t = text.trim();
    if (/^\d+(\.\d+)?$/.test(t)) {
        return "I can't give a final answer like that. What is the first relationship or formula that applies? Try writing what you know and what you need to find.";
    }
    return text;
}

function splitReplyAndRecommendations(raw) {
    const marker = '\nVEELEARN_RECOMMEND_JSON:';
    const idx = raw.indexOf(marker);
    if (idx < 0) {
        return { replyText: raw.trim(), rawRecs: [] };
    }
    const replyText = raw.slice(0, idx).trim();
    const jsonPart = raw.slice(idx + marker.length).trim();
    let rawRecs = [];
    try {
        const parsed = JSON.parse(jsonPart);
        if (Array.isArray(parsed)) rawRecs = parsed;
    } catch (_) {
        /* ignore malformed JSON */
    }
    return { replyText, rawRecs };
}

function validateRecommendations(rawRecs, allowedCatalog) {
    const byId = new Map(allowedCatalog.map((c) => [c.id, c]));
    const out = [];
    const seen = new Set();
    for (const r of rawRecs) {
        const id = parseInt(r?.courseId, 10);
        if (Number.isNaN(id) || seen.has(id)) continue;
        const row = byId.get(id);
        if (!row) continue;
        seen.add(id);
        out.push({
            courseId: id,
            title: row.title,
            reason: typeof r.reason === 'string' ? r.reason.slice(0, 240) : ''
        });
        if (out.length >= 3) break;
    }
    return out;
}

module.exports = function createAiTutorHandlers({ query, openRouterChatCompletion, apiResponse }) {
    async function maybeRefreshLearningProfile(userId) {
        const rows = await query(
            'SELECT COUNT(*) AS cnt FROM ai_tutor_messages WHERE user_id = ? AND role = ?',
            [userId, 'user']
        );
        const cnt = rows[0]?.cnt || 0;
        if (cnt === 0 || cnt % 10 !== 0) return;

        const recent = await query(
            `SELECT role, content FROM ai_tutor_messages WHERE user_id = ? ORDER BY created_at DESC LIMIT 24`,
            [userId]
        );
        const lines = recent
            .reverse()
            .map((r) => `${r.role}: ${String(r.content).slice(0, 500)}`)
            .join('\n');

        const summaryMessages = [
            {
                role: 'system',
                content:
                    'Summarize in 3-5 short bullet points how this student tends to learn: question style, common struggles, pace. No PII, no email. Plain text bullets only.'
            },
            { role: 'user', content: lines }
        ];

        try {
            const s = await openRouterChatCompletion(summaryMessages, { max_tokens: 300, temperature: 0.25 });
            await query(
                `INSERT INTO user_learning_profile (user_id, summary_text) VALUES (?, ?)
                 ON DUPLICATE KEY UPDATE summary_text = VALUES(summary_text)`,
                [userId, s.slice(0, 4000)]
            );
        } catch (e) {
            console.warn('Learning profile refresh skipped:', e.message);
        }
    }

    return {
        async chat(req, res) {
            const userId = req.user.id;
            let message = typeof req.body?.message === 'string' ? req.body.message.trim() : '';
            if (!message) {
                return apiResponse(res, 400, 'Message is required');
            }
            if (message.length > 8000) {
                message = message.slice(0, 8000);
            }

            let courseId = null;
            if (req.body?.courseId != null && req.body.courseId !== '') {
                const cid = parseInt(req.body.courseId, 10);
                if (!Number.isNaN(cid)) courseId = cid;
            }

            let courseTitle = null;
            if (courseId != null) {
                const cr = await query('SELECT id, title FROM courses WHERE id = ? LIMIT 1', [courseId]);
                if (cr.length) courseTitle = cr[0].title;
            }

            const enrolled = await query(
                `SELECT c.id, c.title FROM enrollments e
                 JOIN courses c ON c.id = e.course_id WHERE e.user_id = ? ORDER BY c.title ASC`,
                [userId]
            );

            const catalog = await query(
                `SELECT c.id, c.title, LEFT(IFNULL(c.description,''), 200) AS desc_preview
                 FROM courses c
                 WHERE c.status = 'approved'
                 AND c.id NOT IN (SELECT course_id FROM enrollments WHERE user_id = ?)
                 ORDER BY c.title ASC LIMIT 40`,
                [userId]
            );

            const quizRow = await query(
                `SELECT COUNT(*) AS total, SUM(CASE WHEN is_correct = 1 THEN 1 ELSE 0 END) AS correct
                 FROM user_quiz_attempts WHERE user_id = ?`,
                [userId]
            );
            const totalQ = quizRow[0]?.total || 0;
            const correctQ = quizRow[0]?.correct || 0;

            let profileSummary = '';
            const prof = await query('SELECT summary_text FROM user_learning_profile WHERE user_id = ?', [userId]);
            if (prof.length && prof[0].summary_text) {
                profileSummary = String(prof[0].summary_text).slice(0, 1500);
            }

            const historyRows = await query(
                `SELECT role, content FROM ai_tutor_messages WHERE user_id = ? ORDER BY created_at DESC LIMIT 24`,
                [userId]
            );
            historyRows.reverse();

            const availableLines = catalog.map((c) => `${c.id}: ${c.title}`).join('\n');
            const enrolledLines = enrolled.map((c) => `${c.id}: ${c.title}`).join('\n') || '(none)';

            const contextBlock = [
                `Enrolled courses:\n${enrolledLines}`,
                `Quiz attempts (all time): ${correctQ} correct of ${totalQ} recorded.`,
                courseTitle ? `Current course context: "${courseTitle}" (id ${courseId}).` : 'No specific course context.',
                profileSummary ? `Learning profile notes:\n${profileSummary}` : '',
                `AVAILABLE_COURSES (not enrolled; suggest only from this list):\n${availableLines || '(none available)'}`
            ]
                .filter(Boolean)
                .join('\n\n');

            const historyMessages = [];
            for (const row of historyRows) {
                if (row.role !== 'user' && row.role !== 'assistant') continue;
                historyMessages.push({
                    role: row.role,
                    content: String(row.content).slice(0, 4000)
                });
            }

            const messages = [
                { role: 'system', content: SOCRATIC_SYSTEM },
                { role: 'system', content: `Personalization context:\n${contextBlock}` },
                ...historyMessages,
                { role: 'user', content: message }
            ];

            let rawReply;
            try {
                rawReply = await openRouterChatCompletion(messages, { max_tokens: 1024, temperature: 0.35 });
            } catch (e) {
                console.error('OpenRouter tutor error:', e.message);
                if (e.code === 'OPENROUTER_NOT_CONFIGURED') {
                    return apiResponse(res, 503, 'Study coach is not configured on this server');
                }
                if (e.code === 'OPENROUTER_RATE_LIMITED' || e.status === 429) {
                    return apiResponse(
                        res,
                        429,
                        'Study coach is temporarily rate-limited. Please wait a minute and try again.'
                    );
                }
                return apiResponse(res, 502, 'Study coach is temporarily unavailable. Please try again later.');
            }

            const { replyText, rawRecs } = splitReplyAndRecommendations(rawReply);
            let safeReply = guardSocraticReply(replyText);
            const recommendations = validateRecommendations(rawRecs, catalog);

            try {
                await query(
                    'INSERT INTO ai_tutor_messages (user_id, role, content, course_id) VALUES (?, ?, ?, ?)',
                    [userId, 'user', message, courseId]
                );
                await query(
                    'INSERT INTO ai_tutor_messages (user_id, role, content, course_id) VALUES (?, ?, ?, ?)',
                    [userId, 'assistant', safeReply, courseId]
                );
            } catch (dbErr) {
                console.error('ai_tutor_messages insert:', dbErr);
                return apiResponse(res, 500, 'Could not save conversation');
            }

            setImmediate(() => {
                maybeRefreshLearningProfile(userId).catch(() => {});
            });

            return apiResponse(res, 200, 'OK', { reply: safeReply, recommendations });
        },

        async history(req, res) {
            const userId = req.user.id;
            let limit = parseInt(req.query.limit, 10);
            if (Number.isNaN(limit)) limit = 30;
            limit = Math.min(50, Math.max(1, limit));

            try {
                const rows = await query(
                    `SELECT id, role, content, course_id, created_at FROM ai_tutor_messages
                     WHERE user_id = ? ORDER BY created_at DESC LIMIT ?`,
                    [userId, limit]
                );
                rows.reverse();
                return apiResponse(res, 200, 'OK', rows);
            } catch (e) {
                console.error('ai tutor history:', e);
                return apiResponse(res, 500, 'Could not load history');
            }
        }
    };
};
