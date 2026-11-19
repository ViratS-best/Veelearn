/* ============================================================================
 * AP Physics C: Electricity & Magnetism — one simulation per unit.
 * ========================================================================== */
(function () {
  'use strict';
  const S = window.CourseSims && window.CourseSims.util;
  if (!S) return;
  const { plot, curve, arrow, dot, label, fmt, clamp, lerp, PALETTE } = S;

  const K = 8.99e9;
  const EPS0 = 8.854e-12;

  /* U1 — Coulomb's law and superposition */
  window.CourseSims.register('apphyscem-u1-coulomb', {
    title: 'Two charges, one force law',
    blurb:
      'The force grows with both charges and falls with the square of the distance. Flip a sign and the arrow reverses but its length does not change.',
    params: [
      { k: 'q1', label: 'q₁ (µC)', min: -10, max: 10, step: 0.5, val: 4, decimals: 1 },
      { k: 'q2', label: 'q₂ (µC)', min: -10, max: 10, step: 0.5, val: -3, decimals: 1 },
      { k: 'r', label: 'separation (m)', min: 0.1, max: 1, step: 0.02, val: 0.4, decimals: 2 }
    ],
    readout(s) {
      const q1 = s.q1 * 1e-6;
      const q2 = s.q2 * 1e-6;
      const F = (K * Math.abs(q1 * q2)) / (s.r * s.r);
      return [
        ['force', fmt(F, 3) + ' N'],
        ['direction', q1 * q2 < 0 ? 'attractive' : 'repulsive'],
        ['E from q₁ at q₂', fmt((K * Math.abs(q1)) / (s.r * s.r) / 1000, 1) + ' kN/C'],
        ['doubling r', 'quarters the force']
      ];
    },
    note(s) {
      return s.q1 * s.q2 === 0
        ? 'One charge is zero, so there is no force at all — the field from a zero charge is zero everywhere.'
        : 'The force is mutual: each charge feels the same magnitude, opposite direction. The field E = kq/r² is what one charge creates for the other to feel.';
    },
    draw(ctx, s, box) {
      const cy = box.y + box.h * 0.5;
      const cx = box.x + box.w / 2;
      const half = (s.r / 1) * (box.w * 0.32) + 40;
      const x1 = cx - half;
      const x2 = cx + half;

      const charge = (x, q, name) => {
        const pos = q >= 0;
        dot(ctx, x, cy, 22, pos ? 'rgba(220,38,38,0.85)' : 'rgba(37,99,235,0.85)', '#fff');
        label(ctx, pos ? '+' : '−', x, cy + 7, '#fff', 18);
        label(ctx, name, x, cy + 44, PALETTE.soft, 11);
      };
      charge(x1, s.q1, 'q₁ = ' + fmt(s.q1, 1) + ' µC');
      charge(x2, s.q2, 'q₂ = ' + fmt(s.q2, 1) + ' µC');

      const q1 = s.q1 * 1e-6;
      const q2 = s.q2 * 1e-6;
      const F = (K * Math.abs(q1 * q2)) / (s.r * s.r);
      const len = clamp(Math.log10(F + 1) * 26, 12, 110);
      const attract = q1 * q2 < 0;
      arrow(ctx, x1 + 24, cy - 34, x1 + 24 + (attract ? len : -len), cy - 34, PALETTE.accent, 2.4);
      arrow(ctx, x2 - 24, cy + 34, x2 - 24 + (attract ? -len : len), cy + 34, PALETTE.accent, 2.4);
      label(ctx, 'F = ' + fmt(F, 3) + ' N', cx, box.y + 18, PALETTE.ink, 12);
      label(ctx, 'r = ' + fmt(s.r, 2) + ' m', cx, cy + 74, PALETTE.soft, 10);
    }
  });

  /* U2 — Gauss's law: flux depends on enclosed charge only */
  window.CourseSims.register('apphyscem-u2-gauss', {
    title: 'Flux does not care how big the surface is',
    blurb:
      'Grow the Gaussian sphere around a charge. The surface area grows as r², the field falls as 1/r², and the product — the flux — stays fixed at Q/ε₀.',
    params: [
      { k: 'Q', label: 'enclosed charge (nC)', min: -10, max: 10, step: 0.5, val: 4, decimals: 1 },
      { k: 'r', label: 'Gaussian radius (m)', min: 0.2, max: 2, step: 0.05, val: 0.8, decimals: 2 }
    ],
    readout(s) {
      const Q = s.Q * 1e-9;
      return [
        ['enclosed charge', fmt(s.Q, 1) + ' nC'],
        ['flux Φ = Q/ε₀', fmt(Q / EPS0, 1) + ' N·m²/C'],
        ['E at the surface', fmt((K * Math.abs(Q)) / (s.r * s.r) / 1000, 2) + ' kN/C'],
        ['surface area', fmt(4 * Math.PI * s.r * s.r, 2) + ' m²']
      ];
    },
    note(s) {
      return 'Change r and watch: E changes, area changes, but their product does not. That is Gauss’s law — flux counts field lines crossing the surface, and every line from the charge crosses exactly once.';
    },
    draw(ctx, s, box) {
      const cx = box.x + box.w * 0.42;
      const cy = box.y + box.h / 2;
      const R = clamp(s.r * 90, 26, Math.min(box.w, box.h) * 0.42);

      ctx.strokeStyle = s.Q >= 0 ? 'rgba(220,38,38,0.5)' : 'rgba(37,99,235,0.5)';
      ctx.lineWidth = 2;
      ctx.setLineDash([5, 4]);
      ctx.beginPath();
      ctx.arc(cx, cy, R, 0, Math.PI * 2);
      ctx.stroke();
      ctx.setLineDash([]);

      for (let i = 0; i < 24; i++) {
        const a = (i / 24) * Math.PI * 2;
        const x1 = cx + Math.cos(a) * 12;
        const y1 = cy + Math.sin(a) * 12;
        const x2 = cx + Math.cos(a) * R;
        const y2 = cy + Math.sin(a) * R;
        arrow(ctx, x1, y1, x2, y2, s.Q >= 0 ? 'rgba(220,38,38,0.55)' : 'rgba(37,99,235,0.55)', 1.2);
      }
      dot(ctx, cx, cy, 10, s.Q >= 0 ? '#dc2626' : '#2563eb', '#fff');
      label(ctx, s.Q >= 0 ? '+' : '−', cx, cy + 5, '#fff', 12);

      const p = plot(ctx, { x: box.x + box.w * 0.62, y: box.y + 10, w: box.w * 0.35, h: box.h - 24 }, { xmin: 0.2, xmax: 2, ymin: 0, ymax: 1.2, ticks: 2, xdigits: 1, ydigits: 1, xlabel: 'r' });
      curve(ctx, p, (r) => 1 / (r * r), PALETTE.blue, 2, 0.2, 2, 160);
      dot(ctx, p.X(s.r), p.clampY === undefined ? p.Y(clamp(1 / (s.r * s.r), 0, 1.2)) : p.Y(clamp(1 / (s.r * s.r), 0, 1.2)), 3.6, PALETTE.accent);
      label(ctx, 'E ∝ 1/r²', p.x0 + 6, p.y0 + 14, PALETTE.blue, 9, 'left');
    }
  });

  /* U3 — parallel-plate capacitor */
  window.CourseSims.register('apphyscem-u3-capacitor', {
    title: 'Packing charge onto a capacitor',
    blurb:
      'Bigger plates hold more charge; moving them apart weakens the field for the same voltage and lowers the capacitance. The energy stored is ½CV².',
    params: [
      { k: 'A', label: 'plate area (cm²)', min: 10, max: 200, step: 5, val: 100, decimals: 0 },
      { k: 'd', label: 'separation (mm)', min: 1, max: 10, step: 0.5, val: 2, decimals: 1 },
      { k: 'V', label: 'voltage (V)', min: 1, max: 20, step: 0.5, val: 9, decimals: 1 }
    ],
    readout(s) {
      const A = s.A * 1e-4;
      const d = s.d * 1e-3;
      const C = (EPS0 * A) / d;
      return [
        ['capacitance', fmt(C * 1e12, 2) + ' pF'],
        ['charge Q = CV', fmt(C * s.V * 1e9, 2) + ' nC'],
        ['field E = V/d', fmt(s.V / d / 1000, 2) + ' kV/m'],
        ['energy ½CV²', fmt(0.5 * C * s.V * s.V * 1e9, 3) + ' nJ']
      ];
    },
    note(s) {
      return 'Separating the plates at fixed voltage reduces C, so less charge sits on them. If the capacitor were isolated instead, separating the plates would raise the voltage because Q is stuck.'
    },
    draw(ctx, s, box) {
      const gap = clamp(s.d * 16, 20, 110);
      const plateH = clamp(40 + s.A * 0.7, 50, box.h - 60);
      const cx = box.x + box.w * 0.42;
      const cy = box.y + box.h / 2;

      ctx.fillStyle = '#cbd5e1';
      ctx.fillRect(cx - gap / 2 - 7, cy - plateH / 2, 7, plateH);
      ctx.fillRect(cx + gap / 2, cy - plateH / 2, 7, plateH);

      // field lines run from the positive plate to the negative plate
      for (let i = 1; i < 6; i++) {
        const y = cy - plateH / 2 + (plateH * i) / 6;
        arrow(ctx, cx - gap / 2 + 4, y, cx + gap / 2 - 4, y, 'rgba(37,99,235,0.55)', 1);
      }

      label(ctx, '+', cx - gap / 2 - 20, cy, PALETTE.red, 18);
      label(ctx, '−', cx + gap / 2 + 20, cy, PALETTE.blue, 18);
      label(ctx, 'E', cx, cy - plateH / 2 - 12, PALETTE.blue, 11);
      label(ctx, 'd = ' + fmt(s.d, 1) + ' mm', cx, cy + plateH / 2 + 22, PALETTE.soft, 10);
      label(ctx, 'C = ' + fmt((EPS0 * s.A * 1e-4) / (s.d * 1e-3) * 1e12, 1) + ' pF', box.x + box.w * 0.78, cy, PALETTE.ink, 12);
    }
  });

  /* U4 — series and parallel circuits */
  window.CourseSims.register('apphyscem-u4-circuit', {
    title: 'Same battery, two very different currents',
    blurb:
      'Swap between series and parallel. Series adds resistances and shares one current; parallel adds conductances, splits the current, and draws more from the battery.',
    params: [
      { k: 'emf', label: 'battery (V)', min: 3, max: 24, step: 1, val: 12, decimals: 0 },
      { k: 'R1', label: 'R₁ (Ω)', min: 1, max: 20, step: 1, val: 6, decimals: 0 },
      { k: 'R2', label: 'R₂ (Ω)', min: 1, max: 20, step: 1, val: 6, decimals: 0 },
      {
        k: 'mode',
        label: 'connection',
        type: 'select',
        val: 'series',
        options: [
          { v: 'series', label: 'series' },
          { v: 'parallel', label: 'parallel' }
        ]
      }
    ],
    readout(s) {
      const series = s.mode === 'series';
      const Req = series ? s.R1 + s.R2 : (s.R1 * s.R2) / (s.R1 + s.R2);
      const I = s.emf / Req;
      return [
        ['R equivalent', fmt(Req, 2) + ' Ω'],
        ['total current', fmt(I, 2) + ' A'],
        [series ? 'current in each' : 'branch currents', series ? fmt(I, 2) + ' A' : fmt(s.emf / s.R1, 2) + ' / ' + fmt(s.emf / s.R2, 2) + ' A'],
        ['power from battery', fmt(s.emf * I, 1) + ' W']
      ];
    },
    note(s) {
      return s.mode === 'parallel'
        ? 'Each branch sees the full battery voltage, so each draws its own current. The battery supplies the sum — which is why parallel loads drain faster.'
        : 'The same current passes through both resistors, so the voltage divides in proportion to resistance. Total R is larger than either one.';
    },
    draw(ctx, s, box) {
      const series = s.mode === 'series';
      const x0 = box.x + box.w * 0.18;
      const y0 = box.y + box.h * 0.3;
      const w = box.w * 0.5;
      const h = box.h * 0.34;

      ctx.strokeStyle = '#475569';
      ctx.lineWidth = 2.4;
      ctx.beginPath();
      ctx.rect(x0, y0, w, h);
      ctx.stroke();

      // battery on the left edge
      ctx.strokeStyle = '#111827';
      ctx.lineWidth = 4;
      ctx.beginPath();
      ctx.moveTo(x0 - 8, y0 + h / 2 - 14);
      ctx.lineTo(x0 + 8, y0 + h / 2 - 14);
      ctx.moveTo(x0 - 5, y0 + h / 2 + 14);
      ctx.lineTo(x0 + 5, y0 + h / 2 + 14);
      ctx.stroke();
      label(ctx, fmt(s.emf, 0) + ' V', x0 - 18, y0 + h / 2, PALETTE.ink, 11, 'right');

      const resistor = (x, y, name, value, vertical) => {
        ctx.save();
        ctx.strokeStyle = PALETTE.blue;
        ctx.fillStyle = '#fffdf9';
        ctx.lineWidth = 2;
        if (vertical) {
          ctx.fillRect(x - 10, y - 20, 20, 40);
          ctx.strokeRect(x - 10, y - 20, 20, 40);
        } else {
          ctx.fillRect(x - 20, y - 10, 40, 20);
          ctx.strokeRect(x - 20, y - 10, 40, 20);
        }
        ctx.restore();
        label(ctx, name + ' = ' + value + ' Ω', vertical ? x + 18 : x, vertical ? y : y - 16, PALETTE.blue, 10, vertical ? 'left' : 'center');
      };

      if (series) {
        resistor(x0 + w * 0.35, y0, 'R₁', s.R1, false);
        resistor(x0 + w * 0.7, y0, 'R₂', s.R2, false);
        label(ctx, 'one path — same current', box.x + box.w * 0.5, box.y + box.h - 16, PALETTE.soft, 10);
      } else {
        ctx.beginPath();
        ctx.moveTo(x0 + w * 0.5, y0);
        ctx.lineTo(x0 + w * 0.5, y0 + h * 0.35);
        ctx.moveTo(x0 + w * 0.5, y0 + h * 0.65);
        ctx.lineTo(x0 + w * 0.5, y0 + h);
        ctx.stroke();
        resistor(x0 + w * 0.5, y0 + h * 0.5, 'R₁', s.R1, true);
        resistor(x0 + w * 0.82, y0 + h * 0.5, 'R₂', s.R2, true);
        ctx.beginPath();
        ctx.moveTo(x0 + w * 0.5, y0 + h * 0.5);
        ctx.lineTo(x0 + w * 0.82, y0 + h * 0.5);
        ctx.stroke();
        label(ctx, 'two branches — same voltage', box.x + box.w * 0.5, box.y + box.h - 16, PALETTE.soft, 10);
      }

      const Req = series ? s.R1 + s.R2 : (s.R1 * s.R2) / (s.R1 + s.R2);
      label(ctx, 'I = ' + fmt(s.emf / Req, 2) + ' A', box.x + box.w * 0.78, box.y + 18, PALETTE.accent, 11, 'left');
    }
  });

  /* U5 — RC charging and discharging */
  window.CourseSims.register('apphyscem-u5-rc', {
    title: 'RC circuits: the time constant sets the clock',
    blurb:
      'Charging follows V(1 − e^(−t/τ)) and discharging follows V e^(−t/τ), with τ = RC. Stack more resistance or capacitance and everything slows down by exactly that factor.',
    params: [
      { k: 'R', label: 'R (kΩ)', min: 1, max: 100, step: 1, val: 20, decimals: 0 },
      { k: 'C', label: 'C (µF)', min: 1, max: 200, step: 1, val: 50, decimals: 0 },
      {
        k: 'mode',
        label: 'process',
        type: 'select',
        val: 'charge',
        options: [
          { v: 'charge', label: 'charging' },
          { v: 'discharge', label: 'discharging' }
        ]
      }
    ],
    readout(s) {
      const tau = s.R * 1e3 * s.C * 1e-6;
      const V = s.mode === 'charge' ? 10 * (1 - Math.exp(-1)) : 10 * Math.exp(-1);
      return [
        ['time constant τ = RC', fmt(tau, 3) + ' s'],
        ['V at t = τ', fmt(V, 2) + ' V'],
        ['V after 5τ', s.mode === 'charge' ? '99.3% charged' : '0.7% left'],
        ['I at t = 0', fmt(10 / (s.R * 1e3) * 1000, 3) + ' mA']
      ];
    },
    note(s) {
      return s.mode === 'charge'
        ? 'The capacitor fills quickly at first, when it is empty, then slows as its own voltage opposes the battery. It never reaches the battery voltage exactly.'
        : 'Discharging is the same exponential run backwards. After one time constant 37% of the voltage remains, regardless of the starting value.';
    },
    draw(ctx, s, box) {
      const tau = s.R * 1e3 * s.C * 1e-6;
      const T = Math.max(1, tau * 5);
      const p = plot(ctx, box, { xmin: 0, xmax: T, ymin: 0, ymax: 10.5, ticks: 4, xdigits: 0, ydigits: 0, xlabel: 'time (s)', ylabel: 'V_C' });
      const f = (t) => (s.mode === 'charge' ? 10 * (1 - Math.exp(-t / tau)) : 10 * Math.exp(-t / tau));
      curve(ctx, p, f, PALETTE.blue, 2.6, 0, T, 240);

      ctx.save();
      ctx.setLineDash([4, 4]);
      ctx.strokeStyle = PALETTE.soft;
      ctx.beginPath();
      ctx.moveTo(p.X(tau), p.y0);
      ctx.lineTo(p.X(tau), p.y0 + p.h);
      ctx.stroke();
      ctx.restore();
      label(ctx, 'τ', p.X(tau), p.y0 + p.h + 16, PALETTE.accent, 11);
      dot(ctx, p.X(tau), p.Y(f(tau)), 4, PALETTE.accent);
      label(ctx, fmt(f(tau), 1) + ' V', p.X(tau) + 6, p.Y(f(tau)) - 8, PALETTE.accent, 10, 'left');
      label(ctx, s.mode === 'charge' ? 'charging' : 'discharging', p.x0 + 10, p.y0 + 16, PALETTE.soft, 11, 'left');
      label(ctx, 'τ = ' + fmt(tau, 2) + ' s', p.x0 + p.w - 8, p.y0 + 16, PALETTE.ink, 11, 'right');
    }
  });

  /* U6 — magnetic force on a moving charge */
  window.CourseSims.register('apphyscem-u6-magnetic', {
    title: 'Magnetic force bends paths into circles',
    blurb:
      'The force is qvB sin θ and always perpendicular to velocity, so it does no work — it only turns the particle. At θ = 90° the path is a circle whose radius is mv/(qB).',
    params: [
      { k: 'v', label: 'speed (10⁶ m/s)', min: 1, max: 10, step: 0.5, val: 4, decimals: 1 },
      { k: 'B', label: 'field B (T)', min: 0.1, max: 2, step: 0.05, val: 0.6, decimals: 2 },
      { k: 'angle', label: 'angle v–B (°)', min: 0, max: 90, step: 5, val: 90, decimals: 0 }
    ],
    readout(s) {
      const q = 1.6e-19;
      const m = 9.11e-31;
      const th = (s.angle * Math.PI) / 180;
      const F = q * s.v * 1e6 * s.B * Math.sin(th);
      const r = (m * s.v * 1e6) / (q * s.B);
      return [
        ['force F = qvB sinθ', fmt(F * 1e15, 2) + ' fN'],
        ['radius mv/qB', fmt(r * 1000, 2) + ' mm'],
        ['period', fmt((2 * Math.PI * m) / (q * s.B) * 1e9, 2) + ' ns'],
        ['work done', 'zero — F ⊥ v']
      ];
    },
    note(s) {
      return s.angle < 15
        ? 'Almost parallel: sin θ ≈ 0, so the magnetic force nearly vanishes even though the particle is fast and the field is strong.'
        : 'The field changes the direction but never the speed. Magnetic forces steer; electric fields can also speed things up.';
    },
    draw(ctx, s, box, t) {
      const th = (s.angle * Math.PI) / 180;
      const cx = box.x + box.w * 0.45;
      const cy = box.y + box.h / 2;
      const rPx = clamp(((9.11e-31 * s.v * 1e6) / (1.6e-19 * s.B)) * 1000, 24, 110);
      const spiral = Math.sin(th);

      for (let i = 0; i < 9; i++) {
        const x = box.x + 30 + i * (box.w - 60) / 8;
        for (let j = 0; j < 5; j++) {
          const y = box.y + 24 + j * (box.h - 48) / 4;
          dot(ctx, x, y, 1.6, 'rgba(37,99,235,0.45)');
        }
      }
      label(ctx, 'B out of the page', box.x + box.w - 12, box.y + 14, PALETTE.blue, 10, 'right');

      ctx.strokeStyle = 'rgba(220,38,38,0.6)';
      ctx.lineWidth = 1.6;
      ctx.beginPath();
      if (Math.abs(spiral) > 0.95) {
        ctx.arc(cx, cy, rPx, 0, Math.PI * 2);
      } else {
        for (let i = 0; i <= 200; i++) {
          const a = (i / 200) * Math.PI * 6;
          const shrink = 1 - (i / 200) * (1 - spiral) * 0.8;
          const x = cx + Math.cos(a) * rPx * shrink;
          const y = cy + Math.sin(a) * rPx * shrink * 0.6;
          if (i === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
      }
      ctx.stroke();

      const ang = ((t || 0) / 900) % (Math.PI * 2);
      const px = cx + Math.cos(ang) * rPx;
      const py = cy + Math.sin(ang) * rPx;
      dot(ctx, px, py, 6, PALETTE.accent, '#fff');
      arrow(ctx, px, py, px + Math.cos(ang + Math.PI / 2) * 34, py + Math.sin(ang + Math.PI / 2) * 34, PALETTE.red, 2);
      label(ctx, 'F', px + Math.cos(ang + Math.PI / 2) * 44, py + Math.sin(ang + Math.PI / 2) * 44, PALETTE.red, 10);
      arrow(ctx, px, py, px + Math.cos(ang) * 30, py + Math.sin(ang) * 30, PALETTE.ink, 1.6);
      label(ctx, 'v', px + Math.cos(ang) * 40, py + Math.sin(ang) * 40, PALETTE.ink, 10);
    }
  });

  /* U7 — Faraday, Lenz and motional emf */
  window.CourseSims.register('apphyscem-u7-induction', {
    title: 'Move the magnet and the coil pushes back',
    blurb:
      'An emf appears only while the flux is changing — motion, not the field itself. Lenz’s law says the induced current opposes the change, which is why the coil feels like a brake.',
    params: [
      { k: 'B', label: 'field B (T)', min: 0, max: 2, step: 0.05, val: 0.8, decimals: 2 },
      { k: 'v', label: 'speed (m/s)', min: 0.5, max: 5, step: 0.1, val: 2, decimals: 1 },
      { k: 'N', label: 'turns N', min: 1, max: 50, step: 1, val: 20, decimals: 0 }
    ],
    readout(s) {
      const L = 0.3;
      const emf = s.N * s.B * L * s.v;
      return [
        ['emf', fmt(emf, 2) + ' V'],
        ['flux per turn', fmt(s.B * 0.06, 3) + ' Wb'],
        ['rate of change', fmt(s.B * L * s.v, 3) + ' Wb/s'],
        ['current direction', s.B > 0 ? 'opposes the increase' : 'no field']
      ];
    },
    note(s) {
      return s.B === 0
        ? 'No field means no flux and no induced emf, no matter how fast the coil moves.'
        : 'Hold the magnet still and the emf disappears, even with a strong field. Faraday’s law responds to dΦ/dt, not Φ.';
    },
    draw(ctx, s, box) {
      const cx = box.x + box.w * 0.6;
      const cy = box.y + box.h / 2;
      const coilW = 34;
      const coilH = 90;

      for (let i = 0; i < 7; i++) {
        ctx.strokeStyle = s.B > 0 ? 'rgba(37,99,235,0.75)' : 'rgba(120,113,108,0.35)';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.ellipse(cx, cy, coilW * (0.55 + i * 0.06), coilH / 2, 0, 0, Math.PI * 2);
        ctx.stroke();
      }

      const vScale = (box.w * 0.28) / 5;
      const magX = cx - 70 - s.v * 10;
      ctx.fillStyle = '#dc2626';
      ctx.fillRect(magX - 26, cy - 16, 26, 32);
      ctx.fillStyle = '#2563eb';
      ctx.fillRect(magX, cy - 16, 26, 32);
      label(ctx, 'N', magX - 13, cy + 4, '#fff', 11);
      label(ctx, 'S', magX + 13, cy + 4, '#fff', 11);

      arrow(ctx, magX + 40, cy - 34, magX + 40 + s.v * 14, cy - 34, PALETTE.green, 2);
      label(ctx, 'v = ' + fmt(s.v, 1) + ' m/s', magX + 40, cy - 44, PALETTE.green, 10, 'left');

      label(ctx, 'ε = NBLv = ' + fmt(s.N * s.B * 0.3 * s.v, 1) + ' V', box.x + box.w / 2, box.y + box.h - 14, PALETTE.accent, 12);
      label(ctx, 'induced current opposes the change', box.x + box.w / 2, box.y + 18, PALETTE.soft, 10);
    }
  });

  /* U8 — LC oscillation and energy exchange */
  window.CourseSims.register('apphyscem-u8-lc', {
    title: 'LC circuit: energy sloshes between C and L',
    blurb:
      'Charge the capacitor and let go. The charge oscillates at f = 1/(2π√(LC)); the energy moves completely from the capacitor’s field to the inductor’s and back, with the total fixed.',
    params: [
      { k: 'L', label: 'inductance (mH)', min: 1, max: 100, step: 1, val: 40, decimals: 0 },
      { k: 'C', label: 'capacitance (µF)', min: 1, max: 100, step: 1, val: 20, decimals: 0 }
    ],
    readout(s) {
      const L = s.L * 1e-3;
      const C = s.C * 1e-6;
      const f = 1 / (2 * Math.PI * Math.sqrt(L * C));
      return [
        ['frequency', fmt(f, 1) + ' Hz'],
        ['period', fmt(1000 / f, 3) + ' ms'],
        ['angular frequency ω', fmt(2 * Math.PI * f, 1) + ' rad/s'],
        ['energy', 'constant (ideal)']
      ];
    },
    note(s) {
      return 'At the moment the capacitor is fully charged, all the energy is electric. A quarter period later the capacitor is empty and the current is maximal, so all the energy is magnetic. The total never changes in an ideal LC circuit.';
    },
    draw(ctx, s, box, t) {
      const L = s.L * 1e-3;
      const C = s.C * 1e-6;
      const w = 1 / Math.sqrt(L * C);
      const phase = (t || 0) / 1000;
      const q = Math.cos(w * phase);
      const i = -Math.sin(w * phase);

      const p = plot(ctx, { x: box.x, y: box.y + 6, w: box.w, h: box.h * 0.55 }, { xmin: 0, xmax: 0.02, ymin: -1.2, ymax: 1.2, ticks: 2, xdigits: 0, ydigits: 0, xlabel: 'time (s)' });
      curve(ctx, p, (tt) => Math.cos(w * tt), PALETTE.blue, 2, 0, 0.02, 200);
      curve(ctx, p, (tt) => -Math.sin(w * tt), PALETTE.amber, 2, 0, 0.02, 200);
      label(ctx, 'q', p.x0 + 8, p.y0 + 14, PALETTE.blue, 10, 'left');
      label(ctx, 'i', p.x0 + 24, p.y0 + 14, PALETTE.amber, 10, 'left');

      // energy bars
      const baseY = box.y + box.h - 18;
      const hMax = box.h * 0.24;
      const cx = box.x + box.w / 2;
      [['E_C = ½q²/C', q * q, PALETTE.blue, cx - 60], ['E_L = ½Li²', i * i, PALETTE.amber, cx + 60]].forEach(([name, val, color, x]) => {
        const bh = Math.max(2, val * hMax);
        ctx.fillStyle = color;
        ctx.fillRect(x - 22, baseY - bh, 44, bh);
        label(ctx, name, x, baseY + 10, PALETTE.soft, 9);
      });
      label(ctx, 'total constant', cx, box.y + box.h - 4, PALETTE.soft, 9);
    }
  });
})();
