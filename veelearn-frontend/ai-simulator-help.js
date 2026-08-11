/**
 * Simulator Studio AI — chat panel, block-by-block executor, wait_for_user gates.
 */
(function (global) {
  'use strict';

  const API_BASE_URL = (() => {
    if (typeof location === 'undefined') return 'http://localhost:3000';
    if (location.hostname.includes('veelearn.org')) return 'https://api.veelearn.org';
    if (location.hostname.includes('github.io')) return 'https://veelearn.onrender.com';
    if (location.hostname === 'localhost' || location.hostname === '127.0.0.1') return 'http://localhost:3000';
    return location.origin;
  })();

  let busy = false;
  let waiting = false;
  let waitResolve = null;
  let lastNeed = null;
  let stackCursor = null;
  let nestParent = null;
  let nestInput = null;
  let history = [];
  let stackX = 40;
  let stackY = 40;

  function studio() {
    return global.ScratchStudio || null;
  }

  function delay(ms) {
    if (global.VeelearnTypewriter && global.VeelearnTypewriter.delay) {
      return global.VeelearnTypewriter.delay(ms);
    }
    return new Promise((r) => setTimeout(r, ms));
  }

  function isDoubleSlitLike(text) {
    return /double[\s-]?slit|interference|wavelength|wave[\s-]?function/i.test(String(text || ''));
  }

  function setWaitUi(active, message) {
    waiting = !!active;
    const banner = document.getElementById('sim-ai-wait-banner');
    const continueBtn = document.getElementById('sim-ai-continue');
    const sendBtn = document.getElementById('sim-ai-send');
    if (banner) {
      banner.hidden = !active;
      banner.textContent = message || 'Waiting for you…';
    }
    if (continueBtn) continueBtn.disabled = !active;
    if (sendBtn) sendBtn.disabled = busy && !active ? true : busy;
  }

  async function appendBubble(role, text, opts) {
    const box = document.getElementById('sim-ai-messages');
    if (!box) return null;
    const options = opts || {};
    const wrap = document.createElement('div');
    wrap.className = 'sim-ai-bubble sim-ai-' + role;
    const label = document.createElement('strong');
    label.textContent = role === 'user' ? 'You' : role === 'system' ? 'Studio' : 'AI';
    const body = document.createElement('div');
    body.className = 'sim-ai-body';
    wrap.appendChild(label);
    wrap.appendChild(body);
    box.appendChild(wrap);
    box.scrollTop = box.scrollHeight;

    const instant = !!options.instant || role === 'user' || role === 'error';
    if (instant || !global.VeelearnTypewriter) {
      body.textContent = text == null ? '' : String(text);
    } else {
      await global.VeelearnTypewriter.typeIntoElement(body, text, {
        scrollParent: box,
        msPerChar:
          role === 'system'
            ? global.VeelearnTypewriter.FAST_MS_PER_CHAR
            : global.VeelearnTypewriter.DEFAULT_MS_PER_CHAR
      });
    }
    return wrap;
  }

  function authHeaders() {
    const token = localStorage.getItem('token') || '';
    return {
      'Content-Type': 'application/json',
      Authorization: token ? `Bearer ${token}` : ''
    };
  }

  function attachShadowValue(parentBlock, inputName, value, asText) {
    if (!parentBlock || !inputName || value == null) return;
    const input = parentBlock.getInput(inputName);
    if (!input || !input.connection) return;

    const ws = studio()?.getWorkspace?.();
    if (!ws) return;

    let shadowType = asText ? 'text' : 'math_number';
    if (inputName === 'BROADCAST_INPUT') shadowType = 'text_broadcast';
    if (inputName === 'MESSAGE' || inputName === 'QUESTION' || inputName === 'COSTUME' || inputName === 'BACKDROP' || inputName === 'SOUND_MENU') {
      shadowType = 'text';
    }

    try {
      const shadow = ws.newBlock(shadowType);
      if (shadowType === 'math_number') {
        shadow.setFieldValue(String(value), 'NUM');
      } else {
        shadow.setFieldValue(String(value), 'TEXT');
      }
      shadow.setShadow(true);
      shadow.initSvg();
      shadow.render();
      input.connection.connect(shadow.outputConnection);
    } catch (e) {
      console.warn('shadow attach failed', inputName, e);
    }
  }

  function emptyStatementInput(block) {
    if (!block || !block.getInput) return null;
    for (const name of ['SUBSTACK', 'SUBSTACK2']) {
      const input = block.getInput(name);
      if (input && input.connection && !input.connection.targetBlock()) return name;
    }
    return null;
  }

  function placeBlock(payload) {
    const st = studio();
    const ws = st?.getWorkspace?.();
    if (!ws || typeof Blockly === 'undefined') throw new Error('Workspace not ready');

    const type = payload.type;
    const block = ws.newBlock(type);

    const fields = payload.fields || {};
    for (const [fname, fval] of Object.entries(fields)) {
      try {
        if (fname === 'VARIABLE' || fname === 'CLONE_OPTION') {
          const name = String(fval || '').trim();
          if (name && fname === 'VARIABLE') {
            try {
              ws.createVariable(name);
            } catch (_) { /* already exists */ }
            try {
              const proj = typeof st?.getProject === 'function' ? st.getProject() : null;
              if (proj?.globals?.variables && proj.globals.variables[name] == null) {
                proj.globals.variables[name] = 0;
              }
            } catch (_) { /* ignore */ }
          }
        }
        if (block.getField(fname)) block.setFieldValue(String(fval), fname);
      } catch (_) { /* ignore */ }
    }

    const inputs = payload.inputs || {};
    for (const [iname, ival] of Object.entries(inputs)) {
      const asText = typeof ival === 'string' && Number.isNaN(Number(ival));
      attachShadowValue(block, iname, ival, asText || typeof ival === 'string');
    }

    block.initSvg();
    block.render();

    const isHat = !block.previousConnection;
    const newStack = !!payload.newStack || isHat;
    let into = payload.into || null;

    // Auto-nest into empty C-block SUBSTACK when AI forgets "into"
    if (
      !into &&
      !newStack &&
      block.previousConnection &&
      nestParent &&
      emptyStatementInput(nestParent) &&
      (!stackCursor || !stackCursor.nextConnection || stackCursor === nestParent)
    ) {
      into = emptyStatementInput(nestParent);
    }

    let connected = false;
    if (into && nestParent && nestParent.getInput(into)) {
      const conn = nestParent.getInput(into).connection;
      if (conn && block.previousConnection) {
        try {
          conn.connect(block.previousConnection);
          connected = true;
        } catch (_) { /* ignore */ }
      }
    }

    if (!connected && !newStack && payload.connectToPrevious !== false && stackCursor && stackCursor.nextConnection && block.previousConnection) {
      try {
        stackCursor.nextConnection.connect(block.previousConnection);
        connected = true;
      } catch (_) { /* ignore */ }
    }

    // If still not connected but nestParent has empty substack, force nest
    if (!connected && !newStack && block.previousConnection && nestParent) {
      const empty = emptyStatementInput(nestParent);
      if (empty) {
        try {
          nestParent.getInput(empty).connection.connect(block.previousConnection);
          connected = true;
          into = empty;
        } catch (_) { /* ignore */ }
      }
    }

    if (!connected) {
      block.moveBy(stackX, stackY);
      stackY += 28;
      if (stackY > 280) {
        stackY = 40;
        stackX += 280;
      }
    }

    // C-blocks become the nest parent for following statements
    if (block.getInput && (block.getInput('SUBSTACK') || block.getInput('SUBSTACK2'))) {
      nestParent = block;
    } else if (into && nestParent) {
      // stay nested under same C-block; stackCursor advances for chaining inside
    }

    if (block.nextConnection || block.previousConnection || isHat) {
      stackCursor = block;
    }

    try {
      ws.scrollCenter();
    } catch (_) { /* ignore */ }

    return block;
  }

  function defaultShapesForNeed(need) {
    if (need === 'backdrop') {
      return {
        kind: 'backdrop',
        name: 'lab',
        bg: '#0f172a',
        shapes: [
          { shape: 'rect', x: 0, y: 0, w: 480, h: 360, fill: '#0f172a' },
          { shape: 'rect', x: 40, y: 280, w: 400, h: 50, fill: '#57534e' },
          { shape: 'rect', x: 80, y: 200, w: 320, h: 16, fill: '#78716c' },
          { shape: 'circle', x: 100, y: 48, r: 5, fill: '#f8fafc' },
          { shape: 'circle', x: 160, y: 48, r: 5, fill: '#f8fafc' },
          { shape: 'circle', x: 220, y: 48, r: 5, fill: '#f8fafc' },
          { shape: 'circle', x: 280, y: 48, r: 5, fill: '#f8fafc' },
          { shape: 'circle', x: 340, y: 48, r: 5, fill: '#f8fafc' }
        ]
      };
    }
    return {
      kind: 'costume',
      name: 'blob',
      shapes: [
        { shape: 'sphere', x: 64, y: 64, r: 36, fill: '#38bdf8', highlight: '#e0f2fe', shade: '#0c4a6e' }
      ]
    };
  }

  async function executeActions(actions) {
    if (!Array.isArray(actions)) return { ok: 0, fail: 0 };
    stackCursor = null;
    nestParent = null;
    nestInput = null;
    stackX = 40;
    stackY = 40;
    let ok = 0;
    let fail = 0;
    const total = actions.length;
    await appendBubble('system', `Applying ${total} action${total === 1 ? '' : 's'}…`, { instant: true });

    for (let i = 0; i < actions.length; i++) {
      const action = actions[i];
      const type = action.type;
      const payload = action.payload || {};
      try {
        if (type === 'message') {
          await appendBubble('assistant', payload.text || '');
        } else if (type === 'select_target') {
          studio()?.selectTarget?.(payload.target);
          stackCursor = null;
          nestParent = null;
          await delay(120);
        } else if (type === 'ensure_sprite') {
          studio()?.ensureSprite?.(payload.name || 'Sprite');
          stackCursor = null;
          nestParent = null;
          await appendBubble('system', `Sprite: ${payload.name || 'Sprite'}`, { instant: true });
          await delay(150);
        } else if (type === 'set_sprite_props') {
          studio()?.setSpriteProps?.(payload);
          await delay(80);
        } else if (type === 'draw_asset') {
          if (typeof studio()?.applyDrawnAsset !== 'function') {
            throw new Error('applyDrawnAsset missing — hard-refresh the studio');
          }
          studio().applyDrawnAsset(payload);
          await appendBubble('system', `Drew ${payload.kind || 'asset'}: ${payload.name || ''}`, {
            instant: true
          });
          await delay(160);
        } else if (type === 'add_block') {
          const ws = studio()?.getWorkspace?.();
          if (!ws) throw new Error('Blockly workspace not ready');
          placeBlock(payload);
          if (i === 0 || i === total - 1 || (i + 1) % 4 === 0) {
            await appendBubble('system', `Blocks ${i + 1}/${total}: ${payload.type}`, { instant: true });
          }
          await delay(180);
        } else if (type === 'add_stack') {
          const blocks = payload.blocks || [];
          for (let j = 0; j < blocks.length; j++) {
            const b = { ...blocks[j] };
            if (j === 0) b.newStack = b.newStack != null ? b.newStack : true;
            else b.connectToPrevious = true;
            placeBlock(b);
            await delay(180);
          }
        } else if (type === 'wait_for_user') {
          const need = String(payload.need || 'costume').toLowerCase();
          if (need === 'sound') {
            await appendBubble('system', 'Skipping sound upload — continuing with visuals.', {
              instant: true
            });
          } else {
            const drawn = defaultShapesForNeed(need === 'backdrop' ? 'backdrop' : 'costume');
            if (need === 'backdrop') studio()?.selectTarget?.('stage');
            studio()?.applyDrawnAsset?.(drawn);
            await appendBubble('system', `Auto-drew ${drawn.kind} (no upload needed).`, {
              instant: true
            });
          }
          await delay(120);
        } else if (type === 'done') {
          await appendBubble('assistant', payload.message || 'Done! Press the green flag to try it.');
          try {
            studio()?.switchTab?.('code');
          } catch (_) { /* ignore */ }
        } else {
          await appendBubble('system', `Skipped unknown action: ${type}`, { instant: true });
        }
        ok++;
      } catch (err) {
        fail++;
        console.error('sim AI action failed', type, err);
        await appendBubble('error', `Action ${i + 1}/${total} “${type}” failed: ${err.message || err}`);
      }
    }
    await appendBubble(
      'system',
      fail ? `Finished with ${ok} ok, ${fail} failed.` : `Finished applying ${ok} actions.`,
      { instant: true }
    );
    return { ok, fail };
  }

  function resumeWait(source) {
    // Asset waits are auto-drawn now; Continue asks the AI to keep building.
    if (waiting) {
      waiting = false;
      setWaitUi(false);
    }
    if (waitResolve) {
      const resolve = waitResolve;
      waitResolve = null;
      resolve({ source: source || 'continue' });
    }
  }

  async function callApi(body) {
    const res = await fetch(`${API_BASE_URL}/api/ai/simulator-help`, {
      method: 'POST',
      credentials: 'include',
      headers: authHeaders(),
      body: JSON.stringify(body)
    });
    let data = null;
    try {
      data = await res.json();
    } catch (_) {
      data = null;
    }
    return { res, data };
  }

  /**
   * Realtime SSE stream from /api/ai/simulator-help/stream.
   * Falls back to non-stream callApi if stream endpoint is unavailable.
   */
  async function callApiStream(body, onToken) {
    const res = await fetch(`${API_BASE_URL}/api/ai/simulator-help/stream`, {
      method: 'POST',
      credentials: 'include',
      headers: authHeaders(),
      body: JSON.stringify(body)
    });

    const ct = (res.headers.get('content-type') || '').toLowerCase();
    if (!res.ok || !res.body || !ct.includes('text/event-stream')) {
      // Older deploy / HTML error page — fall back
      if (ct.includes('application/json')) {
        let data = null;
        try {
          data = await res.json();
        } catch (_) {
          data = null;
        }
        return { ok: false, status: res.status, data, result: null, streamed: false };
      }
      const fallback = await callApi(body);
      return {
        ok: fallback.res.ok && fallback.data && fallback.data.success !== false,
        status: fallback.res.status,
        data: fallback.data,
        result: fallback.data?.data || null,
        streamed: false,
        errorMessage:
          (fallback.data && fallback.data.message) ||
          (fallback.res.status === 401
            ? 'Please log in on Veelearn first, then reopen the studio.'
            : null)
      };
    }

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';
    let result = null;
    let errorMessage = null;
    let errorStatus = res.status;

    const handleEvent = (eventName, dataStr) => {
      let payload = null;
      try {
        payload = JSON.parse(dataStr);
      } catch (_) {
        return;
      }
      if (eventName === 'token' && payload && typeof payload.text === 'string') {
        if (typeof onToken === 'function') onToken(payload.text);
      } else if (eventName === 'result' && payload) {
        result = payload;
      } else if (eventName === 'error' && payload) {
        errorMessage = payload.message || 'AI stream error';
        errorStatus = payload.status || errorStatus;
      }
    };

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const parts = buffer.split('\n\n');
      buffer = parts.pop() || '';
      for (const part of parts) {
        if (!part.trim() || part.trim().startsWith(':')) continue;
        let eventName = 'message';
        const dataLines = [];
        for (const line of part.split('\n')) {
          if (line.startsWith('event:')) eventName = line.slice(6).trim();
          else if (line.startsWith('data:')) dataLines.push(line.slice(5).trim());
        }
        if (dataLines.length) handleEvent(eventName, dataLines.join('\n'));
      }
    }

    return {
      ok: !errorMessage && !!result,
      status: errorStatus,
      data: result ? { success: true, data: result } : { success: false, message: errorMessage },
      result,
      streamed: true,
      errorMessage
    };
  }

  async function sendMessage(opts) {
    const options = opts || {};
    if (busy) return;
    const input = document.getElementById('sim-ai-input');
    const sendBtn = document.getElementById('sim-ai-send');
    const text = options.continue
      ? String(options.message || '').trim()
      : (options.message != null ? options.message : (input && input.value) || '').trim();

    if (!options.continue && !text) return;

    busy = true;
    if (sendBtn) sendBtn.disabled = true;
    if (!options.continue) {
      await appendBubble('user', text);
      if (input) input.value = '';
      history.push({ role: 'user', content: text });
    }

    const summary =
      typeof studio()?.getProjectSummary === 'function' ? studio().getProjectSummary() : '';

    // Live streaming bubble — tokens appear as the model generates them
    const liveWrap = await appendBubble('assistant', '', { instant: true });
    const liveBody = liveWrap && liveWrap.querySelector('.sim-ai-body');
    const msgBox = document.getElementById('sim-ai-messages');
    if (liveBody) liveBody.textContent = '…';

    let autoContinuePrompt = null;

    try {
      let sawToken = false;
      const userPrompt =
        text ||
        (history.slice().reverse().find((h) => h.role === 'user') || {}).content ||
        'continue';
      const streamOut = await callApiStream(
        {
          message: userPrompt,
          continue: !!options.continue,
          lastNeed: options.lastNeed || lastNeed || '',
          projectSummary: summary,
          history: history.slice(-10)
        },
        (token) => {
          if (!liveBody) return;
          if (!sawToken) {
            liveBody.textContent = '';
            sawToken = true;
          }
          liveBody.textContent += token;
          if (msgBox) msgBox.scrollTop = msgBox.scrollHeight;
        }
      );

      if (!streamOut.ok || !streamOut.result) {
        const msg =
          streamOut.errorMessage ||
          streamOut.data?.message ||
          (streamOut.status === 401
            ? 'Please log in on Veelearn first, then reopen the studio.'
            : `Simulator AI failed (${streamOut.status})`);
        if (liveBody) liveBody.textContent = msg;
        liveWrap.classList.add('sim-ai-error');
        return;
      }

      const reply = streamOut.result.reply || '';
      let actions = Array.isArray(streamOut.result.actions) ? streamOut.result.actions : [];
      const actionCount =
        streamOut.result.actionCount != null ? streamOut.result.actionCount : actions.length;
      const usedFallback = !!streamOut.result.usedFallback;

      console.log('[Studio AI]', {
        status: streamOut.status,
        streamed: streamOut.streamed,
        actionCount,
        usedFallback,
        salvaged: !!streamOut.result.salvaged,
        needsContinue: !!streamOut.result.needsContinue,
        replyPreview: String(reply).slice(0, 120),
        rawPreview: streamOut.result.rawPreview
      });

      if (liveBody) {
        const current = (liveBody.textContent || '').trim();
        if (reply && (!sawToken || current.length < 8 || current === '…')) {
          liveBody.textContent = reply;
        } else if (reply && current && !current.includes(reply.slice(0, Math.min(20, reply.length)))) {
          liveBody.textContent = (current + '\n' + reply).trim();
        }
      }

      if (reply) {
        history.push({ role: 'assistant', content: reply });
      }

      if (!actions.length) {
        await appendBubble(
          'error',
          'No build actions came back from the server. Check console for [Studio AI] logs, then try Continue.'
        );
        return;
      }

      if (usedFallback) {
        await appendBubble(
          'system',
          isDoubleSlitLike(userPrompt)
            ? 'Model JSON was incomplete — applied a fuller double-slit lab template instead of a tiny bounce demo.'
            : 'Model skipped JSON actions — using a guaranteed starter build.',
          { instant: true }
        );
      } else if (streamOut.result.salvaged) {
        await appendBubble(
          'system',
          'Model output was truncated — recovered complete actions and applying those.',
          { instant: true }
        );
      }

      await appendBubble('system', `Received ${actions.length} actions.`, { instant: true });
      const result = await executeActions(actions);
      if (result && result.ok === 0) {
        await appendBubble(
          'error',
          'Actions were received but none applied. Hard-refresh the studio (Ctrl+Shift+R) and try again.'
        );
        return;
      }

      if (streamOut.result.needsContinue && !options.continue && !options._autoContinued) {
        autoContinuePrompt = userPrompt;
        await appendBubble(
          'system',
          'Continuing automatically with scripts/controls (phase 2)…',
          { instant: true }
        );
      }
    } catch (err) {
      console.error('[Studio AI] network/error', err);
      if (liveBody) {
        liveBody.textContent = 'Could not reach Simulator AI. Check your connection.';
        liveWrap.classList.add('sim-ai-error');
      } else {
        await appendBubble('error', 'Could not reach Simulator AI. Check your connection.');
      }
    } finally {
      busy = false;
      if (sendBtn) sendBtn.disabled = false;
      if (waiting) {
        const continueBtn = document.getElementById('sim-ai-continue');
        if (continueBtn) continueBtn.disabled = false;
      }
    }

    if (autoContinuePrompt) {
      await delay(400);
      await sendMessage({
        continue: true,
        lastNeed: 'phase2',
        message: autoContinuePrompt,
        _autoContinued: true
      });
    }
  }

  function togglePanel(force) {
    const main = document.querySelector('.main');
    const panel = document.getElementById('sim-ai-panel');
    const btn = document.getElementById('sim-ai-toggle');
    if (!main || !panel) return;
    const currentlyOpen = !main.classList.contains('ai-collapsed');
    const open = force != null ? force : !currentlyOpen;
    main.classList.toggle('ai-collapsed', !open);
    if (btn) btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    try {
      const ws = studio()?.getWorkspace?.();
      if (ws && typeof Blockly !== 'undefined') {
        setTimeout(() => Blockly.svgResize(ws), 50);
      }
    } catch (_) { /* ignore */ }
  }

  function setup() {
    const sendBtn = document.getElementById('sim-ai-send');
    const input = document.getElementById('sim-ai-input');
    const continueBtn = document.getElementById('sim-ai-continue');
    const toggle = document.getElementById('sim-ai-toggle');
    const collapse = document.getElementById('sim-ai-collapse');

    if (sendBtn) {
      sendBtn.addEventListener('click', (e) => {
        e.preventDefault();
        sendMessage();
      });
    }
    if (input) {
      input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          sendMessage();
        }
      });
    }
    if (continueBtn) {
      continueBtn.addEventListener('click', async (e) => {
        e.preventDefault();
        if (waiting) {
          resumeWait('continue');
        } else {
          await sendMessage({ continue: true, lastNeed });
        }
      });
    }
    if (toggle) {
      toggle.addEventListener('click', (e) => {
        e.preventDefault();
        togglePanel();
      });
    }
    if (collapse) {
      collapse.addEventListener('click', (e) => {
        e.preventDefault();
        togglePanel(false);
      });
    }

    window.addEventListener('veelearn-asset-added', (e) => {
      const kind = e.detail?.kind;
      if (!waiting || !lastNeed) return;
      if (kind === lastNeed || (lastNeed === 'costume' && kind === 'costume') || (lastNeed === 'backdrop' && kind === 'backdrop')) {
        resumeWait('asset');
      }
    });

    appendBubble(
      'assistant',
      'Describe a simulation and I’ll build it fully — draw costumes/backdrops from shapes and wire complete block stacks. No uploads needed.',
      { instant: true }
    );
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setup);
  } else {
    setup();
  }

  global.VeelearnSimulatorAI = { sendMessage, resumeWait, togglePanel };
})(typeof window !== 'undefined' ? window : globalThis);
