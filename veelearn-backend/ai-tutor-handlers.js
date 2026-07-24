/**
 * Study coach: OpenRouter-backed chat with Socratic constraints and validated recommendations.
 */

const SOCRATIC_SYSTEM = `You are a study coach for Veelearn. Your job is to help students learn using real courses on this platform, not to do their work for them.

Rules (strict):
- Never give final numeric answers, final multiple-choice answers, or copy-paste solutions.
- Never provide complete code that solves an assignment; at most a tiny illustrative snippet with placeholders, or describe the algorithm in words.
- Give at most ONE clear next step: a question to ask themselves, a hint about which concept to review, or how to set up the problem.
- If they demand the answer, briefly refuse and offer a learning step instead.
- Keep responses concise (under 180 words unless they ask for more detail on the method).
- Match their level. If they say they are in grades 1–3 / elementary / don't know basic math, do NOT suggest algebra, competition math, or advanced topics. Prefer AVAILABLE_COURSES whose grade_level and title/description match their request.
- NEVER invent course titles. Only recommend courses that appear in AVAILABLE_COURSES. If the list is empty, say so and coach without naming fake courses.

Course recommendations (required when relevant):
- When the learner asks for a course, says what they want to learn, mentions a grade/level, or is clearly looking for where to start, you MUST recommend 2–3 courses from AVAILABLE_COURSES (or 1 if only one fits).
- Prefer higher like_count when several fit. Prefer matching grade_level. Mix single and master when both fit.
- Always end those turns with a new line exactly:
VEELEARN_RECOMMEND_JSON:
followed by a single JSON array like [{"courseId":123,"title":"Exact title from list","reason":"one short sentence"}].
- Use only courseIds from AVAILABLE_COURSES. If nothing fits, omit VEELEARN_RECOMMEND_JSON and say nothing in the catalog matches yet.`;

function guardSocraticReply(text) {
    if (!text || typeof text !== 'string') return text;
    const t = text.trim();
    if (/^\d+(\.\d+)?$/.test(t)) {
        return "I can't give a final answer like that. What is the first relationship or formula that applies? Try writing what you know and what you need to find.";
    }
    return text;
}

function splitReplyAndRecommendations(raw) {
    if (!raw || typeof raw !== 'string') {
        return { replyText: '', rawRecs: [] };
    }

    const markerRe = /\n?\s*VEELEARN_RECOMMEND_JSON:\s*/i;
    const match = raw.match(markerRe);
    let replyText = raw;
    let jsonPart = '';

    if (match && match.index != null) {
        replyText = raw.slice(0, match.index).trim();
        jsonPart = raw.slice(match.index + match[0].length).trim();
    } else {
        // Model sometimes dumps JSON without the marker
        const bare = raw.match(/(\[[\s\S]*"courseId"[\s\S]*\])/);
        if (bare) {
            jsonPart = bare[1];
            replyText = raw.replace(bare[0], '').trim();
        }
    }

    let rawRecs = [];
    if (jsonPart) {
        // Strip markdown fences if present
        jsonPart = jsonPart.replace(/^```(?:json)?\s*/i, '').replace(/\s*```$/i, '').trim();
        try {
            const parsed = JSON.parse(jsonPart);
            if (Array.isArray(parsed)) rawRecs = parsed;
        } catch (_) {
            const arrMatch = jsonPart.match(/\[[\s\S]*\]/);
            if (arrMatch) {
                try {
                    const parsed = JSON.parse(arrMatch[0]);
                    if (Array.isArray(parsed)) rawRecs = parsed;
                } catch (__) {
                    /* ignore malformed JSON */
                }
            }
        }
    }

    return { replyText: replyText.trim(), rawRecs };
}

