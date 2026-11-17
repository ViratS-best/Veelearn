'use strict';

/**
 * Phase 2 checks that need no browser and no database.
 *
 *   node test-visual-teaching.js
 *
 * Loads the four front-end modules against a stubbed window/document and checks
 * the parts that are pure maths or pure data: the pupil vector, the primitive
 * vocabulary, the board's preset contract, and that every diagram in the seed is
 * something the board can actually mount.
 */

const path = require('path');
const fs = require('fs');

// The modules are plain IIFEs that attach to `window`; in Node that is `global`.
global.window = global;
global.document = {
    addEventListener() {},
    removeEventListener() {},
    querySelector() {
        return null;
    },
    getElementById() {
        return null;
    },
    createElement() {
        return { style: {}, classList: { add() {}, remove() {} }, appendChild() {}, setAttribute() {} };
    }
};
if (!global.performance) global.performance = { now: () => Date.now() };

const FRONTEND = path.join(__dirname, '..', 'veelearn-frontend');
require(path.join(FRONTEND, 'mascot.js'));
require(path.join(FRONTEND, 'annotate.js'));
const boardPath = path.join(FRONTEND, 'board.js');
try {
    require(boardPath);
} catch (e) {
    console.error(`board.js failed to load: ${e.message}`);
    process.exit(1);
}
require(path.join(FRONTEND, 'celebrate.js'));

const { Mascot, Annotate, Board, Celebrate } = global;

let pass = 0;
const failures = [];

function ok(name, cond, detail) {
    if (cond) pass += 1;
    else failures.push(`${name}${detail ? ` — ${detail}` : ''}`);
}

