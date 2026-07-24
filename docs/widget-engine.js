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
    host.style.minHeight = host.style.minHeight || '320px';
    host.style.width = '100%';
    host.style.background = '#0f1220';

    // Force light text on dark boards (JSXGraph defaults are near-black)
    try {
      JXG.Options.text.strokeColor = '#f8fafc';
      JXG.Options.text.highlightStrokeColor = '#ffffff';
      JXG.Options.text.cssDefaultStyle = 'color:#f8fafc;fill:#f8fafc;font-family:Arial,sans-serif;font-weight:700;';
      JXG.Options.text.highlightCssDefaultStyle =
        'color:#ffffff;fill:#ffffff;font-family:Arial,sans-serif;font-weight:700;';
      JXG.Options.point.label = JXG.Options.point.label || {};
      JXG.Options.point.label.strokeColor = '#f8fafc';
      JXG.Options.point.label.highlightStrokeColor = '#ffffff';
      JXG.Options.point.label.cssDefaultStyle =
        'color:#f8fafc !important;fill:#f8fafc !important;font-weight:700;text-shadow:0 1px 3px rgba(0,0,0,.95);';
      JXG.Options.point.label.highlightCssDefaultStyle =
        'color:#ffffff !important;fill:#ffffff !important;font-weight:700;';
    } catch (_) {
      /* ignore */
    }

    const board = JXG.JSXGraph.initBoard(id, {
      boundingbox: Array.isArray(bb) && bb.length === 4 ? bb : [-1, 6, 6, -1],
      axis: true,
      grid: true,
      showCopyright: false,
      showNavigation: true,
      pan: { enabled: true, needTwoFingers: false },
      zoom: { enabled: true },
      keepaspectratio: true,
      defaultAxes: {
        x: {
          strokeColor: '#8b93a7',
          highlight: false,
          ticks: {
            strokeColor: '#8b93a7',
            label: {
              strokeColor: '#f8fafc',
              highlightStrokeColor: '#ffffff',
              cssClass: 'vl-jxg-label',
              highlightCssClass: 'vl-jxg-label',
              cssDefaultStyle: 'color:#f8fafc !important;font-weight:700;'
            }
          }
        },
        y: {
          strokeColor: '#8b93a7',
          highlight: false,
          ticks: {
            strokeColor: '#8b93a7',
            label: {
              strokeColor: '#f8fafc',
              highlightStrokeColor: '#ffffff',
              cssClass: 'vl-jxg-label',
              highlightCssClass: 'vl-jxg-label',
              cssDefaultStyle: 'color:#f8fafc !important;font-weight:700;'
            }
          }
        }
      }
    });
    // Ensure layout after mount (empty boards often mean 0×0 host on first paint)
    requestAnimationFrame(() => {
      try {
        if (typeof board.resize === 'function') board.resize();
        board.fullUpdate();
        restyleBoardLabels(host);
        setTimeout(() => restyleBoardLabels(host), 50);
        setTimeout(() => restyleBoardLabels(host), 250);
      } catch (_) {
        /* ignore */
      }
    });
    return board;
  }

  function readCoord(el, key, fallback) {
    if (el == null) return fallback;
    if (el[key] != null && Number.isFinite(Number(el[key]))) return Number(el[key]);
    if (Array.isArray(el.coords) && el.coords.length >= 2) {
      return Number(el.coords[key === 'x' ? 0 : 1]);
    }
    if (Array.isArray(el.pos) && el.pos.length >= 2) {
      return Number(el.pos[key === 'x' ? 0 : 1]);
    }
    if (Array.isArray(el.position) && el.position.length >= 2) {
      return Number(el.position[key === 'x' ? 0 : 1]);
    }
    const n = Number(el[key]);
    return Number.isFinite(n) ? n : fallback;
  }

  function pointOpts(el, color) {
    return {
      name: el.label || el.name || '',
      size: 4,
      fixed: el.fixed === false ? false : true,
      color: resolveColor(color || el.color, '#ff6b6b'),
      fillColor: resolveColor(color || el.color, '#ff6b6b'),
      strokeColor: '#ffffff',
      strokeWidth: 1,
      label: {
        strokeColor: '#ffffff',
        highlightStrokeColor: '#ffffff',
        fontSize: 16,
        cssClass: 'vl-jxg-label',
        highlightCssClass: 'vl-jxg-label',
        cssDefaultStyle:
          'color:#ffffff !important;fill:#ffffff !important;font-weight:800;text-shadow:0 0 4px #000,0 1px 3px #000;',
        highlightCssDefaultStyle: 'color:#ffffff !important;fill:#ffffff !important;font-weight:800;',
        offset: [10, 10]
      },
      highlight: false,
      showInfobox: false
    };
  }

  function restyleBoardLabels(host) {
    if (!host) return;
    host.querySelectorAll('.JXGtext, .vl-jxg-label, text').forEach((node) => {
      try {
        node.style.setProperty('color', '#ffffff', 'important');
        node.style.setProperty('fill', '#ffffff', 'important');
        node.style.setProperty('font-weight', '800', 'important');
        node.style.setProperty('text-shadow', '0 0 4px #000, 0 1px 3px #000', 'important');
        if (node.tagName === 'text') {
          node.setAttribute('fill', '#ffffff');
          node.setAttribute('stroke', 'none');
        }
      } catch (_) {
        /* ignore */
      }
    });
  }

  function sideLen(ax, ay, bx, by) {
    const dx = bx - ax;
    const dy = by - ay;
    return Math.sqrt(dx * dx + dy * dy);
  }

  function createIncircle(board, p1, p2, p3, el) {
    const stroke = resolveColor(el.color, '#22d3ee');
    try {
      const circle = board.create('incircle', [p1, p2, p3], {
        strokeColor: stroke,
        strokeWidth: 2.5,
        fillColor: stroke,
        fillOpacity: 0.14,
        fixed: true,
        highlight: false
      });
      const incenter = board.create(
        'incenter',
        [p1, p2, p3],
        pointOpts({ name: el.label || 'I', label: el.label || 'I', color: el.color || '#22d3ee' }, '#22d3ee')
      );
      return { circle, incenter };
    } catch (_) {
      /* fall through to manual */
    }
    const x1 = p1.X();
    const y1 = p1.Y();
    const x2 = p2.X();
    const y2 = p2.Y();
    const x3 = p3.X();
    const y3 = p3.Y();
    const a = sideLen(x2, y2, x3, y3);
    const b = sideLen(x1, y1, x3, y3);
    const c = sideLen(x1, y1, x2, y2);
    const peri = a + b + c;
    if (!(peri > 0)) throw new Error('degenerate triangle');
    const ix = (a * x1 + b * x2 + c * x3) / peri;
    const iy = (a * y1 + b * y2 + c * y3) / peri;
    const area2 = Math.abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2);
    const r = area2 / (peri / 2);
    const incenter = board.create(
      'point',
      [ix, iy],
      pointOpts({ name: el.label || 'I', label: el.label || 'I', color: el.color || '#22d3ee' }, '#22d3ee')
    );
    const circle = board.create('circle', [incenter, r], {
      strokeColor: stroke,
      strokeWidth: 2.5,
      fillColor: stroke,
      fillOpacity: 0.14,
      fixed: true,
      highlight: false
    });
    return { circle, incenter };
  }

  function applyGeometryElements(board, JXG, elements, named) {
    const map = named || {};
    (elements || []).forEach((el) => {
      try {
        if (el.type === 'point') {
          const hasX =
            el.x != null ||
            (Array.isArray(el.coords) && el.coords.length >= 2) ||
            (Array.isArray(el.pos) && el.pos.length >= 2) ||
            (Array.isArray(el.position) && el.position.length >= 2);
          const hasY =
            el.y != null ||
            (Array.isArray(el.coords) && el.coords.length >= 2) ||
            (Array.isArray(el.pos) && el.pos.length >= 2) ||
            (Array.isArray(el.position) && el.position.length >= 2);
          if (!hasX || !hasY) {
            console.warn('geometry point missing coordinates, skipping', el);
            return;
          }
          const x = readCoord(el, 'x', NaN);
          const y = readCoord(el, 'y', NaN);
          if (!Number.isFinite(x) || !Number.isFinite(y)) {
            console.warn('geometry point invalid coordinates, skipping', el);
            return;
          }
          map[el.name] = board.create('point', [x, y], pointOpts(el));
        } else if (el.type === 'segment' && map[el.from] && map[el.to]) {
          map[el.name] = board.create('segment', [map[el.from], map[el.to]], {
            strokeColor: resolveColor(el.color, '#6ea8fe'),
            strokeWidth: 2,
            fixed: true,
            highlight: false
          });
        } else if (el.type === 'line' && map[el.from] && map[el.to]) {
          map[el.name] = board.create('line', [map[el.from], map[el.to]], {
            strokeColor: resolveColor(el.color, '#6ea8fe'),
            strokeWidth: 2,
            fixed: true,
            highlight: false
          });
        } else if (el.type === 'ray' && map[el.from] && map[el.to]) {
          map[el.name] = board.create('line', [map[el.from], map[el.to]], {
            straightFirst: false,
            straightLast: true,
            strokeColor: resolveColor(el.color, '#6ea8fe'),
            strokeWidth: 2,
            fixed: true,
            highlight: false
          });
        } else if (el.type === 'circle') {
          if (map[el.center] && map[el.through]) {
            map[el.name] = board.create('circle', [map[el.center], map[el.through]], {
              strokeColor: resolveColor(el.color, '#c084fc'),
              strokeWidth: 2,
              fixed: true,
              highlight: false
            });
          } else if (map[el.center] && el.radius != null) {
            map[el.name] = board.create('circle', [map[el.center], Number(el.radius)], {
              strokeColor: resolveColor(el.color, '#c084fc'),
              strokeWidth: 2,
              fixed: true,
              highlight: false
            });
          }
        } else if (el.type === 'polygon' && Array.isArray(el.points)) {
          const pts = el.points.map((n) => map[n]).filter(Boolean);
          if (pts.length >= 3) {
            map[el.name] = board.create('polygon', pts, {
              fillColor: resolveColor(el.color, '#6ea8fe'),
              fillOpacity: 0.22,
              borders: { strokeColor: resolveColor(el.color, '#6ea8fe'), strokeWidth: 2 },
              fixed: true,
              highlight: false
            });
          }
        } else if (el.type === 'midpoint' && map[el.from] && map[el.to]) {
          map[el.name] = board.create('midpoint', [map[el.from], map[el.to]], pointOpts(el, '#fbbf24'));
        } else if (el.type === 'intersection' && map[el.from] && map[el.to]) {
          map[el.name] = board.create('intersection', [map[el.from], map[el.to], 0], pointOpts(el, '#4ade80'));
        } else if (el.type === 'incircle' && Array.isArray(el.points)) {
          const pts = el.points.map((n) => map[n]).filter(Boolean);
          if (pts.length >= 3) {
            const made = createIncircle(board, pts[0], pts[1], pts[2], el);
            map[el.name] = made.circle;
            map[`${el.name}_I`] = made.incenter;
          }
        } else if (el.type === 'incenter' && Array.isArray(el.points)) {
          const pts = el.points.map((n) => map[n]).filter(Boolean);
          if (pts.length >= 3) {
            map[el.name] = board.create(
              'incenter',
              [pts[0], pts[1], pts[2]],
              pointOpts(el, '#22d3ee')
            );
          }
        } else if (el.type === 'function' && el.expr) {
          const fn = compileExpr(el.expr, ['x']);
          map[el.name] = board.create('functiongraph', [(x) => fn(x, {})], {
            strokeColor: resolveColor(el.color, '#f87171'),
            strokeWidth: 2
          });
        } else if (el.type === 'text') {
          board.create('text', [readCoord(el, 'x', 0), readCoord(el, 'y', 0), el.text || ''], {
            fontSize: 14,
            strokeColor: '#ffffff',
            cssClass: 'vl-jxg-label',
            highlightCssClass: 'vl-jxg-label',
            cssDefaultStyle: 'color:#ffffff !important;fill:#ffffff !important;font-weight:800;'
          });
        } else if (el.type === 'vector' && map[el.from] && map[el.to]) {
          map[el.name] = board.create('arrow', [map[el.from], map[el.to]], {
            strokeColor: resolveColor(el.color, '#fb923c'),
            strokeWidth: 2,
            fixed: true,
            highlight: false
          });
        }
      } catch (err) {
        console.warn('geometry element failed', el, err);
      }
    });
    try {
      const host = board.containerObj || (board.container && document.getElementById(board.container));
      restyleBoardLabels(host);
      requestAnimationFrame(() => restyleBoardLabels(host));
    } catch (_) {
      /* ignore */
    }
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
          board.create('point', [readCoord(el, 'x', 0), 0], pointOpts(el));
        }
      });
      if (state.point != null) {
        const p = board.create(
          'point',
          [Number(state.point) || 0, 0],
          pointOpts({ name: 'P', label: 'P', color: '#e74c3c', fixed: false })
        );
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
        pointOpts({ name: 'P', label: 'P', color: '#e74c3c', fixed: false })
      );
      board.create('segment', [[0, 0], tip], { strokeColor: '#e74c3c' });
      opts._update = () => board.update();
      return { board };
    }

    if (preset === 'triangle_lab') {
      const a = Number(state.a != null ? state.a : params.a) || 3;
      const b = Number(state.b != null ? state.b : params.b) || 4;
      const c = Number(state.c != null ? state.c : params.c) || 5;
      const A = board.create('point', [0, 0], pointOpts({ name: 'A', label: 'A' }));
      const B = board.create('point', [c, 0], pointOpts({ name: 'B', label: 'B' }));
      const cosA = (b * b + c * c - a * a) / (2 * b * c);
      const sinA = Math.sqrt(Math.max(0, 1 - cosA * cosA));
      const C = board.create('point', [b * cosA, b * sinA], pointOpts({ name: 'C', label: 'C' }));
      board.create('polygon', [A, B, C], {
        fillColor: '#667eea',
        fillOpacity: 0.2,
        borders: { strokeColor: '#6ea8fe', strokeWidth: 2 },
        fixed: true,
        highlight: false
      });
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
    try {
      const Desmos = await ensureDesmos();
      if (!Desmos || typeof Desmos.GraphingCalculator !== 'function') {
        throw new Error('Desmos API unavailable');
      }
      host.innerHTML = '';
      const el = document.createElement('div');
      el.style.width = '100%';
      el.style.height = '100%';
      el.style.minHeight = '280px';
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
    } catch (err) {
      console.warn('Desmos unavailable, falling back to function_plot', err);
      const fallback = Object.assign({}, spec, {
        behavior: Object.assign({}, spec.behavior, {
          preset: 'function_plot',
          params: Object.assign({}, (spec.behavior && spec.behavior.params) || {}, {
            boundingbox: [-6, 6, 6, -6]
          })
        })
      });
      return mountJsxPreset(host, fallback, Object.assign({}, spec.state || {}), { _update: null });
    }
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
    const w = Math.max(host.clientWidth || 0, 320);
    const h = Math.max(host.clientHeight || 0, 260);
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

    function n(v, fallback) {
      const x = Number(v);
      return Number.isFinite(x) ? x : fallback;
    }

    let alive = true;
    let raf = 0;
    let t0 = performance.now();
    const particles = [];
    let energy = n(state.energyMeV, 0);
    const rateSeries = Array.isArray(state.fusionRateSeries) ? state.fusionRateSeries.slice() : [];
    let trail = [];
    let lastDensity = -1;

    function spawnParticle(species) {
      const temp = Math.max(1, n(state.temperature, 10));
      const sp = Math.sqrt(temp) * 0.8;
      return {
        x: Math.random() * w,
        y: Math.random() * h,
        vx: (Math.random() - 0.5) * sp,
        vy: (Math.random() - 0.5) * sp,
        species: species == null ? (Math.random() < 0.5 ? 0 : 1) : species,
        r: species ? 4 : 3
      };
    }

    function syncParticleCount(force) {
      const dens = Math.max(10, Math.min(120, Math.round(n(state.density, 50))));
      if (!force && dens === lastDensity) return;
      lastDensity = dens;
      while (particles.length < dens) particles.push(spawnParticle(particles.length % 2));
      while (particles.length > dens) particles.pop();
    }

    function resetParticles() {
      particles.length = 0;
      lastDensity = -1;
      syncParticleCount(true);
      energy = 0;
      rateSeries.length = 0;
      trail = [];
      state.energyMeV = 0;
      state.fusionRateSeries = [];
      state._orb = null;
      state._theta = null;
      state._omega = null;
      state._x = null;
      state._v = null;
      state._balls = null;
      state._phase = 0;
    }
    resetParticles();

    opts._action = (action) => {
      if (action === 'reset') resetParticles();
    };
    opts._update = () => {
      if (preset === 'fusion_dt' || preset === 'particles2d') syncParticleCount(true);
      if (preset === 'projectile') step(0);
      if (preset === 'pendulum' && state.angle != null) {
        state._theta = (n(state.angle, 40) * Math.PI) / 180;
        state._omega = 0;
      }
      if (preset === 'collision_1d') {
        state._balls = null;
      }
      draw();
    };

    function step(dt) {
      if (state.paused) return;
      const temp = Math.max(1, n(state.temperature, 10));
      const mag = Math.max(1, n(state.magneticField, 50));
      const dens = Math.max(10, n(state.density, 50));

      if (preset === 'fusion_dt' || preset === 'particles2d') {
        syncParticleCount(false);
        // Strong, visible response to temperature
        const speedScale = Math.sqrt(temp) * 0.85;
        let fusions = 0;
        const fuseDist = n(params.fusionDistance, 10);
        const ePer = n(params.energyPerFusionMeV, 17.6);
        // Higher mag → tighter pull to center (visible confinement)
        const pull = mag / 35;
        particles.forEach((p) => {
          p.vx += (Math.random() - 0.5) * 0.55 * speedScale;
          p.vy += (Math.random() - 0.5) * 0.55 * speedScale;
          const cx = w / 2;
          const cy = h / 2;
          p.vx += ((cx - p.x) / w) * pull;
          p.vy += ((cy - p.y) / h) * pull;
          const maxV = 1.2 + speedScale * 1.4;
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
          // Fusion rate rises sharply with temp & density
          const fuseChance = Math.min(0.45, (temp * temp * dens) / 80000);
          for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
              const a = particles[i];
              const b = particles[j];
              if (a.species === b.species) continue;
              const dx = a.x - b.x;
              const dy = a.y - b.y;
              if (dx * dx + dy * dy < fuseDist * fuseDist && Math.random() < fuseChance) {
                fusions++;
                energy += ePer;
                Object.assign(a, spawnParticle(0));
                Object.assign(b, spawnParticle(1));
              }
            }
          }
          rateSeries.push(fusions);
          if (rateSeries.length > 48) rateSeries.shift();
          state.energyMeV = Math.round(energy * 10) / 10;
          state.fusionRateSeries = rateSeries.slice();
        }
      } else if (preset === 'projectile') {
        const angle = (n(state.angle, 45) * Math.PI) / 180;
        const speed = n(state.speed, 40);
        const g = n(state.g, 9.8);
        trail = [];
        let x = 40;
        let y = h - 40;
        let vx = Math.cos(angle) * speed;
        let vy = -Math.sin(angle) * speed;
        for (let i = 0; i < 240; i++) {
          trail.push({ x, y });
          vy += g * 0.12;
          x += vx * 0.12;
          y += vy * 0.12;
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
        const G = n(state.gravity, 1200);
        o.vx += (G * dx) / (dist * dist * dist);
        o.vy += (G * dy) / (dist * dist * dist);
        o.x += o.vx;
        o.y += o.vy;
      } else if (preset === 'pendulum') {
        if (state._theta == null) state._theta = (n(state.angle, 40) * Math.PI) / 180;
        if (state._omega == null) state._omega = 0;
        const L = Math.max(40, n(state.length, 120));
        const g = n(state.g, 9.8);
        state._omega += (-(g / (L / 40)) * Math.sin(state._theta)) * 0.05;
        state._theta += state._omega * 0.05;
        state._omega *= 0.999;
        state._L = L;
      } else if (preset === 'spring_mass') {
        if (state._x == null) state._x = n(state.displacement, 40);
        if (state._v == null) state._v = 0;
        const k = n(state.k, 0.08);
        const m = Math.max(0.2, n(state.mass, 1));
        state._v += ((-k * state._x) / m) * 0.4;
        state._x += state._v;
        state._v *= 0.995;
      } else if (preset === 'collision_1d') {
        if (!state._balls) {
          state._balls = [
            { x: 80, v: n(state.v1, 2), m: n(state.m1, 1), r: 14 },
            { x: w - 100, v: n(state.v2, -1.2), m: n(state.m2, 1.5), r: 18 }
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
        const freq = Math.max(0.05, n(state.frequency, 1));
        const speed = n(state.speed != null ? state.speed : state.waveSpeed, 1);
        // speed=0 freezes the wave; amplitude=0 is a flat line (not "high")
        state._phase = (state._phase || 0) + freq * speed * 0.12;
      }
    }

    function draw() {
      ctx.clearRect(0, 0, w, h);
      if (preset === 'fusion_dt' || preset === 'particles2d') {
        const temp = Math.max(1, n(state.temperature, 10));
        const mag = Math.max(1, n(state.magneticField, 50));
        // Chamber glow scales with temperature
        const glow = Math.min(0.55, temp / 70);
        ctx.strokeStyle = `rgba(102,126,234,${0.25 + glow})`;
        ctx.lineWidth = 2 + mag / 40;
        ctx.beginPath();
        ctx.ellipse(w / 2, h / 2, w * 0.38, h * 0.38, 0, 0, Math.PI * 2);
        ctx.stroke();
        if (glow > 0.05) {
          const g = ctx.createRadialGradient(w / 2, h / 2, 10, w / 2, h / 2, Math.min(w, h) * 0.4);
          g.addColorStop(0, `rgba(255,120,60,${glow * 0.35})`);
          g.addColorStop(1, 'rgba(15,18,32,0)');
          ctx.fillStyle = g;
          ctx.fillRect(0, 0, w, h);
        }
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
        // Allow amplitude === 0 (flat line). Do NOT treat 0 as missing.
        const amp = n(state.amplitude, 40);
        const freq = Math.max(0.05, n(state.frequency, 1));
        const phase = state._phase || 0;
        const k = 0.028 * freq;
        ctx.strokeStyle = '#667eea';
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        for (let x = 0; x < w; x++) {
          const y = h / 2 + Math.sin(x * k + phase) * amp;
          if (x === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.stroke();
        // Zero line
        ctx.strokeStyle = 'rgba(255,255,255,0.15)';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(0, h / 2);
        ctx.lineTo(w, h / 2);
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
