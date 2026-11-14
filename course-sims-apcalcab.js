/* ============================================================================
 * AP Calculus AB — one purpose-built simulation per unit.
 *
 * Each spec is written for the specific sections of that unit (limits & tables,
 * difference quotients, related rates, concavity, Riemann sums + FTC, disks,
 * slope fields, and a capstone that ties derivatives to integrals). Nothing
 * here is a generic "math playground": the parameters, readouts and coaching
 * line answer the question that unit actually asks.
 * ========================================================================== */
(function () {
  'use strict';

  const S = window.CourseSims && window.CourseSims.util;
  if (!S) return;
  const { plot, curve, arrow, dot, label, fmt, clamp, lerp, PALETTE } = S;

  const MONO = '11px ui-monospace, SFMono-Regular, Menlo, monospace';
  const SERIF = '12px ui-sans-serif, system-ui, sans-serif';

  function miniPlot(ctx, box, opts) {
    return plot(ctx, box, Object.assign({ ticks: 2, xdigits: 1, ydigits: 1, pad: { l: 30, r: 6, t: 6, b: 16 } }, opts));
  }

  /* ------------------------------------------------------------------ Unit 1
   * "Limit from a graph and table", one-sided limits, infinite limits.
   * The student walks x toward a and watches the table converge from each side.
   */
  const U1_FAMILIES = {
    hole: {
      label: 'Removable hole: (x²−1)/(x−1) at x = 1',
      a: 1,
      f: (x) => (Math.abs(x - 1) < 1e-9 ? NaN : (x * x - 1) / (x - 1)),
      left: 2,
      right: 2,
      verdict: 'The limit exists even though f(1) does not.',
      ymin: -1,
      ymax: 4
    },
    jump: {
      label: 'Jump: piecewise at x = 1',
      a: 1,
      f: (x) => (x < 1 ? 1 : 3),
      left: 1,
      right: 3,
      verdict: 'One-sided limits differ, so the two-sided limit does not exist.',
      ymin: -1,
      ymax: 4
    },
    asymptote: {
      label: 'Vertical asymptote: 1/(x−1)',
      a: 1,
      f: (x) => 1 / (x - 1),
      left: -Infinity,
      right: Infinity,
      verdict: 'The function is unbounded; the limit is not a number.',
      ymin: -5,
      ymax: 5
    },
    continuous: {
      label: 'Continuous: x² near x = 1',
      a: 1,
      f: (x) => x * x,
      left: 1,
      right: 1,
      verdict: 'Limit, function value and both one-sided limits all agree.',
      ymin: -1,
      ymax: 4
    }
  };

  window.CourseSims.register('apcalcab-u1-limits', {
    title: 'Walk x toward the point and watch the table',
    blurb:
      'Pick a function, then slide x toward a. The two columns are the values on the left and on the right — a limit is what those columns agree on, not what the graph does at the point.',
    params: [
      {
        k: 'kind',
        label: 'Function',
        type: 'select',
        val: 'hole',
        options: [
          { v: 'hole', label: 'Removable hole' },
          { v: 'jump', label: 'Jump' },
          { v: 'asymptote', label: 'Vertical asymptote' },
          { v: 'continuous', label: 'Continuous' }
        ]
      },
      { k: 'x', label: 'x', min: -2, max: 3, step: 0.02, val: 0.4, decimals: 2 }
    ],
    readout(s) {
      const fam = U1_FAMILIES[s.kind];
      const f = fam.f(s.x);
      const lim = fam.left === fam.right ? fmt(fam.left, 2) : 'does not exist';
      return [
        ['left limit', fam.left === -Infinity ? '−∞' : fam.left === Infinity ? '+∞' : fmt(fam.left, 2)],
        ['right limit', fam.right === -Infinity ? '−∞' : fam.right === Infinity ? '+∞' : fmt(fam.right, 2)],
        ['limit at a', lim],
        ['f(x) now', Number.isFinite(f) ? fmt(f, 3) : 'undefined']
      ];
    },
    note(s) {
      return U1_FAMILIES[s.kind].verdict;
    },
    draw(ctx, s, box) {
      const fam = U1_FAMILIES[s.kind];
      const plotW = box.w * 0.6;
      const p = plot(ctx, { x: box.x, y: box.y, w: plotW, h: box.h }, {
        xmin: -2,
        xmax: 3,
        ymin: fam.ymin,
        ymax: fam.ymax,
        xlabel: 'x',
        ticks: 5
      });

      curve(ctx, p, fam.f, PALETTE.blue, 2.2, -2, 3, 400);

      // the hole / jump / asymptote at x = a
      const ax = p.X(fam.a);
      if (s.kind === 'hole') {
        dot(ctx, ax, p.Y(fam.left), 4.5, '#fff', PALETTE.blue);
      } else if (s.kind === 'jump') {
        dot(ctx, ax, p.Y(fam.left), 4, '#fff', PALETTE.blue);
        dot(ctx, ax, p.Y(fam.right), 4, PALETTE.blue, '#fff');
      } else if (s.kind === 'asymptote') {
        ctx.save();
        ctx.setLineDash([4, 4]);
        ctx.strokeStyle = PALETTE.red;
        ctx.beginPath();
        ctx.moveTo(ax, p.y0);
        ctx.lineTo(ax, p.y0 + p.h);
        ctx.stroke();
        ctx.restore();
      }

      // approaching arrows on both sides
      const near = 0.18;
      arrow(ctx, p.X(fam.a - near), p.Y(fam.f(fam.a - near)), p.X(fam.a - 0.02), p.Y(fam.f(fam.a - 0.02)), PALETTE.amber, 1.6);
      arrow(ctx, p.X(fam.a + near), p.Y(fam.f(fam.a + near)), p.X(fam.a + 0.02), p.Y(fam.f(fam.a + 0.02)), PALETTE.green, 1.6);
      label(ctx, 'from the left', ax - 46, p.y0 + 12, PALETTE.amber, 10, 'left');
      label(ctx, 'from the right', ax + 46, p.y0 + 12, PALETTE.green, 10, 'left');

      // the movable x
      const fx = fam.f(s.x);
      if (Number.isFinite(fx)) {
        ctx.save();
        ctx.setLineDash([3, 3]);
        ctx.strokeStyle = PALETTE.soft;
        ctx.beginPath();
        ctx.moveTo(p.X(s.x), p.y0);
        ctx.lineTo(p.X(s.x), p.y0 + p.h);
        ctx.stroke();
        ctx.restore();
        dot(ctx, p.X(s.x), p.clipY(fx), 4, PALETTE.accent);
      }

      // the table of values the unit asks students to read
      const tx = box.x + plotW + 18;
      const ty = box.y + 8;
      label(ctx, 'table of values', tx, ty + 2, PALETTE.ink, 11, 'left');
      ctx.save();
      ctx.font = MONO;
      ctx.fillStyle = PALETTE.soft;
      ctx.fillText('x', tx + 4, ty + 24);
      ctx.fillText('f(x)', tx + 92, ty + 24);
      ctx.restore();

      const offsets = [-0.5, -0.2, -0.05, -0.01];
      let row = 0;
      const drawRow = (x, color) => {
        const y = ty + 42 + row * 19;
        const v = fam.f(x);
        ctx.save();
        ctx.font = MONO;
        ctx.fillStyle = color;
        ctx.fillText((x < 0 ? '' : ' ') + x.toFixed(3), tx + 4, y);
        ctx.fillStyle = PALETTE.ink;
        ctx.fillText(Number.isFinite(v) ? (Math.abs(v) > 999 ? v.toExponential(1) : v.toFixed(3)) : '—', tx + 92, y);
        ctx.restore();
        row++;
      };
      offsets.slice().reverse().forEach((d) => drawRow(fam.a + d, PALETTE.amber));
      offsets.forEach((d) => drawRow(fam.a - d, PALETTE.green));

      label(ctx, 'left values ↑   right values ↓', tx + 4, ty + 42 + row * 19 + 4, PALETTE.soft, 10, 'left');
    }
  });

  /* ------------------------------------------------------------------ Unit 2
   * Definition as a limit of the difference quotient, and where differentiability
   * fails. h shrinks and the secant slides onto the tangent.
   */
  const U2_FUNCS = {
    square: { label: 'f(x) = x²', f: (x) => x * x, d: (x) => 2 * x, ymin: -2, ymax: 6, xmin: -2, xmax: 2.4 },
    cube: { label: 'f(x) = x³', f: (x) => x ** 3, d: (x) => 3 * x * x, ymin: -8, ymax: 8, xmin: -2, xmax: 2.2 },
    sine: { label: 'f(x) = sin x', f: Math.sin, d: Math.cos, ymin: -2, ymax: 2, xmin: -1.6, xmax: 4 },
    exp: { label: 'f(x) = eˣ', f: Math.exp, d: Math.exp, ymin: 0, ymax: 8, xmin: -1.6, xmax: 2 },
    abs: { label: 'f(x) = |x|', f: Math.abs, d: (x) => (x > 0 ? 1 : x < 0 ? -1 : NaN), ymin: -1, ymax: 3, xmin: -2, xmax: 2 }
  };

  window.CourseSims.register('apcalcab-u2-derivative', {
    title: 'Shrink h until the secant becomes the tangent',
    blurb:
      'The slope between x₀ and x₀ + h is the difference quotient. Drag h toward zero and watch the secant settle onto the tangent — that limit is the derivative at x₀.',
    params: [
      {
        k: 'fn',
        label: 'Function',
        type: 'select',
        val: 'square',
        options: Object.keys(U2_FUNCS).map((k) => ({ v: k, label: U2_FUNCS[k].label }))
      },
      { k: 'x0', label: 'x₀', min: -1.5, max: 2, step: 0.05, val: 0.8, decimals: 2 },
      { k: 'h', label: 'h (step)', min: 0.01, max: 1.5, step: 0.01, val: 1, decimals: 2 }
    ],
    readout(s) {
      const fam = U2_FUNCS[s.fn];
      const a = fam.f(s.x0);
      const b = fam.f(s.x0 + s.h);
      const sec = (b - a) / s.h;
      const tan = fam.d(s.x0);
      return [
        ['difference quotient', fmt(sec, 3)],
        ['f′(x₀)', Number.isFinite(tan) ? fmt(tan, 3) : 'undefined'],
        ['gap', Number.isFinite(tan) ? fmt(Math.abs(sec - tan), 4) : '—'],
        ['h', fmt(s.h, 2)]
      ];
    },
    note(s) {
      if (s.fn === 'abs' && Math.abs(s.x0) < 0.08) {
        return 'At the corner of |x| the left quotient tends to −1 and the right to +1. They never agree, so f′(0) does not exist — the graph is continuous there but not differentiable.';
      }
      if (s.h < 0.08) return 'h is tiny, so the secant and tangent are visually the same line. That is exactly what the limit means: the secant slope has converged.';
      return 'Cut h in half and watch the gap column. The secant slope approaches a definite number, not zero.';
    },
    draw(ctx, s, box) {
      const fam = U2_FUNCS[s.fn];
      const p = plot(ctx, box, {
        xmin: fam.xmin,
        xmax: fam.xmax,
        ymin: fam.ymin,
        ymax: fam.ymax,
        ticks: 4,
        xlabel: 'x'
      });

      curve(ctx, p, fam.f, PALETTE.blue, 2.4, fam.xmin, fam.xmax, 400);

      const x0 = s.x0;
      const x1 = x0 + s.h;
      const y0v = fam.f(x0);
      const y1v = fam.f(x1);
      const slope = (y1v - y0v) / s.h;

      // secant extended across the plot
      ctx.save();
      p.clipRect();
      ctx.strokeStyle = PALETTE.amber;
      ctx.lineWidth = 2;
      ctx.setLineDash([7, 4]);
      ctx.beginPath();
      ctx.moveTo(p.X(fam.xmin), p.Y(y0v + slope * (fam.xmin - x0)));
      ctx.lineTo(p.X(fam.xmax), p.Y(y0v + slope * (fam.xmax - x0)));
      ctx.stroke();
      ctx.restore();

      // tangent
      const m = fam.d(x0);
      if (Number.isFinite(m)) {
        ctx.save();
        p.clipRect();
        ctx.strokeStyle = PALETTE.green;
        ctx.lineWidth = 2.4;
        ctx.beginPath();
        ctx.moveTo(p.X(fam.xmin), p.Y(y0v + m * (fam.xmin - x0)));
        ctx.lineTo(p.X(fam.xmax), p.Y(y0v + m * (fam.xmax - x0)));
        ctx.stroke();
        ctx.restore();
      }

      dot(ctx, p.X(x0), p.Y(y0v), 4.5, PALETTE.ink);
      dot(ctx, p.X(x1), p.clipY(y1v), 4.5, PALETTE.accent);

      // run/rise guide on the secant
      ctx.save();
      ctx.setLineDash([3, 3]);
      ctx.strokeStyle = '#b9ab9b';
      ctx.beginPath();
      ctx.moveTo(p.X(x1), p.Y(y0v));
      ctx.lineTo(p.X(x1), p.clipY(y1v));
      ctx.moveTo(p.X(x0), p.Y(y0v));
      ctx.lineTo(p.X(x1), p.Y(y0v));
      ctx.stroke();
      ctx.restore();
      label(ctx, 'h', p.X((x0 + x1) / 2), p.Y(y0v) + 14, PALETTE.soft, 10);
      label(ctx, 'Δf', p.X(x1) + 10, p.Y((y0v + y1v) / 2), PALETTE.soft, 10, 'left');

      label(ctx, 'secant', p.X(fam.xmax) - 6, p.clipY(y0v + slope * (fam.xmax - x0)) - 6, PALETTE.amber, 10, 'right');
      label(ctx, 'tangent', p.X(fam.xmax) - 6, p.clipY(y0v + m * (fam.xmax - x0)) + 14, PALETTE.green, 10, 'right');
    }
  });

  /* ------------------------------------------------------------------ Unit 3
   * Related rates. The ladder is the canonical setup, but the readouts are the
   * quantities students are actually asked to justify: dy/dt, its sign, and its
   * blow-up as the top approaches the ground.
   */
  window.CourseSims.register('apcalcab-u3-related-rates', {
    title: 'Slide the ladder base and watch the top speed up',
    blurb:
      'A 5 m ladder leans on a wall. Push the base out at a steady dx/dt and the top does not fall steadily — its rate is set by the geometry, dy/dt = −(x/y)·dx/dt.',
    params: [
      { k: 'x', label: 'base x (m)', min: 0.5, max: 4.8, step: 0.05, val: 3, decimals: 2 },
      { k: 'dxdt', label: 'dx/dt (m/s)', min: 0.1, max: 2, step: 0.05, val: 0.6, decimals: 2 }
    ],
    readout(s) {
      const L = 5;
      const y = Math.sqrt(Math.max(0.0001, L * L - s.x * s.x));
      const dydt = (-s.x / y) * s.dxdt;
      return [
        ['height y', fmt(y, 2) + ' m'],
        ['dy/dt', fmt(dydt, 2) + ' m/s'],
        ['speed of top', fmt(Math.abs(dydt), 2) + ' m/s'],
        ['base x', fmt(s.x, 2) + ' m']
      ];
    },
    note(s) {
      const y = Math.sqrt(Math.max(0.0001, 25 - s.x * s.x));
      if (y < 1) return 'The top is nearly at the ground: y is small, so dy/dt = −(x/y)·dx/dt is huge. The base moves at a constant speed but the top does not.';
      if (s.x < 1.2) return 'Base close to the wall: y is large, so the top barely moves while the base moves quickly.';
      return 'Differentiate x² + y² = 25 with respect to t: 2x·dx/dt + 2y·dy/dt = 0, so dy/dt is negative whenever the base moves out.';
    },
    draw(ctx, s, box) {
      const g = ctx.createLinearGradient(0, box.y, 0, box.y + box.h);
      g.addColorStop(0, '#fffdf9');
      g.addColorStop(1, '#fdf6ec');
      ctx.fillStyle = g;
      ctx.fillRect(box.x, box.y, box.w, box.h);

      const ground = box.y + box.h - 26;
      const wallX = box.x + Math.max(64, box.w * 0.16);
      const scale = Math.min((box.h - 70) / 5.4, (box.w * 0.62) / 5.2);
      const L = 5;
      const y = Math.sqrt(Math.max(0, L * L - s.x * s.x));

      // wall and ground
      ctx.strokeStyle = '#b9a894';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(wallX, ground);
      ctx.lineTo(wallX, ground - 5.3 * scale);
      ctx.moveTo(wallX - 24, ground);
      ctx.lineTo(wallX + 5.2 * scale, ground);
      ctx.stroke();

      // ladder
      const baseX = wallX + s.x * scale;
      const topY = ground - y * scale;
      ctx.strokeStyle = '#8b5e34';
      ctx.lineWidth = 6;
      ctx.lineCap = 'round';
      ctx.beginPath();
      ctx.moveTo(wallX, topY);
      ctx.lineTo(baseX, ground);
      ctx.stroke();
      ctx.lineCap = 'butt';

      // ladder rungs
      for (let i = 1; i < 7; i++) {
        const f = i / 7;
        const x = lerp(wallX, baseX, f);
        const yy = lerp(topY, ground, f);
        const nx = (ground - topY) / 5;
        const ny = (baseX - wallX) / 5;
        ctx.strokeStyle = 'rgba(139,94,52,0.55)';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(x - nx * 0.16, yy - ny * 0.16);
        ctx.lineTo(x + nx * 0.16, yy + ny * 0.16);
        ctx.stroke();
      }

      // base motion arrow
      arrow(ctx, baseX - 34, ground + 12, baseX + 10, ground + 12, PALETTE.blue, 2);
      label(ctx, 'dx/dt = ' + fmt(s.dxdt, 1) + ' m/s', baseX + 4, ground + 26, PALETTE.blue, 10, 'left');

      // top motion arrow (downward, length scaled to actual speed)
      const speed = Math.min(2.6, (s.x / Math.max(0.2, y)) * s.dxdt);
      arrow(ctx, wallX - 12, topY, wallX - 12, topY + 18 + speed * 22, PALETTE.red, 2);
      label(ctx, 'dy/dt = ' + fmt((-s.x / Math.max(0.2, y)) * s.dxdt, 1), wallX - 18, topY + 12, PALETTE.red, 10, 'right');

      // dimension labels
      label(ctx, 'x = ' + fmt(s.x, 2) + ' m', (wallX + baseX) / 2, ground - 8, PALETTE.ink, 11);
      label(ctx, 'y = ' + fmt(y, 2) + ' m', wallX - 10, (ground + topY) / 2, PALETTE.ink, 11, 'right');
      label(ctx, '5 m', (wallX + baseX) / 2 + 12, (ground + topY) / 2 - 6, '#7c5a3a', 11, 'left');
    }
  });

  /* ------------------------------------------------------------------ Unit 4
   * Concavity, the second derivative, extrema and inflection. The cubic is
   * adjustable so students can break and restore each feature.
   */
  window.CourseSims.register('apcalcab-u4-concavity', {
    height: 330,
    title: 'Bend the cubic and watch f′ and f″ respond',
    blurb:
      'Change the coefficients. Green shading is where f is concave up (f″ > 0), rose where it is concave down. The dots mark where f′ changes sign (extrema) and where f″ changes sign (inflection).',
    params: [
      { k: 'a', label: 'x³ coefficient', min: -0.6, max: 0.6, step: 0.05, val: 0.35, decimals: 2 },
      { k: 'b', label: 'x² coefficient', min: -2, max: 2, step: 0.1, val: 0, decimals: 1 },
      { k: 'c', label: 'x coefficient', min: -3, max: 3, step: 0.1, val: -1.5, decimals: 1 },
      { k: 'cursor', label: 'probe x', min: -2.5, max: 2.5, step: 0.05, val: 0.8, decimals: 2 }
    ],
    readout(s) {
      const f2 = 6 * s.a * s.cursor + 2 * s.b;
      const f1 = 3 * s.a * s.cursor * s.cursor + 2 * s.b * s.cursor + s.c;
      return [
        ['f′(probe)', fmt(f1, 2)],
        ['f″(probe)', fmt(f2, 2)],
        ['concavity', Math.abs(f2) < 0.05 ? 'zero (inflection)' : f2 > 0 ? 'up' : 'down'],
        ['inflection', Math.abs(s.a) < 0.05 ? 'none' : 'x = ' + fmt(-s.b / (3 * s.a), 2)]
      ];
    },
    note(s) {
      if (Math.abs(s.a) < 0.05) return 'With the x³ term removed this is a parabola: f″ is constant, so the concavity never changes and there is no inflection point.';
      return 'Where f″ > 0 the curve holds water (concave up); where f″ < 0 it spills (concave down). f″ = 0 alone is not enough for an inflection — the sign must actually change.';
    },
    draw(ctx, s, box) {
      const f = (x) => s.a * x ** 3 + s.b * x * x + s.c * x;
      const f1 = (x) => 3 * s.a * x * x + 2 * s.b * x + s.c;
      const f2 = (x) => 6 * s.a * x + 2 * s.b;

      const topH = box.h * 0.66;
      const p = plot(ctx, { x: box.x, y: box.y, w: box.w, h: topH }, {
        xmin: -2.5,
        xmax: 2.5,
        ymin: -4,
        ymax: 4,
        ticks: 4,
        xlabel: 'x'
      });

      // concavity shading
      for (let i = 0; i < 120; i++) {
        const x = lerp(-2.5, 2.5, i / 120);
        const sign = f2(x);
        if (Math.abs(sign) < 0.02) continue;
        ctx.fillStyle = sign > 0 ? 'rgba(5,150,105,0.07)' : 'rgba(220,38,38,0.06)';
        ctx.fillRect(p.X(x), p.y0, p.w / 120 + 1, p.h);
      }

      curve(ctx, p, f, PALETTE.ink, 2.4, -2.5, 2.5, 400);

      // critical points and inflection
      const disc = 4 * s.b * s.b - 12 * s.a * s.c;
      if (Math.abs(s.a) > 0.02 && disc >= 0) {
        const r = Math.sqrt(disc);
        [-1, 1].forEach((sgn) => {
          const x = (-2 * s.b + sgn * r) / (6 * s.a);
          if (Math.abs(x) <= 2.5) dot(ctx, p.X(x), p.clipY(f(x)), 4, PALETTE.amber, '#fff');
        });
      }
      if (Math.abs(s.a) > 0.02) {
        const xi = -s.b / (3 * s.a);
        if (Math.abs(xi) <= 2.5) {
          dot(ctx, p.X(xi), p.clipY(f(xi)), 4, PALETTE.blue, '#fff');
          label(ctx, 'inflection', p.X(xi) + 6, p.clipY(f(xi)) - 8, PALETTE.blue, 10, 'left');
        }
      }

      // probe
      const px = s.cursor;
      ctx.save();
      ctx.setLineDash([3, 3]);
      ctx.strokeStyle = PALETTE.soft;
      ctx.beginPath();
      ctx.moveTo(p.X(px), p.y0);
      ctx.lineTo(p.X(px), p.y0 + p.h);
      ctx.stroke();
      ctx.restore();
      dot(ctx, p.X(px), p.clipY(f(px)), 4.5, PALETTE.accent);

      // derivative strip
      const lowBox = { x: box.x, y: box.y + topH + 8, w: box.w, h: box.h - topH - 8 };
      const q = plot(ctx, lowBox, {
        xmin: -2.5,
        xmax: 2.5,
        ymin: -8,
        ymax: 8,
        ticks: 2,
        xdigits: 1,
        ydigits: 0,
        background: '#fff'
      });
      curve(ctx, q, f1, PALETTE.amber, 2, -2.5, 2.5, 400);
      curve(ctx, q, f2, PALETTE.blue, 1.6, -2.5, 2.5, 400);
      label(ctx, 'f′', box.x + 8, lowBox.y + 14, PALETTE.amber, 11, 'left');
      label(ctx, 'f″', box.x + 28, lowBox.y + 14, PALETTE.blue, 11, 'left');
    }
  });

  /* ------------------------------------------------------------------ Unit 5
   * Riemann sums and the Fundamental Theorem: the sum converges to the signed
   * area, and the accumulation function's slope is the integrand.
   */
  const U5_FUNCS = {
    square: { label: 'f(x) = x² on [0, 2]', f: (x) => x * x, a: 0, b: 2 },
    sine: { label: 'f(x) = sin x on [0, π]', f: Math.sin, a: 0, b: Math.PI },
    inverse: { label: 'f(x) = 1/x on [1, 4]', f: (x) => 1 / x, a: 1, b: 4 }
  };

  window.CourseSims.register('apcalcab-u5-riemann', {
    height: 320,
    title: 'Rectangles under the curve, and the area they build',
    blurb:
      'Increase n and switch between left, right and midpoint. Then drag the upper limit: the shaded area is F(b), and the slope of that growing F is f at the top.',
    params: [
      {
        k: 'fn',
        label: 'Integrand',
        type: 'select',
        val: 'square',
        options: Object.keys(U5_FUNCS).map((k) => ({ v: k, label: U5_FUNCS[k].label }))
      },
      {
        k: 'method',
        label: 'Sample point',
        type: 'select',
        val: 'left',
        options: [
          { v: 'left', label: 'Left endpoint' },
          { v: 'right', label: 'Right endpoint' },
          { v: 'mid', label: 'Midpoint' }
        ]
      },
      { k: 'n', label: 'rectangles n', min: 1, max: 48, step: 1, val: 4, decimals: 0 },
      { k: 'limit', label: 'upper limit b', min: 0, max: 1, step: 0.02, val: 1, decimals: 2 }
    ],
    setup(s) {
      const fam = U5_FUNCS[s.fn];
      s._b = lerp(fam.a, fam.b, s.limit);
    },
    readout(s) {
      const fam = U5_FUNCS[s.fn];
      const b = lerp(fam.a, fam.b, s.limit);
      const n = Math.round(s.n);
      const dx = (b - fam.a) / n;
      let sum = 0;
      for (let i = 0; i < n; i++) {
        const left = fam.a + i * dx;
        const sample = s.method === 'left' ? left : s.method === 'right' ? left + dx : left + dx / 2;
        sum += fam.f(sample) * dx;
      }
      const exact = analytic(fam, fam.a, b);
      return [
        ['sum', fmt(sum, 3)],
        ['exact area', fmt(exact, 3)],
        ['error', fmt(Math.abs(sum - exact), 4)],
        ['Δx', fmt(dx, 3)]
      ];
    },
    note(s) {
      if (s.fn === 'inverse') return 'On 1/x the left sum overestimates and the right sum underestimates — the curve is decreasing. The gap shrinks like 1/n.';
      return 'f(b) is the rate at which area grows. Drag the upper limit slowly and watch the shaded region grow fastest where the curve is highest.';
    },
    draw(ctx, s, box) {
      const fam = U5_FUNCS[s.fn];
      const b = lerp(fam.a, fam.b, s.limit);
      const fmax = Math.max(fam.f(fam.a), fam.f(b), 1);
      const p = plot(ctx, { x: box.x, y: box.y, w: box.w, h: box.h }, {
        xmin: fam.a,
        xmax: fam.b,
        ymin: 0,
        ymax: fmax * 1.12,
        ticks: 4,
        xlabel: 'x'
      });

      const n = Math.round(s.n);
      const dx = (b - fam.a) / n;
      for (let i = 0; i < n; i++) {
        const left = fam.a + i * dx;
        const sample = s.method === 'left' ? left : s.method === 'right' ? left + dx : left + dx / 2;
        const h = fam.f(sample);
        const x0 = p.X(left);
        const x1 = p.X(left + dx);
        ctx.fillStyle = 'rgba(37,99,235,0.13)';
        ctx.fillRect(x0, p.Y(h), Math.max(1, x1 - x0 - 1), p.Y(0) - p.Y(h));
        ctx.strokeStyle = 'rgba(37,99,235,0.5)';
        ctx.lineWidth = 1;
        ctx.strokeRect(x0 + 0.5, p.Y(h) + 0.5, Math.max(1, x1 - x0 - 1), p.Y(0) - p.Y(h));
      }

      curve(ctx, p, fam.f, PALETTE.ink, 2.4, fam.a, fam.b, 300);

      ctx.save();
      ctx.setLineDash([4, 4]);
      ctx.strokeStyle = PALETTE.accent;
      ctx.beginPath();
      ctx.moveTo(p.X(b), p.y0);
      ctx.lineTo(p.X(b), p.y0 + p.h);
      ctx.stroke();
      ctx.restore();
      label(ctx, 'b', p.X(b), p.y0 + p.h + 16, PALETTE.accent, 11);

      // slope of the accumulation function is f(b)
      const slope = fam.f(b);
      arrow(ctx, p.X(b) - 40, p.Y(0), p.X(b), p.Y(0) - 0, 'rgba(0,0,0,0)', 0);
      label(ctx, 'F′(b) = f(b) = ' + fmt(slope, 2), p.X(b) - 6, p.y0 + 14, PALETTE.accent, 10, 'right');
    }
  });

  function analytic(fam, a, b) {
    if (fam.f === U5_FUNCS.square.f) return (b ** 3 - a ** 3) / 3;
    if (fam.f === U5_FUNCS.sine.f) return -Math.cos(b) + Math.cos(a);
    if (fam.f === U5_FUNCS.inverse.f) return Math.log(b) - Math.log(a);
    return 0;
  }

  /* ------------------------------------------------------------------ Unit 6
   * Volumes by disks and washers: slices seen edge-on, then as a stack.
   */
  window.CourseSims.register('apcalcab-u6-disks', {
    height: 330,
    title: 'Slice the solid and add up the disks',
    blurb:
      'Rotating the region about the x-axis builds a solid. Each slice is a disk (or a washer when there is an inner curve). More slices means the sum tracks the exact volume.',
    params: [
      {
        k: 'solid',
        label: 'Solid',
        type: 'select',
        val: 'disk',
        options: [
          { v: 'disk', label: 'Disk: y = √x on [0, 4]' },
          { v: 'washer', label: 'Washer: √x around x/2' }
        ]
      },
      { k: 'n', label: 'slices', min: 3, max: 40, step: 1, val: 8, decimals: 0 }
    ],
    readout(s) {
      const n = Math.round(s.n);
      let sum = 0;
      const dx = 4 / n;
      for (let i = 0; i < n; i++) {
        // left endpoint, like the slice drawn at the left face of each disk, so
        // the error actually shrinks as n grows instead of vanishing on the first try
        const x = i * dx;
        const outer = Math.sqrt(x);
        const inner = s.solid === 'washer' ? x / 2 : 0;
        sum += Math.PI * (outer * outer - inner * inner) * dx;
      }
      const exact = s.solid === 'washer' ? Math.PI * (8 - 16 / 12) : Math.PI * 8;
      return [
        ['slice volume sum', fmt(sum, 3)],
        ['exact volume', fmt(exact, 3)],
        ['error', fmt(Math.abs(sum - exact), 3)],
        ['Δx', fmt(dx, 3)]
      ];
    },
    note(s) {
      if (s.solid === 'washer') return 'The washer formula subtracts the hole: π(R² − r²)Δx. The inner radius here is the line y = x/2.';
      return 'Each slice is a disk of radius f(x) and thickness Δx, so its volume is π f(x)² Δx. The integral adds infinitely many of them.';
    },
    draw(ctx, s, box) {
      const splitX = box.x + box.w * 0.46;
      const side = { x: box.x, y: box.y, w: box.w * 0.46, h: box.h };
      const p = plot(ctx, side, { xmin: -2.4, xmax: 4.2, ymin: -3, ymax: 3, ticks: 2, xlabel: 'x' });

      const axisY = p.Y(0);
      ctx.strokeStyle = '#b9a894';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(p.x0, axisY);
      ctx.lineTo(p.x0 + p.w, axisY);
      ctx.stroke();

      curve(ctx, p, (x) => Math.sqrt(Math.max(0, x)), PALETTE.blue, 2.2, 0, 4, 200);
      curve(ctx, p, (x) => -Math.sqrt(Math.max(0, x)), 'rgba(37,99,235,0.5)', 2, 0, 4, 200);
      if (s.solid === 'washer') {
        curve(ctx, p, (x) => x / 2, PALETTE.amber, 1.8, 0, 4, 200);
        curve(ctx, p, (x) => -x / 2, PALETTE.amber, 1.8, 0, 4, 200);
      }

      const n = Math.round(s.n);
      const dx = 4 / n;
      for (let i = 0; i < n; i++) {
        const x = i * dx;
        const r = Math.sqrt(Math.max(0, x));
        const inner = s.solid === 'washer' ? x / 2 : 0;
        ctx.strokeStyle = 'rgba(37,99,235,0.45)';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(p.X(x), p.Y(-r));
        ctx.lineTo(p.X(x), p.Y(r));
        ctx.stroke();
        if (inner > 0.01) {
          ctx.strokeStyle = 'rgba(217,119,6,0.6)';
          ctx.beginPath();
          ctx.moveTo(p.X(x), p.Y(-inner));
          ctx.lineTo(p.X(x), p.Y(inner));
          ctx.stroke();
        }
      }

      // oblique stack of disks on the right
      const cx = splitX + 44;
      const cy = box.y + box.h * 0.5;
      label(ctx, 'the stack of slices', cx + 6, box.y + 14, PALETTE.ink, 11, 'left');
      const total = Math.max(3, Math.min(12, n));
      const room = box.x + box.w - cx - 42;
      const step = Math.min(38, room / (total - 1));
      const radiusScale = Math.min(22, Math.max(12, (box.h * 0.34) / 2));
      for (let i = 0; i < total; i++) {
        const f = i / (total - 1);
        const x = f * 4;
        const r = Math.sqrt(Math.max(0.06, x)) * radiusScale;
        const inner = s.solid === 'washer' ? (x / 2) * radiusScale : 0;
        const px = cx + i * step;
        const py = cy + (i % 2) * 2;
        ctx.save();
        ctx.translate(px, py);
        ctx.transform(1, 0.5, 0, 1, 0, 0);
        ctx.strokeStyle = 'rgba(37,99,235,0.75)';
        ctx.fillStyle = 'rgba(37,99,235,0.10)';
        ctx.lineWidth = 1.6;
        ctx.beginPath();
        ctx.ellipse(0, 0, r * 0.42, r, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
        if (inner > 0.5) {
          ctx.fillStyle = '#fffdf9';
          ctx.beginPath();
          ctx.ellipse(0, 0, inner * 0.42, inner, 0, 0, Math.PI * 2);
          ctx.fill();
          ctx.stroke();
        }
        ctx.restore();
      }
      label(ctx, 'radius grows with x', cx + 4, box.y + box.h - 14, PALETTE.soft, 10, 'left');
    }
  });

  /* ------------------------------------------------------------------ Unit 7
   * Slope fields, Euler steps and separable solutions.
   */
  const U7_FIELDS = {
    exp: { label: "y′ = y", f: (x, y) => y, exact: (x, y0) => y0 * Math.exp(x) },
    logistic: { label: 'y′ = y(1 − y)', f: (x, y) => y * (1 - y), exact: null },
    linsum: { label: "y′ = x + y", f: (x, y) => x + y, exact: (x, y0) => (y0 + 1) * Math.exp(x) - x - 1 },
    mix: { label: 'y′ = x − y', f: (x, y) => x - y, exact: (x, y0) => x - 1 + (y0 + 1) * Math.exp(-x) }
  };

  window.CourseSims.register('apcalcab-u7-slope-field', {
    title: 'Follow the little slope segments',
    blurb:
      "Each segment has slope f(x, y) at that point. Pick a starting y and let Euler's method crawl along the field one step at a time; the green curve is the exact solution when one exists.",
    params: [
      {
        k: 'field',
        label: 'Differential equation',
        type: 'select',
        val: 'exp',
        options: Object.keys(U7_FIELDS).map((k) => ({ v: k, label: U7_FIELDS[k].label }))
      },
      { k: 'y0', label: 'starting y(0)', min: -2, max: 2, step: 0.1, val: 1, decimals: 1 },
      { k: 'h', label: 'Euler step h', min: 0.1, max: 0.5, step: 0.05, val: 0.25, decimals: 2 }
    ],
    readout(s) {
      const fam = U7_FIELDS[s.field];
      let y = s.y0;
      let x = 0;
      let steps = 0;
      while (x < 1 - 1e-9) {
        const step = Math.min(s.h, 1 - x);
        y = y + fam.f(x, y) * step;
        x += step;
        steps++;
      }
      const exact = fam.exact ? fam.exact(1, s.y0) : null;
      return [
        ['Euler y(1)', fmt(y, 3)],
        ['exact y(1)', exact === null ? '—' : fmt(exact, 3)],
        ['error', exact === null ? '—' : fmt(Math.abs(y - exact), 3)],
        ['steps', String(steps)]
      ];
    },
    note(s) {
      if (s.h > 0.3) return 'Large steps drift badly: Euler follows the tangent blindly across a whole interval. Halve h and the error usually halves too.';
      return 'The solution curve never crosses another solution curve, and it is tangent to every little segment it passes through.';
    },
    draw(ctx, s, box) {
      const fam = U7_FIELDS[s.field];
      const p = plot(ctx, box, { xmin: -0.2, xmax: 1.2, ymin: -3, ymax: 3, ticks: 4, xlabel: 'x' });

      const cols = 13;
      const rows = 11;
      for (let i = 0; i <= cols; i++) {
        for (let j = 0; j <= rows; j++) {
          const x = lerp(-0.2, 1.2, i / cols);
          const y = lerp(-3, 3, j / rows);
          const m = fam.f(x, y);
          const ang = Math.atan(m);
          const len = 9;
          const px = p.X(x);
          const py = p.Y(y);
          ctx.strokeStyle = 'rgba(120,113,108,0.42)';
          ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.moveTo(px - Math.cos(ang) * len, py - Math.sin(ang) * len * 1.0);
          ctx.lineTo(px + Math.cos(ang) * len, py + Math.sin(ang) * len);
          ctx.stroke();
        }
      }

      if (fam.exact) {
        curve(ctx, p, (x) => fam.exact(x, s.y0), PALETTE.green, 2, 0, 1.2, 200);
      }

      // Euler polyline
      let y = s.y0;
      let x = 0;
      ctx.strokeStyle = PALETTE.accent;
      ctx.lineWidth = 2.2;
      ctx.beginPath();
      ctx.moveTo(p.X(0), p.Y(y));
      const pts = [[0, y]];
      while (x < 1 - 1e-9) {
        const step = Math.min(s.h, 1 - x);
        y = y + fam.f(x, y) * step;
        x += step;
        ctx.lineTo(p.X(x), p.Y(y));
        pts.push([x, y]);
      }
      ctx.stroke();
      pts.forEach(([px, py]) => dot(ctx, p.X(px), p.Y(py), 3, PALETTE.accent));

      label(ctx, 'Euler', p.X(1) + 6, p.Y(pts[pts.length - 1][1]) - 8, PALETTE.accent, 10, 'left');
      if (fam.exact) label(ctx, 'exact', p.X(1) + 6, p.Y(fam.exact(1, s.y0)) + 12, PALETTE.green, 10, 'left');
    }
  });

  /* ------------------------------------------------------------------ Unit 8
   * Mixed-review capstone: one function read four ways — value, slope, bend,
   * and accumulated area — because the AP free-response asks students to move
   * between those four without being told which one is wanted.
   */
  const U8_FUNCS = {
    cubic: { label: 'f(x) = x³ − 3x', f: (x) => x ** 3 - 3 * x, d: (x) => 3 * x * x - 3, d2: (x) => 6 * x, F: (x) => x ** 4 / 4 - 1.5 * x * x, ymin: -5, ymax: 5 },
    sine: { label: 'f(x) = 2 sin x', f: (x) => 2 * Math.sin(x), d: (x) => 2 * Math.cos(x), d2: (x) => -2 * Math.sin(x), F: (x) => -2 * Math.cos(x), ymin: -4, ymax: 4 },
    bell: { label: 'f(x) = 4/(1 + x²)', f: (x) => 4 / (1 + x * x), d: (x) => (-8 * x) / (1 + x * x) ** 2, d2: (x) => (24 * x * x - 8) / (1 + x * x) ** 3, F: (x) => 4 * Math.atan(x), ymin: -1, ymax: 5 }
  };

  window.CourseSims.register('apcalcab-u8-capstone', {
    title: 'One graph, four questions',
    blurb:
      'Every AP free-response mixes these four readings. Move a and b: the dot reads the function, the straight line is its derivative there, the shading is the accumulated area, and the average value is that area spread flat.',
    params: [
      {
        k: 'fn',
        label: 'Function',
        type: 'select',
        val: 'cubic',
        options: Object.keys(U8_FUNCS).map((k) => ({ v: k, label: U8_FUNCS[k].label }))
      },
      { k: 'a', label: 'left a', min: -2, max: 1.6, step: 0.05, val: -1.5, decimals: 2 },
      { k: 'b', label: 'right b', min: -1.6, max: 2, step: 0.05, val: 1.5, decimals: 2 }
    ],
    readout(s) {
      const fam = U8_FUNCS[s.fn];
      const a = Math.min(s.a, s.b);
      const b = Math.max(s.a, s.b);
      const area = fam.F(b) - fam.F(a);
      return [
        ['value', fmt(fam.f(a), 2)],
        ['slope', fmt(fam.d(a), 2)],
        ['bend', fmt(fam.d2(a), 2)],
        ['signed area', fmt(area, 2)],
        ['average value', fmt(area / (b - a || 1), 2)]
      ];
    },
    note(s) {
      if (Math.abs(s.fn === 'cubic' ? s.a : 0) < 0.1) return 'At an extremum the tangent is horizontal, so f′ = 0. Look for that flat line as you move a.';
      return 'The signed area can be negative: area below the axis subtracts. That is why the average value can be less than the peak.';
    },
    draw(ctx, s, box) {
      const fam = U8_FUNCS[s.fn];
      const p = plot(ctx, box, { xmin: -2.2, xmax: 2.2, ymin: fam.ymin, ymax: fam.ymax, ticks: 4, xlabel: 'x' });
      const a = Math.min(s.a, s.b);
      const b = Math.max(s.a, s.b);

      // signed area shading
      for (let i = 0; i < 110; i++) {
        const x = lerp(a, b, i / 110);
        const y = fam.f(x);
        const top = p.Y(Math.max(0, y));
        const bot = p.Y(Math.min(0, y));
        ctx.fillStyle = y >= 0 ? 'rgba(5,150,105,0.16)' : 'rgba(220,38,38,0.12)';
        ctx.fillRect(p.X(x), top, p.w / 110 + 1, bot - top);
      }

      curve(ctx, p, fam.f, PALETTE.ink, 2.4, -2.2, 2.2, 400);

      // tangent at a
      const m = fam.d(a);
      const ya = fam.f(a);
      ctx.save();
      p.clipRect();
      ctx.strokeStyle = PALETTE.accent;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(p.X(-2.2), p.Y(ya + m * (-2.2 - a)));
      ctx.lineTo(p.X(2.2), p.Y(ya + m * (2.2 - a)));
      ctx.stroke();
      ctx.restore();
      dot(ctx, p.X(a), p.clipY(ya), 4.5, PALETTE.accent, '#fff');

      ctx.save();
      ctx.setLineDash([3, 3]);
      ctx.strokeStyle = PALETTE.soft;
      [a, b].forEach((x) => {
        ctx.beginPath();
        ctx.moveTo(p.X(x), p.y0);
        ctx.lineTo(p.X(x), p.y0 + p.h);
        ctx.stroke();
      });
      ctx.restore();
      label(ctx, 'a', p.X(a), p.y0 + p.h + 16, PALETTE.accent, 11);
      label(ctx, 'b', p.X(b), p.y0 + p.h + 16, PALETTE.accent, 11);

      label(ctx, 'slope ' + fmt(m, 2), p.X(a) + 8, p.clipY(ya) - 10, PALETTE.accent, 10, 'left');
      label(ctx, 'signed area ' + fmt(fam.F(b) - fam.F(a), 2), p.X((a + b) / 2), p.y0 + 16, PALETTE.ink, 10);
    }
  });
})();
