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
  const FAR = 260; // px at which pupils are fully deflected
  const BOB_MS = 3000; // idle bob period
  const IDLE_DRIFT_MS = 12000;

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
    bubbleEl: null,
    bubbleTimer: null,
    leaderEl: null,
    leaderTimer: null,
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

  function readRects() {
    const stage = stageRect();
    state.rects.stage = stage;
    const l = state.parts.pupilL && state.parts.pupilL.getBoundingClientRect();
    const r = state.parts.pupilR && state.parts.pupilR.getBoundingClientRect();
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
  function placeFor(anchorEl) {
    const el = q(anchorEl);
    const stage = state.rects.stage || stageRect();
    if (!el) {
      // never throw, never guess: fall back to the centre of the problem card
      return { x: stage.width / 2 - 56, y: stage.height - 130 };
    }
    const r = el.getBoundingClientRect();
    let x = r.left - stage.left - 118; // sit to the left of what we point at
    let y = r.top - stage.top + r.height / 2 - 56;

    if (x < 8) x = r.right - stage.left + 10; // no room on the left, go right
    x = clamp(x, 8, Math.max(8, stage.width - 120));
    y = clamp(y, 8, Math.max(8, stage.height - 120));

    // never cover the answer options
    const opts = state.rects.options;
    if (opts) {
      const box = { left: stage.left + x, top: stage.top + y, right: stage.left + x + 112, bottom: stage.top + y + 112 };
      const hit = !(box.right < opts.left || box.left > opts.right || box.bottom < opts.top || box.top > opts.bottom);
      if (hit) {
        const above = opts.top - stage.top - 122;
        y = above > 8 ? above : clamp(opts.bottom - stage.top + 10, 8, Math.max(8, stage.height - 120));
      }
    }
    return { x, y };
  }

  function moveTo(anchorEl, opts) {
    if (!state.ready) return Promise.resolve();
    const options = opts || {};
    const stage = state.rects.stage || stageRect();
    const el = q(anchorEl);
    const dest = placeFor(anchorEl);
    const from = { x: state.target.x, y: state.target.y };
    const distance = Math.hypot(dest.x - from.x, dest.y - from.y);
    const flip = el ? (el.getBoundingClientRect().left - stage.left > from.x + 56 ? 1 : -1) : 1;

    state.target = dest;
    state.targetFlip = flip;
    state.lastNarration = performance.now();

    const dock = state.dock;
    if (!dock) return Promise.resolve();

    if (state.reduced || options.instant) {
      dock.style.transition = 'none';
      dock.style.transform = `translate(${dest.x}px, ${dest.y}px) scaleX(${flip})`;
      return Promise.resolve();
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
  function leaderTo(anchorEl) {
    const line = state.leaderEl;
    if (!line) return;
    const el = q(anchorEl);
    const stage = state.rects.stage || stageRect();
    if (!el) {
      line.hidden = true;
      return;
    }
    const r = el.getBoundingClientRect();
    const fromX = state.target.x + (state.targetFlip > 0 ? 0 : 112);
    const fromY = state.target.y + 56;
    const toX = r.left - stage.left + (state.targetFlip > 0 ? 0 : r.width);
    const toY = r.top - stage.top + r.height / 2;

    const dx = toX - fromX;
    const dy = toY - fromY;
    const len = Math.hypot(dx, dy);
    const angle = (Math.atan2(dy, dx) * 180) / Math.PI;

    line.hidden = false;
    line.style.width = `${Math.max(0, len)}px`;
    line.style.transform = `translate(${fromX}px, ${fromY}px) rotate(${angle}deg)`;
    clearTimeout(state.leaderTimer);
    state.leaderTimer = setTimeout(() => {
      line.hidden = true;
    }, 600);
  }

  function pointAt(anchorEl, opts) {
    const options = opts || {};
    setMood('pointing');
    return moveTo(anchorEl, options).then(() => {
      leaderTo(anchorEl);
      if (options.text) return say(options.text, options.ms);
      return undefined;
    });
  }

  function park() {
    setMood('idle');
    state.target = { x: state.home.x, y: state.home.y };
    if (state.dock) {
      state.dock.style.transition = state.reduced ? 'none' : 'transform 420ms cubic-bezier(.32,.72,0,1)';
      state.dock.style.transform = `translate(${state.home.x}px, ${state.home.y}px) scaleX(1)`;
    }
    state.lastNarration = performance.now();
  }

  // ------------------------------------------------------------------ frame
  function tick(now) {
    const dt = Math.min(0.2, (now - (state.last || now)) / 1000);
    state.last = now;

    if (state.rectsDirty) readRects();

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
      pupil.style.transform = `translate(${cur.x.toFixed(2)}px, ${cur.y.toFixed(2)}px)`;
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
    const stage = state.rects.stage || stageRect();
    state.lastNarration = performance.now();
    const rest = { x: Math.max(8, stage.width - 128), y: Math.max(8, stage.height - 150) };
    state.target = rest;
    if (state.dock && !state.reduced) {
      state.dock.style.transition = 'transform 900ms cubic-bezier(.32,.72,0,1)';
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

    const leader = document.createElement('div');
    leader.className = 'sx-mascot-leader';
    leader.hidden = true;
    mount.appendChild(leader);

    state.dock = dock;
    state.bobEl = bob;
    state.bubbleEl = bubble;
    state.leaderEl = leader;

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
        state.target = { ...state.home };
        dock.style.transform = `translate(${state.home.x}px, ${state.home.y}px)`;
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
        if (!state.reduced) state.raf = requestAnimationFrame(tick);

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
        state.target = { ...state.home };
        dock.style.transform = `translate(${state.home.x}px, ${state.home.y}px)`;
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
    isReduced: () => state.reduced || prefersReduced(),
    position: () => ({ ...state.target }),
    parts: () => state.parts
  };

  global.Mascot = api;
})(window);