function eq(name, actual, expected) {
    ok(name, actual === expected, `expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);
}

function close(name, actual, expected, tolerance) {
    ok(name, Math.abs(actual - expected) <= tolerance, `expected ≈${expected}, got ${actual}`);
}

// --------------------------------------------------------------- the modules
['Mascot', 'Annotate', 'Board', 'Celebrate'].forEach((name) => {
    ok(`${name} attaches to window`, !!global[name]);
});

// ------------------------------------------------------------ the pupil maths
const straight = Mascot.pupilOffset(1000, 0, 0, 0);
close('a far cursor deflects the pupil to the maximum', Math.hypot(straight.x, straight.y), 9, 0.001);
ok('deflection points toward the cursor', straight.x > 0 && Math.abs(straight.y) < 0.001);

const near = Mascot.pupilOffset(50, 0, 0, 0);
ok('a near cursor deflects less', Math.hypot(near.x, near.y) < 9, `got ${Math.hypot(near.x, near.y)}`);
close('deflection scales with distance', Math.hypot(near.x, near.y), (50 / 620) * 9, 0.001);

const centred = Mascot.pupilOffset(0, 0, 0, 0);
ok('a cursor on the eye centre does not move the pupil', Math.abs(centred.x) < 0.001 && Math.abs(centred.y) < 0.001);

const diagonal = Mascot.pupilOffset(300, 300, 0, 0);
ok('the vector stays inside the iris radius', Math.hypot(diagonal.x, diagonal.y) <= 9.0001);
close('a diagonal is normalised, not clipped', diagonal.x, diagonal.y, 0.001);

ok('the ease is a fraction', Mascot.easeFactor(1 / 60) > 0 && Mascot.easeFactor(1 / 60) < 1);
ok('a longer frame eases further', Mascot.easeFactor(0.05) > Mascot.easeFactor(0.01));
ok('a long stall is capped', Mascot.easeFactor(10) < 1);

// ------------------------------------------------------------- the mood rig
const MOODS = ['idle', 'happy', 'talking', 'pointing', 'writing', 'thinking', 'oops', 'cheer', 'sleepy'];
MOODS.forEach((mood) => {
    ok(`the rig has a ${mood} pose`, Array.isArray(Mascot.moods) && Mascot.moods.includes(mood), (Mascot.moods || []).join(','));
});
ok('a cheer pose exists for the goal', Mascot.moods.includes('cheer'));
ok('a pointing pose exists for annotations', Mascot.moods.includes('pointing'));
ok('the rig can pose without a frame loop', typeof Mascot.poseOnce === 'function');

// --------------------------------------------------------- the ink vocabulary
const PRIMITIVES = ['underline', 'highlight', 'circle', 'ellipseLabel', 'arrow', 'curve', 'strike', 'box', 'brace', 'sweep', 'stamp', 'shake'];
eq('twelve annotation primitives', PRIMITIVES.length, 12);
PRIMITIVES.forEach((name) => {
    ok(`Annotate.${name} exists`, typeof Annotate[name] === 'function');
});
eq('concurrent ink is capped at 12', Annotate.MAX_LIVE, 12);
ok('Annotate can describe a target', typeof Annotate.labelOf === 'function');
ok('Annotate can play a script', typeof Annotate.play === 'function');

// ------------------------------------------------------------ the board contract
['number_line', 'function_plot', 'area_shade', 'coordinate_plane', 'geometry_board', 'triangle_lab', 'unit_circle', 'projectile'].forEach(
    (preset) => {
        ok(`board supports ${preset}`, Board.supported.includes(preset), Board.supported.join(','));
    }
);
eq('a function plot maps to the function view', Board.viewType('function_plot'), 'function');
eq('an area shade maps to the function view', Board.viewType('area_shade'), 'function');
eq('a number line maps to the geometry view', Board.viewType('number_line'), 'geometry');
eq('a projectile maps to the 3d view', Board.viewType('projectile'), 'sim3d');
ok('the board exposes close/skip', typeof Board.close === 'function' && typeof Board.skip === 'function');

// -------------------------------------------------------------- celebration
eq('the goal uses the design particle count', Celebrate.PARTICLES, 90);
ok('celebration has an item-sized pulse', typeof Celebrate.item === 'function');
ok('celebration has a goal-sized burst', typeof Celebrate.goal === 'function');
ok('celebration has a level-up variant', typeof Celebrate.levelUp === 'function');

// ------------------------------------------------------------- seed diagrams
const seed = JSON.parse(fs.readFileSync(path.join(__dirname, 'seed', 'session_seed.json'), 'utf8'));
const withVisual = seed.questions.filter((q) => q.visual);
ok('some items carry a board diagram', withVisual.length >= 3, `${withVisual.length} items`);

// A diagram is either a board preset the widget engine can mount, or an authored
// SVG that the session card renders as a figure. Both must be safe to ship.
let badVisual = 0;
const presetVisuals = [];
const svgVisuals = [];
for (const item of withVisual) {
    const v = item.visual;
    if (!v || typeof v !== 'object') {
        badVisual += 1;
        continue;
    }
    if (typeof v.svg === 'string') {
        const svg = v.svg.trim();
        const unsafe =
            !svg.toLowerCase().startsWith('<svg') ||
            /<script|<foreignObject|<iframe/i.test(svg) ||
            /\son[a-z]+\s*=/i.test(svg) ||
            !String(v.alt || v.caption || '').trim();
        if (unsafe || svg.length > 20000) badVisual += 1;
        svgVisuals.push(item);
        continue;
    }
    if (!Board.supported.includes(v.preset)) badVisual += 1;
    else if (v.params != null && typeof v.params !== 'object') badVisual += 1;
    else presetVisuals.push(item);
}
eq('every diagram is a mountable preset or a safe authored SVG', badVisual, 0);
ok('the bank ships authored SVG figures', svgVisuals.length >= 5, `${svgVisuals.length} svg items`);

const presetsUsed = new Set(presetVisuals.map((q) => q.visual.preset));
ok('the diagrams are not all the same preset', presetsUsed.size >= 3, [...presetsUsed].join(','));

// toCard must carry the diagram through but still hide the answer
const createQBank = require('./qbank');
const qbank = createQBank({ query: async () => [] });
const sample = presetVisuals[0];
const card = qbank.toCard({
    id: 1,
    skill_id: 2,
    tier: sample.tier,
    qtype: 'mcq',
    stem: sample.stem,
    options: JSON.stringify(sample.options),
    answer: sample.answer,
    hints: JSON.stringify(sample.hints),
    solution_steps: JSON.stringify(sample.steps),
    visual: JSON.stringify(sample.visual)
});
ok('the card carries the diagram spec', card.visual && card.visual.preset === sample.visual.preset);
ok('the card still hides the answer', !('answer' in card) && !JSON.stringify(card).includes('"answer"'));

const svgSample = svgVisuals[0];
const svgCard = qbank.toCard({
    id: 2,
    skill_id: 2,
    tier: svgSample.tier,
    qtype: 'mcq',
    stem: svgSample.stem,
    options: JSON.stringify(svgSample.options),
    answer: svgSample.answer,
    hints: JSON.stringify(svgSample.hints),
    solution_steps: JSON.stringify(svgSample.steps),
    visual: JSON.stringify(svgSample.visual)
});
ok('the card carries an authored SVG figure', !!(svgCard.visual && svgCard.visual.svg));

// ------------------------------------------------------- exam bank coverage
// The STEM / English / SAT R&W / ACT / MATHCOUNTS / AMC banks must stay complete
// enough for a session to teach them: four questions per skill, a tier-1 item,
// and an answer keyed to a real option.
const EXAM_TRACKS = [
    'stem.sci', 'english', 'sat.rw', 'act', 'mathcounts', 'amc8', 'amc10', 'amc12',
    // The wider bank: grades 1-8 and high-school math, AP Calculus and AP
    // Statistics, the olympiad ladder, all-grade science, engineering, coding.
    'math.elem', 'math.hs', 'apcalc', 'apstats', 'aime', 'usamo', 'imo',
    'science.all', 'college.eng', 'coding'
];
const seedSkills = new Map(seed.skills.map((s) => [s.code, s]));
const perSkill = new Map();
for (const q of seed.questions) perSkill.set(q.skill, (perSkill.get(q.skill) || 0) + 1);

for (const track of EXAM_TRACKS) {
    const skills = seed.skills.filter((s) => s.track === track);
    ok(`${track} has skills in the bank`, skills.length >= 2, `${skills.length} skills`);
    const thin = skills.filter((s) => (perSkill.get(s.code) || 0) < 4);
    ok(`${track} skills carry at least four questions`, thin.length === 0, thin.map((s) => s.code).join(','));
}

const badKeys = seed.questions.filter((q) => {
    const keys = (q.options || []).map((o) => String(o.k));
    return keys.length !== 4 || !keys.includes(String(q.answer)) || !seedSkills.has(q.skill);
});
eq('every bank question keys to one of its four options', badKeys.length, 0);

const tierOne = new Set(seed.questions.filter((q) => q.tier === 1).map((q) => q.skill));
const missingTierOne = [...seedSkills.keys()].filter((code) => {
    const skill = seedSkills.get(code);
    return EXAM_TRACKS.includes(skill.track) && !tierOne.has(code);
});
eq('every exam skill opens with a recall item', missingTierOne.length, 0);

// -------------------------------------------------------------------- report
if (failures.length) {
    console.error(`\n${failures.length} FAILED of ${pass + failures.length}:`);
    for (const f of failures) console.error(`  ✗ ${f}`);
    process.exit(1);
}
console.log(`\nAll ${pass} checks passed.`);
