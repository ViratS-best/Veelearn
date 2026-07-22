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

Rules:
- Be concise in the human-readable reply (under 120 words).
- Prefer concrete teaching content over fluff.
- When the user asks to add a quiz, PhET sim, LaTeX, marketplace sim, or a full lesson, emit actions.
- For bulk lessons, return an ordered list of actions mixing insert_html, add_latex, add_phet, and add_question.
- For expand/simplify modes: rewrite the provided selection and emit insert_html with the result.
- For check_question mode: emit add_question that checks understanding of the selection.
- For topics or resource paste: emit suggest_sims and/or add_phet with a clear query/title.
- Never invent marketplace simulator IDs; use suggest_sims with a search query instead.
- PhET: use add_phet with payload.query or payload.title matching common PhET names.
- LaTeX: use add_latex with payload.latex (raw TeX without $) and payload.display (true for $$).
- Quiz: use add_question with question_text, question_type (multiple_choice|true_false|short_answer), options (string array for MC), correct_answer, explanation, points.
- HTML: use insert_html with payload.html as simple safe markup (p, strong, em, ul, ol, li, br only). Prefer plain paragraphs.
- Always end your message with a line exactly:
VEELEARN_EDITOR_ACTIONS_JSON:
followed by a single JSON array of action objects: [{"type":"...","payload":{...}}]
- If no editor changes are needed, use an empty array [].`;

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

function splitReplyAndActions(raw) {
    const marker = '\nVEELEARN_EDITOR_ACTIONS_JSON:';
    const alt = 'VEELEARN_EDITOR_ACTIONS_JSON:';
    let idx = raw.indexOf(marker);
    let markerLen = marker.length;
    if (idx < 0) {
        idx = raw.indexOf(alt);
        markerLen = alt.length;
    }
    if (idx < 0) {
        return { replyText: raw.trim(), rawActions: [] };
    }
    const replyText = raw.slice(0, idx).trim();
    const jsonPart = raw.slice(idx + markerLen).trim();
    let rawActions = [];
    try {
        const parsed = JSON.parse(jsonPart);
        if (Array.isArray(parsed)) rawActions = parsed;
    } catch (_) {
        const start = jsonPart.indexOf('[');
        const end = jsonPart.lastIndexOf(']');
        if (start >= 0 && end > start) {
            try {
                const parsed = JSON.parse(jsonPart.slice(start, end + 1));
                if (Array.isArray(parsed)) rawActions = parsed;
            } catch (__) {
                /* ignore */
            }
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
            if (!q.question_text.trim() || !q.correct_answer.trim()) continue;
            if (q.question_type === 'multiple_choice' && (!q.options || q.options.length < 2)) continue;
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

        if (out.length >= 40) break;
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
    return {
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
            if (message.length > 8000) message = message.slice(0, 8000);
            if (selection.length > 6000) selection = selection.slice(0, 6000);
            if (editorSnippet.length > 4000) editorSnippet = editorSnippet.slice(0, 4000);
            if (phetCatalogSummary.length > 3000) phetCatalogSummary = phetCatalogSummary.slice(0, 3000);

            let courseId = null;
            if (req.body?.courseId != null && req.body.courseId !== '') {
                const cid = parseInt(req.body.courseId, 10);
                if (!Number.isNaN(cid)) courseId = cid;
            }

            const modeHints = {
                expand: 'MODE: expand — rewrite the selection to be richer and clearer; emit insert_html.',
                simplify: 'MODE: simplify — rewrite the selection in simpler language; emit insert_html.',
                check_question: 'MODE: check_question — create one review quiz about the selection; emit add_question.',
                validate: 'MODE: validate — review the editor snippet for LaTeX/quiz issues; emit validate_report with findings.',
                chat: 'MODE: chat — follow the user request and emit appropriate actions.'
            };

            const contextParts = [
                modeHints[mode] || modeHints.chat,
                courseId ? `courseId: ${courseId}` : 'courseId: (unsaved draft possible)',
                selection ? `SELECTED_TEXT:\n${selection}` : '',
                editorSnippet ? `EDITOR_SNIPPET:\n${editorSnippet}` : '',
                phetCatalogSummary ? `PHET_TITLES (sample):\n${phetCatalogSummary}` : '',
                `USER_REQUEST:\n${message || '(use mode instructions on selection/snippet)'}`
            ].filter(Boolean);

            const messages = [
                { role: 'system', content: EDITOR_SYSTEM },
                { role: 'user', content: contextParts.join('\n\n') }
            ];

            let raw;
            try {
                raw = await openRouterChatCompletion(messages, {
                    temperature: 0.3,
                    max_tokens: 2500
                });
            } catch (e) {
                if (e.code === 'OPENROUTER_NOT_CONFIGURED') {
                    return apiResponse(res, 503, 'AI Help is not configured (missing OpenRouter keys)');
                }
                console.error('AI editor help OpenRouter error:', e.message);
                return apiResponse(res, 502, 'AI Help request failed');
            }

            const { replyText, rawActions } = splitReplyAndActions(raw);
            let actions = validateActions(rawActions);
            actions = await enrichSuggestSims(actions, query);

            return apiResponse(res, 200, 'OK', {
                reply: replyText || 'Done.',
                actions
            });
        }
    };
};
