/**
 * Content Editor AI Help: OpenRouter-backed authoring assistant with structured actions.
 */

const ALLOWED_ACTION_TYPES = new Set([
    'insert_html',
    'add_question',
    'add_phet',
    'add_latex',
    'add_marketplace_sim',
    'suggest_sims',
    'validate_report'
]);

const EDITOR_SYSTEM = `You are VeeLearn's content editor assistant for course authors.
Help teachers build lessons by returning structured editor actions.

CRITICAL OUTPUT FORMAT (follow exactly):
1) First line must be exactly: VEELEARN_EDITOR_ACTIONS_JSON:
2) Immediately after that, a single JSON array of action objects (no markdown fences, no commentary inside the array).
3) After the JSON array, optionally add a short human reply (under 60 words).
Putting JSON FIRST is required so long lessons are not truncated before actions appear.

Rules:
- Never ask clarifying questions when the user already gave a topic or outline — start generating immediately.
- Prefer concrete teaching content over fluff.
- When the user asks to add a quiz, PhET sim, LaTeX, marketplace sim, or a full lesson, emit actions.
- For bulk/section lessons, return an ordered list of actions mixing insert_html, add_latex, add_phet, and add_question.
- For expand/simplify modes: rewrite the provided selection and emit insert_html with the result.
- For check_question mode: emit add_question that checks understanding of the selection.
- For topics or resource paste: emit suggest_sims and/or add_phet with a clear query/title.
- Never invent marketplace simulator IDs; use suggest_sims with a search query instead.
- PhET: use add_phet with payload.query or payload.title matching common PhET names (e.g. "Area Model Algebra", "Graphing Quadratics", "Proportion Playground", "Equation Grapher").
- LaTeX: use add_latex with payload.latex (raw TeX without $) and payload.display (true for $$). Content is inserted inline automatically.
- Quiz: use add_question with question_text, question_type (multiple_choice|true_false|short_answer), options (string array for MC), correct_answer, explanation (include step-by-step solution), points.
- HTML: use insert_html with payload.html as simple safe markup (h2, h3, p, strong, em, ul, ol, li, br only).
- SECTION mode: generate ONLY the requested section (theory + sim + practice). Do not generate other modules.
- Keep the JSON array complete and valid. Prefer fewer complete actions over truncated JSON.
- Example shape: [{"type":"insert_html","payload":{"html":"<h3>Title</h3><p>Theory...</p>"}},{"type":"add_latex","payload":{"latex":"a^2-b^2=(a-b)(a+b)","display":true}},{"type":"add_phet","payload":{"query":"Area Model Algebra"}},{"type":"add_question","payload":{"question_text":"...","question_type":"multiple_choice","options":["A","B","C","D"],"correct_answer":"A","explanation":"...","points":10}}]`;

