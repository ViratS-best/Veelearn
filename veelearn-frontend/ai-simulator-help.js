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
    if (!Array.isArray(actions)) return;
    stackCursor = null;
    nestParent = null;
    nestInput = null;
    stackX = 40;
    stackY = 40;
    for (const action of actions) {
      const type = action.type;
      const payload = action.payload || {};
      try {
        if (type === 'message') {
          await appendBubble('assistant', payload.text || '');
        } else if (type === 'select_target') {
          studio()?.selectTarget?.(payload.target);
          stackCursor = null;
          nestParent = null;
          await delay(200);
        } else if (type === 'ensure_sprite') {
          studio()?.ensureSprite?.(payload.name || 'Sprite');
          stackCursor = null;
          nestParent = null;
          await delay(250);
        } else if (type === 'set_sprite_props') {
          studio()?.setSpriteProps?.(payload);
          await delay(150);
        } else if (type === 'draw_asset') {
          studio()?.applyDrawnAsset?.(payload);
          await appendBubble('system', `Drew ${payload.kind || 'asset'}: ${payload.name || ''}`);
          await delay(280);
        } else if (type === 'add_block') {
          placeBlock(payload);
          await delay(280);
        } else if (type === 'add_stack') {
          const blocks = payload.blocks || [];
          for (let i = 0; i < blocks.length; i++) {
            const b = { ...blocks[i] };
            if (i === 0) b.newStack = b.newStack != null ? b.newStack : true;
            else b.connectToPrevious = true;
            placeBlock(b);
            await delay(280);
          }
        } else if (type === 'wait_for_user') {
          // Never pause for assets — draw them procedurally
          const need = String(payload.need || 'costume').toLowerCase();
          if (need === 'sound') {
            await appendBubble('system', 'Skipping sound upload — continuing with visuals.');
          } else {
            const drawn = defaultShapesForNeed(need === 'backdrop' ? 'backdrop' : 'costume');
            if (need === 'backdrop') studio()?.selectTarget?.('stage');
            studio()?.applyDrawnAsset?.(drawn);
            await appendBubble('system', `Auto-drew ${drawn.kind} (no upload needed).`);
          }
          await delay(200);
        } else if (type === 'done') {
          await appendBubble('assistant', payload.message || 'Done! Press the green flag to try it.');
          try {
            studio()?.switchTab?.('code');
          } catch (_) { /* ignore */ }
        }
      } catch (err) {
        console.error('sim AI action failed', type, err);
        await appendBubble('error', `Action “${type}” failed: ${err.message || err}`);
      }
    }
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

  async function sendMessage(opts) {
    const options = opts || {};
    if (busy) return;
    const input = document.getElementById('sim-ai-input');
    const sendBtn = document.getElementById('sim-ai-send');
    const text = options.continue
      ? ''
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

    try {
      const { res, data } = await callApi({
        message: text || 'continue',
        continue: !!options.continue,
        lastNeed: options.lastNeed || lastNeed || '',
        projectSummary: summary,
        history: history.slice(-10)
      });

      if (!res.ok || !data || data.success === false) {
        await appendBubble(
          'error',
          (data && data.message) ||
            (res.status === 401
              ? 'Please log in on Veelearn first, then reopen the studio.'
              : `Simulator AI failed (${res.status})`)
        );
        return;
      }

      const reply = data.data?.reply || '';
      const actions = data.data?.actions || [];
      if (reply) {
        await appendBubble('assistant', reply);
        history.push({ role: 'assistant', content: reply });
      }
      await executeActions(actions);
      if (!actions.length && !reply) {
        await appendBubble('assistant', 'No changes suggested.');
      }
    } catch (err) {
      console.error(err);
      await appendBubble('error', 'Could not reach Simulator AI. Check your connection.');
    } finally {
      busy = false;
      if (sendBtn) sendBtn.disabled = false;
      if (waiting) {
        const continueBtn = document.getElementById('sim-ai-continue');
        if (continueBtn) continueBtn.disabled = false;
      }
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
