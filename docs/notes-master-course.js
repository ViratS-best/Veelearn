/**
 * Notes → master course composer (learner dashboard).
 */
(function () {
  const ACCEPT =
    '.pdf,.png,.jpg,.jpeg,.webp,.gif,.doc,.docx,application/pdf,image/png,image/jpeg,image/webp,image/gif,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document';
  const MAX_FILES = 8;
  const MAX_BYTES = 8 * 1024 * 1024;

  /** @type {Array<{ name: string, mime: string, dataBase64: string, size: number }>} */
  let attachments = [];
  let pollTimer = null;
  let activeJobId = null;
  let doneCourseId = null;

  function apiBase() {
    return typeof window.API_BASE_URL === 'string' ? window.API_BASE_URL : '';
  }

  function token() {
    return localStorage.getItem('token') || (typeof window.authToken === 'string' ? window.authToken : '');
  }

  function esc(s) {
    return String(s ?? '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
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
    return res.json().catch(() => ({}));
  }

  function allowedFile(file) {
    const name = (file.name || '').toLowerCase();
    const type = (file.type || '').toLowerCase();
    if (type.startsWith('image/')) return true;
    if (type === 'application/pdf' || name.endsWith('.pdf')) return true;
    if (name.endsWith('.docx') || name.endsWith('.doc')) return true;
    if (type.includes('word')) return true;
    return false;
  }

  function readFile(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(String(reader.result || ''));
      reader.onerror = () => reject(new Error('Could not read file'));
      reader.readAsDataURL(file);
    });
  }

  async function addFiles(fileList) {
    const incoming = Array.from(fileList || []);
    for (const file of incoming) {
      if (attachments.length >= MAX_FILES) break;
      if (!allowedFile(file)) continue;
      if (file.size > MAX_BYTES) continue;
      if (attachments.some((a) => a.name === file.name && a.size === file.size)) continue;
      const dataBase64 = await readFile(file);
      attachments.push({
        name: file.name,
        mime: file.type || '',
        dataBase64,
        size: file.size
      });
    }
    renderChips();
  }

  function renderChips() {
    const el = document.getElementById('ls-notes-chips');
    if (!el) return;
    if (!attachments.length) {
      el.innerHTML = '';
      el.hidden = true;
      return;
    }
    el.hidden = false;
    el.innerHTML = attachments
      .map(
        (a, i) =>
          `<span class="ls-notes-chip">${esc(a.name)} <button type="button" data-notes-remove="${i}" aria-label="Remove">×</button></span>`
      )
      .join('');
    el.querySelectorAll('[data-notes-remove]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const idx = Number(btn.getAttribute('data-notes-remove'));
        attachments.splice(idx, 1);
        renderChips();
      });
    });
  }

  function setMode(mode) {
    const form = document.getElementById('ls-notes-form');
    const progress = document.getElementById('ls-notes-progress');
    const done = document.getElementById('ls-notes-done');
    const err = document.getElementById('ls-notes-error');
    if (form) form.hidden = mode !== 'form';
    if (progress) progress.hidden = mode !== 'progress';
    if (done) done.hidden = mode !== 'done';
    if (err) {
      err.hidden = true;
      err.textContent = '';
    }
  }

  function showError(msg) {
    const err = document.getElementById('ls-notes-error');
    if (!err) return;
    err.hidden = false;
    err.textContent = msg;
  }

  function stopPoll() {
    if (pollTimer) {
      clearInterval(pollTimer);
      pollTimer = null;
    }
  }

  function closeModal() {
    stopPoll();
    document.getElementById('ls-notes-backdrop')?.remove();
  }

  async function pollJob(jobId) {
    const data = await api(`/api/ai/notes-course/${jobId}`);
    const row = data.data || {};
    const stepEl = document.getElementById('ls-notes-step');
    if (stepEl && row.step) stepEl.textContent = row.step;
    if (row.status === 'done' && row.courseId) {
      stopPoll();
      doneCourseId = row.courseId;
      setMode('done');
      window.LearnerShell?.refreshCourseFlyout?.();
      return;
    }
    if (row.status === 'error') {
      stopPoll();
      setMode('form');
      showError(row.error || data.message || 'Generation failed.');
    }
  }

  async function generate() {
    const prompt = document.getElementById('ls-notes-prompt')?.value?.trim() || '';
    const struggles = document.getElementById('ls-notes-struggles')?.value?.trim() || '';
    if (!prompt && !struggles && !attachments.length) {
      showError('Type a topic or attach notes, homework, or images.');
      return;
    }
    const genBtn = document.getElementById('ls-notes-generate');
    if (genBtn) genBtn.disabled = true;
    setMode('progress');
    const stepEl = document.getElementById('ls-notes-step');
    if (stepEl) stepEl.textContent = 'Starting…';
    try {
      const data = await api('/api/ai/notes-course', {
        method: 'POST',
        body: JSON.stringify({
          prompt,
          struggles,
          files: attachments.map((a) => ({
            name: a.name,
            mime: a.mime,
            dataBase64: a.dataBase64
          }))
        })
      });
      if (!data.success || !data.data?.jobId) {
        setMode('form');
        showError(data.message || 'Could not start generation.');
        return;
      }
      activeJobId = data.data.jobId;
      stopPoll();
      pollTimer = setInterval(() => {
        pollJob(activeJobId).catch(() => {});
      }, 2000);
      await pollJob(activeJobId);
    } catch (e) {
      setMode('form');
      showError('Network error — please try again.');
    } finally {
      if (genBtn) genBtn.disabled = false;
    }
  }

  function openCourse() {
    const id = doneCourseId;
    closeModal();
    if (!id) return;
    if (window.LearnerShell?.hideLearnerShell) window.LearnerShell.hideLearnerShell();
    if (typeof window.viewCourse === 'function') {
      window.viewCourse(id);
    }
  }

  function bindDrop(zone) {
    if (!zone) return;
    const on = (e) => {
      e.preventDefault();
      e.stopPropagation();
      zone.classList.add('is-drag');
    };
    const off = (e) => {
      e.preventDefault();
      e.stopPropagation();
      zone.classList.remove('is-drag');
    };
    zone.addEventListener('dragenter', on);
    zone.addEventListener('dragover', on);
    zone.addEventListener('dragleave', off);
    zone.addEventListener('drop', (e) => {
      off(e);
      addFiles(e.dataTransfer?.files).catch(() => {});
    });
  }

  function open() {
    document.getElementById('ls-notes-backdrop')?.remove();
    stopPoll();
    attachments = [];
    doneCourseId = null;
    activeJobId = null;

    const shell = document.getElementById('learner-shell') || document.body;
    const backdrop = document.createElement('div');
    backdrop.className = 'ls-modal-backdrop';
    backdrop.id = 'ls-notes-backdrop';
    backdrop.innerHTML = `
      <div class="ls-notes-modal" role="dialog" aria-labelledby="ls-notes-title">
        <div class="ls-notes-head">
          <h3 id="ls-notes-title">From notes</h3>
          <button type="button" class="ls-notes-x" id="ls-notes-close" aria-label="Close">×</button>
        </div>
        <p class="ls-notes-sub">Attach notes, homework, or past work. Say what you struggle with. We'll build a private master course with units, worked examples, and practice — not the same problems as the examples.</p>
        <div id="ls-notes-form">
          <div class="ls-notes-drop" id="ls-notes-drop">
            <div class="ls-notes-chips" id="ls-notes-chips" hidden></div>
            <textarea id="ls-notes-prompt" maxlength="8000" rows="4" placeholder="What should this course cover? Type extra context, or paste images here…"></textarea>
            <textarea id="ls-notes-struggles" maxlength="4000" rows="2" placeholder="What do you struggle with? (explained in extra depth)"></textarea>
            <div class="ls-notes-bar">
              <button type="button" class="ls-btn-soft ls-notes-plus" id="ls-notes-plus" aria-label="Upload files">+</button>
              <input type="file" id="ls-notes-file" hidden multiple accept="${ACCEPT}" />
              <button type="button" class="ls-btn-primary" id="ls-notes-generate">Generate course</button>
            </div>
          </div>
        </div>
        <div id="ls-notes-progress" hidden>
          <p class="ls-notes-step" id="ls-notes-step">Reading notes…</p>
          <p class="ls-notes-sub">This can take a few minutes. Keep this window open.</p>
        </div>
        <div id="ls-notes-done" hidden>
          <p>Your master course is ready.</p>
          <button type="button" class="ls-btn-primary" id="ls-notes-open">Open course</button>
        </div>
        <p class="ls-notes-error" id="ls-notes-error" hidden></p>
      </div>
    `;
    shell.appendChild(backdrop);

    document.getElementById('ls-notes-close')?.addEventListener('click', closeModal);
    backdrop.addEventListener('click', (e) => {
      if (e.target === backdrop) closeModal();
    });
    document.getElementById('ls-notes-plus')?.addEventListener('click', () => {
      document.getElementById('ls-notes-file')?.click();
    });
    document.getElementById('ls-notes-file')?.addEventListener('change', (e) => {
      addFiles(e.target.files).catch(() => {});
      e.target.value = '';
    });
    document.getElementById('ls-notes-generate')?.addEventListener('click', () => {
      generate();
    });
    document.getElementById('ls-notes-open')?.addEventListener('click', openCourse);
    bindDrop(document.getElementById('ls-notes-drop'));

    const onPaste = (e) => {
      const items = e.clipboardData?.files;
      if (items && items.length) {
        addFiles(items).catch(() => {});
      }
    };
    backdrop.addEventListener('paste', onPaste);
    document.getElementById('ls-notes-prompt')?.addEventListener('paste', onPaste);

    document.getElementById('ls-notes-prompt')?.focus();
  }

  window.NotesMasterCourse = { open, close: closeModal };
})();
