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

  const ENGINE_SRC = 'widget-engine.js?v=4';
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
    frame: null,
    controls: null,
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
        <div class="sx-board-controls" hidden></div>
        <ol class="sx-board-steps"></ol>
      </div>
      <p class="sx-board-note" hidden></p>
    `;
    stage.appendChild(panel);
    state.panel = panel;

    panel.querySelector('#sx-board-close').addEventListener('click', () => api.close());
    panel.addEventListener('click', (e) => {
      if (e.target.closest && e.target.closest('#sx-board-close')) return;
      // A slider drag or a click inside the scene is input, not "skip the typing".
      if (e.target.closest && e.target.closest('input, iframe, .sx-board-controls')) return;
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

  /**
   * A drawing the student cannot touch is a picture. Each quick-draw preset gets
   * one control the learner can move, and the same state can be dragged on the
   * board itself (the point on the line, the point on the circle).
   */
  const INTERACTIVE = {
    number_line: {
      objective: 'Drag the point, or slide it — the readout follows.',
      state: { point: 2 },
      inputs: [
        { key: 'point', label: 'Point on the line', type: 'slider', min: -10, max: 10, step: 0.1 }
      ],
      outputs: [{ key: 'point', label: 'position' }]
    },
    unit_circle: {
      objective: 'Drag the point around the circle, or set the angle.',
      state: { angle: 45 },
      inputs: [{ key: 'angle', label: 'Angle (degrees)', type: 'slider', min: 0, max: 360, step: 1 }],
      outputs: [{ key: 'angle', label: 'angle' }]
    },
    function_plot: {
      objective: 'Change a and watch the curve bend.',
      state: { a: 1 },
      inputs: [{ key: 'a', label: 'a in y = a·x²', type: 'slider', min: -2, max: 2, step: 0.1 }],
      outputs: [{ key: 'a', label: 'a' }]
    }
  };

  const NUDGE = {
    number_line: { key: 'point', step: 0.1, min: -10, max: 10 },
    unit_circle: { key: 'angle', step: 15, min: 0, max: 360 },
    function_plot: { key: 'a', step: 0.1, min: -2, max: 2 }
  };

  /** Tap-friendly step buttons, for touch screens and for anyone who dislikes sliders. */
  function addNudges(canvas, widget, preset) {
    const cfg = NUDGE[preset];
    if (!cfg || !widget || !widget.state) return;
    const controls = canvas.querySelector('.vl-widget-controls');
    if (!controls) return;
    const row = document.createElement('div');
    row.className = 'vl-widget-control-row sx-board-nudge';
    const label = document.createElement('label');
    label.textContent = 'Step it';
    const sync = () => {
      const slider = controls.querySelector('input[type="range"]');
      if (!slider) return;
      slider.value = String(widget.state[cfg.key]);
      const val = slider.parentElement && slider.parentElement.querySelector('.vl-widget-val');
      if (val) val.textContent = slider.value;
    };
    const bump = (dir) => {
      const next = Number(widget.state[cfg.key]) + dir * cfg.step;
      widget.state[cfg.key] = Math.round(Math.min(cfg.max, Math.max(cfg.min, next)) * 100) / 100;
      sync();
      widget.update();
    };
    [['◀', -1, 'Move back'], ['▶', 1, 'Move forward']].forEach(([glyph, dir, aria]) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'sx-nudge';
      btn.textContent = glyph;
      btn.setAttribute('aria-label', aria);
      btn.addEventListener('click', () => bump(dir));
      row.appendChild(btn);
    });
    row.appendChild(label);
    controls.appendChild(row);
  }

  async function mountPreset(canvas, preset, params) {
    if (!preset || !SUPPORTED.includes(preset)) return false;
    try {
      const engine = await loadEngine();
      if (!engine || typeof engine.mountWidget !== 'function') return false;
      const extra = INTERACTIVE[preset] || { objective: '', state: {}, inputs: [], outputs: [] };
      const merged = Object.assign({}, params || {});
      if (preset === 'function_plot' && !(merged.expressions || []).length) {
        merged.expressions = ['a*x^2'];
      }
      const spec = {
        id: 'session-board-widget',
        title: 'Board diagram',
        objective: extra.objective,
        view: { type: viewType(preset), width: 520, height: 240 },
        state: Object.assign({}, extra.state),
        inputs: extra.inputs,
        outputs: extra.outputs,
        behavior: { preset, params: merged }
      };
      state.widget = await engine.mountWidget(canvas, spec, { skipDrawing: true });
      addNudges(canvas, state.widget, preset);
      return true;
    } catch (_) {
      return false;
    }
  }

  /** Remove whatever is mounted (widget or sandboxed scene) without touching the steps. */
  function clearScene() {
    if (state.widget && typeof state.widget.destroy === 'function') {
      try {
        state.widget.destroy();
      } catch (_) {
        /* widget already gone */
      }
    }
    state.widget = null;
    if (state.frame && state.frame.parentNode) state.frame.parentNode.removeChild(state.frame);
    state.frame = null;
    state.controls = null;
    if (state.panel) {
      const controls = state.panel.querySelector('.sx-board-controls');
      if (controls) {
        controls.innerHTML = '';
        controls.hidden = true;
      }
    }
  }

  /**
   * The scene document. The model's code is untrusted: it runs in an iframe with
   * `sandbox="allow-scripts"` (opaque origin, no parent access), and its own CSP
   * allows inline script and nothing else — no network, no images, no frames.
   */
  function sceneDocument(code, initial) {
    const body = String(code || '').replace(/<\/script/gi, '<\\/script');
    const seed = JSON.stringify(initial || {}).replace(/</g, '\\u003c');
    return [
      '<!doctype html><html><head><meta charset="utf-8">',
      '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; script-src \'unsafe-inline\'; style-src \'unsafe-inline\'">',
      '<style>html,body{margin:0;height:100%;background:#fffdf9;overflow:hidden}canvas{display:block;width:100%;height:100%}</style>',
      '</head><body><canvas id="c"></canvas><script>',
      '(function(){',
      "var canvas=document.getElementById('c'),ctx=canvas.getContext('2d');",
      `var S=${seed};`,
      'var W=0,H=0,t0=performance.now(),lastT=0,paused=false;',
      'function fit(){var r=canvas.getBoundingClientRect();var dpr=Math.min(2,window.devicePixelRatio||1);W=r.width||520;H=r.height||260;canvas.width=Math.round(W*dpr);canvas.height=Math.round(H*dpr);ctx.setTransform(dpr,0,0,dpr,0,0);}',
      "window.addEventListener('resize',fit);fit();",
      'var draw=null;',
      'try{',
      `draw=(function(){${body}\nreturn typeof draw === 'function' ? draw : null;})();`,
      "}catch(e){try{parent.postMessage({type:'board-error',message:String(e&&e.message||e)},'*');}catch(_){}}",
      'function frame(now){',
      '  if(!paused) lastT=(now-t0)/1000;',
      '  try{ctx.clearRect(0,0,W,H); if(typeof draw===\'function\') draw(ctx,W,H,S,lastT);}',
      "  catch(e){if(!frame.broken){frame.broken=true;try{parent.postMessage({type:'board-error',message:String(e&&e.message||e)},'*');}catch(_){}}}",
      '  requestAnimationFrame(frame);',
      '}',
      "window.addEventListener('message',function(e){var d=e.data||{};if(d.type==='board-state'&&d.state){for(var k in d.state){if(Object.prototype.hasOwnProperty.call(d.state,k))S[k]=d.state[k];}}if(d.type==='board-pause'){paused=!!d.paused;}});",
      "window.addEventListener('error',function(e){try{parent.postMessage({type:'board-error',message:String(e.message)},'*');}catch(_){}});",
      'requestAnimationFrame(frame);',
      '})();',
      '</script></body></html>'
    ].join('\n');
  }

  /** Sliders from the generated scene: each one re-renders the iframe. */
  function mountControls(controls, values) {
    const host = state.panel && state.panel.querySelector('.sx-board-controls');
    if (!host) return;
    host.innerHTML = '';
    if (!Array.isArray(controls) || !controls.length) {
      host.hidden = true;
      return;
    }
    host.hidden = false;
    controls.forEach((cfg) => {
      const wrap = document.createElement('label');
      wrap.className = 'sx-board-control';
      const name = document.createElement('span');
      name.textContent = cfg.label || cfg.key;
      const input = document.createElement('input');
      input.type = 'range';
      input.min = String(cfg.min);
      input.max = String(cfg.max);
      input.step = String(cfg.step);
      input.value = String(values[cfg.key] != null ? values[cfg.key] : cfg.value != null ? cfg.value : cfg.min);
      input.setAttribute('aria-label', cfg.label || cfg.key);
      const out = document.createElement('output');
      out.textContent = input.value;
      input.addEventListener('input', () => {
        values[cfg.key] = Number(input.value);
        out.textContent = input.value;
        if (state.frame && state.frame.contentWindow) {
          state.frame.contentWindow.postMessage({ type: 'board-state', state: values }, '*');
        }
      });
      wrap.appendChild(name);
      wrap.appendChild(input);
      wrap.appendChild(out);
      host.appendChild(wrap);
    });
  }

  /** A generated canvas scene: the model's drawing code, sandboxed, with sliders. */
  function mountCode(canvas, code, controls, params) {
    if (!code || typeof code !== 'string') return false;
    const values = Object.assign({}, params || {});
    (controls || []).forEach((cfg) => {
      values[cfg.key] = Number(cfg.value != null ? cfg.value : cfg.min);
    });
    const frame = document.createElement('iframe');
    frame.className = 'sx-board-frame';
    frame.setAttribute('sandbox', 'allow-scripts');
    frame.setAttribute('title', 'Interactive diagram');
    frame.setAttribute('aria-label', 'Interactive diagram');
    frame.srcdoc = sceneDocument(code, values);
    canvas.appendChild(frame);
    state.frame = frame;
    state.controls = values;
    mountControls(controls, values);
    return true;
  }

  /**
   * Mount a scene without re-typing the steps. Used to upgrade a board that is
   * already open once the generated drawing arrives.
   */
  async function scene(payload) {
    const data = payload || {};
    const panel = ensurePanel();
    const canvas = panel.querySelector('.sx-board-canvas');
    const note = panel.querySelector('.sx-board-note');
    clearScene();
    canvas.innerHTML = '';
    canvas.hidden = true;
    if (note) note.hidden = true;

    let mounted = false;
    if (data.code) {
      canvas.hidden = false;
      mounted = mountCode(canvas, data.code, data.controls, data.params);
    } else if (data.preset) {
      canvas.hidden = false;
      mounted = await mountPreset(canvas, data.preset, data.params);
    }
    if (!mounted && data.preset) {
      canvas.hidden = true;
      canvas.innerHTML = '';
      if (note) {
        note.textContent = 'The diagram could not load, so this is the written method.';
        note.hidden = false;
      }
    }
    return { ok: mounted };
  }

  /**
   * @param {{title?:string, steps?:string[], preset?:string, params?:object, code?:string, controls?:Array}} payload
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

    clearScene();
    canvas.innerHTML = '';
    canvas.hidden = true;
    note.hidden = true;

    if (data.code) {
      canvas.hidden = false;
      mountCode(canvas, data.code, data.controls, data.params);
    } else if (data.preset) {
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
    clearScene();
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
    scene,
    close,
    skip,
    supported: SUPPORTED,
    isOpen: () => !!(state.panel && !state.panel.hidden),
    viewType
  };

  global.Board = api;
})(window);
