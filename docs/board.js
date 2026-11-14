/**
 * Board mode.
 *
 * Deliberately not a diagram engine: the 23 presets in widget-engine.js already
 * draw number lines, function plots, shaded areas, geometry and physics scenes.
 * The board mounts one of those in a div.vl-widget-host and writes the worked
 * steps next to it, at a readable 34 characters per second.
 *
 * If the engine is missing, the preset is unknown or the mount fails, the board
 * still opens with the steps — never a blank panel.
 */
(function (global) {
  'use strict';

  const ENGINE_SRC = 'widget-engine.js';
  const TYPE_SPEED = 34; // chars/second, same as the mascot's writing pace

  const SUPPORTED = [
    'number_line',
    'function_plot',
    'area_shade',
    'coordinate_plane',
    'geometry_board',
    'triangle_lab',
    'unit_circle',
    'parametric_plot',
    'inequality_region',
    'projectile'
  ];

  const state = {
    panel: null,
    host: null,
    widget: null,
    typing: null,
    enginePromise: null,
    reduced: false,
    resolveTyping: null
  };

  const prefersReduced = () =>
    typeof global.matchMedia === 'function' && global.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function esc(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function viewType(preset) {
    if (preset === 'function_plot' || preset === 'area_shade' || preset === 'parametric_plot') return 'function';
    if (preset === 'projectile') return 'sim3d';
    return 'geometry';
  }

  function loadEngine() {
    if (global.VeelearnWidgetEngine) return Promise.resolve(global.VeelearnWidgetEngine);
    if (state.enginePromise) return state.enginePromise;

    state.enginePromise = new Promise((resolve, reject) => {
      const existing = document.querySelector(`script[data-board-engine]`);
      if (existing) {
        existing.addEventListener('load', () => resolve(global.VeelearnWidgetEngine));
        existing.addEventListener('error', reject);
        return;
      }
      const script = document.createElement('script');
      script.src = ENGINE_SRC;
      script.async = true;
      script.dataset.boardEngine = '1';
      script.onload = () => resolve(global.VeelearnWidgetEngine);
      script.onerror = () => reject(new Error('widget engine unavailable'));
      document.head.appendChild(script);
    }).catch((err) => {
      state.enginePromise = null;
      throw err;
    });

    return state.enginePromise;
  }

  function ensurePanel() {
    if (state.panel && document.body.contains(state.panel)) return state.panel;

    const stage = document.querySelector('.sx-stage') || document.body;
    const panel = document.createElement('section');
    panel.className = 'sx-board';
    panel.id = 'board';
    panel.setAttribute('data-annotate', 'board');
    panel.setAttribute('role', 'region');
    panel.setAttribute('aria-label', 'Worked example board');
    panel.innerHTML = `
      <header class="sx-board-head">
        <h2 class="sx-board-title">On the board</h2>
        <button type="button" class="sx-ghost sx-board-close" id="sx-board-close">Close board</button>
      </header>
      <div class="sx-board-body">
        <div class="sx-board-canvas" hidden></div>
        <ol class="sx-board-steps"></ol>
      </div>
      <p class="sx-board-note" hidden></p>
    `;
    stage.appendChild(panel);
    state.panel = panel;

    panel.querySelector('#sx-board-close').addEventListener('click', () => api.close());
    panel.addEventListener('click', (e) => {
      if (e.target.closest && e.target.closest('#sx-board-close')) return;
      api.skip();
    });

    return panel;
  }

  function typeSteps(list, steps) {
    const container = list;
    container.innerHTML = '';
    state.reduced = prefersReduced();

    const items = steps.map((step) => {
      const li = document.createElement('li');
      const text = document.createElement('span');
      text.textContent = state.reduced ? step : '';
      li.appendChild(text);
      container.appendChild(li);
      return { li, text, step };
    });

    if (state.reduced) return Promise.resolve();

    return new Promise((resolve) => {
      let index = 0;
      let char = 0;
      state.resolveTyping = () => {
        items.forEach(({ text, step }) => {
          text.textContent = step;
        });
        resolve();
      };
      const timer = setInterval(() => {
        if (index >= items.length) {
          clearInterval(timer);
          state.typing = null;
          resolve();
          return;
        }
        const current = items[index];
        char += 2; // ~2 chars per 60 ms tick ≈ 34/s
        current.text.textContent = current.step.slice(0, char);
        if (char >= current.step.length) {
          current.text.textContent = current.step;
          index += 1;
          char = 0;
          current.li.classList.add('is-written');
        }
      }, 60);
      state.typing = timer;
    });
  }

  function skip() {
    if (state.typing) {
      clearInterval(state.typing);
      state.typing = null;
    }
    if (state.resolveTyping) {
      const fn = state.resolveTyping;
      state.resolveTyping = null;
      fn();
    }
  }

  async function mountPreset(canvas, preset, params) {
    if (!preset || !SUPPORTED.includes(preset)) return false;
    try {
      const engine = await loadEngine();
      if (!engine || typeof engine.mountWidget !== 'function') return false;
      const spec = {
        id: 'session-board-widget',
        title: 'Board diagram',
        objective: '',
        view: { type: viewType(preset), width: 520, height: 300 },
        state: {},
        inputs: [],
        outputs: [],
        behavior: { preset, params: params || {} }
      };
      state.widget = await engine.mountWidget(canvas, spec, { skipDrawing: true });
      return true;
    } catch (_) {
      return false;
    }
  }

  /**
   * @param {{title?:string, steps?:string[], preset?:string, params?:object}} payload
   */
  async function open(payload) {
    const data = payload || {};
    const steps = (Array.isArray(data.steps) ? data.steps : []).map((s) => String(s)).filter(Boolean);
    const panel = ensurePanel();

    panel.querySelector('.sx-board-title').textContent = data.title || 'On the board';
    const canvas = panel.querySelector('.sx-board-canvas');
    const note = panel.querySelector('.sx-board-note');
    const list = panel.querySelector('.sx-board-steps');

    panel.hidden = false;
    panel.classList.add('is-open');
    requestAnimationFrame(() => panel.classList.add('is-in'));

    if (state.widget && typeof state.widget.destroy === 'function') {
      try {
        state.widget.destroy();
      } catch (_) {
        /* widget already gone */
      }
      state.widget = null;
    }
    canvas.innerHTML = '';
    canvas.hidden = true;
    note.hidden = true;

    if (data.preset) {
      canvas.hidden = false;
      const mounted = await mountPreset(canvas, data.preset, data.params);
      if (!mounted) {
        canvas.hidden = true;
        canvas.innerHTML = '';
        note.textContent = 'The diagram could not load, so this is the written method.';
        note.hidden = false;
      }
    }

    if (global.Mascot && global.Mascot.writing) global.Mascot.writing(true);
    await typeSteps(list, steps);
    if (global.Mascot && global.Mascot.writing) global.Mascot.writing(false);

    const closeBtn = panel.querySelector('#sx-board-close');
    if (closeBtn) closeBtn.focus({ preventScroll: true });

    return { ok: true, preset: data.preset || null, steps: steps.length };
  }

  function close() {
    skip();
    if (state.widget && typeof state.widget.destroy === 'function') {
      try {
        state.widget.destroy();
      } catch (_) {
        /* ignore */
      }
      state.widget = null;
    }
    if (state.panel) {
      state.panel.classList.remove('is-in', 'is-open');
      state.panel.hidden = true;
    }
    return { ok: true };
  }

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && state.panel && !state.panel.hidden) api.close();
  });

  const api = {
    open,
    close,
    skip,
    supported: SUPPORTED,
    isOpen: () => !!(state.panel && !state.panel.hidden),
    viewType
  };

  global.Board = api;
})(window);
