/**
 * Veelearn Study Coach widget engine — mounts declarative widgetSpecs
 * (no model-supplied JS). Lazy-loads JSXGraph / Desmos / Three.js as needed.
 */
(function (global) {
  'use strict';

  const COLOR_MAP = {
    red: '#e74c3c',
    blue: '#3498db',
    green: '#2ecc71',
    orange: '#e67e22',
    purple: '#9b59b6',
    yellow: '#f1c40f',
    white: '#ecf0f1',
    cyan: '#1abc9c',
    pink: '#ff6b9d'
  };

  function resolveColor(c, fallback) {
    if (c == null) return fallback || '#667eea';
    const s = String(c).toLowerCase();
    if (COLOR_MAP[s]) return COLOR_MAP[s];
    if (/^#([0-9a-f]{3}|[0-9a-f]{6})$/i.test(s)) return s;
    return fallback || '#667eea';
  }

  function loadCss(href) {
    if (document.querySelector(`link[data-vl-widget="${href}"]`)) return Promise.resolve();
    return new Promise((resolve, reject) => {
      const l = document.createElement('link');
      l.rel = 'stylesheet';
      l.href = href;
      l.dataset.vlWidget = href;
      l.onload = () => resolve();
      l.onerror = reject;
      document.head.appendChild(l);
    });
  }

  function loadScript(src) {
    if (document.querySelector(`script[data-vl-widget="${src}"]`)) return Promise.resolve();
    return new Promise((resolve, reject) => {
      const s = document.createElement('script');
      s.src = src;
      s.async = true;
      s.dataset.vlWidget = src;
      s.onload = () => resolve();
      s.onerror = reject;
      document.body.appendChild(s);
    });
  }

  let jsxReady = null;
  function ensureJsxGraph() {
    if (global.JXG) return Promise.resolve(global.JXG);
    if (jsxReady) return jsxReady;
    jsxReady = loadCss('https://cdn.jsdelivr.net/npm/jsxgraph@1.10.1/distrib/jsxgraph.css')
      .then(() => loadScript('https://cdn.jsdelivr.net/npm/jsxgraph@1.10.1/distrib/jsxgraphcore.js'))
      .then(() => global.JXG);
    return jsxReady;
  }

  let desmosReady = null;
  function ensureDesmos() {
    if (global.Desmos) return Promise.resolve(global.Desmos);
    if (desmosReady) return desmosReady;
    desmosReady = loadScript(
      'https://www.desmos.com/api/v1.10/calculator.js?apiKey=dcb31709b452b1cf9dc696757be2ef20'
    ).then(() => global.Desmos);
    return desmosReady;
  }

  let threeReady = null;
  function ensureThree() {
    if (global.THREE) return Promise.resolve(global.THREE);
    if (threeReady) return threeReady;
    const urls = [
      'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js',
      'https://unpkg.com/three@0.160.0/build/three.min.js'
    ];
    threeReady = (async () => {
      let lastErr;
      for (const url of urls) {
        try {
          await loadScript(url);
          if (global.THREE) return global.THREE;
        } catch (e) {
          lastErr = e;
        }
      }
      throw lastErr || new Error('Three.js failed to load');
    })();
    return threeReady;
  }

  function typesetMath(el) {
    if (!el) return Promise.resolve();
    const MJ = global.MathJax;
    if (!MJ || typeof MJ.typesetPromise !== 'function') return Promise.resolve();
    return MJ.typesetPromise([el]).catch(() => {});
  }

  function showDrawingOverlay(host) {
    const overlay = document.createElement('div');
    overlay.className = 'vl-widget-drawing';
    overlay.innerHTML =
      '<div class="vl-widget-drawing-inner"><span class="vl-widget-pen" aria-hidden="true">✎</span><span>Drawing…</span></div>';
    host.style.position = host.style.position || 'relative';
    host.appendChild(overlay);
    return overlay;
  }

  function hideDrawingOverlay(overlay) {
    if (overlay && overlay.parentNode) overlay.parentNode.removeChild(overlay);
  }

  /** Restricted math expression → fn(independentValue, state). State keys (a,b,…) bind from sliders. */
  function compileExpr(expr, independentVars) {
    const vars = independentVars && independentVars.length ? independentVars : ['x'];
    const raw = String(expr || '')
      .replace(/^\s*y\s*=\s*/i, '')
      .replace(/\^/g, '**')
      .replace(/π/gi, 'Math.PI')
      .replace(/\bpi\b/gi, 'Math.PI')
      .trim();
    if (!raw || /[;{}`\\]|<|>|script|function|=>|eval|window|document/i.test(raw)) {
      return () => NaN;
    }
    let body = raw
      .replace(/\bsin\b/g, 'Math.sin')
      .replace(/\bcos\b/g, 'Math.cos')
      .replace(/\btan\b/g, 'Math.tan')
      .replace(/\babs\b/g, 'Math.abs')
      .replace(/\bsqrt\b/g, 'Math.sqrt')
      .replace(/\blog\b/g, 'Math.log')
      .replace(/\bln\b/g, 'Math.log')
      .replace(/\bexp\b/g, 'Math.exp')
      .replace(/\bpow\b/g, 'Math.pow')
      .replace(/\bmin\b/g, 'Math.min')
      .replace(/\bmax\b/g, 'Math.max');
    if (!/^[\d\sA-Za-z_+\-*/().,]+$/.test(body.replace(/Math\./g, ''))) {
      return () => NaN;
    }

    const reserved = new Set([
      ...vars,
      'Math',
      'sin',
      'cos',
      'tan',
      'abs',
      'sqrt',
      'log',
      'ln',
      'exp',
      'pow',
      'min',
      'max',
      'PI',
      'E',
      'true',
      'false',
      'NaN',
      'Infinity'
    ]);
    const freeIds = new Set();
    body.replace(/\b([A-Za-z_][A-Za-z0-9_]*)\b/g, (id) => {
      if (!reserved.has(id)) freeIds.add(id);
      return id;
    });
    let safeBody = body;
    freeIds.forEach((id) => {
      safeBody = safeBody.replace(new RegExp(`\\b${id}\\b`, 'g'), `(+__s[${JSON.stringify(id)}]||0)`);
    });

    try {
      // eslint-disable-next-line no-new-func
      const impl = new Function(...vars, '__s', `"use strict"; return (${safeBody});`);
      return function evalExpr(independent, state) {
        try {
          return impl(independent, state || {});
        } catch (_) {
          return NaN;
        }
      };
    } catch (_) {
      return () => NaN;
    }
  }

  function buildCard(spec) {
    const card = document.createElement('div');
    card.className = 'vl-widget-card';
    const title = document.createElement('div');
    title.className = 'vl-widget-title';
    title.textContent = spec.title || 'Interactive';
    card.appendChild(title);
    if (spec.objective) {
      const obj = document.createElement('div');
      obj.className = 'vl-widget-objective';
      obj.textContent = spec.objective;
      card.appendChild(obj);
    }
    const outputsEl = document.createElement('div');
    outputsEl.className = 'vl-widget-outputs';
    card.appendChild(outputsEl);
    const viewHost = document.createElement('div');
    viewHost.className = 'vl-widget-view';
    const w = (spec.view && spec.view.width) || 520;
    const h = (spec.view && spec.view.height) || 320;
    viewHost.style.width = '100%';
    viewHost.style.maxWidth = `${w}px`;
    viewHost.style.height = `${Math.min(h, 420)}px`;
    card.appendChild(viewHost);
    const controls = document.createElement('div');
    controls.className = 'vl-widget-controls';
    card.appendChild(controls);
    return { card, viewHost, controls, outputsEl };
  }

  function wireControls(controlsEl, state, inputs, onChange, onAction) {
    (inputs || []).forEach((inp) => {
      const row = document.createElement('div');
      row.className = 'vl-widget-control-row';
      const label = document.createElement('label');
      label.textContent = inp.label || inp.key;
      row.appendChild(label);

      if (inp.type === 'slider' || inp.type === 'number') {
        const input = document.createElement('input');
        input.type = inp.type === 'number' ? 'number' : 'range';
        input.min = inp.min != null ? inp.min : 0;
        input.max = inp.max != null ? inp.max : 100;
        input.step = inp.step != null ? inp.step : 1;
        if (state[inp.key] == null) state[inp.key] = Number(input.min) || 0;
        input.value = state[inp.key];
        const val = document.createElement('span');
        val.className = 'vl-widget-val';
        val.textContent = String(state[inp.key]);
        input.addEventListener('input', () => {
          state[inp.key] = Number(input.value);
          val.textContent = String(state[inp.key]);
          onChange();
        });
        row.appendChild(input);
        row.appendChild(val);
      } else if (inp.type === 'select') {
        const sel = document.createElement('select');
        (inp.options || []).forEach((opt) => {
          const o = document.createElement('option');
          o.value = opt;
          o.textContent = opt;
          if (String(state[inp.key]) === String(opt)) o.selected = true;
          sel.appendChild(o);
        });
        if (state[inp.key] == null && inp.options && inp.options[0] != null) {
          state[inp.key] = inp.options[0];
        }
        sel.addEventListener('change', () => {
          state[inp.key] = sel.value;
          onChange();
        });
        row.appendChild(sel);
      } else if (inp.type === 'toggle') {
        const input = document.createElement('input');
        input.type = 'checkbox';
        input.checked = !!state[inp.key];
        input.addEventListener('change', () => {
          state[inp.key] = !!input.checked;
          onChange();
        });
        row.appendChild(input);
      } else if (inp.type === 'button') {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.textContent = inp.label || inp.key;
        btn.addEventListener('click', () => onAction(inp.action || inp.key));
        row.appendChild(btn);
      }
      controlsEl.appendChild(row);
    });
  }

  function wireOutputs(outputsEl, state, outputs) {
    const nodes = {};
    (outputs || []).forEach((o) => {
      const row = document.createElement('div');
      row.className = 'vl-widget-output-row';
      if (o.type === 'sparkline') {
        row.innerHTML = `<span>${escapeText(o.label || o.key)}</span><canvas class="vl-sparkline" width="120" height="28" data-key="${escapeText(o.key)}"></canvas>`;
      } else {
        row.innerHTML = `<span>${escapeText(o.label || o.key)}</span><strong data-key="${escapeText(o.key)}">—</strong>`;
      }
      outputsEl.appendChild(row);
      nodes[o.key] = row;
    });
    function refresh() {
      (outputs || []).forEach((o) => {
        const v = state[o.key];
        if (o.type === 'sparkline') {
          const canvas = outputsEl.querySelector(`canvas[data-key="${o.key}"]`);
          if (canvas && Array.isArray(v)) drawSparkline(canvas, v);
        } else {
          const el = outputsEl.querySelector(`strong[data-key="${o.key}"]`);
          if (el) {
            el.textContent =
              typeof v === 'number' ? (Math.abs(v) >= 100 ? v.toFixed(1) : Number(v.toFixed(3)).toString()) : v == null ? '—' : String(v);
          }
        }
      });
    }
    return { refresh };
  }

  function drawSparkline(canvas, series) {
    const ctx = canvas.getContext('2d');
    const w = canvas.width;
    const h = canvas.height;
    ctx.clearRect(0, 0, w, h);
    if (!series.length) return;
    const min = Math.min(...series);
    const max = Math.max(...series);
    const span = max - min || 1;
    ctx.strokeStyle = '#667eea';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    series.forEach((v, i) => {
      const x = (i / Math.max(1, series.length - 1)) * (w - 2) + 1;
      const y = h - 2 - ((v - min) / span) * (h - 4);
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.stroke();
  }

  function escapeText(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function makeBoard(JXG, host, bb) {
    const id = `vl-jxg-${Date.now()}-${Math.random().toString(36).slice(2, 7)}`;
    host.id = id;
    host.innerHTML = '';
    return JXG.JSXGraph.initBoard(id, {
      boundingbox: bb || [-6, 6, 6, -6],
      axis: true,
      showCopyright: false,
      showNavigation: true,
      pan: { enabled: true },
      zoom: { enabled: true }
    });
  }

  function applyGeometryElements(board, JXG, elements, named) {
    const map = named || {};
    (elements || []).forEach((el) => {
      try {
        if (el.type === 'point') {
          map[el.name] = board.create('point', [el.x || 0, el.y || 0], {
            name: el.label || el.name || '',
            size: 3,
            color: resolveColor(el.color, '#e74c3c')
          });
        } else if (el.type === 'segment' && map[el.from] && map[el.to]) {
          map[el.name] = board.create('segment', [map[el.from], map[el.to]], {
            strokeColor: resolveColor(el.color, '#3498db')
          });
        } else if (el.type === 'line' && map[el.from] && map[el.to]) {
          map[el.name] = board.create('line', [map[el.from], map[el.to]], {
            strokeColor: resolveColor(el.color, '#3498db')
          });
        } else if (el.type === 'ray' && map[el.from] && map[el.to]) {
          map[el.name] = board.create('line', [map[el.from], map[el.to]], {
            straightFirst: false,
            straightLast: true,
            strokeColor: resolveColor(el.color, '#3498db')
          });
        } else if (el.type === 'circle') {
          if (map[el.center] && map[el.through]) {
            map[el.name] = board.create('circle', [map[el.center], map[el.through]], {
              strokeColor: resolveColor(el.color, '#9b59b6')
            });
          } else if (map[el.center] && el.radius != null) {
            map[el.name] = board.create('circle', [map[el.center], el.radius], {
              strokeColor: resolveColor(el.color, '#9b59b6')
            });
          }
        } else if (el.type === 'polygon' && Array.isArray(el.points)) {
          const pts = el.points.map((n) => map[n]).filter(Boolean);
          if (pts.length >= 3) {
            map[el.name] = board.create('polygon', pts, {
              fillColor: resolveColor(el.color, '#3498db'),
              fillOpacity: 0.25
            });
          }
        } else if (el.type === 'midpoint' && map[el.from] && map[el.to]) {
          map[el.name] = board.create('midpoint', [map[el.from], map[el.to]], {
            name: el.label || el.name || '',
            size: 2
          });
        } else if (el.type === 'intersection' && map[el.from] && map[el.to]) {
          map[el.name] = board.create('intersection', [map[el.from], map[el.to], 0], {
            name: el.label || el.name || '',
            size: 3
          });
        } else if (el.type === 'function' && el.expr) {
          const fn = compileExpr(el.expr, ['x']);
          map[el.name] = board.create('functiongraph', [(x) => fn(x, {})], {
            strokeColor: resolveColor(el.color, '#e74c3c'),
            strokeWidth: 2
          });
        } else if (el.type === 'text') {
          board.create('text', [el.x || 0, el.y || 0, el.text || ''], { fontSize: 14 });
        } else if (el.type === 'vector' && map[el.from] && map[el.to]) {
          map[el.name] = board.create('arrow', [map[el.from], map[el.to]], {
            strokeColor: resolveColor(el.color, '#e67e22')
          });
        } else if (el.type === 'angle' && map[el.from] && map[el.center || el.name] === undefined && el.points) {
          /* skip unsupported */
        }
      } catch (err) {
        console.warn('geometry element failed', el, err);
      }
    });
    return map;
  }

  async function mountJsxPreset(host, spec, state, opts) {
    const JXG = await ensureJsxGraph();
    const params = (spec.behavior && spec.behavior.params) || {};
    const board = makeBoard(JXG, host, params.boundingbox);
    const named = {};
    const preset = spec.behavior.preset;

    if (preset === 'number_line') {
      board.setBoundingBox([-10, 2, 10, -2]);
      board.create('line', [[-10, 0], [10, 0]], { strokeColor: '#888' });
      const elements = params.elements || [];
      elements.forEach((el) => {
        if (el.type === 'point') {
          board.create('point', [el.x || 0, 0], { name: el.label || el.name || '', size: 4 });
        }
      });
      if (state.point != null) {
        const p = board.create('point', [Number(state.point) || 0, 0], { name: 'P', size: 5, color: '#e74c3c' });
        opts._update = () => {
          p.setPosition(JXG.COORDS_BY_USER, [Number(state.point) || 0, 0]);
          board.update();
        };
      }
      return { board };
    }

    if (preset === 'unit_circle') {
      board.setBoundingBox([-1.8, 1.8, 1.8, -1.8]);
      board.create('circle', [[0, 0], 1], { strokeColor: '#667eea' });
      const ang = () => ((Number(state.angle) || 0) * Math.PI) / 180;
      const tip = board.create(
        'point',
        [() => Math.cos(ang()), () => Math.sin(ang())],
        { name: 'P', size: 4, color: '#e74c3c' }
      );
      board.create('segment', [[0, 0], tip], { strokeColor: '#e74c3c' });
      opts._update = () => board.update();
      return { board };
    }

    if (preset === 'triangle_lab') {
      const a = Number(state.a != null ? state.a : params.a) || 3;
      const b = Number(state.b != null ? state.b : params.b) || 4;
      const c = Number(state.c != null ? state.c : params.c) || 5;
      const A = board.create('point', [0, 0], { name: 'A', fixed: true });
      const B = board.create('point', [c, 0], { name: 'B', fixed: true });
      const cosA = (b * b + c * c - a * a) / (2 * b * c);
      const sinA = Math.sqrt(Math.max(0, 1 - cosA * cosA));
      const C = board.create('point', [b * cosA, b * sinA], { name: 'C', fixed: true });
      board.create('polygon', [A, B, C], { fillColor: '#667eea', fillOpacity: 0.2 });
      state.sideSummary = `a=${a}, b=${b}, c=${c}`;
      return { board };
    }

    if (preset === 'counting_grid') {
      const rows = Math.min(20, Math.max(2, Number(state.rows || params.rows) || 5));
      const cols = Math.min(20, Math.max(2, Number(state.cols || params.cols) || 5));
      board.setBoundingBox([-0.5, rows + 0.5, cols + 0.5, -0.5]);
      for (let i = 0; i <= cols; i++) {
        board.create('line', [[i, 0], [i, rows]], { strokeColor: '#bbb', straightFirst: false, straightLast: false });
      }
      for (let j = 0; j <= rows; j++) {
        board.create('line', [[0, j], [cols, j]], { strokeColor: '#bbb', straightFirst: false, straightLast: false });
      }
      return { board };
    }

    if (preset === 'transformation_lab') {
      const shape = params.elements && params.elements.length
        ? params.elements
        : [
            { type: 'point', name: 'A', x: 1, y: 1 },
            { type: 'point', name: 'B', x: 3, y: 1 },
            { type: 'point', name: 'C', x: 2, y: 3 },
            { type: 'polygon', name: 'T', points: ['A', 'B', 'C'], color: 'blue' }
          ];
      applyGeometryElements(board, JXG, shape, named);
      const dx = Number(state.dx) || 0;
      const dy = Number(state.dy) || 0;
      const rot = ((Number(state.rotate) || 0) * Math.PI) / 180;
      Object.keys(named).forEach((k) => {
        const p = named[k];
        if (p && p.elType === 'point') {
          const x = p.X();
          const y = p.Y();
          const xr = x * Math.cos(rot) - y * Math.sin(rot) + dx;
          const yr = x * Math.sin(rot) + y * Math.cos(rot) + dy;
          board.create('point', [xr, yr], { name: k + "'", size: 3, color: '#e74c3c' });
        }
      });
      return { board };
    }

    if (preset === 'inequality_region') {
      const exprs = params.expressions || [];
      exprs.forEach((ex, i) => {
        const colors = ['#e74c3c', '#3498db', '#2ecc71'];
        const cleaned = String(ex).replace(/^\s*y\s*[<>]=?\s*/i, '');
        const fn = compileExpr(cleaned, ['x']);
        board.create('functiongraph', [(x) => fn(x, state)], {
          strokeColor: colors[i % colors.length],
          strokeWidth: 2
        });
      });
      applyGeometryElements(board, JXG, params.elements, named);
      opts._update = () => board.update();
      return { board };
    }

    if (preset === 'parametric_plot') {
      const xt = compileExpr(params.xExpr || 'cos(t)', ['t']);
      const yt = compileExpr(params.yExpr || 'sin(t)', ['t']);
      const t0 = Number(params.tMin) || 0;
      const t1 = Number(params.tMax) || Math.PI * 2;
      board.create(
        'curve',
        [(t) => xt(t, state), (t) => yt(t, state), t0, t1],
        { strokeColor: '#e74c3c', strokeWidth: 2 }
      );
      opts._update = () => board.update();
      return { board };
    }

    if (preset === 'area_shade') {
      applyGeometryElements(board, JXG, params.elements, named);
      const expr = params.expressions && params.expressions[0];
      if (expr) {
        const fn = compileExpr(expr, ['x']);
        board.create('functiongraph', [(x) => fn(x, state)], { strokeColor: '#e74c3c', strokeWidth: 2 });
        opts._update = () => board.update();
      }
      return { board };
    }

    if (preset === 'function_plot' || preset === 'coordinate_plane') {
      const exprs = params.expressions || [];
      const colors = ['#e74c3c', '#3498db', '#2ecc71', '#e67e22'];
      let plotted = false;
      exprs.forEach((ex, i) => {
        try {
          const fn = compileExpr(ex, ['x']);
          board.create('functiongraph', [(x) => fn(x, state)], {
            strokeColor: colors[i % colors.length],
            strokeWidth: 2
          });
          plotted = true;
        } catch (err) {
          console.warn('function_plot expr failed', ex, err);
        }
      });
      // Default quadratic when sliders provide a/b/c but no expressions
      if (!plotted && (state.a != null || state.b != null || state.c != null)) {
        board.create(
          'functiongraph',
          [
            (x) => {
              const a = Number(state.a) || 0;
              const b = Number(state.b) || 0;
              const c = Number(state.c) || 0;
              return a * x * x + b * x + c;
            }
          ],
          { strokeColor: '#9b59b6', strokeWidth: 2 }
        );
        plotted = true;
      }
      applyGeometryElements(board, JXG, params.elements, named);
      opts._update = () => board.update();
      return { board };
    }

    // geometry_board (default JSX path)
    applyGeometryElements(board, JXG, params.elements, named);
    const exprs = params.expressions || [];
    exprs.forEach((ex, i) => {
      try {
        const fn = compileExpr(ex, ['x']);
        board.create('functiongraph', [(x) => fn(x, state)], {
          strokeColor: ['#e74c3c', '#3498db'][i % 2],
          strokeWidth: 2
        });
      } catch (err) {
        console.warn('geometry expr failed', ex, err);
      }
    });
    opts._update = () => board.update();
    return { board };
  }

  async function mountDesmos(host, spec) {
    const Desmos = await ensureDesmos();
    host.innerHTML = '';
    const el = document.createElement('div');
    el.style.width = '100%';
    el.style.height = '100%';
    host.appendChild(el);
    const calc = Desmos.GraphingCalculator(el, {
      expressions: true,
      settingsMenu: false,
      zoomButtons: true,
      expressionsCollapsed: true
    });
    const params = (spec.behavior && spec.behavior.params) || {};
    const exprs = params.expressions || [];
    exprs.forEach((latex, i) => {
      let s = String(latex).trim();
      if (!/=/.test(s) && !/y/i.test(s)) s = `y=${s}`;
      calc.setExpression({ id: `e${i}`, latex: s.replace(/\*\*/g, '^') });
    });
    return {
      destroy() {
        try {
          calc.destroy();
        } catch (_) {
          /* ignore */
        }
      }
    };
  }

  async function mountThreePreset(host, spec, state, opts) {
    const THREE = await ensureThree();
    if (!THREE || !THREE.WebGLRenderer) {
      throw new Error('Three.js WebGLRenderer unavailable');
    }
    host.innerHTML = '';
    host.style.position = 'relative';
    host.style.minHeight = host.style.minHeight || '280px';
    host.style.width = '100%';

    const canvas = document.createElement('canvas');
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    canvas.style.display = 'block';
    canvas.style.borderRadius = '10px';
    host.appendChild(canvas);

    // Force layout before measuring (host can be 0×0 on first paint)
    const w = Math.max(host.clientWidth || 0, 320);
    const h = Math.max(host.clientHeight || 0, 280);
    canvas.width = w;
    canvas.height = h;

    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(global.devicePixelRatio || 1, 2));
    renderer.setSize(w, h, false);
    renderer.setClearColor(0x1a1a2e, 1);

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(50, w / h, 0.1, 100);
    camera.position.set(2.5, 2, 3.5);
    camera.lookAt(0, 0, 0);

    const light = new THREE.DirectionalLight(0xffffff, 1.1);
    light.position.set(3, 5, 4);
    scene.add(light);
    scene.add(new THREE.AmbientLight(0xffffff, 0.35));

    const preset = spec.behavior.preset;
    const params = (spec.behavior && spec.behavior.params) || {};
    let mesh = null;
    const meshes = [];

    function colorOf() {
      return new THREE.Color(resolveColor(state.color || params.color, '#e74c3c'));
    }

    if (preset === 'scene3d') {
      const axes = new THREE.AxesHelper(2);
      scene.add(axes);
      (params.objects || []).forEach((o) => {
        let geo;
        const t = String(o.type || 'box');
        if (t === 'sphere') geo = new THREE.SphereGeometry(o.size || 0.5, 24, 16);
        else if (t === 'plane') geo = new THREE.PlaneGeometry(o.size || 2, o.size || 2);
        else geo = new THREE.BoxGeometry(o.size || 1, o.size || 1, o.size || 1);
        const mat = new THREE.MeshStandardMaterial({
          color: resolveColor(o.color, '#667eea'),
          metalness: 0.2,
          roughness: 0.55
        });
        const m = new THREE.Mesh(geo, mat);
        m.position.set(o.x || 0, o.y || 0, o.z || 0);
        if (t === 'plane') m.rotation.x = -Math.PI / 2;
        scene.add(m);
        meshes.push(m);
      });
      if (!params.objects || !params.objects.length) {
        mesh = new THREE.Mesh(
          new THREE.BoxGeometry(1, 1, 1),
          new THREE.MeshStandardMaterial({ color: colorOf() })
        );
        scene.add(mesh);
      }
    } else if (preset === 'orbit_mesh') {
      const shape = String(state.shape || params.shape || 'box');
      let geo;
      if (shape === 'sphere') geo = new THREE.SphereGeometry(0.8, 32, 24);
      else if (shape === 'torus') geo = new THREE.TorusGeometry(0.6, 0.25, 16, 48);
      else geo = new THREE.BoxGeometry(1, 1, 1);
      mesh = new THREE.Mesh(
        geo,
        new THREE.MeshStandardMaterial({ color: colorOf(), metalness: 0.25, roughness: 0.45 })
      );
      scene.add(mesh);
    } else {
      // spinning_box
      mesh = new THREE.Mesh(
        new THREE.BoxGeometry(1, 1, 1),
        new THREE.MeshStandardMaterial({ color: colorOf(), metalness: 0.25, roughness: 0.45 })
      );
      scene.add(mesh);
    }

    let raf = 0;
    let alive = true;
    function applyState() {
      const target = mesh;
      if (!target) return;
      const size = Number(state.size);
      const scale = Number.isFinite(size) ? Math.max(0.2, size / 100) : 1;
      target.scale.set(scale, scale, scale);
      if (target.material && target.material.color) {
        target.material.color.set(resolveColor(state.color, '#e74c3c'));
      }
    }
    applyState();

    function tick() {
      if (!alive) return;
      raf = requestAnimationFrame(tick);
      const speed = Number(state.rotationSpeed != null ? state.rotationSpeed : 1);
      const rotating = state.rotating !== false && state.paused !== true;
      if (mesh && rotating) {
        mesh.rotation.x += 0.01 * speed;
        mesh.rotation.y += 0.015 * speed;
      }
      meshes.forEach((m, i) => {
        if (rotating) {
          m.rotation.y += 0.008 * speed * (1 + i * 0.1);
        }
      });
      applyState();
      renderer.render(scene, camera);
    }
    tick();

    opts._update = () => applyState();

    return {
      destroy() {
        alive = false;
        cancelAnimationFrame(raf);
        renderer.dispose();
        host.innerHTML = '';
      }
    };
  }

  function mountCanvasSim(host, spec, state, outputsApi, opts) {
    host.innerHTML = '';
    const canvas = document.createElement('canvas');
    const w = host.clientWidth || 480;
    const h = host.clientHeight || 300;
    canvas.width = w;
    canvas.height = h;
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    canvas.style.borderRadius = '10px';
    canvas.style.background = '#0f1220';
    host.appendChild(canvas);
    const ctx = canvas.getContext('2d');
    const preset = spec.behavior.preset;
    const params = (spec.behavior && spec.behavior.params) || {};

    let alive = true;
    let raf = 0;
    let t0 = performance.now();
    const particles = [];
    let energy = Number(state.energyMeV) || 0;
    const rateSeries = Array.isArray(state.fusionRateSeries) ? state.fusionRateSeries.slice() : [];
    let trail = [];

    function resetParticles() {
      particles.length = 0;
      const n = Math.min(120, Math.max(10, Number(state.density || params.count) || 40));
      for (let i = 0; i < n; i++) {
        const species = i % 2;
        particles.push({
          x: Math.random() * w,
          y: Math.random() * h,
          vx: (Math.random() - 0.5) * 2,
          vy: (Math.random() - 0.5) * 2,
          species,
          r: species ? 4 : 3
        });
      }
      energy = 0;
      rateSeries.length = 0;
      trail = [];
    }
    resetParticles();

    opts._action = (action) => {
      if (action === 'reset') resetParticles();
    };

    function step(dt) {
      if (state.paused) return;
      const temp = Math.max(1, Number(state.temperature) || 10);
      const mag = Math.max(1, Number(state.magneticField) || 50);
      const dens = Math.max(5, Number(state.density) || 40);

      if (preset === 'fusion_dt' || preset === 'particles2d') {
        const speedScale =
          params.velocityScale === 'sqrt_temperature' ? Math.sqrt(temp) * 0.35 : temp * 0.05;
        let fusions = 0;
        const fuseDist = Number(params.fusionDistance) || 8;
        const ePer = Number(params.energyPerFusionMeV) || 17.6;
        particles.forEach((p) => {
          const sp = speedScale * (0.6 + Math.random() * 0.8);
          p.vx += (Math.random() - 0.5) * 0.4 * sp;
          p.vy += (Math.random() - 0.5) * 0.4 * sp;
          // magnetic confinement pulls toward center
          const cx = w / 2;
          const cy = h / 2;
          p.vx += ((cx - p.x) / w) * (mag / 80);
          p.vy += ((cy - p.y) / h) * (mag / 80);
          const maxV = 2 + speedScale;
          p.vx = Math.max(-maxV, Math.min(maxV, p.vx));
          p.vy = Math.max(-maxV, Math.min(maxV, p.vy));
          p.x += p.vx;
          p.y += p.vy;
          if (p.x < 0 || p.x > w) p.vx *= -1;
          if (p.y < 0 || p.y > h) p.vy *= -1;
          p.x = Math.max(0, Math.min(w, p.x));
          p.y = Math.max(0, Math.min(h, p.y));
        });
        if (preset === 'fusion_dt') {
          for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
              const a = particles[i];
              const b = particles[j];
              if (a.species === b.species) continue;
              const dx = a.x - b.x;
              const dy = a.y - b.y;
              if (dx * dx + dy * dy < fuseDist * fuseDist && Math.random() < dens / 400) {
                fusions++;
                energy += ePer;
                a.x = Math.random() * w;
                a.y = Math.random() * h;
                b.x = Math.random() * w;
                b.y = Math.random() * h;
              }
            }
          }
          rateSeries.push(fusions);
          if (rateSeries.length > 40) rateSeries.shift();
          state.energyMeV = energy;
          state.fusionRateSeries = rateSeries.slice();
        }
      } else if (preset === 'projectile') {
        const angle = ((Number(state.angle) || 45) * Math.PI) / 180;
        const speed = Number(state.speed) || 40;
        const g = Number(state.g) || 9.8;
        trail = [];
        let x = 40;
        let y = h - 40;
        let vx = Math.cos(angle) * speed;
        let vy = -Math.sin(angle) * speed;
        for (let i = 0; i < 200; i++) {
          trail.push({ x, y });
          vy += g * 0.15;
          x += vx * 0.15;
          y += vy * 0.15;
          if (y > h - 20) break;
        }
      } else if (preset === 'gravity_orbit') {
        const cx = w / 2;
        const cy = h / 2;
        if (!state._orb) {
          state._orb = { x: cx + 90, y: cy, vx: 0, vy: 1.6 };
        }
        const o = state._orb;
        const dx = cx - o.x;
        const dy = cy - o.y;
        const dist = Math.sqrt(dx * dx + dy * dy) || 1;
        const G = Number(state.gravity) || 1200;
        o.vx += (G * dx) / (dist * dist * dist);
        o.vy += (G * dy) / (dist * dist * dist);
        o.x += o.vx;
        o.y += o.vy;
      } else if (preset === 'pendulum') {
        if (state._theta == null) state._theta = ((Number(state.angle) || 40) * Math.PI) / 180;
        if (state._omega == null) state._omega = 0;
        const L = Math.max(40, Number(state.length) || 120);
        const g = Number(state.g) || 9.8;
        state._omega += (-(g / (L / 40)) * Math.sin(state._theta)) * 0.05;
        state._theta += state._omega * 0.05;
        state._omega *= 0.999;
        state._L = L;
      } else if (preset === 'spring_mass') {
        if (state._x == null) state._x = Number(state.displacement) || 40;
        if (state._v == null) state._v = 0;
        const k = Number(state.k) || 0.08;
        const m = Number(state.mass) || 1;
        state._v += ((-k * state._x) / m) * 0.4;
        state._x += state._v;
        state._v *= 0.995;
      } else if (preset === 'collision_1d') {
        if (!state._balls) {
          state._balls = [
            { x: 80, v: Number(state.v1) || 2, m: Number(state.m1) || 1, r: 14 },
            { x: w - 100, v: Number(state.v2) || -1.2, m: Number(state.m2) || 1.5, r: 18 }
          ];
        }
        const [A, B] = state._balls;
        A.x += A.v;
        B.x += B.v;
        if (Math.abs(A.x - B.x) < A.r + B.r) {
          const elastic = state.elastic !== false;
          if (elastic) {
            const u1 = A.v;
            const u2 = B.v;
            A.v = ((A.m - B.m) / (A.m + B.m)) * u1 + ((2 * B.m) / (A.m + B.m)) * u2;
            B.v = ((2 * A.m) / (A.m + B.m)) * u1 + ((B.m - A.m) / (A.m + B.m)) * u2;
          } else {
            const v = (A.m * A.v + B.m * B.v) / (A.m + B.m);
            A.v = v;
            B.v = v;
          }
          A.x -= 2;
          B.x += 2;
        }
        if (A.x < A.r || A.x > w - A.r) A.v *= -1;
        if (B.x < B.r || B.x > w - B.r) B.v *= -1;
      } else if (preset === 'wave_1d') {
        state._phase = (state._phase || 0) + (Number(state.frequency) || 1) * 0.08;
      }
    }

    function draw() {
      ctx.clearRect(0, 0, w, h);
      if (preset === 'fusion_dt' || preset === 'particles2d') {
        // chamber ring
        ctx.strokeStyle = 'rgba(102,126,234,0.45)';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.ellipse(w / 2, h / 2, w * 0.38, h * 0.38, 0, 0, Math.PI * 2);
        ctx.stroke();
        particles.forEach((p) => {
          ctx.beginPath();
          ctx.fillStyle = p.species ? '#3498db' : '#e74c3c';
          ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
          ctx.fill();
        });
      } else if (preset === 'projectile') {
        ctx.strokeStyle = '#667eea';
        ctx.lineWidth = 2;
        ctx.beginPath();
        trail.forEach((p, i) => {
          if (i === 0) ctx.moveTo(p.x, p.y);
          else ctx.lineTo(p.x, p.y);
        });
        ctx.stroke();
        if (trail.length) {
          const p = trail[trail.length - 1];
          ctx.fillStyle = '#e74c3c';
          ctx.beginPath();
          ctx.arc(p.x, p.y, 6, 0, Math.PI * 2);
          ctx.fill();
        }
      } else if (preset === 'gravity_orbit') {
        const cx = w / 2;
        const cy = h / 2;
        ctx.fillStyle = '#f1c40f';
        ctx.beginPath();
        ctx.arc(cx, cy, 16, 0, Math.PI * 2);
        ctx.fill();
        const o = state._orb || { x: cx + 90, y: cy };
        ctx.fillStyle = '#3498db';
        ctx.beginPath();
        ctx.arc(o.x, o.y, 8, 0, Math.PI * 2);
        ctx.fill();
      } else if (preset === 'pendulum') {
        const cx = w / 2;
        const cy = 30;
        const L = state._L || 120;
        const x = cx + Math.sin(state._theta || 0) * L;
        const y = cy + Math.cos(state._theta || 0) * L;
        ctx.strokeStyle = '#aaa';
        ctx.beginPath();
        ctx.moveTo(cx, cy);
        ctx.lineTo(x, y);
        ctx.stroke();
        ctx.fillStyle = '#e74c3c';
        ctx.beginPath();
        ctx.arc(x, y, 12, 0, Math.PI * 2);
        ctx.fill();
      } else if (preset === 'spring_mass') {
        const base = 40;
        const x = w / 2 + (state._x || 0);
        const y = h / 2;
        ctx.strokeStyle = '#888';
        ctx.beginPath();
        for (let i = 0; i <= 12; i++) {
          const px = base + ((x - base) * i) / 12;
          const py = y + (i % 2 === 0 ? -10 : 10);
          if (i === 0) ctx.moveTo(px, y);
          else ctx.lineTo(px, py);
        }
        ctx.lineTo(x, y);
        ctx.stroke();
        ctx.fillStyle = '#667eea';
        ctx.fillRect(x - 16, y - 16, 32, 32);
      } else if (preset === 'collision_1d') {
        const balls = state._balls || [];
        ctx.strokeStyle = '#444';
        ctx.beginPath();
        ctx.moveTo(0, h / 2 + 20);
        ctx.lineTo(w, h / 2 + 20);
        ctx.stroke();
        balls.forEach((b, i) => {
          ctx.fillStyle = i ? '#e74c3c' : '#3498db';
          ctx.beginPath();
          ctx.arc(b.x, h / 2, b.r, 0, Math.PI * 2);
          ctx.fill();
        });
      } else if (preset === 'wave_1d') {
        const amp = Number(state.amplitude) || 40;
        const freq = Number(state.frequency) || 1;
        const phase = state._phase || 0;
        ctx.strokeStyle = '#667eea';
        ctx.lineWidth = 2;
        ctx.beginPath();
        for (let x = 0; x < w; x++) {
          const y = h / 2 + Math.sin(x * 0.03 * freq + phase) * amp;
          if (x === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.stroke();
      }
      if (outputsApi) outputsApi.refresh();
    }

    function loop(now) {
      if (!alive) return;
      const dt = Math.min(0.05, (now - t0) / 1000);
      t0 = now;
      step(dt);
      draw();
      raf = requestAnimationFrame(loop);
    }
    raf = requestAnimationFrame(loop);

    opts._update = () => {
      if (preset === 'projectile') step(0);
      draw();
    };

    return {
      destroy() {
        alive = false;
        cancelAnimationFrame(raf);
        host.innerHTML = '';
      }
    };
  }

  async function mountWidget(container, spec, options) {
    if (!container || !spec || !spec.behavior || !spec.behavior.preset) {
      return { destroy() {} };
    }
    const opts = options || {};
    const state = Object.assign({}, spec.state || {});
    const { card, viewHost, controls, outputsEl } = buildCard(spec);
    container.appendChild(card);

    const outputsApi = wireOutputs(outputsEl, state, spec.outputs || []);
    const runtime = { destroy() {} };
    const hook = { _update: null, _action: null };

    wireControls(
      controls,
      state,
      spec.inputs || [],
      () => {
        if (typeof hook._update === 'function') hook._update();
        outputsApi.refresh();
      },
      (action) => {
        if (typeof hook._action === 'function') hook._action(action);
        if (action === 'reset') {
          Object.assign(state, spec.state || {});
          if (typeof hook._update === 'function') hook._update();
          outputsApi.refresh();
        }
      }
    );

    const drawing = opts.skipDrawing ? null : showDrawingOverlay(viewHost);
    try {
      const preset = spec.behavior.preset;
      if (preset === 'desmos_graph') {
        Object.assign(runtime, await mountDesmos(viewHost, spec));
      } else if (preset === 'spinning_box' || preset === 'orbit_mesh' || preset === 'scene3d') {
        Object.assign(runtime, await mountThreePreset(viewHost, spec, state, hook));
      } else if (
        [
          'particles2d',
          'fusion_dt',
          'projectile',
          'gravity_orbit',
          'pendulum',
          'spring_mass',
          'collision_1d',
          'wave_1d'
        ].includes(preset)
      ) {
        Object.assign(runtime, mountCanvasSim(viewHost, spec, state, outputsApi, hook));
      } else {
        Object.assign(runtime, await mountJsxPreset(viewHost, spec, state, hook));
      }
      outputsApi.refresh();
    } catch (err) {
      console.error('mountWidget failed', err);
      viewHost.innerHTML = `<div class="vl-widget-error">Could not render this interactive (${escapeText(
        spec.behavior.preset
      )}).</div>`;
    } finally {
      hideDrawingOverlay(drawing);
      if (!opts.skipDrawing) {
        card.classList.add('vl-widget-fade-in');
      }
    }

    return {
      destroy() {
        if (runtime && typeof runtime.destroy === 'function') runtime.destroy();
        if (card.parentNode) card.parentNode.removeChild(card);
      },
      card,
      state
    };
  }

  async function ensureEngine() {
    return global.VeelearnWidgetEngine;
  }

  async function mountWidgets(container, widgets, options) {
    if (!container) return [];
    const list = Array.isArray(widgets) ? widgets : [];
    const handles = [];
    for (const spec of list) {
      // eslint-disable-next-line no-await-in-loop
      handles.push(await mountWidget(container, spec, options));
    }
    return handles;
  }

  global.VeelearnWidgetEngine = {
    mountWidget,
    mountWidgets,
    typesetMath,
    showDrawingOverlay,
    hideDrawingOverlay,
    ensureEngine
  };
})(typeof window !== 'undefined' ? window : globalThis);
