/**
 * Global section progress rings, XP awards, and completion celebrations.
 */
(function () {
  let pageIndex = 0;
  let pageTotal = 1;
  let courseId = null;
  let unitId = null;
  let awardedPages = new Set();

  function apiBase() {
    return typeof window.API_BASE_URL === 'string' ? window.API_BASE_URL : '';
  }

  function token() {
    return localStorage.getItem('token') || (typeof window.authToken === 'string' ? window.authToken : '');
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

  function playDing() {
    try {
      const Ctx = window.AudioContext || window.webkitAudioContext;
      if (!Ctx) return;
      const ctx = new Ctx();
      const o = ctx.createOscillator();
      const g = ctx.createGain();
      o.type = 'sine';
      o.frequency.value = 880;
      g.gain.value = 0.06;
      o.connect(g);
      g.connect(ctx.destination);
      o.start();
      g.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.28);
      o.stop(ctx.currentTime + 0.3);
      setTimeout(() => ctx.close(), 400);
    } catch (_) {
      /* ignore */
    }
  }

  function celebrate() {
    if (window.LearnerGamification && typeof window.LearnerGamification.celebrateCorrect === 'function') {
      window.LearnerGamification.celebrateCorrect();
    }
    playDing();
  }

  function ensureRing() {
    let el = document.getElementById('vl-progress-ring');
    if (el) return el;
    const viewer = document.getElementById('course-viewer-section');
    const header = viewer && viewer.querySelector('.viewer-header');
    el = document.createElement('div');
    el.id = 'vl-progress-ring';
    el.className = 'vl-progress-ring-wrap';
    el.innerHTML = `<svg viewBox="0 0 36 36" class="vl-progress-ring" aria-label="Section progress">
      <path class="vl-ring-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
      <path class="vl-ring-fg" stroke-dasharray="0, 100" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
      <text x="18" y="21" class="vl-ring-text">0%</text>
    </svg>`;
    if (header) header.appendChild(el);
    else if (viewer) viewer.prepend(el);
    return el;
  }

  function setRing(pct) {
    const wrap = ensureRing();
    wrap.hidden = false;
    const p = Math.max(0, Math.min(100, Math.round(pct)));
    const fg = wrap.querySelector('.vl-ring-fg');
    const text = wrap.querySelector('.vl-ring-text');
    if (fg) fg.setAttribute('stroke-dasharray', `${p}, 100`);
    if (text) text.textContent = `${p}%`;
  }

  function applyRewards(data) {
    if (!data) return;
    if (window.LearnerGamification && typeof window.LearnerGamification.applyAward === 'function') {
      window.LearnerGamification.applyAward(data);
      return;
    }
    if (data.xpAwarded > 0 && window.LearnerGamification?.showXpToast) {
      window.LearnerGamification.showXpToast(data.xpAwarded);
    }
    if (data.gemsAwarded > 0 && window.LearnerGamification?.showGemToast) {
      window.LearnerGamification.showGemToast(data.gemsAwarded);
    }
    if ((data.xpAwarded > 0 || data.gemsAwarded > 0) && data.newBadges && data.newBadges.length) {
      data.newBadges.forEach((b) => {
        if (window.LearnerGamification?.showBadgeToast) window.LearnerGamification.showBadgeToast(b);
      });
    }
  }

  async function awardKind(kind, extra) {
    try {
      const data = await api('/api/learner/award-xp', {
        method: 'POST',
        body: JSON.stringify(Object.assign({ kind }, extra || {}))
      });
      if (data.success && data.data) applyRewards(data.data);
      return data.data;
    } catch (_) {
      return null;
    }
  }

  async function onPageShown(index, total, opts) {
    pageIndex = index;
    pageTotal = Math.max(1, total || 1);
    courseId = (opts && opts.courseId) || window.currentViewingCourseId || courseId;
    if (opts && 'unitId' in opts) unitId = opts.unitId;
    const pct = ((index + 1) / pageTotal) * 100;
    setRing(pct);

    try {
      if (courseId != null) localStorage.setItem(`vl:coursePage:${courseId}`, String(index));
    } catch (_) { /* ignore */ }

    const key = `${courseId}:${index}`;
    if (courseId != null && !awardedPages.has(key)) {
      awardedPages.add(key);
      const result = await awardKind('page', { courseId, pageIndex: index });
      if (result && result.xpAwarded > 0) celebrate();
    }

    if (unitId && typeof window.updateUnitProgress === 'function' && Math.round(pct) > 0) {
      window.updateUnitProgress(unitId, Math.round(pct));
    } else if (!unitId && courseId && Math.round(pct) >= 0) {
      api(`/api/courses/${courseId}/progress`, {
        method: 'PUT',
        body: JSON.stringify({
          progress_percentage: Math.round(pct),
          last_page_index: index
        })
      }).catch(() => {});
    }
  }

  async function onUnitQuizzesProgress() {
    const qs = window.courseQuestions || [];
    if (!qs.length) return;
    const answered = qs.filter((q) => q._answeredCorrect).length;
    const pct = Math.round((answered / qs.length) * 100);
    if (pct <= 0) return;
    setRing(pct);
    if (unitId && typeof window.updateUnitProgress === 'function') {
      window.updateUnitProgress(unitId, pct);
    } else if (courseId) {
      api(`/api/courses/${courseId}/progress`, {
        method: 'PUT',
        body: JSON.stringify({ progress_percentage: pct })
      }).catch(() => {});
    }
  }

  async function awardInteractive(kind, blockId) {
    return awardKind(kind, {
      courseId: window.currentViewingCourseId || courseId,
      blockId
    });
  }

  window.CourseProgress = {
    onPageShown,
    onUnitQuizzesProgress,
    awardInteractive,
    awardKind,
    applyRewards,
    celebrate,
    setRing,
    setContext(ctx) {
      if (ctx && 'courseId' in ctx) courseId = ctx.courseId;
      if (ctx && 'unitId' in ctx) unitId = ctx.unitId;
    }
  };
})();
