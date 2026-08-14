/**
 * Native course-editor embeds: callouts, step reveal, matching, Desmos/graph.
 * Follows the existing placeholder/embed pattern (quiz, PhET, simulators).
 */
(function () {
  const EMBED_SELECTOR = '.vl-callout, .vl-step-reveal, .vl-matching, .vl-graph-embed';
  const CHECKPOINT_SELECTOR =
    '.quiz-question-placeholder, .vl-matching, .vl-step-reveal, .vl-graph-embed, .phet-sim-wrapper, .simulator-block';
  const WORD_LIMIT = 250;
  const MASCOT_SRC = 'assets/learner/mascot.svg';

  let setupDone = false;
  let wordTipEl = null;

  function esc(s) {
    if (typeof window.escapeHtml === 'function') return window.escapeHtml(s);
    return String(s ?? '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function uid(prefix) {
    return `${prefix}-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`;
  }

  function encodeData(obj) {
    try {
      return encodeURIComponent(JSON.stringify(obj));
    } catch (_) {
      return encodeURIComponent('{}');
    }
  }

  function decodeData(raw) {
    if (!raw) return null;
    try {
      return JSON.parse(decodeURIComponent(raw));
    } catch (_) {
      try {
        return JSON.parse(raw);
      } catch (e) {
        return null;
      }
    }
  }

  function applyFlow(el, extra) {
    if (typeof window.applyFlowEmbedStyles === 'function') {
      window.applyFlowEmbedStyles(el, extra || '');
      return;
    }
    el.classList.add('editor-embed-flow');
    el.style.cssText =
      'position:relative;width:100%;max-width:720px;margin:1em 0;display:block;box-sizing:border-box;' +
      (extra || '');
  }

  function insertNode(node) {
    if (typeof window.insertNodeInDocumentFlow === 'function') {
      window.insertNodeInDocumentFlow(node);
      return;
    }
    const editor = document.getElementById('course-content-editor');
    if (editor) editor.appendChild(node);
  }

  function startPlace(type, data) {
    if (typeof window.startPlacementMode === 'function') {
      window.startPlacementMode(type, data);
    } else {
      insertAtPlacement(type, data);
    }
  }

  function typeset(el) {
    if (!el) return;
    if (window.MathJax && typeof window.MathJax.typesetPromise === 'function') {
      window.MathJax.typesetPromise([el]).catch(() => {});
    }
  }

  /* ---------- Editor chrome ---------- */

  function ensureModals() {
    if (document.getElementById('vl-block-modal')) return;
    const wrap = document.createElement('div');
    wrap.id = 'vl-block-modal';
    wrap.className = 'modal vl-block-modal';
    wrap.style.display = 'none';
    wrap.innerHTML = `
      <div class="modal-content" style="max-width:640px;">
        <span class="close-modal" id="vl-block-modal-close">&times;</span>
        <h2 id="vl-block-modal-title">Add block</h2>
        <div id="vl-block-modal-body"></div>
        <div class="modal-actions" style="margin-top:16px;">
          <button type="button" id="vl-block-modal-save">Insert</button>
          <button type="button" id="vl-block-modal-cancel" class="secondary-btn">Cancel</button>
        </div>
      </div>`;
    document.body.appendChild(wrap);
    const close = () => {
      wrap.style.display = 'none';
    };
    wrap.querySelector('#vl-block-modal-close').addEventListener('click', close);
    wrap.querySelector('#vl-block-modal-cancel').addEventListener('click', close);
    wrap.addEventListener('click', (e) => {
      if (e.target === wrap) close();
    });
  }

  function openModal(title, bodyHtml, onSave) {
    ensureModals();
    const wrap = document.getElementById('vl-block-modal');
    document.getElementById('vl-block-modal-title').textContent = title;
    document.getElementById('vl-block-modal-body').innerHTML = bodyHtml;
    wrap.style.display = 'block';
    const saveBtn = document.getElementById('vl-block-modal-save');
    const handler = () => {
      if (onSave()) {
        wrap.style.display = 'none';
        saveBtn.removeEventListener('click', handler);
      }
    };
    saveBtn.onclick = handler;
  }

  function setupToolbar() {
    const menuBtn = document.getElementById('insert-add-block');
    const panel = document.getElementById('add-block-panel');
    if (menuBtn && panel && !menuBtn.dataset.vlBound) {
      menuBtn.dataset.vlBound = '1';
      menuBtn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        const open = panel.hasAttribute('hidden');
        if (open) panel.removeAttribute('hidden');
        else panel.setAttribute('hidden', '');
      });
      document.addEventListener('click', (e) => {
        if (!e.target.closest('#add-block-menu')) panel.setAttribute('hidden', '');
      });
      panel.querySelectorAll('[data-vl-block]').forEach((btn) => {
        btn.addEventListener('click', (e) => {
          e.preventDefault();
          panel.setAttribute('hidden', '');
          openCreator(btn.getAttribute('data-vl-block'));
        });
      });
    }

    const editor = document.getElementById('course-content-editor');
    if (editor && !editor.dataset.vlWordBound) {
      editor.dataset.vlWordBound = '1';
      editor.addEventListener('input', updateWordCountTip);
      editor.addEventListener('keyup', updateWordCountTip);
    }
  }

  function openCreator(kind) {
    if (kind === 'callout') openCalloutCreator();
    else if (kind === 'steps') openStepsCreator();
    else if (kind === 'matching') openMatchingCreator();
    else if (kind === 'graph') openGraphCreator();
  }

  function openCalloutCreator() {
    openModal(
      'Callout box',
      `<label>Style</label>
       <select id="vl-callout-kind">
         <option value="trap">Trap / Watch Out</option>
         <option value="strategy">Test Strategy</option>
         <option value="mascot">Mascot Tip</option>
       </select>
       <label>Title</label>
       <input type="text" id="vl-callout-title" placeholder="e.g. Sign error on vertex form" />
       <label>Body</label>
       <textarea id="vl-callout-body" rows="4" placeholder="Short warning or strategy students should remember."></textarea>`,
      () => {
        const kind = document.getElementById('vl-callout-kind').value;
        const title = document.getElementById('vl-callout-title').value.trim() || defaultCalloutTitle(kind);
        const body = document.getElementById('vl-callout-body').value.trim() || 'Add a short tip here.';
        startPlace('vl-callout', { kind, title, body });
        return true;
      }
    );
  }

  function defaultCalloutTitle(kind) {
    if (kind === 'trap') return 'Watch out';
    if (kind === 'strategy') return 'Test strategy';
    return 'Mascot tip';
  }

  function openStepsCreator() {
    openModal(
      'Interactive step reveal',
      `<p class="info-text">Students see one step at a time. Optional: ask a quick prediction before unlocking.</p>
       <label>Step 1</label><textarea id="vl-step-1" rows="2" placeholder="First idea or setup"></textarea>
       <label>Step 2</label><textarea id="vl-step-2" rows="2" placeholder="Main work"></textarea>
       <label>Step 3</label><textarea id="vl-step-3" rows="2" placeholder="Conclusion"></textarea>
       <label>Prediction check (optional)</label>
       <input type="text" id="vl-step-pred" placeholder="What do you think happens next?" />`,
      () => {
        const steps = [1, 2, 3]
          .map((n) => document.getElementById(`vl-step-${n}`).value.trim())
          .filter(Boolean);
        if (!steps.length) {
          alert('Enter at least one step.');
          return false;
        }
        startPlace('vl-steps', {
          steps,
          prompt: document.getElementById('vl-step-pred').value.trim()
        });
        return true;
      }
    );
  }

  function openMatchingCreator() {
    openModal(
      'Matching game',
      `<p class="info-text">Enter pairs. Students match the left column to the shuffled right column.</p>
       <div id="vl-match-rows"></div>
       <button type="button" id="vl-match-add" class="secondary-btn">+ Add pair</button>`,
      () => {
        const pairs = [];
        document.querySelectorAll('#vl-match-rows .vl-match-row').forEach((row) => {
          const left = row.querySelector('.vl-match-left').value.trim();
          const right = row.querySelector('.vl-match-right').value.trim();
          if (left && right) pairs.push({ left, right });
        });
        if (pairs.length < 2) {
          alert('Add at least two complete pairs.');
          return false;
        }
        startPlace('vl-matching', { pairs });
        return true;
      }
    );
    const rows = document.getElementById('vl-match-rows');
    const addRow = (l = '', r = '') => {
      const div = document.createElement('div');
      div.className = 'vl-match-row';
      div.innerHTML = `<input class="vl-match-left" placeholder="Left (e.g. $y=x^2$)" value="${esc(l)}" />
        <span>↔</span>
        <input class="vl-match-right" placeholder="Right (e.g. parabola)" value="${esc(r)}" />`;
      rows.appendChild(div);
    };
    addRow();
    addRow();
    addRow();
    document.getElementById('vl-match-add').addEventListener('click', () => addRow());
  }

  function openGraphCreator() {
    openModal(
      'Dynamic graph',
      `<label>Mode</label>
       <select id="vl-graph-mode">
         <option value="quadratic">Quick sliders: y = a(x − h)² + k</option>
         <option value="url">Paste Desmos or GeoGebra link</option>
       </select>
       <div id="vl-graph-url-wrap" style="display:none;">
         <label>Graph URL</label>
         <input type="url" id="vl-graph-url" placeholder="https://www.desmos.com/calculator/..." />
       </div>
       <div id="vl-graph-quad-wrap">
         <p class="info-text">Students get sliders for a, h, and k inside a Desmos graph.</p>
       </div>`,
      () => {
        const mode = document.getElementById('vl-graph-mode').value;
        if (mode === 'url') {
          const url = document.getElementById('vl-graph-url').value.trim();
          if (!isSafeGraphUrl(url)) {
            alert('Paste a https://www.desmos.com or https://www.geogebra.org link.');
            return false;
          }
          startPlace('vl-graph', { mode: 'url', url });
          return true;
        }
        startPlace('vl-graph', {
          mode: 'quadratic',
          expressions: ['y=a(x-h)^2+k'],
          state: { a: 1, h: 0, k: 0 }
        });
        return true;
      }
    );
    const modeSel = document.getElementById('vl-graph-mode');
    const sync = () => {
      const urlMode = modeSel.value === 'url';
      document.getElementById('vl-graph-url-wrap').style.display = urlMode ? 'block' : 'none';
      document.getElementById('vl-graph-quad-wrap').style.display = urlMode ? 'none' : 'block';
    };
    modeSel.addEventListener('change', sync);
  }

  function isSafeGraphUrl(url) {
    try {
      const u = new URL(url);
      if (u.protocol !== 'https:') return false;
      const host = u.hostname.replace(/^www\./, '');
      return host === 'desmos.com' || host.endsWith('.desmos.com') || host === 'geogebra.org' || host.endsWith('.geogebra.org');
    } catch (_) {
      return false;
    }
  }

  /* ---------- Insert into editor ---------- */

  function insertAtPlacement(type, data) {
    let node = null;
    if (type === 'vl-callout' || type === 'callout') node = buildCalloutEditorNode(data);
    else if (type === 'vl-steps' || type === 'steps') node = buildStepsEditorNode(data);
    else if (type === 'vl-matching' || type === 'matching') node = buildMatchingEditorNode(data);
    else if (type === 'vl-graph' || type === 'graph') node = buildGraphEditorNode(data);
    if (node) insertNode(node);
  }

  function removeBtnHtml() {
    return `<button type="button" class="vl-embed-remove" title="Remove">Remove</button>`;
  }

  function bindRemove(el) {
    const btn = el.querySelector('.vl-embed-remove');
    if (btn) {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (confirm('Remove this block?')) el.remove();
      });
    }
  }

  function buildCalloutEditorNode(data) {
    const kind = data.kind || 'trap';
    const el = document.createElement('div');
    el.className = `vl-callout vl-callout-${kind} editor-embed-flow`;
    el.contentEditable = 'false';
    el.dataset.vlKind = kind;
    el.dataset.vlTitle = data.title || '';
    el.dataset.vlBody = data.body || '';
    applyFlow(el, '');
    el.innerHTML = `${calloutInnerHtml(kind, data.title, data.body)}${removeBtnHtml()}`;
    bindRemove(el);
    return el;
  }

  function calloutInnerHtml(kind, title, body) {
    const icon =
      kind === 'strategy'
        ? '💡'
        : kind === 'mascot'
          ? `<img src="${MASCOT_SRC}" alt="" class="vl-callout-mascot" />`
          : '⚠️';
    const label = kind === 'strategy' ? 'Test strategy' : kind === 'mascot' ? 'Mascot tip' : 'Watch out';
    return `<div class="vl-callout-icon">${icon}</div>
      <div class="vl-callout-body"><h4>${esc(title || label)}</h4><p>${esc(body || '')}</p></div>`;
  }

  function buildStepsEditorNode(data) {
    const el = document.createElement('div');
    el.className = 'vl-step-reveal editor-embed-flow';
    el.contentEditable = 'false';
    el.dataset.vlId = uid('steps');
    el.dataset.vlSteps = encodeData(data.steps || []);
    el.dataset.vlPrompt = data.prompt || '';
    applyFlow(el, '');
    const steps = data.steps || [];
    el.innerHTML = `<div class="vl-embed-label">Step reveal (${steps.length} steps)</div>
      <ol class="vl-step-preview">${steps.map((s) => `<li>${esc(s)}</li>`).join('')}</ol>
      ${data.prompt ? `<p class="vl-step-prompt-preview">Prediction: ${esc(data.prompt)}</p>` : ''}
      ${removeBtnHtml()}`;
    bindRemove(el);
    return el;
  }

  function buildMatchingEditorNode(data) {
    const el = document.createElement('div');
    el.className = 'vl-matching editor-embed-flow';
    el.contentEditable = 'false';
    el.dataset.vlId = uid('match');
    el.dataset.vlPairs = encodeData(data.pairs || []);
    applyFlow(el, '');
    const pairs = data.pairs || [];
    el.innerHTML = `<div class="vl-embed-label">Matching game (${pairs.length} pairs)</div>
      <ul class="vl-match-preview">${pairs.map((p) => `<li>${esc(p.left)} ↔ ${esc(p.right)}</li>`).join('')}</ul>
      ${removeBtnHtml()}`;
    bindRemove(el);
    return el;
  }

  function buildGraphEditorNode(data) {
    const el = document.createElement('div');
    el.className = 'vl-graph-embed editor-embed-flow';
    el.contentEditable = 'false';
    el.dataset.vlId = uid('graph');
    el.dataset.vlGraph = encodeData(data);
    applyFlow(el, '');
    const label =
      data.mode === 'url' ? `Graph: ${data.url || 'link'}` : 'Desmos: y = a(x − h)² + k';
    el.innerHTML = `<div class="vl-embed-label">${esc(label)}</div>
      <p class="vl-graph-preview-note">Students will see an interactive graph here.</p>
      ${removeBtnHtml()}`;
    bindRemove(el);
    return el;
  }

  /* ---------- Viewer hydration ---------- */

  function hydrateViewer(root) {
    const host = root || document.getElementById('course-viewer-content') || document.getElementById('course-content-display');
    if (!host) return;
    wrapLegacyCallouts(host);
    host.querySelectorAll('.vl-step-reveal').forEach(hydrateSteps);
    host.querySelectorAll('.vl-matching').forEach(hydrateMatching);
    host.querySelectorAll('.vl-graph-embed').forEach(hydrateGraph);
    host.querySelectorAll('.vl-embed-remove').forEach((btn) => btn.remove());
    typeset(host);
  }

  function wrapLegacyCallouts(root) {
    if (!root) return;
    root.querySelectorAll('h3, h4').forEach((h) => {
      if (h.closest('.vl-callout')) return;
      const text = (h.textContent || '').trim();
      let kind = null;
      if (/^common mistake/i.test(text) || /^watch out/i.test(text)) kind = 'trap';
      else if (/^test strategy/i.test(text)) kind = 'strategy';
      if (!kind) return;
      const box = h.closest('div') || h.parentElement;
      if (!box || box.classList.contains('vl-callout')) return;
      const alreadyAmber =
        /fffbeb|fcd34d|fef3c7/i.test(box.getAttribute('style') || '') || box === h.parentElement;
      const target = alreadyAmber && box !== root ? box : h;
      wrapNodeAsCallout(target === h ? wrapHeadingWithSiblings(h) : target, kind);
    });
  }

  function wrapHeadingWithSiblings(h) {
    const wrap = document.createElement('div');
    h.parentNode.insertBefore(wrap, h);
    wrap.appendChild(h);
    let n = wrap.nextSibling;
    while (n && n.nodeType === Node.ELEMENT_NODE && !/^H[1-6]$/.test(n.tagName) && !n.classList.contains('quiz-question-placeholder') && !n.classList.contains('vl-callout')) {
      const next = n.nextSibling;
      wrap.appendChild(n);
      n = next;
      if (wrap.children.length > 4) break;
    }
    return wrap;
  }

  function wrapNodeAsCallout(node, kind) {
    if (!node || node.classList.contains('vl-callout')) return;
    node.classList.add('vl-callout', `vl-callout-${kind}`);
    node.dataset.vlKind = kind;
    if (!node.querySelector('.vl-callout-icon')) {
      const icon = document.createElement('div');
      icon.className = 'vl-callout-icon';
      icon.textContent = kind === 'strategy' ? '💡' : '⚠️';
      node.insertBefore(icon, node.firstChild);
    }
  }

  function hydrateSteps(el) {
    if (el.dataset.vlHydrated === '1') return;
    el.dataset.vlHydrated = '1';
    const steps = decodeData(el.dataset.vlSteps) || [];
    const prompt = el.dataset.vlPrompt || '';
    if (!steps.length) return;
    let shown = 0;
    let predicted = !prompt;
    el.innerHTML = `<div class="vl-embed-label">Worked steps</div>
      ${prompt ? `<div class="vl-step-pred"><label>${esc(prompt)}</label><input type="text" class="vl-step-pred-input" placeholder="Your guess" /><button type="button" class="vl-step-pred-btn">Check</button></div>` : ''}
      <ol class="vl-step-list"></ol>
      <button type="button" class="vl-step-next">Show next step</button>
      <p class="vl-step-done" hidden>All steps revealed.</p>`;
    const list = el.querySelector('.vl-step-list');
    const nextBtn = el.querySelector('.vl-step-next');
    const done = el.querySelector('.vl-step-done');
    const reveal = () => {
      if (shown >= steps.length) return;
      const li = document.createElement('li');
      li.className = 'vl-step-item';
      li.innerHTML = steps[shown];
      list.appendChild(li);
      typeset(li);
      shown += 1;
      if (shown >= steps.length) {
        nextBtn.hidden = true;
        done.hidden = false;
        awardXp('step_reveal', el.dataset.vlId);
      }
    };
    if (prompt) {
      nextBtn.disabled = true;
      el.querySelector('.vl-step-pred-btn').addEventListener('click', () => {
        predicted = true;
        nextBtn.disabled = false;
        const box = el.querySelector('.vl-step-pred');
        if (box) box.classList.add('vl-step-pred-done');
      });
    }
    nextBtn.addEventListener('click', () => {
      if (!predicted) return;
      reveal();
    });
  }

  function hydrateMatching(el) {
    if (el.dataset.vlHydrated === '1') return;
    el.dataset.vlHydrated = '1';
    const pairs = decodeData(el.dataset.vlPairs) || [];
    if (pairs.length < 2) return;
    const rights = pairs.map((p, i) => ({ text: p.right, i })).sort(() => Math.random() - 0.5);
    el.innerHTML = `<div class="vl-embed-label">Match each pair</div>
      <div class="vl-match-board">
        <div class="vl-match-left-col">${pairs
          .map(
            (p, i) =>
              `<button type="button" class="vl-match-chip vl-match-l" data-i="${i}">${esc(p.left)}</button>`
          )
          .join('')}</div>
        <div class="vl-match-right-col">${rights
          .map(
            (p) =>
              `<button type="button" class="vl-match-chip vl-match-r" data-i="${p.i}">${esc(p.text)}</button>`
          )
          .join('')}</div>
      </div>
      <p class="vl-match-status">Click a left item, then its match.</p>
      <button type="button" class="vl-match-check" hidden>Check matches</button>`;
    let selectedL = null;
        const matched = new Set();
        el.querySelectorAll('.vl-match-l').forEach((btn) => {
      btn.addEventListener('click', () => {
        el.querySelectorAll('.vl-match-l').forEach((b) => b.classList.remove('selected'));
        btn.classList.add('selected');
        selectedL = btn.getAttribute('data-i');
      });
    });
    el.querySelectorAll('.vl-match-r').forEach((btn) => {
      btn.addEventListener('click', () => {
        if (selectedL == null) return;
        const ri = btn.getAttribute('data-i');
        const leftBtn = el.querySelector(`.vl-match-l[data-i="${selectedL}"]`);
        if (matched.has(selectedL)) return;
        if (String(selectedL) === String(ri)) {
          matched.add(selectedL);
          leftBtn.classList.add('vl-match-ok');
          btn.classList.add('vl-match-ok');
          leftBtn.disabled = true;
          btn.disabled = true;
        } else {
          leftBtn.classList.add('vl-match-bad');
          btn.classList.add('vl-match-bad');
          setTimeout(() => {
            leftBtn.classList.remove('vl-match-bad', 'selected');
            btn.classList.remove('vl-match-bad');
          }, 600);
        }
        selectedL = null;
        el.querySelectorAll('.vl-match-l').forEach((b) => b.classList.remove('selected'));
        if (matched.size === pairs.length) {
          el.querySelector('.vl-match-status').textContent = 'Perfect match!';
          awardXp('matching', el.dataset.vlId);
        }
      });
    });
    typeset(el);
  }

  async function hydrateGraph(el) {
    if (el.dataset.vlHydrated === '1') return;
    el.dataset.vlHydrated = '1';
    const spec = decodeData(el.dataset.vlGraph) || {};
    const mount = document.createElement('div');
    mount.className = 'vl-graph-host';
    el.innerHTML = '';
    el.appendChild(mount);
    if (spec.mode === 'url' && spec.url && isSafeGraphUrl(spec.url)) {
      const iframe = document.createElement('iframe');
      iframe.src = toEmbedUrl(spec.url);
      iframe.title = 'Interactive graph';
      iframe.setAttribute('loading', 'lazy');
      iframe.allow = 'fullscreen';
      mount.appendChild(iframe);
      return;
    }
    try {
      if (typeof window.__veelearnLoadHeavy === 'function') {
        await window.__veelearnLoadHeavy('widgets');
      }
    } catch (_) {
      /* ignore */
    }
    const eng = window.VeelearnWidgetEngine;
    if (eng && typeof eng.mountWidget === 'function') {
      const exprs = spec.expressions || ['y=a(x-h)^2+k'];
      const joined = exprs.join(' ');
      const isQuad =
        spec.mode === 'quadratic' || /a\s*\(\s*x\s*-\s*h\s*\)\s*\^\s*2/i.test(joined);
      const quadInputs = [
        { key: 'a', type: 'slider', label: 'a (stretch)', min: -5, max: 5, step: 0.1 },
        { key: 'h', type: 'slider', label: 'h (left / right)', min: -10, max: 10, step: 0.5 },
        { key: 'k', type: 'slider', label: 'k (up / down)', min: -10, max: 10, step: 0.5 }
      ];
      await eng.mountWidget(mount, {
        title: isQuad ? 'y = a(x − h)² + k' : 'Dynamic graph',
        state: Object.assign({ a: 1, h: 0, k: 0 }, spec.state || {}),
        inputs: isQuad ? quadInputs : spec.inputs || [],
        view: { width: 640, height: 380 },
        behavior: {
          preset: 'desmos_graph',
          params: { expressions: exprs }
        }
      });
    } else {
      mount.innerHTML = '<p>Graph widget unavailable.</p>';
    }
  }

  function toEmbedUrl(url) {
    try {
      const u = new URL(url);
      if (u.hostname.includes('desmos.com') && !u.pathname.includes('/calculator/')) {
        return url;
      }
      if (u.hostname.includes('geogebra.org') && !u.searchParams.has('embed')) {
        u.searchParams.set('embed', '1');
        return u.toString();
      }
      return url;
    } catch (_) {
      return url;
    }
  }

  function awardXp(kind, id) {
    if (window.CourseProgress && typeof window.CourseProgress.awardInteractive === 'function') {
      window.CourseProgress.awardInteractive(kind, id);
    }
  }

  /* ---------- Reading chunking ---------- */

  function countWordsInHtml(html) {
    const tmp = document.createElement('div');
    tmp.innerHTML = html || '';
    tmp.querySelectorAll(CHECKPOINT_SELECTOR + ', ' + EMBED_SELECTOR).forEach((n) => n.remove());
    const text = (tmp.innerText || tmp.textContent || '').replace(/\s+/g, ' ').trim();
    if (!text) return 0;
    return text.split(' ').filter(Boolean).length;
  }

  function htmlHasCheckpoint(html) {
    const tmp = document.createElement('div');
    tmp.innerHTML = html || '';
    return !!tmp.querySelector(CHECKPOINT_SELECTOR);
  }

  function updateWordCountTip() {
    const editor = document.getElementById('course-content-editor');
    if (!editor) return;
    if (!wordTipEl) {
      wordTipEl = document.getElementById('vl-word-tip');
    }
    if (!wordTipEl) return;
    const html = editor.innerHTML || '';
    const words = countWordsInHtml(html);
    const hasCheck = htmlHasCheckpoint(html);
    if (words > WORD_LIMIT && !hasCheck) {
      wordTipEl.hidden = false;
      wordTipEl.textContent = `Tip: this page is ${words} words with no checkpoint. Insert a Quick Check or Widget here to break up the reading!`;
    } else {
      wordTipEl.hidden = true;
    }
  }

  function checkPublishGate(pages) {
    const list = Array.isArray(pages) ? pages : [];
    let run = 0;
    for (let i = 0; i < list.length; i++) {
      if (htmlHasCheckpoint(list[i])) run = 0;
      else run += 1;
      if (run >= 3) {
        alert(
          'Add a Quick Check or interactive widget at least every 2–3 pages before submitting. (Draft save is still allowed.)'
        );
        return false;
      }
    }
    return true;
  }

  function setup() {
    if (setupDone) {
      setupToolbar();
      return;
    }
    setupDone = true;
    setupToolbar();
    ensureModals();
  }

  window.CourseInteractiveBlocks = {
    EMBED_SELECTOR,
    CHECKPOINT_SELECTOR,
    setup,
    insertAtPlacement,
    hydrateViewer,
    wrapLegacyCallouts,
    htmlHasCheckpoint,
    checkPublishGate,
    updateWordCountTip,
    openCreator,
    isSafeGraphUrl
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => setTimeout(setup, 0));
  } else {
    setTimeout(setup, 0);
  }
})();