function stripUnsafeHtml(html) {
    if (typeof html !== 'string') return '';
    let s = html.slice(0, 12000);
    s = s.replace(/<\s*script[\s\S]*?>[\s\S]*?<\s*\/\s*script\s*>/gi, '');
    s = s.replace(/\son\w+\s*=\s*(['"]).*?\1/gi, '');
    s = s.replace(/\son\w+\s*=\s*[^\s>]+/gi, '');
    s = s.replace(/javascript\s*:/gi, '');
    s = s.replace(/<\s*(iframe|object|embed|link|meta|form|input|button|svg|math)[\s\S]*?>/gi, '');
    s = s.replace(/<\/\s*(iframe|object|embed|form|button|svg|math)\s*>/gi, '');
    return s;
}

function tryParseActionsJson(jsonPart) {
    if (!jsonPart || typeof jsonPart !== 'string') return [];
    let s = jsonPart.trim();
    // Strip markdown fences
    s = s.replace(/^```(?:json)?\s*/i, '').replace(/\s*```$/i, '').trim();

    const attempts = [];
    attempts.push(s);

    const start = s.indexOf('[');
    const end = s.lastIndexOf(']');
    if (start >= 0 && end > start) {
        attempts.push(s.slice(start, end + 1));
    }

    // Object wrapper: {"actions":[...]} or {"type":...}
    const objStart = s.indexOf('{');
    if (objStart >= 0) {
        const objEnd = s.lastIndexOf('}');
        if (objEnd > objStart) attempts.push(s.slice(objStart, objEnd + 1));
    }

    // Truncation repair: close open brackets if JSON was cut mid-stream
    if (start >= 0 && (end < 0 || end < start)) {
        let fragment = s.slice(start);
        // Drop trailing incomplete string/object piece after last complete element
        const lastComplete = Math.max(fragment.lastIndexOf('},'), fragment.lastIndexOf('}]'));
        if (lastComplete > 0) {
            fragment = fragment.slice(0, lastComplete + 1);
        }
        const opens = (fragment.match(/\[/g) || []).length;
        const closes = (fragment.match(/\]/g) || []).length;
        const openBraces = (fragment.match(/\{/g) || []).length;
        const closeBraces = (fragment.match(/\}/g) || []).length;
        // Close dangling braces then arrays
        fragment += '}'.repeat(Math.max(0, openBraces - closeBraces));
        fragment += ']'.repeat(Math.max(0, opens - closes));
        attempts.push(fragment);
    }

    for (const attempt of attempts) {
        try {
            const parsed = JSON.parse(attempt);
            if (Array.isArray(parsed)) return parsed;
            if (parsed && typeof parsed === 'object') {
                if (Array.isArray(parsed.actions)) return parsed.actions;
                if (parsed.type) return [parsed];
            }
        } catch (_) {
            /* try next */
        }
    }
    return [];
}

function splitReplyAndActions(raw) {
    const text = String(raw || '');
    const markers = [
        '\nVEELEARN_EDITOR_ACTIONS_JSON:',
        'VEELEARN_EDITOR_ACTIONS_JSON:',
        '\n```json',
        '```json'
    ];

    let idx = -1;
    let markerLen = 0;
    for (const m of markers) {
        const i = text.indexOf(m);
        if (i >= 0 && (idx < 0 || i < idx)) {
            idx = i;
            markerLen = m.length;
        }
    }

    // Prefer explicit marker; otherwise hunt for first JSON array of actions
    if (idx < 0) {
        const arrStart = text.search(/\[[\s\S]*?"type"\s*:/);
        if (arrStart >= 0) {
            const rawActions = tryParseActionsJson(text.slice(arrStart));
            const replyText = text.slice(0, arrStart).trim();
            return { replyText, rawActions };
        }
        return { replyText: text.trim(), rawActions: [] };
    }

    const before = text.slice(0, idx).trim();
    const after = text.slice(idx + markerLen).trim();
    const rawActions = tryParseActionsJson(after);

    // If JSON came first, reply may be after the array
    let replyText = before;
    if (!replyText && rawActions.length) {
        const endBracket = after.lastIndexOf(']');
        if (endBracket >= 0) {
            replyText = after.slice(endBracket + 1).replace(/^```\s*/i, '').trim();
        }
    }

    return { replyText, rawActions };
}

function normalizeQuestionPayload(payload) {
    const p = payload && typeof payload === 'object' ? payload : {};
    const question_type = ['multiple_choice', 'true_false', 'short_answer', 'fill_in_blank_with_image'].includes(p.question_type)
        ? p.question_type
        : 'multiple_choice';
    let options = null;
    if (question_type === 'multiple_choice' && Array.isArray(p.options)) {
        options = p.options.map((o) => String(o).slice(0, 500)).filter(Boolean).slice(0, 8);
        if (options.length < 2) options = null;
    }
    if (question_type === 'true_false') {
        options = ['True', 'False'];
    }
    const points = Math.min(100, Math.max(1, parseInt(p.points, 10) || 10));
    return {
        question_text: String(p.question_text || '').slice(0, 4000),
        question_type,
        options,
        correct_answer: String(p.correct_answer != null ? p.correct_answer : '').slice(0, 2000),
        explanation: String(p.explanation || '').slice(0, 2000),
        points
    };
}

function validateActions(rawActions) {
    const out = [];
    for (const a of rawActions) {
        if (!a || typeof a !== 'object') continue;
        const type = String(a.type || '').trim();
        if (!ALLOWED_ACTION_TYPES.has(type)) continue;
        const payload = a.payload && typeof a.payload === 'object' ? a.payload : {};

        if (type === 'insert_html') {
            const html = stripUnsafeHtml(String(payload.html || payload.text || ''));
            if (!html.trim()) continue;
            out.push({ type, payload: { html } });
        } else if (type === 'add_question') {
            const q = normalizeQuestionPayload(payload);
            if (!q.question_text.trim()) continue;
            // Soften MC: if options missing/invalid, fall back to short_answer
            if (q.question_type === 'multiple_choice' && (!q.options || q.options.length < 2)) {
                q.question_type = 'short_answer';
                q.options = null;
            }
            if (!q.correct_answer.trim()) {
                // Last resort: use first option or placeholder so content still inserts
                if (Array.isArray(q.options) && q.options.length) {
                    q.correct_answer = String(q.options[0]);
                } else {
                    q.correct_answer = 'See explanation';
                }
            }
            out.push({ type, payload: q });
        } else if (type === 'add_phet') {
            const query = String(payload.query || payload.title || '').slice(0, 200).trim();
            if (!query) continue;
            out.push({ type, payload: { query, title: String(payload.title || query).slice(0, 200) } });
        } else if (type === 'add_latex') {
            const latex = String(payload.latex || '').replace(/^\$+|\$+$/g, '').trim().slice(0, 2000);
            if (!latex) continue;
            out.push({ type, payload: { latex, display: !!payload.display } });
        } else if (type === 'add_marketplace_sim') {
            const id = parseInt(payload.simulatorId ?? payload.id, 10);
            if (Number.isNaN(id)) continue;
            out.push({
                type,
                payload: {
                    simulatorId: id,
                    title: String(payload.title || 'Marketplace Simulator').slice(0, 200)
                }
            });
        } else if (type === 'suggest_sims') {
            out.push({
                type,
                payload: {
                    query: String(payload.query || '').slice(0, 200),
                    reason: String(payload.reason || '').slice(0, 300),
                    suggestions: Array.isArray(payload.suggestions) ? payload.suggestions.slice(0, 5) : []
                }
            });
        } else if (type === 'validate_report') {
            out.push({
                type,
                payload: {
                    findings: Array.isArray(payload.findings)
                        ? payload.findings.map((f) => String(f).slice(0, 400)).slice(0, 20)
                        : []
                }
            });
        }

        if (out.length >= 50) break;
    }
    return out;
}

async function enrichSuggestSims(actions, queryFn) {
    const enriched = [];
    for (const action of actions) {
        if (action.type !== 'suggest_sims') {
            enriched.push(action);
            continue;
        }
        const search = (action.payload.query || '').trim();
        let suggestions = Array.isArray(action.payload.suggestions) ? [...action.payload.suggestions] : [];
        if (search && queryFn) {
            try {
                const rows = await queryFn(
                    `SELECT s.id, s.title, s.description
                     FROM simulators s
                     WHERE (s.is_blocked IS NULL OR s.is_blocked = FALSE)
                       AND (s.title LIKE ? OR s.description LIKE ? OR s.tags LIKE ?)
                     ORDER BY s.downloads DESC, s.created_at DESC
                     LIMIT 5`,
                    [`%${search}%`, `%${search}%`, `%${search}%`]
                );
                const fromDb = (rows || []).map((r) => ({
                    id: r.id,
                    title: r.title,
                    source: 'marketplace'
                }));
                const seen = new Set(suggestions.map((s) => s.id).filter(Boolean));
                for (const s of fromDb) {
                    if (!seen.has(s.id)) {
                        suggestions.push(s);
                        seen.add(s.id);
                    }
                }
            } catch (e) {
                console.warn('suggest_sims enrichment skipped:', e.message);
            }
        }
        enriched.push({
            type: 'suggest_sims',
            payload: {
                query: search,
                reason: action.payload.reason || '',
                suggestions: suggestions.slice(0, 5)
            }
        });
    }
    return enriched;
}

module.exports = function createAiEditorHelpHandlers({ query, openRouterChatCompletion, apiResponse, getOpenRouterKeys }) {
    async function loadHistoryMessages(userId, courseId, limit = 20) {
        if (!userId || !courseId) return [];
        try {
            const rows = await query(
                `SELECT role, content FROM ai_editor_help_messages
                 WHERE user_id = ? AND course_id = ?
                 ORDER BY created_at DESC LIMIT ?`,
                [userId, courseId, limit]
            );
            return (rows || []).reverse();
        } catch (e) {
            console.error('ai editor help load history:', e.message);
            return [];
        }
    }

    async function persistTurn(userId, courseId, userText, assistantText) {
        if (!userId || !courseId) return;
        try {
            if (userText) {
                await query(
                    'INSERT INTO ai_editor_help_messages (user_id, course_id, role, content) VALUES (?, ?, ?, ?)',
                    [userId, courseId, 'user', String(userText).slice(0, 16000)]
                );
            }
            if (assistantText) {
                await query(
                    'INSERT INTO ai_editor_help_messages (user_id, course_id, role, content) VALUES (?, ?, ?, ?)',
                    [userId, courseId, 'assistant', String(assistantText).slice(0, 16000)]
                );
            }
        } catch (e) {
            console.error('ai editor help persist:', e.message);
        }
    }

    return {
        async history(req, res) {
            const userId = req.user?.id;
            const courseId = parseInt(req.query?.courseId, 10);
            if (!userId) return apiResponse(res, 401, 'Unauthorized');
            if (!courseId || Number.isNaN(courseId)) return apiResponse(res, 400, 'courseId is required');

            try {
                const rows = await query(
                    `SELECT id, role, content, course_id, created_at FROM ai_editor_help_messages
                     WHERE user_id = ? AND course_id = ?
                     ORDER BY created_at ASC LIMIT 100`,
                    [userId, courseId]
                );
                return apiResponse(res, 200, 'OK', rows || []);
            } catch (e) {
                console.error('ai editor help history:', e);
                return apiResponse(res, 500, 'Could not load history');
            }
        },

        async clearHistory(req, res) {
            const userId = req.user?.id;
            const courseId = parseInt(req.query?.courseId || req.body?.courseId, 10);
            if (!userId) return apiResponse(res, 401, 'Unauthorized');
            if (!courseId || Number.isNaN(courseId)) return apiResponse(res, 400, 'courseId is required');

            try {
                await query(
                    'DELETE FROM ai_editor_help_messages WHERE user_id = ? AND course_id = ?',
                    [userId, courseId]
                );
                return apiResponse(res, 200, 'History cleared');
            } catch (e) {
                console.error('ai editor help clear:', e);
                return apiResponse(res, 500, 'Could not clear history');
            }
        },

        async help(req, res) {
            const keys = typeof getOpenRouterKeys === 'function' ? getOpenRouterKeys() : [];
            if (!keys.length) {
                return apiResponse(res, 503, 'AI Help is not configured (missing OpenRouter keys)');
            }

            let message = typeof req.body?.message === 'string' ? req.body.message.trim() : '';
            const mode = typeof req.body?.mode === 'string' ? req.body.mode.trim() : 'chat';
            let selection = typeof req.body?.selection === 'string' ? req.body.selection.trim() : '';
            let editorSnippet = typeof req.body?.editorSnippet === 'string' ? req.body.editorSnippet.trim() : '';
            let phetCatalogSummary =
                typeof req.body?.phetCatalogSummary === 'string' ? req.body.phetCatalogSummary.trim() : '';

            if (!message && mode !== 'validate' && !selection) {
                return apiResponse(res, 400, 'Message is required');
            }
            const maxMsg = mode === 'section' ? 14000 : 8000;
            if (message.length > maxMsg) message = message.slice(0, maxMsg);
            if (selection.length > 6000) selection = selection.slice(0, 6000);
            if (editorSnippet.length > 4000) editorSnippet = editorSnippet.slice(0, 4000);
            if (phetCatalogSummary.length > 3000) phetCatalogSummary = phetCatalogSummary.slice(0, 3000);

            let courseId = null;
            if (req.body?.courseId != null && req.body.courseId !== '') {
                const cid = parseInt(req.body.courseId, 10);
                if (!Number.isNaN(cid)) courseId = cid;
            }

            const userId = req.user?.id;
            const prior = courseId && userId ? await loadHistoryMessages(userId, courseId, 20) : [];

            const modeHints = {
                expand: 'MODE: expand — rewrite the selection to be richer and clearer; emit insert_html.',
                simplify: 'MODE: simplify — rewrite the selection in simpler language; emit insert_html.',
                check_question: 'MODE: check_question — create one review quiz about the selection; emit add_question.',
                validate: 'MODE: validate — review the editor snippet for LaTeX/quiz issues; emit validate_report with findings.',
                section:
                    'MODE: section — Generate ONLY the requested section now. Include: (1) Core Theory as insert_html + add_latex formulas, (2) add_phet for the recommended simulation, (3) exactly 3 add_question practice problems with step-by-step explanations. Do not ask questions. Do not generate other sections.',
                chat: 'MODE: chat — follow the user request and emit appropriate actions. Never ask for more info if an outline/topic is already provided.'
            };

            const contextParts = [
                modeHints[mode] || modeHints.chat,
                courseId ? `courseId: ${courseId}` : 'courseId: (unsaved draft possible)',
                selection ? `SELECTED_TEXT:\n${selection}` : '',
                editorSnippet ? `EDITOR_SNIPPET:\n${editorSnippet}` : '',
                phetCatalogSummary ? `PHET_TITLES (sample):\n${phetCatalogSummary}` : '',
                `USER_REQUEST:\n${message || '(use mode instructions on selection/snippet)'}`
            ].filter(Boolean);

            const messages = [{ role: 'system', content: EDITOR_SYSTEM }];
            for (const row of prior) {
                if (row.role === 'user' || row.role === 'assistant') {
                    messages.push({ role: row.role, content: String(row.content || '').slice(0, 8000) });
                }
            }
            messages.push({ role: 'user', content: contextParts.join('\n\n') });

            const isSection = mode === 'section';
            let raw;
            try {
                raw = await openRouterChatCompletion(messages, {
                    temperature: 0.25,
                    max_tokens: isSection ? 4500 : 2200,
                    budgetMs: isSection ? 55000 : 40000
                });
            } catch (e) {
                if (e.code === 'OPENROUTER_NOT_CONFIGURED') {
                    return apiResponse(res, 503, 'AI Help is not configured (missing OpenRouter keys)');
                }
                if (e.code === 'OPENROUTER_RATE_LIMITED' || e.status === 429) {
                    return apiResponse(
                        res,
                        429,
                        'AI is temporarily rate-limited. Please wait about a minute and try again.'
                    );
                }
                if (e.code === 'OPENROUTER_MODEL_UNAVAILABLE' || e.status === 404) {
                    return apiResponse(
                        res,
                        503,
                        'AI model is temporarily unavailable on OpenRouter. Please try again shortly.'
                    );
                }
                if (e.code === 'OPENROUTER_TIMEOUT') {
                    return apiResponse(res, 504, 'AI Help timed out. Please try a shorter request.');
                }
                console.error('AI editor help OpenRouter error:', e.message);
                return apiResponse(res, 502, 'AI Help request failed. Please try again.');
            }

            const { replyText, rawActions } = splitReplyAndActions(raw);
            let actions = validateActions(rawActions);

            // If the model wrote prose but forgot/truncated JSON, still place content
            if (!actions.length && replyText && replyText.length > 40) {
                const paras = replyText
                    .split(/\n{2,}/)
                    .map((p) => p.trim())
                    .filter(Boolean)
                    .slice(0, 12)
                    .map((p) => `<p>${String(p).replace(/</g, '&lt;').replace(/>/g, '&gt;')}</p>`)
                    .join('');
                if (paras) {
                    actions.push({ type: 'insert_html', payload: { html: paras } });
                }
            }

            actions = await enrichSuggestSims(actions, query);

            const reply =
                replyText || (actions.length ? 'Inserted content into the editor.' : 'Done.');

            const userPersist =
                message ||
                (mode === 'expand'
                    ? 'Expand selection'
                    : mode === 'simplify'
                      ? 'Simplify selection'
                      : mode === 'check_question'
                        ? 'Add check question'
                        : mode === 'validate'
                          ? 'Validate page'
                          : mode);

            await persistTurn(userId, courseId, userPersist, reply);

            return apiResponse(res, 200, 'OK', {
                reply,
                actions
            });
        }
    };
};
