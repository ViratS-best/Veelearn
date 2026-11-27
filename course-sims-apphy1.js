/* ============================================================================
 * AP Physics 1 — one simulation per unit, matched to that unit's sections.
 * ========================================================================== */
(function () {
  'use strict';
  const S = window.CourseSims && window.CourseSims.util;
  if (!S) return;
  const { plot, curve, arrow, dot, label, fmt, clamp, lerp, PALETTE } = S;

  /* U1 — position, velocity, acceleration together */
  window.CourseSims.register('apphy1-u1-kinematics', {
    title: 'Three graphs, one motion',
    blurb:
      'Set the initial velocity and acceleration, then move the clock. The dot’s slope on the x–t graph is the velocity, and the slope of v–t is the acceleration — the same number in all three views.',
    params: [
      { k: 'v0', label: 'v₀ (m/s)', min: -10, max: 15, step: 1, val: 4, decimals: 0 },
      { k: 'a', label: 'a (m/s²)', min: -5, max: 5, step: 0.5, val: 1, decimals: 1 },
      { k: 't', label: 'time t (s)', min: 0, max: 6, step: 0.1, val: 2, decimals: 1 }
    ],
    readout(s) {
      const x = s.v0 * s.t + 0.5 * s.a * s.t * s.t;
      const v = s.v0 + s.a * s.t;
      return [
        ['x', fmt(x, 2) + ' m'],
        ['v', fmt(v, 2) + ' m/s'],
        ['a', fmt(s.a, 1) + ' m/s²'],
        ['turning point', s.a !== 0 && -s.v0 / s.a > 0 ? fmt(-s.v0 / s.a, 2) + ' s' : 'none']
      ];
    },
    note(s) {
      const v = s.v0 + s.a * s.t;
      if (s.a === 0) return 'With zero acceleration the v–t graph is flat and the x–t graph is a straight line: constant velocity.';
      if (v * s.v0 < 0) return 'Velocity changed sign while acceleration stayed fixed: the object turned around at the moment v = 0, yet the acceleration never changed direction.';
      return 'The three graphs are the same motion read three ways: derivative goes uphill (x → v → a), integral goes downhill.';
    },
    draw(ctx, s, box) {
      const y = s.v0 * s.t + 0.5 * s.a * s.t * s.t;
      const trackH = 54;
      // track
      ctx.fillStyle = '#fdf6ec';
      ctx.fillRect(box.x, box.y, box.w, trackH);
      const xmin = Math.min(0, s.v0 * 6 + 18 * s.a, y);
      const xmax = Math.max(10, s.v0 * 6 + 18 * s.a, y);
      const X = (v) => box.x + 16 + ((v - xmin) / (xmax - xmin || 1)) * (box.w - 32);
      ctx.strokeStyle = '#d8c8b6';
      ctx.beginPath();
      ctx.moveTo(box.x + 8, box.y + trackH - 10);
      ctx.lineTo(box.x + box.w - 8, box.y + trackH - 10);
      ctx.stroke();
      dot(ctx, X(y), box.y + trackH - 18, 8, PALETTE.accent, '#fff');
      label(ctx, fmt(y, 1) + ' m', X(y), box.y + 16, PALETTE.accent, 10);

      const gTop = { x: box.x, y: box.y + trackH + 8, w: box.w, h: (box.h - trackH - 20) / 3 };
      const p1 = plot(ctx, gTop, { xmin: 0, xmax: 6, ymin: Math.min(0, xmin), ymax: Math.max(10, xmax), ticks: 2, xdigits: 0, ydigits: 0, xlabel: 'x' });
      curve(ctx, p1, (t) => s.v0 * t + 0.5 * s.a * t * t, PALETTE.blue, 2, 0, 6, 160);
      dot(ctx, p1.X(s.t), p1.clipY(y), 3.4, PALETTE.accent);

      const p2 = plot(ctx, { x: box.x, y: gTop.y + gTop.h + 4, w: box.w, h: gTop.h }, { xmin: 0, xmax: 6, ymin: Math.min(0, s.v0 + 6 * s.a) - 1, ymax: Math.max(2, s.v0 + 6 * s.a) + 1, ticks: 2, xdigits: 0, ydigits: 0, xlabel: 'v' });
      curve(ctx, p2, (t) => s.v0 + s.a * t, PALETTE.green, 2, 0, 6, 160);
      dot(ctx, p2.X(s.t), p2.clipY(s.v0 + s.a * s.t), 3.4, PALETTE.accent);

      const p3 = plot(ctx, { x: box.x, y: gTop.y + gTop.h * 2 + 8, w: box.w, h: gTop.h }, { xmin: 0, xmax: 6, ymin: -6, ymax: 6, ticks: 2, xdigits: 0, ydigits: 0, xlabel: 'a' });
      curve(ctx, p3, () => s.a, PALETTE.amber, 2, 0, 6, 2);
    }
  });

  /* U2 — free-body diagram and net force */
  window.CourseSims.register('apphy1-u2-forces', {
    title: 'Free-body diagram: what is the net force?',
    blurb:
      'Push the block and add friction. The arrows are the forces; the acceleration is set by the vector sum, not by the biggest single arrow.',
    params: [
      { k: 'F', label: 'applied force (N)', min: 0, max: 60, step: 1, val: 24, decimals: 0 },
      { k: 'mu', label: 'μ friction', min: 0, max: 0.7, step: 0.02, val: 0.25, decimals: 2 },
      { k: 'm', label: 'mass (kg)', min: 1, max: 10, step: 0.5, val: 4, decimals: 1 }
    ],
    readout(s) {
      const N = s.m * 9.8;
      const fMax = s.mu * N;
      const moving = s.F > fMax;
      const friction = moving ? fMax : s.F;
      const net = s.F - friction;
      return [
        ['normal force', fmt(N, 1) + ' N'],
        ['max static friction', fmt(fMax, 1) + ' N'],
        ['net force', fmt(net, 1) + ' N'],
        ['acceleration', fmt(net / s.m, 2) + ' m/s²']
      ];
    },
    note(s) {
      const fMax = s.mu * s.m * 9.8;
      if (s.F > fMax) return 'Once the applied force beats the maximum static friction the block slides, and kinetic friction stays fixed at μN regardless of how hard you push.';
      if (s.F > 0) return 'Not moving: the applied force is below the static limit, so friction matches it exactly and the net force is zero.';
      return 'No applied force: the normal force and weight cancel, and nothing accelerates horizontally.';
    },
    draw(ctx, s, box) {
      const N = s.m * 9.8;
      const fMax = s.mu * N;
      const moving = s.F > fMax;
      const friction = moving ? fMax : s.F;
      const net = s.F - friction;
      const groundY = box.y + box.h - 46;
      const cx = box.x + box.w * 0.42;

      ctx.strokeStyle = '#c9b9a6';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(box.x + 16, groundY);
      ctx.lineTo(box.x + box.w - 16, groundY);
      ctx.stroke();

      ctx.fillStyle = '#f3e3cf';
      ctx.strokeStyle = '#8a5a34';
      ctx.lineWidth = 2;
      ctx.fillRect(cx - 40, groundY - 60, 80, 60);
      ctx.strokeRect(cx - 40, groundY - 60, 80, 60);

      const scale = 0.9;
      arrow(ctx, cx + 40, groundY - 40, cx + 40 + s.F * scale, groundY - 40, PALETTE.blue, 3);
      label(ctx, 'F = ' + fmt(s.F, 0) + ' N', cx + 44 + s.F * scale, groundY - 46, PALETTE.blue, 10, 'left');
      arrow(ctx, cx - 40, groundY - 20, cx - 40 - friction * scale, groundY - 20, PALETTE.red, 3);
      label(ctx, 'f = ' + fmt(friction, 1), cx - 44 - friction * scale, groundY - 26, PALETTE.red, 10, 'right');
      arrow(ctx, cx, groundY, cx, groundY + 30, PALETTE.soft, 2);

      label(ctx, 'net ' + fmt(net, 1) + ' N → a = ' + fmt(net / s.m, 2) + ' m/s²', box.x + box.w / 2, box.y + 18, PALETTE.ink, 12);
      if (!moving) label(ctx, 'static: friction matches the push', box.x + box.w / 2, box.y + 40, PALETTE.soft, 10);
    }
  });

  /* U3 — energy on a ramp */
  window.CourseSims.register('apphy1-u3-energy', {
    title: 'Where does the potential energy go?',
    blurb:
      'Release a block from a height. Without friction all of the gravitational potential energy becomes kinetic at the bottom; add friction and part of it leaves as thermal energy.',
    params: [
      { k: 'h', label: 'start height (m)', min: 0.5, max: 5, step: 0.1, val: 3, decimals: 1 },
      { k: 'mu', label: 'friction μ', min: 0, max: 0.3, step: 0.01, val: 0.05, decimals: 2 },
      { k: 'm', label: 'mass (kg)', min: 1, max: 8, step: 0.5, val: 2, decimals: 1 }
    ],
    readout(s) {
      const pe = s.m * 9.8 * s.h;
      const v = Math.sqrt(Math.max(0, 2 * 9.8 * s.h * (1 - s.mu / Math.tan(Math.PI / 6))));
      const ke = 0.5 * s.m * v * v;
      return [
        ['PE at top', fmt(pe, 1) + ' J'],
        ['speed at bottom', fmt(v, 2) + ' m/s'],
        ['KE at bottom', fmt(ke, 1) + ' J'],
        ['lost to friction', fmt(pe - ke, 1) + ' J']
      ];
    },
    note(s) {
      return s.mu === 0
        ? 'Energy is conserved: every joule of PE becomes KE. The mass cancels out of the final speed.'
        : 'Friction converts mechanical energy to thermal energy, so the block arrives slower. The “lost” energy still exists — it just left the mechanical accounting.';
    },
    draw(ctx, s, box) {
      const angle = Math.PI / 6;
      const groundY = box.y + box.h - 40;
      const baseX = box.x + 70;
      const run = 200;
      const topX = baseX + run * Math.cos(angle);
      const topY = groundY - run * Math.sin(angle) * (s.h / 4);

      ctx.strokeStyle = '#b9a894';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(baseX, groundY);
      ctx.lineTo(topX, topY);
      ctx.lineTo(topX, groundY);
      ctx.stroke();

      const frac = clamp(1 - (s.h - 0.5) / 8, 0.15, 0.85);
      const bx = lerp(baseX, topX, frac);
      const by = lerp(groundY, topY, frac);
      ctx.fillStyle = '#f3e3cf';
      ctx.strokeStyle = '#8a5a34';
      ctx.lineWidth = 2;
      ctx.save();
      ctx.translate(bx, by);
      ctx.rotate(-angle);
      ctx.fillRect(-16, -26, 32, 26);
      ctx.strokeRect(-16, -26, 32, 26);
      ctx.restore();

      // energy bars
      const pe = s.m * 9.8 * s.h;
      const v = Math.sqrt(Math.max(0, 2 * 9.8 * s.h * (1 - s.mu / Math.tan(angle))));
      const ke = 0.5 * s.m * v * v;
      const x0 = box.x + box.w * 0.6;
      const barW = 34;
      const maxE = pe || 1;
      const bars = [
        ['PE', pe, PALETTE.blue],
        ['KE', ke, PALETTE.green],
        ['heat', Math.max(0, pe - ke), PALETTE.amber]
      ];
      bars.forEach(([name, val, color], i) => {
        const h = (val / maxE) * (box.h - 90);
        ctx.fillStyle = color;
        ctx.fillRect(x0 + i * 52, groundY - h, barW, h);
        label(ctx, name, x0 + i * 52 + barW / 2, groundY + 14, PALETTE.soft, 10);
      });
      label(ctx, 'h = ' + fmt(s.h, 1) + ' m', baseX + 8, groundY - 8, PALETTE.soft, 10, 'left');
    }
  });

  /* U4 — collisions in one dimension */
  window.CourseSims.register('apphy1-u4-collision', {
    title: 'Elastic or inelastic: what survives the crash?',
    blurb:
      'Momentum is conserved in every collision. Kinetic energy is conserved only when the collision is elastic — slide the elasticity and watch the kinetic energy that disappears.',
    params: [
      { k: 'm1', label: 'mass 1 (kg)', min: 1, max: 6, step: 0.5, val: 3, decimals: 1 },
      { k: 'm2', label: 'mass 2 (kg)', min: 1, max: 6, step: 0.5, val: 1, decimals: 1 },
      { k: 'v1', label: 'v₁ (m/s)', min: 1, max: 8, step: 0.5, val: 4, decimals: 1 },
      { k: 'e', label: 'elasticity e', min: 0, max: 1, step: 0.05, val: 0.4, decimals: 2 }
    ],
    readout(s) {
      const { u1, u2 } = after(s);
      const p = s.m1 * s.v1;
      const pAfter = s.m1 * u1 + s.m2 * u2;
      const ke = 0.5 * s.m1 * s.v1 * s.v1;
      const keAfter = 0.5 * s.m1 * u1 * u1 + 0.5 * s.m2 * u2 * u2;
      return [
        ['v₁′', fmt(u1, 2) + ' m/s'],
        ['v₂′', fmt(u2, 2) + ' m/s'],
        ['momentum before/after', fmt(p, 2) + ' / ' + fmt(pAfter, 2)],
        ['KE lost', fmt(ke - keAfter, 2) + ' J']
      ];
    },
    note(s) {
      return s.e === 1
        ? 'e = 1: perfectly elastic. Both momentum and kinetic energy are conserved — the masses simply exchange motion according to their inertia.'
        : 'e < 1: the bodies deform and heat up, so kinetic energy is lost while momentum is still exactly conserved. e = 0 is perfectly inelastic: they stick together.';
    },
    draw(ctx, s, box, t) {
      const { u1, u2 } = after(s);
      const cy = box.y + box.h * 0.45;
      const cycle = ((t || 0) / 2600) % 1;
      const before = cycle < 0.45;
      const p1 = before ? lerp(0.18, 0.46, cycle / 0.45) : lerp(0.46, 0.46 + u1 * 0.02, (cycle - 0.45) / 0.55);
      const p2 = before ? 0.74 : lerp(0.52, 0.52 + u2 * 0.02, (cycle - 0.45) / 0.55);
      const x1 = box.x + box.w * clamp(p1, 0.1, 0.9);
      const x2 = box.x + box.w * clamp(p2, 0.1, 0.95);

      const block = (x, m, color, name, v) => {
        const w = 26 + m * 8;
        const h = 26 + m * 8;
        ctx.fillStyle = color;
        ctx.fillRect(x - w / 2, cy - h / 2, w, h);
        label(ctx, name, x, cy + 4, '#fff', 11);
        arrow(ctx, x, cy - h / 2 - 8, x + v * 4, cy - h / 2 - 8, PALETTE.ink, 1.6);
      };
      block(x1, s.m1, 'rgba(37,99,235,0.85)', '1', before ? s.v1 : u1);
      block(x2, s.m2, 'rgba(217,119,6,0.85)', '2', before ? 0 : u2);

      label(ctx, before ? 'approaching' : 'after collision', box.x + box.w / 2, box.y + 18, PALETTE.soft, 11);
      label(ctx, 'p conserved always · KE only if e = 1', box.x + box.w / 2, box.y + box.h - 10, PALETTE.soft, 10);
    }
  });

  /* U5 — torque and static equilibrium on a beam */
  window.CourseSims.register('apphy1-u5-torque', {
    title: 'Balance the beam: torque, not force',
    blurb:
      'Torque is force times lever arm. A small mass far from the pivot can balance a large mass close to it — move the distances and watch which side wins.',
    params: [
      { k: 'm1', label: 'left mass (kg)', min: 1, max: 10, step: 0.5, val: 6, decimals: 1 },
      { k: 'd1', label: 'left distance (m)', min: 0.4, max: 2, step: 0.1, val: 1.6, decimals: 1 },
      { k: 'd2', label: 'right distance (m)', min: 0.4, max: 2, step: 0.1, val: 1.2, decimals: 1 }
    ],
    readout(s) {
      const tLeft = s.m1 * 9.8 * s.d1;
      const m2 = (s.m1 * s.d1) / s.d2;
      return [
        ['left torque', fmt(tLeft, 1) + ' N·m'],
        ['mass needed right', fmt(m2, 2) + ' kg'],
        ['torque right (that mass)', fmt(m2 * 9.8 * s.d2, 1) + ' N·m'],
        ['state', Math.abs(tLeft - m2 * 9.8 * s.d2) < 0.5 ? 'balanced' : 'not balanced']
      ];
    },
    note(s) {
      return s.d2 < s.d1
        ? 'The right side is closer to the pivot, so it needs a larger mass to produce the same torque. Lever arm matters as much as weight.'
        : 'A longer lever arm means less mass is needed. That is the whole idea behind a wrench, a crowbar and a see-saw.';
    },
    draw(ctx, s, box) {
      const m2 = (s.m1 * s.d1) / s.d2;
      const beamY = box.y + box.h * 0.5;
      const cx = box.x + box.w / 2;
      const scale = (box.w * 0.34) / 2;
      const x1 = cx - s.d1 * scale * 0.85;
      const x2 = cx + s.d2 * scale * 0.85;

      ctx.strokeStyle = '#8a5a34';
      ctx.lineWidth = 8;
      ctx.beginPath();
      ctx.moveTo(x1 - 30, beamY);
      ctx.lineTo(x2 + 30, beamY);
      ctx.stroke();

      // pivot
      ctx.fillStyle = '#c9b9a6';
      ctx.beginPath();
      ctx.moveTo(cx, beamY);
      ctx.lineTo(cx - 16, beamY + 46);
      ctx.lineTo(cx + 16, beamY + 46);
      ctx.closePath();
      ctx.fill();

      const weight = (x, m, color) => {
        const h = 24 + m * 4;
        ctx.fillStyle = color;
        ctx.fillRect(x - 14, beamY + 10, 28, h);
        label(ctx, fmt(m, 1) + ' kg', x, beamY + 24 + h, PALETTE.ink, 10);
      };
      weight(x1, s.m1, 'rgba(37,99,235,0.8)');
      weight(x2, m2, 'rgba(217,119,6,0.8)');

      arrow(ctx, x1, beamY + 6, x1, beamY + 6 + s.m1 * 9.8 * 0.5, PALETTE.blue, 2);
      arrow(ctx, x2, beamY + 6, x2, beamY + 6 + m2 * 9.8 * 0.5, PALETTE.amber, 2);

      label(ctx, 'd₁ = ' + fmt(s.d1, 1) + ' m', x1, beamY - 16, PALETTE.soft, 10);
      label(ctx, 'd₂ = ' + fmt(s.d2, 1) + ' m', x2, beamY - 16, PALETTE.soft, 10);
      label(ctx, 'pivot', cx, beamY + 62, PALETTE.soft, 10);
    }
  });

  /* U6 — angular momentum with a changing moment of inertia */
  window.CourseSims.register('apphy1-u6-spin', {
    title: 'Pull the arms in and spin faster',
    blurb:
      'With no external torque, L = Iω cannot change. Halving I doubles ω — but the kinetic energy rises, because the skater does work pulling the arms inward.',
    params: [{ k: 'I', label: 'moment of inertia I', min: 0.5, max: 4, step: 0.1, val: 3, decimals: 1 }],
    readout(s) {
      const L = 12;
      const w = L / s.I;
      const ke = 0.5 * s.I * w * w;
      return [
        ['ω', fmt(w, 2) + ' rad/s'],
        ['L = Iω', fmt(L, 1)],
        ['rotational KE', fmt(ke, 1) + ' J'],
        ['period', fmt((Math.PI * 2) / w, 2) + ' s']
      ];
    },
    note(s) {
      return s.I < 1.5
        ? 'Small I means a large ω for the same L. The extra kinetic energy came from the work the skater did pulling mass toward the axis.'
        : 'Large I gives a slow spin. Momentum L stays fixed unless a net external torque acts — friction with the ice eventually provides one.';
    },
    draw(ctx, s, box, t) {
      const L = 12;
      const w = L / s.I;
      const cx = box.x + box.w / 2;
      const cy = box.y + box.h / 2;
      const ang = ((t || 0) / 1000) * w;
      const arm = 20 + s.I * 16;

      ctx.save();
      ctx.translate(cx, cy);
      ctx.rotate(ang);
      ctx.strokeStyle = '#8a5a34';
      ctx.lineWidth = 7;
      ctx.beginPath();
      ctx.moveTo(-arm, -6);
      ctx.lineTo(arm, -6);
      ctx.moveTo(-arm * 0.5, 18);
      ctx.lineTo(arm * 0.5, 18);
      ctx.stroke();
      dot(ctx, 0, 0, 15, PALETTE.accent, '#fff');
      dot(ctx, -arm, -6, 7, PALETTE.blue);
      dot(ctx, arm, -6, 7, PALETTE.blue);
      dot(ctx, -arm * 0.5, 18, 7, PALETTE.blue);
      dot(ctx, arm * 0.5, 18, 7, PALETTE.blue);
      ctx.restore();

      label(ctx, 'ω = ' + fmt(w, 2) + ' rad/s', cx, box.y + 18, PALETTE.ink, 12);
      label(ctx, s.I < 1.5 ? 'arms in — small I' : 'arms out — large I', cx, box.y + box.h - 12, PALETTE.soft, 10);
    }
  });

  /* U7 — spring-mass SHM */
  window.CourseSims.register('apphy1-u7-shm', {
    title: 'Period depends on m and k, not on amplitude',
    blurb:
      'Change the amplitude and the period does not move. Change the mass or the spring constant and it does — T = 2π√(m/k).',
    params: [
      { k: 'm', label: 'mass (kg)', min: 0.5, max: 5, step: 0.1, val: 1, decimals: 1 },
      { k: 'k', label: 'spring k (N/m)', min: 10, max: 100, step: 5, val: 40, decimals: 0 },
      { k: 'A', label: 'amplitude (m)', min: 0.2, max: 1.5, step: 0.1, val: 1, decimals: 1 }
    ],
    readout(s) {
      const w = Math.sqrt(s.k / s.m);
      const T = (2 * Math.PI) / w;
      return [
        ['period T', fmt(T, 2) + ' s'],
        ['ω', fmt(w, 2) + ' rad/s'],
        ['v max', fmt(w * s.A, 2) + ' m/s'],
        ['total energy', fmt(0.5 * s.k * s.A * s.A, 2) + ' J']
      ];
    },
    note(s) {
      return 'Amplitude sets how far it travels, not how long a cycle takes. That independence is what makes SHM predictable.';
    },
    draw(ctx, s, box, t) {
      const w = Math.sqrt(s.k / s.m);
      const x = s.A * Math.cos(w * ((t || 0) / 1000));
      const wallX = box.x + 26;
      const cx = box.x + box.w * 0.36;
      const cy = box.y + box.h * 0.42;
      const scale = 90;
      const massX = cx + x * scale;

      ctx.strokeStyle = '#b9a894';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(wallX, cy - 50);
      ctx.lineTo(wallX, cy + 50);
      ctx.stroke();

      ctx.strokeStyle = '#8a5a34';
      ctx.lineWidth = 2;
      ctx.beginPath();
      const coils = 14;
      for (let i = 0; i <= coils; i++) {
        const px = wallX + ((massX - 22 - wallX) * i) / coils;
        const py = cy + (i === 0 || i === coils ? 0 : i % 2 === 0 ? -12 : 12);
        if (i === 0) ctx.moveTo(px, py);
        else ctx.lineTo(px, py);
      }
      ctx.stroke();

      ctx.fillStyle = '#f3e3cf';
      ctx.strokeStyle = '#8a5a34';
      ctx.lineWidth = 2;
      ctx.fillRect(massX - 20, cy - 22, 40, 44);
      ctx.strokeRect(massX - 20, cy - 22, 40, 44);

      label(ctx, 'equilibrium', cx, box.y + box.h - 14, PALETTE.soft, 10);
      ctx.save();
      ctx.setLineDash([4, 4]);
      ctx.strokeStyle = '#d8c8b6';
      ctx.beginPath();
      ctx.moveTo(cx, cy - 44);
      ctx.lineTo(cx, cy + 44);
      ctx.stroke();
      ctx.restore();

      // x(t) trace on the right
      const p = plot(ctx, { x: box.x + box.w * 0.52, y: box.y + 14, w: box.w * 0.45, h: box.h - 34 }, { xmin: 0, xmax: 6, ymin: -1.8, ymax: 1.8, ticks: 2, xdigits: 0, ydigits: 0, xlabel: 't' });
      curve(ctx, p, (tt) => s.A * Math.cos(w * tt), PALETTE.blue, 2, 0, 6, 200);
    }
  });

  /* U8 — pressure with depth and buoyancy */
  window.CourseSims.register('apphy1-u8-fluids', {
    title: 'Pressure with depth, and what floats',
    blurb:
      'Gauge pressure grows with depth and density. A block floats when it is less dense than the fluid, and the fraction submerged is exactly the density ratio.',
    params: [
      { k: 'rho', label: 'fluid density (kg/m³)', min: 700, max: 1400, step: 10, val: 1000, decimals: 0 },
      { k: 'rhoObj', label: 'object density (kg/m³)', min: 200, max: 1300, step: 10, val: 600, decimals: 0 },
      { k: 'depth', label: 'gauge depth (m)', min: 0, max: 10, step: 0.1, val: 3, decimals: 1 }
    ],
    readout(s) {
      const p = s.rho * 9.8 * s.depth;
      const frac = clamp(s.rhoObj / s.rho, 0, 1);
      return [
        ['gauge pressure', fmt(p / 1000, 1) + ' kPa'],
        ['absolute pressure', fmt((p + 101325) / 1000, 1) + ' kPa'],
        ['submerged fraction', fmt(frac * 100, 0) + '%'],
        ['floats?', frac < 1 ? 'yes' : 'sinks']
      ];
    },
    note(s) {
      return s.rhoObj < s.rho
        ? 'The block displaces its own weight in fluid, not its own volume. That is why the submerged fraction equals ρ_object / ρ_fluid.'
        : 'Denser than the fluid: the buoyant force can never match the weight, so it sinks no matter how deep it starts.';
    },
    draw(ctx, s, box) {
      const tankX = box.x + 30;
      const tankY = box.y + 20;
      const tankW = box.w * 0.5;
      const tankH = box.h - 40;
      ctx.fillStyle = 'rgba(37,99,235,0.16)';
      ctx.fillRect(tankX, tankY, tankW, tankH);
      ctx.strokeStyle = '#93c5fd';
      ctx.lineWidth = 2;
      ctx.strokeRect(tankX, tankY, tankW, tankH);

      const frac = clamp(s.rhoObj / s.rho, 0, 1);
      const blockH = 56;
      const blockW = 70;
      const surfaceY = tankY + 6;
      const by = frac < 1 ? surfaceY + frac * blockH - blockH : tankY + tankH - blockH - 10;
      ctx.fillStyle = '#f3e3cf';
      ctx.strokeStyle = '#8a5a34';
      ctx.fillRect(tankX + tankW / 2 - blockW / 2, by, blockW, blockH);
      ctx.strokeRect(tankX + tankW / 2 - blockW / 2, by, blockW, blockH);
      label(ctx, fmt(frac * 100, 0) + '% under', tankX + tankW / 2, by - 8, PALETTE.ink, 10);
      label(ctx, 'ρ = ' + fmt(s.rho, 0), tankX + 8, tankY + tankH - 8, '#1d4ed8', 10, 'left');

      // depth gauge
      const gx = box.x + box.w * 0.72;
      const gy = tankY + 10;
      const gh = tankH - 20;
      ctx.strokeStyle = '#c9b9a6';
      ctx.beginPath();
      ctx.moveTo(gx, gy);
      ctx.lineTo(gx, gy + gh);
      ctx.stroke();
      const dy = gy + (s.depth / 10) * gh;
      dot(ctx, gx, dy, 5, PALETTE.accent);
      label(ctx, fmt(s.depth, 1) + ' m', gx + 12, dy + 4, PALETTE.accent, 10, 'left');
      label(ctx, fmt((s.rho * 9.8 * s.depth) / 1000, 1) + ' kPa', gx + 12, dy + 22, PALETTE.soft, 10, 'left');
    }
  });

  /* ---- helpers ---- */

  function after(s) {
    const e = s.e;
    const u1 = ((s.m1 - e * s.m2) * s.v1) / (s.m1 + s.m2);
    const u2 = ((s.m1 * (1 + e)) * s.v1) / (s.m1 + s.m2);
    return { u1, u2 };
  }
})();
