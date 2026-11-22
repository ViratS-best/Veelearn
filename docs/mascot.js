/**
 * The study buddy as a rig.
 *
 * Four behaviours, no game engine:
 *   1. eyes follow the cursor (damped pupil vector, clamped inside the iris)
 *   2. it walks to what it is explaining (arc waypoint, hop when close, whoosh when far)
 *   3. it can point, hold a pencil and fall asleep
 *   4. it never covers the answer options
 *
 * One rAF loop for the whole character. Rects are cached on resize/scroll; the
 * pointermove handler only writes two numbers. Everything degrades to a static
 * pose under prefers-reduced-motion or on low-core devices.
 */
(function (global) {
  'use strict';

  const R_MAX = 9; // rig units of pupil travel inside the iris
  const FAR = 620; // px at which pupils are fully deflected (eye-relative)
  const BOB_MS = 3000; // idle bob period
  const IDLE_DRIFT_MS = 12000;
  const DRAG_KEY = 'veelearnMascotPos';
  const DRAG_SLOP = 4; // px before a press counts as a drag, not a click

  const MOUTH = {
    idle: 'M54 61.5 Q64 68 74 61.5',
    happy: 'M52 59 Q64 76 76 59 Q64 68 52 59',
    thinking: 'M55 64 q4 -2.5 9 0 q4 2.5 9 0',
    oops: 'M53 66 h22',
    sleepy: 'M54 65.5 q10 3.5 20 0',
    talking: 'M53 60 Q64 74 75 60 Q64 66 53 60',
    // 'cheer' is the goal pose: same open smile, both arms up, a hop
    cheer: 'M50 58 Q64 78 78 58 Q64 66 50 58',
    // 'pointing' keeps a small open mouth so the state is not silently 'idle'
    pointing: 'M54 61 Q64 71 74 61 Q64 66 54 61',
    // 'writing': concentrating, mouth closed and level
    writing: 'M55 63 h18'
  };

  const prefersReduced = () =>
    typeof global.matchMedia === 'function' && global.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const lowEnd = () => (global.navigator && global.navigator.hardwareConcurrency ? global.navigator.hardwareConcurrency <= 4 : false);

  const clamp = (n, lo, hi) => Math.min(hi, Math.max(lo, n));

  /**
   * Pupil offset for a cursor at (x,y) relative to the eye centre.
   * Exported shape is pure so it can be tested without a DOM.
   */
  function pupilOffset(x, y, eyeCx, eyeCy, maxTravel) {
    const dx = x - eyeCx;
    const dy = y - eyeCy;
    const d = Math.hypot(dx, dy) || 1;
    const k = Math.min(1, d / FAR) * (maxTravel || R_MAX);
    return { x: (dx / d) * k, y: (dy / d) * k };
  }

  /** Frame-rate independent ease factor (~120 ms settle at 60 fps). */
  function easeFactor(dt) {
    return 1 - Math.pow(0.001, Math.max(0, Math.min(dt, 0.2)));
  }

  const state = {
    ready: false,
    host: null,
    dock: null,
    bobEl: null,
    svg: null,
    mood: 'idle',
    root: null,
    parts: {},
    pointer: { x: 0, y: 0, t: 0 },
    pupils: { l: { x: 0, y: 0 }, r: { x: 0, y: 0 } },
    target: { x: 0, y: 0 }, // dock transform target (px, relative to stage)
    targetFlip: 1,
    home: { x: 0, y: 0 },
    rects: { l: null, r: null, stage: null, options: null },
    rectsDirty: false,
    raf: null,
    last: 0,
    lastNarration: performance.now(),
    rectsAt: 0,
    manual: false, // the learner placed Vee here: the tutor stops moving it
    dragging: false,
    dragAt: 0,
    bubbleEl: null,
    bubbleTimer: null,
    blinkAt: 0,
    reduced: false,
    lite: false,
    onMove: null,
    onScroll: null
  };

  // ------------------------------------------------------------------ helpers
  function q(sel) {
    return sel && typeof sel === 'string' ? document.querySelector(sel) : sel;
  }

  function stageRect() {
    const stage = document.querySelector('.sx-stage') || document.body;
    return stage.getBoundingClientRect();
  }

  function invalidate() {
    state.rectsDirty = true;
  }

  // ------------------------------------------------------- remembered drag
  function storedPos() {
    try {
      const raw = global.localStorage && global.localStorage.getItem(DRAG_KEY);
      if (!raw) return null;
      const parsed = JSON.parse(raw);
      if (!parsed || !Number.isFinite(parsed.fx) || !Number.isFinite(parsed.fy)) return null;
      return { fx: clamp(parsed.fx, 0, 1), fy: clamp(parsed.fy, 0, 1) };
    } catch (_) {
      return null;
    }
  }

  /** Fractions of the stage, so a split-screen window still finds Vee. */
  function rememberPos(x, y, stage) {
    try {
      if (!global.localStorage) return;
      global.localStorage.setItem(
        DRAG_KEY,
        JSON.stringify({ fx: stage.width ? x / stage.width : 0, fy: stage.height ? y / stage.height : 0 })
      );
    } catch (_) {
      /* private mode: the drag still holds for this page */
    }
  }

  function forgetPos() {
    try {
      if (global.localStorage) global.localStorage.removeItem(DRAG_KEY);
    } catch (_) {
      /* nothing to clear */
    }
  }

  function restorePos(stage) {
    const saved = storedPos();
    if (!saved) return null;
    const size = mascotSize();
    return {
      x: clamp(saved.fx * stage.width, 8, Math.max(8, stage.width - size - 8)),
      y: clamp(saved.fy * stage.height, 8, Math.max(8, stage.height - size - 8))
    };
  }

  /** Move the dock to an exact spot, without asking where an anchor is. */
  function setDock(x, y, flip) {
    if (!state.dock) return;
    state.target = { x, y };
    if (flip) state.targetFlip = flip;
    state.dock.style.transition = state.reduced ? 'transform 200ms ease-out' : 'transform 240ms ease-out';
    state.dock.style.transform = `translate(${x}px, ${y}px) scaleX(${state.targetFlip === -1 ? -1 : 1})`;
  }

  /**
   * Drag Vee out of the way. A press only becomes a drag after a few pixels, so
   * the click that opens the board still works; once dragged, the tutor stops
   * moving the mascot and the spot is remembered across sessions.
   */
  function enableDrag(dock) {
    let start = null;

    dock.addEventListener('pointerdown', (e) => {
      if (e.button !== 0) return;
      start = { px: e.clientX, py: e.clientY, x: state.target.x, y: state.target.y, moved: false };
      state.dragging = true;
      dock.classList.add('is-dragging');
      dock.style.transition = 'none';
      try {
        dock.setPointerCapture(e.pointerId);
      } catch (_) {
        /* capture is a nicety: the drag still works without it */
      }
    });

    dock.addEventListener('pointermove', (e) => {
      if (!start || !state.dragging) return;
      const dx = e.clientX - start.px;
      const dy = e.clientY - start.py;
      if (!start.moved && Math.hypot(dx, dy) < DRAG_SLOP) return;
      start.moved = true;
      const stage = state.rects.stage || stageRect();
      const size = mascotSize();
      const x = clamp(start.x + dx, 8, Math.max(8, stage.width - size - 8));
      const y = clamp(start.y + dy, 8, Math.max(8, stage.height - size - 8));
      state.manual = true;
      state.target = { x, y };
      dock.style.transform = `translate(${x}px, ${y}px) scaleX(${state.targetFlip === -1 ? -1 : 1})`;
    });

    const finish = () => {
      if (!start) return;
      const moved = start.moved;
      start = null;
      state.dragging = false;
      dock.classList.remove('is-dragging');
      if (!moved) return;
      state.dragAt = Date.now();
      state.lastNarration = Date.now();
      rememberPos(state.target.x, state.target.y, state.rects.stage || stageRect());
      hideBubble();
    };
    dock.addEventListener('pointerup', finish);
    dock.addEventListener('pointercancel', finish);
  }

  /** Hand the position back to the page: Vee follows the lesson again. */
  function resetPosition() {
    forgetPos();
    state.manual = false;
    state.dragAt = 0;
    const stage = state.rects.stage || stageRect();
    const size = mascotSize();
    state.home = { x: Math.max(8, stage.width - size - 16), y: Math.max(8, stage.height - size - 38) };
    setDock(state.home.x, state.home.y, 1);
  }

  function readRects() {
    const stage = stageRect();
    state.rects.stage = stage;
    // Anchor on the eye (the white sclera), not the pupil: the pupil moves as it
    // looks, so measuring it feeds its own offset back into the aim.
    const l = state.parts.eyeL && state.parts.eyeL.getBoundingClientRect();
    const r = state.parts.eyeR && state.parts.eyeR.getBoundingClientRect();
    state.rects.l = l;
    state.rects.r = r;
    const opts = document.getElementById('sx-options');
    state.rects.options = opts ? opts.getBoundingClientRect() : null;
    state.rectsDirty = false;
  }

  // -------------------------------------------------------------------- moods
  function setMood(name) {
    if (!state.ready) {
      state.mood = name;
      return;
    }
    const mood = MOUTH[name] ? name : 'idle';
    state.mood = mood;
    if (!state.root) return;

    state.root.setAttribute('data-mood', mood);

    const mouth = state.parts.mouth;
    if (mouth) mouth.setAttribute('d', MOUTH[mood]);

    const happy = mood === 'happy' || mood === 'cheer';
    if (state.parts.smileL) state.parts.smileL.style.opacity = happy ? '1' : '0';
    if (state.parts.smileR) state.parts.smileR.style.opacity = happy ? '1' : '0';
    if (state.parts.eyeL) state.parts.eyeL.style.opacity = happy ? '0' : '1';
    if (state.parts.eyeR) state.parts.eyeR.style.opacity = happy ? '0' : '1';

    // brows: an oops tilt, a thinking raise, a neutral arch
    // CSS transforms need degrees: the SVG `rotate(a x y)` form is silently dropped.
    const brow = { oops: ['rotate(9deg)', 'rotate(-9deg)'], thinking: ['rotate(-8deg)', 'rotate(4deg)'] }[mood] || [
      'rotate(0deg)',
      'rotate(0deg)'
    ];
    if (state.parts.browL) state.parts.browL.style.transform = brow[0];
    if (state.parts.browR) state.parts.browR.style.transform = brow[1];

    // arms: up for cheer, out for pointing, tucked otherwise
    const armL = { cheer: 'rotate(-38deg)' }[mood] || 'rotate(0deg)';
    const armR = { cheer: 'rotate(38deg)', pointing: 'rotate(-24deg)', writing: 'rotate(-30deg)' }[mood] || 'rotate(0deg)';
    if (state.parts.armL) state.parts.armL.style.transform = armL;
    if (state.parts.armR) state.parts.armR.style.transform = armR;

    if (mood === 'cheer' && !state.reduced) hop();
  }

  // ------------------------------------------------------------------- hop(s)
  function hop() {
    const body = state.parts.body;
    if (!body || state.reduced) return;
    body.classList.remove('rig-hop');
    // reflow so the animation can restart
    void body.getBoundingClientRect();
    body.classList.add('rig-hop');
    setTimeout(() => body.classList.remove('rig-hop'), 520);
  }

  // -------------------------------------------------------------- movement
  /** Split-screen laptops still deserve a tutor: shrink and dock instead. */
  function compactMode() {
    return typeof global.matchMedia === 'function' && global.matchMedia('(max-width: 720px)').matches;
  }

  function mascotSize() {
    return compactMode() ? 64 : 112;
  }

  function placeFor(anchorEl) {
    const el = q(anchorEl);
    const stage = state.rects.stage || stageRect();
    const size = mascotSize();
    const maxX = Math.max(8, stage.width - size - 8);
    const maxY = Math.max(8, stage.height - size - 8);
    if (!el) {
      // never throw, never guess: fall back to the centre of the problem card
      return { x: clamp(stage.width / 2 - size / 2, 8, maxX), y: maxY };
    }
    const r = el.getBoundingClientRect();
    if (compactMode()) {
      // Narrow: pin to the card's top-right corner, clear of the text column.
      return { x: maxX, y: 6 };
    }

    const boxAt = (x, y) => ({
      left: stage.left + x,
      top: stage.top + y,
      right: stage.left + x + size,
      bottom: stage.top + y + size
    });
    const hits = (a, b) => !!b && !(a.right <= b.left || a.left >= b.right || a.bottom <= b.top || a.top >= b.bottom);
    const opts = state.rects.options;
    // A sentence span is only one line: keep off the whole paragraph it lives in,
    // not just the words it covers, or Vee lands across the next line.
    const para = el.closest ? el.closest('p, li, td, .sx-intro, .sx-stem') : null;
    const avoid = para && para !== el ? [r, para.getBoundingClientRect()] : [r];
    // Never sit on the words being explained, nor on the answer options.
    const clear = (x, y) => {
      const b = boxAt(x, y);
      return avoid.every((rect) => !hits(b, rect)) && !hits(b, opts);
    };

    const midY = clamp(r.top - stage.top + r.height / 2 - size / 2, 8, maxY);
    const spots = [
      { x: r.left - stage.left - (size + 6), y: midY }, // the gutter to its left
      { x: r.right - stage.left + 10, y: midY }, // or to its right
      { x: clamp(r.right - stage.left - size - 8, 8, maxX), y: clamp(r.top - stage.top - size - 10, 8, maxY) }, // above
      { x: clamp(r.left - stage.left + 8, 8, maxX), y: clamp(r.bottom - stage.top + 10, 8, maxY) } // below
    ].map((s) => ({ x: clamp(s.x, 8, maxX), y: clamp(s.y, 8, maxY) }));

    for (const spot of spots) {
      if (clear(spot.x, spot.y)) return spot;
    }
    // Nowhere clean beside it: sit below the block rather than across it.
    return { x: clamp(r.left - stage.left + 8, 8, maxX), y: clamp(r.bottom - stage.top + 10, 8, maxY) };
  }

  function moveTo(anchorEl, opts) {
    if (!state.ready) return Promise.resolve();
    const options = opts || {};
    // Once the learner has placed Vee, a hint must not drag it back over the
    // sentence they moved it away from.
    if (state.manual && !options.force) return Promise.resolve();
    const stage = state.rects.stage || stageRect();
    const el = q(anchorEl);
    const dest = placeFor(anchorEl);
    const from = { x: state.target.x, y: state.target.y };
    const distance = Math.hypot(dest.x - from.x, dest.y - from.y);
    const flip = el ? (el.getBoundingClientRect().left - stage.left > from.x + 56 ? 1 : -1) : 1;

    state.target = dest;
    state.targetFlip = flip;
    state.lastAnchor = anchorEl;
    state.lastNarration = performance.now();

    const dock = state.dock;
    if (!dock) return Promise.resolve();

    if (options.instant) {
      dock.style.transition = 'none';
      dock.style.transform = `translate(${dest.x}px, ${dest.y}px) scaleX(${flip})`;
      return Promise.resolve();
    }
    if (state.reduced) {
      // Reduced motion means shorter and gentler, not a teleport: the mascot
      // still glides so the eye can follow where it went.
      dock.style.transition = 'transform 200ms ease-out';
      dock.style.transform = `translate(${dest.x}px, ${dest.y}px) scaleX(${flip})`;
      return new Promise((resolve) => setTimeout(resolve, 210));
    }

    if (distance > 900) {
      // whoosh: fade out, jump, fade back in — never a two second walk
      dock.style.transition = 'opacity 120ms ease';
      dock.style.opacity = '0';
      return new Promise((resolve) => {
        setTimeout(() => {
          dock.style.transition = 'none';
          dock.style.transform = `translate(${dest.x}px, ${dest.y}px) scaleX(${flip})`;
          requestAnimationFrame(() => {
            dock.style.transition = 'opacity 160ms ease';
            dock.style.opacity = '1';
            setTimeout(resolve, 170);
          });
        }, 130);
      });
    }

    if (distance < 60) {
      hop();
      dock.style.transition = `transform 180ms cubic-bezier(.32,.72,0,1)`;
      dock.style.transform = `translate(${dest.x}px, ${dest.y}px) scaleX(${flip})`;
      return new Promise((resolve) => setTimeout(resolve, 190));
    }

    // walk: arc waypoint (midpoint, -24px) then to the target
    const mid = { x: (from.x + dest.x) / 2, y: Math.min(from.y, dest.y) - 24 };
    dock.style.transition = 'transform 210ms cubic-bezier(.32,.72,0,1)';
    dock.style.transform = `translate(${mid.x}px, ${mid.y}px) scaleX(${flip})`;
    return new Promise((resolve) => {
      setTimeout(() => {
        dock.style.transition = 'transform 210ms cubic-bezier(.32,.72,0,1)';
        dock.style.transform = `translate(${dest.x}px, ${dest.y}px) scaleX(${flip})`;
        setTimeout(resolve, 220);
      }, 210);
    });
  }

  // --------------------------------------------------------------- bubble
  function say(text, ms) {
    if (!state.ready) return Promise.resolve();
    const clean = String(text == null ? '' : text).trim();
    if (!clean) return Promise.resolve();

    // 140 chars per bubble, per the spec; longer copy is split, never truncated.
    const chunks = [];
    let rest = clean;
    while (rest.length > 140) {
      const cut = rest.lastIndexOf(' ', 140);
      chunks.push(rest.slice(0, cut > 40 ? cut : 140));
      rest = rest.slice(cut > 40 ? cut + 1 : 140);
    }
    if (rest) chunks.push(rest);

    const bubble = state.bubbleEl;
    if (!bubble) return Promise.resolve();

    clearTimeout(state.bubbleTimer);
    bubble.hidden = false;
    bubble.textContent = chunks[0];
    bubble.classList.add('is-in');

    const hold = ms || Math.max(1400, chunks[0].length * 34);
    return new Promise((resolve) => {
      state.bubbleTimer = setTimeout(() => {
        bubble.classList.remove('is-in');
        bubble.hidden = true;
        if (chunks.length > 1) say(chunks.slice(1).join(' '), ms).then(resolve);
        else resolve();
      }, hold);
    });
  }

  function hideBubble() {
    if (!state.bubbleEl) return;
    clearTimeout(state.bubbleTimer);
    state.bubbleEl.classList.remove('is-in');
    state.bubbleEl.hidden = true;
  }

  // --------------------------------------------------------------- pointing
  function pointAt(anchorEl, opts) {
    const options = opts || {};
    setMood('pointing');
    // No leader arrow: it read as a stray stroke and the mascot's pose already
    // shows where it is looking.
    return moveTo(anchorEl, options).then(() => {
      if (options.text) return say(options.text, options.ms);
      return undefined;
    });
  }

  function park() {
    setMood('idle');
    if (state.manual) return;
    state.target = { x: state.home.x, y: state.home.y };
    if (state.dock) {
      state.dock.style.transition = state.reduced ? 'transform 200ms ease-out' : 'transform 420ms cubic-bezier(.32,.72,0,1)';
      state.dock.style.transform = `translate(${state.home.x}px, ${state.home.y}px) scaleX(1)`;
    }
    state.lastNarration = performance.now();
  }

  // ------------------------------------------------------------------ frame
  function tick(now) {
    const dt = Math.min(0.2, (now - (state.last || now)) / 1000);
    state.last = now;

    if (state.rectsDirty) readRects();
    // The mascot walks and hops: its eyes move with it, so a cached rect makes the
    // pupils point at where it used to stand. Refresh while the page is live.
    if (now - state.rectsAt > 220) {
      readRects();
      state.rectsAt = now;
    }

    // eyes
    updatePupils(easeFactor(dt));

    // bob + blink
    if (!state.reduced && !state.lite) {
      if (state.bobEl) {
        const phase = (now % BOB_MS) / BOB_MS;
        const bob = Math.sin(phase * Math.PI * 2) * 2.2;
        state.bobEl.style.transform = `translateY(${bob.toFixed(2)}px)`;
      }
      if (now > state.blinkAt) {
        state.blinkAt = now + 4000 + Math.random() * 2000;
        blink();
      }
      if (state.mood === 'idle' && now - state.lastNarration > IDLE_DRIFT_MS) {
        drift();
      }
    }

    state.raf = requestAnimationFrame(tick);
  }

  /**
   * Move both pupils toward the last known cursor.
   * @param {number} a ease factor: 1 snaps, <1 eases.
   */
  function updatePupils(a) {
    const factor = typeof a === 'number' ? Math.max(0, Math.min(1, a)) : 1;
    [
      [state.parts.pupilL, state.rects.l, 'l'],
      [state.parts.pupilR, state.rects.r, 'r']
    ].forEach(([pupil, rect, key]) => {
      if (!pupil || !rect) return;
      const t = pupilOffset(state.pointer.x, state.pointer.y, rect.left + rect.width / 2, rect.top + rect.height / 2);
      const cur = state.pupils[key];
      cur.x += (t.x - cur.x) * factor;
      cur.y += (t.y - cur.y) * factor;
      // The dock flips with scaleX(-1) when the mascot faces left, and that mirror
      // applies to the pupils too. Negating the horizontal offset keeps the eyes
      // pointing at the cursor instead of the opposite side of the card.
      const flip = state.targetFlip === -1 ? -1 : 1;
      pupil.style.transform = `translate(${(cur.x * flip).toFixed(2)}px, ${cur.y.toFixed(2)}px)`;
    });
  }

  /** One synchronous pose: a throttled or reduced-motion tab still looks awake. */
  function poseOnce() {
    if (state.rectsDirty) readRects();
    updatePupils(1);
  }

  function blink() {
    const { eyeL, eyeR } = state.parts;
    if (!eyeL || !eyeR || state.mood === 'happy' || state.mood === 'cheer') return;
    [eyeL, eyeR].forEach((eye) => {
      eye.style.transform = 'scaleY(0.12)';
      eye.style.transformOrigin = 'center';
    });
    setTimeout(() => {
      [eyeL, eyeR].forEach((eye) => {
        eye.style.transform = 'scaleY(1)';
      });
    }, 130);
  }

  function drift() {
    if (state.manual) return;
    const stage = state.rects.stage || stageRect();
    state.lastNarration = performance.now();
    const rest = { x: Math.max(8, stage.width - 128), y: Math.max(8, stage.height - 150) };
    state.target = rest;
    if (state.dock) {
      state.dock.style.transition = state.reduced ? 'transform 240ms ease-out' : 'transform 900ms cubic-bezier(.32,.72,0,1)';
      state.dock.style.transform = `translate(${rest.x}px, ${rest.y}px) scaleX(1)`;
    }
    setMood('sleepy');
  }

  // ------------------------------------------------------------------- mount
  function attach(host, opts) {
    const options = opts || {};
    const mount = q(host);
    if (!mount) return Promise.resolve(null);

    state.host = mount;
    state.reduced = prefersReduced();
    state.lite = lowEnd();

    mount.classList.add('sx-mascot-host');
    mount.innerHTML = '';

    const dock = document.createElement('div');
    dock.className = 'sx-mascot-dock';
    dock.setAttribute('aria-hidden', 'true');
    const bob = document.createElement('div');
    bob.className = 'sx-mascot-bob';
    const holder = document.createElement('div');
    holder.className = 'sx-mascot-svg';
    bob.appendChild(holder);
    dock.appendChild(bob);
    mount.appendChild(dock);

    const bubble = document.createElement('div');
    bubble.className = 'sx-mascot-bubble';
    bubble.hidden = true;
    bubble.setAttribute('role', 'status');
    mount.appendChild(bubble);

    state.dock = dock;
    state.bobEl = bob;
    state.bubbleEl = bubble;
    enableDrag(dock);

    // Crossing the split-screen threshold re-homes the mascot instead of
    // leaving it parked at coordinates from the other width.
    if (!state.onResize) {
      state.onResize = () => {
        invalidate();
        // Wait for the layout to settle: reading rects mid-resize parks Vee off-screen.
        clearTimeout(state.resizeTimer);
        state.resizeTimer = setTimeout(() => {
          invalidate();
          if (state.manual) {
            const kept = restorePos(state.rects.stage || stageRect());
            if (kept) setDock(kept.x, kept.y);
            return;
          }
          if (state.lastAnchor) moveTo(state.lastAnchor, { instant: true });
        }, 180);
      };
      global.addEventListener('resize', state.onResize);
    }

    const src = options.src || 'assets/learner/mascot-rig.svg';

    return fetch(src, { credentials: 'same-origin' })
      .then((res) => (res.ok ? res.text() : Promise.reject(new Error(`mascot rig ${res.status}`))))
      .then((markup) => {
        holder.innerHTML = markup;
        const svg = holder.querySelector('svg');
        state.svg = svg;
        state.root = svg;
        const byId = (id) => (svg ? svg.querySelector(`#${id}`) : null);
        state.parts = {
          body: byId('m-body'),
          torso: byId('m-torso'),
          head: byId('m-head'),
          eyeL: byId('m-eye-l'),
          eyeR: byId('m-eye-r'),
          smileL: byId('m-smile-l'),
          smileR: byId('m-smile-r'),
          pupilL: byId('m-pupil-l'),
          pupilR: byId('m-pupil-r'),
          browL: byId('m-brow-l'),
          browR: byId('m-brow-r'),
          mouth: byId('m-mouth'),
          armL: byId('m-arm-l'),
          armR: byId('m-arm-r'),
          pencil: byId('m-pencil')
        };
        if (svg) svg.removeAttribute('role'); // decorative next to real text

        state.pointer = { x: window.innerWidth / 2, y: 0, t: 0 };
        readRects();
        const stage = state.rects.stage;
        state.home = { x: Math.max(8, stage.width - 128), y: Math.max(8, stage.height - 150) };
        // A spot the learner dragged Vee to survives a reload and a resize.
        const restored = restorePos(stage);
        state.manual = Boolean(restored);
        state.target = restored ? { ...restored } : { ...state.home };
        dock.style.transform = `translate(${state.target.x}px, ${state.target.y}px)`;
        setMood(options.mood || 'idle');

        state.onMove = (e) => {
          state.pointer.x = e.clientX;
          state.pointer.y = e.clientY;
          state.pointer.t = performance.now();
        };
        state.onScroll = invalidate;
        window.addEventListener('pointermove', state.onMove, { passive: true });
        window.addEventListener('resize', invalidate);
        window.addEventListener('scroll', state.onScroll, { passive: true });

        state.ready = true;
        poseOnce();
        // Always run the frame loop: pupils track the cursor even for learners
        // who turned motion down, only the decorative bob/blink/drift is skipped.
        state.raf = requestAnimationFrame(tick);

        return api;
      })
      .catch(() => {
        // No rig (offline, 404): fall back to the flat mascot, parked in its corner
        // so it can never sit on top of the answer options.
        holder.innerHTML = `<img src="assets/learner/mascot.svg" alt="" width="112" height="112">`;
        state.ready = true;
        state.reduced = true;
        readRects();
        const stageBox = state.rects.stage;
        state.home = { x: Math.max(8, stageBox.width - 128), y: Math.max(8, stageBox.height - 150) };
        const kept = restorePos(stageBox);
        state.manual = Boolean(kept);
        state.target = kept ? { ...kept } : { ...state.home };
        dock.style.transform = `translate(${state.target.x}px, ${state.target.y}px)`;
        return api;
      });
  }

  function destroy() {
    if (state.raf) cancelAnimationFrame(state.raf);
    state.raf = null;
    if (state.onMove) window.removeEventListener('pointermove', state.onMove);
    if (state.onScroll) window.removeEventListener('scroll', state.onScroll);
    window.removeEventListener('resize', invalidate);
    hideBubble();
    if (state.host) state.host.innerHTML = '';
    state.ready = false;
  }

  // writing: pencil scribble while the board draws
  function writing(on) {
    const { pencil } = state.parts;
    if (!pencil) return;
    if (on) {
      pencil.style.transition = 'transform 200ms ease';
      pencil.style.transform = 'rotate(-18deg) translateY(-2px)';
      setMood('writing');
    } else {
      pencil.style.transform = 'rotate(0deg)';
      setMood('idle');
    }
  }

  const api = {
    attach,
    destroy,
    hop,
    mood: setMood,
    moveTo,
    park,
    pointAt,
    say,
    hideBubble,
    writing,
    invalidate,
    poseOnce,
    pupilOffset,
    easeFactor,
    moods: Object.keys(MOUTH),
    isReady: () => state.ready,
    isManual: () => state.manual,
    // A drag ends in a click event: the page must not read that as "open the board".
    wasDragged: () => Date.now() - state.dragAt < 400,
    resetPosition,
    isReduced: () => state.reduced || prefersReduced(),
    position: () => ({ ...state.target }),
    parts: () => state.parts
  };

  global.Mascot = api;
})(window);
