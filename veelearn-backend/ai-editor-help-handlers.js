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
3) After the JSON array, optionally add a short human reply (under 40 words).
Putting JSON FIRST is required so long lessons are not truncated before actions appear.

JSON ESCAPING (critical — invalid JSON is discarded):
- In every JSON string, backslashes must be doubled. For LaTeX write "\\\\frac{n}{k}" not "\\frac{n}{k}".
- Prefer putting formulas inside insert_html as $...$ / $$...$$ text instead of add_latex when unsure about escaping.
- Prefer short_answer questions over multiple_choice when options are long (fewer JSON commas/quotes to break).

Rules:
- Never ask clarifying questions when the user already gave a topic or outline — start generating immediately.
- Prefer concrete teaching content over fluff.
- When the user asks to add a quiz, PhET sim, LaTeX, marketplace sim, or a full lesson, emit actions.
- For bulk/section lessons, return an ordered list of actions mixing insert_html, add_latex, add_phet, and add_question.
- For expand/simplify modes: rewrite the provided selection and emit insert_html.
- For check_question mode: emit add_question that checks understanding of the selection.
- Never invent marketplace simulator IDs; use suggest_sims with a search query instead.
- PhET: use add_phet with payload.query matching a real PhET title closely (e.g. "Plinko Probability", "Area Model Algebra", "Graphing Quadratics"). Do NOT invent titles; if unsure omit add_phet.
- Quiz: use add_question with question_text, question_type (multiple_choice|true_false|short_answer), options (string array for MC), correct_answer, explanation (step-by-step), points.
- HTML: use insert_html with payload.html as simple safe markup (h2, h3, p, strong, em, ul, ol, li, br only). Put example problems and worked solutions in the HTML.
- SECTION mode: generate ONLY the requested section. Always include at least one insert_html with substantive theory + examples. Then 2–3 add_question items. Optional: one add_phet, optional add_latex.
- Keep the JSON array complete and valid. Prefer fewer complete actions over truncated JSON.
- Minimum viable section: [{"type":"insert_html","payload":{"html":"<h3>Title</h3><p>Theory...</p><p>Example...</p>"}},{"type":"add_question","payload":{"question_text":"...","question_type":"short_answer","correct_answer":"...","explanation":"...","points":10}}]`;

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

/**
 * Fix invalid / LaTeX-corrupted backslash escapes inside JSON string literals.
 * Turns `\frac` / `\neq` into `\\frac` / `\\neq` while keeping real JSON escapes
 * like `\n` before a quote/space/punctuation.
 */
function repairJsonStringEscapes(input) {
    const s = String(input || '');
    let out = '';
    let inString = false;
    let escaped = false;
    for (let i = 0; i < s.length; i++) {
        const ch = s[i];
        if (!inString) {
            if (ch === '"') inString = true;
            out += ch;
            continue;
        }
        if (escaped) {
            out += ch;
            escaped = false;
            continue;
        }
        if (ch === '\\') {
            const next = s[i + 1];
            if (next == null) {
                out += '\\\\';
                continue;
            }
            // Always-safe JSON escapes
            if ('"\\/'.includes(next)) {
                out += ch;
                escaped = true;
                continue;
            }
            if (next === 'u' && /^[0-9a-fA-F]{4}/.test(s.slice(i + 2, i + 6))) {
                out += ch;
                escaped = true;
                continue;
            }
            // \b \f \n \r \t are valid JSON, but LaTeX macros use the same letters
            // (\neq, \frac, \times, \binom, \rightarrow). If a letter follows, treat as LaTeX.
            if ('bfnrt'.includes(next)) {
                const after = s[i + 2];
                if (after && /[a-zA-Z]/.test(after)) {
                    out += '\\\\';
                    continue;
                }
                out += ch;
                escaped = true;
                continue;
            }
            // Any other escape (e.g. \a, \c for LaTeX) — double the backslash
            out += '\\\\';
            continue;
        }
        if (ch === '"') {
            inString = false;
            out += ch;
            continue;
        }
        out += ch;
    }
    return out;
}

function extractBalancedJsonArray(text) {
    const s = String(text || '');
    const start = s.indexOf('[');
    if (start < 0) return null;
    let depth = 0;
    let inString = false;
    let escaped = false;
    for (let i = start; i < s.length; i++) {
        const ch = s[i];
        if (inString) {
            if (escaped) {
                escaped = false;
                continue;
            }
            if (ch === '\\') {
                escaped = true;
                continue;
            }
            if (ch === '"') inString = false;
            continue;
        }
        if (ch === '"') {
            inString = true;
            continue;
        }
        if (ch === '[') depth += 1;
        else if (ch === ']') {
            depth -= 1;
            if (depth === 0) return s.slice(start, i + 1);
        }
    }
    return s.slice(start); // truncated — caller may repair
}

function extractActionsByRegex(text) {
    const s = String(text || '');
    const actions = [];

    // insert_html blocks
    const htmlRe = /"type"\s*:\s*"insert_html"[\s\S]*?"html"\s*:\s*"((?:[^"\\]|\\.)*)"/gi;
    let m;
    while ((m = htmlRe.exec(s)) !== null) {
        try {
            const html = JSON.parse(`"${m[1]}"`);
            if (html && String(html).trim()) {
                actions.push({ type: 'insert_html', payload: { html: String(html) } });
            }
        } catch (_) {
            const loose = m[1]
                .replace(/\\n/g, '\n')
                .replace(/\\"/g, '"')
                .replace(/\\\\/g, '\\');
            if (loose.trim()) actions.push({ type: 'insert_html', payload: { html: loose } });
        }
    }

    // add_latex
    const latexRe = /"type"\s*:\s*"add_latex"[\s\S]*?"latex"\s*:\s*"((?:[^"\\]|\\.)*)"/gi;
    while ((m = latexRe.exec(s)) !== null) {
        try {
            const latex = JSON.parse(`"${m[1]}"`);
            if (latex && String(latex).trim()) {
                actions.push({ type: 'add_latex', payload: { latex: String(latex), display: true } });
            }
        } catch (_) {
            /* skip */
        }
    }

    // add_phet
    const phetRe = /"type"\s*:\s*"add_phet"[\s\S]*?"(?:query|title)"\s*:\s*"((?:[^"\\]|\\.)*)"/gi;
    while ((m = phetRe.exec(s)) !== null) {
        try {
            const query = JSON.parse(`"${m[1]}"`);
            if (query && String(query).trim()) {
                actions.push({ type: 'add_phet', payload: { query: String(query), title: String(query) } });
            }
        } catch (_) {
            /* skip */
        }
    }

    // add_question — capture nearby fields loosely
    const qBlocks = s.split(/"type"\s*:\s*"add_question"/i).slice(1);
    for (const block of qBlocks.slice(0, 8)) {
        const grab = (key) => {
            const re = new RegExp(`"${key}"\\s*:\\s*"((?:[^"\\\\]|\\\\.)*)"`, 'i');
            const mm = block.match(re);
            if (!mm) return '';
            try {
                return JSON.parse(`"${mm[1]}"`);
            } catch (_) {
                return mm[1].replace(/\\n/g, '\n').replace(/\\"/g, '"').replace(/\\\\/g, '\\');
            }
        };
        const question_text = grab('question_text');
        if (!question_text.trim()) continue;
        let options = null;
        const optMatch = block.match(/"options"\s*:\s*(\[[^\]]*\])/i);
        if (optMatch) {
            try {
                options = JSON.parse(repairJsonStringEscapes(optMatch[1]));
            } catch (_) {
                options = null;
            }
        }
        actions.push({
            type: 'add_question',
            payload: {
                question_text,
                question_type: options && options.length >= 2 ? 'multiple_choice' : 'short_answer',
                options,
                correct_answer: grab('correct_answer') || 'See explanation',
                explanation: grab('explanation'),
                points: 10
            }
        });
    }

    return actions;
}

