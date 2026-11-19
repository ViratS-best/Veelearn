/* ============================================================================
 * AP Chemistry — one simulation per unit, tied to that unit's sections.
 * ========================================================================== */
(function () {
  'use strict';
  const S = window.CourseSims && window.CourseSims.util;
  if (!S) return;
  const { plot, curve, arrow, dot, label, fmt, clamp, lerp, PALETTE } = S;

  /* U1 — electron configuration and periodic trends */
  window.CourseSims.register('apchem-u1-atomic', {
    title: 'Build the atom and watch the trends',
    blurb:
      'Add protons and the electrons fill in order: 1s, 2s, 2p, 3s, 3p, 4s. Watch the valence count reset at each new shell, which is exactly where the periodic trends turn around.',
    params: [{ k: 'z', label: 'atomic number Z', min: 1, max: 20, step: 1, val: 11, decimals: 0 }],
    readout(s) {
      const z = Math.round(s.z);
      return [
        ['configuration', configOf(z)],
        ['valence electrons', String(valenceOf(z))],
        ['shells used', String(shellsOf(z).length)],
        ['trend', z < 3 ? 'H/He: simple' : valenceOf(z) <= 2 ? 'metal side — low EN' : 'nonmetal side — high EN']
      ];
    },
    note(s) {
      const z = Math.round(s.z);
      if (z === 2 || z === 10 || z === 18) return 'A full outer shell: these are the noble gases, with almost no tendency to gain or lose electrons.';
      if (valenceOf(z) <= 2) return 'Few valence electrons: these atoms lose them easily, so atomic radius grows down a group and shrinks across a period as the nucleus pulls harder.';
      return 'More protons across a period pull the same shell in tighter, so radius falls and electronegativity rises even though the valence count is similar.';
    },
    draw(ctx, s, box) {
      const z = Math.round(s.z);
      const shells = shellsOf(z);
      const cx = box.x + box.w * 0.34;
      const cy = box.y + box.h / 2;
      const R = Math.min(box.w * 0.3, box.h * 0.42);

      dot(ctx, cx, cy, 15, '#dc2626', '#7f1d1d');
      label(ctx, String(z), cx, cy + 4, '#fff', 11);

      shells.forEach((count, i) => {
        const r = R * ((i + 1) / shells.length);
        ctx.strokeStyle = 'rgba(37,99,235,0.25)';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.arc(cx, cy, r, 0, Math.PI * 2);
        ctx.stroke();
        for (let e = 0; e < count; e++) {
          const ang = (e / count) * Math.PI * 2 - Math.PI / 2;
          dot(ctx, cx + Math.cos(ang) * r, cy + Math.sin(ang) * r, 3.2, '#2563eb');
        }
      });

      const tx = box.x + box.w * 0.62;
      label(ctx, 'orbitals', tx, box.y + 16, PALETTE.soft, 10, 'left');
      ctx.font = '12px ui-monospace, monospace';
      ctx.fillStyle = PALETTE.ink;
      const cfg = configOf(z).split(' ');
      cfg.forEach((part, i) => ctx.fillText(part, tx + (i % 4) * 46, box.y + 42 + Math.floor(i / 4) * 22));
      label(ctx, 'valence ' + valenceOf(z) + ' e⁻', tx, box.y + box.h - 16, PALETTE.accent, 11, 'left');
    }
  });

  /* U2 — electronegativity difference decides the bond */
  window.CourseSims.register('apchem-u2-bonding', {
    title: 'How unequal sharing becomes an ionic bond',
    blurb:
      'Slide the electronegativity difference. Small differences share electrons almost evenly; large ones transfer them outright. The arrow shows where the electron density actually sits.',
    params: [{ k: 'den', label: 'ΔEN', min: 0, max: 3.2, step: 0.05, val: 1.2, decimals: 2 }],
    readout(s) {
      const type = s.den < 0.4 ? 'nonpolar covalent' : s.den < 1.7 ? 'polar covalent' : 'ionic';
      const ionic = (1 - Math.exp(-0.25 * s.den * s.den)) * 100;
      return [
        ['bond type', type],
        ['% ionic character', fmt(ionic, 0) + '%'],
        ['dipole', s.den < 0.4 ? 'negligible' : s.den < 1.7 ? 'present (δ+ / δ−)' : 'full charge transfer'],
        ['example', s.den < 0.4 ? 'C–C, C–H' : s.den < 1.7 ? 'O–H, C–Cl' : 'NaCl, MgO']
      ];
    },
    note(s) {
      return s.den < 1.7
        ? 'The bond is a continuum, not two categories: even a polar covalent bond keeps shared electrons in a molecular orbital, just unequally.'
        : 'Past ΔEN ≈ 1.7 the energy gained by transferring an electron outweighs the cost of separating the charges, so the lattice becomes ionic.';
    },
    draw(ctx, s, box) {
      const cy = box.y + box.h * 0.45;
      const left = box.x + box.w * 0.28;
      const right = box.x + box.w * 0.72;
      const shift = clamp(s.den / 3.2, 0, 1) * 26;

      dot(ctx, left, cy, 26, '#93c5fd', '#1e3a8a');
      dot(ctx, right, cy, 26, '#fca5a5', '#7f1d1d');
      label(ctx, 'A', left, cy + 5, '#1e3a8a', 14);
      label(ctx, 'B', right, cy + 5, '#7f1d1d', 14);
      label(ctx, 'less electronegative', left, cy + 46, PALETTE.soft, 10);
      label(ctx, 'more electronegative', right, cy + 46, PALETTE.soft, 10);

      // shared electron cloud drifting toward B
      dot(ctx, (left + right) / 2 + shift, cy, 7, '#1f2937');
      arrow(ctx, (left + right) / 2, cy - 34, (left + right) / 2 + shift, cy - 34, PALETTE.accent, 2);

      label(ctx, 'δ+', left + 18, cy - 34, PALETTE.blue, 11);
      label(ctx, 'δ' + (s.den < 0.4 ? '−' : '−'), right - 18, cy - 34, PALETTE.red, 11);
      if (s.den > 1.7) {
        label(ctx, 'e⁻ transferred', right, box.y + box.h - 6, PALETTE.red, 10);
      }
    }
  });

  /* U3 — intermolecular forces and boiling point */
  window.CourseSims.register('apchem-u3-imf', {
    title: 'Which force has to be broken to boil?',
    blurb:
      'Pick the strongest force a molecule can make and its size. Boiling means pulling molecules apart, so stronger forces and larger electron clouds both push the boiling point up.',
    params: [
      {
        k: 'imf',
        label: 'strongest IMF',
        type: 'select',
        val: 'dipole',
        options: [
          { v: 'london', label: 'London dispersion' },
          { v: 'dipole', label: 'Dipole–dipole' },
          { v: 'hbond', label: 'Hydrogen bonding' }
        ]
      },
      { k: 'mass', label: 'molar mass (g/mol)', min: 16, max: 180, step: 2, val: 46, decimals: 0 }
    ],
    readout(s) {
      const bonus = s.imf === 'hbond' ? 80 : s.imf === 'dipole' ? 32 : 0;
      const bp = Math.round(-120 + s.mass * 0.9 + bonus);
      return [
        ['estimated boiling point', bp + ' °C'],
        ['dominant force', s.imf === 'hbond' ? 'H-bond' : s.imf === 'dipole' ? 'dipole–dipole' : 'dispersion'],
        ['relative strength', s.imf === 'hbond' ? 'strongest' : s.imf === 'dipole' ? 'moderate' : 'weakest'],
        ['vapour pressure', bp < 0 ? 'very high at 25 °C' : bp < 80 ? 'moderate' : 'low']
      ];
    },
    note(s) {
      if (s.imf === 'hbond') return 'Hydrogen bonding needs H attached to N, O or F. It is why water boils at 100 °C while H₂S, a heavier molecule, boils at −60 °C.';
      if (s.imf === 'dipole') return 'Permanent dipoles line up, but the attraction is weaker than a hydrogen bond — just stronger than transient London forces of the same size.';
      return 'London forces exist in everything and grow with the number of electrons, which is why heavier noble gases boil at higher temperatures.';
    },
    draw(ctx, s, box) {
      const p = plot(ctx, box, { xmin: 0, xmax: 180, ymin: -140, ymax: 260, ticks: 4, xdigits: 0, ydigits: 0, xlabel: 'molar mass', ylabel: 'bp (°C)' });
      const lineFor = (imf) => (m) => -120 + m * 0.9 + (imf === 'hbond' ? 80 : imf === 'dipole' ? 32 : 0);
      curve(ctx, p, lineFor('london'), 'rgba(120,113,108,0.45)', 1.8, 16, 180, 80);
      curve(ctx, p, lineFor('dipole'), 'rgba(37,99,235,0.55)', 1.8, 16, 180, 80);
      curve(ctx, p, lineFor('hbond'), 'rgba(5,150,105,0.7)', 2, 16, 180, 80);
      const bp = -120 + s.mass * 0.9 + (s.imf === 'hbond' ? 80 : s.imf === 'dipole' ? 32 : 0);
      dot(ctx, p.X(s.mass), p.Y(bp), 4.5, PALETTE.accent);
      label(ctx, 'your molecule', p.X(s.mass) + 8, p.Y(bp) - 8, PALETTE.accent, 10, 'left');
      label(ctx, 'London', p.X(150), p.Y(lineFor('london')(150)) - 8, PALETTE.soft, 9, 'left');
      label(ctx, 'dipole', p.X(150), p.Y(lineFor('dipole')(150)) - 8, PALETTE.blue, 9, 'left');
      label(ctx, 'H-bond', p.X(150), p.Y(lineFor('hbond')(150)) - 8, PALETTE.green, 9, 'left');
    }
  });

  /* U4 — limiting reactant with particle counts */
  window.CourseSims.register('apchem-u4-limiting', {
    title: '2 A + B → 3 C: which reactant runs out?',
    blurb:
      'Set how many A and B particles you have. The reaction needs two A for every B, so the limiting reactant is whichever runs out first — and the leftover is what cannot react.',
    params: [
      { k: 'a', label: 'moles of A', min: 0, max: 12, step: 0.5, val: 7, decimals: 1 },
      { k: 'b', label: 'moles of B', min: 0, max: 8, step: 0.5, val: 2, decimals: 1 }
    ],
    readout(s) {
      const byA = s.a / 2;
      const byB = s.b;
      const lim = Math.min(byA, byB);
      const product = 3 * lim;
      const leftA = s.a - 2 * lim;
      const leftB = s.b - lim;
      return [
        ['limiting reactant', byA < byB ? 'A' : byB < byA ? 'B' : 'neither — stoich ratio'],
        ['moles of C', fmt(product, 2)],
        ['A left over', fmt(leftA, 2)],
        ['B left over', fmt(leftB, 2)]
      ];
    },
    note(s) {
      const byA = s.a / 2;
      const byB = s.b;
      if (Math.abs(byA - byB) < 0.01) return 'Exactly stoichiometric: both reactants are consumed completely, so no leftover remains.';
      return byA < byB
        ? 'A is limiting: there is not enough A to pair with all of B, so some B is left unreacted no matter what you do.'
        : 'B is limiting: extra A cannot help, because every B can only consume two A.';
    },
    draw(ctx, s, box) {
      const byA = s.a / 2;
      const lim = Math.min(byA, s.b);
      const remainingA = Math.max(0, s.a - 2 * lim);
      const remainingB = Math.max(0, s.b - lim);
      const product = 3 * lim;

      const groups = [
        ['A', remainingA, PALETTE.blue, 1],
        ['B', remainingB, PALETTE.amber, 1],
        ['C', product, PALETTE.green, 1]
      ];
      const colW = box.w / 3;
      groups.forEach(([name, count, color], i) => {
        const cx = box.x + colW * i + colW / 2;
        label(ctx, name, cx, box.y + 18, color, 13);
        const n = Math.min(30, Math.round(count));
        for (let k = 0; k < n; k++) {
          const x = cx - 54 + (k % 6) * 20;
          const y = box.y + 46 + Math.floor(k / 6) * 20;
          dot(ctx, x, y, 6, color);
        }
        label(ctx, fmt(count, 1) + ' mol', cx, box.y + box.h - 10, PALETTE.soft, 11);
      });
      label(ctx, '2 A + B → 3 C', box.x + box.w / 2, box.y + box.h - 30, PALETTE.ink, 12);
    }
  });

  /* U5 — rate law order changes the shape of the decay */
  window.CourseSims.register('apchem-u5-kinetics', {
    title: 'Reaction order changes the whole curve',
    blurb:
      'Zero, first and second order all start at the same concentration but decay differently. Switch the order and watch the half-life: constant for first order, growing for second, shrinking for zero.',
    params: [
      {
        k: 'order',
        label: 'order in A',
        type: 'select',
        val: '1',
        options: [
          { v: '0', label: 'zero order' },
          { v: '1', label: 'first order' },
          { v: '2', label: 'second order' }
        ]
      },
      { k: 'k', label: 'rate constant k', min: 0.05, max: 0.6, step: 0.01, val: 0.2, decimals: 2 },
      { k: 'a0', label: '[A]₀', min: 0.2, max: 2, step: 0.05, val: 1, decimals: 2 }
    ],
    readout(s) {
      const n = Number(s.order);
      const conc = (t) => (n === 0 ? Math.max(0, s.a0 - s.k * t) : n === 1 ? s.a0 * Math.exp(-s.k * t) : s.a0 / (1 + s.k * s.a0 * t));
      const half = n === 0 ? s.a0 / (2 * s.k) : n === 1 ? Math.log(2) / s.k : 1 / (s.k * s.a0);
      return [
        ['[A] at t = 10', fmt(conc(10), 3)],
        ['half-life', fmt(half, 2) + ' s'],
        ['initial rate', fmt(s.k * Math.pow(s.a0, n), 3)],
        ['units of k', n === 0 ? 'M/s' : n === 1 ? '1/s' : '1/(M·s)']
      ];
    },
    note(s) {
      if (Number(s.order) === 1) return 'First order: each half-life removes the same fraction, so the half-life is constant and independent of [A]₀. That is the signature on a ln[A] vs t plot.';
      if (Number(s.order) === 2) return 'Second order: as [A] falls the rate falls faster, so each successive half-life is longer. A 1/[A] vs t plot is linear.';
      return 'Zero order: the rate does not depend on [A] at all, so concentration falls in a straight line until it runs out.';
    },
    draw(ctx, s, box) {
      const n = Number(s.order);
      const p = plot(ctx, box, { xmin: 0, xmax: 12, ymin: 0, ymax: 2.1, ticks: 4, xdigits: 0, ydigits: 1, xlabel: 'time (s)', ylabel: '[A]' });
      const conc = (t) => (n === 0 ? Math.max(0, s.a0 - s.k * t) : n === 1 ? s.a0 * Math.exp(-s.k * t) : s.a0 / (1 + s.k * s.a0 * t));
      curve(ctx, p, conc, PALETTE.blue, 2.6, 0, 12, 240);
      dot(ctx, p.X(10), p.Y(conc(10)), 4.5, PALETTE.accent);
      label(ctx, 't = 10', p.X(10) + 6, p.Y(conc(10)) - 8, PALETTE.accent, 10, 'left');
      label(ctx, 'order ' + s.order, p.x0 + 10, p.y0 + 18, PALETTE.soft, 11, 'left');
    }
  });

  /* U6 — energy profile: activation energy versus ΔH */
  window.CourseSims.register('apchem-u6-thermo', {
    title: 'Activation energy and ΔH are different numbers',
    blurb:
      'The peak height above the reactants is Ea; the gap between reactants and products is ΔH. A catalyst lowers the peak without touching ΔH — the thermodynamics stay the same, only the path changes.',
    params: [
      { k: 'ea', label: 'Ea (kJ/mol)', min: 20, max: 150, step: 5, val: 80, decimals: 0 },
      { k: 'dh', label: 'ΔH (kJ/mol)', min: -80, max: 40, step: 5, val: -40, decimals: 0 },
      {
        k: 'cat',
        label: 'catalyst',
        type: 'select',
        val: 'no',
        options: [
          { v: 'no', label: 'none' },
          { v: 'yes', label: 'present (−25 kJ/mol)' }
        ]
      }
    ],
    readout(s) {
      const ea = s.cat === 'yes' ? Math.max(5, s.ea - 25) : s.ea;
      const factor = Math.exp((s.ea - ea) / (0.008314 * 298));
      return [
        ['Ea', fmt(ea, 0) + ' kJ/mol'],
        ['ΔH', fmt(s.dh, 0) + ' kJ/mol'],
        ['reaction', s.dh < 0 ? 'exothermic' : s.dh > 0 ? 'endothermic' : 'thermoneutral'],
        ['rate multiplier', s.cat === 'yes' ? fmt(factor, 0) + '×' : '1×']
      ];
    },
    note(s) {
      return s.cat === 'yes'
        ? 'The catalyst provides a lower-energy path, so more collisions clear the barrier at the same temperature. ΔH is unchanged because the reactants and products are unchanged.'
        : 'Ea controls the rate; ΔH controls the energy released. A large negative ΔH does not make a reaction fast if the barrier is high.';
    },
    draw(ctx, s, box) {
      const ea = s.cat === 'yes' ? Math.max(5, s.ea - 25) : s.ea;
      const top = Math.max(ea, 0) + 20;
      const p = plot(ctx, box, { xmin: 0, xmax: 10, ymin: Math.min(-100, s.dh - 20), ymax: top + 20, ticks: 3, xlabels: false, ydigits: 0, ylabel: 'energy' });
      const y0 = 0;
      const yPeak = ea;
      const yProd = s.dh;

      const profile = (x) => {
        const x1 = 2.4;
        const x2 = 4.4;
        const x3 = 6.4;
        if (x < x1) return y0;
        if (x < x2) return y0 + (yPeak - y0) * smooth((x - x1) / (x2 - x1));
        if (x < x3) return yPeak + (yProd - yPeak) * smooth((x - x2) / (x3 - x2));
        return yProd;
      };
      curve(ctx, p, profile, PALETTE.ink, 2.6, 0, 10, 300);

      ctx.save();
      ctx.setLineDash([4, 4]);
      ctx.strokeStyle = PALETTE.soft;
      ctx.beginPath();
      ctx.moveTo(p.x0, p.Y(y0));
      ctx.lineTo(p.x0 + p.w, p.Y(y0));
      ctx.stroke();
      ctx.restore();

      arrow(ctx, p.X(1.2), p.Y(y0), p.X(1.2), p.Y(yPeak), PALETTE.red, 1.6);
      label(ctx, 'Ea', p.X(1.2) - 6, p.Y(yPeak / 2), PALETTE.red, 10, 'right');
      arrow(ctx, p.X(8.4), p.Y(y0), p.X(8.4), p.Y(yProd), PALETTE.blue, 1.6);
      label(ctx, 'ΔH', p.X(8.4) + 6, p.Y(yProd / 2), PALETTE.blue, 10, 'left');
      label(ctx, 'reactants', p.X(0.4), p.Y(y0) - 6, PALETTE.soft, 10, 'left');
      label(ctx, 'products', p.X(9.4), p.Y(yProd) - 6, PALETTE.soft, 10, 'right');
    }
  });

  /* U7 — equilibrium and Le Châtelier */
  window.CourseSims.register('apchem-u7-equilibrium', {
    title: 'K sets the ratio; a stress moves Q away from it',
    blurb:
      'For A ⇌ B, K fixes the ratio at equilibrium. Add more A and Q drops below K, so the system shifts forward until Q returns to K — that is Le Châtelier in one variable.',
    params: [
      { k: 'K', label: 'equilibrium constant K', min: 0.05, max: 20, step: 0.05, val: 2, decimals: 2 },
      { k: 'a0', label: 'initial A (M)', min: 0.2, max: 2, step: 0.05, val: 1, decimals: 2 },
      { k: 'stress', label: 'extra A added (M)', min: 0, max: 1, step: 0.05, val: 0, decimals: 2 }
    ],
    readout(s) {
      const A = s.a0 + s.stress;
      const x = (s.K * A) / (1 + s.K);
      const B = x;
      const Aeq = A - x;
      const Q = B / Aeq;
      return [
        ['[A] equilibrium', fmt(Aeq, 3)],
        ['[B] equilibrium', fmt(B, 3)],
        ['Q', fmt(Q, 2)],
        ['direction', Math.abs(Q - s.K) < 0.05 ? 'at equilibrium' : Q < s.K ? 'shifts forward' : 'shifts reverse']
      ];
    },
    note(s) {
      if (s.stress > 0.05) return 'Adding A lowers Q below K. The forward reaction speeds up until Q climbs back to K — the ratio is restored, not the original concentrations.';
      return 'K is a ratio, not a quantity. Doubling both concentrations can leave Q unchanged; only a change in the ratio moves the system.';
    },
    draw(ctx, s, box) {
      const A = s.a0 + s.stress;
      const x = (s.K * A) / (1 + s.K);
      const Aeq = A - x;
      const Beq = x;
      const max = Math.max(A, 1);
      const barW = box.w * 0.18;
      const base = box.y + box.h - 30;

      const bar = (cx, value, color, name) => {
        const h = (value / max) * (box.h - 70);
        ctx.fillStyle = color;
        ctx.fillRect(cx - barW / 2, base - h, barW, h);
        label(ctx, name, cx, base + 16, PALETTE.ink, 12);
        label(ctx, fmt(value, 2) + ' M', cx, base - h - 8, PALETTE.soft, 10);
      };
      bar(box.x + box.w * 0.3, Aeq, 'rgba(37,99,235,0.75)', 'A');
      bar(box.x + box.w * 0.62, Beq, 'rgba(5,150,105,0.75)', 'B');

      const Q = Beq / Aeq;
      const msg = Math.abs(Q - s.K) < 0.05 ? 'Q = K' : Q < s.K ? 'Q < K → forward' : 'Q > K → reverse';
      label(ctx, msg, box.x + box.w * 0.82, box.y + 24, PALETTE.accent, 12);
      label(ctx, 'K = ' + fmt(s.K, 2), box.x + box.w * 0.82, box.y + 44, PALETTE.soft, 11);
    }
  });

  /* U8 — weak-acid titration with a buffer region */
  window.CourseSims.register('apchem-u8-titration', {
    title: 'Titration: the buffer plateau and the equivalence cliff',
    blurb:
      'Titrate a weak acid with strong base. The pH rises slowly through the buffer region, then jumps at equivalence; the half-equivalence point sits exactly at pH = pKa.',
    params: [
      { k: 'pka', label: 'pKa of acid', min: 2, max: 7, step: 0.1, val: 4.8, decimals: 1 },
      { k: 'vol', label: 'NaOH added (mL)', min: 0, max: 50, step: 0.5, val: 12, decimals: 1 }
    ],
    readout(s) {
      const ph = pHAt(s.pka, s.vol);
      return [
        ['pH', fmt(ph, 2)],
        ['equivalence at', '25.0 mL'],
        ['half-equivalence', 'pH = pKa = ' + fmt(s.pka, 1)],
        ['region', s.vol < 22 ? 'buffer' : s.vol < 28 ? 'equivalence' : 'excess base']
      ];
    },
    note(s) {
      if (s.vol < 5) return 'Before any base is added the acid is only partly dissociated, so the starting pH is already above a strong acid of the same concentration.';
      if (Math.abs(s.vol - 12.5) < 1.5) return 'Half-equivalence: [HA] = [A⁻], so the Henderson–Hasselbalch ratio is 1 and pH = pKa. This is the flattest, most buffered part of the curve.';
      if (Math.abs(s.vol - 25) < 1) return 'At equivalence the acid is fully neutralised and the pH is set by the conjugate base, not by 7 — that is why the jump is not centred on neutral.';
      return 'Past equivalence the curve flattens again, now controlled by excess OH⁻.';
    },
    draw(ctx, s, box) {
      const p = plot(ctx, box, { xmin: 0, xmax: 50, ymin: 0, ymax: 14, ticks: 4, xdigits: 0, ydigits: 0, xlabel: 'NaOH added (mL)', ylabel: 'pH' });
      curve(ctx, p, (v) => pHAt(s.pka, v), PALETTE.blue, 2.4, 0, 50, 300);

      ctx.save();
      ctx.setLineDash([4, 4]);
      ctx.strokeStyle = PALETTE.soft;
      ctx.beginPath();
      ctx.moveTo(p.X(25), p.y0);
      ctx.lineTo(p.X(25), p.y0 + p.h);
      ctx.stroke();
      ctx.restore();
      label(ctx, 'equivalence', p.X(25), p.y0 + 14, PALETTE.soft, 10);

      dot(ctx, p.X(s.vol), p.Y(pHAt(s.pka, s.vol)), 4.5, PALETTE.accent);
      label(ctx, 'pH ' + fmt(pHAt(s.pka, s.vol), 1), p.X(s.vol) + 8, p.Y(pHAt(s.pka, s.vol)) - 8, PALETTE.accent, 10, 'left');
    }
  });

  /* ---- helpers ---- */

  function smooth(t) {
    const x = clamp(t, 0, 1);
    return x * x * (3 - 2 * x);
  }

  function shellsOf(z) {
    const capacity = [2, 8, 8, 2];
    const shells = [];
    let left = z;
    for (const cap of capacity) {
      if (left <= 0) break;
      const take = Math.min(cap, left);
      shells.push(take);
      left -= take;
    }
    return shells;
  }

  function valenceOf(z) {
    const s = shellsOf(z);
    return s[s.length - 1] || 0;
  }

  function configOf(z) {
    const order = [
      ['1s', 2],
      ['2s', 2],
      ['2p', 6],
      ['3s', 2],
      ['3p', 6],
      ['4s', 2]
    ];
    let left = z;
    const parts = [];
    for (const [name, cap] of order) {
      if (left <= 0) break;
      const take = Math.min(cap, left);
      parts.push(name + take);
      left -= take;
    }
    return parts.join(' ');
  }

  function pHAt(pka, v) {
    const ka = Math.pow(10, -pka);
    const cAcid = 0.1;
    const cBase = 0.1;
    const vAcid = 25;
    const molesAcid = cAcid * vAcid;
    const molesBase = cBase * v;
    const total = vAcid + v;
    if (v < 25) {
      const ha = molesAcid - molesBase;
      const a = molesBase;
      if (a <= 1e-6) return -Math.log10(Math.sqrt(ka * cAcid));
      return pka + Math.log10(a / ha);
    }
    if (Math.abs(v - 25) < 0.3) {
      const concA = molesAcid / total;
      const kb = 1e-14 / ka;
      const oh = Math.sqrt(kb * concA);
      return 14 + Math.log10(oh);
    }
    const excess = molesBase - molesAcid;
    return 14 + Math.log10(excess / total);
  }
})();
