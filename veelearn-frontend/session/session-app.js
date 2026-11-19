/**
 * Session page controller.
 *
 * One question on screen at a time, graded on the server. The page never decides
 * whether an answer is right — it renders whatever the engine returns, so a
 * modified client cannot award itself XP or a mastery dot.
 */
(function () {
  const API_BASE_URL = (() => {
    const host = window.location.hostname;
    if (host.includes('veelearn.org')) return 'https://api.veelearn.org';
    if (host.includes('github.io')) return 'https://veelearn.onrender.com';
    if (host === 'localhost' || host === '127.0.0.1') return 'http://localhost:3000';
    return window.location.origin;
  })();

  const token = localStorage.getItem('token');
  if (!token) {
    window.location.href = 'index.html';
    return;
  }

  const params = new URLSearchParams(window.location.search);
  const storedMinutes = parseInt((() => { try { return localStorage.getItem('learnerSessionMinutes') || ''; } catch (_) { return ''; } })(), 10);
  const requestedMinutes = Math.min(90, Math.max(5, parseInt(params.get('minutes') || '', 10) || storedMinutes || 15));
  const requestedTrack = params.get('track') || '';
  const requestedMode = params.get('mode') || '';
  const requestedCourse = params.get('course') || '';
  const requestedSession = params.get('session') || '';

  const esc = (window.SessionMap && window.SessionMap.esc) || String;
  const dotsHtml = (window.SessionMap && window.SessionMap.dotsHtml) || (() => '');
  const trackName = (window.SessionMap && window.SessionMap.trackName) || ((t) => t || 'Practice');

  const el = (id) => document.getElementById(id);

  // MathJax arrives async; every render asks it to typeset the live nodes so a
  // stem like $(x-r)^2$ never shows as raw dollars.
  let mathPending = false;

  function mathReady() {
    const mj = window.MathJax;
    return !!(mj && mj.startup && typeof mj.typesetPromise === 'function');
  }

  /**
   * MathJax is loaded async, so the first renders happen before it exists. Rather
   * than dropping those calls (which is why LaTeX only appeared after answering,
   * when a later render happened to land), remember that a typeset is owed and
   * run it the moment the typesetter is up.
   */
  let typesetTimer = null;

  /**
   * MathJax rejects a typeset call made while it is still working on the previous
   * one (which is exactly what happens when a streamed lesson is being typeset as
   * the first question appears). Coalesce the calls, and retry if it was busy —
   * otherwise the stem kept its raw dollars until some later render.
   */
  function typesetContent() {
    if (!mathReady()) {
      mathPending = true;
      const wait = () => {
        if (mathReady()) {
          if (mathPending) {
            mathPending = false;
            typesetContent();
          }
          return;
        }
        setTimeout(wait, 120);
      };
      setTimeout(wait, 120);
      return;
    }
    clearTimeout(typesetTimer);
    typesetTimer = setTimeout(() => runTypeset(0), 60);
  }

  function runTypeset(attempt) {
    const nodes = ['sx-stem', 'sx-options', 'sx-feedback', 'sx-hintbox', 'sx-intro-text', 'sx-ask-log']
      .map((id) => document.getElementById(id))
      .filter(Boolean);
    if (!nodes.length) return;
    Promise.resolve(window.MathJax.startup.promise)
      .then(() => window.MathJax.typesetPromise(nodes))
      .catch(() => {
        if (attempt < 6) setTimeout(() => runTypeset(attempt + 1), 220);
      });
  }

  const state = {
    id: null,
    session: null,
    item: null,
    question: null,
    hints: 0,
    qStart: 0,
    deadline: 0,
    timer: null,
    busy: false,
    solved: false,
    ending: false,
    ended: false,
    introSeen: new Set(),
    map: null,
    lastSolution: null,
    visualReady: false
  };

  const TIER_LABEL = { 1: 'recall', 2: 'apply', 3: 'stretch', 4: 'challenge' };

  // ------------------------------------------------------------------ helpers
  async function api(path, body) {
    // A request that never settles used to leave `busy` true forever, which reads
    // as "the buttons stopped working". Every call now has a deadline.
    const controller = typeof AbortController === 'function' ? new AbortController() : null;
    const timer = controller ? setTimeout(() => controller.abort(), 40000) : null;
    let res;
    try {
      res = await fetch(`${API_BASE_URL}${path}`, {
        method: body ? 'POST' : 'GET',
        headers: Object.assign(
          { Authorization: `Bearer ${token}` },
          body ? { 'Content-Type': 'application/json' } : {}
        ),
        credentials: 'include',
        body: body ? JSON.stringify(body) : undefined,
        signal: controller ? controller.signal : undefined
      });
    } catch (err) {
      throw new Error(
        err && err.name === 'AbortError' ? 'That took too long. Try again.' : 'Network error. Try again.'
      );
    } finally {
      if (timer) clearTimeout(timer);
    }

    if (res.status === 401 || res.status === 403) {
      localStorage.removeItem('token');
      window.location.href = 'index.html';
      throw new Error('Please sign in again');
    }

    const payload = await res.json().catch(() => ({}));
    if (!res.ok || payload.success === false) {
      throw new Error(payload.message || `Something went wrong (${res.status})`);
    }
    return payload.data;
  }

  function showError(message) {
    const box = el('sx-error');
    if (!box) return;
    box.textContent = message || 'Something went wrong. Try again.';
    box.hidden = false;
  }

  function hideError() {
    const box = el('sx-error');
    if (box) {
      box.hidden = true;
      box.textContent = '';
    }
  }

  function hideCards() {
    ['sx-intro', 'sx-question-card', 'sx-summary'].forEach((id) => {
      const node = el(id);
      if (node) node.hidden = true;
    });
  }

  // -------------------------------------------------------------------- timer
  function formatClock(ms) {
    const total = Math.max(0, Math.round(ms / 1000));
    const m = Math.floor(total / 60);
    const s = total % 60;
    return `${m}:${String(s).padStart(2, '0')}`;
  }

  function stopTimer() {
    if (state.timer) {
      clearInterval(state.timer);
      state.timer = null;
    }
  }

  function paintTimer() {
    const left = Math.max(0, state.deadline - Date.now());
    const node = el('sx-timer');
    if (node) {
      node.textContent = formatClock(left);
      node.classList.toggle('is-low', left < 60000);
    }
    if (left <= 0) {
      stopTimer();
      finish('time');
    }
  }

  function startTimer(remainingMs) {
    stopTimer();
    state.deadline = Date.now() + Math.max(0, Number(remainingMs) || 0);
    paintTimer();
    state.timer = setInterval(paintTimer, 1000);
  }

  // -------------------------------------------------------------------- focus
  /**
   * The rail lists one skill per row, grouped by the unit it belongs to. Each
   * row's single circle is that skill (not a four-dot mastery strip): the count
   * matches the skills in the unit, hovering names the skill and its level, and
   * a completed skill's circle fills in as the plan advances.
   */
  function renderFocus(focus, activeId) {
    const list = el('sx-focus');
    if (!list) return;
    const groups = [];
    (focus || []).forEach((f) => {
      const key = f.unitLabel || (f.unitIndex ? `Unit ${f.unitIndex}` : 'This session');
      let group = groups.find((g) => g.key === key);
      if (!group) {
        group = { key, items: [] };
        groups.push(group);
      }
      group.items.push(f);
    });

    list.innerHTML = groups
      .map((group) => {
        const done = group.items.filter((f) => f.status === 'done').length;
        const rows = group.items
          .map((f) => {
            const isActive = Number(f.id) === Number(activeId);
            const mark = f.status === 'done' ? '✓' : f.status === 'deferred' ? '–' : isActive ? '●' : '○';
            const cls = ['sx-focus-item'];
            if (f.status === 'done') cls.push('is-done');
            else if (f.status === 'deferred') cls.push('is-deferred');
            else if (isActive) cls.push('is-active');
            const level = Math.max(0, Math.min(4, Number(f.level) || 0));
            const state = f.status === 'done' ? 'done' : isActive ? 'current skill' : 'not started';
            const tip = `${f.name} — ${state}, mastery ${level} of 4`;
            return `<li class="${cls.join(' ')}" title="${esc(tip)}">
          <span class="sx-focus-mark" title="${esc(f.name)}" aria-hidden="true">${mark}</span>
          <span class="sx-focus-name">${esc(f.name)}</span>
          ${f.isReview ? '<span class="sx-badge">review</span>' : ''}
          <span class="sx-focus-level" title="Mastery ${level} of 4">${level}/4</span>
        </li>`;
          })
          .join('');
        return `<li class="sx-focus-unit">
          <p class="sx-unit-name"><span>${esc(group.key)}</span><span class="sx-unit-count">${done}/${group.items.length}</span></p>
          <ul class="sx-unit-skills">${rows}</ul>
        </li>`;
      })
      .join('');
  }

  // -------------------------------------------------------------------- cards
  /**
   * A lesson written now, for this unit, streamed as the model types it. The
   * static `item.intro` is only the seed: the learner watches it being written
   * instead of being handed the finished paragraph after a spinner.
   *
   * A vague unit can make the tutor think out loud ("The user wants me to…").
   * That is not a lesson: planning lines are dropped here, and every remaining
   * section is kept — a lesson with worked examples has many paragraphs, so
   * keeping only the last one (the old behaviour) threw the teaching away.
   */
  const PLANNING_TELL =
    /(the user wants|the user is asking|the user asked|the learner wants|i need to teach|i should teach|i should interpret|given the ambiguity|the safest approach is|that actually makes sense|the most sensible interpretation|as an ai|these instructions|this prompt|word count|let me (?:think|plan|write|draft|work out))/i;
  const PLANNING_LEAD =
    /^(the user|the learner|i need to|i should|i'll|i will now|let me|we need to|okay,?\s+(?:so|let)|hmm\b|wait\b|given the ambiguity|the most sensible|plan:|draft:|outline of the lesson|thinking:)/i;

  function cleanLesson(text) {
    let raw = String(text || '').trim();
    if (!raw) return '';
    raw = raw
      .replace(/<(?:thinking|thought|reasoning|scratchpad)>[\s\S]*?<\/(?:thinking|thought|reasoning|scratchpad)>/gi, ' ')
      .replace(/^\s*(?:thinking|planning|reasoning|analysis|scratchpad)\s*:[^\n]*(?:\n(?!\s*\n)[^\n]*)*/i, ' ')
      .trim();
    if (!raw) return '';

    const kept = [];
    let dropping = false;
    raw.split(/\r?\n/).forEach((line) => {
      const trimmed = line.trim();
      if (!trimmed) {
        dropping = false;
        kept.push('');
        return;
      }
      // A section heading always belongs to the lesson.
      if (/^#{1,4}\s/.test(trimmed)) {
        dropping = false;
        kept.push(trimmed);
        return;
      }
      if (dropping) return;
      const meta =
        PLANNING_TELL.test(trimmed) ||
        (PLANNING_LEAD.test(trimmed) && /\b(i|me|we|the user|the learner)\b/i.test(trimmed.slice(0, 40)));
      if (meta) {
        dropping = true;
        return;
      }
      kept.push(trimmed);
    });

    const out = kept
      .join('\n')
      .replace(/\n{3,}/g, '\n\n')
      .trim();
    return out.length >= 40 ? out : '';
  }

  /** **bold** only; everything else stays text so MathJax still sees $...$. */
  function renderInline(node, text) {
    String(text || '')
      .split(/\*\*([^*]{1,160})\*\*/g)
      .forEach((part, i) => {
        if (!part) return;
        if (i % 2 === 1) {
          const strong = document.createElement('strong');
          strong.textContent = part;
          node.appendChild(strong);
        } else {
          node.appendChild(document.createTextNode(part));
        }
      });
  }

  /**
   * The learning section: the model writes "## The idea", worked examples with
   * numbered steps and a "Watch out" block. Render those as real headings, lists
   * and tables so a long lesson reads like a lesson instead of one wall of text.
   */
  function renderLesson(box, text) {
    if (!box) return null;
    const raw = String(text || '').trim();
    box.textContent = '';
    if (!raw) return null;

    let firstTable = null;
    raw
      .split(/\n{2,}/)
      .map((block) => block.trim())
      .filter(Boolean)
      .forEach((block) => {
        const lines = block
          .split('\n')
          .map((l) => l.trim())
          .filter(Boolean);
        if (!lines.length) return;

        const head = lines[0].match(/^#{1,4}\s+(.*)$/);
        if (head) {
          const h = document.createElement('h3');
          h.className = 'sx-lesson-h';
          h.textContent = head[1].replace(/[:.]+$/, '');
          box.appendChild(h);
          lines.shift();
          if (!lines.length) return;
        }

        if (lines.every((l) => /^[-*•]\s+/.test(l))) {
          const ul = document.createElement('ul');
          ul.className = 'sx-lesson-list';
          lines.forEach((l) => {
            const li = document.createElement('li');
            renderInline(li, l.replace(/^[-*•]\s+/, ''));
            ul.appendChild(li);
          });
          box.appendChild(ul);
          return;
        }

        if (lines.every((l) => /^\d+[.)]\s+/.test(l))) {
          const ol = document.createElement('ol');
          ol.className = 'sx-lesson-list sx-lesson-steps';
          lines.forEach((l) => {
            const li = document.createElement('li');
            renderInline(li, l.replace(/^\d+[.)]\s+/, ''));
            ol.appendChild(li);
          });
          box.appendChild(ol);
          return;
        }

        if (lines.some((l) => /^\|/.test(l))) {
          const holder = document.createElement('div');
          holder.className = 'sx-lesson-table';
          const table = renderTables(holder, lines.join('\n'));
          if (table) {
            box.appendChild(holder);
            if (!firstTable) firstTable = table;
            return;
          }
        }

        const p = document.createElement('p');
        p.className = 'sx-lesson-p';
        renderInline(p, lines.join(' '));
        box.appendChild(p);
      });

    return firstTable || box.querySelector('.sx-table');
  }

  function paintSentences(box, text) {
    const raw = String(text || '');
    const parts = raw.match(/[^.!?\n]*[.!?]+[\s]*|\n+|.+$/g) || [];
    box.textContent = '';
    const spans = [];
    parts.forEach((part) => {
      if (!part) return;
      const span = document.createElement('span');
      span.className = 'sx-sent';
      span.textContent = part;
      box.appendChild(span);
      spans.push(span);
    });
    return spans;
  }

  let lastPointAt = 0;
  let lastPointed = null;

  /** Keep Vee beside the sentence it is currently writing, not the whole block. */
  function pointAtSentence(spans, box) {
    if (!state.visualReady || !window.Mascot) return;
    const target = (spans && spans.length ? spans[spans.length - 1] : box) || null;
    if (!target) return;
    if (!target || target === lastPointed) return;
    if (Date.now() - lastPointAt < 600) return;
    lastPointAt = Date.now();
    lastPointed = target;
    Mascot.mood('talking');
    Promise.resolve(Mascot.pointAt(target)).catch(() => {});
  }

  /**
   * Once the lesson is on screen, underline the parts worth remembering.
   * MathJax rewrites the paragraph, so the anchor is the block and the phrase is
   * matched against the text actually rendered — a span would already be gone.
   */
  function underlineKeyParts(box, text) {
    if (!state.visualReady || !window.Annotate || !box) return;
    const shown = String(box.innerText || box.textContent || '').replace(/\s+/g, ' ');
    const src = String(text || shown).replace(/\s+/g, ' ');
    const sentences = (src.match(/[^.!?]*[.!?]+/g) || [src]).map((s) => s.trim()).filter((s) => s.length > 24);
    if (!sentences.length) return;
    const math = sentences.find((s) => /\$[^$]+\$/.test(s));
    const rule = sentences.find((s) => /\b(because|means|remember|rule|key|notice|so)\b/i.test(s));
    const picks = [math || rule || sentences[0]].filter(Boolean);
    picks.forEach((sentence, i) => {
      const clean = sentence.replace(/\$[^$]*\$/g, ' ').replace(/\s+/g, ' ').trim();
      const words = clean.split(' ').filter(Boolean);
      // Start on something worth underlining, not on "It" or "So".
      const lead = /^(it|this|that|they|so|and|but|then)$/i.test(words[0] || '') ? 1 : 0;
      const body = words.slice(lead);
      let phrase = '';
      for (let n = Math.min(7, body.length); n >= 3; n -= 1) {
        const slice = body.slice(0, n);
        // Do not end a passage on a preposition or a joining word.
        if (/^(from|of|to|in|for|with|and|or|but|so|the|a|an)$/i.test(slice[slice.length - 1] || '')) continue;
        const cand = slice.join(' ').replace(/[,;:]$/, '');
        if (cand.length >= 8 && shown.includes(cand)) {
          phrase = cand;
          break;
        }
      }
      if (!phrase) return;
      setTimeout(() => {
        ink(() => Annotate.underline({ anchor: box, text: phrase, ms: 420 }));
        if (i === 0 && window.Mascot) Promise.resolve(Mascot.pointAt(box)).catch(() => {});
      }, 260 + i * 340);
    });
  }

  async function streamTeach(container, { silent } = {}) {
    if (!state.id) return '';
    const box = container || el('sx-intro-text');
    if (!box) return '';
    box.textContent = '';
    box.classList.add('is-streaming');
    el('sx-teach-status').hidden = !silent;
    lastPointed = null;

    let text = '';
    let typesetAt = 0;
    let lastPaint = 0;
    try {
      const res = await fetch(`${API_BASE_URL}/api/session/${state.id}/teach`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({})
      });
      if (!res.ok || !res.body) throw new Error('teach unavailable');

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';
      for (;;) {
        const { value, done } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const frames = buffer.split('\n\n');
        buffer = frames.pop() || '';
        for (const frame of frames) {
          const lines = frame.split('\n');
          const event = (lines.find((l) => l.startsWith('event:')) || '').slice(6).trim();
          const dataLine = lines.find((l) => l.startsWith('data:'));
          if (!dataLine) continue;
          let data = {};
          try {
            data = JSON.parse(dataLine.slice(5).trim());
          } catch (_) {
            continue;
          }
          if (event === 'delta' && data.t) {
            // One chunk at a time: this is the model's own token, not a replay.
            text += data.t;
            if (Date.now() - lastPaint > 90) {
              lastPaint = Date.now();
              // Headings are markers, not words: while the lesson is being typed
              // they would appear as "##". They become real headings at the end.
              const live = cleanLesson(text).replace(/^#{1,4}\s+/gm, '');
              pointAtSentence(paintSentences(box, live), box);
            }
            if (Date.now() - typesetAt > 700) {
              typesetAt = Date.now();
              typesetContent();
            }
          } else if (event === 'done' && data.text) {
            text = data.text;
            pointAtSentence(paintSentences(box, cleanLesson(text)), box);
          }
        }
      }
    } catch (_) {
      text = box.textContent || '';
    }
    text = cleanLesson(text) || String(text || '');
    if (!String(text).trim() && state.item && state.item.intro) {
      text = state.item.intro;
      paintSentences(box, text);
    }

    box.classList.remove('is-streaming');
    el('sx-teach-status').hidden = true;
    // The finished lesson is laid out in sections: idea, worked examples, watch out.
    const table = renderLesson(box, text);
    typesetContent();
    if (table && state.visualReady && window.Mascot) {
      Promise.resolve(Mascot.pointAt(table)).catch(() => {});
    } else {
      underlineKeyParts(box, text);
    }
    return text;
  }

  function showIntro(sessionState) {
    const item = sessionState.item;
    hideCards();
    el('sx-loading').hidden = true;
    el('sx-intro').hidden = false;
    el('sx-intro-kicker').textContent = item.isReview ? 'Review' : 'Learning';
    el('sx-intro-skill').textContent = item.name;
    el('sx-intro-text').textContent = item.intro || '';
    el('sx-intro-start').textContent = 'Start practice';
    if (state.visualReady && window.Mascot) {
      Mascot.mood('talking');
      Promise.resolve(Mascot.pointAt('#sx-intro-text')).catch(() => {});
    }

    const teachBtn = el('sx-intro-teach');
    let taught = false;
    const teach = async () => {
      if (teachBtn) {
        teachBtn.disabled = true;
        teachBtn.textContent = 'Writing…';
      }
      await streamTeach(el('sx-intro-text'));
      taught = true;
      if (teachBtn) {
        teachBtn.disabled = false;
        teachBtn.textContent = 'Explain it again';
      }
      // The practice button stays under the lesson, however long it ran.
      const start = el('sx-intro-start');
      if (start) {
        start.disabled = false;
        start.textContent = 'Start practice';
      }
    };
    if (teachBtn) teachBtn.onclick = teach;
    // Teach on arrival: the first thing a learner sees is Vee explaining, and the
    // text is being written while they read it.
    teach();
    // Meanwhile the unit's first question is being written server-side. Fetch it
    // in the background so "Let's go" usually has it already.
    if (!sessionState.question) {
      api(`/api/session/${state.id}`)
        .then((next) => {
          if (next && next.question) state.prefetched = next;
        })
        .catch(() => {});
    }

    const btn = el('sx-intro-start');
    btn.disabled = false;
    btn.textContent = 'Start practice';
    btn.onclick = () => {
      state.introSeen.add(Number(item.id));
      state.item = item;
      if (sessionState.question) {
        showQuestion(sessionState.question, item);
        return;
      }
      // No card yet: the server writes one on demand, so wait for it instead of
      // bouncing between intro and a refresh that never resolves.
      if (state.prefetched && state.prefetched.question) {
        applyState(state.prefetched);
        state.prefetched = null;
        return;
      }
      showWriting();
      loadCard();
    };
    return taught;
  }

  /** The "Vee is writing this one" state while a question is generated. */
  function showWriting() {
    hideCards();
    el('sx-loading').hidden = false;
    el('sx-loading').textContent = 'Vee is writing this question…';
  }

  /** Fetch the session until it has a card for the current item (on-demand AI). */
  async function loadCard(tries = 0) {
    try {
      const sessionState = await api(`/api/session/${state.id}`);
      if (sessionState.question) {
        applyState(sessionState);
        return;
      }
      if (sessionState.summary || sessionState.session.status === 'completed') {
        applyState(sessionState);
        return;
      }
      if (tries < 14) {
        setTimeout(() => loadCard(tries + 1), 2000);
        return;
      }
      showError('That unit has no questions yet. Try another session.');
    } catch (err) {
      showError(err.message);
    }
  }

  function renderOptions(options) {
    const box = el('sx-options');
    box.innerHTML = '';
    (options || []).forEach((opt) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'sx-option';
      btn.dataset.key = opt.k;
      btn.dataset.annotate = `opt-${opt.k}`;
      btn.innerHTML = `<span class="sx-option-key">${esc(opt.k)}</span><span class="sx-option-text">${esc(opt.t)}</span>`;
      btn.addEventListener('click', () => submit(opt.k));
      box.appendChild(btn);
    });
    typesetContent();
  }

  function setOptionsEnabled(enabled) {
    el('sx-options')
      .querySelectorAll('button')
      .forEach((b) => {
        b.disabled = !enabled;
      });
  }

  function renderFigure(question) {
    const box = el('sx-figure');
    if (!box) return;
    box.innerHTML = '';
    box.hidden = true;
    const v = question && question.visual;
    if (!v || typeof v !== 'object') return;

    const src = v.image || v.image_url || v.url || v.src;
    if (typeof src === 'string' && src) {
      const img = document.createElement('img');
      img.src = src;
      img.alt = String(v.alt || v.caption || 'Question diagram');
      img.loading = 'lazy';
      box.appendChild(img);
    } else if (typeof v.svg === 'string' && v.svg.trim().toLowerCase().startsWith('<svg')) {
      // Bank diagrams are authored SVGs, so they can go in as-is; scripts are not.
      box.innerHTML = String(v.svg).replace(/<script[\s\S]*?<\/script>/gi, '');
    }

    const caption = v.caption || v.alt || v.description || v.label;
    if (caption) {
      const p = document.createElement('p');
      p.className = 'sx-figure-cap';
      p.textContent = String(caption);
      box.appendChild(p);
    }
    box.hidden = box.childElementCount === 0;
  }

  /**
   * The source chip on the card.
   *
   * Only a third-party question is credited: an OpenBookQA or GSM8K item shows
   * "OpenBookQA · Apache-2.0" (tap or hover for the full author/licence line); a
   * question Veelearn wrote shows nothing at all. Called from showQuestion, so a
   * fresh card and a resumed one render identically.
   */
  function renderProvenance(question) {
    const chip = el('sx-q-src');
    const credit = el('sx-q-src-credit');
    if (!chip) return;
    const prov = window.QBankProvenance;
    const third = prov ? prov.isThirdParty(question) : Boolean(question && question.source && question.source !== 'authored');
    if (!third) {
      chip.hidden = true;
      chip.textContent = '';
      chip.removeAttribute('title');
      if (credit) {
        credit.hidden = true;
        credit.textContent = '';
      }
      return;
    }
    const label = prov ? prov.label(question) : String(question.source || 'Third-party');
    const detail = prov ? prov.detail(question) : String(question.attribution || '');
    chip.hidden = false;
    chip.textContent = label;
    if (detail) chip.title = detail;
    else chip.removeAttribute('title');
    if (credit) {
      credit.hidden = true;
      credit.textContent = detail || label;
    }
  }

  function showQuestion(question, item) {
    if (window.Annotate) Annotate.clear();
    if (state.visualReady && window.Mascot) {
      Mascot.hideBubble();
      Mascot.mood('idle');
      Mascot.park();
    }
    if (window.Board && Board.isOpen()) Board.close();

    state.question = question;
    state.item = item;
    state.hints = 0;
    state.solved = false;
    state.busy = false;
    state.qStart = Date.now();

    hideCards();
    el('sx-loading').hidden = true;
    el('sx-question-card').hidden = false;

    el('sx-q-skill').textContent = item.name;
    el('sx-q-tier').textContent = `tier ${question.tier} · ${TIER_LABEL[question.tier] || 'practice'}`;
    el('sx-stem').textContent = question.stem;
    renderProvenance(question);
    renderFigure(question);
    const card = el('sx-question-card');
    if (card) {
      card.classList.remove('is-in');
      void card.offsetWidth;
      card.classList.add('is-in');
    }
    typesetContent();

    // Vee is still on the job when a saved session reopens: point at the question
    // on screen and underline the part of it that carries the ask.
    if (state.visualReady) {
      setTimeout(() => {
        if (window.Mascot) Promise.resolve(Mascot.pointAt('#sx-stem')).catch(() => {});
        underlineKeyParts(el('sx-stem'), question.stem);
      }, 320);
    }

    renderOptions(question.options);
    setOptionsEnabled(true);

    const feedback = el('sx-feedback');
    feedback.hidden = true;
    feedback.innerHTML = '';

    const hintbox = el('sx-hintbox');
    hintbox.hidden = true;
    hintbox.textContent = '';

    const askLog = el('sx-ask-log');
    if (askLog) {
      askLog.innerHTML = '';
      askLog.hidden = true;
    }

    const hintBtn = el('sx-hint-btn');
    hintBtn.hidden = false;
    hintBtn.disabled = false;
    hintBtn.textContent = 'Need a hint';
    el('sx-skip-btn').hidden = false;

    renderFocus(state.session ? state.session.focus : [], item.id);
  }

  // ------------------------------------------------------------------ grading
  async function submit(key) {
    if (state.busy || state.solved || !state.item || !state.question) return;
    state.busy = true;
    setOptionsEnabled(false);
    hideError();

    const box = el('sx-options');
    const picked = box.querySelector(`[data-key="${CSS.escape(String(key))}"]`);
    if (picked) picked.classList.add('is-picked');

    try {
      const result = await api(`/api/session/${state.id}/answer`, {
        itemId: state.item.id,
        questionId: state.question.id,
        answer: key,
        ms: Date.now() - state.qStart,
        hints: state.hints
      });
      state.hints = 0;
      state.solved = true;
      renderFeedback(result, key);
    } catch (err) {
      if (picked) picked.classList.remove('is-picked');
      showError(err.message);
    } finally {
      // Released whatever happened: a stuck request must never leave the card dead.
      if (!state.solved) {
        state.busy = false;
        setOptionsEnabled(true);
      }
    }
  }

  function markOptions(correctKey, chosenKey) {
    el('sx-options')
      .querySelectorAll('.sx-option')
      .forEach((btn) => {
        const k = btn.dataset.key;
        btn.disabled = true;
        if (k === correctKey) btn.classList.add('is-right');
        else if (k === chosenKey) btn.classList.add('is-wrong');
      });
  }

  function renderFeedback(result, chosenKey) {
    const good = !!result.correct;
    const itemName = (result.item && result.item.name) || (state.item && state.item.name) || 'this skill';

    // Reveal the key only now that grading has happened.
    if (good) {
      const card = el('sx-options').querySelector(`[data-key="${CSS.escape(String(chosenKey))}"]`);
      if (card) card.classList.add('is-right');
    } else if (result.solution) {
      markOptions(result.solution.answer, chosenKey);
    } else {
      const card = el('sx-options').querySelector(`[data-key="${CSS.escape(String(chosenKey))}"]`);
      if (card) card.classList.add('is-wrong');
    }

    const parts = [
      `<p class="sx-verdict ${good ? 'is-good' : 'is-bad'}" data-annotate="verdict">${good ? 'Correct.' : 'Not quite.'}</p>`
    ];

    if (good) {
      const dots = (result.mastery && result.mastery.dots) || [];
      const filled = dots.filter(Boolean).length;
      const count = result.item ? `${result.item.correctCount} of ${result.item.needed} correct` : 'Counted';
      parts.push(
        result.mastery && result.mastery.levelUp
          ? `<p class="sx-line">Level up — ${esc(itemName)} now has ${filled} of 4 dots. ${count} for this focus item.</p>`
          : `<p class="sx-line">${count} for this focus item. ${filled} of 4 dots in ${esc(itemName)}.</p>`
      );
    } else {
      if (result.selected) {
        parts.push(`<p class="sx-line">You chose ${esc(chosenKey)} — ${esc(result.selected)}.</p>`);
      }
      if (result.why) parts.push(`<p class="sx-line sx-why" data-annotate="why">${esc(result.why)}</p>`);
      if (result.hint) parts.push(`<p class="sx-line sx-hintline"><strong>Hint.</strong> ${esc(result.hint)}</p>`);
      if (result.solution && result.solution.steps && result.solution.steps.length) {
        parts.push(`<div class="sx-solution" data-annotate="solution">
          <p class="sx-kicker">The full method</p>
          <ol>${result.solution.steps.map((s) => `<li>${esc(s)}</li>`).join('')}</ol>
          <p class="sx-line" data-annotate="solution-answer">Answer: <strong>${esc(result.solution.answer)}</strong>. Here is an easier one to lock it in.</p>
          <button type="button" class="sx-ghost" id="sx-board-btn">Show me on the board</button>
        </div>`);
      }
    }

    if (!good) {
      parts.push('<button type="button" class="sx-ghost" id="sx-explain-btn">Explain it another way</button>');
    }

    if (result.reward && (result.reward.xp || result.reward.gems)) {
      parts.push(`<p class="sx-reward-line">+${result.reward.xp} XP · +${result.reward.gems} gems</p>`);
    }

    const label = good
      ? result.next === 'advance'
        ? 'Continue'
        : 'Next question'
      : result.next === 'retry'
        ? 'Try again'
        : 'Continue';

    parts.push(`<button type="button" class="sx-btn sx-primary sx-continue" id="sx-continue">${label}</button>`);

    const feedback = el('sx-feedback');
    feedback.innerHTML = parts.join('');
    feedback.hidden = false;
    typesetContent();
    state.lastSolution = result.solution || null;

    const boardBtn = el('sx-board-btn');
    if (boardBtn) boardBtn.addEventListener('click', drawBoard);

    const explainBtn = el('sx-explain-btn');
    if (explainBtn) explainBtn.addEventListener('click', explainAgain);

    react(good, result, chosenKey);

    el('sx-hint-btn').hidden = true;
    el('sx-skip-btn').hidden = true;

    if (result.totals) el('sx-xp').textContent = `${result.totals.xp} XP`;

    if (result.item) {
      state.item = Object.assign({}, state.item, {
        correctCount: result.item.correctCount,
        attempts: result.item.attempts,
        needed: result.item.needed
      });
    }

    if (state.session) {
      const doneId = result.item && result.item.done ? Number(result.item.id) : null;
      const focus = (state.session.focus || []).map((f) => {
        // Match the row first: a review card's question belongs to a different
        // skill id, so a skillId-only match left the rail stuck at the old level.
        const byRow = doneId && Number(f.id) === doneId;
        const bySkill = Number(f.skillId) === Number(result.item && result.item.skillId);
        if (!byRow && !bySkill) return f;
        const next = Object.assign({}, f, { level: result.mastery ? result.mastery.levelAfter : f.level });
        if (byRow) next.status = 'done';
        return next;
      });
      state.session.focus = focus;
      renderFocus(focus, state.item && state.item.id);
    }

    // A finished focus item gets the small celebration; confetti is for the goal.
    if (result.item && result.item.done && window.Celebrate) {
      Celebrate.item(el('sx-focus').querySelector('.is-done'), {
        xp: result.reward ? result.reward.xp : 0,
        level: result.mastery ? result.mastery.levelAfter : undefined
      });
    }

    el('sx-continue').addEventListener('click', () => advance(result));
  }

  function advance(result) {
    if (result.next === 'retry') {
      // Same card, second attempt: clear the explanation and let them answer.
      state.solved = false;
      state.busy = false;
      const feedback = el('sx-feedback');
      feedback.hidden = true;
      feedback.innerHTML = '';
      el('sx-options')
        .querySelectorAll('.sx-option')
        .forEach((btn) => {
          btn.disabled = false;
          btn.classList.remove('is-picked', 'is-wrong', 'is-right');
        });
      el('sx-hint-btn').hidden = false;
      el('sx-skip-btn').hidden = false;
      state.qStart = Date.now();
      return;
    }

    if ((result.next === 'more' || result.next === 'variant') && result.question) {
      showQuestion(result.question, state.item);
      return;
    }

    refresh();
  }

  // -------------------------------------------------------------------- state
  function applyState(sessionState) {
    if (!sessionState || !sessionState.session) {
      showError('That session could not be loaded.');
      return;
    }

    hideError();
    state.id = sessionState.session.id;
    state.session = sessionState;
    state.map = sessionState.map;

    el('sx-app').setAttribute('aria-busy', 'false');
    el('sx-loading').hidden = true;
    el('sx-goal-label').textContent = sessionState.session.goal || 'Practice session';
    el('sx-track').textContent = trackName(sessionState.session.track);
    el('sx-xp').textContent = `${sessionState.session.xpAwarded || 0} XP`;

    if (state.map) window.SessionMap && window.SessionMap.render(el('sx-map'), state.map, sessionState.session.track);

    const summary = sessionState.summary;
    if (sessionState.session.status === 'completed' || summary) {
      renderFocus(sessionState.focus, null);
      showSummary(summary, sessionState.session);
      return;
    }

    if (!sessionState.item) {
      finish('goal');
      return;
    }

    renderFocus(sessionState.focus, sessionState.item.id);
    startTimer(sessionState.session.remainingMs);

    // A review is a test, not a lesson: it opens straight on its card, so nobody
    // has to sit through a teach stream (or press through one) to start it.
    const fresh =
        !sessionState.item.isReview &&
        Number(sessionState.item.attempts) === 0 &&
        !state.introSeen.has(Number(sessionState.item.id));
    // A new skill always opens on its learning section: the lesson is written from
    // the outline, so it does not depend on a stored intro paragraph existing.
    if (fresh) showIntro(sessionState);
    else if (sessionState.question) showQuestion(sessionState.question, sessionState.item);
    else refresh();
  }

  async function refresh() {
    try {
      const sessionState = await api(`/api/session/${state.id}`);
      applyState(sessionState);
    } catch (err) {
      showError(err.message);
    }
  }

  // ------------------------------------------------------------------- hint
  async function askHint() {
    if (!state.question || state.solved) return;
    const btn = el('sx-hint-btn');
    btn.disabled = true;
    try {
      const out = await api(`/api/session/${state.id}/hint`, { questionId: state.question.id });
      const box = el('sx-hintbox');
      box.textContent = out.hint || 'Look again at what the question is really asking you to find.';
      box.hidden = false;
      typesetContent();
      if (state.visualReady && window.Mascot) {
        Mascot.mood('thinking');
        Promise.resolve(Mascot.pointAt('#sx-hintbox')).catch(() => {});
      }
      if (window.Annotate) {
        Promise.resolve(
          Annotate.underline({ anchor: '#sx-hintbox', text: box.textContent.slice(0, 40), ms: 300 })
        ).catch(() => {});
      }
      state.hints = Number(out.level) || state.hints + 1;
      btn.textContent = out.exhausted ? 'That is all the hints' : 'Another hint';
      btn.disabled = !!out.exhausted;
    } catch (err) {
      btn.disabled = false;
      showError(err.message);
    }
  }

  // ------------------------------------------------------------------- skip
  async function skip() {
    if (!state.item) return;
    hideError();
    el('sx-skip-btn').disabled = true;
    try {
      const out = await api(`/api/session/${state.id}/skip`, { itemId: state.item.id });
      if (out.state) applyState(out.state);
      else refresh();
    } catch (err) {
      showError(err.message);
    } finally {
      el('sx-skip-btn').disabled = false;
    }
  }

  // -------------------------------------------------------------------- end
  function showSummary(summary, session) {
    stopTimer();
    hideCards();
    el('sx-loading').hidden = true;
    el('sx-summary').hidden = false;
    el('sx-end-btn').hidden = true;

    const text = (summary && summary.text) || 'Session saved. Everything you did today counts.';
    el('sx-summary-text').textContent = text;
    el('sx-summary-next').textContent = (summary && summary.nextStep) || '';

    if (summary && summary.aiLine) showAiLine(summary.aiLine);

    const earned = state.lastEndReward || { xp: 0, gems: 0 };
    const xp = Number(earned.xp || 0) + Number((session && session.xpAwarded) || 0);
    const gems = Number(earned.gems || 0) + Number((session && session.gemsAwarded) || 0);
    el('sx-summary-rewards').innerHTML =
      xp || gems
        ? `${xp ? `<span>+${xp} XP</span>` : ''}${gems ? `<span>+${gems} gems</span>` : ''}`
        : '';

    const heading = el('sx-summary-title');
    if (heading) heading.textContent = session && session.status === 'completed' ? 'Session saved.' : 'Nice work.';
  }

  /** The model's end-of-session line, asked for after the ending is already on screen. */
  function showAiLine(text) {
    const stale = document.querySelector('.sx-ai-line');
    if (stale) stale.remove();
    if (!text) return;
    const line = document.createElement('p');
    line.className = 'sx-line sx-ai-line';
    line.textContent = text;
    el('sx-summary-text').insertAdjacentElement('afterend', line);
  }

  async function requestSummaryLine() {
    if (!state.id) return;
    try {
      const out = await api(`/api/session/${state.id}/summary`, {});
      if (out && out.line && !out.fallback) showAiLine(out.line);
    } catch (_) {
      /* the stored summary stands */
    }
  }

  async function finish(reason) {
    if (state.ended || state.ending || !state.id) return;
    state.ending = true;
    stopTimer();
    try {
      const out = await api(`/api/session/${state.id}/end`, { reason });
      state.ended = true;
      state.lastEndReward = (out && out.reward) || { xp: 0, gems: 0 };
      if (out && out.state) {
        state.session = out.state;
        window.SessionMap && window.SessionMap.render(el('sx-map'), out.state.map, out.state.session.track);
        renderFocus(out.state.focus, null);
      }
      showSummary({ text: out.summary, nextStep: out.nextStep, aiLine: out.aiLine }, out.state && out.state.session);
      requestSummaryLine();

      if (window.Celebrate && out.done > 0) {
        const session = (out.state && out.state.session) || {};
        const reward = out.reward || {};
        Celebrate.goal({
          xp: Number(session.xpAwarded || reward.xp || 0),
          gems: Number(session.gemsAwarded || reward.gems || 0),
          onChoose: (choice) => {
            if (choice === 'keep') window.location.href = `session.html?minutes=${state.session ? state.session.minutes : requestedMinutes}`;
          }
        });
      }
    } catch (err) {
      state.ending = false;
      showError(err.message);
    }
  }


  // ------------------------------------------------------------ visual teaching
  /** Run an annotation without ever letting it break the session. */
  function ink(fn) {
    try {
      const p = fn();
      if (p && typeof p.catch === 'function') p.catch(() => {});
    } catch (_) {
      /* cosmetic only */
    }
  }

  /**
   * P3: the model chooses the script. The server validates every step against the
   * primitive whitelist and always answers with something playable — when it
   * cannot (no key, 429, bad JSON) it returns the deterministic template and the
   * page plays that instead. Ink is cosmetic either way: never let it break a turn.
   */
  async function requestAI(kind, extra) {
    if (!state.id || !state.question) return null;
    try {
      const out = await api(`/api/session/${state.id}/ai`, Object.assign({
        kind,
        questionId: state.question.id,
        attempts: state.lastAttempts,
        correct: false
      }, extra || {}));
      if (!out || out.ok === false || !Array.isArray(out.script)) return null;
      return out;
    } catch (_) {
      return null;
    }
  }

  /** A quick confetti puff for every correct answer: fun, cheap, no canvas. */
  function confettiBurst() {
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    const colors = ['#ea580c', '#f59e0b', '#22c55e', '#3b82f6', '#ec4899'];
    const host = document.createElement('div');
    host.className = 'sx-confetti';
    host.setAttribute('aria-hidden', 'true');
    for (let i = 0; i < 26; i += 1) {
      const bit = document.createElement('i');
      const angle = Math.random() * Math.PI * 2;
      const dist = 60 + Math.random() * 120;
      bit.style.background = colors[i % colors.length];
      bit.style.left = 50 + '%';
      bit.style.top = 40 + '%';
      bit.style.setProperty('--dx', Math.cos(angle) * dist + 'px');
      bit.style.setProperty('--dy', Math.sin(angle) * dist + 'px');
      bit.style.animationDelay = Math.random() * 90 + 'ms';
      host.appendChild(bit);
    }
    document.body.appendChild(host);
    setTimeout(() => host.remove(), 1100);
  }

  /** Play a validated script, saying the line first so the ink lands on speech. */
  function playAI(payload) {
    if (!window.Annotate || !Array.isArray(payload.script)) return false;
    // A board step is not an annotation: open the drawing, then play the ink
    // around it. The validator only lets a whitelisted preset through.
    const boardStep = payload.script.find((s) => s && s.do === 'board');
    if (boardStep && window.Board) {
      Board.open({
        title: state.item ? state.item.name : 'On the board',
        steps: ((state.lastSolution && state.lastSolution.steps) || []).slice(0, 3),
        preset: boardStep.preset,
        params: boardStep.params
      }).catch(() => {});
    }
    const steps = [];
    if (payload.say) steps.push({ at: 0, do: 'say', text: payload.say });
    let lastAt = 0;
    for (const step of payload.script) {
      if (!step || step.do === 'board') continue;
      steps.push(step);
      lastAt = Math.max(lastAt, Number(step.at) || 0);
    }
    if (payload.ask && payload.ask.text) steps.push({ at: lastAt + 500, do: 'say', text: payload.ask.text });
    if (window.Mascot && payload.mood) Mascot.mood(payload.mood);
    Promise.resolve(Annotate.play(steps, { tail: 500 })).catch(() => {});
    return true;
  }

  /** The pre-P3 choreography: used when the AI turn cannot be reached at all. */
  function ruleFirstMiss(optionEl, result) {
    if (window.Mascot) Mascot.mood('oops');
    ink(() => Annotate.circle({ anchor: optionEl, ms: 380 }));
    ink(() => Mascot.moveTo('#sx-feedback [data-annotate="why"]'));

    const why = String(result.why || '');
    const first = why.split('. ')[0];
    const phrase = first ? (first.endsWith('.') ? first : `${first}.`) : '';
    if (phrase && phrase.length > 8 && why.includes(phrase)) {
      ink(() => Annotate.underline({ anchor: '#sx-feedback [data-annotate="why"]', text: phrase, ms: 320 }));
    }
  }

  function ruleReteach(optionEl) {
    if (window.Mascot) Mascot.mood('oops');
    ink(() => Annotate.strike({ anchor: optionEl, ms: 320 }));
    ink(() => Annotate.box({ anchor: '#sx-feedback [data-annotate="solution"]', ms: 380 }));
    ink(() => Annotate.stamp({ anchor: '#sx-feedback [data-annotate="solution-answer"]', mark: 'v', ms: 300 }));
    ink(() => Mascot.pointAt('#sx-feedback [data-annotate="solution"]'));
  }

  /**
   * The visual reaction to a graded answer.
   *   wrong #1 → one narrowing move (FUNNEL, authored reason: no AI call)
   *   wrong #2 → reteach (TEACH): model-chosen script, cached, template fallback
   *   correct  → stamp + dots, no AI call
   */
  function react(good, result, chosenKey) {
    if (!state.visualReady) return;
    const optionEl = `#sx-options [data-key="${CSS.escape(String(chosenKey))}"]`;

    if (good) {
      if (window.Mascot) Mascot.mood('happy');
      confettiBurst();
      ink(() => Annotate.stamp({ anchor: optionEl, mark: 'v', ms: 300 }));
      if (result.mastery && result.mastery.levelUp && window.Celebrate) {
        const filled = (result.mastery.dots || []).filter(Boolean).length;
        Celebrate.levelUp({ text: `${filled} of 4 dots · ${state.item ? state.item.name : ''}` });
      }
      return;
    }

    const attempts = result.item ? Number(result.item.attempts) || 1 : 1;
    state.lastAttempts = attempts;
    state.lastChosen = chosenKey;

    if (result.solution) {
      // Second miss: the template plays now, the model upgrades it if it lands.
      // Free models here answer in 5–25 s, so nothing may wait on them.
      ruleReteach(optionEl);
      Promise.resolve(requestAI('reteach', { distractor: chosenKey, attempts }))
        .then((payload) => {
          if (!payload || payload.fallback) return; // the template on screen is the answer
          if (window.Annotate) Annotate.clear();
          playAI(payload);
        })
        .catch(() => {});
      return;
    }

    ruleFirstMiss(optionEl, result);
  }

  /** "Explain it another way" — one more AI turn, capped on the server. */
  async function explainAgain() {
    if (!state.question) return;
    const btn = el('sx-explain-btn');
    if (btn) {
      btn.disabled = true;
      btn.textContent = 'Thinking…';
    }
    const payload = await requestAI('explain_again', {
      distractor: state.lastChosen || '',
      attempts: state.lastAttempts || 1
    });
    if (btn) {
      btn.disabled = false;
      btn.textContent = 'Explain it another way';
    }
    if (!payload) {
      // Nothing playable came back: the deterministic rule is still better than silence.
      if (window.Annotate) Annotate.clear();
      if (state.lastChosen) ruleReteach(`#sx-options [data-key="${CSS.escape(String(state.lastChosen))}"]`);
      return;
    }
    if (window.Annotate) Annotate.clear();
    playAI(payload);
  }

  /** Does the learner's question ask Vee to show something rather than say it? */
  function wantsDrawing(question) {
    return /(^|\s)(draw|sketch|plot|graph|diagram|simulate|simulation|visuali[sz]e|number line|picture)\b/i.test(
      String(question || '')
    );
  }

  /**
   * The drawing for this question, generated for this question.
   *
   * The board used to fall back to a stock `y = a·x²` plot whenever the card had
   * no preset, which is why a fractions question could open a parabola. Now the
   * server writes a scene from the card and the authored method; when that is
   * unavailable the board shows the method itself, never an unrelated graph.
   */
  async function requestBoardScene(ask) {
    if (!state.id || !state.question) return null;
    try {
      const out = await api(`/api/session/${state.id}/board`, {
        questionId: state.question.id,
        ask: ask || ''
      });
      return out && out.scene ? out.scene : null;
    } catch (_) {
      return null;
    }
  }

  async function buildBoard(title, ask) {
    if (!window.Board) return;
    const question = state.question || {};
    const visual = question.visual && typeof question.visual === 'object' ? question.visual : {};
    const steps = ((state.lastSolution && state.lastSolution.steps) || []).slice(0, 3);
    const base = {
      title: title || (state.item ? state.item.name : 'On the board'),
      // Even with nothing to draw, the board holds the question and the ask, not
      // a diagram from another topic.
      steps: steps.length ? steps : [String(question.stem || 'Read the question once more.').slice(0, 220)]
    };
    if (window.Mascot) Mascot.mood('writing');

    if (visual.preset) {
      await Board.open(Object.assign({}, base, { preset: visual.preset, params: visual.params })).catch(() => {});
      if (state.visualReady && window.Mascot) Mascot.pointAt('#board').catch(() => {});
      return;
    }

    // Method first (instant), then the generated interactive scene on top.
    await Board.open(base).catch(() => {});
    if (state.visualReady && window.Mascot) Mascot.pointAt('#board').catch(() => {});
    const scene = await requestBoardScene(ask);
    if (!scene || !window.Board || !Board.isOpen()) return;
    await Board.scene(scene).catch(() => {});
  }

  /** Vee draws a small interactive sketch when the question asks to be shown. */
  function openQuickDraw(question) {
    return buildBoard('Vee’s sketch', question);
  }

  /** Board mode: the worked steps plus the drawing generated for this card. */
  function drawBoard() {
    return buildBoard(state.item ? state.item.name : 'On the board');
  }

  function initVisual() {
    if (state.visualReady) return;
    state.visualReady = true;
    if (window.Annotate) Annotate.attach(el('sx-stage'));
    // Resizing clears the ink layer; re-issue pointing and underlining for whatever
    // is on screen so a split-screen window is not less interactive than a full one.
    if (!state.onResize) {
      let resizeTimer = null;
      state.onResize = () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
          if (!state.visualReady) return;
          const intro = el('sx-intro');
          const introText = el('sx-intro-text');
          const stem = el('sx-stem');
          if (intro && !intro.hidden && introText) {
            if (window.Mascot) Promise.resolve(Mascot.pointAt(introText)).catch(() => {});
            underlineKeyParts(introText, introText.textContent);
          } else if (stem && state.question && el('sx-question-card') && !el('sx-question-card').hidden) {
            if (window.Mascot) Promise.resolve(Mascot.pointAt(stem)).catch(() => {});
            underlineKeyParts(stem, state.question.stem);
          }
        }, 420);
      };
      window.addEventListener('resize', state.onResize);
    }
    if (window.Mascot) {
      Promise.resolve(Mascot.attach('#sx-mascot-host'))
        .then(() => {
          Mascot.park();
          Mascot.mood('idle');
          // A resumed session renders its card before the mascot exists, so the
          // pointing and underline are re-issued here rather than lost.
          if (state.question && el('sx-question-card') && !el('sx-question-card').hidden) {
            setTimeout(() => {
              Promise.resolve(Mascot.pointAt('#sx-stem')).catch(() => {});
              underlineKeyParts(el('sx-stem'), state.question.stem);
            }, 400);
          }
        })
        .catch(() => {});
      // Clicking Vee is a shortcut for "show me on the board".
      const host = document.querySelector('#sx-mascot-host');
      if (host) {
        host.style.cursor = 'pointer';
        host.title = 'Click Vee to draw this on the board';
        host.addEventListener('click', () => drawBoard());
      }
    }
  }


  // ------------------------------------------------- read aloud (QoL 11)
  /** Browser speech only: no API, no key, works offline, stops on mute. */
  function speak(text) {
    if (!state.readAloud || !text || !window.speechSynthesis) return;
    try {
      window.speechSynthesis.cancel();
      const line = new SpeechSynthesisUtterance(String(text).slice(0, 400));
      line.rate = 0.95;
      window.speechSynthesis.speak(line);
    } catch (_) {
      /* speech is a bonus, never a failure */
    }
  }

  function paintReadButton() {
    const btn = el('sx-read-btn');
    if (!btn) return;
    btn.textContent = state.readAloud ? 'Read aloud: on' : 'Read aloud: off';
    btn.setAttribute('aria-pressed', String(state.readAloud));
  }

  function toggleReadAloud() {
    state.readAloud = !state.readAloud;
    localStorage.setItem('veelearnReadAloud', state.readAloud ? '1' : '0');
    if (!state.readAloud && window.speechSynthesis) {
      try {
        window.speechSynthesis.cancel();
      } catch (_) {}
    }
    paintReadButton();
  }

  // ---------------------------------------------------------------- modal
  function openModal(title, html) {
    el('sx-modal-title').textContent = title;
    el('sx-modal-body').innerHTML = html;
    el('sx-modal').hidden = false;
  }
  function closeModal() {
    el('sx-modal').hidden = true;
    el('sx-modal-body').innerHTML = '';
  }

  function flash(message) {
    const box = el('sx-summary-next');
    if (box) box.textContent = message;
  }

  // ------------------------------------------------------------- rating
  async function rateSession(stars) {
    if (!state.id) return;
    try {
      await api(`/api/session/${state.id}/rate`, { rating: Number(stars) });
      state.rated = Number(stars);
      el('sx-stars').querySelectorAll('.sx-star').forEach((btn) => {
        btn.classList.toggle('is-on', Number(btn.dataset.stars) <= Number(stars));
      });
    } catch (err) {
      flash(err.message);
    }
  }

  // -------------------------------------------------------- transcript
  async function downloadTranscript() {
    if (!state.id) return;
    try {
      const out = await api(`/api/session/${state.id}/transcript`);
      const blob = new Blob([out.markdown || ''], { type: 'text/markdown;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = out.filename || `veelearn-session-${state.id}.md`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      setTimeout(() => URL.revokeObjectURL(url), 2000);
    } catch (err) {
      flash(err.message);
    }
  }

  // --------------------------------------------------------- flashcards
  async function makeCards() {
    if (!state.id) return;
    try {
      const out = await api(`/api/session/${state.id}/flashcards`, {});
      const total = Array.isArray(out.cards) ? out.cards.length : 0;
      flash(
        out.created
          ? `${out.created} card${out.created === 1 ? '' : 's'} saved. ${total} waiting in your deck.`
          : `No new cards — your deck already has these (${total} card${total === 1 ? '' : 's'}).`
      );
    } catch (err) {
      flash(err.message);
    }
  }

  async function saveNote() {
    if (!state.id) return;
    try {
      await api(`/api/session/${state.id}/note`, {});
      flash('Saved to your notes — searchable from this button any time.');
    } catch (err) {
      flash(err.message);
    }
  }

  // ---------------------------------------------------- history + digest
  async function openHistory() {
    openModal('My sessions', '<p class="sx-modal-note">Loading…</p>');
    let history = { sessions: [] };
    let digest = null;
    try {
      history = await api('/api/session/history?limit=20');
      digest = await api('/api/profile/digest').catch(() => null);
    } catch (err) {
      el('sx-modal-body').innerHTML = `<p class="sx-modal-note">${esc(err.message)}</p>`;
      return;
    }

    const rows = (history.sessions || [])
      .map(
        (row) => `
      <li class="sx-hist-row">
        <div>
          <strong>${esc((row.startedAt || '').slice(0, 10))}</strong>
          <span class="sx-hist-meta">${row.minutes || 0} min · ${esc(row.mode || 'focus')}${
            row.rating ? ` · ${row.rating}★` : ''
          }</span>
          <p class="sx-hist-summary">${esc(row.summary || 'No summary saved.')}</p>
        </div>
      </li>`
      )
      .join('');

    el('sx-modal-body').innerHTML = `
      <label class="sx-modal-label" for="sx-hist-search">Search by skill or summary</label>
      <input type="text" id="sx-hist-search" class="sx-modal-input" placeholder="exponents, fractions, energy…" />
      <ul class="sx-hist" id="sx-hist-list">${rows || '<li class="sx-modal-note">No finished sessions yet.</li>'}</ul>

      <div class="sx-digest">
        <h3>Weekly digest for a parent</h3>
        <p class="sx-modal-note">${
          digest && digest.sent
            ? 'Last digest sent to ' + esc(digest.emailedTo || 'your parent') + '.'
            : 'One email a week: sessions, minutes, skills. Opt in whenever you like.'
        }</p>
        <input type="email" id="sx-parent-email" class="sx-modal-input" placeholder="parent@example.com"
          value="${esc((digest && digest.emailedTo) || '')}" />
        <label class="sx-check"><input type="checkbox" id="sx-digest-on" ${digest && digest.emailedTo ? 'checked' : ''} /> Email it weekly</label>
        <button type="button" class="sx-btn sx-primary" id="sx-digest-save">Save</button>
      </div>`;

    const search = el('sx-hist-search');
    if (search) {
      search.addEventListener('input', async () => {
        const term = search.value.trim();
        try {
          const found = await api(`/api/session/history?limit=20&q=${encodeURIComponent(term)}`);
          const list = el('sx-hist-list');
          list.innerHTML = (found.sessions || [])
            .map(
              (row) => `<li class="sx-hist-row"><div><strong>${esc((row.startedAt || '').slice(0, 10))}</strong>
                <span class="sx-hist-meta">${row.minutes || 0} min · ${esc(row.mode || 'focus')}</span>
                <p class="sx-hist-summary">${esc(row.summary || 'No summary saved.')}</p></div></li>`
            )
            .join('') || '<li class="sx-modal-note">Nothing matches that yet.</li>';
        } catch (_) {
          /* keep the previous list */
        }
      });
    }

    const save = el('sx-digest-save');
    if (save) {
      save.addEventListener('click', async () => {
        try {
          await api('/api/profile/digest', {
            parentEmail: el('sx-parent-email').value.trim(),
            optIn: el('sx-digest-on').checked
          });
          save.textContent = 'Saved';
        } catch (err) {
          save.textContent = err.message;
        }
      });
    }
  }

  // ------------------------------------------------------------- exam sprint
  async function loadExam() {
    try {
      const status = await api('/api/profile/exam');
      const block = el('sx-exam');
      const copy = el('sx-exam-copy');
      const go = el('sx-exam-go');
      const input = el('sx-exam-date');
      if (status.examDate) input.value = status.examDate;
      block.hidden = false;
      if (status.sprintAvailable) {
        copy.textContent = status.offer;
        go.hidden = false;
      } else if (status.examDate) {
        copy.textContent = `Exam on ${status.examDate} — sprints open 45 days out.`;
        go.hidden = true;
      } else {
        copy.textContent = 'Set an exam date and the page offers a 6-item sprint.';
        go.hidden = true;
      }
    } catch (_) {
      /* signed-out or offline: the rail block stays hidden */
    }
  }

  async function saveExam() {
    const value = el('sx-exam-date').value;
    try {
      await api('/api/profile/exam', { date: value || null });
      await loadExam();
    } catch (err) {
      showError(err.message);
    }
  }

  // ------------------------------------------------------------- shortcuts
  // A–D or 1–4 answers, Enter continues, H asks for a hint, S skips. Typing in a
  // field is left alone.
  function wireShortcuts() {
    document.addEventListener('keydown', (e) => {
      const tag = (e.target && e.target.tagName) || '';
      if (/INPUT|TEXTAREA|SELECT/.test(tag) || e.metaKey || e.ctrlKey || e.altKey) return;
      if (e.key === 'Enter') {
        const next = el('sx-continue');
        if (next && !next.hidden) {
          e.preventDefault();
          next.click();
        }
        return;
      }
      const key = String(e.key || '').toUpperCase();
      const asKey = { 1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F' }[key] || key;
      if (/^[A-F]$/.test(asKey)) {
        if (state.busy || state.solved || !state.question) return;
        const option = el('sx-options').querySelector(`[data-key="${asKey}"]`);
        if (option && !option.disabled) {
          e.preventDefault();
          submit(asKey);
        }
        return;
      }
      if (key === 'H') {
        const hint = el('sx-hint-btn');
        if (hint && !hint.hidden && !hint.disabled) hint.click();
      } else if (key === 'S') {
        const skip = el('sx-skip-btn');
        if (skip && !skip.hidden && !skip.disabled) skip.click();
      }
    });
  }

  // ---------------------------------------------------------------- ask Vee
  let asking = false;

  /**
   * Vee writes tables as markdown pipes. Show them as real tables instead of a
   * wall of "|" characters, and hand the table back so the mascot can point at it.
   */
  function renderTables(host, text) {
    if (!host) return null;
    const raw = String(text || '');
    const isRow = (line) => /^\s*\|/.test(line);
    if (!raw.split('\n').some(isRow)) {
      host.textContent = raw;
      return null;
    }
    const lines = raw.split('\n');
    const parts = [];
    let firstTable = null;
    let run = [];
    const flushRun = () => {
      if (!run.length) return;
      const block = document.createElement('div');
      block.className = 'sx-ask-p';
      block.textContent = run.join('\n').trim();
      if (block.textContent) parts.push(block);
      run = [];
    };
    for (let i = 0; i < lines.length; ) {
      if (!isRow(lines[i])) {
        run.push(lines[i]);
        i += 1;
        continue;
      }
      const block = [];
      while (i < lines.length && isRow(lines[i])) block.push(lines[i++]);
      const rows = block
        .map((line) =>
          line
            .trim()
            .replace(/^\|/, '')
            .replace(/\|$/, '')
            .split('|')
            .map((cell) => cell.trim())
        )
        .filter((cells) => !cells.every((cell) => cell === '' || /^:?-{2,}:?$/.test(cell)));
      if (rows.length < 2) {
        run.push(...block);
        continue;
      }
      flushRun();
      const table = document.createElement('table');
      table.className = 'sx-table';
      rows.forEach((cells, r) => {
        const tr = document.createElement('tr');
        cells.forEach((c) => {
          const cell = document.createElement(r === 0 ? 'th' : 'td');
          cell.textContent = c;
          tr.appendChild(cell);
        });
        table.appendChild(tr);
      });
      if (!firstTable) firstTable = table;
      parts.push(table);
    }
    flushRun();
    host.textContent = '';
    parts.forEach((part) => host.appendChild(part));
    return firstTable;
  }

  /**
   * The tutor sometimes drafts out loud ("sentence" (11) = 26). Keep the
   * finished sentences and drop the word-count working before it is shown.
   */
  function cleanAskText(text) {
    const raw = String(text || '');
    const quoted = raw.match(/"([^"]{8,})"\s*\(\d+\)/g) || [];
    if (quoted.length < 2) return raw;
    const kept = quoted
      .map((m) =>
        m
          .replace(/"\s*\(\d+\)$/, '')
          .replace(/^"/, '')
          .trim()
      )
      .filter(Boolean);
    return kept.length ? kept.join(' ') : raw;
  }

  async function askVee() {
    const input = el('sx-ask-input');
    const btn = el('sx-ask-btn');
    const log = el('sx-ask-log');
    if (!input || !log || asking || !state.id) return;
    const question = String(input.value || '').trim();
    if (!question) return;

    asking = true;
    if (btn) btn.disabled = true;
    input.value = '';
    log.hidden = false;

    const entry = document.createElement('div');
    entry.className = 'sx-ask-entry';
    const asked = document.createElement('p');
    asked.className = 'sx-ask-q';
    asked.textContent = question;
    const answer = document.createElement('p');
    answer.className = 'sx-ask-a is-streaming';
    answer.textContent = '';
    entry.appendChild(asked);
    entry.appendChild(answer);
    log.appendChild(entry);
    while (log.children.length > 4) log.removeChild(log.firstChild);
    entry.scrollIntoView({ block: 'nearest' });

    let text = '';
    let typesetAt = 0;
    // Typed out as the words arrive, not in one block when the stream ends.
    let shown = 0;
    let revealing = true;
    const reveal = () => {
      if (!revealing) return;
      if (shown < text.length) {
        shown = Math.min(text.length, shown + 3);
        answer.textContent = text.slice(0, shown);
      }
      setTimeout(reveal, 14);
    };
    setTimeout(reveal, 14);
    try {
      const res = await fetch(`${API_BASE_URL}/api/session/${state.id}/teach`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ question })
      });
      if (!res.ok || !res.body) throw new Error('unavailable');
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';
      for (;;) {
        const { value, done } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const frames = buffer.split('\n\n');
        buffer = frames.pop() || '';
        for (const frame of frames) {
          const lines = frame.split('\n');
          const event = (lines.find((l) => l.startsWith('event:')) || '').slice(6).trim();
          const dataLine = lines.find((l) => l.startsWith('data:'));
          if (!dataLine) continue;
          let data = {};
          try {
            data = JSON.parse(dataLine.slice(5).trim());
          } catch (_) {
            continue;
          }
          if (event === 'delta' && data.t) {
            text += data.t;
            if (Date.now() - typesetAt > 700) {
              typesetAt = Date.now();
              typesetContent();
            }
          } else if (event === 'done' && data.text) {
            text = data.text;
          }
        }
      }
    } catch (_) {
      // A stream that dies mid-sentence would otherwise leave half a word on screen.
      if (String(text || '').trim().length < 20) {
        text = 'I could not finish that answer — ask me again in a moment.';
      }
    }

    // Let the typing finish, so the answer never snaps in whole at the end.
    if (shown < text.length) {
      await new Promise((resolve) => {
        // A background tab throttles the typing; give it six seconds, then finish.
        const deadline = Date.now() + 6000;
        const wait = () =>
          shown >= text.length || Date.now() > deadline ? resolve() : setTimeout(wait, 30);
        wait();
      });
    }
    revealing = false;
    answer.classList.remove('is-streaming');
    const table = renderTables(answer, cleanAskText(text));
    typesetContent();
    if (table && state.visualReady && window.Mascot) {
      Mascot.mood('happy');
      Promise.resolve(Mascot.pointAt(table)).catch(() => {});
    }
    if (wantsDrawing(question)) openQuickDraw(question);
    asking = false;
    if (btn) btn.disabled = false;
  }

  // -------------------------------------------------------------------- boot
  async function boot() {
    try {
      // ?session=<id> opens exactly that session, so the dashboard can resume any
      // one of them rather than always starting the newest.
      if (requestedSession) {
        const existing = await api(`/api/session/${encodeURIComponent(requestedSession)}`);
        if (existing && existing.session && existing.session.status === 'active') {
          applyState(existing);
          initVisual();
          return;
        }
      }
      const body = { minutes: requestedMinutes };
      if (requestedTrack) body.track = requestedTrack;
      // ?course=<id> is how a course opens a session (§15.2). Without this the
      // server had no course to plan from and fell back to the learner's track.
      if (requestedCourse) {
        const id = parseInt(requestedCourse, 10);
        if (id) body.courseId = id;
      }
      const sessionState = await api('/api/session/start', body);
      applyState(sessionState);
      initVisual();
    } catch (err) {
      el('sx-loading').hidden = true;
      showError(err.message || 'Could not start a session.');
    }
  }

  async function extendSession() {
    const btn = el('sx-extend');
    if (!state.id || !btn) return;
    btn.disabled = true;
    btn.textContent = 'Adding…';
    try {
      const out = await api(`/api/session/${state.id}/extend`, { minutes: 10 });
      if (out && out.state) applyState(out.state);
      else refresh();
    } catch (err) {
      showError(err.message);
    } finally {
      btn.disabled = false;
      btn.textContent = '+10 min';
    }
  }

  function wire() {
    wireShortcuts();
    const extendBtn = el('sx-extend');
    if (extendBtn) extendBtn.addEventListener('click', extendSession);
    const askBtn = el('sx-ask-btn');
    if (askBtn) askBtn.addEventListener('click', askVee);
    const askInput = el('sx-ask-input');
    if (askInput) {
      askInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          e.preventDefault();
          askVee();
        }
      });
    }
    el('sx-hint-btn').addEventListener('click', askHint);
    el('sx-skip-btn').addEventListener('click', skip);
    // Tapping the source chip reveals the full credit (hover shows it as a title).
    if (el('sx-q-src')) {
      el('sx-q-src').addEventListener('click', () => {
        const credit = el('sx-q-src-credit');
        if (credit) credit.hidden = !credit.hidden;
      });
    }
    el('sx-end-btn').addEventListener('click', () => finish('quit'));

    const mapToggle = el('sx-map-toggle');
    mapToggle.addEventListener('click', () => {
      const panel = el('sx-map');
      const showing = panel.hidden;
      panel.hidden = !showing;
      mapToggle.setAttribute('aria-expanded', String(showing));
      mapToggle.textContent = showing ? 'Hide map' : 'Where I am';
      if (showing && state.map) {
        window.SessionMap && window.SessionMap.render(panel, state.map, state.session && state.session.session ? state.session.session.track : null);
      }
    });

    document.addEventListener('keydown', (e) => {
      if (e.target && /input|textarea/i.test(e.target.tagName)) return;
      const cont = el('sx-continue');
      if (e.key === 'Enter' && cont && !el('sx-feedback').hidden) {
        e.preventDefault();
        cont.click();
        return;
      }
      if (el('sx-question-card').hidden || state.solved) return;
      if (/^[1-4]$/.test(e.key)) {
        const btns = el('sx-options').querySelectorAll('.sx-option');
        const btn = btns[Number(e.key) - 1];
        if (btn && !btn.disabled) btn.click();
      } else if (e.key === 'h' || e.key === 'H') {
        askHint();
      }
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => { wire(); boot(); });
  else { wire(); boot(); }
})();
