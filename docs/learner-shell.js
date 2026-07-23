/**
 * Khan-style learner shell navigation and layout.
 * Activated for all logged-in roles except superadmin.
 */
(function () {
  const ASSET = 'assets/learner';

  const NAV_ICONS = {
    dashboard: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 10.5L12 4l8 6.5V20a1 1 0 0 1-1 1h-5v-6H10v6H5a1 1 0 0 1-1-1v-9.5z"/></svg>`,
    achievements: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M8 21h8M12 17v4M7 4h10v5a5 5 0 0 1-10 0V4z"/><path d="M7 6H4a3 3 0 0 0 3 3M17 6h3a3 3 0 0 1-3 3"/></svg>`,
    enrolled: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>`,
    create: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 5v14M5 12h14"/></svg>`,
    studio: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="4" width="18" height="14" rx="2"/><path d="M8 21h8M12 18v3"/></svg>`,
    store: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M6 9h12l-1 11H7L6 9z"/><path d="M9 9V7a3 3 0 0 1 6 0v2"/></svg>`,
    settings: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="3"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>`,
    help: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="M9.5 9a2.5 2.5 0 1 1 3.6 2.2c-.7.4-1.1.9-1.1 1.8V14"/><circle cx="12" cy="17" r="0.8" fill="currentColor"/></svg>`,
    feedback: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 10v8l4-3h8a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v4z"/></svg>`
  };

  function esc(s) {
    return String(s ?? '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function ensureShellDom() {
    if (document.getElementById('learner-shell')) return;

    const shell = document.createElement('div');
    shell.id = 'learner-shell';
    shell.setAttribute('data-learner-theme', 'warm');
    shell.innerHTML = `
      <button type="button" class="ls-mobile-toggle" id="ls-mobile-toggle" aria-label="Open menu">☰</button>
      <aside id="learner-sidebar" aria-label="Veelearn navigation">
        <div class="ls-brand">
          <h1 class="ls-brand-name">Veelearn</h1>
          <button type="button" class="ls-sidebar-close" id="ls-sidebar-close" aria-label="Close">×</button>
        </div>
        <div class="ls-gems-pill" title="Your gems">
          <img src="${ASSET}/gem.svg" alt="" />
          <span id="ls-gems-count">0</span>
        </div>
        <nav class="ls-nav" id="ls-nav-top">
          <button type="button" class="ls-nav-btn active" data-ls-nav="dashboard"><span class="ls-nav-icon">${NAV_ICONS.dashboard}</span>Dashboard</button>
          <button type="button" class="ls-nav-btn" data-ls-nav="achievements"><span class="ls-nav-icon">${NAV_ICONS.achievements}</span>Achievements</button>
          <button type="button" class="ls-nav-btn" data-ls-nav="enrolled"><span class="ls-nav-icon">${NAV_ICONS.enrolled}</span>Enrolled Courses</button>
          <div class="ls-nav-flyout" data-flyout="create">
            <button type="button" class="ls-nav-btn" data-ls-nav="create"><span class="ls-nav-icon">${NAV_ICONS.create}</span>Course Creation</button>
            <div class="ls-flyout-panel" aria-label="Your courses">
              <div class="ls-flyout-panel-inner">
                <button type="button" class="ls-flyout-action" data-flyout-new="course">+ New course</button>
                <div class="ls-flyout-list" id="ls-flyout-courses"><div class="ls-flyout-empty">Hover to load…</div></div>
              </div>
            </div>
          </div>
          <div class="ls-nav-flyout" data-flyout="studio">
            <button type="button" class="ls-nav-btn" data-ls-nav="studio"><span class="ls-nav-icon">${NAV_ICONS.studio}</span>Simulator Studio</button>
            <div class="ls-flyout-panel" aria-label="Your simulators">
              <div class="ls-flyout-panel-inner">
                <button type="button" class="ls-flyout-action" data-flyout-new="sim">+ New simulator</button>
                <div class="ls-flyout-list" id="ls-flyout-sims"><div class="ls-flyout-empty">Hover to load…</div></div>
              </div>
            </div>
          </div>
          <button type="button" class="ls-nav-btn" data-ls-nav="store"><span class="ls-nav-icon">${NAV_ICONS.store}</span>Gem Store</button>
        </nav>
        <div class="ls-nav-bottom">
          <button type="button" class="ls-nav-btn" data-ls-nav="settings"><span class="ls-nav-icon">${NAV_ICONS.settings}</span>Settings</button>
          <button type="button" class="ls-nav-btn" data-ls-nav="help"><span class="ls-nav-icon">${NAV_ICONS.help}</span>Help</button>
          <button type="button" class="ls-nav-btn" data-ls-nav="feedback"><span class="ls-nav-icon">${NAV_ICONS.feedback}</span>Leave feedback</button>
          <div class="ls-profile" tabindex="0" id="ls-profile">
            <div class="ls-avatar-stack" id="ls-sidebar-avatar"></div>
            <div class="ls-profile-name" id="ls-profile-name">Learner</div>
            <div class="ls-profile-menu">
              <button type="button" id="ls-profile-settings">Settings</button>
              <button type="button" id="ls-profile-logout">Logout</button>
            </div>
          </div>
        </div>
      </aside>
      <main id="learner-main">
        <section class="ls-pane active" id="ls-pane-dashboard" data-pane="dashboard">
          <div class="ls-home-hero">
            <h2>How can I help you study today?</h2>
            <img src="${ASSET}/mascot.svg" alt="Veelearn study buddy" />
          </div>
          <div class="ls-ai-box">
            <div id="ls-ai-messages"></div>
            <div class="ls-ai-composer">
              <textarea id="ls-ai-input" maxlength="8000" placeholder="Ask me a question, or tell me what you want to learn…" rows="2"></textarea>
              <button type="button" id="ls-ai-send">Send</button>
            </div>
          </div>
          <p class="ls-ai-hint">I can help with questions and recommend single or master courses that fit you best.</p>
          <div id="ls-ai-recs"></div>
        </section>

        <section class="ls-pane" id="ls-pane-achievements" data-pane="achievements"></section>
        <section class="ls-pane" id="ls-pane-enrolled" data-pane="enrolled"></section>
        <section class="ls-pane" id="ls-pane-store" data-pane="store"></section>
        <section class="ls-pane" id="ls-pane-settings" data-pane="settings"></section>
        <section class="ls-pane" id="ls-pane-help" data-pane="help">
          <h2 class="ls-section-title">Help</h2>
          <p class="ls-section-sub">Quick tips for getting around Veelearn.</p>
          <div class="ls-help-card">
            <p><strong>Dashboard</strong> — Ask the study coach anything, or describe what you want to learn for course ideas.</p>
            <p><strong>Achievements</strong> — Visit daily to grow your streak and earn gems.</p>
            <p><strong>Gem Store</strong> — Spend gems on avatar looks and dashboard themes.</p>
            <p><strong>Course Creation / Simulator Studio</strong> — Build courses and sims like before.</p>
            <p><strong>Marketplace</strong> — Open it from Simulator Studio (you'll be asked to save first).</p>
          </div>
        </section>
      </main>
    `;
    document.body.prepend(shell);

    document.getElementById('ls-mobile-toggle')?.addEventListener('click', () => {
      document.body.classList.add('ls-sidebar-open');
    });
    document.getElementById('ls-sidebar-close')?.addEventListener('click', () => {
      document.body.classList.remove('ls-sidebar-open');
    });

    shell.querySelectorAll('[data-ls-nav]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const nav = btn.getAttribute('data-ls-nav');
        window.LearnerShell.navigate(nav);
        document.body.classList.remove('ls-sidebar-open');
      });
    });

    setupNavFlyouts(shell);

    document.getElementById('ls-profile-logout')?.addEventListener('click', (e) => {
      e.stopPropagation();
      if (typeof window.logout === 'function') window.logout();
    });
    document.getElementById('ls-profile-settings')?.addEventListener('click', (e) => {
      e.stopPropagation();
      window.LearnerShell.navigate('settings');
    });

    document.getElementById('ls-ai-send')?.addEventListener('click', () => {
      window.LearnerGamification?.sendDashboardAi?.();
    });
    document.getElementById('ls-ai-input')?.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        window.LearnerGamification?.sendDashboardAi?.();
      }
    });
  }

  function setActiveNav(name) {
    document.querySelectorAll('#learner-shell [data-ls-nav]').forEach((btn) => {
      btn.classList.toggle('active', btn.getAttribute('data-ls-nav') === name);
    });
  }

  function showPane(name) {
    document.querySelectorAll('#learner-shell .ls-pane').forEach((pane) => {
      pane.classList.toggle('active', pane.getAttribute('data-pane') === name);
    });
  }

  function hideLegacyDashboardSections() {
    const dash = document.getElementById('dashboard-section');
    if (dash) dash.style.display = 'none';
    const fabRoot = document.getElementById('study-coach-root');
    if (fabRoot) fabRoot.style.display = 'none';
  }

  function showLearnerShell() {
    ensureShellDom();
    // Prefer warm light for learners unless they already chose a theme
    if (!localStorage.getItem('veelearn-theme')) {
      document.documentElement.setAttribute('data-theme', 'light');
      localStorage.setItem('veelearn-theme', 'light');
    }
    document.body.classList.add('learner-shell-active');
    hideLegacyDashboardSections();

    ['landing-page', 'auth-section', 'course-editor-section', 'course-viewer-section', 'unit-management-section'].forEach((id) => {
      const el = document.getElementById(id);
      if (el) el.style.display = 'none';
    });

    const shell = document.getElementById('learner-shell');
    if (shell) shell.style.display = 'flex';

    window.LearnerGamification?.onShellShown?.();
    navigate('dashboard');
  }

  function hideLearnerShell() {
    document.body.classList.remove('learner-shell-active', 'ls-sidebar-open');
    document.body.style.background = '';
    const shell = document.getElementById('learner-shell');
    if (shell) shell.style.display = 'none';
  }

  function apiBase() {
    return typeof window.API_BASE_URL === 'string' ? window.API_BASE_URL : '';
  }

  function authHeaders() {
    const token = localStorage.getItem('token') || (typeof window.authToken === 'string' ? window.authToken : '');
    return token ? { Authorization: `Bearer ${token}` } : {};
  }

  async function fetchJson(path) {
    const res = await fetch(`${apiBase()}${path}`, {
      headers: authHeaders(),
      credentials: 'include'
    });
    return res.json().catch(() => ({}));
  }

  function setupNavFlyouts(shell) {
    const createFlyout = shell.querySelector('[data-flyout="create"]');
    const studioFlyout = shell.querySelector('[data-flyout="studio"]');

    const bindHoverLoad = (el, loader) => {
      if (!el) return;
      let collapseTimer = null;
      let lastFetch = 0;
      let lastBumpSeen = 0;
      let busy = false;
      const open = () => {
        clearTimeout(collapseTimer);
        el.classList.add('is-open');
        const now = Date.now();
        let bump = 0;
        try {
          bump = Number(localStorage.getItem('veelearn-sims-updated') || 0);
        } catch (e) {
          bump = 0;
        }
        const forceRefresh = bump > lastBumpSeen;
        if (busy || (!forceRefresh && now - lastFetch < 4000)) return;
        if (forceRefresh) lastBumpSeen = bump;
        busy = true;
        lastFetch = now;
        Promise.resolve(loader()).finally(() => {
          busy = false;
        });
      };
      const scheduleClose = () => {
        clearTimeout(collapseTimer);
        collapseTimer = setTimeout(() => el.classList.remove('is-open'), 180);
      };
      el.addEventListener('mouseenter', open);
      el.addEventListener('mouseleave', scheduleClose);
      el.addEventListener('focusin', open);
      el.addEventListener('focusout', (e) => {
        if (!el.contains(e.relatedTarget)) scheduleClose();
      });
      // Touch / click toggle when hover isn't available
      el.querySelector('.ls-nav-btn')?.addEventListener('pointerdown', (e) => {
        if (window.matchMedia('(hover: hover)').matches) return;
        // First tap expands; second tap on the label navigates via click handler
        if (!el.classList.contains('is-open')) {
          e.preventDefault();
          e.stopPropagation();
          open();
        }
      }, true);
    };

    bindHoverLoad(createFlyout, loadCourseFlyout);
    bindHoverLoad(studioFlyout, loadSimFlyout);

    shell.querySelector('[data-flyout-new="course"]')?.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      window.LearnerShell.navigate('create');
      document.body.classList.remove('ls-sidebar-open');
    });
    shell.querySelector('[data-flyout-new="sim"]')?.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      window.location.href = 'scratch-studio.html';
    });
  }

  function currentUserId() {
    if (window.currentUser?.id != null) return Number(window.currentUser.id);
    try {
      const token = localStorage.getItem('token') || '';
      const parts = token.split('.');
      if (parts.length === 3) {
        const payload = JSON.parse(atob(parts[1].replace(/-/g, '+').replace(/_/g, '/')));
        if (payload.id != null) return Number(payload.id);
        if (payload.userId != null) return Number(payload.userId);
      }
    } catch (_) { /* ignore */ }
    const profile = window.LearnerGamification?.getProfile?.();
    return profile?.id != null ? Number(profile.id) : null;
  }

  async function loadCourseFlyout() {
    const list = document.getElementById('ls-flyout-courses');
    if (!list) return;
    list.innerHTML = '<div class="ls-flyout-empty">Loading…</div>';
    try {
      const uid = currentUserId();
      let courses = [];
      if (uid) {
        const owned = await fetchJson(`/api/users/${uid}/courses`);
        if (owned.success && Array.isArray(owned.data)) {
          courses = owned.data;
        }
      }
      if (!courses.length) {
        const data = await fetchJson('/api/courses');
        courses = (data.success ? data.data || [] : []).filter(
          (c) => uid != null && Number(c.creator_id) === uid
        );
      }
      courses = [...courses].sort(
        (a, b) =>
          new Date(b.created_at || b.creation_time || 0) -
          new Date(a.created_at || a.creation_time || 0)
      );

      if (!courses.length) {
        list.innerHTML = '<div class="ls-flyout-empty">No courses yet — create one!</div>';
        return;
      }

      list.innerHTML = courses
        .map((c) => {
          const status = c.status ? `<span class="ls-flyout-meta">${esc(c.status)}</span>` : '';
          return `<button type="button" class="ls-flyout-item" data-edit-course="${c.id}" data-my-course="1">
            <span class="ls-flyout-title">${esc(c.title || 'Untitled')}</span>${status}
          </button>`;
        })
        .join('');

      list.querySelectorAll('[data-edit-course]').forEach((btn) => {
        btn.addEventListener('click', async (e) => {
          e.preventDefault();
          e.stopPropagation();
          const id = parseInt(btn.getAttribute('data-edit-course'), 10);
          const course = courses.find((c) => Number(c.id) === id);
          if (course && typeof window.__veelearnPushCourse === 'function') {
            window.__veelearnPushCourse(course);
          }
          document.body.classList.remove('ls-sidebar-open');
          if (typeof window.editCourse === 'function') {
            window.LearnerShell.hideLearnerShell();
            await window.editCourse(id);
          }
        });
        btn.addEventListener('contextmenu', (e) => {
          e.preventDefault();
          e.stopPropagation();
          if (typeof e.stopImmediatePropagation === 'function') e.stopImmediatePropagation();
          const id = parseInt(btn.getAttribute('data-edit-course'), 10);
          if (!id) return;
          // Keep flyout open while the menu is used
          const flyout = btn.closest('[data-flyout="create"]');
          if (flyout) flyout.classList.add('is-open');
          if (typeof window.showCourseContextMenu === 'function') {
            window.showCourseContextMenu(e.clientX, e.clientY, id);
          } else if (typeof window.deleteCourse === 'function') {
            window.deleteCourse(id);
          }
        });
      });
    } catch (err) {
      list.innerHTML = '<div class="ls-flyout-empty">Could not load courses.</div>';
    }
  }

  async function loadSimFlyout() {
    const list = document.getElementById('ls-flyout-sims');
    if (!list) return;
    list.innerHTML = '<div class="ls-flyout-empty">Loading…</div>';
    try {
      const data = await fetchJson('/api/my-simulators');
      const sims = data.success ? data.data || [] : [];
      if (!sims.length) {
        list.innerHTML = '<div class="ls-flyout-empty">No simulators yet — create one!</div>';
        return;
      }
      list.innerHTML = sims
        .map((s) => {
          const vis = s.is_public ? 'public' : 'draft';
          return `<button type="button" class="ls-flyout-item" data-edit-sim="${s.id}">
            <span class="ls-flyout-title">${esc(s.title || 'Untitled')}</span>
            <span class="ls-flyout-meta">${esc(vis)}</span>
          </button>`;
        })
        .join('');
      list.querySelectorAll('[data-edit-sim]').forEach((btn) => {
        btn.addEventListener('click', (e) => {
          e.preventDefault();
          e.stopPropagation();
          const id = btn.getAttribute('data-edit-sim');
          window.location.href = `scratch-studio.html?simId=${encodeURIComponent(id)}`;
        });
      });
    } catch (err) {
      list.innerHTML = '<div class="ls-flyout-empty">Could not load simulators.</div>';
    }
  }

  function navigate(name) {
    ensureShellDom();

    if (name === 'create') {
      if (typeof window.createNewCourse === 'function') {
        hideLearnerShell();
        window.createNewCourse();
      }
      return;
    }
    if (name === 'studio') {
      window.location.href = 'scratch-studio.html';
      return;
    }
    if (name === 'feedback') {
      window.LearnerGamification?.openFeedbackModal?.();
      return;
    }

    const paneName = ['dashboard', 'achievements', 'enrolled', 'store', 'settings', 'help'].includes(name)
      ? name
      : 'dashboard';
    setActiveNav(paneName === 'help' ? 'help' : paneName === 'settings' ? 'settings' : paneName);
    showPane(paneName);

    if (paneName === 'dashboard') window.LearnerGamification?.loadDashboardAi?.();
    if (paneName === 'achievements') window.LearnerGamification?.renderAchievements?.();
    if (paneName === 'enrolled') window.LearnerGamification?.renderEnrolled?.();
    if (paneName === 'store') window.LearnerGamification?.renderStore?.();
    if (paneName === 'settings') window.LearnerGamification?.renderSettings?.();
  }

  function updateProfileUI(profile) {
    ensureShellDom();
    if (!profile) return;
    const nameEl = document.getElementById('ls-profile-name');
    if (nameEl) nameEl.textContent = profile.displayName || 'Learner';
    const gemsEl = document.getElementById('ls-gems-count');
    if (gemsEl) gemsEl.textContent = String(profile.gems ?? 0);
    const shell = document.getElementById('learner-shell');
    if (shell && profile.dashboardTheme) {
      shell.setAttribute('data-learner-theme', profile.dashboardTheme);
      try { localStorage.setItem('learnerDashboardTheme', profile.dashboardTheme); } catch (e) { /* ignore */ }
      requestAnimationFrame(() => {
        const bg = getComputedStyle(shell).getPropertyValue('--ls-bg').trim();
        if (bg) document.body.style.background = bg;
      });
    }
    window.LearnerGamification?.renderAvatarInto?.(
      document.getElementById('ls-sidebar-avatar'),
      profile.avatarConfig
    );
  }

  window.LearnerShell = {
    ASSET,
    esc,
    ensureShellDom,
    showLearnerShell,
    hideLearnerShell,
    navigate,
    updateProfileUI,
    refreshCourseFlyout: () => loadCourseFlyout(),
    refreshSimFlyout: () => loadSimFlyout(),
    isActive: () => document.body.classList.contains('learner-shell-active')
  };
})();
