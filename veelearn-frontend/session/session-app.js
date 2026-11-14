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
  const requestedMinutes = Math.min(45, Math.max(5, parseInt(params.get('minutes') || '10', 10) || 10));
  const requestedTrack = params.get('track') || '';

  const esc = (window.SessionMap && window.SessionMap.esc) || String;
  const dotsHtml = (window.SessionMap && window.SessionMap.dotsHtml) || (() => '');
  const trackName = (window.SessionMap && window.SessionMap.trackName) || ((t) => t || 'Practice');

  const el = (id) => document.getElementById(id);

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
    const res = await fetch(`${API_BASE_URL}${path}`, {
      method: body ? 'POST' : 'GET',
      headers: Object.assign(
        { Authorization: `Bearer ${token}` },
        body ? { 'Content-Type': 'application/json' } : {}
      ),
      credentials: 'include',
      body: body ? JSON.stringify(body) : undefined
    });

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
  function renderFocus(focus, activeId) {
    const list = el('sx-focus');
    if (!list) return;
    list.innerHTML = (focus || [])
      .map((f) => {
        const isActive = Number(f.id) === Number(activeId);
        const mark = f.status === 'done' ? '✓' : f.status === 'deferred' ? '–' : isActive ? '●' : '○';
        const cls = ['sx-focus-item'];
        if (f.status === 'done') cls.push('is-done');
        else if (f.status === 'deferred') cls.push('is-deferred');
        else if (isActive) cls.push('is-active');
        return `<li class="${cls.join(' ')}">
          <span class="sx-focus-mark" aria-hidden="true">${mark}</span>
          <span class="sx-focus-body">
            <span class="sx-focus-name">${esc(f.name)}</span>
            ${dotsHtml(f.level)}
          </span>
          ${f.isReview ? '<span class="sx-badge">review</span>' : ''}
        </li>`;
      })
      .join('');
  }

  // -------------------------------------------------------------------- cards
  function showIntro(sessionState) {
    const item = sessionState.item;
    hideCards();
    el('sx-loading').hidden = true;
    el('sx-intro').hidden = false;
    el('sx-intro-kicker').textContent = item.isReview ? 'Review' : 'New skill';
    el('sx-intro-skill').textContent = item.name;
    el('sx-intro-text').textContent =
      item.intro || 'Take this one slowly. You will get a few questions on it and a hint whenever you want one.';
    if (state.visualReady && window.Mascot) {
      Mascot.mood('talking');
      Promise.resolve(Mascot.pointAt('#sx-intro-text')).catch(() => {});
    }

    const btn = el('sx-intro-start');
    btn.onclick = () => {
      state.introSeen.add(Number(item.id));
      if (sessionState.question) showQuestion(sessionState.question, item);
      else refresh();
    };
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
  }

  function setOptionsEnabled(enabled) {
    el('sx-options')
      .querySelectorAll('button')
      .forEach((b) => {
        b.disabled = !enabled;
      });
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

    renderOptions(question.options);
    setOptionsEnabled(true);

    const feedback = el('sx-feedback');
    feedback.hidden = true;
    feedback.innerHTML = '';

    const hintbox = el('sx-hintbox');
    hintbox.hidden = true;
    hintbox.textContent = '';

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
      state.busy = false;
      setOptionsEnabled(true);
      if (picked) picked.classList.remove('is-picked');
      showError(err.message);
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
        if (Number(f.skillId) !== Number(result.item && result.item.skillId)) return f;
        const next = Object.assign({}, f, { level: result.mastery ? result.mastery.levelAfter : f.level });
        if (doneId && Number(f.id) === doneId) next.status = 'done';
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

    const fresh = Number(sessionState.item.attempts) === 0 && !state.introSeen.has(Number(sessionState.item.id));
    if (fresh && sessionState.item.intro) showIntro(sessionState);
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
      box.textContent = out.hint || 'No hint for this one — trust your first step.';
      box.hidden = false;
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

    // One optional model sentence; the template summary above stands without it.
    const stale = document.querySelector('.sx-ai-line');
    if (stale) stale.remove();
    if (summary && summary.aiLine) {
      const line = document.createElement('p');
      line.className = 'sx-line sx-ai-line';
      line.textContent = summary.aiLine;
      el('sx-summary-text').insertAdjacentElement('afterend', line);
    }

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

      if (window.Celebrate && out.done > 0) {
        const session = (out.state && out.state.session) || {};
        const reward = out.reward || {};
        Celebrate.goal({
          xp: Number(session.xpAwarded || reward.xp || 0),
          gems: Number(session.gemsAwarded || reward.gems || 0),
          onChoose: (choice) => {
            if (choice === 'keep') window.location.href = 'session.html?minutes=10';
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

  /** Play a validated script, saying the line first so the ink lands on speech. */
  function playAI(payload) {
    if (!window.Annotate || !Array.isArray(payload.script)) return false;
    const steps = [];
    if (payload.say) steps.push({ at: 0, do: 'say', text: payload.say });
    let lastAt = 0;
    for (const step of payload.script) {
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
    ink(() => Annotate.curve({ anchor: '#sx-feedback [data-annotate="why"]', ms: 400 }));
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
      // Second miss: ask for the reteach script, keep the rules if it fails.
      Promise.resolve(requestAI('reteach', { distractor: chosenKey, attempts }))
        .then((payload) => {
          if (payload && playAI(payload)) return;
          ruleReteach(optionEl);
        })
        .catch(() => ruleReteach(optionEl));
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

  /** Board mode: the worked steps, plus the item's diagram preset when it has one. */
  function drawBoard() {
    if (!window.Board) return;
    const steps = (state.lastSolution && state.lastSolution.steps) || [];
    const visual = state.question && state.question.visual;
    const spec = visual && typeof visual === 'object' ? visual : {};
    if (window.Mascot) Mascot.mood('writing');
    Board.open({
      title: state.item ? state.item.name : 'On the board',
      steps,
      preset: spec.preset,
      params: spec.params
    })
      .then(() => {
        if (state.visualReady && window.Mascot) Mascot.pointAt('#board').catch(() => {});
      })
      .catch(() => {});
  }

  function initVisual() {
    if (state.visualReady) return;
    state.visualReady = true;
    if (window.Annotate) Annotate.attach(el('sx-stage'));
    if (window.Mascot) {
      Promise.resolve(Mascot.attach('#sx-mascot-host'))
        .then(() => {
          Mascot.park();
          Mascot.mood('idle');
        })
        .catch(() => {});
    }
  }

  // -------------------------------------------------------------------- boot
  async function boot() {
    try {
      const body = { minutes: requestedMinutes };
      if (requestedTrack) body.track = requestedTrack;
      const sessionState = await api('/api/session/start', body);
      applyState(sessionState);
      initVisual();
    } catch (err) {
      el('sx-loading').hidden = true;
      showError(err.message || 'Could not start a session.');
    }
  }

  function wire() {
    el('sx-hint-btn').addEventListener('click', askHint);
    el('sx-skip-btn').addEventListener('click', skip);
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
