/**
 * P4/P5 dashboard surfaces.
 *
 * Kept out of script.js on purpose: this file owns the creator pane (readiness
 * and teaching impact), the teacher's "assign a practice session" flow with
 * per-student mastery, and the entry point from a course into a session. It
 * talks to the same API as the rest of the dashboard and renders into elements
 * index.html already provides.
 *
 * Every colour comes from a `.vl-*` class in index.html so the surfaces follow
 * the page's light/dark theme instead of pinning their own dark palette.
 */
(function () {
    const API_BASE_URL = (() => {
        const host = window.location.hostname;
        if (host.includes('veelearn.org')) return 'https://api.veelearn.org';
        if (host.includes('github.io')) return 'https://veelearn.onrender.com';
        if (host === 'localhost' || host === '127.0.0.1') return 'http://localhost:3000';
        return window.location.origin;
    })();

    const esc = (value) =>
        String(value == null ? '' : value).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);

    async function api(path, body) {
        const token = localStorage.getItem('token') || '';
        const res = await fetch(`${API_BASE_URL}${path}`, {
            method: body ? 'POST' : 'GET',
            headers: Object.assign(
                token ? { Authorization: `Bearer ${token}` } : {},
                body ? { 'Content-Type': 'application/json' } : {}
            ),
            credentials: 'include',
            body: body ? JSON.stringify(body) : undefined
        });
        const payload = await res.json().catch(() => ({}));
        if (!res.ok || payload.success === false) {
            const err = new Error(payload.message || `Something went wrong (${res.status})`);
            err.status = res.status;
            throw err;
        }
        return payload.data;
    }

    // The gem-store theme lives on #learner-shell, but this file's modal and pill
    // hang off <body>. Mirror the attribute so the --ls-* palette reaches them.
    function syncLearnerTheme() {
        const shell = document.getElementById('learner-shell');
        const theme =
            (shell && shell.getAttribute('data-learner-theme')) ||
            (() => {
                try {
                    return localStorage.getItem('learnerDashboardTheme');
                } catch (_) {
                    return null;
                }
            })() ||
            'warm';
        if (document.body.getAttribute('data-learner-theme') !== theme) {
            document.body.setAttribute('data-learner-theme', theme);
        }
    }

    const modal = () => document.getElementById('impact-modal');
    const body = () => document.getElementById('impact-body');
    const title = () => document.getElementById('impact-title');

    function openModal(heading, html) {
        const host = modal();
        if (!host) return;
        syncLearnerTheme();
        if (title()) title().textContent = heading;
        if (body()) body().innerHTML = html;
        host.hidden = false;
        document.body.classList.add('vl-modal-open');
    }

    function closeModal() {
        const host = modal();
        if (!host) return;
        host.hidden = true;
        document.body.classList.remove('vl-modal-open');
        if (body()) body().innerHTML = '';
    }

    // ------------------------------------------------------- creator pane
    function readinessBlock(report) {
        const fixes = (report.checks || []).filter((c) => !c.pass && c.fix);
        return `
      <div class="vl-card">
        <div class="vl-card-head">
          <strong>${esc(report.title)}</strong>
          <span class="vl-chip ${report.passed ? 'vl-good' : 'vl-warn'}">
            ${report.score}% session-ready ${report.passed ? '' : '· bank-led'}
          </span>
        </div>
        <p class="vl-muted vl-small">
          ${report.units.length} unit(s) · ${report.skills.length} skill(s) mapped${
            report.filled.length ? ` · ${report.filled.length} filled from the shared bank` : ''
          }
        </p>
        ${fixes.length ? `<ul class="vl-list vl-warn">${fixes.map((c) => `<li>${esc(c.fix)}</li>`).join('')}</ul>` : '<p class="vl-good vl-small">Every readiness check passes.</p>'}
      </div>`;
    }

    function impactBlock(pane) {
        return `
      <div class="vl-card">
        <strong>${esc(pane.title)}</strong>
        <div class="vl-stats">
          <span><b>${pane.learners}</b> learners taught</span>
          <span><b>${pane.avgGain >= 0 ? '+' : ''}${pane.avgGain}</b> avg mastery gain</span>
          <span><b>${pane.rating || '—'}</b> ★ (${pane.ratingCount})</span>
          <span><b>+${pane.hours}h</b> volunteer hours</span>
        </div>
        <p class="vl-muted vl-small">
          ${pane.paidSessions} paid session(s) · ${pane.refusedSessions} not yet payable
          (${pane.learners < 2 ? 'needs 2 distinct learners before hours pay' : 'gates met'})
        </p>
        ${
            pane.stuck.length
                ? `<p class="vl-small vl-strong">Where your learners get stuck</p>
             <ul class="vl-list vl-warn">
               ${pane.stuck.map((s) => `<li>${esc(s.name)} — ${s.misses}/${s.attempts} misses</li>`).join('')}
             </ul>`
                : '<p class="vl-good vl-small">No repeated misses recorded yet.</p>'
        }
        <p class="vl-faint vl-small">
          Funnel: started ${pane.funnel.started} · 50% ${pane.funnel.half} · 80% ${pane.funnel.eighty} · finished ${pane.funnel.finished}
        </p>
      </div>`;
    }

    async function openTeachingImpact() {
        openModal('Teaching impact', '<p class="vl-muted">Loading your courses…</p>');
        let summary;
        try {
            summary = await api('/api/creator/impact');
        } catch (err) {
            openModal('Teaching impact', `<p class="vl-bad">${esc(err.message)}</p>`);
            return;
        }
        if (!summary.courses.length) {
            openModal('Teaching impact', '<p class="vl-muted">Create a course and sessions on it will show up here.</p>');
            return;
        }

        const parts = [
            `<p class="vl-intro">
               ${summary.courses.length} course(s) · <b>+${summary.hours}h</b> volunteer hours from teaching
             </p>`
        ];
        for (const course of summary.courses) {
            try {
                const [report, pane] = await Promise.all([
                    api(`/api/session/course/${course.courseId}/readiness`),
                    api(`/api/course/${course.courseId}/impact`)
                ]);
                parts.push(readinessBlock(report));
                parts.push(impactBlock(pane));
            } catch (err) {
                parts.push(
                    `<div class="vl-card">
                       <strong>${esc(course.title)}</strong>
                       <p class="vl-bad vl-small">${esc(err.message)}</p>
                     </div>`
                );
            }
        }
        openModal('Teaching impact', parts.join(''));
    }

    // ------------------------------------------------ teacher: assign session
    async function assignSession() {
        const select = document.getElementById('assignment-course-select');
        const minutesEl = document.getElementById('assign-session-minutes');
        const dueEl = document.getElementById('assign-session-due');
        const button = document.getElementById('assign-session-btn');
        const courseId = select && parseInt(select.value, 10);

        if (!courseId) {
            if (button) button.textContent = 'Pick a course above first';
            return;
        }
        const original = button ? button.textContent : '';
        if (button) {
            button.disabled = true;
            button.textContent = 'Assigning…';
        }
        try {
            const created = await api('/api/teacher/assign-session', {
                courseId,
                minutes: parseInt(minutesEl && minutesEl.value, 10) || 20,
                dueAt: (dueEl && dueEl.value) || null
            });
            if (button) button.textContent = `Assigned #${created.id} ✓`;
            await loadTeacherSessions();
        } catch (err) {
            if (button) button.textContent = err.message;
        } finally {
            if (button) {
                button.disabled = false;
                setTimeout(() => {
                    button.textContent = original;
                }, 2600);
            }
        }
    }

    async function loadTeacherSessions() {
        const host = document.getElementById('teacher-session-list');
        if (!host) return;
        try {
            const out = await api('/api/teacher/session-assignments');
            if (!out.count) {
                host.innerHTML = '';
                return;
            }
            host.innerHTML =
                '<p class="vl-muted vl-small vl-tight">Assigned sessions</p>' +
                out.assignments
                    .map(
                        (a) => `<div class="vl-row">
                          <span>${esc(a.course_title || a.title)} · ${a.minutes}m</span>
                          <button type="button" class="secondary-btn vl-mini-btn" data-mastery="${a.id}">Mastery</button>
                        </div>`
                    )
                    .join('');
        } catch (_) {
            host.innerHTML = '';
        }
    }

    async function showMastery(assignmentId) {
        openModal('Per-student mastery', '<p class="vl-muted">Loading…</p>');
        try {
            const out = await api(`/api/teacher/session-assignment/${assignmentId}`);
            const rows = out.students
                .map(
                    (s) => `<tr>
                      <td>${esc(s.email)}</td>
                      <td>${s.mastery}%</td>
                      <td>${s.masteredSkills}/${s.skillsTracked}</td>
                      <td>${s.sessions}</td>
                    </tr>`
                )
                .join('');
            openModal(
                `${out.assignment.title} — mastery`,
                `<table class="vl-table">
                   <thead><tr><th>Student</th><th>Mastery</th><th>Skills mastered</th><th>Sessions</th></tr></thead>
                   <tbody>${rows || '<tr><td colspan="4" class="vl-muted">No students enrolled yet.</td></tr>'}</tbody>
                 </table>`
            );
        } catch (err) {
            openModal('Per-student mastery', `<p class="vl-bad">${esc(err.message)}</p>`);
        }
    }

    // ------------------------------------------- a course opens a session (§15.2)
    function showCourseSessionPill(courseId) {
        let pill = document.getElementById('vl-session-pill');
        if (!pill) {
            pill = document.createElement('div');
            pill.id = 'vl-session-pill';
            pill.className = 'vl-pill';
            pill.innerHTML = `
              <a id="vl-session-pill-go" href="#" class="vl-pill-link">Practice this course with the tutor</a>
              <button type="button" id="vl-session-pill-x" class="vl-pill-x" aria-label="Dismiss">✕</button>`;
            document.body.appendChild(pill);
            pill.querySelector('#vl-session-pill-x').addEventListener('click', () => pill.remove());
        }
        const go = pill.querySelector('#vl-session-pill-go');
        go.href = `session.html?course=${encodeURIComponent(courseId)}&minutes=15`;
    }

    // ------------------------------------------------------------------- wire
    function wire() {
        const impactBtn = document.getElementById('my-impact-btn');
        if (impactBtn) impactBtn.addEventListener('click', openTeachingImpact);

        const close = document.getElementById('impact-close');
        if (close) close.addEventListener('click', closeModal);
        const host = modal();
        if (host) {
            host.addEventListener('click', (e) => {
                if (e.target === host) closeModal();
            });
        }
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && host && !host.hidden) closeModal();
        });

        // The shell and the profile arrive after this script runs, so follow the
        // attribute instead of reading it once.
        syncLearnerTheme();
        [300, 1200, 3000].forEach((ms) => setTimeout(syncLearnerTheme, ms));
        if (window.MutationObserver) {
            const shell = document.getElementById('learner-shell');
            if (shell) {
                new MutationObserver(syncLearnerTheme).observe(shell, {
                    attributes: true,
                    attributeFilter: ['data-learner-theme']
                });
            }
        }

        const assignBtn = document.getElementById('assign-session-btn');
        if (assignBtn) assignBtn.addEventListener('click', assignSession);
        loadTeacherSessions();

        document.addEventListener('click', (e) => {
            const btn = e.target.closest && e.target.closest('[data-mastery]');
            if (btn) showMastery(btn.dataset.mastery);
        });

        document.addEventListener('vee:course-view', (e) => {
            const id = e.detail && e.detail.courseId;
            if (id) setTimeout(() => {
                syncLearnerTheme();
                showCourseSessionPill(id);
            }, 0);
        });
    }

    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', wire);
    else wire();
})();