function proseToHtml(text) {
    const raw = String(text || '').trim();
    if (!raw) return '';
    // Strip residual JSON marker noise
    let body = raw
        .replace(/^VEELEARN_EDITOR_ACTIONS_JSON:\s*/i, '')
        .replace(/^```(?:json)?\s*/i, '')
        .replace(/\s*```$/i, '')
        .trim();
    if (!body || body.length < 20) return '';
    // If it still looks like JSON, don't dump it as prose
    if (/^\s*[\[{]/.test(body) && /"type"\s*:/.test(body)) return '';

    const lines = body.split(/\n/);
    const parts = [];
    let listBuf = [];
    const flushList = () => {
        if (!listBuf.length) return;
        parts.push(`<ul>${listBuf.map((li) => `<li>${li}</li>`).join('')}</ul>`);
        listBuf = [];
    };
    for (const line of lines) {
        const t = line.trim();
        if (!t) {
            flushList();
            continue;
        }
        const esc = t.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        if (/^#{1,3}\s+/.test(t)) {
            flushList();
            const level = Math.min(3, (t.match(/^#+/) || ['#'])[0].length);
            const title = esc.replace(/^#+\s+/, '');
            parts.push(`<h${level + 1}>${title}</h${level + 1}>`);
        } else if (/^[-*•]\s+/.test(t)) {
            listBuf.push(esc.replace(/^[-*•]\s+/, ''));
        } else if (/^\d+[.)]\s+/.test(t)) {
            listBuf.push(esc.replace(/^\d+[.)]\s+/, ''));
        } else {
            flushList();
            parts.push(`<p>${esc}</p>`);
        }
    }
    flushList();
    return parts.join('').slice(0, 12000);
}

function tryParseActionsJson(jsonPart) {
    if (!jsonPart || typeof jsonPart !== 'string') return [];
    let s = jsonPart.trim();
    s = s.replace(/^```(?:json)?\s*/i, '').replace(/\s*```$/i, '').trim();

    const attempts = [];
    const balanced = extractBalancedJsonArray(s);
    if (balanced) attempts.push(balanced);
    attempts.push(s);

    const start = s.indexOf('[');
    const end = s.lastIndexOf(']');
    if (start >= 0 && end > start) attempts.push(s.slice(start, end + 1));

    const objStart = s.indexOf('{');
    if (objStart >= 0) {
        const objEnd = s.lastIndexOf('}');
        if (objEnd > objStart) attempts.push(s.slice(objStart, objEnd + 1));
    }

    // Truncation repair
    if (start >= 0 && (end < 0 || end < start)) {
        let fragment = s.slice(start);
        const lastComplete = Math.max(fragment.lastIndexOf('},'), fragment.lastIndexOf('}]'));
        if (lastComplete > 0) fragment = fragment.slice(0, lastComplete + 1);
        const opens = (fragment.match(/\[/g) || []).length;
        const closes = (fragment.match(/\]/g) || []).length;
        const openBraces = (fragment.match(/\{/g) || []).length;
        const closeBraces = (fragment.match(/\}/g) || []).length;
        fragment += '}'.repeat(Math.max(0, openBraces - closeBraces));
        fragment += ']'.repeat(Math.max(0, opens - closes));
        attempts.push(fragment);
    }

    // Prefer escape-repaired variants first (LaTeX \neq/\frac often "parse" but corrupt)
    const expanded = [];
    for (const a of attempts) {
        expanded.push(repairJsonStringEscapes(a));
        expanded.push(a);
    }

    for (const attempt of expanded) {
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

    // Last resort: regex salvage of individual actions from broken JSON
    return extractActionsByRegex(s);
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

    if (idx < 0) {
        const arrStart = text.search(/\[[\s\S]*?"type"\s*:/);
        if (arrStart >= 0) {
            const rawActions = tryParseActionsJson(text.slice(arrStart));
            const replyText = text.slice(0, arrStart).trim();
            return { replyText, rawActions, rawText: text };
        }
        return { replyText: text.trim(), rawActions: [], rawText: text };
    }

    const before = text.slice(0, idx).trim();
    const after = text.slice(idx + markerLen).trim();
    const rawActions = tryParseActionsJson(after);

    let replyText = before;
    if (!replyText && rawActions.length) {
        const endBracket = after.lastIndexOf(']');
        if (endBracket >= 0) {
            replyText = after.slice(endBracket + 1).replace(/^```\s*/i, '').trim();
        }
    }
    // If JSON failed, keep the full model text as reply candidate for prose fallback
    if (!rawActions.length && !replyText) {
        replyText = after.slice(0, 8000);
    }

    return { replyText, rawActions, rawText: text };
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
                    'MODE: section — Generate ONLY this section. REQUIRED: at least one insert_html (theory + worked examples with $LaTeX$ inline). Then 2–3 add_question (prefer short_answer). Optional one add_phet with a real PhET title. Optional add_latex only if escapes are correct (\\\\frac). Never ask questions. Never generate other sections. JSON must be valid.',
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
                    temperature: 0.2,
                    max_tokens: isSection ? 5000 : 2200,
                    budgetMs: isSection ? 60000 : 40000
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

            let { replyText, rawActions, rawText } = splitReplyAndActions(raw);
            let actions = validateActions(rawActions);

            // Server-side recovery retry for section mode when JSON/actions are empty
            if (!actions.length && isSection) {
                try {
                    const retryMessages = [
                        { role: 'system', content: EDITOR_SYSTEM },
                        {
                            role: 'user',
                            content: [
                                'CRITICAL: Previous reply had no usable editor actions.',
                                'Return ONLY valid JSON in this exact shape (no markdown, no prose before JSON):',
                                'VEELEARN_EDITOR_ACTIONS_JSON:',
                                '[{"type":"insert_html","payload":{"html":"<h3>Section Title</h3><p>Core theory with examples. Use $x^2$ for math.</p><p><strong>Example:</strong> worked solution...</p>"}},{"type":"add_question","payload":{"question_text":"Practice 1?","question_type":"short_answer","correct_answer":"answer","explanation":"steps","points":10}},{"type":"add_question","payload":{"question_type":"short_answer","question_text":"Practice 2?","correct_answer":"answer","explanation":"steps","points":10}}]',
                                'Fill with real content for this request (keep HTML under 2500 chars; no add_latex; no add_phet):',
                                message.slice(0, 5000)
                            ].join('\n')
                        }
                    ];
                    const retryRaw = await openRouterChatCompletion(retryMessages, {
                        temperature: 0.1,
                        max_tokens: 3500,
                        budgetMs: 45000
                    });
                    const parsedRetry = splitReplyAndActions(retryRaw);
                    const retryActions = validateActions(parsedRetry.rawActions);
                    if (retryActions.length) {
                        actions = retryActions;
                        replyText = parsedRetry.replyText || replyText;
                        rawText = parsedRetry.rawText || rawText;
                        raw = retryRaw;
                    } else if (!replyText && parsedRetry.replyText) {
                        replyText = parsedRetry.replyText;
                        rawText = parsedRetry.rawText || rawText;
                    }
                } catch (retryErr) {
                    console.warn('AI editor help section retry failed:', retryErr.message);
                }
            }

            // Prose / salvage fallback so the section is never empty
            if (!actions.length) {
                const html =
                    proseToHtml(replyText) ||
                    proseToHtml(rawText) ||
                    proseToHtml(String(raw || ''));
                if (html) {
                    actions.push({ type: 'insert_html', payload: { html } });
                }
            }

            // Ensure section responses always have theory HTML if we only got quizzes/phet
            if (isSection && actions.length && !actions.some((a) => a.type === 'insert_html')) {
                const html = proseToHtml(replyText) || proseToHtml(rawText);
                if (html) actions.unshift({ type: 'insert_html', payload: { html } });
            }

            actions = await enrichSuggestSims(actions, query);

            const reply =
                (replyText && !/^\s*[\[{]/.test(replyText) && replyText.length < 500
                    ? replyText
                    : '') ||
                (actions.length ? 'Inserted content into the editor.' : 'Done.');

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

// Test helpers (used by local scripts; not wired to HTTP)
module.exports._test = {
    repairJsonStringEscapes,
    tryParseActionsJson,
    splitReplyAndActions,
    proseToHtml,
    extractActionsByRegex,
    validateActions
};
