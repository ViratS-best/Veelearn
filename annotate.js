/**
 * The annotation vocabulary: twelve primitives on one SVG layer over the problem
 * column, so the mascot can point at the actual words.
 *
 *   underline · highlight · circle · ellipse-with-label · arrow · curved pointer
 *   strike · box · brace · underline-sweep · stamp · shake
 *
 * Every primitive takes {anchor, text?, color?, ms?, delay?}, resolves a DOM
 * target (using Range.getClientRects for a phrase so wrapped text yields one
 * stroke per line), animates, and resolves a promise. Every primitive also has a
 * text equivalent: the layer is aria-hidden and the sentences go to a polite live
 * region, so a screen-reader user gets the same explanation.
 */
(function (global) {
  'use strict';

  const MAX_LIVE = 12;
  const DEFAULT_MS = 520;
  const ACCENT = '#ea580c';
  const GOOD = '#0f7b52';
  const BAD = '#b42318';

  const state = {
    layer: null,
    container: null,
    live: null,
    shapes: [],
    seq: 0,
    reduced: false,
    narrator: null,
    board: null
  };

  const prefersReduced = () =>
    typeof global.matchMedia === 'function' && global.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /** Primitives take {anchor, ...}; a bare selector is accepted as a shorthand. */
  function optsOf(o) {
    if (typeof o === 'string') return { anchor: o };
    return o || {};
  }

  function svgEl(tag, attrs) {
    const el = document.createElementNS('http://www.w3.org/2000/svg', tag);
    Object.keys(attrs || {}).forEach((k) => {
      el.setAttribute(k, attrs[k]);
    });
    return el;
  }

  function q(sel) {
    return sel && typeof sel === 'string' ? document.querySelector(sel) : sel;
  }

  /** Human label for a target: named slots read better than raw text. */
  function labelOf(el) {
    if (!el) return 'the problem';
    const slot = el.getAttribute && el.getAttribute('data-annotate');
    const names = { stem: 'the question', why: 'the explanation', hint: 'the hint', solution: 'the worked steps', board: 'the board' };
    if (slot && names[slot]) return names[slot];
    if (slot && /^opt-/.test(slot)) return `option ${slot.slice(4)}`;
    const txt = (el.textContent || '').trim().replace(/\s+/g, ' ');
    return txt ? `“${txt.slice(0, 60)}”` : 'the problem';
  }

  /** Rects of `text` inside `el`, in layer coordinates. Falls back to the element. */
  function rectsFor(el, text) {
    if (!el) return [];
    const layer = state.layer.getBoundingClientRect();
    let raw = [];

    if (text) {
      const needle = String(text);
      const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null);
      let node = walker.nextNode();
      while (node) {
        const idx = node.nodeValue.indexOf(needle);
        if (idx !== -1) {
          const range = document.createRange();
          range.setStart(node, idx);
          range.setEnd(node, idx + needle.length);
          raw = Array.from(range.getClientRects());
          break;
        }
        node = walker.nextNode();
      }
    }
    if (!raw.length) raw = [el.getBoundingClientRect()];

    return raw
      .filter((r) => r.width > 0.5 || r.height > 0.5)
      .map((r) => ({ left: r.left - layer.left, top: r.top - layer.top, width: r.width, height: r.height }));
  }

  function union(rects) {
    if (!rects.length) return { left: 0, top: 0, width: 0, height: 0 };
    const left = Math.min(...rects.map((r) => r.left));
    const top = Math.min(...rects.map((r) => r.top));
    const right = Math.max(...rects.map((r) => r.left + r.width));
    const bottom = Math.max(...rects.map((r) => r.top + r.height));
    return { left, top, width: right - left, height: bottom - top };
  }

  function announce(sentence) {
    if (!state.live) return;
    const p = document.createElement('p');
    p.textContent = sentence;
    state.live.appendChild(p);
    // keep the region short: the last three sentences are enough
    while (state.live.childElementCount > 3) state.live.removeChild(state.live.firstElementChild);
  }

  function keep(el) {
    state.shapes.push(el);
    while (state.shapes.length > MAX_LIVE) {
      const old = state.shapes.shift();
      if (old && old.remove) old.remove();
    }
  }

  function title(el, sentence) {
    const t = svgEl('title');
    t.textContent = sentence;
    el.appendChild(t);
  }

  function animateDash(el, len, ms) {
    el.style.strokeDasharray = `${len}`;
    el.style.strokeDashoffset = `${len}`;
    void el.getBoundingClientRect();
    el.style.transition = `stroke-dashoffset ${ms}ms ease-out`;
    el.style.strokeDashoffset = '0';
  }

  function settle(ms, delay) {
    if (state.reduced) return Promise.resolve();
    return new Promise((resolve) => setTimeout(resolve, (ms || 0) + (delay || 0)));
  }

  function detached(err) {
    return Promise.resolve({ ok: false, error: err && err.message ? err.message : 'annotation target missing' });
  }

  // ------------------------------------------------------------- primitives
  function underline(opts) {
    const o = optsOf(opts);
    const el = q(o.anchor);
    if (!el) return detached(new Error('missing anchor'));
    const rects = rectsFor(el, o.text);
    const color = o.color || ACCENT;
    const ms = o.ms || 320;
    const group = svgEl('g', { class: 'annot annot-underline' });
    const sentence = `Underlined ${o.text ? `“${o.text}”` : labelOf(el)}.`;
    title(group, sentence);

    rects.forEach((r, i) => {
      const line = svgEl('line', {
        x1: r.left,
        x2: r.left + r.width,
        y1: r.top + r.height - 1.5,
        y2: r.top + r.height - 1.5,
        stroke: color,
        'stroke-width': 2.4,
        'stroke-linecap': 'round'
      });
      group.appendChild(line);
      animateDash(line, r.width, state.reduced ? 0 : ms);
      if (i === 0 && !state.reduced) {
        line.style.transitionDelay = `${o.delay || 0}ms`;
      }
    });

    state.layer.appendChild(group);
    keep(group);
    announce(sentence);
    return settle(ms, o.delay).then(() => ({ ok: true, kind: 'underline', sentence }));
  }

  function sweep(opts) {
    const o = optsOf(opts);
    const el = q(o.anchor);
    if (!el) return detached(new Error('missing anchor'));
    const rects = rectsFor(el, o.text);
    const color = o.color || ACCENT;
    const ms = o.ms || 700;
    const group = svgEl('g', { class: 'annot annot-sweep' });
    const sentence = `Underlined ${o.text ? `“${o.text}”` : labelOf(el)} as it was written.`;
    title(group, sentence);

    rects.forEach((r) => {
      const pen = svgEl('path', {
        d: `M ${r.left} ${r.top + r.height - 2} q ${r.width / 2} 4 ${r.width} 0`,
        fill: 'none',
        stroke: color,
        'stroke-width': 3.2,
        'stroke-linecap': 'round'
      });
      group.appendChild(pen);
      animateDash(pen, r.width * 1.1, state.reduced ? 0 : ms);
      const dot = svgEl('circle', { cx: r.left, cy: r.top + r.height - 2, r: 3, fill: color, opacity: '0.9' });
      group.appendChild(dot);
      if (!state.reduced) {
        dot.style.transition = `cx ${ms}ms ease-out, opacity 200ms ease`;
        requestAnimationFrame(() => {
          dot.setAttribute('cx', String(r.left + r.width));
          dot.style.opacity = '0';
        });
      }
    });

    state.layer.appendChild(group);
    keep(group);
    announce(sentence);
    return settle(ms, o.delay).then(() => ({ ok: true, kind: 'sweep', sentence }));
  }

  function highlight(opts) {
    const o = optsOf(opts);
    const el = q(o.anchor);
    if (!el) return detached(new Error('missing anchor'));
    const rects = rectsFor(el, o.text);
    const color = o.color || '#fbbf24';
    const ms = o.ms || 260;
    const group = svgEl('g', { class: 'annot annot-highlight' });
    const sentence = `Highlighted ${o.text ? `“${o.text}”` : labelOf(el)}.`;
    title(group, sentence);

    rects.forEach((r) => {
      const band = svgEl('rect', {
        x: r.left - 2,
        y: r.top + 1,
        width: r.width + 4,
        height: r.height - 2,
        rx: 3,
        fill: color,
        opacity: state.reduced ? '0.28' : '0'
      });
      band.style.transformBox = 'fill-box';
      band.style.transformOrigin = 'left center';
      if (!state.reduced) band.style.transform = 'scaleX(0.02)';
      group.appendChild(band);
      if (!state.reduced) {
        band.style.transition = `opacity 160ms ease, transform ${ms}ms ease-out`;
        requestAnimationFrame(() => {
          band.style.opacity = '0.28';
          band.style.transform = 'scaleX(1)';
        });
      }
    });

    state.layer.appendChild(group);
    keep(group);
    announce(sentence);
    return settle(ms, o.delay).then(() => ({ ok: true, kind: 'highlight', sentence }));
  }

  function circle(opts) {
    const o = optsOf(opts);
    const el = q(o.anchor);
    if (!el) return detached(new Error('missing anchor'));
    const rects = rectsFor(el, o.text);
    if (!rects.length) return detached(new Error('no rects'));
    const u = union(rects);
    const cx = u.left + u.width / 2;
    const cy = u.top + u.height / 2;
    const rx = u.width / 2 + 8;
    const ry = u.height / 2 + 7;
    const ms = o.ms || 420;
    const group = svgEl('g', { class: 'annot annot-circle' });
    const sentence = `Circled ${o.text ? `“${o.text}”` : labelOf(el)}.`;
    title(group, sentence);

    const ellipse = svgEl('ellipse', {
      cx,
      cy,
      rx,
      ry,
      fill: 'none',
      stroke: o.color || ACCENT,
      'stroke-width': 2.4,
      transform: `rotate(-4 ${cx} ${cy})`
    });
    group.appendChild(ellipse);
    animateDash(ellipse, Math.PI * (rx + ry), state.reduced ? 0 : ms);

    state.layer.appendChild(group);
    keep(group);
    announce(sentence);
    return settle(ms, o.delay).then(() => ({ ok: true, kind: 'circle', sentence }));
  }

  function ellipseLabel(opts) {
    const o = optsOf(opts);
    const el = q(o.anchor);
    if (!el) return detached(new Error('missing anchor'));
    const rects = rectsFor(el, o.text);
    const u = union(rects);
    const ms = o.ms || 420;
    const label = String(o.label || o.text || '').slice(0, 32);
    const group = svgEl('g', { class: 'annot annot-ellipse-label' });
    const sentence = `Marked ${o.text ? `“${o.text}”` : labelOf(el)}${label ? ` — ${label}` : ''}.`;
    title(group, sentence);

    const cx = u.left + u.width / 2;
    const cy = u.top + u.height / 2;
    const rx = u.width / 2 + 10;
    const ry = u.height / 2 + 8;
    group.appendChild(
      svgEl('ellipse', { cx, cy, rx, ry, fill: 'none', stroke: o.color || ACCENT, 'stroke-width': 2.2 })
    );

    if (label) {
      const chipW = 8 + label.length * 6.4;
      const chipX = Math.min(cx + rx + 4, (state.layer.getBoundingClientRect().width || 0) - chipW - 4);
      const chipY = cy - 11;
      group.appendChild(svgEl('rect', { x: chipX, y: chipY, width: chipW, height: 22, rx: 11, fill: '#fff7ed', stroke: o.color || ACCENT, 'stroke-width': 1.2 }));
      const text = svgEl('text', {
        x: chipX + 6,
        y: chipY + 15,
        'font-size': '12',
        fill: o.color || ACCENT,
        'font-family': 'Inter, system-ui, sans-serif',
        'font-weight': '600'
      });
      text.textContent = label;
      group.appendChild(text);
    }

    state.layer.appendChild(group);
    keep(group);
    announce(sentence);
    return settle(ms, o.delay).then(() => ({ ok: true, kind: 'ellipse-label', sentence }));
  }

  function arrowHead(id, color) {
    const marker = svgEl('marker', {
      id,
      viewBox: '0 0 10 10',
      refX: '9',
      refY: '5',
      markerWidth: '7',
      markerHeight: '7',
      orient: 'auto-start-reverse'
    });
    marker.appendChild(svgEl('path', { d: 'M 0 0 L 10 5 L 0 10 z', fill: color }));
    return marker;
  }

  function fromPoint(o, el) {
    const layer = state.layer.getBoundingClientRect();
    if (o.from) {
      const fromEl = q(o.from);
      if (fromEl) {
        const r = fromEl.getBoundingClientRect();
        return { x: r.left - layer.left + r.width / 2, y: r.top - layer.top + r.height / 2 };
      }
    }
    const mascot = global.Mascot && global.Mascot.isReady && global.Mascot.isReady() ? global.Mascot.position() : null;
    if (mascot) return { x: mascot.x + 56, y: mascot.y + 56 };
    const r = el.getBoundingClientRect();
    return { x: r.left - layer.left - 40, y: r.top - layer.top };
  }

  function arrow(opts) {
    const o = optsOf(opts);
    const el = q(o.anchor);
    if (!el) return detached(new Error('missing anchor'));
    const rects = rectsFor(el, o.text);
    const u = union(rects);
    const to = { x: u.left - 6, y: u.top + u.height / 2 };
    const from = fromPoint(o, el);
    const color = o.color || ACCENT;
    const ms = o.ms || 380;
    const group = svgEl('g', { class: 'annot annot-arrow' });
    const sentence = `Arrow pointing at ${labelOf(el)}.`;
    title(group, sentence);

    const markerId = `annot-arrowhead-${++state.seq}`;
    const defs = svgEl('defs');
    defs.appendChild(arrowHead(markerId, color));
    group.appendChild(defs);

    const line = svgEl('line', {
      x1: from.x,
      y1: from.y,
      x2: to.x,
      y2: to.y,
      stroke: color,
      'stroke-width': 2.2,
      'stroke-linecap': 'round',
      'marker-end': `url(#${markerId})`
    });
    group.appendChild(line);
    animateDash(line, Math.hypot(to.x - from.x, to.y - from.y), state.reduced ? 0 : ms);

    state.layer.appendChild(group);
    keep(group);
    announce(sentence);
    return settle(ms, o.delay).then(() => ({ ok: true, kind: 'arrow', sentence }));
  }

  function curve(opts) {
    const o = optsOf(opts);
    const el = q(o.anchor);
    if (!el) return detached(new Error('missing anchor'));
    const rects = rectsFor(el, o.text);
    const u = union(rects);
    const to = { x: u.left - 6, y: u.top + u.height / 2 };
    const from = fromPoint(o, el);
    const cx = (from.x + to.x) / 2;
    const cy = Math.min(from.y, to.y) - 44;
    const color = o.color || ACCENT;
    const ms = o.ms || 420;
    const group = svgEl('g', { class: 'annot annot-curve' });
    const sentence = `Curved pointer to ${labelOf(el)}.`;
    title(group, sentence);

    const markerId = `annot-arrowhead-${++state.seq}`;
    const defs = svgEl('defs');
    defs.appendChild(arrowHead(markerId, color));
    group.appendChild(defs);

    const path = svgEl('path', {
      d: `M ${from.x} ${from.y} Q ${cx} ${cy} ${to.x} ${to.y}`,
      fill: 'none',
      stroke: color,
      'stroke-width': 2.2,
      'stroke-linecap': 'round',
      'marker-end': `url(#${markerId})`
    });
    group.appendChild(path);
    const len = Math.hypot(to.x - from.x, to.y - from.y) * 1.15;
    animateDash(path, len, state.reduced ? 0 : ms);

    state.layer.appendChild(group);
    keep(group);
    announce(sentence);
    return settle(ms, o.delay).then(() => ({ ok: true, kind: 'curve', sentence }));
  }

  function strike(opts) {
    const o = optsOf(opts);
    const el = q(o.anchor);
    if (!el) return detached(new Error('missing anchor'));
    const rects = rectsFor(el, o.text);
    const u = union(rects);
    const color = o.color || BAD;
    const ms = o.ms || 340;
    const group = svgEl('g', { class: 'annot annot-strike' });
    const sentence = `Crossed out ${o.text ? `“${o.text}”` : labelOf(el)} — that is the wrong idea.`;
    title(group, sentence);

    const line = svgEl('line', {
      x1: u.left - 2,
      y1: u.top + u.height / 2,
      x2: u.left + u.width + 2,
      y2: u.top + u.height / 2,
      stroke: color,
      'stroke-width': 2.4,
      'stroke-linecap': 'round'
    });
    group.appendChild(line);
    animateDash(line, u.width + 4, state.reduced ? 0 : ms);

    state.layer.appendChild(group);
    keep(group);
    el.classList.add('annot-struck');
    announce(sentence);
    return settle(ms, o.delay).then(() => ({ ok: true, kind: 'strike', sentence }));
  }

  function box(opts) {
    const o = optsOf(opts);
    const el = q(o.anchor);
    if (!el) return detached(new Error('missing anchor'));
    const rects = rectsFor(el, o.text);
    const u = union(rects);
    const ms = o.ms || 380;
    const group = svgEl('g', { class: 'annot annot-box' });
    const sentence = `Boxed ${o.text ? `“${o.text}”` : labelOf(el)}.`;
    title(group, sentence);

    const rect = svgEl('rect', {
      x: u.left - 6,
      y: u.top - 5,
      width: u.width + 12,
      height: u.height + 10,
      rx: 7,
      fill: 'none',
      stroke: o.color || ACCENT,
      'stroke-width': 2,
      'stroke-dasharray': '5 4'
    });
    group.appendChild(rect);
    if (!state.reduced) {
      rect.style.opacity = '0';
      rect.style.transition = `opacity ${ms}ms ease-out`;
      requestAnimationFrame(() => {
        rect.style.opacity = '1';
      });
    }

    state.layer.appendChild(group);
    keep(group);
    announce(sentence);
    return settle(ms, o.delay).then(() => ({ ok: true, kind: 'box', sentence }));
  }

  function brace(opts) {
    const o = optsOf(opts);
    const el = q(o.anchor);
    if (!el) return detached(new Error('missing anchor'));
    const rects = rectsFor(el, o.text);
    const u = union(rects);
    const ms = o.ms || 340;
    const x = u.left - 9;
    const y1 = u.top + 2;
    const y2 = u.top + u.height - 2;
    const group = svgEl('g', { class: 'annot annot-brace' });
    const label = String(o.label || '').slice(0, 28);
    const sentence = `Braced ${o.text ? `“${o.text}”` : labelOf(el)}${label ? ` — ${label}` : ''}.`;
    title(group, sentence);

    // a square bracket with a mid tick reads as a brace at 2 px and never wobbles
    const path = svgEl('path', {
      d: `M ${x + 5} ${y1} L ${x} ${y1} L ${x} ${y2} L ${x + 5} ${y2} M ${x} ${(y1 + y2) / 2} L ${x - 4} ${(y1 + y2) / 2}`,
      fill: 'none',
      stroke: o.color || ACCENT,
      'stroke-width': 2.2,
      'stroke-linecap': 'round'
    });
    group.appendChild(path);
    animateDash(path, (y2 - y1) * 2 + 20, state.reduced ? 0 : ms);

    if (label) {
      const text = svgEl('text', {
        x: Math.max(2, x - 8 - label.length * 6.2),
        y: (y1 + y2) / 2 + 4,
        'font-size': '12',
        fill: o.color || ACCENT,
        'font-family': 'Inter, system-ui, sans-serif',
        'font-weight': '600'
      });
      text.textContent = label;
      group.appendChild(text);
    }

    state.layer.appendChild(group);
    keep(group);
    announce(sentence);
    return settle(ms, o.delay).then(() => ({ ok: true, kind: 'brace', sentence }));
  }

  function stamp(opts) {
    const o = optsOf(opts);
    const el = q(o.anchor);
    if (!el) return detached(new Error('missing anchor'));
    const rects = rectsFor(el, o.text);
    const u = union(rects);
    const good = o.mark !== 'x' && o.mark !== 'wrong';
    const color = o.color || (good ? GOOD : BAD);
    const ms = o.ms || 300;
    const group = svgEl('g', { class: 'annot annot-stamp' });
    const sentence = good
      ? `Marked ${o.text ? `“${o.text}”` : labelOf(el)} as correct.`
      : `Marked ${o.text ? `“${o.text}”` : labelOf(el)} as incorrect.`;
    title(group, sentence);

    const gx = u.left + u.width + 10;
    const gy = u.top + u.height / 2;
    group.appendChild(svgEl('circle', { cx: gx, cy: gy, r: 11, fill: good ? '#e6f6ef' : '#fdecea', stroke: color, 'stroke-width': 1.6 }));

    if (good) {
      const tick = svgEl('path', {
        d: `M ${gx - 4.5} ${gy} l 3.2 3.4 l 6 -7`,
        fill: 'none',
        stroke: color,
        'stroke-width': 2.2,
        'stroke-linecap': 'round'
      });
      group.appendChild(tick);
      animateDash(tick, 18, state.reduced ? 0 : ms);
    } else {
      const cross = svgEl('path', {
        d: `M ${gx - 4} ${gy - 4} l 8 8 M ${gx + 4} ${gy - 4} l -8 8`,
        fill: 'none',
        stroke: color,
        'stroke-width': 2.2,
        'stroke-linecap': 'round'
      });
      group.appendChild(cross);
      animateDash(cross, 23, state.reduced ? 0 : ms);
    }

    if (!state.reduced) {
      group.style.transformBox = 'fill-box';
      group.style.transformOrigin = 'center';
      group.style.transform = 'scale(0.5)';
      group.style.transition = `transform ${ms}ms cubic-bezier(.32,.72,0,1)`;
      requestAnimationFrame(() => {
        group.style.transform = 'scale(1)';
      });
    }

    state.layer.appendChild(group);
    keep(group);
    announce(sentence);
    return settle(ms, o.delay).then(() => ({ ok: true, kind: 'stamp', sentence }));
  }

  function shake(opts) {
    const o = optsOf(opts);
    const el = q(o.anchor);
    if (!el) return detached(new Error('missing anchor'));
    const ms = o.ms || 420;
    const sentence = `Gave ${labelOf(el)} a shake — check it again.`;
    if (!state.reduced) {
      el.classList.remove('sx-shake');
      void el.getBoundingClientRect();
      el.classList.add('sx-shake');
      setTimeout(() => el.classList.remove('sx-shake'), ms);
    }
    announce(sentence);
    return settle(ms, o.delay).then(() => ({ ok: true, kind: 'shake', sentence }));
  }

  // ------------------------------------------------------------- the director
  /**
   * Play a timed script. Entries are {at, do, ...}. The AI writes these in P3;
   * P2 renders hand-written ones. Unknown actions are skipped, never thrown.
   */
  function play(script, opts) {
    const entries = Array.isArray(script) ? script : [];
    const options = opts || {};
    const timers = [];
    const done = [];

    entries.forEach((entry) => {
      if (!entry || typeof entry !== 'object') return;
      const at = Math.max(0, Number(entry.at) || 0);
      const run = () => {
        const action = entry.do;
        if (action === 'say') {
          done.push(global.Mascot && global.Mascot.say ? global.Mascot.say(entry.text, entry.ms) : Promise.resolve());
          return;
        }
        if (action === 'move') {
          done.push(global.Mascot && global.Mascot.moveTo ? global.Mascot.moveTo(entry.to || entry.anchor) : Promise.resolve());
          return;
        }
        if (action === 'mood') {
          if (global.Mascot && global.Mascot.mood) global.Mascot.mood(entry.mood);
          return;
        }
        if (action === 'board') {
          done.push(
            global.Board && global.Board.open
              ? global.Board.open({ preset: entry.preset, params: entry.params, steps: entry.steps })
              : Promise.resolve()
          );
          return;
        }
        const fn = api[action];
        if (typeof fn === 'function') {
          done.push(fn({ anchor: entry.anchor, text: entry.text, label: entry.label, color: entry.color, ms: entry.ms }));
        }
      };
      if (state.reduced) run();
      else timers.push(setTimeout(run, at));
    });

    return new Promise((resolve) => {
      const wait = state.reduced ? 0 : Math.max(0, ...entries.map((e) => Number(e.at) || 0)) + (options.tail || 600);
      setTimeout(() => {
        Promise.all(done.map((p) => Promise.resolve(p).catch(() => null))).then(() => resolve({ ok: true, count: done.length }));
      }, wait);
    });
  }

  function clear() {
    if (state.layer) state.layer.innerHTML = '';
    state.shapes = [];
    document.querySelectorAll('.annot-struck, .sx-shake').forEach((el) => el.classList.remove('annot-struck', 'sx-shake'));
    if (state.live) state.live.innerHTML = '';
  }

  function attach(container) {
    const host = q(container);
    if (!host) return null;
    state.container = host;
    state.reduced = prefersReduced();

    const existing = host.querySelector('#annot-layer');
    if (existing) existing.remove();

    const layer = svgEl('svg', { id: 'annot-layer', 'aria-hidden': 'true', focusable: 'false', class: 'annot-layer' });
    host.appendChild(layer);
    state.layer = layer;

    const live = document.createElement('div');
    live.id = 'sx-annot-live';
    live.className = 'sr-only';
    live.setAttribute('role', 'log');
    live.setAttribute('aria-live', 'polite');
    live.setAttribute('aria-atomic', 'false');
    host.appendChild(live);
    state.live = live;

    if (typeof ResizeObserver === 'function') {
      // Height changes as the card grows; only a width change can misplace ink.
      let lastWidth = host.clientWidth;
      const ro = new ResizeObserver(() => {
        if (Math.abs(host.clientWidth - lastWidth) < 2) return;
        lastWidth = host.clientWidth;
        clear();
      });
      ro.observe(host);
      state.observer = ro;
    }

    return api;
  }

  const api = {
    attach,
    clear,
    play,
    arrow,
    box,
    brace,
    circle,
    curve,
    ellipseLabel,
    highlight,
    labelOf,
    shake,
    stamp,
    strike,
    sweep,
    underline,
    isReduced: () => state.reduced || prefersReduced(),
    count: () => state.shapes.length,
    MAX_LIVE
  };

  global.Annotate = api;
})(window);
