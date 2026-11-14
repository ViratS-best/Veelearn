#!/usr/bin/env node
/**
 * Insert one purpose-built simulation into each AP Calculus AB unit course.
 *
 * Placement: inside the named section, immediately before the stage card
 * labelled "3 ·" (the step-by-step rule). That is after the plain-words stage
 * and the static picture, and before the formal rule — the point where the
 * reader has something concrete to poke at.
 *
 *   node inject_unit_sims.js --dry-run
 *   node inject_unit_sims.js
 */
const { Client } = require('./veelearn-backend/node_modules/pg');

const required = ['PGHOST', 'PGUSER', 'PGPASSWORD'];
const missing = required.filter((k) => !process.env[k]);
if (missing.length) {
  console.error('Missing env vars: ' + missing.join(', '));
  process.exit(1);
}
const DB = {
  host: process.env.PGHOST,
  port: Number(process.env.PGPORT || 5432),
  user: process.env.PGUSER,
  password: process.env.PGPASSWORD,
  database: process.env.PG_DATABASE || 'defaultdb',
  ssl: { rejectUnauthorized: false }
};

const UNITS = {
  718: [
    '1. Limit from a graph and table',
    'apcalcab-u1-limits',
    'Limits: walk x toward the point',
    'Before the algebra, watch the two columns converge. A limit is a prediction about what the values approach, not a claim about the value at the point.'
  ],
  719: [
    '1. Definition as limit of difference quotient',
    'apcalcab-u2-derivative',
    'Derivatives: shrink the secant into the tangent',
    'The derivative is not a new formula to memorise — it is the number this secant slope settles on as h shrinks.'
  ],
  720: [
    '2. Related rates',
    'apcalcab-u3-related-rates',
    'Related rates: the ladder that will not fall steadily',
    'Move the base at a constant speed and watch the top. The derivative ties the two rates together through the constraint x² + y² = 25.'
  ],
  721: [
    '1. Concavity and the second derivative',
    'apcalcab-u4-concavity',
    'Concavity: bend the curve and read f″',
    'Change the coefficients and watch where the shading flips. That flip is the inflection point, and it is the only place concavity changes.'
  ],
  722: [
    '2. Riemann sums',
    'apcalcab-u5-riemann',
    'Riemann sums: rectangles that become the area',
    'Add rectangles and switch sample points. Then drag the upper limit and watch the accumulated area grow at a rate equal to the height of the curve.'
  ],
  723: [
    '2. Volumes by disks and washers',
    'apcalcab-u6-disks',
    'Volumes: stack the slices into a solid',
    'Each slice is a disk of radius f(x). More slices means the sum of their volumes closes in on the exact volume.'
  ],
  724: [
    '1. Slope fields',
    'apcalcab-u7-slope-field',
    'Slope fields: follow the segments with Euler',
    'Every little segment obeys y′ = f(x, y). Step along them with Euler and compare with the exact solution — then shrink the step and watch the error fall.'
  ],
  725: [
    '6. Justifying with theorems',
    'apcalcab-u8-capstone',
    'Capstone: one graph, four questions',
    'Free-response questions switch between value, slope, concavity and accumulated area without telling you which one is wanted. This is that switch, in one view.'
  ],

  // ---- AP Calculus BC ----
  727: [
    '2. Parametric dy/dx',
    'apcalcbc-u1-parametric',
    'Parametric motion: one parameter, two derivatives',
    'Slide t along the cycloid. The slope is the ratio of the two rates, and at the cusp the ratio fails because dx/dt is zero.'
  ],
  728: [
    '5. Improper integrals Type 1',
    'apcalcbc-u2-improper',
    'Improper integrals: does the tail close?',
    'Shade the area out to R and change p. Above p = 1 the area stops at a finite total; below it, each extra strip keeps adding.'
  ],
  729: [
    '3. Arc length of y=f(x)',
    'apcalcbc-u3-arclength',
    'Arc length: straighten the curve with segments',
    'Cut the parabola into chords. Their total length approaches the arc length, and the limit is the integral of √(1 + (dy/dx)²).'
  ],
  730: [
    '2. Geometric series',
    'apcalcbc-u4-geometric',
    'Geometric series: watch the partial sums decide',
    'Terms shrink for every |r| < 1, but that alone does not make a series converge. Slide r past 1 and −1 and see what the sums do.'
  ],
  731: [
    '4. Interval and radius of convergence',
    'apcalcbc-u5-radius',
    'Power series: where do the partial sums settle?',
    'The ratio test gives |x|, so the radius is 1. Move x inside, to the edge and outside; the endpoints need their own tests.'
  ],
  732: [
    '1. Taylor polynomial',
    'apcalcbc-u6-taylor',
    'Taylor polynomials: add one term at a time',
    'Raise the degree and watch how far the polynomial stays glued to the function — and where it finally peels away.'
  ],
  733: [
    '1. Polar area',
    'apcalcbc-u7-polar-area',
    'Polar area: sweep the ray and add the slivers',
    'Each thin wedge has area ½r²Δθ. Rotate the ray through a rose and watch the region fill in.'
  ],
  734: [
    '2. Logistic differential equation',
    'apcalcbc-u8-logistic',
    'Logistic growth: the rate depends on the population',
    'Raise r and the S-curve steepens; move K and it levels elsewhere. The growth rate peaks at exactly half the carrying capacity.'
  ],

  // ---- AP Biology ----
  736: [
    '1. Water and hydrogen bonding',
    'apbio-u1-water',
    'Hydrogen bonds: strong together, weak alone',
    'Warm the water and watch the bonds break and re-form. Below freezing they lock into an open lattice, which is why ice floats.'
  ],
  737: [
    '4. Passive transport',
    'apbio-u2-transport',
    'Which way will water and solutes move?',
    'Set the solute concentration on each side. Passive transport follows the gradient; active transport can push against it with ATP.'
  ],
  738: [
    '2. Environmental effects on enzymes',
    'apbio-u3-enzyme',
    'Enzyme rate: saturation, then denaturation',
    'More substrate speeds the reaction until every active site is full. Heat it too far and the rate collapses instead.'
  ],
  739: [
    '3. Mitosis',
    'apbio-u4-mitosis',
    'Mitosis: follow two chromosomes through the cycle',
    'Step through the phases. The chromosome count never changes; what changes is how the DNA is packed, aligned and pulled apart.'
  ],
  740: [
    '2. Probability and Punnett',
    'apbio-u5-punnett',
    'Punnett squares: where the ratios come from',
    'Choose each parent’s genotype. The 3:1 and 1:1 ratios are just counts of the four boxes, not rules to memorise.'
  ],
  741: [
    '3. Translation',
    'apbio-u6-translation',
    'From DNA triplet to amino acid',
    'Slide along the gene: DNA is transcribed to mRNA, the anticodon pairs, and the codon table names the amino acid.'
  ],
  742: [
    '2. Hardy',
    'apbio-u7-hardyweinberg',
    'Selection shifts allele frequencies',
    'Hardy–Weinberg holds still only without selection. Add selection against aa and q falls — slowly, because recessive alleles hide in heterozygotes.'
  ],
  743: [
    '2. Population growth',
    'apbio-u8-population',
    'Exponential growth meets a limit',
    'Unlimited resources give an exponential curve. Add a carrying capacity and the same rate produces an S-curve, fastest at K/2.'
  ],

  // ---- AP Chemistry ----
  781: [
    '3. Electron configuration',
    'apchem-u1-atomic',
    'Build the atom and watch the trends',
    'Add protons and electrons fill 1s, 2s, 2p, 3s, 3p, 4s. The valence count resets at each new shell — exactly where the trends turn around.'
  ],
  782: [
    '5. Bond polarity',
    'apchem-u2-bonding',
    'How unequal sharing becomes an ionic bond',
    'Slide ΔEN: small differences share almost evenly, large ones transfer the electron outright, and the arrow shows where the density sits.'
  ],
  783: [
    '1. Intermolecular forces',
    'apchem-u3-imf',
    'Which force has to be broken to boil?',
    'Pick the strongest IMF and the molar mass. Boiling means pulling molecules apart, so stronger forces push the boiling point up.'
  ],
  784: [
    '3. Limiting reactant',
    'apchem-u4-limiting',
    '2 A + B → 3 C: which reactant runs out?',
    'Set the particle counts. The reaction needs two A per B, so one reactant runs out first and the leftovers cannot react.'
  ],
  785: [
    '2. Integrated rate laws',
    'apchem-u5-kinetics',
    'Reaction order changes the whole curve',
    'Switch the order and watch the half-life: constant for first order, growing for second, shrinking for zero.'
  ],
  786: [
    '6. Energy diagrams',
    'apchem-u6-thermo',
    'Activation energy and ΔH are different numbers',
    'The peak above the reactants is Ea; the gap to the products is ΔH. A catalyst lowers the peak and leaves ΔH untouched.'
  ],
  787: [
    '3. Le Chatelier',
    'apchem-u7-equilibrium',
    'K sets the ratio; a stress moves Q away from it',
    'Add more A and Q drops below K, so the system shifts forward until Q returns to K. That is Le Chatelier in one variable.'
  ],
  788: [
    '4. Titration curves',
    'apchem-u8-titration',
    'Titration: the buffer plateau and the equivalence cliff',
    'The pH crawls through the buffer region, jumps at equivalence, and the half-equivalence point sits exactly at pH = pKa.'
  ],

  // ---- AP Physics 1 ----
  745: [
    '3. Graphs of motion',
    'apphy1-u1-kinematics',
    'Three graphs, one motion',
    'Move the clock: the slope of x–t is v, and the slope of v–t is a. The same motion, read three ways.'
  ],
  746: [
    "2. Newton's second law and net force",
    'apphy1-u2-forces',
    'Free-body diagram: what is the net force?',
    'Push the block and add friction. The acceleration is set by the vector sum, not by the largest single arrow.'
  ],
  747: [
    '4. Conservation of energy',
    'apphy1-u3-energy',
    'Where does the potential energy go?',
    'Without friction every joule of PE becomes KE. Add friction and part of it leaves as thermal energy, so the block arrives slower.'
  ],
  748: [
    '3. Elastic collisions',
    'apphy1-u4-collision',
    'Elastic or inelastic: what survives the crash?',
    'Momentum is conserved every time. Kinetic energy is conserved only when e = 1 — slide the elasticity and watch what disappears.'
  ],
  749: [
    '2. Torque',
    'apphy1-u5-torque',
    'Balance the beam: torque, not force',
    'Torque is force times lever arm, so a small mass far from the pivot can balance a large mass close to it.'
  ],
  750: [
    '3. Conservation of',
    'apphy1-u6-spin',
    'Pull the arms in and spin faster',
    'With no external torque L = Iω cannot change. Halve I and ω doubles, but the kinetic energy rises.'
  ],
  751: [
    '2. Period of a spring',
    'apphy1-u7-shm',
    'Period depends on m and k, not on amplitude',
    'Change the amplitude and the period does not move. Change the mass or spring constant and it does — T = 2π√(m/k).'
  ],
  752: [
    '3. Buoyancy',
    'apphy1-u8-fluids',
    'Pressure with depth, and what floats',
    'Gauge pressure grows with depth and density, and the fraction of a floating block that is submerged equals ρ_object/ρ_fluid.'
  ],

  // ---- AP Physics C: Mechanics ----
  754: [
    '2. Integrating to recover motion',
    'apphyscm-u1-calculus-kinematics',
    'Integrate a(t) twice to get the motion',
    'Here the acceleration changes: a(t) = a₀ + jt. Velocity is its area, position the area of velocity — the calculus is accumulation.'
  ],
  755: [
    '4. Drag proportional to velocity',
    'apphyscm-u2-drag',
    'Drag: the acceleration that switches itself off',
    'With drag proportional to v, the net force shrinks as the object speeds up, so velocity approaches a terminal value it never reaches.'
  ],
  756: [
    '2. Work',
    'apphyscm-u3-work-integral',
    'Work is the area under F(x)',
    'A force that grows with distance does more work than F·d suggests, because each later metre is pushed harder than the first.'
  ],
  757: [
    '1. Center of mass by integral',
    'apphyscm-u4-com',
    'Centre of mass: the point that moves simply',
    'The centre of mass is the mass-weighted average position, and under internal forces it moves as if all the mass lived there.'
  ],
  758: [
    '2. Torque as r cross F',
    'apphyscm-u5-torque-i',
    'Torque is r × F, and inertia decides α',
    'Push at a larger radius or a better angle and the torque grows. The same torque accelerates a spread-out body more slowly.'
  ],
  759: [
    '5. Atwood machine with a massive pulley',
    'apphyscm-u6-atwood',
    'A pulley with mass steals some of the acceleration',
    'An ideal pulley gives a = (m₁−m₂)g/(m₁+m₂). Give the pulley inertia and it must spin up too, so the acceleration drops.'
  ],
  760: [
    '4. The physical pendulum',
    'apphyscm-u7-pendulum',
    'Physical pendulum: where the mass sits changes the period',
    'A real pendulum is not a point mass on a string. Spread the mass out and the same length gives a different period.'
  ],
  761: [
    '3. Circular orbit speed',
    'apphyscm-u8-orbit',
    'One speed decides circular, elliptical or escape',
    'Launch at increasing speed: below circular it falls back, at circular it repeats, above it traces an ellipse, past escape it never returns.'
  ],

  // ---- AP Physics C: E&M ----
  763: [
    "1. Coulomb's law",
    'apphyscem-u1-coulomb',
    'Two charges, one force law',
    'The force grows with both charges and falls as 1/r². Flip a sign and the arrow reverses but its length does not change.'
  ],
  764: [
    "2. Gauss's law statement",
    'apphyscem-u2-gauss',
    'Flux does not care how big the surface is',
    'Grow the Gaussian sphere: area grows as r², field falls as 1/r², and the flux stays fixed at Q/ε₀.'
  ],
  765: [
    '4. Capacitance',
    'apphyscem-u3-capacitor',
    'Packing charge onto a capacitor',
    'Bigger plates hold more charge; moving them apart weakens the field at fixed voltage and lowers the capacitance.'
  ],
  766: [
    '4. Series and parallel',
    'apphyscem-u4-circuit',
    'Same battery, two very different currents',
    'Series adds resistances and shares one current. Parallel splits the current and draws more from the battery.'
  ],
  767: [
    '3. Time constant',
    'apphyscem-u5-rc',
    'RC circuits: the time constant sets the clock',
    'Charging follows V(1−e^(−t/τ)), discharging V e^(−t/τ). More R or more C slows everything by exactly τ.'
  ],
  768: [
    '1. Force on a moving charge',
    'apphyscem-u6-magnetic',
    'Magnetic force bends paths into circles',
    'F = qvB sin θ is always perpendicular to v, so it does no work — it only turns the particle, into a circle of radius mv/(qB).'
  ],
  769: [
    "2. Faraday's law",
    'apphyscem-u7-induction',
    'Move the magnet and the coil pushes back',
    'An emf appears only while the flux changes. Lenz’s law says the induced current opposes the change, so the coil acts like a brake.'
  ],
  770: [
    '1. LC oscillations',
    'apphyscem-u8-lc',
    'LC circuit: energy sloshes between C and L',
    'Energy moves completely from the capacitor field to the inductor field and back at f = 1/(2π√(LC)); the total stays fixed.'
  ]
};

