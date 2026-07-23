/**
 * Learner gamification: gems, streaks, store, avatar, AI dashboard home, celebrations.
 */
(function () {
  let profileCache = null;
  let aiHistoryLoaded = false;

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
    const layers = ['cape', 'base', 'shirt', 'glasses', 'hat', 'accessory'];
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

  function appendAiBubble(role, text) {
    const box = document.getElementById('ls-ai-messages');
    if (!box) return;
    const wrap = document.createElement('div');
    wrap.style.marginBottom = '10px';
    wrap.style.padding = '10px 12px';
    wrap.style.borderRadius = '12px';
    wrap.style.whiteSpace = 'pre-wrap';
    if (role === 'user') {
      wrap.style.background = 'var(--ls-blue-soft)';
      wrap.style.marginLeft = '24px';
      wrap.innerHTML = `<strong>You</strong><div>${esc(text)}</div>`;
    } else {
      wrap.style.background = 'var(--ls-accent-soft)';
      wrap.style.marginRight = '24px';
      wrap.innerHTML = `<strong>Coach</strong><div>${esc(text)}</div>`;
    }
    box.appendChild(wrap);
    box.scrollTop = box.scrollHeight;
  }

  function renderRecs(recs) {
    const el = document.getElementById('ls-ai-recs');
    if (!el) return;
    if (!recs || !recs.length) {
      el.innerHTML = '';
      return;
    }
    el.innerHTML = recs
      .map(
        (r) => `
      <div class="ls-rec-card">
        <strong>${esc(r.title)}</strong>
        <div style="color:var(--ls-muted);font-size:0.9rem;">${esc(r.reason || '')}</div>
        <div class="ls-rec-actions">
          <button type="button" class="ls-btn-primary" data-enroll="${r.courseId}">View / Enroll</button>
          <button type="button" class="ls-btn-soft" data-like="${r.courseId}">Like this course</button>
        </div>
      </div>`
      )
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
        data.data.forEach((m) => appendAiBubble(m.role === 'user' ? 'user' : 'assistant', m.content));
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
    try {
      const data = await api('/api/ai/tutor/chat', {
        method: 'POST',
        body: JSON.stringify({ message })
      });
      if (data.success) {
        appendAiBubble('assistant', data.data.reply || '…');
        renderRecs(data.data.recommendations || []);
      } else {
        appendAiBubble('assistant', data.message || 'Sorry, I could not reply just now.');
      }
    } catch (e) {
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
    pane.innerHTML = `<h2 class="ls-section-title">Enrolled Courses</h2><p class="ls-section-sub">Jump back into what you're learning.</p><ul class="ls-enrolled-list" id="ls-enrolled-ul"><li>Loading…</li></ul>`;
    try {
      let data = await api('/api/users/enrollments/enhanced');
      let courses = data.success ? data.data || [] : [];
      if (!courses.length) {
        data = await api('/api/users/enrollments');
        courses = data.success ? data.data || [] : [];
      }
      const list = document.getElementById('ls-enrolled-ul');
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
        btn.addEventListener('click', () => {
          const id = parseInt(btn.getAttribute('data-open'), 10);
          window.LearnerShell?.hideLearnerShell?.();
          if (typeof window.viewCourse === 'function') window.viewCourse(id);
        });
      });
    } catch (e) {
      const list = document.getElementById('ls-enrolled-ul');
      if (list) list.innerHTML = '<li>Could not load enrollments.</li>';
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
        <button type="button" id="ls-save-settings">Save</button>
        <hr style="border:none;border-top:1px solid var(--ls-border);margin:18px 0;" />
        <p style="margin:0 0 8px;font-weight:700;">Appearance</p>
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
          <button type="button" id="ls-feedback-send">Send</button>
          <button type="button" class="ls-btn-soft" id="ls-feedback-cancel" style="background:var(--ls-accent-soft);color:var(--ls-accent);">Cancel</button>
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

  async function onShellShown() {
    aiHistoryLoaded = false;
    await refreshProfile();
    await checkin();
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
    renderSettings,
    openFeedbackModal,
    renderAvatarInto,
    onShellShown,
    getProfile: () => profileCache
  };
})();
