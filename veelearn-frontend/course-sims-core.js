/* ============================================================================
 * course-sims-core.js — interactive simulation engine for course content.
 *
 * Course HTML can contain:
 *   <div class="vl-sim" data-sim="projectile" data-title="...">
 *     <div class="vl-sim-cap">Optional caption shown under the canvas.</div>
 *   </div>
 *
 * The library file (course-sims-library.js) registers sim definitions with
 * CourseSims.register(key, spec). This file turns each .vl-sim node into a
 * canvas + sliders + live readout, runs the animation only while visible, and
 * re-mounts itself whenever new course HTML is injected.
 *
 * A sim spec is:
 *   {
 *     title:   string,
 *     blurb:   string,                       // one line under the title
 *     params:  [{ k, label, min, max, step, val, unit }],
 *     setup?:  (s) => void,                  // derive cached values
 *     draw:    (ctx, s, box, t) => void,     // box = { x, y, w, h }
 *     readout: (s) => [[label, value], ...],
 *     note?:   (s) => string                 // coaching line that can change
 *   }
 * ========================================================================== */
(function () {
  'use strict';

  const NS = (window.CourseSims = window.CourseSims || {});
  const registry = Object.create(null);
  const mounted = new WeakSet();

  const PALETTE = {
    ink: '#1f2937',
    soft: '#6b7280',
    line: '#e7e2da',
    accent: '#9A3412',
    blue: '#2563eb',
    cyan: '#0891b2',
    green: '#059669',
    amber: '#d97706',
    red: '#dc2626',
    paper: '#ffffff'
  };

  /* ---------- small helpers, exported for the library ---------- */

  function fmt(n, digits) {
    if (!isFinite(n)) return '—';
    const d = digits === undefined ? 2 : digits;
    const abs = Math.abs(n);
    if (abs >= 10000) return n.toExponential(2).replace('e+', 'e');
    return n.toFixed(d).replace(/\.0+$/, '').replace(/(\.\d*?)0+$/, '$1');
  }

  function clamp(v, lo, hi) {
    return Math.max(lo, Math.min(hi, v));
  }

  function lerp(a, b, t) {
    return a + (b - a) * t;
  }

  /** Draw a labelled plot and return value<->pixel mapping helpers. */
  function plot(ctx, box, opts) {
    const o = opts || {};
    const xmin = o.xmin !== undefined ? o.xmin : 0;
    const xmax = o.xmax !== undefined ? o.xmax : 1;
    const ymin = o.ymin !== undefined ? o.ymin : 0;
    const ymax = o.ymax !== undefined ? o.ymax : 1;
    const pad = o.pad || { l: 34, r: 8, t: 10, b: 20 };
    const x0 = box.x + pad.l;
    const y0 = box.y + pad.t;
    const w = box.w - pad.l - pad.r;
    const h = box.h - pad.t - pad.b;

    ctx.save();
    ctx.fillStyle = o.background || '#fdfaf5';
    ctx.fillRect(box.x, box.y, box.w, box.h);
    ctx.strokeStyle = PALETTE.line;
    ctx.lineWidth = 1;
    ctx.strokeRect(box.x + 0.5, box.y + 0.5, box.w - 1, box.h - 1);

    const X = (v) => x0 + ((v - xmin) / (xmax - xmin || 1)) * w;
    const Y = (v) => y0 + h - ((v - ymin) / (ymax - ymin || 1)) * h;

    const ticks = o.ticks === undefined ? 4 : o.ticks;
    ctx.strokeStyle = '#f0ece4';
    ctx.fillStyle = PALETTE.soft;
    ctx.font = '10px ui-sans-serif, system-ui, sans-serif';
    ctx.lineWidth = 1;
    for (let i = 0; i <= ticks; i++) {
      const vx = lerp(xmin, xmax, i / ticks);
      const vy = lerp(ymin, ymax, i / ticks);
      ctx.beginPath();
      ctx.moveTo(X(vx), y0);
      ctx.lineTo(X(vx), y0 + h);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(x0, Y(vy));
      ctx.lineTo(x0 + w, Y(vy));
      ctx.stroke();
      if (o.xlabels !== false) {
        ctx.textAlign = 'center';
        ctx.fillText(fmt(vx, o.xdigits === undefined ? 1 : o.xdigits), X(vx), y0 + h + 13);
      }
      if (o.ylabels !== false) {
        ctx.textAlign = 'right';
        ctx.fillText(fmt(vy, o.ydigits === undefined ? 1 : o.ydigits), x0 - 5, Y(vy) + 3);
      }
    }

    // axes through zero when the range straddles it
    ctx.strokeStyle = '#c9c2b6';
    if (ymin < 0 && ymax > 0) {
      ctx.beginPath();
      ctx.moveTo(x0, Y(0));
      ctx.lineTo(x0 + w, Y(0));
      ctx.stroke();
    }
    if (xmin < 0 && xmax > 0) {
      ctx.beginPath();
      ctx.moveTo(X(0), y0);
      ctx.lineTo(X(0), y0 + h);
      ctx.stroke();
    }

    if (o.xlabel) {
      ctx.fillStyle = PALETTE.soft;
      ctx.textAlign = 'right';
      ctx.fillText(o.xlabel, x0 + w, box.y + box.h - 4);
    }
    if (o.ylabel) {
      ctx.fillStyle = PALETTE.soft;
      ctx.textAlign = 'left';
      ctx.fillText(o.ylabel, box.x + 4, box.y + 11);
    }
    ctx.restore();

    return {
      X,
      Y,
      x0,
      y0,
      w,
      h,
      xmin,
      xmax,
      ymin,
      ymax,
      px: (v) => X(v),
      py: (v) => Y(v),
      // clip subsequent drawing to the plotting rectangle (used for tangents
      // and secants that run off the top or bottom of the axes)
      clipRect: () => {
        ctx.beginPath();
        ctx.rect(x0, y0, w, h);
        ctx.clip();
      },
      // clip a canvas y into the plot area so wild functions stay inside
      clipY: (v) => clamp(Y(v), y0, y0 + h)
    };
  }

  /** Sample f(x) and stroke it, splitting at non-finite jumps. */
  function curve(ctx, p, f, color, width, xmin, xmax, steps) {
    const a = xmin === undefined ? p.xmin : xmin;
    const b = xmax === undefined ? p.xmax : xmax;
    const n = steps || 240;
    ctx.save();
    ctx.strokeStyle = color;
    ctx.lineWidth = width || 2;
    ctx.lineJoin = 'round';
    ctx.beginPath();
    let pen = false;
    for (let i = 0; i <= n; i++) {
      const x = lerp(a, b, i / n);
      const y = f(x);
      if (!isFinite(y) || y > p.ymax * 8 || y < p.ymin * 8) {
        pen = false;
        continue;
      }
      const px = p.X(x);
      const py = p.clipY(y);
      if (pen) ctx.lineTo(px, py);
      else {
        ctx.moveTo(px, py);
        pen = true;
      }
    }
    ctx.stroke();
    ctx.restore();
  }

  function arrow(ctx, x1, y1, x2, y2, color, width) {
    const ang = Math.atan2(y2 - y1, x2 - x1);
    const head = 7;
    ctx.save();
    ctx.strokeStyle = color;
    ctx.fillStyle = color;
    ctx.lineWidth = width || 2;
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(x2, y2);
    ctx.lineTo(x2 - head * Math.cos(ang - 0.4), y2 - head * Math.sin(ang - 0.4));
    ctx.lineTo(x2 - head * Math.cos(ang + 0.4), y2 - head * Math.sin(ang + 0.4));
    ctx.closePath();
    ctx.fill();
    ctx.restore();
  }

  function dot(ctx, x, y, r, fill, stroke) {
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fillStyle = fill;
    ctx.fill();
    if (stroke) {
      ctx.strokeStyle = stroke;
      ctx.lineWidth = 1.5;
      ctx.stroke();
    }
  }

  function label(ctx, text, x, y, color, size, align) {
    ctx.save();
    ctx.fillStyle = color || PALETTE.ink;
    ctx.font = (size || 11) + 'px ui-sans-serif, system-ui, sans-serif';
    ctx.textAlign = align || 'center';
    ctx.fillText(text, x, y);
    ctx.restore();
  }

  NS.util = { fmt, clamp, lerp, plot, curve, arrow, dot, label, PALETTE };

  /* ---------- registration & mounting ---------- */

  function register(key, spec) {
    registry[key] = spec;
    // a library loaded after a hydrate pass: mount anything still waiting
    hydrate(document);
  }

  function buildControls(sim, state, rerender) {
    const wrap = document.createElement('div');
    wrap.className = 'vl-sim-controls';
    (sim.params || []).forEach((p) => {
      const row = document.createElement('label');
      row.className = 'vl-sim-control';

      const name = document.createElement('span');
      name.className = 'vl-sim-control-label';
      name.textContent = p.label;

      if (p.type === 'select') {
        const select = document.createElement('select');
        select.className = 'vl-sim-select';
        (p.options || []).forEach((opt) => {
          const option = document.createElement('option');
          option.value = String(opt.v);
          option.textContent = opt.label;
          if (String(state[p.k]) === String(opt.v)) option.selected = true;
          select.appendChild(option);
        });
        const value = document.createElement('span');
        value.className = 'vl-sim-control-value';
        value.textContent = '';
        select.addEventListener('change', () => {
          state[p.k] = select.value;
          if (sim.setup) sim.setup(state);
          rerender();
        });
        row.append(name, select, value);
        wrap.appendChild(row);
        return;
      }

      const input = document.createElement('input');
      input.type = 'range';
      input.min = p.min;
      input.max = p.max;
      input.step = p.step;
      input.value = state[p.k];
      input.setAttribute('aria-label', p.label);

      const value = document.createElement('span');
      value.className = 'vl-sim-control-value';
      const show = () => {
        value.textContent = fmt(state[p.k], p.decimals === undefined ? (p.step < 1 ? 2 : 0) : p.decimals) + (p.unit ? ' ' + p.unit : '');
      };
      show();

      input.addEventListener('input', () => {
        state[p.k] = parseFloat(input.value);
        show();
        if (sim.setup) sim.setup(state);
        rerender();
      });

      row.append(name, input, value);
      wrap.appendChild(row);
    });
    return wrap;
  }

  function mount(host) {
    if (mounted.has(host)) return;
    const key = host.dataset.sim;
    const sim = registry[key];
    if (!sim) return; // library not registered yet; a later hydrate picks it up
    mounted.add(host);
    host.dataset.simMounted = '1';

    const state = {};
    (sim.params || []).forEach((p) => {
      const override = host.dataset[p.k];
      state[p.k] = override !== undefined && override !== '' ? parseFloat(override) : p.val;
    });
    if (host.dataset.mode) state.mode = host.dataset.mode;
    if (sim.setup) sim.setup(state);

    host.classList.add('vl-sim-live');
    host.innerHTML = '';

    const head = document.createElement('div');
    head.className = 'vl-sim-head';
    const title = document.createElement('div');
    title.className = 'vl-sim-title';
    title.textContent = host.dataset.title || sim.title;
    head.appendChild(title);
    if (sim.blurb) {
      const blurb = document.createElement('div');
      blurb.className = 'vl-sim-blurb';
      blurb.textContent = sim.blurb;
      head.appendChild(blurb);
    }
    host.appendChild(head);

    const stage = document.createElement('div');
    stage.className = 'vl-sim-stage';
    const canvas = document.createElement('canvas');
    canvas.className = 'vl-sim-canvas';
    canvas.setAttribute('role', 'img');
    canvas.setAttribute('aria-label', sim.title + ' interactive simulation');
    stage.appendChild(canvas);
    host.appendChild(stage);

    const controls = buildControls(sim, state, () => drawOnce());
    if (controls.children.length) host.appendChild(controls);

    const readout = document.createElement('div');
    readout.className = 'vl-sim-readout';
    host.appendChild(readout);

    const note = document.createElement('p');
    note.className = 'vl-sim-note';
    host.appendChild(note);

    const caption = host.querySelector('.vl-sim-cap');
    if (caption) {
      const tail = document.createElement('p');
      tail.className = 'vl-sim-caption';
      tail.textContent = caption.textContent;
      host.appendChild(tail);
    }

    const ctx = canvas.getContext('2d');
    let width = 0;
    let height = 0;
    let visible = false;
    let t0 = performance.now();
    let t = 0;

    function resize() {
      // clientWidth excludes the stage border, so the canvas never forces a
      // scrollbar inside the card.
      const cssW = Math.max(240, Math.round(stage.clientWidth || stage.getBoundingClientRect().width));
      const h = sim.height || Math.min(300, Math.max(200, cssW * 0.5));
      const cssH = Math.round(Math.min(380, Math.max(180, h)));
      const dpr = Math.min(2, window.devicePixelRatio || 1);
      canvas.width = Math.round(cssW * dpr);
      canvas.height = Math.round(cssH * dpr);
      canvas.style.width = cssW + 'px';
      canvas.style.height = cssH + 'px';
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      width = cssW;
      height = cssH;
      drawOnce();
    }

    function paint(time) {
      t = time;
      ctx.clearRect(0, 0, width, height);
      ctx.fillStyle = PALETTE.paper;
      ctx.fillRect(0, 0, width, height);
      try {
        sim.draw(ctx, state, { x: 8, y: 8, w: width - 16, h: height - 16 }, t);
      } catch (err) {
        ctx.fillStyle = PALETTE.red;
        ctx.font = '12px ui-sans-serif, system-ui, sans-serif';
        ctx.fillText('Simulation error', 16, 24);
      }
    }

    function updateText() {
      const rows = sim.readout ? sim.readout(state) : [];
      readout.innerHTML = '';
      rows.forEach(([k, v]) => {
        const cell = document.createElement('div');
        cell.className = 'vl-sim-metric';
        const keyEl = document.createElement('span');
        keyEl.className = 'vl-sim-metric-key';
        keyEl.textContent = k;
        const valEl = document.createElement('strong');
        valEl.className = 'vl-sim-metric-value';
        valEl.textContent = v;
        cell.append(keyEl, valEl);
        readout.appendChild(cell);
      });
      if (sim.note) {
        const msg = sim.note(state);
        note.textContent = msg || '';
        note.style.display = msg ? '' : 'none';
      }
    }

    let textClock = 0;
    function drawOnce() {
      paint(performance.now());
      updateText();
    }

    function frame(now) {
      if (!visible) return;
      paint(now);
      if (now - textClock > 120) {
        textClock = now;
        updateText();
      }
      requestAnimationFrame(frame);
    }

    if ('ResizeObserver' in window) {
      new ResizeObserver(resize).observe(stage);
    } else {
      window.addEventListener('resize', resize);
    }

    if ('IntersectionObserver' in window) {
      new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            const was = visible;
            visible = entry.isIntersecting;
            if (visible && !was) requestAnimationFrame(frame);
          });
        },
        { rootMargin: '120px' }
      ).observe(host);
    } else {
      visible = true;
      requestAnimationFrame(frame);
    }

    resize();
    t0 = performance.now();
    t = t0;
  }

  function hydrate(root) {
    const scope = root && root.querySelectorAll ? root : document;
    const nodes = scope.querySelectorAll('.vl-sim[data-sim]');
    nodes.forEach((node) => {
      if (node.dataset.simMounted === '1') return;
      mount(node);
    });
  }

  NS.register = register;
  NS.hydrate = hydrate;
  NS.registry = registry;

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => hydrate(document));
  } else {
    hydrate(document);
  }

  // Course HTML is injected by the SPA, the standalone viewer and the editor,
  // so watch for new nodes rather than relying on a single hook.
  if ('MutationObserver' in window) {
    let queued = false;
    new MutationObserver(() => {
      if (queued) return;
      queued = true;
      requestAnimationFrame(() => {
        queued = false;
        hydrate(document);
      });
    }).observe(document.body, { childList: true, subtree: true });
  }
})();
