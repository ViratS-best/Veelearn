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
