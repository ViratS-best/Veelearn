/**
 * VeeLearn Content Editor — AI Help panel, skills, validation.
 * Depends on globals from script.js: API_BASE_URL, authToken, currentEditingCourseId,
 * courseBlocks, courseQuestions, PHET_SIMS, escapeHtml, insertQuizPlaceholder,
 * insertSimulatorBlock, loadCourseQuestions, saveCourse (optional).
 */
(function (global) {
    'use strict';

    let lastEditorAnchorEl = null;
    let aiHelpBusy = false;
    let latexPlacementPending = null;

    const BLOCK_SELECTOR =
        '.quiz-question-placeholder, .simulator-block, .phet-sim-wrapper, .latex-equation, p, h1, h2, h3, h4, li, div';

    function getEditor() {
        return document.getElementById('course-content-editor');
    }

    function esc(s) {
        if (typeof global.escapeHtml === 'function') return global.escapeHtml(s);
        return String(s == null ? '' : s)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    }

    function setLastAnchor(el) {
        if (!el || !getEditor() || !getEditor().contains(el)) return;
        lastEditorAnchorEl = el;
    }

    function resolveAnchorFromNode(node) {
        const editor = getEditor();
        if (!editor || !node) return null;
        let el = node.nodeType === Node.TEXT_NODE ? node.parentElement : node;
        while (el && el !== editor) {
            if (el.matches && el.matches(BLOCK_SELECTOR)) return el;
            el = el.parentElement;
        }
        return null;
    }

    function trackEditorFocus() {
        const editor = getEditor();
        if (!editor || editor.dataset.aiHelpFocusBound === '1') return;
        editor.dataset.aiHelpFocusBound = '1';

        editor.addEventListener('focusin', (e) => {
            const anchor = resolveAnchorFromNode(e.target);
            if (anchor) setLastAnchor(anchor);
        });

        editor.addEventListener('mouseup', () => {
            const sel = window.getSelection();
            if (!sel || !sel.rangeCount) return;
            const anchor = resolveAnchorFromNode(sel.anchorNode);
            if (anchor) setLastAnchor(anchor);
            updateSelectionModesVisibility();
        });

        document.addEventListener('selectionchange', () => {
            const editorSection = document.getElementById('course-editor-section');
            if (!editorSection || getComputedStyle(editorSection).display === 'none') return;
            updateSelectionModesVisibility();
        });
    }

    function insertBelowAnchor(node) {
        const editor = getEditor();
        if (!editor || !node) return null;

        let anchor = lastEditorAnchorEl;
        if (anchor && !editor.contains(anchor)) anchor = null;

        if (anchor && anchor.parentNode) {
            if (anchor.nextSibling) {
                anchor.parentNode.insertBefore(node, anchor.nextSibling);
            } else {
                anchor.parentNode.appendChild(node);
            }
        } else {
            editor.appendChild(node);
        }

        setLastAnchor(node);
        return node;
    }

    function sanitizeAiHtml(html) {
        const tmp = document.createElement('div');
        tmp.innerHTML = String(html || '');
        tmp.querySelectorAll('script, iframe, object, embed, form, input, button, link, meta, style').forEach((n) =>
            n.remove()
        );
        tmp.querySelectorAll('*').forEach((el) => {
            [...el.attributes].forEach((attr) => {
                const name = attr.name.toLowerCase();
                if (name.startsWith('on') || name === 'href' && /^\s*javascript:/i.test(attr.value)) {
                    el.removeAttribute(attr.name);
                }
            });
        });
        return tmp.innerHTML;
    }

    function appendBubble(role, text) {
        const box = document.getElementById('ai-help-messages');
        if (!box) return;
        const div = document.createElement('div');
        div.className = `ai-help-bubble ${role}`;
        div.textContent = text;
        box.appendChild(div);
        box.scrollTop = box.scrollHeight;
    }

    function clearAiHelpMessages() {
        const box = document.getElementById('ai-help-messages');
        if (box) box.innerHTML = '';
        clearSuggestions();
    }

    async function loadAiHelpHistory(courseId) {
        clearAiHelpMessages();
        if (!courseId) return;
        const apiBase = global.API_BASE_URL || '';
        const token = global.authToken || localStorage.getItem('token');
        try {
            const res = await fetch(`${apiBase}/api/ai/editor-help/history?courseId=${encodeURIComponent(courseId)}`, {
                headers: { Authorization: `Bearer ${token}` },
                credentials: 'include'
            });
            const data = await res.json();
            if (!data.success || !Array.isArray(data.data)) return;
            data.data.forEach((row) => {
                if (row.role === 'user' || row.role === 'assistant') {
                    appendBubble(row.role, row.content);
                }
            });
        } catch (err) {
            console.warn('AI help history load failed:', err);
        }
    }

    function onAiEditorCourseChanged(info) {
        if (info && info.isNew) {
            clearAiHelpMessages();
            return;
        }
        const id = (info && info.courseId) || global.currentEditingCourseId;
        if (id) loadAiHelpHistory(id);
        else clearAiHelpMessages();
    }

    global.onAiEditorCourseChanged = onAiEditorCourseChanged;
    global.clearAiHelpMessages = clearAiHelpMessages;
    global.loadAiHelpHistory = loadAiHelpHistory;

    function clearSuggestions() {
        const el = document.getElementById('ai-help-suggestions');
        if (el) el.innerHTML = '';
    }

    function getEditorSelectionText() {
        const editor = getEditor();
        const sel = window.getSelection();
        if (!sel || sel.isCollapsed || !editor) return '';
        if (!editor.contains(sel.anchorNode) || !editor.contains(sel.focusNode)) return '';
        return sel.toString().trim();
    }

    function updateSelectionModesVisibility() {
        const modes = document.getElementById('ai-help-modes');
        if (!modes) return;
        const has = !!getEditorSelectionText();
        modes.hidden = !has;
    }

    function phetCatalogSummary() {
        const list = global.PHET_SIMS;
        if (!Array.isArray(list)) return '';
        return list
            .slice(0, 80)
            .map((s) => s.title)
            .join(', ');
    }

    function fuzzyMatchPhet(query) {
        const list = Array.isArray(global.PHET_SIMS) ? global.PHET_SIMS : [];
        const qRaw = String(query || '').toLowerCase().trim();
        if (!qRaw || !list.length) return null;

        // Topic aliases → prefer known good sims over weak fuzzy hits like "Quantum Coin Toss"
        const aliases = [
            { re: /plinko|probability|combinator|dice|coin toss|random|chance|stars?\s*and\s*bars/, prefer: /plinko|probability|random/i },
            { re: /area|factor|binomial|ncr|npr|permut|combinat/, prefer: /area model|combination/i },
            { re: /quadrat|parabola|graph/, prefer: /graphing quadratic|parabola/i },
            { re: /fraction|ratio|proportion/, prefer: /fraction|proportion|ratio/i },
            { re: /vector|force|newton/, prefer: /forces|vector|newton/i },
            { re: /wave|sound|interference/, prefer: /wave|sound|interference/i }
        ];
        for (const a of aliases) {
            if (a.re.test(qRaw)) {
                const hit = list.find((s) => a.prefer.test(String(s.title || '')));
                if (hit) return hit;
            }
        }

        const q = qRaw;
        let best = null;
        let bestScore = 0;
        for (const sim of list) {
            const title = String(sim.title || '').toLowerCase();
            const desc = String(sim.description || '').toLowerCase();
            let score = 0;
            if (title === q) score = 100;
            else if (title.includes(q) || (q.length > 8 && q.includes(title))) score = 80;
            else {
                const parts = q.split(/\s+/).filter((p) => p.length > 2);
                if (!parts.length) continue;
                const hits = parts.filter((p) => title.includes(p)).length;
                // Require title word hits (ignore description-only) to avoid junk matches
                score = hits * 20;
                if (hits === parts.length && parts.length >= 2) score += 25;
            }
            if (score > bestScore) {
                bestScore = score;
                best = sim;
            }
        }
        return bestScore >= 40 ? best : null;
    }

    async function ensureDraftCourseSaved() {
        if (global.currentEditingCourseId) return global.currentEditingCourseId;

        const titleEl = document.getElementById('course-title');
        const descEl = document.getElementById('course-description');
        const gradeEl = document.getElementById('course-grade-level');
        const videoEl = document.getElementById('course-video-url');
        const editor = getEditor();

        const title = (titleEl && titleEl.value.trim()) || 'Untitled Course (AI Draft)';
        if (titleEl && !titleEl.value.trim()) titleEl.value = title;

        if (typeof global.saveCurrentPageContent === 'function') {
            global.saveCurrentPageContent();
        }

        let content = editor ? editor.innerHTML : '';
        if (Array.isArray(global.coursePages) && global.coursePages.length) {
            if (typeof global.saveCurrentPageContent === 'function') global.saveCurrentPageContent();
            content = global.coursePages.join('<hr class="page-break">');
        }

        const blocks = Array.isArray(global.courseBlocks) ? global.courseBlocks : [];
        const apiBase = global.API_BASE_URL || '';
        const token = global.authToken || localStorage.getItem('token');

        const res = await fetch(`${apiBase}/api/courses`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${token}`
            },
            credentials: 'include',
            body: JSON.stringify({
                title,
                description: (descEl && descEl.value) || '',
                grade_level: gradeEl && gradeEl.value ? parseInt(gradeEl.value, 10) : null,
                content,
                blocks: JSON.stringify(blocks),
                status: 'draft',
                video_url: (videoEl && videoEl.value) || null,
                course_type: 'single'
            })
        });
        const data = await res.json();
        if (!data.success) {
            throw new Error(data.message || 'Failed to save draft course');
        }
        const id = data.data?.id || data.data;
        global.currentEditingCourseId = id;
        return id;
    }

    function buildFlowPhetWrapper(sim) {
        const wrapper = document.createElement('div');
        wrapper.className = 'phet-sim-wrapper';
        wrapper.contentEditable = 'false';
        wrapper.style.cssText =
            'position:relative; width:100%; max-width:720px; margin:1em 0; border:1px solid #ddd; border-radius:8px; overflow:hidden; background:#fff; box-shadow:0 2px 8px rgba(0,0,0,0.1);';
        wrapper.innerHTML = `
            <div style="background:#f0f0f0; padding:10px; display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #ddd;">
                <strong>⚛️ ${esc(sim.title)}</strong>
                <button type="button" class="phet-remove-btn" style="background:#ff4444; color:white; border:none; padding:4px 8px; border-radius:4px; cursor:pointer;">Remove</button>
            </div>
            <div style="position:relative; padding-bottom:56.25%; height:0; overflow:hidden;">
                <iframe src="${esc(sim.url)}" style="position:absolute; top:0; left:0; width:100%; height:100%; border:0;" allowfullscreen></iframe>
            </div>`;
        const btn = wrapper.querySelector('.phet-remove-btn');
        if (btn) {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                if (confirm('Remove this simulator?')) wrapper.remove();
            });
        }
        return wrapper;
    }

    function startLatexClickPlacement(latex, display) {
        const editor = getEditor();
        if (!editor) return;
        latexPlacementPending = { latex, display: !!display };
        editor.classList.add('ai-latex-placement');
        appendBubble('system', 'Click anywhere in the editor to place the equation.');

        const handler = (e) => {
            if (!latexPlacementPending) return;
            if (!editor.contains(e.target) && e.target !== editor) return;
            e.preventDefault();
            e.stopPropagation();

            const pending = latexPlacementPending;
            latexPlacementPending = null;
            editor.classList.remove('ai-latex-placement');
            editor.removeEventListener('click', handler, true);

            const wrapped = pending.display ? `$$${pending.latex}$$` : `$${pending.latex}$`;
            const span = document.createElement('span');
            span.className = 'latex-equation';
            span.dataset.latex = 'true';
            span.textContent = wrapped;

            // Prefer drop at caret under click
            let placed = false;
            try {
                const range = document.caretRangeFromPoint
                    ? document.caretRangeFromPoint(e.clientX, e.clientY)
                    : null;
                if (range && editor.contains(range.startContainer)) {
                    range.collapse(true);
                    range.insertNode(span);
                    const zw = document.createTextNode('\u200B');
                    if (span.nextSibling) span.parentNode.insertBefore(zw, span.nextSibling);
                    else span.parentNode.appendChild(zw);
                    placed = true;
                    setLastAnchor(span);
                }
            } catch (_) {
                /* fall through */
            }
            if (!placed) insertBelowAnchor(span);

            if (global.MathJax && typeof global.MathJax.typesetPromise === 'function') {
                global.MathJax.typesetPromise([span]).catch(() => {});
            }
            appendBubble('system', 'Equation placed.');
        };

        editor.addEventListener('click', handler, true);
    }

    function createQuizPlaceholderEl(questionText, questionId) {
        const placeholder = document.createElement('div');
        placeholder.className = 'quiz-question-placeholder';
        placeholder.dataset.questionId = questionId || '';
        placeholder.contentEditable = 'false';
        placeholder.style.cssText =
            'background:#e0e7ff; border:2px solid var(--primary,#667eea); padding:1.5em; margin:1.5em 0; border-radius:8px; position:relative; cursor:pointer; user-select:none; box-shadow:0 4px 6px rgba(0,0,0,0.1);';
        const qid = questionId || '';
        const deleteBtn = qid
            ? `<button type="button" class="quiz-placeholder-delete-btn" data-question-id="${qid}" style="position:absolute; top:5px; right:5px; background:#e53e3e; color:white; border:none; border-radius:4px; padding:2px 6px; cursor:pointer; font-size:0.8em; z-index:10;">🗑️ Delete</button>`
            : '';
        const trunc = String(questionText || '').substring(0, 100);
        placeholder.innerHTML = `
            <strong>❓ Quiz Question:</strong> ${esc(trunc)}${questionText && questionText.length > 100 ? '...' : ''}
            ${deleteBtn}
            <div style="font-size:0.85em; color:#999; margin-top:0.5em;">Click to edit</div>`;
        placeholder.addEventListener('click', (e) => {
            if (e.target.closest('button')) return;
            const id = placeholder.dataset.questionId;
            if (id && typeof global.openQuizModal === 'function') {
                global.openQuizModal(parseInt(id, 10));
            }
        });
        return placeholder;
    }

    async function skillInsertHtml(payload) {
        const wrap = document.createElement('div');
        wrap.className = 'ai-inserted-content';
        wrap.innerHTML = sanitizeAiHtml(payload.html);
        if (!wrap.innerHTML.trim()) {
            wrap.textContent = String(payload.html || '').replace(/<[^>]+>/g, '');
        }
        insertBelowAnchor(wrap);
    }

    async function skillAddQuestion(payload) {
        const courseId = await ensureDraftCourseSaved();
        const apiBase = global.API_BASE_URL || '';
        const token = global.authToken || localStorage.getItem('token');
        const orderIndex = Array.isArray(global.courseQuestions) ? global.courseQuestions.length : 0;

        const questionData = {
            question_text: payload.question_text,
            question_type: payload.question_type || 'multiple_choice',
            options: payload.options || null,
            correct_answer: payload.correct_answer,
            explanation: payload.explanation || '',
            points: payload.points || 10,
            order_index: orderIndex
        };

        const res = await fetch(`${apiBase}/api/courses/${courseId}/questions`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${token}`
            },
            credentials: 'include',
            body: JSON.stringify(questionData)
        });
        const data = await res.json();
        if (!data.success) throw new Error(data.message || 'Failed to create question');

        const qid = data.data?.id || data.data?.questionId || data.data;
        if (typeof global.loadCourseQuestions === 'function') {
            await global.loadCourseQuestions(courseId);
        } else if (Array.isArray(global.courseQuestions)) {
            global.courseQuestions.push({ id: qid, ...questionData });
        }

        const el = createQuizPlaceholderEl(payload.question_text, qid);
        insertBelowAnchor(el);
    }

    async function skillAddPhet(payload) {
        const sim = fuzzyMatchPhet(payload.query || payload.title);
        if (!sim) {
            appendBubble('system', `No PhET match for “${payload.query || payload.title}”. Try a closer title.`);
            return;
        }
        const wrapper = buildFlowPhetWrapper(sim);
        insertBelowAnchor(wrapper);
        appendBubble('system', `Inserted PhET: ${sim.title}`);
    }

    async function skillAddLatex(payload) {
        const latex = String(payload.latex || '').trim();
        if (!latex) return;
        const display = !!payload.display;
        // Click-to-place only when explicitly requested; bulk/section inserts inline
        if (payload.place === 'click') {
            startLatexClickPlacement(latex, display);
            return;
        }
        const wrapped = display ? `$$${latex}$$` : `$${latex}$`;
        const span = document.createElement('span');
        span.className = 'latex-equation';
        span.dataset.latex = 'true';
        span.textContent = wrapped;
        const wrap = document.createElement('p');
        wrap.appendChild(span);
        wrap.appendChild(document.createTextNode('\u200B'));
        insertBelowAnchor(display ? wrap : span);
        if (global.MathJax && typeof global.MathJax.typesetPromise === 'function') {
            global.MathJax.typesetPromise([span]).catch(() => {});
        }
    }

    function splitOutlineIntoSections(text) {
        const src = String(text || '').trim();
        if (!src) return [];

        const headingRe = /^(#{2,3})\s+(.+)$/gm;
        const matches = [...src.matchAll(headingRe)];
        if (matches.length >= 2) {
            const sections = [];
            for (let i = 0; i < matches.length; i++) {
                const start = matches[i].index;
                const end = i + 1 < matches.length ? matches[i + 1].index : src.length;
                const title = matches[i][2].trim();
                const body = src.slice(start, end).trim();
                // Prefer ### leaf sections; if only ## modules, use those
                if (matches[i][1] === '###' || matches.every((m) => m[1] === '##')) {
                    sections.push({ title, body });
                }
            }
            if (sections.length >= 2) return sections;
            // Mixed ##/### — use only ###
            const leaf = [];
            for (let i = 0; i < matches.length; i++) {
                if (matches[i][1] !== '###') continue;
                const start = matches[i].index;
                const end = i + 1 < matches.length ? matches[i + 1].index : src.length;
                leaf.push({
                    title: matches[i][2].trim(),
                    body: src.slice(start, end).trim()
                });
            }
            if (leaf.length >= 2) return leaf;
        }

        // Fallback: Module N / numbered subsections
        const modRe = /(?:^|\n)((?:Module\s+\d+|#{0,3}\s*\d+\.\d+)[^\n]*)([\s\S]*?)(?=(?:\n(?:Module\s+\d+|#{0,3}\s*\d+\.\d+))|$)/gi;
        const modParts = [];
        let m;
        while ((m = modRe.exec(src)) !== null) {
            const title = m[1].replace(/^#+\s*/, '').trim();
            const body = (m[1] + m[2]).trim();
            if (title && body.length > 40) modParts.push({ title, body });
        }
        return modParts.length >= 2 ? modParts : [];
    }

    function shouldChunkRequest(text, mode) {
        if (mode && mode !== 'chat') return false;
        const t = String(text || '');
        if (t.length < 1200) return false;
        const sections = splitOutlineIntoSections(t);
        if (sections.length >= 2) return true;
        return /full course|comprehensive|every sub-topic|module\s+\d+/i.test(t) && t.length > 2000;
    }

    async function callEditorHelpApi({ message, mode, selection, editorSnippet }) {
        // Persist chat per course: ensure draft exists before first message
        try {
            await ensureDraftCourseSaved();
        } catch (err) {
            console.warn('Could not ensure draft before AI help:', err);
        }

        const apiBase = global.API_BASE_URL || '';
        const token = global.authToken || localStorage.getItem('token');
        const res = await fetch(`${apiBase}/api/ai/editor-help`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${token}`
            },
            credentials: 'include',
            body: JSON.stringify({
                message,
                mode: mode || 'chat',
                selection: selection || undefined,
                courseId: global.currentEditingCourseId || undefined,
                editorSnippet: editorSnippet || undefined,
                phetCatalogSummary: phetCatalogSummary()
            })
        });

        const rawText = await res.text();
        let data = null;
        try {
            data = rawText ? JSON.parse(rawText) : null;
        } catch (_) {
            data = null;
        }
        return { res, data };
    }

    function errorMessageFromResponse(res, data) {
        return (
            (data && data.message) ||
            (res.status === 429
                ? 'AI is temporarily rate-limited. Please wait about a minute and try again.'
                : res.status === 502 || res.status === 504
                  ? 'AI service is busy or timed out. Please try again in a moment.'
                  : `AI Help failed (${res.status})`)
        );
    }

    async function sendChunkedAiHelp(fullText, sections, selection, editorSnippet) {
        appendBubble(
            'system',
            `Large lesson detected — generating ${sections.length} sections one at a time so it won’t time out…`
        );

        let okCount = 0;
        for (let i = 0; i < sections.length; i++) {
            const sec = sections[i];
            appendBubble('system', `Generating “${sec.title}” (${i + 1}/${sections.length})…`);

            const chunkMessage = [
                'Generate ONLY this one section for the VeeLearn course editor right now.',
                'Do not ask clarifying questions.',
                'OUTPUT RULE: Start with VEELEARN_EDITOR_ACTIONS_JSON: then a complete valid JSON array FIRST.',
                'REQUIRED actions: (1) insert_html with theory + worked examples (put math as $...$ inside HTML), (2) 2–3 add_question with short_answer preferred.',
                'OPTIONAL: one add_phet only if you know a real PhET title; skip add_latex (put formulas in HTML instead).',
                'JSON escaping: double every backslash in strings. Prefer fewer complete actions over truncated JSON.',
                '',
                `SECTION TITLE: ${sec.title}`,
                '',
                'SECTION DETAILS:',
                sec.body.slice(0, 4000),
                '',
                'OUTLINE CONTEXT (do not generate other sections):',
                fullText.slice(0, 2000)
            ].join('\n');

            try {
                let result = null;
                for (let attempt = 0; attempt < 2; attempt++) {
                    try {
                        result = await callEditorHelpApi({
                            message: chunkMessage,
                            mode: 'section',
                            selection,
                            editorSnippet: i === 0 && attempt === 0 ? editorSnippet : undefined
                        });
                        break;
                    } catch (netErr) {
                        if (attempt === 0) {
                            appendBubble('system', `Network hiccup on “${sec.title}” — retrying…`);
                            await new Promise((r) => setTimeout(r, 1500));
                            continue;
                        }
                        throw netErr;
                    }
                }

                let { res, data } = result;

                if (!res.ok || !data || data.success === false) {
                    // One more try on timeout/rate-limit with a shorter prompt
                    if (res.status === 504 || res.status === 429 || res.status === 502) {
                        appendBubble('system', `Simplifying “${sec.title}” after ${res.status}…`);
                        await new Promise((r) => setTimeout(r, res.status === 429 ? 2500 : 1000));
                        const simple = await callEditorHelpApi({
                            message: [
                                'Return ONLY VEELEARN_EDITOR_ACTIONS_JSON: then a JSON array.',
                                'Include one insert_html (theory + 1 example) and two short_answer add_question items.',
                                'No add_latex. No add_phet. Keep under 1800 characters of HTML.',
                                `Section: ${sec.title}`,
                                sec.body.slice(0, 1800)
                            ].join('\n'),
                            mode: 'section',
                            selection
                        });
                        if (simple.res.ok && simple.data && simple.data.success !== false) {
                            res = simple.res;
                            data = simple.data;
                        } else {
                            appendBubble('error', `${sec.title}: ${errorMessageFromResponse(res, data)}`);
                            await new Promise((r) => setTimeout(r, 800));
                            continue;
                        }
                    } else {
                        appendBubble('error', `${sec.title}: ${errorMessageFromResponse(res, data)}`);
                        await new Promise((r) => setTimeout(r, 800));
                        continue;
                    }
                }

                let reply = data.data?.reply || '';
                let actions = Array.isArray(data.data?.actions) ? data.data.actions : [];

                // Client retry if still empty (backend should usually salvage)
                if (!actions.length) {
                    appendBubble('system', `Retrying “${sec.title}” with simpler HTML-only instructions…`);
                    const retry = await callEditorHelpApi({
                        message: [
                            'CRITICAL RETRY: emit ONLY:',
                            'VEELEARN_EDITOR_ACTIONS_JSON:',
                            `[{"type":"insert_html","payload":{"html":"<h3>${sec.title.replace(/"/g, '')}</h3><p>Write 3-5 paragraphs of theory and one worked example. Use $n$ for variables.</p>"}},{"type":"add_question","payload":{"question_text":"Practice question 1","question_type":"short_answer","correct_answer":"...","explanation":"...","points":10}},{"type":"add_question","payload":{"question_text":"Practice question 2","question_type":"short_answer","correct_answer":"...","explanation":"...","points":10}}]`,
                            'Replace placeholders with real content for:',
                            sec.title,
                            sec.body.slice(0, 2500)
                        ].join('\n'),
                        mode: 'section',
                        selection
                    });
                    if (retry.res.ok && retry.data && retry.data.success !== false) {
                        data = retry.data;
                        reply = data.data?.reply || reply;
                        actions = Array.isArray(data.data?.actions) ? data.data.actions : [];
                    }
                }

                if (!actions.length && reply && reply.length > 40 && !/^done\.?$/i.test(reply.trim())) {
                    actions = [
                        {
                            type: 'insert_html',
                            payload: { html: `<h3>${esc(sec.title)}</h3><p>${esc(reply)}</p>` }
                        }
                    ];
                    appendBubble('system', `Placed written summary for “${sec.title}” (actions were incomplete).`);
                }

                if (reply && !/^done\.?$/i.test(reply.trim())) appendBubble('assistant', reply);
                if (actions.length) {
                    await executeEditorActions(actions);
                    okCount += 1;
                    appendBubble('system', `✓ Placed “${sec.title}”.`);
                } else {
                    appendBubble('system', `No content placed for “${sec.title}”.`);
                }
            } catch (err) {
                console.error(err);
                appendBubble('error', `${sec.title}: network error — ${err.message || 'failed'}`);
            }

            if (i < sections.length - 1) {
                await new Promise((r) => setTimeout(r, 1100));
            }
        }

        appendBubble(
            'assistant',
            okCount
                ? `Finished generating ${okCount} of ${sections.length} sections into the editor.`
                : 'Could not generate sections. Wait a minute and try again, or generate one module at a time.'
        );
    }

    async function sendAiHelp(message, mode) {
        if (aiHelpBusy) return;
        const input = document.getElementById('ai-help-input');
        const sendBtn = document.getElementById('ai-help-send');
        const text = (message != null ? message : input && input.value ? input.value : '').trim();
        const activeMode = mode || 'chat';
        const selection = getEditorSelectionText();

        if (!text && activeMode === 'chat' && !selection) {
            appendBubble('error', 'Enter a request or select text first.');
            return;
        }

        aiHelpBusy = true;
        if (sendBtn) sendBtn.disabled = true;
        clearSuggestions();

        const displayMsg =
            text ||
            (activeMode === 'expand'
                ? 'Expand selection'
                : activeMode === 'simplify'
                  ? 'Simplify selection'
                  : activeMode === 'check_question'
                    ? 'Add check question for selection'
                    : activeMode === 'validate'
                      ? 'Validate page'
                      : 'Help');
        appendBubble('user', displayMsg.length > 500 ? displayMsg.slice(0, 500) + '…' : displayMsg);
        if (input && message == null) input.value = '';

        const editor = getEditor();
        const snippet = editor ? (editor.innerText || '').slice(0, 4000) : '';

        // Anchor near selection if present
        if (selection) {
            const sel = window.getSelection();
            if (sel && sel.rangeCount) {
                const a = resolveAnchorFromNode(sel.anchorNode);
                if (a) setLastAnchor(a);
            }
        }

        try {
            if (shouldChunkRequest(text || displayMsg, activeMode)) {
                let sections = splitOutlineIntoSections(text || displayMsg);
                if (sections.length < 2) {
                    // Force a single long job into 2–4 artificial chunks by paragraphs
                    const paras = (text || displayMsg).split(/\n{2,}/).filter((p) => p.trim().length > 80);
                    const chunkSize = Math.max(1, Math.ceil(paras.length / 4));
                    sections = [];
                    for (let i = 0; i < paras.length; i += chunkSize) {
                        const body = paras.slice(i, i + chunkSize).join('\n\n');
                        sections.push({ title: `Part ${sections.length + 1}`, body });
                    }
                }
                if (sections.length >= 2) {
                    await sendChunkedAiHelp(text || displayMsg, sections.slice(0, 12), selection, snippet);
                    return;
                }
            }

            const { res, data } = await callEditorHelpApi({
                message: text || displayMsg,
                mode: activeMode,
                selection,
                editorSnippet: snippet
            });

            if (!res.ok || !data || data.success === false) {
                appendBubble('error', errorMessageFromResponse(res, data));
                return;
            }

            const reply = data.data?.reply || '';
            const actions = data.data?.actions || [];
            if (reply) appendBubble('assistant', reply);
            await executeEditorActions(actions);
            if (!actions.length && !reply) appendBubble('assistant', 'No changes suggested.');
        } catch (err) {
            console.error(err);
            appendBubble(
                'error',
                'Could not reach AI Help (network or CORS). If this persists after a redeploy, try again in a minute.'
            );
        } finally {
            aiHelpBusy = false;
            if (sendBtn) sendBtn.disabled = false;
        }
    }

    async function skillAddMarketplaceSim(payload) {
        const id = payload.simulatorId || payload.id;
        const title = payload.title || 'Marketplace Simulator';
        if (!id) return;

        if (!Array.isArray(global.courseBlocks)) global.courseBlocks = [];
        const blockId = Date.now();
        global.courseBlocks.push({
            id: blockId,
            type: 'marketplace-simulator',
            title,
            simulatorId: id,
            data: { simulatorId: id }
        });

        const div = document.createElement('div');
        div.className = 'simulator-block';
        div.dataset.blockId = String(blockId);
        div.contentEditable = 'false';
        div.style.cssText =
            'background:#f0f0f0; padding:15px; margin:10px 0; border-left:4px solid #667eea; border-radius:4px; display:block;';
        div.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <strong>Marketplace Simulator</strong>
                    <p style="margin:5px 0; color:#666;">${esc(title)}</p>
                </div>
                <div style="display:flex; gap:10px;">
                    <button type="button" onclick="handleEditSimulator(event, ${blockId})" style="padding:5px 10px; background:#667eea; color:white; border:none; border-radius:4px; cursor:pointer;">Edit</button>
                    <button type="button" onclick="handleRemoveSimulator(event, ${blockId})" style="padding:5px 10px; background:#f44336; color:white; border:none; border-radius:4px; cursor:pointer;">Remove</button>
                </div>
            </div>`;
        insertBelowAnchor(div);
    }

    function renderSimSuggestions(payload) {
        const box = document.getElementById('ai-help-suggestions');
        if (!box) return;
        clearSuggestions();

        const suggestions = Array.isArray(payload.suggestions) ? payload.suggestions : [];
        if (payload.query) {
            const phet = fuzzyMatchPhet(payload.query);
            if (phet) {
                suggestions.unshift({
                    id: null,
                    title: phet.title,
                    source: 'phet',
                    phetTitle: phet.title
                });
            }
        }

        if (!suggestions.length) {
            appendBubble('system', payload.reason || 'No interactive matches found.');
            return;
        }

        if (payload.reason) appendBubble('system', payload.reason);

        suggestions.slice(0, 5).forEach((s) => {
            const chip = document.createElement('button');
            chip.type = 'button';
            chip.className = 'ai-help-suggest-chip';
            const source = s.source === 'phet' || s.phetTitle ? 'PhET' : 'Marketplace';
            chip.textContent = `+ ${s.title} (${source})`;
            chip.addEventListener('click', async () => {
                try {
                    if (s.source === 'phet' || s.phetTitle || !s.id) {
                        await skillAddPhet({ query: s.phetTitle || s.title });
                    } else {
                        await skillAddMarketplaceSim({ simulatorId: s.id, title: s.title });
                        appendBubble('system', `Added marketplace sim: ${s.title}`);
                    }
                } catch (err) {
                    appendBubble('error', err.message || 'Failed to add simulation');
                }
            });
            box.appendChild(chip);
        });
    }

    function renderValidateFindings(findings) {
        if (!findings.length) {
            appendBubble('assistant', 'No issues found.');
            return;
        }
        appendBubble('assistant', 'Validation findings:\n• ' + findings.join('\n• '));
    }

    function validateCurrentEditorPage() {
        const findings = [];
        const editor = getEditor();
        if (!editor) {
            findings.push('Content editor not found.');
            return findings;
        }

        const text = editor.innerText || '';
        // Count unescaped $ that are not inside .latex-equation
        const clone = editor.cloneNode(true);
        clone.querySelectorAll('.latex-equation').forEach((n) => n.remove());
        const raw = clone.innerText || '';
        const dollarCount = (raw.match(/\$/g) || []).length;
        if (dollarCount % 2 !== 0) {
            findings.push('Unmatched $ delimiter in page text (possible broken inline LaTeX).');
        }
        const dd = (raw.match(/\$\$/g) || []).length;
        if (dd % 2 !== 0) {
            findings.push('Unmatched $$ delimiter in page text (possible broken display LaTeX).');
        }

        editor.querySelectorAll('.latex-equation').forEach((el, i) => {
            const content = (el.textContent || '').trim();
            if (!content || content === '$' || content === '$$') {
                findings.push(`Empty LaTeX equation node (#${i + 1}).`);
            } else if (!/^\$[\s\S]+\$$/.test(content) && !/^\$\$[\s\S]+\$\$$/.test(content)) {
                findings.push(`LaTeX node (#${i + 1}) missing $ / $$ delimiters.`);
            }
        });

        const questions = Array.isArray(global.courseQuestions) ? global.courseQuestions : [];
        const qIds = new Set(questions.map((q) => String(q.id)));

        editor.querySelectorAll('.quiz-question-placeholder').forEach((el, i) => {
            const id = el.dataset.questionId;
            if (!id) findings.push(`Quiz placeholder (#${i + 1}) missing data-question-id.`);
            else if (!qIds.has(String(id))) {
                findings.push(`Quiz placeholder id ${id} not found in loaded questions.`);
            }
        });

        questions.forEach((q) => {
            if (!q.question_text || !String(q.question_text).trim()) {
                findings.push(`Question #${q.id} has empty question_text.`);
            }
            if (q.question_type === 'multiple_choice') {
                let opts = q.options;
                if (typeof opts === 'string') {
                    try {
                        opts = JSON.parse(opts);
                    } catch (_) {
                        opts = [];
                    }
                }
                if (!Array.isArray(opts) || opts.length < 2) {
                    findings.push(`Question #${q.id} (MC) needs at least 2 options.`);
                }
            }
            if (!q.correct_answer && q.correct_answer !== 0) {
                findings.push(`Question #${q.id} missing correct_answer.`);
            }
        });

        return findings;
    }

    async function executeEditorActions(actions) {
        if (!Array.isArray(actions)) return;
        for (const action of actions) {
            const type = action.type;
            const payload = action.payload || {};
            try {
                if (type === 'insert_html') await skillInsertHtml(payload);
                else if (type === 'add_question') await skillAddQuestion(payload);
                else if (type === 'add_phet') await skillAddPhet(payload);
                else if (type === 'add_latex') await skillAddLatex(payload);
                else if (type === 'add_marketplace_sim') await skillAddMarketplaceSim(payload);
                else if (type === 'suggest_sims') renderSimSuggestions(payload);
                else if (type === 'validate_report') renderValidateFindings(payload.findings || []);
            } catch (err) {
                console.error('AI skill failed:', type, err);
                appendBubble('error', `Action “${type}” failed: ${err.message || err}`);
            }
        }
    }

    async function runLocalValidateThenOptionalAi() {
        const findings = validateCurrentEditorPage();
        renderValidateFindings(findings);
        // Optional narrative pass
        await sendAiHelp(
            findings.length
                ? `Review these validation findings and suggest fixes:\n${findings.join('\n')}`
                : 'Quickly confirm the page looks structurally sound for quizzes and LaTeX.',
            'validate'
        );
    }

    function togglePanel(forceOpen) {
        const panel = document.getElementById('ai-help-panel');
        const btn = document.getElementById('ai-help-toggle');
        if (!panel || !btn) return;
        const open = forceOpen != null ? forceOpen : panel.hidden;
        panel.hidden = !open;
        btn.setAttribute('aria-expanded', open ? 'true' : 'false');
        if (open) {
            updateSelectionModesVisibility();
            const input = document.getElementById('ai-help-input');
            if (input) input.focus();
        }
    }

    function setupAiEditorHelp() {
        trackEditorFocus();

        const toggle = document.getElementById('ai-help-toggle');
        const sendBtn = document.getElementById('ai-help-send');
        const input = document.getElementById('ai-help-input');
        const validateBtn = document.getElementById('ai-help-validate');

        if (toggle) {
            toggle.addEventListener('click', (e) => {
                e.preventDefault();
                togglePanel();
            });
        }
        if (sendBtn) {
            sendBtn.addEventListener('click', (e) => {
                e.preventDefault();
                sendAiHelp();
            });
        }
        if (input) {
            input.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendAiHelp();
                }
            });
        }
        if (validateBtn) {
            validateBtn.addEventListener('click', (e) => {
                e.preventDefault();
                const panel = document.getElementById('ai-help-panel');
                if (panel && panel.hidden) togglePanel(true);
                runLocalValidateThenOptionalAi();
            });
        }

        document.querySelectorAll('.ai-help-mode-chip').forEach((chip) => {
            chip.addEventListener('click', (e) => {
                e.preventDefault();
                const mode = chip.dataset.mode;
                const panel = document.getElementById('ai-help-panel');
                if (panel && panel.hidden) togglePanel(true);
                sendAiHelp('', mode);
            });
        });
    }

    // Exports
    global.setupAiEditorHelp = setupAiEditorHelp;
    global.validateCurrentEditorPage = validateCurrentEditorPage;
    global.executeEditorActions = executeEditorActions;
    global.insertBelowAnchor = insertBelowAnchor;
    global.setAiEditorLastAnchor = setLastAnchor;
    global.onCourseDraftIdAssigned = function (courseId) {
        // After first autosave/AI draft create, history is empty for new courses — keep current bubbles
        if (courseId && !document.getElementById('ai-help-messages')?.childElementCount) {
            loadAiHelpHistory(courseId);
        }
    };
})(typeof window !== 'undefined' ? window : globalThis);
