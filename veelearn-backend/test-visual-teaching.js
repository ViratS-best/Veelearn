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
close('deflection scales with distance', Math.hypot(near.x, near.y), (50 / 260) * 9, 0.001);

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

let badVisual = 0;
for (const item of withVisual) {
    const v = item.visual;
    if (!v || typeof v !== 'object' || !Board.supported.includes(v.preset)) badVisual += 1;
    else if (v.params != null && typeof v.params !== 'object') badVisual += 1;
}
eq('every diagram uses a preset the board can mount', badVisual, 0);

const presetsUsed = new Set(withVisual.map((q) => q.visual.preset));
ok('the diagrams are not all the same preset', presetsUsed.size >= 3, [...presetsUsed].join(','));

// toCard must carry the diagram through but still hide the answer
const createQBank = require('./qbank');
const qbank = createQBank({ query: async () => [] });
const sample = withVisual[0];
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

// -------------------------------------------------------------------- report
if (failures.length) {
    console.error(`\n${failures.length} FAILED of ${pass + failures.length}:`);
    for (const f of failures) console.error(`  ✗ ${f}`);
    process.exit(1);
}
console.log(`\nAll ${pass} checks passed.`);
