/**
 * Learner gamification: gems, streaks, store, avatar, AI dashboard home, celebrations.
 */
(function () {
  let profileCache = null;
  let aiHistoryLoaded = false;
  /** @type {Array|null} Cached enhanced enrollments for instant Enrolled pane */
  let enrollmentsCache = null;
  /** @type {Promise<Array>|null} In-flight prefetch so renderEnrolled can await it */
  let enrollmentsPrefetch = null;

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
    const res = await fetch(`${apiBase()}${path}`, {
      ...opts,
      headers,
      credentials: 'include'
    });
    const data = await res.json().catch(() => ({}));
    return data;
  }

  /**
   * Fetch enrollments once and cache. Falls back to basic list only when enhanced fails
   * (not when enhanced legitimately returns an empty array).
   * @param {{ force?: boolean }} [opts]
   * @returns {Promise<Array>}
   */
  async function fetchEnrollments(opts = {}) {
    if (!opts.force && enrollmentsCache) return enrollmentsCache;
    if (!opts.force && enrollmentsPrefetch) return enrollmentsPrefetch;

    enrollmentsPrefetch = (async () => {
      try {
        const data = await api('/api/users/enrollments/enhanced');
        if (data.success) {
          enrollmentsCache = data.data || [];
          return enrollmentsCache;
        }
        // Enhanced failed — try basic list once
        const fallback = await api('/api/users/enrollments');
        if (fallback.success) {
          enrollmentsCache = fallback.data || [];
          return enrollmentsCache;
        }
        enrollmentsCache = [];
        return enrollmentsCache;
      } catch (_) {
        enrollmentsCache = enrollmentsCache || [];
        return enrollmentsCache;
      } finally {
        enrollmentsPrefetch = null;
      }
    })();

    return enrollmentsPrefetch;
  }

  function paintEnrolledList(courses) {
    const list = document.getElementById('ls-enrolled-ul');
    if (!list) return;
    if (!courses.length) {
      list.innerHTML = '<li>No enrollments yet — ask the Dashboard coach to suggest a course!</li>';
      return;
    }
    list.innerHTML = courses
      .map((c) => {
        const title = c.title || c.course_title || 'Course';
        const id = c.course_id || c.id;
        return `<li><div><strong>${esc(title)}</strong></div>
          <button type="button" class="ls-btn-primary" data-open="${id}">Open</button></li>`;
      })
      .join('');
    list.querySelectorAll('[data-open]').forEach((btn) => {
      btn.addEventListener('click', async () => {
        const id = parseInt(btn.getAttribute('data-open'), 10);
        window.LearnerShell?.hideLearnerShell?.();
        try {
          const detail = await api(`/api/courses/${id}`);
          if (detail.success && detail.data && typeof window.__veelearnPushCourse === 'function') {
            window.__veelearnPushCourse(detail.data);
          }
        } catch (_) { /* ignore */ }
        if (typeof window.viewCourse === 'function') window.viewCourse(id);
      });
    });
  }

  function asset(key) {
    const base = window.LearnerShell?.ASSET || 'assets/learner';
    return `${base}/${key}.svg`;
  }

  function itemAsset(itemId) {
    const map = {
      hat_blue: 'hat-blue',
      hat_crown: 'hat-crown',
      glasses_round: 'glasses-round',
      shirt_green: 'shirt-green',
      shirt_hero: 'shirt-hero',
      cape_red: 'cape-red',
      acc_star: 'acc-star',
      theme_warm: 'gem',
      theme_blue: 'gem',
      theme_red: 'gem',
      theme_cool: 'gem',
      theme_happy: 'gem',
      theme_hacker: 'gem',
      theme_superhero: 'gem'
    };
    return asset(map[itemId] || 'gem');
  }

  function esc(s) {
    return window.LearnerShell?.esc ? window.LearnerShell.esc(s) : String(s ?? '');
  }

  function renderAvatarInto(container, cfg) {
    if (!container) return;
    const c = cfg || {};
    const layers = ['cape', 'base', 'shirt', 'hat', 'glasses', 'accessory'];
    const html = [];
    layers.forEach((slot) => {
      if (slot === 'base') {
        html.push(`<img src="${asset('avatar-base')}" alt="" />`);
        return;
      }
      const id = c[slot];
      if (!id) return;
      html.push(`<img src="${itemAsset(id)}" alt="" />`);
    });
    container.innerHTML = html.join('');
  }

  async function refreshProfile() {
    const data = await api('/api/learner/profile');
    if (data.success) {
      profileCache = data.data;
      window.LearnerShell?.updateProfileUI?.(profileCache);
    }
    return profileCache;
  }

  async function checkin() {
    const data = await api('/api/learner/checkin', { method: 'POST', body: '{}' });
    if (data.success && data.data) {
      if (!data.data.alreadyCheckedIn && data.data.gemsAwarded > 0) {
        showGemToast(data.data.gemsAwarded, 'Daily streak bonus!');
      }
      await refreshProfile();
    }
    return data;
  }

  function showGemToast(amount, label) {
    document.querySelectorAll('.ls-gem-toast').forEach((el) => el.remove());
    const toast = document.createElement('div');
    toast.className = 'ls-gem-toast';
    toast.innerHTML = `<img src="${asset('gem')}" alt="" /><span>+${amount} gems${label ? ` — ${esc(label)}` : ''}</span>`;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 2800);
  }

  function celebrateCorrect() {
    let root = document.getElementById('ls-celebrate');
    if (!root) {
      root = document.createElement('div');
      root.id = 'ls-celebrate';
      document.body.appendChild(root);
    }
    root.innerHTML = '';
    const emojis = ['🎉', '✨', '😄', '🌟', '💛', '🥳', '🔥', '👏', '🌈', '⭐'];
    for (let i = 0; i < 36; i++) {
      const span = document.createElement('span');
      span.className = 'ls-emoji-particle';
      span.textContent = emojis[i % emojis.length];
      const angle = (Math.PI * 2 * i) / 36;
      const dist = 120 + Math.random() * 220;
      span.style.left = '50%';
      span.style.top = '45%';
      span.style.setProperty('--dx', `${Math.cos(angle) * dist}px`);
      span.style.setProperty('--dy', `${Math.sin(angle) * dist}px`);
      span.style.animationDelay = `${Math.random() * 0.15}s`;
      root.appendChild(span);
    }
    setTimeout(() => {
      root.innerHTML = '';
    }, 1600);
  }

  async function onQuizCorrect(questionId) {
    celebrateCorrect();
    try {
      const data = await api('/api/learner/reward-quiz', {
        method: 'POST',
        body: JSON.stringify({ questionId })
      });
      if (data.success && data.data?.gemsAwarded > 0) {
        showGemToast(data.data.gemsAwarded, `${data.data.multiplier || 1}x streak`);
        await refreshProfile();
      }
    } catch (e) {
      console.error('reward-quiz', e);
    }
  }

  function typesetCoachBubble(el) {
    if (!el) return;
    const eng = window.VeelearnWidgetEngine;
    if (eng && typeof eng.typesetMath === 'function') {
      eng.typesetMath(el);
      return;
    }
    if (window.MathJax && typeof window.MathJax.typesetPromise === 'function') {
      window.MathJax.typesetPromise([el]).catch(() => {});
    }
  }

  async function ensureWidgetEngine() {
    if (window.VeelearnWidgetEngine) return window.VeelearnWidgetEngine;
    if (typeof window.__veelearnLoadHeavy === 'function') {
      await window.__veelearnLoadHeavy('widgets');
    }
    return window.VeelearnWidgetEngine;
  }

  async function mountCoachWidgets(host, widgets, opts) {
    if (!host || !widgets || !widgets.length) return;
    const eng = await ensureWidgetEngine();
    if (!eng || typeof eng.mountWidgets !== 'function') return;
    await eng.mountWidgets(host, widgets, opts || {});
  }

  function showDashboardTyping() {
    const box = document.getElementById('ls-ai-messages');
    if (!box) return;
    removeDashboardTyping();
    const wrap = document.createElement('div');
    wrap.id = 'ls-ai-typing';
    wrap.classList.add('ls-bubble-coach');
    wrap.style.marginBottom = '10px';
    wrap.style.padding = '10px 12px';
    wrap.style.borderRadius = '12px';
    wrap.style.marginRight = '24px';
    wrap.setAttribute('aria-busy', 'true');
    wrap.innerHTML =
      '<strong>Coach</strong><div class="ls-ai-typing-dots" aria-hidden="true"><span>.</span><span>.</span><span>.</span></div>';
    box.appendChild(wrap);
    box.scrollTop = box.scrollHeight;
  }

  function removeDashboardTyping() {
    document.getElementById('ls-ai-typing')?.remove();
  }

  function appendAiBubble(role, text, widgets, mountOpts) {
    const box = document.getElementById('ls-ai-messages');
    if (!box) return null;
    const wrap = document.createElement('div');
    wrap.style.marginBottom = '10px';
    wrap.style.padding = '10px 12px';
    wrap.style.borderRadius = '12px';
    wrap.style.whiteSpace = 'pre-wrap';
    if (role === 'user') {
      wrap.classList.add('ls-bubble-user');
      wrap.style.marginLeft = '24px';
      wrap.innerHTML = `<strong>You</strong><div class="ls-bubble-body">${esc(text)}</div>`;
    } else {
      wrap.classList.add('ls-bubble-coach');
      wrap.style.marginRight = '24px';
      wrap.innerHTML = `<strong>Coach</strong><div class="ls-bubble-body">${esc(text)}</div>`;
    }
    const widgetHost = document.createElement('div');
    widgetHost.className = 'vl-widget-host';
    wrap.appendChild(widgetHost);
    box.appendChild(wrap);
    box.scrollTop = box.scrollHeight;
    typesetCoachBubble(wrap.querySelector('.ls-bubble-body') || wrap);
    if (role !== 'user' && widgets && widgets.length) {
      mountCoachWidgets(widgetHost, widgets, mountOpts).then(() => {
        box.scrollTop = box.scrollHeight;
      });
    }
    return wrap;
  }

  function renderRecs(recs) {
    const el = document.getElementById('ls-ai-recs');
    if (!el) return;
    if (!recs || !recs.length) {
      el.innerHTML = '';
      return;
    }
    el.innerHTML = recs
      .map((r) => {
        const meta = [
          r.courseType ? String(r.courseType) : null,
          r.gradeLevel != null ? `Grade ${r.gradeLevel}` : null,
          typeof r.likeCount === 'number' ? `${r.likeCount} likes` : null
        ]
          .filter(Boolean)
          .join(' · ');
        return `
      <div class="ls-rec-card">
        <strong>${esc(r.title)}</strong>
        ${meta ? `<div style="color:var(--ls-muted);font-size:0.8rem;margin-top:2px;">${esc(meta)}</div>` : ''}
        <div style="color:var(--ls-muted);font-size:0.9rem;">${esc(r.reason || '')}</div>
        <div class="ls-rec-actions">
          <button type="button" class="ls-btn-primary" data-enroll="${r.courseId}">View / Enroll</button>
          <button type="button" class="ls-btn-soft" data-like="${r.courseId}">Like this course</button>
        </div>
      </div>`;
      })
      .join('');

    el.querySelectorAll('[data-enroll]').forEach((btn) => {
      btn.addEventListener('click', async () => {
        const id = parseInt(btn.getAttribute('data-enroll'), 10);
        try {
          // Prefer enroll then open; fall back to view if already enrolled
          const enrollRes = await api(`/api/courses/${id}/enroll`, { method: 'POST', body: '{}' });
          if (!enrollRes.success && !(enrollRes.message || '').toLowerCase().includes('already')) {
            // Try master enroll
            await api(`/api/courses/${id}/enroll-master`, { method: 'POST', body: '{}' });
          }
        } catch (_) { /* ignore */ }
        window.LearnerShell?.hideLearnerShell?.();
        if (typeof window.viewCourse === 'function') {
          try {
            const detail = await api(`/api/courses/${id}`);
            if (detail.success && detail.data && typeof window.__veelearnPushCourse === 'function') {
              window.__veelearnPushCourse(detail.data);
            }
          } catch (_) { /* ignore */ }
          window.viewCourse(id);
        }
      });
    });
    el.querySelectorAll('[data-like]').forEach((btn) => {
      btn.addEventListener('click', async () => {
        const id = parseInt(btn.getAttribute('data-like'), 10);
        try {
          await api(`/api/courses/${id}/like`, { method: 'POST', body: '{}' });
          btn.textContent = 'Liked!';
          btn.disabled = true;
        } catch (_) {
          /* ignore */
        }
      });
    });
  }

  async function loadDashboardAi() {
    const box = document.getElementById('ls-ai-messages');
    if (!box) return;
    if (aiHistoryLoaded && box.childElementCount) return;
    box.innerHTML = '';
    try {
      const data = await api('/api/ai/tutor/history?limit=30');
      if (data.success && Array.isArray(data.data)) {
        for (const m of data.data) {
          appendAiBubble(
            m.role === 'user' ? 'user' : 'assistant',
            m.content,
            m.widgets || [],
            { skipDrawing: true }
          );
        }
      }
      if (!box.childElementCount) {
        appendAiBubble(
          'assistant',
          "Hi! Tell me what you want to learn, or ask a question — I'll help and can suggest great courses (I'll pick top liked ones when there are a few that fit)."
        );
      }
      aiHistoryLoaded = true;
    } catch (e) {
      appendAiBubble('assistant', 'Welcome! Ask me anything about what you want to study.');
    }
  }

  async function sendDashboardAi() {
    const input = document.getElementById('ls-ai-input');
    const sendBtn = document.getElementById('ls-ai-send');
    if (!input) return;
    const message = input.value.trim();
    if (!message) return;
    input.value = '';
    appendAiBubble('user', message);
    if (sendBtn) sendBtn.disabled = true;
    showDashboardTyping();
    try {
      const data = await api('/api/ai/tutor/chat', {
        method: 'POST',
        body: JSON.stringify({ message })
      });
      removeDashboardTyping();
      if (data.success) {
        appendAiBubble('assistant', data.data.reply || '…', data.data.widgets || []);
        renderRecs(data.data.recommendations || []);
      } else {
        appendAiBubble('assistant', data.message || 'Sorry, I could not reply just now.');
      }
    } catch (e) {
      removeDashboardTyping();
      appendAiBubble('assistant', 'Network error — please try again.');
    } finally {
      if (sendBtn) sendBtn.disabled = false;
    }
  }

  function renderAchievements() {
    const pane = document.getElementById('ls-pane-achievements');
    if (!pane || !profileCache) {
      refreshProfile().then(() => renderAchievements());
      return;
    }
    const p = profileCache;
    const badges = [
      { id: 'first', label: 'First spark', ok: (p.quizCorrect || 0) >= 1 },
      { id: 'streak3', label: '3-day streak', ok: (p.currentStreak || 0) >= 3 || (p.longestStreak || 0) >= 3 },
      { id: 'streak7', label: 'Week warrior', ok: (p.longestStreak || 0) >= 7 },
      { id: 'quiz20', label: '20 correct', ok: (p.quizCorrect || 0) >= 20 },
      { id: 'gems100', label: '100 gems earned', ok: (p.gems || 0) >= 100 }
    ];
    pane.innerHTML = `
      <div class="ls-ach-header">
        <div>
          <h2>Achievements</h2>
          <p>Your top achievements</p>
        </div>
        <img src="${asset('achievements-hero')}" alt="" />
      </div>
      <div class="ls-metrics">
        <div class="ls-metric">
          <img src="${asset('streak-flame')}" alt="" />
          <div class="val">${p.currentStreak || 0} days</div>
          <div class="label">Current streak</div>
        </div>
        <div class="ls-metric">
          <img src="${asset('stopwatch')}" alt="" />
          <div class="val">${p.longestStreak || 0} days</div>
          <div class="label">Longest streak</div>
        </div>
        <div class="ls-metric">
          <img src="${asset('crown')}" alt="" />
          <div class="val">${p.quizCorrect || 0}</div>
          <div class="label">Correct answers</div>
        </div>
        <div class="ls-metric">
          <img src="${asset('gem')}" alt="" />
          <div class="val">${p.gems || 0}</div>
          <div class="label">Gems · ${p.streakMultiplier || 1}x quiz bonus</div>
        </div>
      </div>
      <div class="ls-badges">
        ${badges
          .map((b) => `<span class="ls-badge ${b.ok ? '' : 'locked'}">${esc(b.label)}</span>`)
          .join('')}
      </div>
    `;
  }

  async function renderEnrolled() {
    const pane = document.getElementById('ls-pane-enrolled');
    if (!pane) return;
    const hasCache = Array.isArray(enrollmentsCache);
    pane.innerHTML = `<h2 class="ls-section-title">Enrolled Courses</h2><p class="ls-section-sub">Jump back into what you're learning.</p><ul class="ls-enrolled-list" id="ls-enrolled-ul">${hasCache ? '' : '<li>Loading…</li>'}</ul>`;
    if (hasCache) {
      paintEnrolledList(enrollmentsCache);
    }
    try {
      // Use in-flight prefetch if shell already started one; otherwise fetch (refresh in background when cached)
      const courses = await fetchEnrollments({ force: hasCache });
      paintEnrolledList(courses);
    } catch (e) {
      const list = document.getElementById('ls-enrolled-ul');
      if (list && !hasCache) list.innerHTML = '<li>Could not load enrollments.</li>';
    }
  }

  async function renderStore() {
    const pane = document.getElementById('ls-pane-store');
    if (!pane) return;
    pane.innerHTML = `<h2 class="ls-section-title">Gem Store</h2><p class="ls-section-sub">Customize your avatar and dashboard with gems.</p><div class="ls-store-grid" id="ls-store-grid">Loading…</div>
      <h3 style="margin-top:28px;">Equip avatar</h3>
      <div id="ls-equip-area" style="margin-top:12px;"></div>`;
    const data = await api('/api/learner/store');
    const grid = document.getElementById('ls-store-grid');
    if (!data.success) {
      grid.textContent = 'Store unavailable.';
      return;
    }
    if (typeof data.data.gems === 'number') {
      const el = document.getElementById('ls-gems-count');
      if (el) el.textContent = String(data.data.gems);
    }
    grid.innerHTML = (data.data.items || [])
      .map((it) => {
        const owned = it.owned;
        const isTheme = it.item_type === 'theme';
        return `<div class="ls-store-card">
          <img src="${itemAsset(it.item_id)}" alt="" />
          <h4>${esc(it.name)}</h4>
          <p>${esc(it.description || '')}</p>
          <p><strong>${it.gem_cost || 0}</strong> gems · ${esc(it.item_type)}</p>
          ${
            owned
              ? `<button type="button" class="ls-btn-soft" data-equip="${it.item_id}" data-type="${it.item_type}">${isTheme ? 'Use theme' : 'Equip'}</button>`
              : `<button type="button" class="ls-btn-primary" data-buy="${it.item_id}">Buy</button>`
          }
        </div>`;
      })
      .join('');

    grid.querySelectorAll('[data-buy]').forEach((btn) => {
      btn.addEventListener('click', async () => {
        const id = btn.getAttribute('data-buy');
        const res = await api('/api/learner/store/purchase', {
          method: 'POST',
          body: JSON.stringify({ itemId: id })
        });
        if (res.success) {
          showGemToast(1, 'Item unlocked!');
          await refreshProfile();
          renderStore();
        } else {
          alert(res.message || 'Purchase failed');
        }
      });
    });

    grid.querySelectorAll('[data-equip]').forEach((btn) => {
      btn.addEventListener('click', async () => {
        const id = btn.getAttribute('data-equip');
        const type = btn.getAttribute('data-type');
        let body;
        if (type === 'theme') {
          const theme = id.replace(/^theme_/, '');
          body = { theme };
        } else {
          const slot =
            type === 'hat'
              ? 'hat'
              : type === 'glasses'
                ? 'glasses'
                : type === 'shirt'
                  ? 'shirt'
                  : type === 'cape'
                    ? 'cape'
                    : 'accessory';
          body = { slot, itemId: id };
        }
        const res = await api('/api/learner/equip', {
          method: 'POST',
          body: JSON.stringify(body)
        });
        if (res.success) {
          await refreshProfile();
          renderStore();
        } else {
          alert(res.message || 'Could not equip');
        }
      });
    });

    const equip = document.getElementById('ls-equip-area');
    if (equip && profileCache) {
      equip.innerHTML = `<div class="ls-avatar-stack" style="width:96px;height:120px;position:relative;" id="ls-store-avatar-preview"></div>
        <button type="button" class="ls-btn-soft" id="ls-unequip-all" style="margin-top:10px;">Clear accessories</button>`;
      renderAvatarInto(document.getElementById('ls-store-avatar-preview'), profileCache.avatarConfig);
      document.getElementById('ls-unequip-all')?.addEventListener('click', async () => {
        for (const slot of ['hat', 'glasses', 'shirt', 'cape', 'accessory']) {
          await api('/api/learner/equip', {
            method: 'POST',
            body: JSON.stringify({ slot, itemId: null })
          });
        }
        await refreshProfile();
        renderStore();
      });
    }
  }

  function renderSettings() {
    const pane = document.getElementById('ls-pane-settings');
    if (!pane) return;
    const name = profileCache?.displayName || '';
    pane.innerHTML = `
      <h2 class="ls-section-title">Settings</h2>
      <p class="ls-section-sub">Your display name shows instead of your email.</p>
      <div class="ls-settings-card">
        <label for="ls-display-name">Display name</label>
        <input id="ls-display-name" maxlength="80" value="${esc(name)}" />
        <button type="button" id="ls-save-settings" class="ls-btn-primary">Save</button>
        <hr style="border:none;border-top:1px solid var(--ls-border);margin:18px 0;" />
        <p style="margin:0 0 8px;font-weight:700;color:var(--ls-text);">Appearance</p>
        <button type="button" class="ls-btn-soft" id="ls-toggle-dark" style="margin-top:0;">Toggle light / dark mode</button>
      </div>`;
    document.getElementById('ls-save-settings')?.addEventListener('click', async () => {
      const displayName = document.getElementById('ls-display-name')?.value?.trim();
      const res = await api('/api/learner/settings', {
        method: 'PUT',
        body: JSON.stringify({ displayName })
      });
      if (res.success) {
        await refreshProfile();
        alert('Saved!');
      } else {
        alert(res.message || 'Could not save');
      }
    });
    document.getElementById('ls-toggle-dark')?.addEventListener('click', () => {
      const html = document.documentElement;
      const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', next);
      localStorage.setItem('veelearn-theme', next);
    });
  }

  function openFeedbackModal() {
    document.getElementById('ls-feedback-backdrop')?.remove();
    const backdrop = document.createElement('div');
    backdrop.className = 'ls-modal-backdrop';
    backdrop.id = 'ls-feedback-backdrop';
    backdrop.innerHTML = `
      <div class="ls-feedback-modal" role="dialog" aria-labelledby="ls-fb-title">
        <h3 id="ls-fb-title">Leave feedback</h3>
        <p style="color:var(--ls-muted);font-size:0.9rem;">Sent to the Veelearn team (superadmin).</p>
        <textarea id="ls-feedback-text" rows="5" maxlength="4000" placeholder="What should we improve?"></textarea>
        <div style="display:flex;gap:8px;">
          <button type="button" id="ls-feedback-send" class="ls-btn-primary">Send</button>
          <button type="button" class="ls-btn-soft" id="ls-feedback-cancel">Cancel</button>
        </div>
      </div>`;
    document.body.appendChild(backdrop);
    document.getElementById('ls-feedback-cancel')?.addEventListener('click', () => backdrop.remove());
    backdrop.addEventListener('click', (e) => {
      if (e.target === backdrop) backdrop.remove();
    });
    document.getElementById('ls-feedback-send')?.addEventListener('click', async () => {
      const message = document.getElementById('ls-feedback-text')?.value?.trim();
      const res = await api('/api/learner/feedback', {
        method: 'POST',
        body: JSON.stringify({ message })
      });
      if (res.success) {
        alert(res.message || 'Thanks!');
        backdrop.remove();
      } else {
        alert(res.message || 'Could not send');
      }
    });
  }

  async function renderVolunteer() {
    const pane = document.getElementById('ls-pane-volunteer');
    if (!pane) return;
    pane.innerHTML = `
      <h2 class="ls-section-title">Volunteer Hours</h2>
      <p class="ls-section-sub">Hours earned creating courses, plus certificates you can download.</p>
      <div class="ls-volunteer-stats"><p class="ls-section-sub">Loading…</p></div>
    `;
    try {
      const result = await api('/api/users/volunteer-stats');
      const container = pane.querySelector('.ls-volunteer-stats');
      if (!container) return;
      if (!result.success || !result.data) {
        container.innerHTML = `<p class="ls-section-sub">${esc(result.message || 'Could not load volunteer hours.')}</p>`;
        return;
      }

      const data = result.data;
      const hours = Number(data.total_volunteer_hours) || 0;
      const verified = !!data.is_verified_creator;
      const certs = Array.isArray(data.certificates) ? data.certificates : [];
      const nextMilestone = getNextVolunteerMilestone(hours);
      const base = apiBase();

      let certsHtml = '';
      if (certs.length > 0) {
        certsHtml = `
          <div class="ls-cert-list">
            <h3 class="ls-volunteer-certs-title">Your certificates</h3>
            ${certs
              .map((cert) => {
                const code = esc(cert.verification_code || '');
                const issued = cert.issued_at ? new Date(cert.issued_at).toLocaleDateString() : '';
                const hrs = Number(cert.hours_certified) || 0;
                return `
                  <div class="ls-cert-row">
                    <div class="ls-cert-info">
                      <strong>${hrs} Hours Volunteer Certificate</strong>
                      <span class="ls-cert-meta">Issued: ${esc(issued)}</span>
                    </div>
                    <div class="ls-cert-actions">
                      <a class="ls-btn-primary" href="${base}/api/certificates/verify/${code}?format=pdf" target="_blank" rel="noopener">Download PDF</a>
                      <a class="ls-btn-soft" href="${base}/api/certificates/verify/${code}" target="_blank" rel="noopener">Verify</a>
                    </div>
                  </div>`;
              })
              .join('')}
          </div>`;
      } else if (hours > 0) {
        certsHtml = `
          <div class="ls-cert-list">
            <p class="ls-section-sub">Certificates unlock every 5 hours. Refresh this page if a new milestone should appear.</p>
          </div>`;
      } else {
        certsHtml = `
          <div class="ls-cert-list">
            <p class="ls-section-sub">No hours yet. Time spent actively creating courses counts toward volunteer hours and certificates.</p>
          </div>`;
      }

      container.innerHTML = `
        <div class="ls-metrics ls-volunteer-metrics">
          <div class="ls-metric ls-volunteer-metric">
            <div class="val">${hours.toFixed(1)}h</div>
            <div class="label">Total hours</div>
          </div>
          <div class="ls-metric ls-volunteer-metric">
            <div class="val">${verified ? 'Verified Creator' : 'Not yet verified'}</div>
            <div class="label">${verified ? 'Status' : 'Need 20h for verification'}</div>
          </div>
          <div class="ls-metric ls-volunteer-metric">
            <div class="val">${esc(String(nextMilestone))}${nextMilestone === 'All achieved!' ? '' : 'h'}</div>
            <div class="label">Next milestone</div>
          </div>
        </div>
        ${certsHtml}
      `;
    } catch (e) {
      const container = pane.querySelector('.ls-volunteer-stats');
      if (container) container.innerHTML = '<p class="ls-section-sub">Could not load volunteer hours.</p>';
    }
  }

  function getNextVolunteerMilestone(currentHours) {
    const milestones = [5, 10, 20, 50, 100];
    for (const m of milestones) {
      if (currentHours < m) return m;
    }
    return 'All achieved!';
  }

  async function onShellShown() {
    aiHistoryLoaded = false;
    // Prefetch enrollments in parallel with profile/checkin so Enrolled pane is instant
    const enrollmentsReady = fetchEnrollments({ force: true });
    await Promise.all([refreshProfile(), checkin(), enrollmentsReady]);
  }

  window.LearnerGamification = {
    refreshProfile,
    checkin,
    onQuizCorrect,
    celebrateCorrect,
    showGemToast,
    loadDashboardAi,
    sendDashboardAi,
    renderAchievements,
    renderEnrolled,
    renderStore,
    renderVolunteer,
    renderSettings,
    openFeedbackModal,
    renderAvatarInto,
    onShellShown,
    getProfile: () => profileCache,
    prefetchEnrollments: () => fetchEnrollments({ force: true })
  };
})();