function validateRecommendations(rawRecs, allowedCatalog) {
    const byId = new Map(allowedCatalog.map((c) => [Number(c.id), c]));
    const out = [];
    const seen = new Set();
    for (const r of rawRecs) {
        const id = parseInt(r?.courseId ?? r?.id, 10);
        if (Number.isNaN(id) || seen.has(id)) continue;
        const row = byId.get(id);
        if (!row) continue;
        seen.add(id);
        out.push({
            courseId: id,
            title: row.title,
            courseType: row.course_type || 'single',
            gradeLevel: row.grade_level != null ? Number(row.grade_level) : null,
            likeCount: Number(row.like_count) || 0,
            reason: typeof r.reason === 'string' ? r.reason.slice(0, 240) : 'A good match from Veelearn for what you asked.'
        });
        if (out.length >= 3) break;
    }
    return out;
}

function extractGradeHints(message) {
    const msg = String(message || '').toLowerCase();
    const grades = new Set();

    const range = msg.match(/\b(?:grades?\s*)?(\d{1,2})\s*[-–to]+\s*(\d{1,2})(?:\s*(?:st|nd|rd|th)?\s*grade)?\b/);
    if (range) {
        const a = parseInt(range[1], 10);
        const b = parseInt(range[2], 10);
        if (!Number.isNaN(a) && !Number.isNaN(b)) {
            const lo = Math.min(a, b);
            const hi = Math.max(a, b);
            for (let g = lo; g <= hi && g <= 13; g++) grades.add(g);
        }
    }

    const singles = msg.matchAll(/\b(?:grade\s*)?(\d{1,2})(?:st|nd|rd|th)?\s*grade\b/g);
    for (const m of singles) {
        const g = parseInt(m[1], 10);
        if (!Number.isNaN(g) && g >= 1 && g <= 13) grades.add(g);
    }

    if (/\b(elementary|primary|k-?5|kindergarten)\b/.test(msg)) {
        [1, 2, 3, 4, 5].forEach((g) => grades.add(g));
    }
    if (/\b(middle\s*school|junior\s*high)\b/.test(msg)) {
        [6, 7, 8].forEach((g) => grades.add(g));
    }
    if (/\b(high\s*school|secondary)\b/.test(msg)) {
        [9, 10, 11, 12].forEach((g) => grades.add(g));
    }
    if (/\b(1st|first)\s*grade\b/.test(msg)) grades.add(1);
    if (/\b(2nd|second)\s*grade\b/.test(msg)) grades.add(2);
    if (/\b(3rd|third)\s*grade\b/.test(msg)) grades.add(3);

    return [...grades];
}

