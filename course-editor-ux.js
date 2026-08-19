/**
 * Course editor UX: collapsible sidebars, page strip reorder, undo/redo,
 * autosave status, keyboard shortcuts. Works with hooks from script.js.
 */
(function (global) {
    'use strict';

    let editorUndoStack = [];
    let editorRedoStack = [];
    let editorUndoApplying = false;
    const EDITOR_UNDO_MAX = 50;
    let autosaveTimer = null;
    let autosaveDirty = false;
    let uxBound = false;

    function esc(s) {
        if (typeof global.escapeHtml === 'function') return global.escapeHtml(s);
        return String(s == null ? '' : s)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    }

    function setEditorAutosaveStatus(text) {
        const el = document.getElementById('editor-autosave-status');
        if (el) el.textContent = text;
    }
    global.setEditorAutosaveStatus = setEditorAutosaveStatus;

    function setupEditorSidebarToggles() {
        const layout = document.getElementById('course-form');
        const sidebar = document.getElementById('editor-sidebar');
        const inspector = document.getElementById('editor-inspector');
        if (!layout || !sidebar || !inspector) return;

        const applyState = () => {
            const sideCollapsed = localStorage.getItem('editor-sidebar-collapsed') === '1';
            const inspCollapsed = localStorage.getItem('editor-inspector-collapsed') === '1';
            layout.classList.toggle('sidebar-collapsed', sideCollapsed);
            layout.classList.toggle('inspector-collapsed', inspCollapsed);
            sidebar.classList.toggle('collapsed', sideCollapsed);
            inspector.classList.toggle('collapsed', inspCollapsed);
            const sideBody = document.getElementById('editor-sidebar-body');
            const sideRail = document.getElementById('editor-sidebar-rail');
            const inspBody = document.getElementById('editor-inspector-body');
            const inspRail = document.getElementById('editor-inspector-rail');
            if (sideBody) sideBody.hidden = sideCollapsed;
            if (sideRail) sideRail.hidden = !sideCollapsed;
            if (inspBody) inspBody.hidden = inspCollapsed;
            if (inspRail) inspRail.hidden = !inspCollapsed;
        };

        const bind = (id, key) => {
            const btn = document.getElementById(id);
            if (!btn || btn.dataset.uxBound === '1') return;
            btn.dataset.uxBound = '1';
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const next = localStorage.getItem(key) === '1' ? '0' : '1';
                localStorage.setItem(key, next);
                applyState();
            });
        };

        bind('toggle-editor-sidebar', 'editor-sidebar-collapsed');
        bind('expand-editor-sidebar', 'editor-sidebar-collapsed');
        bind('toggle-editor-inspector', 'editor-inspector-collapsed');
        bind('expand-editor-inspector', 'editor-inspector-collapsed');
        applyState();
    }

    function pageSnippetFromHtml(html) {
        const tmp = document.createElement('div');
        tmp.innerHTML = html || '';
        const text = (tmp.textContent || '').replace(/\s+/g, ' ').trim();
        return text ? text.slice(0, 48) + (text.length > 48 ? '…' : '') : '(Empty page)';
    }

    function getPages() {
        return Array.isArray(global.coursePages) ? global.coursePages : [''];
    }

    function getPageIndex() {
        return typeof global.currentPageIndex === 'number' ? global.currentPageIndex : 0;
    }

    function setPageIndex(i) {
        global.currentPageIndex = i;
    }

    function renderPageStrip() {
        const strip = document.getElementById('page-strip');
        if (!strip) return;
        if (typeof global.saveCurrentPageContent === 'function') global.saveCurrentPageContent();

        const pages = getPages();
        const cur = getPageIndex();
        strip.innerHTML = '';

        pages.forEach((html, i) => {
            const thumb = document.createElement('div');
            thumb.className = 'page-thumb' + (i === cur ? ' active' : '');
            thumb.draggable = true;
            thumb.dataset.pageIndex = String(i);
            thumb.innerHTML = `
                <div class="page-thumb-num">Page ${i + 1}</div>
                <div class="page-thumb-snippet">${esc(pageSnippetFromHtml(html))}</div>
                <div class="page-thumb-actions">
                    <button type="button" class="page-thumb-move" data-dir="-1" title="Move left" ${i === 0 ? 'disabled' : ''}>←</button>
                    <button type="button" class="page-thumb-move" data-dir="1" title="Move right" ${i === pages.length - 1 ? 'disabled' : ''}>→</button>
                </div>`;

            thumb.addEventListener('click', (e) => {
                if (e.target.closest('.page-thumb-move')) return;
                if (i === getPageIndex()) return;
                if (typeof global.saveCurrentPageContent === 'function') global.saveCurrentPageContent();
                setPageIndex(i);
                if (typeof global.renderCurrentPage === 'function') global.renderCurrentPage();
            });

            thumb.querySelectorAll('.page-thumb-move').forEach((btn) => {
                btn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    movePage(i, i + parseInt(btn.dataset.dir, 10));
                });
            });

            thumb.addEventListener('dragstart', (e) => {
                e.dataTransfer.setData('text/plain', String(i));
                e.dataTransfer.effectAllowed = 'move';
                thumb.classList.add('dragging');
            });
            thumb.addEventListener('dragend', () => thumb.classList.remove('dragging'));
            thumb.addEventListener('dragover', (e) => {
                e.preventDefault();
                thumb.classList.add('drag-over');
            });
            thumb.addEventListener('dragleave', () => thumb.classList.remove('drag-over'));
            thumb.addEventListener('drop', (e) => {
                e.preventDefault();
                thumb.classList.remove('drag-over');
                const from = parseInt(e.dataTransfer.getData('text/plain'), 10);
                if (!Number.isNaN(from) && from !== i) movePage(from, i);
            });

            strip.appendChild(thumb);
        });
    }

    function movePage(fromIndex, toIndex) {
        const pages = getPages();
        if (fromIndex < 0 || fromIndex >= pages.length) return;
        if (toIndex < 0 || toIndex >= pages.length) return;
        if (typeof global.saveCurrentPageContent === 'function') global.saveCurrentPageContent();
        const [item] = pages.splice(fromIndex, 1);
        pages.splice(toIndex, 0, item);
        global.coursePages = pages;
        let cur = getPageIndex();
        if (cur === fromIndex) cur = toIndex;
        else if (fromIndex < cur && toIndex >= cur) cur -= 1;
        else if (fromIndex > cur && toIndex <= cur) cur += 1;
        setPageIndex(cur);
        if (typeof global.renderCurrentPage === 'function') global.renderCurrentPage();
    }

    function resetEditorUndoStack() {
        const editor = document.getElementById('course-content-editor');
        editorUndoStack = [editor ? editor.innerHTML : ''];
        editorRedoStack = [];
        updateUndoRedoButtons();
    }

    function pushEditorUndoSnapshot() {
        if (editorUndoApplying) return;
        const editor = document.getElementById('course-content-editor');
        if (!editor) return;
        const html = editor.innerHTML;
        if (editorUndoStack.length && editorUndoStack[editorUndoStack.length - 1] === html) return;
        editorUndoStack.push(html);
        if (editorUndoStack.length > EDITOR_UNDO_MAX) editorUndoStack.shift();
        editorRedoStack = [];
        updateUndoRedoButtons();
        autosaveDirty = true;
    }

    function updateUndoRedoButtons() {
        const undoBtn = document.getElementById('editor-undo-btn');
        const redoBtn = document.getElementById('editor-redo-btn');
        if (undoBtn) undoBtn.disabled = editorUndoStack.length <= 1;
        if (redoBtn) redoBtn.disabled = editorRedoStack.length === 0;
    }

    function editorUndo() {
        const editor = document.getElementById('course-content-editor');
        if (!editor || editorUndoStack.length <= 1) return;
        const current = editor.innerHTML;
        editorUndoStack.pop();
        const prev = editorUndoStack[editorUndoStack.length - 1];
        editorRedoStack.push(current);
        editorUndoApplying = true;
        editor.innerHTML = prev;
        if (typeof global.normalizeAbsoluteEmbeds === 'function') global.normalizeAbsoluteEmbeds(editor);
        editorUndoApplying = false;
        updateUndoRedoButtons();
        autosaveDirty = true;
    }

    function editorRedo() {
        const editor = document.getElementById('course-content-editor');
        if (!editor || !editorRedoStack.length) return;
        const next = editorRedoStack.pop();
        editorUndoStack.push(next);
        editorUndoApplying = true;
        editor.innerHTML = next;
        if (typeof global.normalizeAbsoluteEmbeds === 'function') global.normalizeAbsoluteEmbeds(editor);
        editorUndoApplying = false;
        updateUndoRedoButtons();
        autosaveDirty = true;
    }

    global.pushEditorUndoSnapshot = pushEditorUndoSnapshot;
    global.resetEditorUndoStack = resetEditorUndoStack;
    global.editorUndo = editorUndo;
    global.editorRedo = editorRedo;
    global.renderPageStrip = renderPageStrip;

    function setupEditorUndoRedo() {
        const editor = document.getElementById('course-content-editor');
        if (!editor || editor.dataset.uxUndoBound === '1') return;
        editor.dataset.uxUndoBound = '1';
        resetEditorUndoStack();

        let debounceTimer = null;
        editor.addEventListener('input', () => {
            autosaveDirty = true;
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(pushEditorUndoSnapshot, 350);
        });

        const undoBtn = document.getElementById('editor-undo-btn');
        const redoBtn = document.getElementById('editor-redo-btn');
        if (undoBtn && undoBtn.dataset.uxBound !== '1') {
            undoBtn.dataset.uxBound = '1';
            undoBtn.addEventListener('click', (e) => {
                e.preventDefault();
                editorUndo();
            });
        }
        if (redoBtn && redoBtn.dataset.uxBound !== '1') {
            redoBtn.dataset.uxBound = '1';
            redoBtn.addEventListener('click', (e) => {
                e.preventDefault();
                editorRedo();
            });
        }
    }

    function startCourseEditorAutosave() {
        if (autosaveTimer) return;
        const editor = document.getElementById('course-content-editor');
        const title = document.getElementById('course-title');
        const desc = document.getElementById('course-description');
        [editor, title, desc].filter(Boolean).forEach((el) => {
            if (el.dataset.uxAutosaveBound === '1') return;
            el.dataset.uxAutosaveBound = '1';
            el.addEventListener('input', () => {
                autosaveDirty = true;
            });
        });

        autosaveTimer = setInterval(() => {
            const section = document.getElementById('course-editor-section');
            if (!section || section.style.display === 'none') return;
            if (global.isPlacementMode) return;
            if (!autosaveDirty) return;
            const titleVal = (document.getElementById('course-title')?.value || '').trim();
            if (!titleVal) {
                setEditorAutosaveStatus('Add a title to auto-save');
                return;
            }
            if (typeof global.saveCourse !== 'function') return;
            autosaveDirty = false;
            global.saveCourse('draft', { quiet: true });
        }, 30000);
    }

    function setupEditorKeyboardShortcuts() {
        if (document.body.dataset.editorUxShortcuts === '1') return;
        document.body.dataset.editorUxShortcuts = '1';

        document.addEventListener(
            'keydown',
            (e) => {
                const section = document.getElementById('course-editor-section');
                if (!section || section.style.display === 'none') return;

                const target = e.target;
                const inAiInput =
                    target && (target.id === 'ai-help-input' || (target.closest && target.closest('#ai-help-panel')));

                if (e.key === 'Escape') {
                    if (global.isPlacementMode && typeof global.cancelPlacementMode === 'function') {
                        e.preventDefault();
                        global.cancelPlacementMode();
                    }
                    return;
                }

                if ((e.ctrlKey || e.metaKey) && (e.key === 's' || e.key === 'S')) {
                    e.preventDefault();
                    if (typeof global.saveCourse === 'function') global.saveCourse('draft');
                    return;
                }

                if (e.altKey && (e.key === 'ArrowLeft' || e.key === 'ArrowRight')) {
                    e.preventDefault();
                    if (typeof global.changePage === 'function') {
                        global.changePage(e.key === 'ArrowLeft' ? -1 : 1);
                    }
                    return;
                }

                if (inAiInput) return;

                if ((e.ctrlKey || e.metaKey) && (e.key === 'y' || e.key === 'Y')) {
                    e.preventDefault();
                    editorRedo();
                    return;
                }

                if ((e.ctrlKey || e.metaKey) && e.shiftKey && (e.key === 'z' || e.key === 'Z')) {
                    e.preventDefault();
                    editorRedo();
                    return;
                }

                if ((e.ctrlKey || e.metaKey) && (e.key === 'z' || e.key === 'Z') && !e.shiftKey) {
                    const editor = document.getElementById('course-content-editor');
                    if (editor && (document.activeElement === editor || editor.contains(document.activeElement))) {
                        e.preventDefault();
                        e.stopImmediatePropagation();
                        editorUndo();
                    }
                }
            },
            true
        );
    }

    function onCoursePageRendered() {
        renderPageStrip();
        resetEditorUndoStack();
        const editor = document.getElementById('course-content-editor');
        if (editor && typeof global.normalizeAbsoluteEmbeds === 'function') {
            global.normalizeAbsoluteEmbeds(editor);
        }
    }

    function onCourseEditorOpened(info) {
        setupEditorSidebarToggles();
        setupEditorUndoRedo();
        startCourseEditorAutosave();
        setupEditorKeyboardShortcuts();
        renderPageStrip();
        resetEditorUndoStack();
        setEditorAutosaveStatus('Drafts auto-save every 30s');

        if (typeof global.onAiEditorCourseChanged === 'function') {
            global.onAiEditorCourseChanged(info || {});
        }
    }

    global.onCoursePageRendered = onCoursePageRendered;
    global.onCourseEditorOpened = onCourseEditorOpened;

    function initCourseEditorUx() {
        if (uxBound) return;
        uxBound = true;
        setupEditorSidebarToggles();
        setupEditorUndoRedo();
        startCourseEditorAutosave();
        setupEditorKeyboardShortcuts();
        renderPageStrip();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initCourseEditorUx);
    } else {
        initCourseEditorUx();
    }
})(typeof window !== 'undefined' ? window : globalThis);
