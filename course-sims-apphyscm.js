/* ============================================================================
 * AP Physics C: Mechanics — one simulation per unit, with the calculus visible.
 * ========================================================================== */
(function () {
  'use strict';
  const S = window.CourseSims && window.CourseSims.util;
  if (!S) return;
  const { plot, curve, arrow, dot, label, fmt, clamp, lerp, PALETTE } = S;
  const G = 9.8;

  /* U1 — integrate acceleration to recover motion */
  window.CourseSims.register('apphyscm-u1-calculus-kinematics', {
    title: 'Integrate a(t) twice to get the motion',
    blurb:
      'Here the acceleration is not constant: a(t) = a₀ + jt. Velocity is its area, position is the area of the velocity graph — the calculus is just accumulation.',
    params: [
      { k: 'a0', label: 'a₀ (m/s²)', min: -2, max: 4, step: 0.5, val: 1, decimals: 1 },
      { k: 'j', label: 'jerk j (m/s³)', min: -1, max: 1, step: 0.1, val: 0.4, decimals: 1 },
      { k: 't', label: 'time (s)', min: 0, max: 5, step: 0.1, val: 3, decimals: 1 }
    ],
    readout(s) {
      const v = s.a0 * s.t + 0.5 * s.j * s.t * s.t;
      const x = 0.5 * s.a0 * s.t * s.t + (s.j * s.t ** 3) / 6;
      return [
        ['a(t)', fmt(s.a0 + s.j * s.t, 2) + ' m/s²'],
        ['v(t) = ∫a dt', fmt(v, 2) + ' m/s'],
        ['x(t) = ∫v dt', fmt(x, 2) + ' m'],
        ['jerk', fmt(s.j, 1) + ' m/s³']
      ];
    },
    note(s) {
      return s.j === 0
        ? 'With zero jerk the acceleration is constant and the familiar ½at² formulas apply. Any nonzero jerk makes those formulas wrong after the first instant.'
        : 'Constant-acceleration formulas fail here: a is changing, so v is a curve, not a line. Integrating term by term still works, which is why calculus replaces the formula sheet.';
    },
    draw(ctx, s, box) {
      const h3 = (box.h - 16) / 3;
      const p1 = plot(ctx, { x: box.x, y: box.y, w: box.w, h: h3 }, { xmin: 0, xmax: 5, ymin: -3, ymax: 5, ticks: 2, xdigits: 0, ydigits: 0, xlabel: 'a' });
      curve(ctx, p1, (t) => s.a0 + s.j * t, PALETTE.amber, 2, 0, 5, 120);
      dot(ctx, p1.X(s.t), p1.clipY(s.a0 + s.j * s.t), 3.4, PALETTE.accent);

      const p2 = plot(ctx, { x: box.x, y: box.y + h3 + 6, w: box.w, h: h3 }, { xmin: 0, xmax: 5, ymin: -6, ymax: 16, ticks: 2, xdigits: 0, ydigits: 0, xlabel: 'v' });
      curve(ctx, p2, (t) => s.a0 * t + 0.5 * s.j * t * t, PALETTE.green, 2, 0, 5, 120);
      dot(ctx, p2.X(s.t), p2.clipY(s.a0 * s.t + 0.5 * s.j * s.t * s.t), 3.4, PALETTE.accent);

      const p3 = plot(ctx, { x: box.x, y: box.y + (h3 + 6) * 2, w: box.w, h: h3 }, { xmin: 0, xmax: 5, ymin: -2, ymax: 24, ticks: 2, xdigits: 0, ydigits: 0, xlabel: 'x' });
      curve(ctx, p3, (t) => 0.5 * s.a0 * t * t + (s.j * t ** 3) / 6, PALETTE.blue, 2, 0, 5, 120);
      dot(ctx, p3.X(s.t), p3.clipY(0.5 * s.a0 * s.t * s.t + (s.j * s.t ** 3) / 6), 3.4, PALETTE.accent);
    }
  });

  /* U2 — linear drag and terminal velocity */
  window.CourseSims.register('apphyscm-u2-drag', {
    title: 'Drag: the acceleration that switches itself off',
    blurb:
      'With drag proportional to velocity, the net force shrinks as the object speeds up. The velocity approaches a terminal value asymptotically — it never quite arrives.',
    params: [
      { k: 'm', label: 'mass (kg)', min: 0.5, max: 5, step: 0.1, val: 2, decimals: 1 },
      { k: 'b', label: 'drag b (N·s/m)', min: 0.5, max: 6, step: 0.1, val: 2, decimals: 1 }
    ],
    readout(s) {
      const vt = (s.m * G) / s.b;
      const tau = s.m / s.b;
      const v2 = vt * (1 - Math.exp(-2 / tau));
      return [
        ['terminal velocity', fmt(vt, 2) + ' m/s'],
        ['time constant m/b', fmt(tau, 2) + ' s'],
        ['v at t = 2 s', fmt(v2, 2) + ' m/s'],
        ['a at t = 0', fmt(G, 1) + ' m/s²']
      ];
    },
    note(s) {
      return 'Terminal velocity is the speed where drag equals weight, so the net force is zero. Halving b doubles the terminal speed, but the approach still takes a few time constants.';
    },
    draw(ctx, s, box) {
      const vt = (s.m * G) / s.b;
      const tau = s.m / s.b;
      const p = plot(ctx, box, { xmin: 0, xmax: 6, ymin: 0, ymax: vt * 1.1, ticks: 4, xdigits: 0, xlabel: 'time (s)', ylabel: 'v' });
      curve(ctx, p, (t) => vt * (1 - Math.exp(-t / tau)), PALETTE.blue, 2.6, 0, 6, 200);

      ctx.save();
      ctx.setLineDash([5, 4]);
      ctx.strokeStyle = PALETTE.green;
      ctx.beginPath();
      ctx.moveTo(p.x0, p.Y(vt));
      ctx.lineTo(p.x0 + p.w, p.Y(vt));
      ctx.stroke();
      ctx.restore();
      label(ctx, 'v_terminal = mg/b', p.x0 + p.w - 8, p.Y(vt) - 6, PALETTE.green, 10, 'right');

      const t0 = tau;
      dot(ctx, p.X(t0), p.Y(vt * (1 - Math.exp(-1))), 4, PALETTE.accent);
      label(ctx, '1 time constant → 63%', p.X(t0) + 8, p.Y(vt * 0.63) + 14, PALETTE.accent, 10, 'left');
    }
  });

  /* U3 — work as the integral of a variable force */
  window.CourseSims.register('apphyscm-u3-work-integral', {
    title: 'Work is the area under F(x)',
    blurb:
      'A force that grows with distance does more work than F·d suggests, because each later metre is pushed harder than the first. The shaded area is the work.',
    params: [
      { k: 'k', label: 'force scale k (N/mᵖ)', min: 1, max: 12, step: 0.5, val: 4, decimals: 1 },
      { k: 'p', label: 'exponent p', min: 0, max: 2, step: 0.1, val: 1, decimals: 1 },
      { k: 'd', label: 'displacement d (m)', min: 0.2, max: 3, step: 0.1, val: 2, decimals: 1 }
    ],
    readout(s) {
      const w = (s.k * Math.pow(s.d, s.p + 1)) / (s.p + 1);
      const f = s.k * Math.pow(s.d, s.p);
      return [
        ['work ∫F dx', fmt(w, 2) + ' J'],
        ['F at d', fmt(f, 2) + ' N'],
        ['F·d (wrong)', fmt(f * s.d, 2) + ' J'],
        ['average force', fmt(w / s.d, 2) + ' N']
      ];
    },
    note(s) {
      return s.p === 0
        ? 'With p = 0 the force is constant and F·d is exact — the area is a rectangle.'
        : 'Using the final force times distance overestimates the work badly, because F was smaller earlier. The integral weights every position correctly.';
    },
    draw(ctx, s, box) {
      const f = (x) => s.k * Math.pow(x, s.p);
      const fmax = f(3);
      const p = plot(ctx, box, { xmin: 0, xmax: 3, ymin: 0, ymax: fmax * 1.15, ticks: 4, xdigits: 1, ydigits: 0, xlabel: 'x (m)', ylabel: 'F (N)' });
      for (let i = 0; i < 60; i++) {
        const x = (s.d * i) / 60;
        const nx = (s.d * (i + 1)) / 60;
        ctx.fillStyle = 'rgba(5,150,105,0.15)';
        ctx.fillRect(p.X(x), p.Y(f(x)), p.X(nx) - p.X(x) + 1, p.Y(0) - p.Y(f(x)));
      }
      curve(ctx, p, f, PALETTE.blue, 2.4, 0, 3, 200);
      ctx.save();
      ctx.setLineDash([4, 4]);
      ctx.strokeStyle = PALETTE.accent;
      ctx.beginPath();
      ctx.moveTo(p.X(s.d), p.y0);
      ctx.lineTo(p.X(s.d), p.y0 + p.h);
      ctx.stroke();
      ctx.restore();
      label(ctx, 'd', p.X(s.d), p.y0 + p.h + 16, PALETTE.accent, 10);
      label(ctx, 'W = ' + fmt((s.k * Math.pow(s.d, s.p + 1)) / (s.p + 1), 1) + ' J', p.x0 + 10, p.y0 + 18, PALETTE.green, 11, 'left');
    }
  });

  /* U4 — centre of mass */
  window.CourseSims.register('apphyscm-u4-com', {
    title: 'Centre of mass: the point that moves simply',
    blurb:
      'Two masses on a rod. The centre of mass is the mass-weighted average position — and under any internal force, it moves as if all the mass and all the external force lived there.',
    params: [
      { k: 'm1', label: 'left mass (kg)', min: 1, max: 8, step: 0.5, val: 2, decimals: 1 },
      { k: 'm2', label: 'right mass (kg)', min: 1, max: 8, step: 0.5, val: 6, decimals: 1 },
      { k: 'x2', label: 'right position (m)', min: 2, max: 8, step: 0.2, val: 6, decimals: 1 }
    ],
    readout(s) {
      const com = (s.m1 * 0 + s.m2 * s.x2) / (s.m1 + s.m2);
      return [
        ['centre of mass', fmt(com, 2) + ' m'],
        ['total mass', fmt(s.m1 + s.m2, 1) + ' kg'],
        ['closer to', com < s.x2 / 2 ? 'left mass' : 'right mass'],
        ['fraction from left', fmt(com / s.x2, 2)]
      ];
    },
    note(s) {
      return s.m2 > s.m1
        ? 'The heavier mass pulls the centre toward itself, but never past it: the centre always lies between the masses.'
        : 'Equal masses put the centre exactly halfway. Doubling one mass moves it two-thirds of the way toward that mass.';
    },
    draw(ctx, s, box) {
      const com = (s.m1 * 0 + s.m2 * s.x2) / (s.m1 + s.m2);
      const y = box.y + box.h * 0.5;
      const X = (m) => box.x + 40 + (m / 8) * (box.w - 80);

      ctx.strokeStyle = '#8a5a34';
      ctx.lineWidth = 6;
      ctx.beginPath();
      ctx.moveTo(X(0), y);
      ctx.lineTo(X(8), y);
      ctx.stroke();

      const block = (x, m, color, name) => {
        const h = 26 + m * 5;
        ctx.fillStyle = color;
        ctx.fillRect(X(x) - 20, y - h / 2, 40, h);
        label(ctx, name, X(x), y + 4, '#fff', 11);
        label(ctx, fmt(m, 1) + ' kg', X(x), y + h / 2 + 16, PALETTE.soft, 10);
      };
      block(0, s.m1, 'rgba(37,99,235,0.85)', '1');
      block(s.x2, s.m2, 'rgba(217,119,6,0.85)', '2');

      dot(ctx, X(com), y - 46, 6, PALETTE.red, '#fff');
      ctx.save();
      ctx.setLineDash([3, 3]);
      ctx.strokeStyle = PALETTE.red;
      ctx.beginPath();
      ctx.moveTo(X(com), y - 40);
      ctx.lineTo(X(com), y);
      ctx.stroke();
      ctx.restore();
      label(ctx, 'COM ' + fmt(com, 2) + ' m', X(com), y - 58, PALETTE.red, 11);

      // ruler
      for (let m = 0; m <= 8; m += 2) label(ctx, String(m), X(m), y + 78, PALETTE.soft, 9);
      label(ctx, 'position (m)', X(4), y + 96, PALETTE.soft, 10);
    }
  });

  /* U5 — torque as a cross product, and the inertia that resists it */
  window.CourseSims.register('apphyscm-u5-torque-i', {
    title: 'Torque is r × F, and inertia decides α',
    blurb:
      'Push at a larger radius or at a better angle and the torque grows. The same torque produces a smaller angular acceleration on a shape whose mass sits farther from the axis.',
    params: [
      { k: 'r', label: 'lever arm r (m)', min: 0.2, max: 1.2, step: 0.05, val: 0.8, decimals: 2 },
      { k: 'F', label: 'force F (N)', min: 1, max: 30, step: 1, val: 12, decimals: 0 },
      { k: 'angle', label: 'angle θ (°)', min: 10, max: 90, step: 5, val: 60, decimals: 0 },
      {
        k: 'shape',
        label: 'rotating body',
        type: 'select',
        val: 'rod',
        options: [
          { v: 'rod', label: 'rod about end (ML²/3)' },
          { v: 'disc', label: 'disc (MR²/2)' },
          { v: 'hoop', label: 'hoop (MR²)' }
        ]
      }
    ],
    readout(s) {
      const th = (s.angle * Math.PI) / 180;
      const tau = s.r * s.F * Math.sin(th);
      const M = 2;
      const L = 1.2;
      const I = s.shape === 'rod' ? (M * L * L) / 3 : s.shape === 'disc' ? (M * L * L) / 8 : (M * L * L) / 4;
      return [
        ['torque τ', fmt(tau, 2) + ' N·m'],
        ['moment of inertia I', fmt(I, 3) + ' kg·m²'],
        ['angular acceleration', fmt(tau / I, 2) + ' rad/s²'],
        ['effective lever arm', fmt(s.r * Math.sin(th), 2) + ' m']
      ];
    },
    note(s) {
      return s.angle < 45
        ? 'Pushing almost along the lever gives a small torque even with a big force: only the perpendicular component counts.'
        : 'At 90° the whole force acts perpendicular, so τ = rF. That is the maximum a given force can produce at that radius.';
    },
    draw(ctx, s, box) {
      const th = (s.angle * Math.PI) / 180;
      const cx = box.x + box.w * 0.4;
      const cy = box.y + box.h * 0.55;
      const R = s.r * 130;

      ctx.strokeStyle = '#8a5a34';
      ctx.lineWidth = 7;
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.lineTo(cx + R, cy);
      ctx.stroke();
      dot(ctx, cx, cy, 6, PALETTE.ink);

      const px = cx + R * Math.cos(th);
      const py = cy - R * Math.sin(th);
      arrow(ctx, px, py, px + s.F * 5 * Math.cos(th - Math.PI / 2), py - s.F * 5 * Math.sin(th - Math.PI / 2), PALETTE.blue, 3);
      label(ctx, 'F', px + 6, py - 6, PALETTE.blue, 11, 'left');

      ctx.save();
      ctx.setLineDash([3, 3]);
      ctx.strokeStyle = PALETTE.soft;
      ctx.beginPath();
      ctx.arc(cx, cy, R * 0.28, 0, -th, true);
      ctx.stroke();
      ctx.restore();
      label(ctx, s.angle + '°', cx + R * 0.34, cy - 10, PALETTE.soft, 10, 'left');

      // body sketch
      const bx = box.x + box.w * 0.8;
      ctx.fillStyle = 'rgba(37,99,235,0.14)';
      ctx.strokeStyle = PALETTE.blue;
      ctx.lineWidth = 2;
      if (s.shape === 'rod') {
        ctx.fillRect(bx - 8, cy - 70, 16, 140);
        ctx.strokeRect(bx - 8, cy - 70, 16, 140);
      } else if (s.shape === 'disc') {
        ctx.beginPath();
        ctx.arc(bx, cy, 60, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
      } else {
        ctx.beginPath();
        ctx.arc(bx, cy, 60, 0, Math.PI * 2);
        ctx.stroke();
        ctx.beginPath();
        ctx.arc(bx, cy, 46, 0, Math.PI * 2);
        ctx.stroke();
      }
      label(ctx, s.shape, bx, cy + 90, PALETTE.soft, 10);
    }
  });

  /* U6 — Atwood machine with a massive pulley */
  window.CourseSims.register('apphyscm-u6-atwood', {
    title: 'A pulley with mass steals some of the acceleration',
    blurb:
      'A massless pulley would give a = (m₁ − m₂)g/(m₁ + m₂). Give the pulley inertia and it must be spun up too, so the acceleration drops.',
    params: [
      { k: 'm1', label: 'left mass (kg)', min: 1, max: 8, step: 0.5, val: 4, decimals: 1 },
      { k: 'm2', label: 'right mass (kg)', min: 1, max: 8, step: 0.5, val: 2, decimals: 1 },
      { k: 'I', label: 'pulley I (kg·m²)', min: 0, max: 4, step: 0.2, val: 1, decimals: 1 }
    ],
    readout(s) {
      const R = 0.15;
      const a = ((s.m1 - s.m2) * G) / (s.m1 + s.m2 + s.I / (R * R));
      const ideal = ((s.m1 - s.m2) * G) / (s.m1 + s.m2);
      return [
        ['acceleration', fmt(a, 2) + ' m/s²'],
        ['massless-pulley value', fmt(ideal, 2) + ' m/s²'],
        ['reduction', fmt(ideal - a, 2) + ' m/s²'],
        ['tension difference', fmt((s.I / (R * R)) * a, 2) + ' N']
      ];
    },
    note(s) {
      return s.I === 0
        ? 'With I = 0 the pulley is just a redirect for the string and the ideal Atwood result applies.'
        : 'The pulley adds I/R² to the effective mass on both sides. Real pulleys are never quite massless, which is why measured accelerations fall short of the textbook value.';
    },
    draw(ctx, s, box, t) {
      const R = 0.15;
      const a = ((s.m1 - s.m2) * G) / (s.m1 + s.m2 + s.I / (R * R));
      const cx = box.x + box.w / 2;
      const cy = box.y + 60;
      const phase = ((t || 0) / 1000) * 0.6;

      ctx.strokeStyle = '#8a5a34';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.arc(cx, cy, 26, 0, Math.PI * 2);
      ctx.stroke();
      dot(ctx, cx, cy, 4, PALETTE.ink);
      ctx.beginPath();
      ctx.moveTo(cx - 30, cy - 30);
      ctx.lineTo(cx + 30, cy - 30);
      ctx.stroke();

      const drop = Math.sin(phase) * 20;
      ctx.strokeStyle = '#b9a894';
      ctx.beginPath();
      ctx.moveTo(cx - 26, cy);
      ctx.lineTo(cx - 26, cy + 120 + drop);
      ctx.moveTo(cx + 26, cy);
      ctx.lineTo(cx + 26, cy + 120 - drop);
      ctx.stroke();

      const block = (x, y, m, color) => {
        const h = 22 + m * 4;
        ctx.fillStyle = color;
        ctx.fillRect(x - 22, y, 44, h);
        label(ctx, fmt(m, 1) + ' kg', x, y + h / 2 + 4, '#fff', 10);
      };
      block(cx - 26, cy + 120 + drop, s.m1, 'rgba(37,99,235,0.85)');
      block(cx + 26, cy + 120 - drop, s.m2, 'rgba(217,119,6,0.85)');

      label(ctx, 'a = ' + fmt(a, 2) + ' m/s²', cx, box.y + box.h - 12, PALETTE.ink, 12);
      if (s.I > 0) label(ctx, 'pulley must spin up too', cx, box.y + box.h - 32, PALETTE.soft, 10);
    }
  });

  /* U7 — physical versus simple pendulum */
  window.CourseSims.register('apphyscm-u7-pendulum', {
    title: 'Physical pendulum: where the mass sits changes the period',
    blurb:
      'A real pendulum is not a point mass on a string. Push the mass outward or use a rod and the same length gives a different period, because the period depends on I/(md).',
    params: [
      { k: 'L', label: 'length (m)', min: 0.3, max: 1.6, step: 0.05, val: 1, decimals: 2 },
      {
        k: 'shape',
        label: 'pendulum',
        type: 'select',
        val: 'simple',
        options: [
          { v: 'simple', label: 'point mass on a string' },
          { v: 'rod', label: 'uniform rod pivoted at an end' },
          { v: 'disc', label: 'disc of radius L/2 on the end' }
        ]
      }
    ],
    readout(s) {
      const g = 9.8;
      const simple = 2 * Math.PI * Math.sqrt(s.L / g);
      const T = s.shape === 'simple' ? simple : s.shape === 'rod' ? 2 * Math.PI * Math.sqrt(((2 * s.L) / 3) / g) : 2 * Math.PI * Math.sqrt(((s.L + (s.L / 2) ** 2 / s.L) / 2) / g);
      return [
        ['period T', fmt(T, 3) + ' s'],
        ['simple pendulum', fmt(simple, 3) + ' s'],
        ['difference', fmt(T - simple, 3) + ' s'],
        ['frequency', fmt(1 / T, 2) + ' Hz']
      ];
    },
    note(s) {
      return s.shape === 'simple'
        ? 'The simple pendulum formula assumes all mass at one point a distance L from the pivot. Real objects have mass spread out, which raises I and slows the swing.'
        : 'A physical pendulum has T = 2π√(I/(mgd)) with d the distance to the centre of mass. Spread-out mass means a longer period at the same length.';
    },
    draw(ctx, s, box, t) {
      const cx = box.x + box.w * 0.45;
      const cy = box.y + 26;
      const Lpx = s.L * 120;
      const theta = 0.5 * Math.cos(((t || 0) / 1200) * 2);
      const ex = cx + Math.sin(theta) * Lpx;
      const ey = cy + Math.cos(theta) * Lpx;

      ctx.strokeStyle = '#b9a894';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(cx - 50, cy);
      ctx.lineTo(cx + 50, cy);
      ctx.stroke();

      if (s.shape === 'rod') {
        ctx.strokeStyle = '#8a5a34';
        ctx.lineWidth = 7;
        ctx.beginPath();
        ctx.moveTo(cx, cy);
        ctx.lineTo(ex, ey);
        ctx.stroke();
      } else {
        ctx.strokeStyle = '#8a5a34';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(cx, cy);
        ctx.lineTo(ex, ey);
        ctx.stroke();
        dot(ctx, ex, ey, s.shape === 'disc' ? 26 : 14, '#f3e3cf', '#8a5a34');
      }
      dot(ctx, cx, cy, 4, PALETTE.ink);
      label(ctx, 'pivot', cx, cy - 10, PALETTE.soft, 10);
      label(ctx, 'T = ' + fmt(2 * Math.PI * Math.sqrt(s.L / 9.8), 2) + ' s (simple)', box.x + box.w * 0.7, box.y + 20, PALETTE.soft, 11, 'left');
    }
  });

  /* U8 — orbits, energy and escape speed */
  window.CourseSims.register('apphyscm-u8-orbit', {
    title: 'One speed decides circular, elliptical or escape',
    blurb:
      'Launch a satellite horizontally at increasing speed. Below circular speed it falls back; at circular speed it repeats; between there and escape it traces an ellipse; past escape it never returns.',
    params: [
      { k: 'v', label: 'launch speed (km/s)', min: 3, max: 12, step: 0.1, val: 7.5, decimals: 1 },
      { k: 'r0', label: 'launch radius (10³ km)', min: 7, max: 20, step: 0.5, val: 10, decimals: 1 }
    ],
    readout(s) {
      const mu = 3.986e14;
      const r0 = s.r0 * 1e6; // slider is in 10³ km
      const v = s.v * 1000;
      const vc = Math.sqrt(mu / r0) / 1000;
      const esc = Math.sqrt((2 * mu) / r0) / 1000;
      const E = (0.5 * v * v - mu / r0) / 1e6;
      return [
        ['circular speed', fmt(vc, 2) + ' km/s'],
        ['escape speed', fmt(esc, 2) + ' km/s'],
        ['specific energy', fmt(E, 1) + ' MJ/kg'],
        ['orbit', s.v < vc - 0.05 ? 'sub-orbital' : Math.abs(s.v - vc) < 0.08 ? 'circular' : s.v < esc ? 'elliptical' : 'escape']
      ];
    },
    note(s) {
      return s.v >= Math.sqrt(3.986e14 / (s.r0 * 1e6)) * 1.414 / 1000
        ? 'Above escape speed the total energy is positive and the path is a hyperbola: no amount of waiting brings the satellite back.'
        : 'The orbit shape is set by one number, the specific energy. Circular is the special case where the speed matches the local curvature exactly.';
    },
    draw(ctx, s, box) {
      const mu = 3.986e14;
      const r0 = s.r0 * 1e6;
      const x = [r0, 0];
      const vel = [0, s.v * 1000];
      const dt = 20;
      const pts = [];
      for (let i = 0; i < 4000; i++) {
        const r = Math.hypot(x[0], x[1]) || 1;
        const ax = (-mu * x[0]) / r ** 3;
        const ay = (-mu * x[1]) / r ** 3;
        vel[0] += ax * dt;
        vel[1] += ay * dt;
        x[0] += vel[0] * dt;
        x[1] += vel[1] * dt;
        pts.push([x[0], x[1]]);
        if (Math.hypot(x[0], x[1]) > r0 * 2.2) break;
      }
      const maxR = Math.max(r0 * 1.1, ...pts.map(([px, py]) => Math.hypot(px, py)));
      const scale = (Math.min(box.w, box.h) * 0.42) / maxR;
      const cx = box.x + box.w / 2;
      const cy = box.y + box.h / 2;

      dot(ctx, cx, cy, 10, '#dc2626', '#7f1d1d');
      ctx.strokeStyle = PALETTE.blue;
      ctx.lineWidth = 1.8;
      ctx.beginPath();
      pts.forEach(([px, py], i) => {
        const sx = cx + px * scale;
        const sy = cy - py * scale;
        if (i === 0) ctx.moveTo(sx, sy);
        else ctx.lineTo(sx, sy);
      });
      ctx.stroke();
      dot(ctx, cx + r0 * scale, cy, 3.5, PALETTE.accent);
      label(ctx, 'launch', cx + r0 * scale + 6, cy - 8, PALETTE.accent, 10, 'left');
    }
  });
})();
