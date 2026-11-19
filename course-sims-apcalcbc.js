/* ============================================================================
 * AP Calculus BC — one simulation per unit, matched to that unit's sections.
 * ========================================================================== */
(function () {
  'use strict';
  const S = window.CourseSims && window.CourseSims.util;
  if (!S) return;
  const { plot, curve, arrow, dot, label, fmt, clamp, lerp, PALETTE } = S;

  /* U1 — parametric derivatives: dy/dx = (dy/dt)/(dx/dt), cusp where dx/dt = 0 */
  window.CourseSims.register('apcalcbc-u1-parametric', {
    title: 'Parametric motion: one parameter, two derivatives',
    blurb:
      'A cycloid is traced by a point on a rolling wheel. Slide t along the curve: the tangent slope is (dy/dt) ÷ (dx/dt), and at the cusp the ratio breaks because dx/dt hits zero.',
    params: [
      { k: 'a', label: 'wheel radius a', min: 0.4, max: 1.4, step: 0.05, val: 1, decimals: 2 },
      { k: 't', label: 't', min: 0.2, max: 6.1, step: 0.02, val: 2, decimals: 2 }
    ],
    readout(s) {
      const dx = s.a * (1 - Math.cos(s.t));
      const dy = s.a * Math.sin(s.t);
      return [
        ['dx/dt', fmt(dx, 3)],
        ['dy/dt', fmt(dy, 3)],
        ['dy/dx', Math.abs(dx) < 1e-3 ? 'undefined (cusp)' : fmt(dy / dx, 3)],
        ['speed', fmt(Math.hypot(dx, dy), 3)]
      ];
    },
    note(s) {
      return Math.abs(1 - Math.cos(s.t)) < 0.05
        ? 'At the cusp the point reverses direction: dx/dt = 0 but dy/dt ≠ 0, so the slope is vertical/undefined. Parametric curves can fail where ordinary graphs cannot.'
        : 'The tangent slope comes from dividing the two rates. Speed, unlike slope, uses both components and never divides.';
    },
    draw(ctx, s, box) {
      const X = (t) => s.a * (t - Math.sin(t));
      const Y = (t) => s.a * (1 - Math.cos(t));
      const p = plot(ctx, box, { xmin: -0.5, xmax: 9, ymin: -0.4, ymax: 2.6, ticks: 4, xlabel: 'x' });
      ctx.strokeStyle = '#b9a894';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(p.X(-0.5), p.Y(0));
      ctx.lineTo(p.X(9), p.Y(0));
      ctx.stroke();

      ctx.strokeStyle = PALETTE.blue;
      ctx.lineWidth = 2.4;
      ctx.beginPath();
      for (let t = 0; t <= 6.4; t += 0.02) {
        const px = p.X(X(t));
        const py = p.Y(Y(t));
        if (t === 0) ctx.moveTo(px, py);
        else ctx.lineTo(px, py);
      }
      ctx.stroke();

      const px = p.X(X(s.t));
      const py = p.Y(Y(s.t));
      const dx = s.a * (1 - Math.cos(s.t));
      const dy = s.a * Math.sin(s.t);
      const len = 34;
      const n = Math.hypot(dx, dy) || 1;
      arrow(ctx, px, py, px + (dx / n) * len, py - (dy / n) * len, PALETTE.accent, 2);

      ctx.save();
      const m = Math.abs(dx) < 1e-3 ? 0 : dy / dx;
      if (m && isFinite(m)) {
        p.clipRect();
        ctx.strokeStyle = PALETTE.green;
        ctx.lineWidth = 1.8;
        ctx.beginPath();
        ctx.moveTo(px - 60, py + 60 * m);
        ctx.lineTo(px + 60, py - 60 * m);
        ctx.stroke();
      } else {
        ctx.strokeStyle = PALETTE.red;
        ctx.lineWidth = 1.8;
        ctx.beginPath();
        ctx.moveTo(px, py - 40);
        ctx.lineTo(px, py + 40);
        ctx.stroke();
      }
      ctx.restore();
      dot(ctx, px, py, 5, PALETTE.accent, '#fff');
      label(ctx, 'velocity', px + 42, py - 14, PALETTE.accent, 10, 'left');
    }
  });

  /* U2 — improper integrals: p-test and the tail that will not close */
  window.CourseSims.register('apcalcbc-u2-improper', {
    title: 'Improper integrals: does the tail close?',
    blurb:
      'Shade 1/xᵖ out to x = R. Raise p above 1 and the area stops at a finite number; drop below 1 and it keeps growing — the difference between convergence and divergence is one exponent.',
    params: [
      { k: 'p', label: 'exponent p', min: 0.3, max: 2.5, step: 0.05, val: 1.2, decimals: 2 },
      { k: 'R', label: 'cutoff R', min: 2, max: 60, step: 1, val: 20, decimals: 0 }
    ],
    readout(s) {
      const area = Math.abs(s.p - 1) < 1e-3 ? Math.log(s.R) : (Math.pow(s.R, 1 - s.p) - 1) / (1 - s.p);
      const limit = s.p > 1 ? 1 / (s.p - 1) : Infinity;
      return [
        ['area to R', fmt(area, 3)],
        ['limit as R→∞', isFinite(limit) ? fmt(limit, 3) : 'diverges'],
        ['verdict', s.p > 1 ? 'converges' : s.p === 1 ? 'diverges (log)' : 'diverges'],
        ['tail remaining', isFinite(limit) ? fmt(Math.max(0, limit - area), 3) : '—']
      ];
    },
    note(s) {
      if (Math.abs(s.p - 1) < 0.06) return 'p = 1 is the borderline case: the area grows like ln R, slowly but without bound. Every p > 1 converges, no matter how slightly.';
      return s.p > 1
        ? 'The tail still contributes, but less and less: the remaining sliver shrinks toward the finite total. Push R larger and watch the limit column stop changing.'
        : 'Each extra strip adds enough to matter. The partial area keeps climbing, so the improper integral has no finite value.';
    },
    draw(ctx, s, box) {
      const f = (x) => Math.pow(x, -s.p);
      const ymax = Math.min(2.2, f(1) * 1.15);
      const p = plot(ctx, box, { xmin: 1, xmax: 60, ymin: 0, ymax: Math.max(0.6, ymax), ticks: 4, xdigits: 0, ydigits: 1, xlabel: 'x' });

      for (let i = 0; i < 80; i++) {
        const x = lerp(1, s.R, i / 80);
        const nx = lerp(1, s.R, (i + 1) / 80);
        ctx.fillStyle = 'rgba(37,99,235,0.14)';
        ctx.fillRect(p.X(x), p.Y(f(x)), Math.max(1, p.X(nx) - p.X(x) + 1), p.Y(0) - p.Y(f(x)));
      }
      curve(ctx, p, f, PALETTE.blue, 2.2, 1, 60, 300);

      ctx.save();
      ctx.setLineDash([4, 4]);
      ctx.strokeStyle = PALETTE.accent;
      ctx.beginPath();
      ctx.moveTo(p.X(s.R), p.y0);
      ctx.lineTo(p.X(s.R), p.y0 + p.h);
      ctx.stroke();
      ctx.restore();
      label(ctx, 'R', p.X(s.R), p.y0 + p.h + 16, PALETTE.accent, 11);
      label(ctx, '1/x^' + fmt(s.p, 2), p.X(6), p.Y(f(6)) - 8, PALETTE.blue, 10);
    }
  });

  /* U3 — arc length: straight segments approximating a curve */
  window.CourseSims.register('apcalcbc-u3-arclength', {
    title: 'Arc length: straighten the curve with segments',
    blurb:
      'Chop y = x² into n straight pieces. The sum of their lengths climbs toward the true arc length; the integrand √(1 + (dy/dx)²) is just the hypotenuse of one piece in the limit.',
    params: [
      { k: 'n', label: 'segments n', min: 1, max: 40, step: 1, val: 4, decimals: 0 },
      { k: 'x', label: 'marker x', min: 0, max: 2, step: 0.05, val: 1.2, decimals: 2 }
    ],
    readout(s) {
      const n = Math.round(s.n);
      const dx = 2 / n;
      let sum = 0;
      for (let i = 0; i < n; i++) {
        const x0 = i * dx;
        const y0 = x0 * x0;
        const y1 = (x0 + dx) * (x0 + dx);
        sum += Math.hypot(dx, y1 - y0);
      }
      const exact = 4.6468; // ∫₀² √(1 + 4x²) dx
      return [
        ['polyline', fmt(sum, 4)],
        ['arc length', fmt(exact, 4)],
        ['short by', fmt(exact - sum, 4)],
        ['segments', String(n)]
      ];
    },
    note(s) {
      return s.n < 6
        ? 'Few long chords cut the corners, so the polyline is shorter than the curve. Doubling n adds the in-between detail back.'
        : 'Each chord is √(Δx² + Δy²). Factor out Δx and the sum becomes a Riemann sum for √(1 + (dy/dx)²).';
    },
    draw(ctx, s, box) {
      const p = plot(ctx, box, { xmin: 0, xmax: 2, ymin: 0, ymax: 4.4, ticks: 4, xlabel: 'x' });
      curve(ctx, p, (x) => x * x, PALETTE.ink, 2.2, 0, 2, 200);

      const n = Math.round(s.n);
      const dx = 2 / n;
      ctx.strokeStyle = PALETTE.amber;
      ctx.lineWidth = 2;
      ctx.beginPath();
      for (let i = 0; i <= n; i++) {
        const x = i * dx;
        const px = p.X(x);
        const py = p.Y(x * x);
        if (i === 0) ctx.moveTo(px, py);
        else ctx.lineTo(px, py);
      }
      ctx.stroke();

      // one segment's dx and dy, labelled
      const i = Math.min(n - 1, Math.floor((s.x / 2) * n));
      const x0 = i * dx;
      const x1 = x0 + dx;
      ctx.save();
      ctx.setLineDash([3, 3]);
      ctx.strokeStyle = PALETTE.blue;
      ctx.beginPath();
      ctx.moveTo(p.X(x0), p.Y(x0 * x0));
      ctx.lineTo(p.X(x1), p.Y(x0 * x0));
      ctx.lineTo(p.X(x1), p.Y(x1 * x1));
      ctx.stroke();
      ctx.restore();
      label(ctx, 'Δx', p.X((x0 + x1) / 2), p.Y(x0 * x0) + 14, PALETTE.blue, 10);
      dot(ctx, p.X(s.x), p.Y(s.x * s.x), 4, PALETTE.accent);
    }
  });

  /* U4 — geometric series: partial sums and the radius of convergence */
  window.CourseSims.register('apcalcbc-u4-geometric', {
    title: 'Geometric series: watch the partial sums decide',
    blurb:
      'Terms shrink for every |r| < 1, but shrinking terms alone do not make a series converge. Slide r through 1 and −1 and watch what the partial sums do.',
    params: [
      { k: 'r', label: 'ratio r', min: -1.4, max: 1.4, step: 0.02, val: 0.6, decimals: 2 },
      { k: 'n', label: 'terms n', min: 1, max: 30, step: 1, val: 8, decimals: 0 }
    ],
    readout(s) {
      const n = Math.round(s.n);
      let sum = 0;
      for (let i = 0; i < n; i++) sum += Math.pow(s.r, i);
      const limit = Math.abs(s.r) < 1 ? 1 / (1 - s.r) : Infinity;
      return [
        ['Sₙ', fmt(sum, 4)],
        ['limit', isFinite(limit) ? fmt(limit, 4) : 'diverges'],
        ['aₙ', fmt(Math.pow(s.r, n - 1), 4)],
        ['gap', isFinite(limit) ? fmt(Math.abs(limit - sum), 4) : '—']
      ];
    },
    note(s) {
      if (s.r <= -1) return 'At r = −1 the terms do not shrink at all and the sums alternate between 0 and 1: no limit. For r < −1 the terms grow and the sums explode.';
      if (s.r >= 1) return 'Terms do not approach zero (at r = 1 they are all 1), so the series cannot converge — the nth-term test rules it out immediately.';
      return 'The gap column is the whole story: each added term closes part of the remaining gap, and the limit is exactly a/(1 − r).';
    },
    draw(ctx, s, box) {
      const p = plot(ctx, box, { xmin: 0, xmax: 30, ymin: -3, ymax: 4, ticks: 3, xdigits: 0, ydigits: 0, xlabel: 'n' });
      let sum = 0;
      const pts = [];
      for (let i = 1; i <= 30; i++) {
        sum += Math.pow(s.r, i - 1);
        pts.push([i, sum]);
      }
      ctx.strokeStyle = PALETTE.soft;
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      pts.forEach(([x, y], idx) => {
        const px = p.X(x);
        const py = p.clipY(y);
        if (idx === 0) ctx.moveTo(px, py);
        else ctx.lineTo(px, py);
      });
      ctx.stroke();
      pts.forEach(([x, y], idx) => {
        dot(ctx, p.X(x), p.clipY(y), idx < Math.round(s.n) ? 3.2 : 2, idx < Math.round(s.n) ? PALETTE.accent : '#cbbfb2');
      });

      if (Math.abs(s.r) < 1) {
        const L = 1 / (1 - s.r);
        ctx.save();
        ctx.setLineDash([5, 4]);
        ctx.strokeStyle = PALETTE.green;
        ctx.beginPath();
        ctx.moveTo(p.x0, p.clipY(L));
        ctx.lineTo(p.x0 + p.w, p.clipY(L));
        ctx.stroke();
        ctx.restore();
        label(ctx, 'a/(1−r) = ' + fmt(L, 2), p.x0 + p.w - 6, p.clipY(L) - 6, PALETTE.green, 10, 'right');
      }
    }
  });

  /* U5 — radius of convergence for Σ xⁿ/n */
  window.CourseSims.register('apcalcbc-u5-radius', {
    title: 'Power series: where do the partial sums settle?',
    blurb:
      'For Σ xⁿ/n the ratio test gives |x|, so the radius is 1. Move x inside, to the edge, and outside: inside converges, outside blows up, and the endpoints each need their own test.',
    params: [
      { k: 'x', label: 'x', min: -1.6, max: 1.6, step: 0.02, val: 0.8, decimals: 2 },
      { k: 'n', label: 'terms n', min: 1, max: 60, step: 1, val: 20, decimals: 0 }
    ],
    readout(s) {
      const n = Math.round(s.n);
      let sum = 0;
      let last = 0;
      for (let i = 1; i <= n; i++) {
        last = Math.pow(s.x, i) / i;
        sum += last;
      }
      const ratio = Math.abs(s.x) * n / (n + 1);
      return [
        ['Sₙ', Number.isFinite(sum) ? fmt(sum, 4) : '—'],
        ['last term', fmt(last, 4)],
        ['ratio bound |x|', fmt(Math.abs(s.x), 2)],
        ['converges?', Math.abs(s.x) < 1 ? 'yes' : Math.abs(s.x) === 1 ? 'endpoint — test it' : 'no']
      ];
    },
    note(s) {
      if (Math.abs(s.x - 1) < 0.02) return 'At x = 1 this becomes the harmonic series Σ 1/n, which diverges. The radius alone does not decide endpoints.';
      if (Math.abs(s.x + 1) < 0.02) return 'At x = −1 it is the alternating harmonic series, which converges by the AST. Same radius, different endpoint verdicts.';
      return 'The ratio |aₙ₊₁/aₙ| → |x|. Below 1 the terms are eventually shrinking geometrically; above 1 they grow.';
    },
    draw(ctx, s, box) {
      const p = plot(ctx, box, { xmin: 0, xmax: 61, ymin: -6, ymax: 4, ticks: 3, xdigits: 0, ydigits: 0, xlabel: 'n' });
      let sum = 0;
      const pts = [];
      for (let i = 1; i <= 60; i++) {
        sum += Math.pow(s.x, i) / i;
        pts.push([i, sum]);
      }
      ctx.strokeStyle = PALETTE.blue;
      ctx.lineWidth = 2;
      ctx.beginPath();
      pts.forEach(([x, y], idx) => {
        const px = p.X(x);
        const py = p.clipY(y);
        if (idx === 0) ctx.moveTo(px, py);
        else ctx.lineTo(px, py);
      });
      ctx.stroke();

      const n = Math.round(s.n);
      dot(ctx, p.X(n), p.clipY(pts[n - 1][1]), 4.5, PALETTE.accent);
      if (Math.abs(s.x) < 1) {
        const L = -Math.log(1 - s.x);
        ctx.save();
        ctx.setLineDash([5, 4]);
        ctx.strokeStyle = PALETTE.green;
        ctx.beginPath();
        ctx.moveTo(p.x0, p.clipY(L));
        ctx.lineTo(p.x0 + p.w, p.clipY(L));
        ctx.stroke();
        ctx.restore();
        label(ctx, '−ln(1−x) = ' + fmt(L, 2), p.x0 + p.w - 6, p.clipY(L) + 13, PALETTE.green, 10, 'right');
      }
    }
  });

  /* U6 — Taylor polynomial degree vs the real function */
  window.CourseSims.register('apcalcbc-u6-taylor', {
    title: 'Taylor polynomials: add one term at a time',
    blurb:
      'A Taylor polynomial is built to match the function at one point, then is trusted further away. Raise the degree and watch how far the match survives — and where it breaks.',
    params: [
      {
        k: 'fn',
        label: 'Function',
        type: 'select',
        val: 'sin',
        options: [
          { v: 'sin', label: 'sin x (about 0)' },
          { v: 'exp', label: 'eˣ (about 0)' },
          { v: 'ln', label: 'ln(1+x) (about 0)' }
        ]
      },
      { k: 'deg', label: 'degree n', min: 1, max: 11, step: 2, val: 3, decimals: 0 },
      { k: 'x', label: 'x', min: 0.1, max: 3, step: 0.05, val: 1.5, decimals: 2 }
    ],
    readout(s) {
      const n = Math.round(s.deg);
      const exact = s.fn === 'sin' ? Math.sin(s.x) : s.fn === 'exp' ? Math.exp(s.x) : Math.log(1 + s.x);
      let poly = 0;
      for (let k = 0; k <= n; k++) poly += taylorCoeff(s.fn, k) * Math.pow(s.x, k);
      return [
        ['Pₙ(x)', fmt(poly, 4)],
        ['f(x)', fmt(exact, 4)],
        ['error', fmt(Math.abs(exact - poly), 4)],
        ['degree', String(n)]
      ];
    },
    note(s) {
      return s.x > 2
        ? 'Far from the centre the polynomial drifts away no matter how many terms you add; near the centre each extra term buys a bit more accuracy.'
        : 'Every added term is chosen so the derivatives at 0 match. That is why the polynomial hugs the curve at the centre before diverging.';
    },
    draw(ctx, s, box) {
      const p = plot(ctx, box, { xmin: -0.2, xmax: 3.2, ymin: -2, ymax: 4, ticks: 4, xlabel: 'x' });
      const exact = s.fn === 'sin' ? Math.sin : s.fn === 'exp' ? Math.exp : (x) => Math.log(1 + x);
      const n = Math.round(s.deg);
      const poly = (x) => {
        let sum = 0;
        for (let k = 0; k <= n; k++) sum += taylorCoeff(s.fn, k) * Math.pow(x, k);
        return sum;
      };
      curve(ctx, p, exact, PALETTE.ink, 2.4, -0.2, 3.2, 300);
      curve(ctx, p, poly, PALETTE.accent, 2.2, -0.2, 3.2, 300);
      dot(ctx, p.X(s.x), p.clipY(exact(s.x)), 4, PALETTE.green);
      label(ctx, 'f', p.X(2.6), p.clipY(exact(2.6)) - 8, PALETTE.ink, 10);
      label(ctx, 'Pₙ', p.X(2.6), p.clipY(poly(2.6)) + 12, PALETTE.accent, 10);
    }
  });

  /* U7 — polar area swept from the pole */
  window.CourseSims.register('apcalcbc-u7-polar-area', {
    title: 'Polar area: sweep the ray and add the slivers',
    blurb:
      'A polar curve is traced by a rotating ray. Each thin wedge has area ½r²Δθ, so the region inside r = cos(kθ) is one petal at a time — rotate the ray and watch the area accumulate.',
    params: [
      { k: 'k', label: 'petal count k', min: 2, max: 5, step: 1, val: 3, decimals: 0 },
      { k: 'theta', label: 'sweep θ (deg)', min: 0, max: 180, step: 2, val: 90, decimals: 0 }
    ],
    readout(s) {
      const th = (s.theta * Math.PI) / 180;
      let area = 0;
      const steps = 180;
      for (let i = 0; i < steps; i++) {
        const t = (th * i) / steps;
        area += 0.5 * Math.pow(Math.cos(s.k * t), 2) * (th / steps);
      }
      const full = s.k % 2 === 1 ? Math.PI / 4 : Math.PI / 2;
      return [
        ['swept area', fmt(area, 4)],
        ['full region', fmt(full, 4)],
        ['fraction', fmt(area / full, 3)],
        ['r at θ', fmt(Math.cos(s.k * th), 3)]
      ];
    },
    note(s) {
      return s.theta > 179
        ? 'A full sweep of cos(3θ) covers the same region three times; polar area integrals are usually set up over one period of the curve, not 0 to 2π.'
        : 'The wedge area uses r², not r — doubling the radius quadruples the area, which is why the integrand is ½r².';
    },
    draw(ctx, s, box) {
      const cx = box.x + box.w / 2;
      const cy = box.y + box.h / 2 + 6;
      const R = Math.min(box.w, box.h) * 0.42;
      const p = { X: (v) => cx + v * R, Y: (v) => cy - v * R };

      ctx.strokeStyle = '#efe6da';
      ctx.lineWidth = 1;
      for (let i = 1; i <= 4; i++) {
        ctx.beginPath();
        ctx.arc(cx, cy, (R * i) / 4, 0, Math.PI * 2);
        ctx.stroke();
      }
      ctx.beginPath();
      ctx.moveTo(cx - R, cy);
      ctx.lineTo(cx + R, cy);
      ctx.moveTo(cx, cy - R);
      ctx.lineTo(cx, cy + R);
      ctx.stroke();

      const th = (s.theta * Math.PI) / 180;
      ctx.fillStyle = 'rgba(37,99,235,0.16)';
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      for (let i = 0; i <= 120; i++) {
        const t = (th * i) / 120;
        const r = Math.cos(s.k * t);
        ctx.lineTo(p.X(r * Math.cos(t)), p.Y(r * Math.sin(t)));
      }
      ctx.closePath();
      ctx.fill();

      ctx.strokeStyle = PALETTE.blue;
      ctx.lineWidth = 2.2;
      ctx.beginPath();
      for (let i = 0; i <= 720; i++) {
        const t = (i / 720) * Math.PI * 2;
        const r = Math.cos(s.k * t);
        const px = p.X(r * Math.cos(t));
        const py = p.Y(r * Math.sin(t));
        if (i === 0) ctx.moveTo(px, py);
        else ctx.lineTo(px, py);
      }
      ctx.stroke();

      const rNow = Math.cos(s.k * th);
      arrow(ctx, cx, cy, p.X(rNow * Math.cos(th)), p.Y(rNow * Math.sin(th)), PALETTE.accent, 2);
      dot(ctx, cx, cy, 3, PALETTE.ink);
      label(ctx, 'θ', cx + 18, cy - 10, PALETTE.soft, 10);
    }
  });

  /* U8 — logistic differential equation and its carrying capacity */
  window.CourseSims.register('apcalcbc-u8-logistic', {
    title: 'Logistic growth: the rate depends on the population',
    blurb:
      'dP/dt = rP(1 − P/K) starts exponential and bends over as P approaches K. Raise r and the curve steepens; change K and it levels somewhere else.',
    params: [
      { k: 'r', label: 'growth rate r', min: 0.1, max: 1.2, step: 0.05, val: 0.6, decimals: 2 },
      { k: 'K', label: 'carrying capacity K', min: 2, max: 20, step: 0.5, val: 10, decimals: 1 },
      { k: 'P0', label: 'initial P₀', min: 0.2, max: 12, step: 0.2, val: 1, decimals: 1 }
    ],
    readout(s) {
      const rate = s.r * s.P0 * (1 - s.P0 / s.K);
      const P5 = solveLogistic(s, 8);
      return [
        ['dP/dt at P₀', fmt(rate, 3)],
        ['P(8) predicted', fmt(P5, 3)],
        ['K', fmt(s.K, 1)],
        ['max rate at', fmt(s.K / 2, 1)]
      ];
    },
    note(s) {
      return s.P0 > s.K / 2
        ? 'Above K/2 the growth rate is already slowing: dP/dt peaks at P = K/2 and falls to zero at K.'
        : 'Below K/2 the population grows almost exponentially; as it passes K/2 the (1 − P/K) factor starts to bite.';
    },
    draw(ctx, s, box) {
      const p = plot(ctx, box, { xmin: 0, xmax: 8, ymin: 0, ymax: Math.max(4, s.K * 1.25), ticks: 4, xdigits: 0, xlabel: 't' });

      // slope field: short segments for dP/dt
      for (let i = 0; i <= 12; i++) {
        for (let j = 0; j <= 8; j++) {
          const t = (i / 12) * 8;
          const P = (j / 8) * (s.K * 1.2);
          const m = s.r * P * (1 - P / s.K);
          const px = p.X(t);
          const py = p.Y(P);
          const ang = Math.atan(clamp(m, -6, 6) * 0.25);
          ctx.strokeStyle = 'rgba(120,113,108,0.3)';
          ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.moveTo(px - Math.cos(ang) * 6, py - Math.sin(ang) * 6);
          ctx.lineTo(px + Math.cos(ang) * 6, py + Math.sin(ang) * 6);
          ctx.stroke();
        }
      }

      ctx.strokeStyle = PALETTE.accent;
      ctx.lineWidth = 2.4;
      ctx.beginPath();
      for (let i = 0; i <= 200; i++) {
        const t = (i / 200) * 8;
        const P = solveLogistic(s, t);
        const px = p.X(t);
        const py = p.Y(P);
        if (i === 0) ctx.moveTo(px, py);
        else ctx.lineTo(px, py);
      }
      ctx.stroke();

      ctx.save();
      ctx.setLineDash([5, 4]);
      ctx.strokeStyle = PALETTE.green;
      ctx.beginPath();
      ctx.moveTo(p.x0, p.Y(s.K));
      ctx.lineTo(p.x0 + p.w, p.Y(s.K));
      ctx.stroke();
      ctx.restore();
      label(ctx, 'K', p.x0 + p.w - 8, p.Y(s.K) - 6, PALETTE.green, 10, 'right');
    }
  });

  function fact(n) {
    let r = 1;
    for (let i = 2; i <= n; i++) r *= i;
    return r;
  }

  /** Maclaurin coefficient of xᵏ for the three functions above. */
  function taylorCoeff(fn, k) {
    if (fn === 'exp') return 1 / fact(k);
    if (fn === 'sin') {
      if (k % 2 === 0) return 0;
      const sign = ((k - 1) / 2) % 2 === 0 ? 1 : -1;
      return sign / fact(k);
    }
    if (k === 0) return 0;
    if (k % 2 === 0) return 0;
    return (k % 4 === 1 ? 1 : -1) / k;
  }

  function solveLogistic(s, t) {
    const A = (s.K - s.P0) / s.P0;
    return s.K / (1 + A * Math.exp(-s.r * t));
  }
})();
