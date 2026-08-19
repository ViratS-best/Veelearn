/**
 * Global course progress rings, XP awards, and resume position.
 */
(function () {
  let pageIndex = 0;
  let pageTotal = 1;
  let courseId = null;
  let unitId = null;
  let awardedPages = new Set();
  let lastContentScrollY = 0;
  let scrollTimer = null;
  let resumeMasterId = null;
  let resumePageIndex = 0;

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

  function masterOverallProgress(units) {
    const list = units || window.courseUnits || [];
    if (!list.length) return 0;
    const sum = list.reduce((s, u) => {
      if (u.completed) return s + 100;
      const p = Number(u.progress_percentage);
      return s + (Number.isFinite(p) ? Math.max(0, Math.min(100, p)) : 0);
    }, 0);
    return Math.round(sum / list.length);
  }

  function currentOverallPct() {
    const units = window.courseUnits;
    if (Array.isArray(units) && units.length && window.currentMasterCourse) {
      return masterOverallProgress(units);
    }
    const qs = window.courseQuestions || [];
    const quiz = qs.length
      ? Math.round((qs.filter((q) => q._answeredCorrect).length / qs.length) * 100)
      : 0;
    const page = pageTotal > 0 ? ((pageIndex + 1) / pageTotal) * 100 : 0;
    return Math.round(Math.max(quiz, page));
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
    el.innerHTML = `<svg viewBox="0 0 36 36" class="vl-progress-ring" aria-label="Course progress">
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

  function syncOverallRing() {
    setRing(currentOverallPct());
  }

  function refreshEnrolledDisplays() {
    if (typeof window.loadEnrolledCourses === 'function') {
      window.loadEnrolledCourses();
    }
    if (window.LearnerGamification?.fetchEnrollments) {
      window.LearnerGamification.fetchEnrollments({ force: true }).then((list) => {
        if (window.LearnerGamification.renderEnrolled) window.LearnerGamification.renderEnrolled();
        else if (Array.isArray(list) && typeof window.LearnerGamification.paintEnrolledList === 'function') {
          window.LearnerGamification.paintEnrolledList(list);
        }
      }).catch(() => {});
    }
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

  function resumeStorageKey(id) {
    return `vl:resume:${id}`;
  }

  function contentScrollY() {
    const y = window.scrollY || document.documentElement.scrollTop || 0;
    const content = document.getElementById('course-viewer-content');
    if (!content) return y;
    const top = content.getBoundingClientRect().top + y;
    const bottom = top + content.offsetHeight;
    const cap = Math.max(0, bottom - window.innerHeight + 48);
    return Math.max(0, Math.min(y, cap));
  }

  function persistLocal() {
    const id = resumeMasterId || courseId;
    if (id == null) return;
    const payload = {
      courseId,
      masterId: resumeMasterId,
      unitId,
      pageIndex: resumePageIndex,
      scrollY: lastContentScrollY
    };
    try {
      localStorage.setItem(resumeStorageKey(id), JSON.stringify(payload));
      if (resumeMasterId && courseId && resumeMasterId !== courseId) {
        localStorage.setItem(resumeStorageKey(courseId), JSON.stringify(payload));
      }
    } catch (_) { /* ignore */ }
  }

  function readLocal(id) {
    if (id == null) return null;
    try {
      const raw = localStorage.getItem(resumeStorageKey(id));
      if (!raw) return null;
      return JSON.parse(raw);
    } catch (_) {
      return null;
    }
  }

  function captureScroll() {
    lastContentScrollY = contentScrollY();
    persistLocal();
  }

  function onScroll() {
    lastContentScrollY = contentScrollY();
    if (scrollTimer) return;
    scrollTimer = setTimeout(() => {
      scrollTimer = null;
      persistLocal();
      flushServer({ keepalive: true });
    }, 2000);
  }

  function bindScroll() {
    window.removeEventListener('scroll', onScroll);
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  function unbindScroll() {
    window.removeEventListener('scroll', onScroll);
    if (scrollTimer) {
      clearTimeout(scrollTimer);
      scrollTimer = null;
    }
  }

  function flushServer(opts) {
    captureScroll();
    const targetId = resumeMasterId || courseId;
    if (targetId == null) return;
    const body = {
      progress_percentage: currentOverallPct(),
      last_scroll_y: lastContentScrollY
    };
    if (resumePageIndex != null) body.last_page_index = resumePageIndex;
    if (unitId) body.last_unit_id = unitId;
    const headers = {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token()}`
    };
    const init = {
      method: 'PUT',
      credentials: 'include',
      keepalive: !!(opts && opts.keepalive),
      headers,
      body: JSON.stringify(body)
    };
    try {
      fetch(`${apiBase()}/api/courses/${targetId}/progress`, init).catch(() => {});
    } catch (_) { /* ignore */ }
  }

  async function loadResume(id) {
    const local = readLocal(id) || {};
    let server = {};
    try {
      const json = await api(`/api/courses/${id}/progress`);
      if (json.success && json.data) server = json.data;
    } catch (_) { /* ignore */ }
    return {
      unitId: local.unitId || server.last_unit_id || null,
      pageIndex: Math.max(Number(local.pageIndex) || 0, Number(server.last_page_index) || 0),
      scrollY: Math.max(Number(local.scrollY) || 0, Number(server.last_scroll_y) || 0)
    };
  }

  function restoreScroll(y) {
    const target = Math.max(0, Number(y) || 0);
    if (target <= 0) return;
    const apply = () => window.scrollTo(0, target);
    apply();
    setTimeout(apply, 150);
    setTimeout(apply, 400);
  }

  function setContext(ctx) {
    if (ctx && 'courseId' in ctx) courseId = ctx.courseId;
    if (ctx && 'unitId' in ctx) unitId = ctx.unitId;
    if (ctx && 'masterId' in ctx) resumeMasterId = ctx.masterId;
    if (ctx && 'pageIndex' in ctx) resumePageIndex = ctx.pageIndex;
  }

  function startSession(ctx) {
    setContext(ctx || {});
    lastContentScrollY = 0;
    bindScroll();
    persistLocal();
  }

  function endSession() {
    flushServer({ keepalive: false });
    unbindScroll();
    courseId = null;
    unitId = null;
    resumeMasterId = null;
  }

  async function onPageShown(index, total, opts) {
    pageIndex = index;
    pageTotal = Math.max(1, total || 1);
    courseId = (opts && opts.courseId) || window.currentViewingCourseId || courseId;
    if (opts && 'unitId' in opts) unitId = opts.unitId;
    resumePageIndex = index;
    syncOverallRing();

    try {
      if (courseId != null) localStorage.setItem(`vl:coursePage:${courseId}`, String(index));
    } catch (_) { /* ignore */ }
    persistLocal();

    const key = `${courseId}:${index}`;
    if (courseId != null && !awardedPages.has(key)) {
      awardedPages.add(key);
      const result = await awardKind('page', { courseId, pageIndex: index });
      if (result && result.xpAwarded > 0) celebrate();
    }

    const pct = Math.round(((index + 1) / pageTotal) * 100);
    if (unitId && typeof window.updateUnitProgress === 'function' && pct > 0) {
      window.updateUnitProgress(unitId, pct);
    } else if (!unitId && courseId && pct >= 0) {
      api(`/api/courses/${courseId}/progress`, {
        method: 'PUT',
        body: JSON.stringify({
          progress_percentage: pct,
          last_page_index: index,
          last_scroll_y: lastContentScrollY
        })
      }).catch(() => {});
    }
  }

  async function onUnitQuizzesProgress() {
    const qs = window.courseQuestions || [];
    if (!qs.length) {
      syncOverallRing();
      return;
    }
    const answered = qs.filter((q) => q._answeredCorrect).length;
    const pct = Math.round((answered / qs.length) * 100);
    if (pct > 0 && unitId && typeof window.updateUnitProgress === 'function') {
      const units = window.courseUnits;
      if (Array.isArray(units)) {
        const u = units.find((x) => String(x.unit_id) === String(unitId));
        if (u) u.progress_percentage = Math.max(Number(u.progress_percentage) || 0, pct);
      }
      window.updateUnitProgress(unitId, pct);
    } else if (pct > 0 && courseId) {
      api(`/api/courses/${courseId}/progress`, {
        method: 'PUT',
        body: JSON.stringify({ progress_percentage: pct, last_scroll_y: lastContentScrollY })
      }).catch(() => {});
    }
    syncOverallRing();
    refreshEnrolledDisplays();
  }

  async function awardInteractive(kind, blockId) {
    return awardKind(kind, {
      courseId: window.currentViewingCourseId || courseId,
      blockId
    });
  }

  window.addEventListener('pagehide', () => flushServer({ keepalive: true }));
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'hidden') flushServer({ keepalive: true });
  });

  window.CourseProgress = {
    onPageShown,
    onUnitQuizzesProgress,
    awardInteractive,
    awardKind,
    applyRewards,
    celebrate,
    setRing,
    syncOverallRing,
    masterOverallProgress,
    refreshEnrolledDisplays,
    setContext,
    startSession,
    endSession,
    loadResume,
    restoreScroll,
    flush: flushServer
  };
})();