function tokenizeForMatch(text) {
    return String(text || '')
        .toLowerCase()
        .replace(/[^a-z0-9\s+#]/g, ' ')
        .split(/\s+/)
        .filter((w) => w.length > 2 && !['the', 'and', 'for', 'want', 'learn', 'course', 'with', 'that', 'this', 'have', 'dont', "don't", 'know', 'please', 'recommend', 'something', 'about'].includes(w));
}

function wantsCourseRecommendation(message) {
    const msg = String(message || '').toLowerCase();
    return (
        /\b(recommend|suggestion|suggest|enroll|course|learn|stud(y|ying)|teach me|where (do|should) i start|help me (with|learn)|grade|math|science|physics|chem|algebra|geometry|bio)\b/.test(
            msg
        ) || extractGradeHints(msg).length > 0
    );
}

/**
 * Server-side ranking when the model forgets VEELEARN_RECOMMEND_JSON.
 */
function fallbackRecommendations(message, catalog, limit = 3) {
    if (!catalog?.length) return [];
    const msg = String(message || '').toLowerCase();
    const grades = extractGradeHints(msg);
    const tokens = tokenizeForMatch(msg);

    const scored = catalog.map((c) => {
        const title = String(c.title || '').toLowerCase();
        const desc = String(c.desc_preview || c.description || '').toLowerCase();
        const hay = `${title} ${desc}`;
        let score = Number(c.like_count) || 0;

        for (const t of tokens) {
            if (title.includes(t)) score += 12;
            else if (hay.includes(t)) score += 6;
        }

        const g = c.grade_level != null ? Number(c.grade_level) : null;
        if (grades.length && g != null && grades.includes(g)) score += 40;
        else if (grades.length && g != null) {
            const near = grades.some((x) => Math.abs(x - g) <= 1);
            score += near ? 15 : -25;
        }

        // Penalize advanced-sounding titles when learner asked for elementary
        if (grades.length && grades.every((x) => x <= 5)) {
            if (/\b(algebra|calculus|competition|amc|amc\s*8|olympiad|trigonometry|linear algebra)\b/i.test(hay)) {
                score -= 50;
            }
            if (/\b(addition|subtraction|counting|number|fraction|multiply|division|grade|elementary|basic)\b/i.test(hay)) {
                score += 20;
            }
        }

        return { course: c, score };
    });

    scored.sort((a, b) => b.score - a.score || (Number(b.course.like_count) || 0) - (Number(a.course.like_count) || 0));

    const top = scored.filter((s) => s.score > 0).slice(0, limit);
    const pick = top.length ? top : scored.slice(0, Math.min(limit, scored.length));

    return pick.map(({ course: row }) => ({
        courseId: Number(row.id),
        title: row.title,
        courseType: row.course_type || 'single',
        gradeLevel: row.grade_level != null ? Number(row.grade_level) : null,
        likeCount: Number(row.like_count) || 0,
        reason: grades.length
            ? `Matches what you asked for around grades ${grades.join('–')}.`
            : 'A popular Veelearn course that fits what you asked about.'
    }));
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
                    'Summarize in 3-5 short bullet points how this student tends to learn: question style, common struggles, pace, and grade/level if known. No PII, no email. Plain text bullets only.'
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
                `SELECT c.id, c.title, c.course_type, c.grade_level, IFNULL(c.like_count, 0) AS like_count,
                        LEFT(IFNULL(c.description,''), 220) AS desc_preview
                 FROM courses c
                 WHERE c.status = 'approved'
                 AND c.id NOT IN (SELECT course_id FROM enrollments WHERE user_id = ?)
                 ORDER BY IFNULL(c.like_count, 0) DESC, c.title ASC LIMIT 80`,
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

            const availableLines = catalog
                .map((c) => {
                    const g = c.grade_level != null ? `grade=${c.grade_level}` : 'grade=any';
                    const d = String(c.desc_preview || '').replace(/\s+/g, ' ').trim();
                    return `${c.id}: ${c.title} [${c.course_type || 'single'}, ${g}, likes=${c.like_count || 0}] ${d ? `— ${d}` : ''}`;
                })
                .join('\n');
            const enrolledLines = enrolled.map((c) => `${c.id}: ${c.title}`).join('\n') || '(none)';

            const contextBlock = [
                `Enrolled courses:\n${enrolledLines}`,
                `Quiz attempts (all time): ${correctQ} correct of ${totalQ} recorded.`,
                courseTitle ? `Current course context: "${courseTitle}" (id ${courseId}).` : 'No specific course context.',
                profileSummary ? `Learning profile notes:\n${profileSummary}` : '',
                `AVAILABLE_COURSES (not enrolled; suggest ONLY from this list; include grade_level when matching):\n${availableLines || '(none available)'}`
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
                if (e.code === 'OPENROUTER_MODEL_UNAVAILABLE' || e.status === 404) {
                    return apiResponse(
                        res,
                        503,
                        'Study coach model is temporarily unavailable. Please try again shortly.'
                    );
                }
                return apiResponse(res, 502, 'Study coach is temporarily unavailable. Please try again later.');
            }

            const { replyText, rawRecs } = splitReplyAndRecommendations(rawReply);
            let safeReply = guardSocraticReply(replyText);
            let recommendations = validateRecommendations(rawRecs, catalog);

            // If the model skipped / invented recs, fill from catalog when the user is clearly looking for courses
            if (!recommendations.length && catalog.length && wantsCourseRecommendation(message)) {
                recommendations = fallbackRecommendations(message, catalog, 3);
                if (recommendations.length && !/veelearn course|recommended course|here are (a few )?courses/i.test(safeReply)) {
                    safeReply = `${safeReply}\n\nI picked a few Veelearn courses that fit — tap View / Enroll below to open one.`.trim();
                }
            }

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
