/**
 * P4/P5 dashboard surfaces.
 *
 * Kept out of script.js on purpose: this file owns the creator pane (readiness
 * and teaching impact), the teacher's "assign a practice session" flow with
 * per-student mastery, and the entry point from a course into a session. It
 * talks to the same API as the rest of the dashboard and renders into elements
 * index.html already provides.
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

    const modal = () => document.getElementById('impact-modal');
    const body = () => document.getElementById('impact-body');
    const title = () => document.getElementById('impact-title');

    function openModal(heading, html) {
        const host = modal();
        if (!host) return;
        if (title()) title().textContent = heading;
        if (body()) body().innerHTML = html;
        host.hidden = false;
        host.style.display = 'flex';
    }

    function closeModal() {
        const host = modal();
        if (!host) return;
        host.hidden = true;
        host.style.display = 'none';
        if (body()) body().innerHTML = '';
    }

    // ------------------------------------------------------- creator pane
    function readinessBlock(report) {
        const fixes = (report.checks || []).filter((c) => !c.pass && c.fix);
        return `
      <div style="border:1px solid #444;border-radius:8px;padding:14px;margin-bottom:14px;">
        <div style="display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;">
          <strong>${esc(report.title)}</strong>
          <span style="font-size:13px;color:${report.passed ? '#4ade80' : '#fbbf24'}">
            ${report.score}% session-ready ${report.passed ? '' : '· bank-led'}
          </span>
        </div>
        <p style="font-size:13px;color:#aaa;margin:8px 0;">
          ${report.units.length} unit(s) · ${report.skills.length} skill(s) mapped${
            report.filled.length ? ` · ${report.filled.length} filled from the shared bank` : ''
          }
        </p>
        ${fixes.length ? `<ul style="font-size:13px;color:#fbbf24;margin:8px 0 0 18px;">${fixes
            .map((c) => `<li>${esc(c.fix)}</li>`)
            .join('')}</ul>` : '<p style="font-size:13px;color:#4ade80;margin:0;">Every readiness check passes.</p>'}
      </div>`;
    }

    function impactBlock(pane) {
        return `
      <div style="border:1px solid #444;border-radius:8px;padding:14px;margin-bottom:14px;">
        <strong>${esc(pane.title)}</strong>
        <div style="display:flex;gap:18px;flex-wrap:wrap;margin:10px 0;font-size:14px;">
          <span><b>${pane.learners}</b> learners taught</span>
          <span><b>${pane.avgGain >= 0 ? '+' : ''}${pane.avgGain}</b> avg mastery gain</span>
          <span><b>${pane.rating || '—'}</b> ★ (${pane.ratingCount})</span>
          <span><b>+${pane.hours}h</b> volunteer hours</span>
        </div>
        <p style="font-size:13px;color:#aaa;margin:0 0 8px;">
          ${pane.paidSessions} paid session(s) · ${pane.refusedSessions} not yet payable
          (${pane.learners < 2 ? 'needs 2 distinct learners before hours pay' : 'gates met'})
        </p>
        ${
            pane.stuck.length
                ? `<p style="font-size:13px;margin:8px 0 4px;">Where your learners get stuck</p>
             <ul style="font-size:13px;color:#fbbf24;margin:0 0 0 18px;">
               ${pane.stuck.map((s) => `<li>${esc(s.name)} — ${s.misses}/${s.attempts} misses</li>`).join('')}
             </ul>`
                : '<p style="font-size:13px;color:#4ade80;margin:0;">No repeated misses recorded yet.</p>'
        }
        <p style="font-size:12px;color:#888;margin:10px 0 0;">
          Funnel: started ${pane.funnel.started} · 50% ${pane.funnel.half} · 80% ${pane.funnel.eighty} · finished ${pane.funnel.finished}
        </p>
      </div>`;
    }

    async function openTeachingImpact() {
        openModal('Teaching impact', '<p style="color:#aaa;">Loading your courses…</p>');
        let summary;
        try {
            summary = await api('/api/creator/impact');
        } catch (err) {
            openModal('Teaching impact', `<p style="color:#f87171;">${esc(err.message)}</p>`);
            return;
        }
        if (!summary.courses.length) {
            openModal('Teaching impact', '<p style="color:#aaa;">Create a course and sessions on it will show up here.</p>');
            return;
        }

        const parts = [
            `<p style="font-size:14px;color:#ddd;margin:0 0 14px;">
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
                    `<div style="border:1px solid #444;border-radius:8px;padding:14px;margin-bottom:14px;">
                       <strong>${esc(course.title)}</strong>
                       <p style="color:#f87171;font-size:13px;">${esc(err.message)}</p>
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
            host.innerHTML = `<p style="margin:0 0 6px;color:#aaa;">Assigned sessions</p>` +
                out.assignments
                    .map(
                        (a) => `<div style="display:flex;justify-content:space-between;gap:8px;padding:4px 0;border-bottom:1px solid #333;">
                          <span>${esc(a.course_title || a.title)} · ${a.minutes}m</span>
                          <button type="button" class="secondary-btn" data-mastery="${a.id}"
                            style="padding:2px 8px;font-size:12px;color:#1e293b !important;">Mastery</button>
                        </div>`
                    )
                    .join('');
        } catch (_) {
            host.innerHTML = '';
        }
    }

    async function showMastery(assignmentId) {
        openModal('Per-student mastery', '<p style="color:#aaa;">Loading…</p>');
        try {
            const out = await api(`/api/teacher/session-assignment/${assignmentId}`);
            const rows = out.students
                .map(
                    (s) => `<tr>
                      <td style="padding:6px 8px;border-bottom:1px solid #333;">${esc(s.email)}</td>
                      <td style="padding:6px 8px;border-bottom:1px solid #333;">${s.mastery}%</td>
                      <td style="padding:6px 8px;border-bottom:1px solid #333;">${s.masteredSkills}/${s.skillsTracked}</td>
                      <td style="padding:6px 8px;border-bottom:1px solid #333;">${s.sessions}</td>
                    </tr>`
                )
                .join('');
            openModal(
                `${out.assignment.title} — mastery`,
                `<table style="width:100%;border-collapse:collapse;font-size:14px;">
                   <thead><tr style="text-align:left;color:#aaa;">
                     <th style="padding:6px 8px;">Student</th><th style="padding:6px 8px;">Mastery</th>
                     <th style="padding:6px 8px;">Skills mastered</th><th style="padding:6px 8px;">Sessions</th>
                   </tr></thead>
                   <tbody>${rows || '<tr><td colspan="4" style="padding:10px;color:#aaa;">No students enrolled yet.</td></tr>'}</tbody>
                 </table>`
            );
        } catch (err) {
            openModal('Per-student mastery', `<p style="color:#f87171;">${esc(err.message)}</p>`);
        }
    }

    // ------------------------------------------- a course opens a session (§15.2)
    function showCourseSessionPill(courseId) {
        let pill = document.getElementById('vl-session-pill');
        if (!pill) {
            pill = document.createElement('div');
            pill.id = 'vl-session-pill';
            pill.style.cssText =
                'position:fixed;right:18px;bottom:18px;z-index:9000;display:flex;gap:8px;align-items:center;' +
                'background:#1e1e1e;color:#eee;border:1px solid #444;border-radius:999px;padding:8px 10px;' +
                'box-shadow:0 8px 24px rgba(0,0,0,.35);font:13px/1.2 system-ui,sans-serif;';
            pill.innerHTML = `
              <a id="vl-session-pill-go" href="#" style="color:#fb923c;text-decoration:none;font-weight:600;">
                Practice this course with the tutor
              </a>
              <button type="button" id="vl-session-pill-x"
                style="background:none;border:none;color:#888;cursor:pointer;font-size:15px;">✕</button>`;
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

        const assignBtn = document.getElementById('assign-session-btn');
        if (assignBtn) assignBtn.addEventListener('click', assignSession);
        loadTeacherSessions();

        document.addEventListener('click', (e) => {
            const btn = e.target.closest && e.target.closest('[data-mastery]');
            if (btn) showMastery(btn.dataset.mastery);
        });

        document.addEventListener('vee:course-view', (e) => {
            const id = e.detail && e.detail.courseId;
            if (id) setTimeout(() => showCourseSessionPill(id), 0);
        });
    }

    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', wire);
    else wire();
})();