function sectionSpan(content, fragment) {
  const re = /<h2[^>]*>([\s\S]*?)<\/h2>/gi;
  const matches = [];
  let m;
  while ((m = re.exec(content))) {
    matches.push({ start: m.index, title: m[1].replace(/<[^>]+>/g, '') });
  }
  for (let i = 0; i < matches.length; i++) {
    if (matches[i].title.toLowerCase().includes(fragment.toLowerCase())) {
      return { start: matches[i].start, end: i + 1 < matches.length ? matches[i + 1].start : content.length };
    }
  }
  return null;
}

function insertPoint(content, span) {
  const marker = content.indexOf('3 ·', span.start);
  if (marker !== -1 && marker < span.end) {
    const card = content.lastIndexOf('<div class="vl-stage"', marker);
    if (card !== -1 && card >= span.start) return card;
  }
  return span.end;
}

/** Remove a previously inserted sim + its lead-in so re-runs can reposition it. */
function stripExisting(content, key) {
  const re = new RegExp(
    '(?:<p style="margin:18px 0 6px;"><strong>Try it yourself\\.</strong>[^<]*</p>)?<div class="vl-sim" data-sim="' +
      key +
      '"[^>]*></div>',
    'g'
  );
  return content.replace(re, '');
}

function block(key, title, lead) {
  return (
    `<p style="margin:18px 0 6px;"><strong>Try it yourself.</strong> ${lead}</p>` +
    `<div class="vl-sim" data-sim="${key}" data-title="${title}"></div>`
  );
}

