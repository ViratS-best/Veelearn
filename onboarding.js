/**
 * First-login welcome gift + one-time dashboard tour.
 *
 * Shown once per account: the gift popup asks the learner to claim the Freebuff
 * offer, then a spotlight tour points at the parts of the dashboard they need to
 * get started. Finishing (or skipping) the tour records it on the server, and the
 * only thing that stays reachable afterwards is the Freebuff link in Settings.
 */
(function () {
  const GIFT_URL =
    'https://freebuff.com/?ref=ref-2e1c9b1d-8a0e-40b5-9a27-729d7501336d&via=rewards_link';
  const GIFT_LABEL = 'FREEBUFF';
  const DONE_KEY = 'veelearnOnboardingDone';

  function apiBase() {
    return typeof window.API_BASE_URL === 'string' ? window.API_BASE_URL : '';
  }

  function token() {
    return localStorage.getItem('token') || (typeof window.authToken === 'string' ? window.authToken : '');
  }

  async function api(path, opts = {}) {
    const headers = Object.assign(
      { 'Content-Type': 'application/json', Authorization: `Bearer ${token()}` },
      opts.headers || {}
    );
    const res = await fetch(`${apiBase()}${path}`, { ...opts, headers, credentials: 'include' });
    return res.json().catch(() => ({}));
  }

  const TOUR_STEPS = [
    {
      target: '#ls-start-session',
      fallback: '.ls-session-cta',
      title: 'Start here: a short session',
      body: 'A session gives you a few skills and one question at a time. Pick how long you have and Vee teaches the lesson before it asks you anything.'
    },
    {
      target: '#ls-ai-input',
      fallback: '.ls-ai-box',
      title: 'Ask Vee anything',
      body: 'Type a question or say what you want to learn. Vee answers, and it can suggest a course that matches your grade and goal.'
    },
    {
      target: '#ls-new-outline',
      fallback: '.ls-outline-cta',
      title: 'Build your own course',
      body: 'Turn your notes or homework into an outline of skills and questions. The AI teaches the map in the order you make it.'
    },
    {
      target: '#learner-shell [data-ls-nav="sessions"]',
      fallback: null,
      title: 'Pick up where you left off',
      body: 'Every session is saved here with its summary, so you can resume one or start a fresh practice run.'
    },
    {
      target: '#learner-shell [data-ls-nav="achievements"]',
      fallback: '#learner-shell .ls-gems-pill',
      title: 'Earn gems and keep a streak',
      body: 'Correct answers earn gems and XP. Check in daily to grow your streak, and spend gems in the Gem Store on themes and avatar gear.'
    },
    {
      target: '#learner-shell [data-ls-nav="settings"]',
      fallback: null,
      title: 'Your gift lives in Settings',
      body: 'That free coding offer is always available under Settings, so you can claim it whenever you are ready. Enjoy learning!'
    }
  ];

  let tour = null;
  let activeUserId = 'guest';

  function doneKey(userId) {
    return `${DONE_KEY}:${userId == null ? 'guest' : userId}`;
  }

  function hasSeen(userId) {
    try {
      return localStorage.getItem(doneKey(userId)) === '1';
    } catch (_) {
      return false;
    }
  }

  function rememberSeen(userId) {
    try {
      localStorage.setItem(doneKey(userId), '1');
    } catch (_) {
      /* storage may be blocked; the server flag is the real record */
    }
  }

  async function markDone() {
    rememberSeen(activeUserId);
    try {
      await api('/api/learner/onboarding/complete', { method: 'POST', body: '{}' });
    } catch (_) {
      /* offline: the local flag still stops it nagging */
    }
  }

  // ------------------------------------------------------------------ gift
  function showGift() {
    if (document.getElementById('ls-gift-backdrop')) return;

    const backdrop = document.createElement('div');
    backdrop.className = 'ls-gift-backdrop';
    backdrop.id = 'ls-gift-backdrop';
    backdrop.innerHTML = `
      <div class="ls-gift-card" role="dialog" aria-modal="true" aria-labelledby="ls-gift-title">
        <button type="button" class="ls-gift-close" id="ls-gift-close" aria-label="Close and take the tour">×</button>
        <div class="ls-gift-badge" aria-hidden="true">🎁</div>
        <h2 class="ls-gift-title" id="ls-gift-title">Thank you for signing up!</h2>
        <p class="ls-gift-body">
          As a gift, get unlimited free coding forever with models as good as
          <strong>FABLE 5</strong>! Sign up here:
          <a class="ls-gift-link" id="ls-gift-link" href="${GIFT_URL}" target="_blank" rel="noopener noreferrer">${GIFT_LABEL}</a>
        </p>
        <p class="ls-gift-note">Click the link to claim it, or close this to take a quick tour of your dashboard.</p>
        <div class="ls-gift-actions">
          <a class="ls-gift-cta" href="${GIFT_URL}" target="_blank" rel="noopener noreferrer" id="ls-gift-cta">Claim my gift</a>
          <button type="button" class="ls-gift-skip" id="ls-gift-tour">Show me around</button>
        </div>
      </div>`;
    document.body.appendChild(backdrop);

    const dismiss = () => {
      backdrop.remove();
      startTour();
    };

    // The gift is claimed first, then the tour runs in this tab so the learner
    // comes back to a dashboard they know how to use.
    backdrop.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => setTimeout(dismiss, 250));
    });
    document.getElementById('ls-gift-close')?.addEventListener('click', dismiss);
    document.getElementById('ls-gift-tour')?.addEventListener('click', dismiss);
    backdrop.addEventListener('click', (e) => {
      if (e.target === backdrop) dismiss();
    });
    document.getElementById('ls-gift-link')?.focus({ preventScroll: true });
  }

  // ------------------------------------------------------------------ tour
  function currentStepTarget(step) {
    const direct = step.target ? document.querySelector(step.target) : null;
    if (direct) return direct;
    return step.fallback ? document.querySelector(step.fallback) : null;
  }

  function visibleRect(el) {
    if (!el) return null;
    const rect = el.getBoundingClientRect();
    if (rect.width < 8 || rect.height < 8) return null;
    return rect;
  }

  function buildTour() {
    const root = document.createElement('div');
    root.className = 'ls-tour';
    root.id = 'ls-tour';
    root.innerHTML = `
      <div class="ls-tour-spot" id="ls-tour-spot" aria-hidden="true"></div>
      <div class="ls-tour-card" id="ls-tour-card" role="dialog" aria-modal="true" aria-labelledby="ls-tour-title">
        <p class="ls-tour-count" id="ls-tour-count"></p>
        <h3 class="ls-tour-title" id="ls-tour-title"></h3>
        <p class="ls-tour-body" id="ls-tour-body"></p>
        <div class="ls-tour-actions">
          <button type="button" class="ls-tour-skip" id="ls-tour-skip">Skip tour</button>
          <span class="ls-tour-gap"></span>
          <button type="button" class="ls-tour-back" id="ls-tour-back">Back</button>
          <button type="button" class="ls-tour-next" id="ls-tour-next">Next</button>
        </div>
      </div>`;
    document.body.appendChild(root);

    document.getElementById('ls-tour-next')?.addEventListener('click', next);
    document.getElementById('ls-tour-back')?.addEventListener('click', () => goTo(tour.index - 1));
    document.getElementById('ls-tour-skip')?.addEventListener('click', finish);
    return root;
  }

  function positionStep() {
    if (!tour) return;
    const step = TOUR_STEPS[tour.index];
    if (!step) return finish();

    const el = currentStepTarget(step);
    if (!el) return goTo(tour.index + (tour.direction < 0 ? -1 : 1));

    const rect = visibleRect(el);
    if (!rect) {
      el.scrollIntoView({ block: 'center', behavior: 'smooth' });
      clearTimeout(tour.scrollTimer);
      tour.scrollTimer = setTimeout(positionStep, 280);
      tour.attempts = (tour.attempts || 0) + 1;
      // Give the scroll one chance; a target that stays hidden (collapsed
      // sidebar on a phone) is skipped instead of retried forever.
      if (tour.attempts > 1) return goTo(tour.index + (tour.direction < 0 ? -1 : 1));
      return;
    }
    tour.attempts = 0;

    const pad = 6;
    const spot = document.getElementById('ls-tour-spot');
    const card = document.getElementById('ls-tour-card');
    if (!spot || !card) return;

    spot.style.display = 'block';
    spot.style.top = `${rect.top - pad}px`;
    spot.style.left = `${rect.left - pad}px`;
    spot.style.width = `${rect.width + pad * 2}px`;
    spot.style.height = `${rect.height + pad * 2}px`;

    const gap = 14;
    const cardRect = card.getBoundingClientRect();
    const vw = window.innerWidth;
    const vh = window.innerHeight;
    let top = rect.bottom + gap;
    if (top + cardRect.height > vh - 12) {
      top = rect.top - pad - gap - cardRect.height;
    }
    if (top < 12) top = Math.max(12, vh - cardRect.height - 12);
    let left = rect.left + rect.width / 2 - cardRect.width / 2;
    left = Math.min(Math.max(12, left), Math.max(12, vw - cardRect.width - 12));

    card.style.top = `${top}px`;
    card.style.left = `${left}px`;
  }

  function goTo(index) {
    if (!tour) return;
    if (index < 0) index = 0;
    if (index >= TOUR_STEPS.length) return finish();

    tour.direction = index < tour.index ? -1 : 1;
    tour.index = index;
    tour.attempts = 0;
    const step = TOUR_STEPS[index];
    const count = document.getElementById('ls-tour-count');
    const title = document.getElementById('ls-tour-title');
    const body = document.getElementById('ls-tour-body');
    const nextBtn = document.getElementById('ls-tour-next');
    const backBtn = document.getElementById('ls-tour-back');
    if (count) count.textContent = `Step ${index + 1} of ${TOUR_STEPS.length}`;
    if (title) title.textContent = step.title;
    if (body) body.textContent = step.body;
    if (nextBtn) nextBtn.textContent = index === TOUR_STEPS.length - 1 ? 'Finish' : 'Next';
    if (backBtn) backBtn.style.visibility = index === 0 ? 'hidden' : 'visible';

    positionStep();
    document.getElementById('ls-tour-next')?.focus({ preventScroll: true });
  }

  function next() {
    if (!tour) return;
    goTo(tour.index + 1);
  }

  function finish() {
    if (!tour) return;
    clearTimeout(tour.scrollTimer);
    window.removeEventListener('resize', positionStep);
    window.removeEventListener('scroll', positionStep, true);
    document.removeEventListener('keydown', onKey);
    document.getElementById('ls-tour')?.remove();
    tour = null;
    markDone();
  }

  function onKey(e) {
    if (!tour) return;
    if (e.key === 'Escape') {
      e.preventDefault();
      finish();
    } else if (e.key === 'ArrowRight') {
      e.preventDefault();
      next();
    } else if (e.key === 'ArrowLeft') {
      e.preventDefault();
      goTo(tour.index - 1);
    }
  }

  function startTour() {
    if (tour) return;
    if (!document.body.classList.contains('learner-shell-active')) return;
    buildTour();
    tour = { index: -1, direction: 1, scrollTimer: null };
    window.LearnerShell?.navigate?.('dashboard');
    window.addEventListener('resize', positionStep);
    window.addEventListener('scroll', positionStep, true);
    document.addEventListener('keydown', onKey);
    goTo(0);
  }

  // --------------------------------------------------------------- entry
  async function maybeStart() {
    if (document.getElementById('ls-gift-backdrop') || tour) return;
    if (!document.body.classList.contains('learner-shell-active')) return;
    try {
      const data = await api('/api/learner/onboarding');
      if (!data || !data.success || !data.data) return;
      activeUserId = data.data.id != null ? data.data.id : 'guest';
      if (data.data.done) {
        rememberSeen(activeUserId);
        return;
      }
      if (hasSeen(activeUserId)) return;
      showGift();
    } catch (_) {
      /* no status, no popup — never interrupt a learner on a broken network */
    }
  }

  window.LearnerOnboarding = {
    GIFT_URL,
    maybeStart,
    showGift,
    startTour,
    markDone
  };
})();
