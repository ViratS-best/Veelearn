/**
 * Veelearn Scratch stage: 480x360 canvas renderer + sprite helpers.
 */
(function (global) {
  'use strict';

  const STAGE_W = 480;
  const STAGE_H = 360;

  function scratchToCanvas(x, y) {
    return { cx: STAGE_W / 2 + x, cy: STAGE_H / 2 - y };
  }

  function canvasToScratch(cx, cy) {
    return { x: cx - STAGE_W / 2, y: STAGE_H / 2 - cy };
  }

  function makeDefaultCostume(name, color) {
    const c = document.createElement('canvas');
    c.width = 96;
    c.height = 96;
    const ctx = c.getContext('2d');
    ctx.fillStyle = color || '#6366f1';
    ctx.beginPath();
    ctx.ellipse(48, 52, 28, 36, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = '#fff';
    ctx.beginPath();
    ctx.arc(38, 42, 6, 0, Math.PI * 2);
    ctx.arc(58, 42, 6, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = '#111';
    ctx.beginPath();
    ctx.arc(38, 42, 3, 0, Math.PI * 2);
    ctx.arc(58, 42, 3, 0, Math.PI * 2);
    ctx.fill();
    return {
      name: name || 'costume1',
      dataUrl: c.toDataURL('image/png'),
      bitmapResolution: 1,
      rotationCenterX: 48,
      rotationCenterY: 48,
      width: 96,
      height: 96
    };
  }

  function makeDefaultBackdrop(name, color) {
    const c = document.createElement('canvas');
    c.width = STAGE_W;
    c.height = STAGE_H;
    const ctx = c.getContext('2d');
    const g = ctx.createLinearGradient(0, 0, 0, STAGE_H);
    g.addColorStop(0, color || '#87CEEB');
    g.addColorStop(1, '#E0F2FE');
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, STAGE_W, STAGE_H);
    return {
      name: name || 'backdrop1',
      dataUrl: c.toDataURL('image/png'),
      width: STAGE_W,
      height: STAGE_H
    };
  }

  function makeLibraryCostume(kind) {
    const c = document.createElement('canvas');
    c.width = 100;
    c.height = 100;
    const ctx = c.getContext('2d');
    if (kind === 'ball') {
      const g = ctx.createRadialGradient(40, 35, 5, 50, 50, 40);
      g.addColorStop(0, '#fca5a5');
      g.addColorStop(1, '#ef4444');
      ctx.fillStyle = g;
      ctx.beginPath();
      ctx.arc(50, 50, 40, 0, Math.PI * 2);
      ctx.fill();
    } else if (kind === 'box') {
      ctx.fillStyle = '#f59e0b';
      ctx.fillRect(20, 20, 60, 60);
      ctx.strokeStyle = '#92400e';
      ctx.lineWidth = 3;
      ctx.strokeRect(20, 20, 60, 60);
    } else if (kind === 'arrow') {
      ctx.fillStyle = '#10b981';
      ctx.beginPath();
      ctx.moveTo(20, 50);
      ctx.lineTo(70, 20);
      ctx.lineTo(70, 40);
      ctx.lineTo(90, 40);
      ctx.lineTo(90, 60);
      ctx.lineTo(70, 60);
      ctx.lineTo(70, 80);
      ctx.closePath();
      ctx.fill();
    } else {
      return makeDefaultCostume(kind, '#8b5cf6');
    }
    return {
      name: kind,
      dataUrl: c.toDataURL('image/png'),
      bitmapResolution: 1,
      rotationCenterX: 50,
      rotationCenterY: 50,
      width: 100,
      height: 100
    };
  }

  function drawOneShape(ctx, s) {
    if (!s || typeof s !== 'object') return;
    const shape = String(s.shape || s.type || 'rect').toLowerCase();
    const fill = s.fill || s.color || '#6366f1';
    const stroke = s.stroke || null;
    const lw = s.lineWidth != null ? Number(s.lineWidth) : 2;

    ctx.save();
    if (s.opacity != null) ctx.globalAlpha = Math.max(0, Math.min(1, Number(s.opacity)));
    if (s.rotate) {
      const cx = Number(s.x) || 0;
      const cy = Number(s.y) || 0;
      ctx.translate(cx, cy);
      ctx.rotate((Number(s.rotate) * Math.PI) / 180);
      ctx.translate(-cx, -cy);
    }

    const applyFillStroke = () => {
      if (fill && fill !== 'none') {
        ctx.fillStyle = fill;
        ctx.fill();
      }
      if (stroke) {
        ctx.strokeStyle = stroke;
        ctx.lineWidth = lw;
        ctx.stroke();
      }
    };

    if (shape === 'rect' || shape === 'rectangle') {
      const x = Number(s.x) || 0;
      const y = Number(s.y) || 0;
      const w = Number(s.w != null ? s.w : s.width) || 40;
      const h = Number(s.h != null ? s.h : s.height) || 40;
      ctx.beginPath();
      ctx.rect(x, y, w, h);
      applyFillStroke();
    } else if (shape === 'roundedrect' || shape === 'roundrect') {
      const x = Number(s.x) || 0;
      const y = Number(s.y) || 0;
      const w = Number(s.w != null ? s.w : s.width) || 40;
      const h = Number(s.h != null ? s.h : s.height) || 40;
      const r = Math.min(Number(s.r) || 8, w / 2, h / 2);
      ctx.beginPath();
      ctx.moveTo(x + r, y);
      ctx.arcTo(x + w, y, x + w, y + h, r);
      ctx.arcTo(x + w, y + h, x, y + h, r);
      ctx.arcTo(x, y + h, x, y, r);
      ctx.arcTo(x, y, x + w, y, r);
      ctx.closePath();
      applyFillStroke();
    } else if (shape === 'circle' || shape === 'sphere') {
      const x = Number(s.x) || 0;
      const y = Number(s.y) || 0;
      const r = Number(s.r != null ? s.r : s.radius) || 20;
      if (shape === 'sphere') {
        const g = ctx.createRadialGradient(x - r * 0.3, y - r * 0.3, r * 0.1, x, y, r);
        g.addColorStop(0, s.highlight || '#ffffff');
        g.addColorStop(0.35, fill);
        g.addColorStop(1, s.shade || '#111827');
        ctx.fillStyle = g;
        ctx.beginPath();
        ctx.arc(x, y, r, 0, Math.PI * 2);
        ctx.fill();
      } else {
        ctx.beginPath();
        ctx.arc(x, y, r, 0, Math.PI * 2);
        applyFillStroke();
      }
    } else if (shape === 'ellipse' || shape === 'oval') {
      const x = Number(s.x) || 0;
      const y = Number(s.y) || 0;
      const rx = Number(s.rx != null ? s.rx : s.w / 2) || 20;
      const ry = Number(s.ry != null ? s.ry : s.h / 2) || 30;
      ctx.beginPath();
      ctx.ellipse(x, y, rx, ry, 0, 0, Math.PI * 2);
      applyFillStroke();
    } else if (shape === 'trapezoid') {
      const x = Number(s.x) || 0;
      const y = Number(s.y) || 0;
      const wTop = Number(s.wTop != null ? s.wTop : s.top) || 40;
      const wBottom = Number(s.wBottom != null ? s.wBottom : s.bottom) || 80;
      const h = Number(s.h) || 50;
      ctx.beginPath();
      ctx.moveTo(x - wTop / 2, y);
      ctx.lineTo(x + wTop / 2, y);
      ctx.lineTo(x + wBottom / 2, y + h);
      ctx.lineTo(x - wBottom / 2, y + h);
      ctx.closePath();
      applyFillStroke();
    } else if (shape === 'triangle') {
      const x = Number(s.x) || 0;
      const y = Number(s.y) || 0;
      const w = Number(s.w) || 40;
      const h = Number(s.h) || 50;
      ctx.beginPath();
      ctx.moveTo(x, y);
      ctx.lineTo(x + w / 2, y + h);
      ctx.lineTo(x - w / 2, y + h);
      ctx.closePath();
      applyFillStroke();
    } else if (shape === 'line') {
      ctx.beginPath();
      ctx.moveTo(Number(s.x1) || 0, Number(s.y1) || 0);
      ctx.lineTo(Number(s.x2) || 0, Number(s.y2) || 0);
      ctx.strokeStyle = stroke || fill;
      ctx.lineWidth = lw;
      ctx.stroke();
    } else if (shape === 'polygon' && Array.isArray(s.points) && s.points.length >= 3) {
      ctx.beginPath();
      s.points.forEach((p, i) => {
        const px = Array.isArray(p) ? p[0] : p.x;
        const py = Array.isArray(p) ? p[1] : p.y;
        if (i === 0) ctx.moveTo(px, py);
        else ctx.lineTo(px, py);
      });
      ctx.closePath();
      applyFillStroke();
    } else if (shape === 'text') {
      ctx.fillStyle = fill;
      ctx.font = s.font || '16px sans-serif';
      ctx.fillText(String(s.text || ''), Number(s.x) || 0, Number(s.y) || 0);
    }
    ctx.restore();
  }

  /**
   * Build a costume/backdrop from declarative shapes (AI / procedural art).
   * @param {string} name
   * @param {Array<object>} shapes
   * @param {{ width?: number, height?: number, bg?: string, asBackdrop?: boolean }} opts
   */
  function makeShapesAsset(name, shapes, opts) {
    const options = opts || {};
    const asBackdrop = !!options.asBackdrop;
    const width = Math.max(16, Math.min(960, Number(options.width) || (asBackdrop ? STAGE_W : 128)));
    const height = Math.max(16, Math.min(720, Number(options.height) || (asBackdrop ? STAGE_H : 128)));
    const c = document.createElement('canvas');
    c.width = width;
    c.height = height;
    const ctx = c.getContext('2d');
    if (options.bg && options.bg !== 'transparent') {
      ctx.fillStyle = options.bg;
      ctx.fillRect(0, 0, width, height);
    } else if (asBackdrop) {
      ctx.fillStyle = '#0f172a';
      ctx.fillRect(0, 0, width, height);
    } else {
      ctx.clearRect(0, 0, width, height);
    }
    const list = Array.isArray(shapes) ? shapes.slice(0, 80) : [];
    for (const s of list) drawOneShape(ctx, s);
    return {
      name: name || (asBackdrop ? 'backdrop' : 'costume'),
      dataUrl: c.toDataURL('image/png'),
      bitmapResolution: 1,
      rotationCenterX: width / 2,
      rotationCenterY: height / 2,
      width,
      height
    };
  }

  class ScratchStage {
    constructor(canvas, monitorsEl, speechEl) {
      this.canvas = canvas;
      this.ctx = canvas.getContext('2d');
      this.monitorsEl = monitorsEl;
      this.speechEl = speechEl;
      this.imageCache = new Map();
      this.mouse = { x: 0, y: 0, down: false };
      this.keys = new Set();
      this.answer = '';
      this.timerStart = performance.now();
      this.monitors = new Map(); // name -> {value, mode, min, max, x, y}
      this._bindInput();
    }

    _bindInput() {
      const wrap = this.canvas.parentElement;
      const updateMouse = (e) => {
        const rect = this.canvas.getBoundingClientRect();
        const cx = ((e.clientX - rect.left) / rect.width) * STAGE_W;
        const cy = ((e.clientY - rect.top) / rect.height) * STAGE_H;
        const p = canvasToScratch(cx, cy);
        this.mouse.x = p.x;
        this.mouse.y = p.y;
      };
      this.canvas.addEventListener('mousemove', updateMouse);
      this.canvas.addEventListener('mousedown', (e) => { updateMouse(e); this.mouse.down = true; });
      window.addEventListener('mouseup', () => { this.mouse.down = false; });
      window.addEventListener('keydown', (e) => {
        const k = this.normalizeKey(e.key);
        if (k) this.keys.add(k);
      });
      window.addEventListener('keyup', (e) => {
        const k = this.normalizeKey(e.key);
        if (k) this.keys.delete(k);
      });
      // Keep focus for keys when clicking stage
      this.canvas.tabIndex = 0;
      this.canvas.addEventListener('click', () => this.canvas.focus());
    }

    normalizeKey(key) {
      if (!key) return null;
      const map = {
        ' ': 'space',
        ArrowLeft: 'left arrow',
        ArrowRight: 'right arrow',
        ArrowUp: 'up arrow',
        ArrowDown: 'down arrow'
      };
      if (map[key]) return map[key];
      if (key.length === 1) return key.toLowerCase();
      return key.toLowerCase();
    }

    isKeyPressed(option) {
      if (option === 'any') return this.keys.size > 0;
      return this.keys.has(option);
    }

    timer() {
      return (performance.now() - this.timerStart) / 1000;
    }

    resetTimer() {
      this.timerStart = performance.now();
    }

    async loadImage(dataUrl) {
      if (!dataUrl) return null;
      if (this.imageCache.has(dataUrl)) return this.imageCache.get(dataUrl);
      const img = new Image();
      const p = new Promise((resolve, reject) => {
        img.onload = () => resolve(img);
        img.onerror = reject;
      });
      img.src = dataUrl;
      this.imageCache.set(dataUrl, p);
      try {
        const loaded = await p;
        this.imageCache.set(dataUrl, loaded);
        return loaded;
      } catch {
        this.imageCache.delete(dataUrl);
        return null;
      }
    }

    getCostumeImage(costume) {
      if (!costume) return null;
      const cached = this.imageCache.get(costume.dataUrl);
      if (cached && !(cached instanceof Promise)) return cached;
      this.loadImage(costume.dataUrl);
      return null;
    }

    setMonitor(name, value, opts = {}) {
      const existing = this.monitors.get(name) || {
        mode: 'default',
        min: 0,
        max: 100,
        x: 10 + this.monitors.size * 8,
        y: 10 + this.monitors.size * 36
      };
      existing.value = value;
      if (opts.mode) existing.mode = opts.mode;
      if (opts.visible !== undefined) existing.visible = opts.visible;
      else if (existing.visible === undefined) existing.visible = true;
      this.monitors.set(name, existing);
      this.renderMonitors();
    }

    hideMonitor(name) {
      const m = this.monitors.get(name);
      if (m) {
        m.visible = false;
        this.renderMonitors();
      }
    }

    renderMonitors() {
      if (!this.monitorsEl) return;
      this.monitorsEl.innerHTML = '';
      for (const [name, m] of this.monitors) {
        if (m.visible === false) continue;
        const el = document.createElement('div');
        el.className = 'monitor' + (m.mode === 'slider' ? ' slider' : '');
        el.style.left = m.x + 'px';
        el.style.top = m.y + 'px';
        if (m.mode === 'slider') {
          el.innerHTML = `<label>${name}: <span class="val">${m.value}</span></label>`;
          const input = document.createElement('input');
          input.type = 'range';
          input.min = m.min;
          input.max = m.max;
          input.step = (m.max - m.min) / 100 || 1;
          input.value = Number(m.value) || 0;
          input.addEventListener('input', () => {
            m.value = Number(input.value);
            el.querySelector('.val').textContent = m.value;
            if (this.onSliderChange) this.onSliderChange(name, m.value);
          });
          el.appendChild(input);
        } else {
          el.textContent = `${name}: ${m.value}`;
        }
        this.monitorsEl.appendChild(el);
      }
    }

    renderSpeech(targets) {
      if (!this.speechEl) return;
      this.speechEl.innerHTML = '';
      for (const t of targets) {
        if (!t.visible || !t.bubble) continue;
        const { cx, cy } = scratchToCanvas(t.x, t.y);
        const el = document.createElement('div');
        el.className = 'bubble' + (t.bubble.think ? ' think' : '');
        el.textContent = String(t.bubble.text);
        el.style.left = cx + 'px';
        el.style.top = (cy - 20) + 'px';
        this.speechEl.appendChild(el);
      }
    }

    draw(project, targets) {
      const ctx = this.ctx;
      ctx.clearRect(0, 0, STAGE_W, STAGE_H);

      // Backdrop
      const stage = project.stage;
      const bd = stage.backdrops[stage.currentBackdrop || 0];
      if (bd) {
        const img = this.getCostumeImage(bd);
        if (img) ctx.drawImage(img, 0, 0, STAGE_W, STAGE_H);
        else {
          ctx.fillStyle = '#87CEEB';
          ctx.fillRect(0, 0, STAGE_W, STAGE_H);
        }
      } else {
        ctx.fillStyle = '#87CEEB';
        ctx.fillRect(0, 0, STAGE_W, STAGE_H);
      }

      const sorted = [...targets].filter(t => t.visible !== false).sort((a, b) => (a.layer || 0) - (b.layer || 0));
      for (const t of sorted) {
        this.drawTarget(t);
      }
      this.renderSpeech(targets);
    }

    drawTarget(t) {
      const costume = t.costumes[t.currentCostume || 0];
      const img = costume ? this.getCostumeImage(costume) : null;
      const { cx, cy } = scratchToCanvas(t.x, t.y);
      const ctx = this.ctx;
      ctx.save();
      ctx.translate(cx, cy);

      const size = (t.size || 100) / 100;
      let flip = 1;
      const style = t.rotationStyle || 'all around';
      let rot = ((t.direction || 90) - 90) * Math.PI / 180;
      if (style === 'left-right') {
        if (Math.abs(((t.direction || 90) + 360) % 360 - 180) < 90 || (t.direction || 90) < 0) {
          // facing left-ish
        }
        if ((t.direction || 90) < 0 || Math.abs(t.direction) > 90 && Math.abs(t.direction) < 270) {
          // Scratch: negative direction or past 90 means flip
        }
        // Simplified left-right: flip when direction is between -180..0 or 180..360 pointing left
        const d = ((t.direction % 360) + 360) % 360;
        if (d > 180) flip = -1;
        rot = 0;
      } else if (style === "don't rotate") {
        rot = 0;
      }
      ctx.rotate(rot);
      ctx.scale(size * flip, size);

      const ghost = (t.effects && t.effects.ghost) || 0;
      const brightness = (t.effects && t.effects.brightness) || 0;
      ctx.globalAlpha = Math.max(0, Math.min(1, 1 - ghost / 100));
      if (brightness) {
        ctx.filter = `brightness(${100 + brightness}%)`;
      }

      if (img) {
        const rcx = costume.rotationCenterX || img.width / 2;
        const rcy = costume.rotationCenterY || img.height / 2;
        ctx.drawImage(img, -rcx, -rcy);
      } else {
        ctx.fillStyle = '#6366f1';
        ctx.beginPath();
        ctx.ellipse(0, 0, 30, 40, 0, 0, Math.PI * 2);
        ctx.fill();
      }
      ctx.restore();
    }

    getTargetBounds(t) {
      const costume = t.costumes[t.currentCostume || 0];
      const size = (t.size || 100) / 100;
      const w = (costume?.width || 60) * size;
      const h = (costume?.height || 60) * size;
      return { left: t.x - w / 2, right: t.x + w / 2, top: t.y + h / 2, bottom: t.y - h / 2, w, h };
    }

    touchingEdge(t) {
      const b = this.getTargetBounds(t);
      return b.left <= -STAGE_W / 2 || b.right >= STAGE_W / 2 || b.bottom <= -STAGE_H / 2 || b.top >= STAGE_H / 2;
    }

    touchingMouse(t) {
      const b = this.getTargetBounds(t);
      return this.mouse.x >= b.left && this.mouse.x <= b.right && this.mouse.y >= b.bottom && this.mouse.y <= b.top;
    }

    touchingSprite(t, other) {
      if (!other || !other.visible) return false;
      const a = this.getTargetBounds(t);
      const b = this.getTargetBounds(other);
      return !(a.right < b.left || a.left > b.right || a.top < b.bottom || a.bottom > b.top);
    }

    distanceToMouse(t) {
      const dx = this.mouse.x - t.x;
      const dy = this.mouse.y - t.y;
      return Math.sqrt(dx * dx + dy * dy);
    }

    drawStageThumb(canvas, project) {
      const ctx = canvas.getContext('2d');
      const bd = project.stage.backdrops[project.stage.currentBackdrop || 0];
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      if (bd) {
        const img = this.getCostumeImage(bd);
        if (img) ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        else {
          ctx.fillStyle = '#87CEEB';
          ctx.fillRect(0, 0, canvas.width, canvas.height);
        }
      }
    }
  }

  global.ScratchStage = ScratchStage;
  global.ScratchStageUtils = {
    STAGE_W,
    STAGE_H,
    scratchToCanvas,
    canvasToScratch,
    makeDefaultCostume,
    makeDefaultBackdrop,
    makeLibraryCostume,
    makeShapesAsset
  };
})(window);
