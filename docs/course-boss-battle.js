/**
 * Boss Battle + Hearts for unit finales.
 * Concept drills stay open; finale questions are stage-gated.
 */
(function () {
  const STAGE_NEED = { easy: 10, medium: 8 };
  let state = {
    courseId: null,
    hearts: 3,
    heartsEnabled: false,
    bossEnabled: false,
    unlocked: { easy: true, medium: false, hard: false },
    questions: []
  };

  function apiBase() {
    return typeof window.API_BASE_URL === 'string' ? window.API_BASE_URL : '';
  }

  function token() {
    return localStorage.getItem('token') || (typeof window.authToken === 'string' ? window.authToken : '');
  }

  function escapeHtml(str) {
    return String(str || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  async function api(path, opts) {
    const res = await fetch(`${apiBase()}${path}`, {
      credentials: 'include',
      headers: Object.assign(
        { 'Content-Type': 'application/json', Authorization: `Bearer ${token()}` },
        (opts && opts.headers) || {}
      ),
      ...opts
    });
    return res.json().catch(() => ({}));
  }

  function parseSettings(course, questionCount, parentCourse) {
    let settings = {};
    const raw = course && (course.gamification || course.gamification_json);
    if (raw) {
      try {
        settings = typeof raw === 'string' ? JSON.parse(raw) : raw;
      } catch (_) {
        settings = {};
      }
    }
    const parent = parentCourse || (typeof window.currentMasterCourse === 'object' ? window.currentMasterCourse : null);
    const parentRaw = parent && parent !== course && (parent.gamification || parent.gamification_json);
    if (parentRaw && !settings.hearts && !settings.bossBattle) {
      try {
        const p = typeof parentRaw === 'string' ? JSON.parse(parentRaw) : parentRaw;
        if (p.hearts) settings.hearts = true;
        if (p.bossBattle) settings.bossBattle = true;
      } catch (_) {
        /* ignore */
      }
    }
    if ((raw == null || raw === '') && questionCount >= 50) {
      settings.bossBattle = settings.bossBattle !== false;
      settings.hearts = settings.hearts !== false;
      settings.inferred = true;
    }
    return settings;
  }

  function isFinale(q) {
    return q && q.finale !== false && q.concept_drill !== true && q._conceptDrill !== true;
  }

  function difficultyOf(q) {
    return (q && q.difficulty) || 'easy';
  }

  function countCorrect(diff) {
    const qs = (window.courseQuestions || state.questions || []).filter(
      (q) => isFinale(q) && difficultyOf(q) === diff
    );
    return qs.filter((q) => q._answeredCorrect).length;
  }

  function recomputeUnlocks() {
    const easyOk = countCorrect('easy') >= STAGE_NEED.easy;
    const medOk = countCorrect('medium') >= STAGE_NEED.medium;
    state.unlocked.medium = easyOk;
    state.unlocked.hard = easyOk && medOk;
  }

  function stageAllowed(diff) {
    if (!state.bossEnabled) return true;
    if (diff === 'easy') return true;
    if (diff === 'medium') return state.unlocked.medium;
    return state.unlocked.hard;
  }

  function ensureHud() {
    let hud = document.getElementById('vl-boss-hud');
    if (hud) return hud;
    hud = document.createElement('div');
    hud.id = 'vl-boss-hud';
    hud.className = 'vl-boss-hud';
    const content =
      document.getElementById('course-viewer-content') || document.querySelector('.viewer-content');
    const viewer = document.getElementById('course-viewer-section');
    if (content && content.parentNode) {
      content.parentNode.insertBefore(hud, content);
    } else if (viewer) {
      viewer.prepend(hud);
    } else {
      document.body.appendChild(hud);
    }
    return hud;
  }

  function renderHud() {
    if (!state.bossEnabled && !state.heartsEnabled) {
      const el = document.getElementById('vl-boss-hud');
      if (el) el.hidden = true;
      return;
    }
    const hud = ensureHud();
    hud.hidden = false;
    const hearts = state.heartsEnabled
      ? `<span class="vl-hearts" aria-label="${state.hearts} hearts left">${'❤'.repeat(
          Math.max(0, state.hearts)
        )}${'♡'.repeat(Math.max(0, 3 - state.hearts))}</span>
         <span class="vl-hearts-label">${state.hearts} HP</span>`
      : '';
    let stageLabel = '';
    let progress = '';
    if (state.bossEnabled) {
      if (state.unlocked.hard) stageLabel = 'Final Boss — Hard + Stretch';
      else if (state.unlocked.medium) stageLabel = 'Stage 2 — Medium';
      else stageLabel = 'Stage 1 — Easy (solve 10 to unlock)';
      progress = `<span class="vl-boss-progress">Easy ${countCorrect('easy')}/${STAGE_NEED.easy} · Medium ${countCorrect(
        'medium'
      )}/${STAGE_NEED.medium}</span>`;
    } else if (state.heartsEnabled) {
      stageLabel = 'Hearts mode — miss 3 times to get a hint';
    }
    hud.innerHTML = `${hearts}<span class="vl-boss-stage">${stageLabel}</span>${progress}`;
  }

  function flashHeartsToast(msg) {
    document.querySelectorAll('.vl-heart-toast').forEach((el) => el.remove());
    const toast = document.createElement('div');
    toast.className = 'vl-heart-toast';
    toast.textContent = msg;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 2800);
  }

  function applyGates(root) {
    const host =
      root ||
      document.getElementById('course-content-display') ||
      document.getElementById('course-viewer-content');
    if (!host || !state.bossEnabled) {
      renderHud();
      return;
    }
    recomputeUnlocks();
    host.querySelectorAll('.quiz-question[data-question-id], .quiz-question-placeholder[data-question-id]').forEach(
      (el) => {
        const id = parseInt(el.dataset.questionId, 10);
        const q = (window.courseQuestions || []).find((x) => Number(x.id) === id);
        if (!q || !isFinale(q)) return;
        const diff = difficultyOf(q);
        const allowed = stageAllowed(diff);
        el.classList.toggle('vl-boss-locked', !allowed);
        let lock = el.querySelector('.vl-boss-lock-msg');
        if (!allowed) {
          if (!lock) {
            lock = document.createElement('div');
            lock.className = 'vl-boss-lock-msg';
            el.appendChild(lock);
          }
          lock.textContent =
            diff === 'medium'
              ? 'Locked — solve 10 Easy finale problems to unlock Stage 2.'
              : 'Locked — defeat Stage 2 (8 Medium) to face the Final Boss.';
          el.querySelectorAll('input, button.quiz-submit-btn').forEach((n) => {
            n.disabled = true;
          });
        } else if (lock) {
          lock.remove();
        }
        let badge = el.querySelector('.vl-diff-badge');
        if (!badge) {
          badge = document.createElement('span');
          badge.className = 'vl-diff-badge';
          const header = el.querySelector('.quiz-question-header') || el;
          header.appendChild(badge);
        }
        badge.dataset.diff = diff;
        badge.textContent = diff === 'stretch' ? 'SAT / Honors Stretch' : diff;
      }
    );
    renderHud();
  }

  async function persist() {
    if (!state.courseId) return;
    try {
      await api(`/api/learner/boss-state/${state.courseId}`, {
        method: 'POST',
        body: JSON.stringify({
          hearts: state.hearts,
          unlocked: state.unlocked
        })
      });
    } catch (_) {
      /* ignore */
    }
  }

  async function init(course, questions, extras) {
    const qs = questions || window.courseQuestions || [];
    const parent = (extras && extras.parent) || null;
    const settings = parseSettings(course, qs.length, parent);
    const nextId = course && (course.id || course.child_course_id);
    const sameCourse = state.courseId != null && String(state.courseId) === String(nextId);
    const keepHearts = sameCourse ? state.hearts : 3;
    const quizCount = qs.length;

    state.courseId = nextId;
    state.questions = qs;
    // Stage gates only make sense on a full finale (10+ questions)
    state.bossEnabled = !!settings.bossBattle && quizCount >= 10;
    state.heartsEnabled = !!settings.hearts;
    state.hearts = keepHearts;
    if (!sameCourse) {
      state.unlocked = { easy: true, medium: false, hard: false };
    }

    if (state.courseId && (state.bossEnabled || state.heartsEnabled)) {
      try {
        const data = await api(`/api/learner/boss-state/${state.courseId}`);
        if (data.success && data.data) {
          if (!sameCourse && typeof data.data.hearts === 'number') state.hearts = data.data.hearts;
          if (data.data.unlocked) state.unlocked = Object.assign(state.unlocked, data.data.unlocked);
        }
      } catch (_) {
        /* ignore */
      }
    }

    qs.forEach((q) => {
      if (q.already_correct || q._answeredCorrect) q._answeredCorrect = true;
    });
    recomputeUnlocks();
    applyGates();
    renderHud();
  }

  function showHint(explanation) {
    const existing = document.getElementById('vl-heart-hint');
    if (existing) existing.remove();
    const modal = document.createElement('div');
    modal.id = 'vl-heart-hint';
    modal.className = 'vl-heart-hint-overlay';
    modal.setAttribute('role', 'dialog');
    modal.setAttribute('aria-modal', 'true');
    const teaser = String(explanation || 'Re-read the last example, then try a simpler number first.').slice(0, 240);
    modal.innerHTML = `<div class="vl-heart-hint-card">
      <h2>Out of hearts</h2>
      <p>You missed 3 questions. Here’s a hint — then continue with 1 heart restored.</p>
      <p class="vl-hint-body">${escapeHtml(teaser)}${teaser.length >= 240 ? '…' : ''}</p>
      <button type="button" id="vl-heart-ok" class="vl-heart-ok-btn">Got it — restore 1 HP</button>
    </div>`;
    document.body.appendChild(modal);
    const ok = modal.querySelector('#vl-heart-ok');
    if (ok) {
      ok.addEventListener('click', () => {
        state.hearts = 1;
        modal.remove();
        renderHud();
        persist();
      });
      ok.focus();
    }
  }

  function onAnswer(questionId, isCorrect, extra) {
    const q = (window.courseQuestions || []).find((x) => Number(x.id) === Number(questionId));
    if (isCorrect && q) q._answeredCorrect = true;

    if (!isCorrect && state.heartsEnabled) {
      const now = Date.now();
      if (state._lastWrongId === Number(questionId) && now - (state._lastWrongAt || 0) < 1000) {
        recomputeUnlocks();
        applyGates();
        return;
      }
      state._lastWrongId = Number(questionId);
      state._lastWrongAt = now;
      state.hearts = Math.max(0, state.hearts - 1);
      renderHud();
      if (state.hearts <= 0) {
        showHint((extra && extra.explanation) || (q && q.explanation));
      } else {
        flashHeartsToast(`${state.hearts} heart${state.hearts === 1 ? '' : 's'} left`);
      }
    }

    recomputeUnlocks();
    applyGates();
    persist();
  }

  window.CourseBossBattle = {
    init,
    applyGates,
    onAnswer,
    parseSettings,
    getState: () => state
  };
})();