(async () => {
  const dryRun = process.argv.includes('--dry-run');
  const client = new Client(DB);
  await client.connect();
  try {
    for (const [id, [heading, key, title, lead]] of Object.entries(UNITS)) {
      const { rows } = await client.query('SELECT title, content FROM courses WHERE id = $1', [id]);
      if (!rows.length) {
        console.log(`[skip] ${id}: course not found`);
        continue;
      }
      const { title: courseTitle } = rows[0];
      const content = stripExisting(rows[0].content, key);
      const span = sectionSpan(content, heading);
      if (!span) {
        console.log(`[miss] ${id}: heading ${JSON.stringify(heading)} not found`);
        continue;
      }
      const at = insertPoint(content, span);
      const updated = content.slice(0, at) + block(key, title, lead) + content.slice(at);
      console.log(`[add ] ${id}: ${key} -> ${courseTitle.slice(0, 52)} (+${updated.length - content.length} chars)`);
      if (!dryRun) {
        await client.query('UPDATE courses SET content = $1, updated_at = NOW() WHERE id = $2', [updated, id]);
      }
    }
  } finally {
    await client.end();
  }
  console.log(dryRun ? 'dry run: nothing written' : 'done');
})().catch((err) => {
  console.error('ERR', err.message);
  process.exit(1);
});
