/* ============================================================================
 * AP Biology — one simulation per unit, tied to that unit's sections.
 * ========================================================================== */
(function () {
  'use strict';
  const S = window.CourseSims && window.CourseSims.util;
  if (!S) return;
  const { plot, curve, arrow, dot, label, fmt, clamp, lerp, PALETTE } = S;

  /* U1 — water: hydrogen bonds versus thermal energy */
  window.CourseSims.register('apbio-u1-water', {
    title: 'Hydrogen bonds: strong together, weak alone',
    blurb:
      'Each water can hydrogen-bond to four neighbours. Add thermal energy and those bonds break and re-form faster; below freezing they lock into a lattice, which is why ice floats.',
    params: [{ k: 'temp', label: 'temperature (°C)', min: -10, max: 110, step: 1, val: 25, decimals: 0 }],
    readout(s) {
      const bonds = s.temp < 0 ? 4 : s.temp < 40 ? 3.6 : s.temp < 70 ? 2.8 : s.temp < 100 ? 1.9 : 1.1;
      const state = s.temp < 0 ? 'solid (lattice)' : s.temp < 100 ? 'liquid' : 'gas';
      return [
        ['H-bonds / molecule', fmt(bonds, 1)],
        ['state', state],
        ['density', s.temp < 0 ? 'lower than liquid' : s.temp < 100 ? '≈ 1.00 g/mL' : 'very low'],
        ['behaviour', s.temp < 0 ? 'ordered, expanded' : s.temp < 100 ? 'cohesive, flowing' : 'bonds broken']
      ];
    },
    note(s) {
      if (s.temp < 0) return 'In ice every molecule is locked to four neighbours in an open lattice. The gaps make ice less dense than liquid water, so it floats and insulates the water below.';
      if (s.temp >= 100) return 'Above boiling, thermal energy exceeds the hydrogen-bond energy: molecules escape the liquid instead of pulling each other back.';
      return 'Cohesion (water to water) and adhesion (water to a surface) both come from these bonds, which is why water climbs narrow tubes and beads into droplets.';
    },
    draw(ctx, s, box) {
      const p = plot(ctx, box, { xmin: 0, xmax: 10, ymin: 0, ymax: 6, ticks: 0, xlabels: false, ylabels: false, background: '#fdfaf5' });
      const bonds = clamp((s.temp < 0 ? 4 : s.temp < 40 ? 3.6 : s.temp < 70 ? 2.8 : s.temp < 100 ? 1.9 : 1.1) / 4, 0.2, 1);
      const spread = s.temp > 100 ? 1.5 : s.temp < 0 ? 0.72 : 1;

      const mols = [
        [2.6, 3.2],
        [5.0, 3.4],
        [7.4, 3.0],
        [3.8, 1.6],
        [6.3, 1.4]
      ];
      const pts = mols.map(([x, y], i) => [p.X(5 + (x - 5) * spread), p.Y(3 + (y - 3) * spread + Math.sin(i) * (1 - bonds) * 0.3)]);

      // hydrogen bonds between neighbours, fading as temperature rises
      ctx.save();
      ctx.setLineDash([5, 5]);
      for (let i = 0; i < pts.length; i++) {
        for (let j = i + 1; j < pts.length; j++) {
          const d = Math.hypot(pts[i][0] - pts[j][0], pts[i][1] - pts[j][1]);
          if (d < 120) {
            ctx.strokeStyle = 'rgba(37,99,235,' + (0.12 + bonds * 0.45) + ')';
            ctx.lineWidth = 1.6;
            ctx.beginPath();
            ctx.moveTo(pts[i][0], pts[i][1]);
            ctx.lineTo(pts[j][0], pts[j][1]);
            ctx.stroke();
          }
        }
      }
      ctx.restore();

      pts.forEach(([x, y]) => {
        dot(ctx, x, y, 15, '#ef4444', '#7f1d1d');
        dot(ctx, x - 12, y - 10, 7, '#93c5fd', '#1e3a8a');
        dot(ctx, x + 12, y - 10, 7, '#93c5fd', '#1e3a8a');
        label(ctx, 'O', x, y + 4, '#fff', 11);
      });

      label(ctx, s.temp < 0 ? 'ordered lattice — open gaps' : s.temp >= 100 ? 'bonds broken — molecules escape' : 'bonds constantly breaking and re-forming', box.x + box.w / 2, box.y + box.h - 8, PALETTE.soft, 11);
      label(ctx, 'δ+ H attracts δ− O of a neighbour', box.x + 12, box.y + 16, PALETTE.blue, 10, 'left');
    }
  });

  /* U2 — membrane transport and tonicity */
  window.CourseSims.register('apbio-u2-transport', {
    title: 'Which way will water and solutes move?',
    blurb:
      'Set the solute concentration on each side of the membrane. Passive transport follows the gradient; active transport can push against it, but only if ATP is available.',
    params: [
      { k: 'outside', label: 'outside solute', min: 0, max: 1, step: 0.02, val: 0.8, decimals: 2 },
      { k: 'inside', label: 'inside solute', min: 0, max: 1, step: 0.02, val: 0.3, decimals: 2 },
      {
        k: 'mode',
        label: 'transport',
        type: 'select',
        val: 'passive',
        options: [
          { v: 'passive', label: 'Passive (diffusion)' },
          { v: 'active', label: 'Active (ATP)' }
        ]
      }
    ],
    readout(s) {
      const diff = s.outside - s.inside;
      const direction = Math.abs(diff) < 0.02 ? 'at equilibrium' : diff > 0 ? 'inward' : 'outward';
      const tonicity = s.outside > s.inside ? 'hypertonic outside' : s.outside < s.inside ? 'hypotonic outside' : 'isotonic';
      return [
        ['solute gradient', fmt(diff, 2)],
        ['net solute flux', direction],
        ['water moves', s.outside > s.inside ? 'out of the cell' : s.outside < s.inside ? 'into the cell' : 'both ways equally'],
        ['solution', tonicity]
      ];
    },
    note(s) {
      if (s.mode === 'active') return 'Active transport hydrolyses ATP to move solute against its gradient, which is why the flux can reverse while the gradient stays the same.';
      return 'Passive transport needs no ATP: solutes move down their gradient, and water follows osmotically. A cell in a hypertonic solution loses water and shrinks.';
    },
    draw(ctx, s, box) {
      const midY = box.y + box.h / 2;
      const leftW = box.w * 0.46;
      ctx.fillStyle = '#e0f2fe';
      ctx.fillRect(box.x, box.y, leftW, box.h);
      ctx.fillStyle = '#fef3c7';
      ctx.fillRect(box.x + leftW + 26, box.y, box.w - leftW - 26, box.h);

      // membrane with channels
      ctx.fillStyle = '#f5d0a9';
      ctx.fillRect(box.x + leftW, box.y, 26, box.h);
      ctx.fillStyle = '#c98b5a';
      [0.25, 0.5, 0.75].forEach((f) => {
        ctx.beginPath();
        ctx.ellipse(box.x + leftW + 13, box.y + box.h * f, 8, 20, 0, 0, Math.PI * 2);
        ctx.fill();
      });

      const count = (v) => Math.round(v * 26);
      for (let i = 0; i < count(s.outside); i++) {
        const x = box.x + 14 + (i % 7) * 26;
        const y = box.y + 24 + Math.floor(i / 7) * 30;
        dot(ctx, x, y, 6, '#2563eb');
      }
      for (let i = 0; i < count(s.inside); i++) {
        const x = box.x + leftW + 48 + (i % 7) * 26;
        const y = box.y + 24 + Math.floor(i / 7) * 30;
        dot(ctx, x, y, 6, '#2563eb');
      }

      const diff = s.outside - s.inside;
      if (Math.abs(diff) > 0.02) {
        const inward = diff > 0;
        const y = midY;
        const x1 = inward ? box.x + leftW - 20 : box.x + leftW + 46;
        const x2 = inward ? box.x + leftW + 46 : box.x + leftW - 20;
        arrow(ctx, x1, y, x2, y, s.mode === 'active' ? PALETTE.red : PALETTE.green, 3);
        label(ctx, s.mode === 'active' ? 'ATP-driven' : 'down the gradient', (x1 + x2) / 2, y - 10, s.mode === 'active' ? PALETTE.red : PALETTE.green, 10);
      }

      label(ctx, 'outside', box.x + 10, box.y + 14, PALETTE.soft, 10, 'left');
      label(ctx, 'inside', box.x + leftW + 36, box.y + 14, PALETTE.soft, 10, 'left');
      label(ctx, 'membrane', box.x + leftW + 13, box.y + box.h - 8, '#8a5a34', 10);
    }
  });

  /* U3 — enzymes: saturation and denaturation */
  window.CourseSims.register('apbio-u3-enzyme', {
    title: 'Enzyme rate: saturation, then denaturation',
    blurb:
      'At first more substrate means more collisions and a faster rate, until every active site is occupied. Temperature adds a second effect: past the optimum the enzyme unfolds and the rate collapses.',
    params: [
      { k: 's', label: 'substrate [S]', min: 0, max: 10, step: 0.1, val: 3, decimals: 1 },
      { k: 'temp', label: 'temperature (°C)', min: 0, max: 80, step: 1, val: 37, decimals: 0 }
    ],
    readout(s) {
      const denature = s.temp <= 37 ? 1 : Math.max(0.05, 1 - (s.temp - 37) / 30);
      const cold = s.temp < 10 ? 0.35 : 1;
      const vmax = 100 * denature * cold;
      const v = (vmax * s.s) / (2 + s.s);
      return [
        ['rate v', fmt(v, 1)],
        ['Vmax (at this temp)', fmt(vmax, 0)],
        ['active sites used', fmt(Math.min(1, s.s / (2 + s.s)) * 100, 0) + '%'],
        ['state', s.temp > 45 ? 'denaturing' : s.temp < 10 ? 'too cold' : 'optimal range']
      ];
    },
    note(s) {
      if (s.temp > 50) return 'The active site has lost its shape: adding more substrate cannot help, because the substrate no longer fits. Denaturation is not reversible here.';
      if (s.s > 8) return 'All active sites are occupied, so the rate has plateaued at Vmax. The enzyme is saturated — the limiting factor is enzyme, not substrate.';
      return 'The curve is a rectangular hyperbola: half of Vmax occurs at [S] = Km, a measure of how tightly the enzyme binds its substrate.';
    },
    draw(ctx, s, box) {
      const plotW = box.w * 0.58;
      const p = plot(ctx, { x: box.x, y: box.y, w: plotW, h: box.h }, { xmin: 0, xmax: 10, ymin: 0, ymax: 110, ticks: 4, xdigits: 0, ydigits: 0, xlabel: '[S]' });
      const denature = s.temp <= 37 ? 1 : Math.max(0.05, 1 - (s.temp - 37) / 30);
      const cold = s.temp < 10 ? 0.35 : 1;
      const vmax = 100 * denature * cold;
      curve(ctx, p, (x) => (vmax * x) / (2 + x), PALETTE.blue, 2.4, 0, 10, 200);
      const v = (vmax * s.s) / (2 + s.s);
      dot(ctx, p.X(s.s), p.clampY === undefined ? p.Y(v) : p.Y(v), 4.5, PALETTE.accent);
      label(ctx, 'v = ' + fmt(v, 0), p.X(s.s) + 8, p.Y(v) - 8, PALETTE.accent, 10, 'left');

      // active-site occupancy animation
      const cx = box.x + plotW + 34;
      const cy = box.y + box.h * 0.45;
      label(ctx, 'active sites', cx + 10, box.y + 16, PALETTE.ink, 11, 'left');
      const occupied = Math.min(6, Math.round((s.s / (2 + s.s)) * 6));
      for (let i = 0; i < 6; i++) {
        const x = cx + 18 + (i % 3) * 46;
        const y = cy + Math.floor(i / 3) * 52;
        ctx.fillStyle = '#fde68a';
        ctx.strokeStyle = '#b45309';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.arc(x, y, 17, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
        if (i < occupied) dot(ctx, x, y, 7, '#2563eb');
      }
      label(ctx, s.temp > 45 ? 'shape lost' : occupied + '/6 occupied', cx + 10, cy + 128, s.temp > 45 ? PALETTE.red : PALETTE.soft, 10, 'left');
    }
  });

  /* U4 — mitosis: chromosomes through the phases */
  window.CourseSims.register('apbio-u4-mitosis', {
    title: 'Mitosis: follow two chromosomes through the cycle',
    blurb:
      'Step through the phases. The chromosome number stays constant; what changes is how the DNA is packaged, aligned, and pulled apart.',
    params: [{ k: 'phase', label: 'phase', min: 0, max: 4, step: 1, val: 1, decimals: 0 }],
    readout(s) {
      const names = ['Interphase', 'Prophase', 'Metaphase', 'Anaphase', 'Telophase / cytokinesis'];
      return [
        ['phase', names[Math.round(s.phase)]],
        ['chromosomes', '4 (2 pairs)'],
        ['sister chromatids', s.phase < 3 ? '4' : '0 (separated)'],
        ['DNA copies', s.phase <= 1 ? 'replicated' : 'one per pole']
      ];
    },
    note(s) {
      const n = Math.round(s.phase);
      if (n === 2) return 'At metaphase the chromosomes line up on the equator — this is the checkpoint where the spindle verifies every chromosome is attached.';
      if (n === 3) return 'Sister chromatids are pulled to opposite poles. Each pole still gets one copy of every chromosome, so the daughter cells are genetically identical.';
      if (n === 0) return 'DNA replicates during S phase, so each chromosome enters mitosis as two identical sister chromatids.';
      return 'The nuclear envelope breaks down and the spindle forms. Chromosomes condense so they can be moved without tangling.';
    },
    draw(ctx, s, box) {
      const cx = box.x + box.w / 2;
      const cy = box.y + box.h / 2;
      const R = Math.min(box.w, box.h) * 0.4;
      const n = Math.round(s.phase);

      ctx.fillStyle = '#fdf2f8';
      ctx.strokeStyle = '#f0abfc';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(cx, cy, R, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      if (n >= 1 && n <= 3) {
        ctx.save();
        ctx.setLineDash([4, 4]);
        ctx.strokeStyle = '#c4b5fd';
        ctx.beginPath();
        ctx.arc(cx, cy, R * 0.78, 0, Math.PI * 2);
        ctx.stroke();
        ctx.restore();
      }

      const drawChrom = (x, y, angle, separated) => {
        ctx.save();
        ctx.translate(x, y);
        ctx.rotate(angle);
        ctx.fillStyle = '#7c3aed';
        if (separated) {
          ctx.fillRect(-3, -20, 6, 16);
          ctx.fillRect(-3, 4, 6, 16);
        } else {
          ctx.fillRect(-3, -20, 6, 40);
        }
        ctx.restore();
      };

      if (n === 0 || n === 1) {
        drawChrom(cx - R * 0.35, cy - R * 0.2, 0.2, false);
        drawChrom(cx + R * 0.35, cy - R * 0.2, -0.2, false);
        drawChrom(cx - R * 0.25, cy + R * 0.35, 0.5, false);
        drawChrom(cx + R * 0.25, cy + R * 0.35, -0.5, false);
      } else if (n === 2) {
        drawChrom(cx, cy - R * 0.3, 0, false);
        drawChrom(cx, cy + R * 0.15, 0, false);
        ctx.save();
        ctx.setLineDash([5, 4]);
        ctx.strokeStyle = '#a78bfa';
        ctx.beginPath();
        ctx.moveTo(cx - R * 0.75, cy);
        ctx.lineTo(cx + R * 0.75, cy);
        ctx.stroke();
        ctx.restore();
      } else if (n === 3) {
        drawChrom(cx - R * 0.45, cy - R * 0.3, 0.6, true);
        drawChrom(cx + R * 0.45, cy - R * 0.3, -0.6, true);
        drawChrom(cx - R * 0.45, cy + R * 0.3, -0.6, true);
        drawChrom(cx + R * 0.45, cy + R * 0.3, 0.6, true);
      } else {
        ctx.strokeStyle = '#f0abfc';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(cx, cy - R);
        ctx.lineTo(cx, cy + R);
        ctx.stroke();
        drawChrom(cx - R * 0.4, cy - R * 0.2, 0.3, false);
        drawChrom(cx + R * 0.4, cy - R * 0.2, -0.3, false);
      }

      if (n === 4) label(ctx, 'two daughter cells', cx, cy + R + 22, PALETTE.soft, 11);
      if (n === 0) label(ctx, 'nucleus intact, DNA copying', cx, cy + R + 22, PALETTE.soft, 11);
    }
  });

  /* U5 — Mendelian genetics with a Punnett square */
  window.CourseSims.register('apbio-u5-punnett', {
    title: 'Punnett squares: where the ratios come from',
    blurb:
      'Pick each parent’s genotype. The four boxes are the possible gamete fusions; the 3:1 and 1:1 ratios are just counts of those boxes, not rules to memorise.',
    params: [
      {
        k: 'p1',
        label: 'Parent 1',
        type: 'select',
        val: 'Aa',
        options: [
          { v: 'AA', label: 'AA (homozygous dominant)' },
          { v: 'Aa', label: 'Aa (heterozygous)' },
          { v: 'aa', label: 'aa (homozygous recessive)' }
        ]
      },
      {
        k: 'p2',
        label: 'Parent 2',
        type: 'select',
        val: 'Aa',
        options: [
          { v: 'AA', label: 'AA' },
          { v: 'Aa', label: 'Aa' },
          { v: 'aa', label: 'aa' }
        ]
      }
    ],
    readout(s) {
      const boxes = punnett(s.p1, s.p2);
      const dom = boxes.filter((b) => b.includes('A')).length;
      return [
        ['dominant phenotype', dom + '/4 (' + Math.round((dom / 4) * 100) + '%)'],
        ['recessive phenotype', 4 - dom + '/4'],
        ['genotypes', genotypeCount(boxes)],
        ['cross', s.p1 + ' × ' + s.p2]
      ];
    },
    note(s) {
      const boxes = punnett(s.p1, s.p2);
      const dom = boxes.filter((b) => b.includes('A')).length;
      if (dom === 4) return 'Every box carries a dominant allele, so all offspring show the dominant trait — but two of them are carriers (Aa).';
      if (dom === 0) return 'No dominant allele anywhere: all four offspring are aa and show the recessive trait.';
      return 'The ratio is a statement about probability per offspring, not a promise about a litter. Each fertilisation is independent.';
    },
    draw(ctx, s, box) {
      const boxes = punnett(s.p1, s.p2);
      const cell = Math.min(64, (Math.min(box.w, box.h) - 40) / 3);
      const x0 = box.x + (box.w - cell * 3) / 2;
      const y0 = box.y + (box.h - cell * 3) / 2;

      const a1 = s.p1.split('');
      const a2 = s.p2.split('');

      label(ctx, a1[0], x0 + cell * 1.5, y0 - 8, PALETTE.soft, 13);
      label(ctx, a1[1], x0 + cell * 2.5, y0 - 8, PALETTE.soft, 13);
      label(ctx, a2[0], x0 - 14, y0 + cell * 1.5 + 4, PALETTE.soft, 13);
      label(ctx, a2[1], x0 - 14, y0 + cell * 2.5 + 4, PALETTE.soft, 13);

      for (let r = 0; r < 2; r++) {
        for (let c = 0; c < 2; c++) {
          const i = r * 2 + c;
          const x = x0 + cell * (c + 1);
          const y = y0 + cell * (r + 1);
          const dom = boxes[i].includes('A');
          ctx.fillStyle = dom ? 'rgba(5,150,105,0.16)' : 'rgba(220,38,38,0.10)';
          ctx.fillRect(x, y, cell, cell);
          ctx.strokeStyle = '#e7e2da';
          ctx.lineWidth = 1.4;
          ctx.strokeRect(x, y, cell, cell);
          label(ctx, boxes[i], x + cell / 2, y + cell / 2 + 5, dom ? '#065f46' : '#991b1b', 15);
        }
      }
    }
  });

  /* U6 — transcription and translation, codon by codon */
  window.CourseSims.register('apbio-u6-translation', {
    title: 'From DNA triplet to amino acid',
    blurb:
      'Slide along the gene. Each DNA triplet is transcribed into an mRNA codon, the anticodon pairs with it, and the codon table decides which amino acid joins the chain.',
    params: [{ k: 'codon', label: 'codon index', min: 0, max: 5, step: 1, val: 1, decimals: 0 }],
    readout(s) {
      const gene = ['ATG', 'TTT', 'GGG', 'CAG', 'TAC', 'TGA'];
      const dna = gene[Math.round(s.codon)];
      const mrna = dna.replace(/T/g, 'U');
      return [
        ['DNA triplet', dna],
        ['mRNA codon', mrna],
        ['anticodon', complement(mrna)],
        ['amino acid', codonTable[mrna] || 'unknown']
      ];
    },
    note(s) {
      const gene = ['ATG', 'TTT', 'GGG', 'CAG', 'TAC', 'TGA'];
      const mrna = gene[Math.round(s.codon)].replace(/T/g, 'U');
      if (mrna === 'AUG') return 'AUG is the start codon: it sets the reading frame, so every triplet after it is read in order.';
      if (codonTable[mrna] === 'STOP') return 'UGA is a stop codon. No tRNA carries an amino acid for it, so the ribosome releases the finished chain.';
      return 'The anticodon is antiparallel and complementary, so U pairs with A and G pairs with C. That is why the tRNA must carry exactly this codon’s partner.';
    },
    draw(ctx, s, box) {
      const gene = ['ATG', 'TTT', 'GGG', 'CAG', 'TAC', 'TGA'];
      const idx = Math.round(s.codon);
      const dna = gene[idx];
      const mrna = dna.replace(/T/g, 'U');

      const bw = Math.min(70, (box.w - 60) / 7);
      const y = box.y + box.h * 0.32;
      const startX = box.x + (box.w - bw * 6.6) / 2;

      label(ctx, 'DNA', box.x + 14, y - 24, PALETTE.soft, 10, 'left');
      label(ctx, 'mRNA', box.x + 14, y + 34, PALETTE.blue, 10, 'left');

      gene.forEach((triplet, i) => {
        const x = startX + i * bw * 1.1;
        const active = i === idx;
        ctx.fillStyle = active ? 'rgba(37,99,235,0.18)' : '#f6f1e9';
        ctx.fillRect(x, y - 16, bw, 30);
        label(ctx, triplet, x + bw / 2, y + 4, active ? PALETTE.blue : PALETTE.soft, 11);
        if (active) {
          label(ctx, triplet.replace(/T/g, 'U'), x + bw / 2, y + 44, PALETTE.blue, 11);
          arrow(ctx, x + bw / 2, y + 16, x + bw / 2, y + 32, PALETTE.blue, 1.5);
        }
      });

      // ribosome + tRNA
      const rx = startX + idx * bw * 1.1 + bw / 2;
      const ry = y + 96;
      ctx.fillStyle = '#fde68a';
      ctx.strokeStyle = '#b45309';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.ellipse(rx, ry, 46, 26, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
      label(ctx, 'ribosome', rx, ry + 4, '#7c2d12', 10);
      label(ctx, complement(mrna), rx, ry - 34, PALETTE.accent, 12);
      label(ctx, codonTable[mrna] || '?', rx, ry + 46, PALETTE.ink, 13);
    }
  });

  /* U7 — natural selection on allele frequencies */
  window.CourseSims.register('apbio-u7-hardyweinberg', {
    title: 'Selection shifts allele frequencies',
    blurb:
      'Start with the recessive allele at frequency q. Hardy–Weinberg holds it steady only when there is no selection; add selection against one phenotype and q falls generation after generation.',
    params: [
      { k: 'q0', label: 'starting q', min: 0.05, max: 0.95, step: 0.05, val: 0.5, decimals: 2 },
      { k: 's', label: 'selection against aa', min: 0, max: 0.9, step: 0.05, val: 0.3, decimals: 2 }
    ],
    readout(s) {
      const q20 = alleleAfter(s.q0, s.s, 20);
      return [
        ['p² (AA)', fmt((1 - s.q0) ** 2, 3)],
        ['2pq (Aa)', fmt(2 * s.q0 * (1 - s.q0), 3)],
        ['q² (aa)', fmt(s.q0 ** 2, 3)],
        ['q after 20 gens', fmt(q20, 3)]
      ];
    },
    note(s) {
      if (s.s === 0) return 'With no selection, no mutation, no drift and random mating, the frequencies do not move: that is the Hardy–Weinberg equilibrium.';
      return 'Selection changes phenotype frequencies first, then allele frequencies. Recessive alleles hide in heterozygotes, so even strong selection removes them slowly.';
    },
    draw(ctx, s, box) {
      const p = plot(ctx, box, { xmin: 0, xmax: 20, ymin: 0, ymax: 1, ticks: 4, xdigits: 0, ydigits: 1, xlabel: 'generation' });
      let q = s.q0;
      const pts = [[0, q]];
      for (let g = 1; g <= 20; g++) {
        q = alleleAfter(q, s.s, 1);
        pts.push([g, q]);
      }
      ctx.strokeStyle = PALETTE.accent;
      ctx.lineWidth = 2.4;
      ctx.beginPath();
      pts.forEach(([g, v], i) => {
        const x = p.X(g);
        const y = p.Y(v);
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      });
      ctx.stroke();
      pts.forEach(([g, v]) => dot(ctx, p.X(g), p.Y(v), 2.6, PALETTE.accent));

      if (s.s === 0) {
        ctx.save();
        ctx.setLineDash([5, 4]);
        ctx.strokeStyle = PALETTE.green;
        ctx.beginPath();
        ctx.moveTo(p.x0, p.Y(s.q0));
        ctx.lineTo(p.x0 + p.w, p.Y(s.q0));
        ctx.stroke();
        ctx.restore();
        label(ctx, 'equilibrium', p.x0 + p.w - 6, p.Y(s.q0) - 6, PALETTE.green, 10, 'right');
      }
    }
  });

  /* U8 — population growth against a carrying capacity */
  window.CourseSims.register('apbio-u8-population', {
    title: 'Exponential growth meets a limit',
    blurb:
      'A population with unlimited resources grows exponentially. Add a carrying capacity and the same growth rate produces an S-curve, fastest at half of K.',
    params: [
      { k: 'r', label: 'growth rate r', min: 0.05, max: 1, step: 0.05, val: 0.5, decimals: 2 },
      { k: 'K', label: 'carrying capacity K', min: 100, max: 2000, step: 50, val: 1000, decimals: 0 },
      { k: 'N0', label: 'start N₀', min: 10, max: 400, step: 10, val: 50, decimals: 0 }
    ],
    readout(s) {
      const logistic = s.K / (1 + ((s.K - s.N0) / s.N0) * Math.exp(-s.r * 10));
      return [
        ['N(10) logistic', fmt(logistic, 0)],
        ['N(10) exponential', fmt(s.N0 * Math.exp(s.r * 10), 0)],
        ['dN/dt at N₀', fmt(s.r * s.N0 * (1 - s.N0 / s.K), 1)],
        ['fastest growth at', fmt(s.K / 2, 0)]
      ];
    },
    note(s) {
      return s.N0 > s.K * 0.8
        ? 'Starting near K leaves almost no room to grow: the (1 − N/K) factor is tiny, so the curve is nearly flat.'
        : 'Exponential growth ignores limits: it keeps accelerating. Logistic growth bends because each new individual also reduces the resources available to the next.';
    },
    draw(ctx, s, box) {
      const p = plot(ctx, box, { xmin: 0, xmax: 15, ymin: 0, ymax: Math.max(1200, s.K * 1.15), ticks: 4, xdigits: 0, ydigits: 0, xlabel: 'time' });
      const logistic = (t) => s.K / (1 + ((s.K - s.N0) / s.N0) * Math.exp(-s.r * t));
      curve(ctx, p, logistic, PALETTE.blue, 2.6, 0, 15, 240);
      curve(ctx, p, (t) => s.N0 * Math.exp(s.r * t), 'rgba(220,38,38,0.55)', 2, 0, Math.min(15, Math.log((s.K * 1.2) / s.N0) / s.r), 200);

      ctx.save();
      ctx.setLineDash([5, 4]);
      ctx.strokeStyle = PALETTE.green;
      ctx.beginPath();
      ctx.moveTo(p.x0, p.Y(s.K));
      ctx.lineTo(p.x0 + p.w, p.Y(s.K));
      ctx.stroke();
      ctx.restore();
      label(ctx, 'K', p.x0 + p.w - 8, p.Y(s.K) - 6, PALETTE.green, 10, 'right');
      label(ctx, 'logistic', p.x0 + 10, p.Y(logistic(14)) - 8, PALETTE.blue, 10, 'left');
      label(ctx, 'exponential', p.x0 + 10, p.Y(s.N0 * Math.exp(s.r * 8)) - 8, PALETTE.red, 10, 'left');
    }
  });

  /* ---- helpers ---- */

  function punnett(p1, p2) {
    const a = [p1[0], p1[1]];
    const b = [p2[0], p2[1]];
    const out = [];
    for (const x of b) for (const y of a) out.push([x, y].sort().join(''));
    return out;
  }

  function genotypeCount(boxes) {
    const counts = {};
    boxes.forEach((b) => (counts[b] = (counts[b] || 0) + 1));
    return Object.entries(counts)
      .map(([g, n]) => g + ':' + n)
      .join(' ');
  }

  const codonTable = {
    AUG: 'Met (start)',
    UUU: 'Phe',
    GGG: 'Gly',
    CAG: 'Gln',
    UAC: 'Tyr',
    UGA: 'STOP'
  };

  function complement(mrna) {
    return mrna
      .split('')
      .map((c) => ({ A: 'U', U: 'A', G: 'C', C: 'G' })[c] || c)
      .join('');
  }

  function alleleAfter(q, s, generations) {
    for (let i = 0; i < generations; i++) {
      const p = 1 - q;
      const wAA = 1;
      const wAa = 1;
      const waa = 1 - s;
      const mean = p * p * wAA + 2 * p * q * wAa + q * q * waa;
      if (mean <= 0) return 0;
      q = (q * q * waa + p * q * wAa) / mean;
    }
    return q;
  }
})();
