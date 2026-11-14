'use strict';

/**
 * Phase 1 checks that need no database.
 *
 *   node test-session-core.js
 *
 * Covers (a) the reported bug — an 8th grader must not be recommended
 * AP Physics C — (b) mastery/level maths and review scheduling, (c) the shipped
 * seed file and the client-safe question card.
 */

const path = require('path');
const fs = require('fs');

const gradeGate = require('./grade-gate');
const mastery = require('./mastery');
const createQBank = require('./qbank');

let pass = 0;
const failures = [];

function ok(name, cond, detail) {
    if (cond) {
        pass += 1;
    } else {
        failures.push(`${name}${detail ? ` — ${detail}` : ''}`);
    }
}

function eq(name, actual, expected) {
    ok(name, actual === expected, `expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);
}

// --------------------------------------------------------------- the catalog
// Mirrors the shape the tutor query returns, including the broken grade_level
// value that caused the bug: an AP course mislabelled as grade 8.
const CATALOG = [
    { id: 1, title: 'AP Physics C: Mechanics', description: '', grade_level: 8, course_type: 'ap', like_count: 40 },
    { id: 2, title: 'Grade 8 Math: Exponents and Scientific Notation', description: '', grade_level: 8, like_count: 5 },
    { id: 3, title: 'Middle School Physical Science', description: '', grade_level: 8, like_count: 9 },
    { id: 4, title: 'Algebra 1 Foundations', description: '', grade_level: 9, like_count: 12 },
    { id: 5, title: 'AP Calculus AB', description: '', grade_level: 12, course_type: 'ap', like_count: 30 },
    { id: 6, title: 'SAT Math: Heart of Algebra', description: '', grade_level: 11, like_count: 20 },
    { id: 7, title: 'Counting and Addition for Grade 2', description: '', grade_level: 2, like_count: 3 }
];

const QUESTION = 'can you recommend me an 8th grade course?';

// --------------------------------------------------------- (a) the grade bug
const g8 = gradeGate.resolveLearnerGrade({ message: QUESTION });
eq('detects grade 8 from the message', g8.grade, 8);

const gated = gradeGate.filterCatalog(CATALOG, { grade: 8 });
const ids = gated.allowed.map((c) => c.id);
ok('AP Physics C is blocked for a grade-8 learner', !ids.includes(1), `allowed: ${ids.join(',')}`);
ok('AP Calculus is blocked for a grade-8 learner', !ids.includes(5), `allowed: ${ids.join(',')}`);
ok('grade-8 math survives the gate', ids.includes(2));
ok('the blocked course is reported', gated.blocked.some((b) => b.id === 1));

// The exact regression: the old fallback sorted purely by likes and returned
// the AP course first for this prompt.
const rankedForG8 = gated.allowed
    .slice()
    .sort((a, b) => gradeGate.gradeDistance(a, 8) - gradeGate.gradeDistance(b, 8) || b.like_count - a.like_count);
ok('top pick for grade 8 is not AP Physics C', rankedForG8[0].id !== 1, `top: ${rankedForG8[0].title}`);
ok(
    'nothing left in the list starts more than one grade above the learner',
    gated.allowed.every((c) => {
        const band = gradeGate.inferCourseBand(c);
        return !band || band.min <= 9;
    }),
    gated.allowed.map((c) => `${c.id}:${JSON.stringify(gradeGate.inferCourseBand(c))}`).join(' ')
);
ok('SAT Math is hidden from a grade-8 learner', !ids.includes(6));
ok('a grade-8 math course is still offered', rankedForG8[0].id !== 1 && rankedForG8.some((c) => c.id === 2));

// Explicit subject request still wins — the vetting must not be a hard wall.
const explicit = gradeGate.filterCatalog(CATALOG, {
    grade: 8,
    message: 'I really want to learn AP Physics C mechanics, recommend me a course'
});
ok('naming the subject unlocks it', explicit.allowed.some((c) => c.id === 1));

// Older learners keep their access.
const g11 = gradeGate.filterCatalog(CATALOG, { grade: 11 });
ok('grade 11 keeps AP Physics C', g11.allowed.some((c) => c.id === 1));
ok('grade 11 keeps AP Calculus', g11.allowed.some((c) => c.id === 5));
// Remediation stays available; it just stops being offered first.
ok('grade 11 still sees grade-2 counting', g11.allowed.some((c) => c.id === 7));
ok(
    'grade-2 counting ranks behind grade-11 material',
    g11.allowed
        .slice()
        .sort((a, b) => gradeGate.gradeDistance(a, 11) - gradeGate.gradeDistance(b, 11))
        .findIndex((c) => c.id === 7) > 0
);

// A grade-2 learner must not get algebra or AP.
const g2 = gradeGate.filterCatalog(CATALOG, { grade: 2 });
ok('grade 2 keeps counting', g2.allowed.some((c) => c.id === 7));
ok('grade 2 loses Algebra 1', !g2.allowed.some((c) => c.id === 4));
ok('grade 2 loses AP anything', !g2.allowed.some((c) => c.id === 1 || c.id === 5));

// Unknown grade: nothing is hidden.
const unknown = gradeGate.filterCatalog(CATALOG, { grade: null });
eq('unknown grade hides nothing', unknown.allowed.length, CATALOG.length);

// Title beats the (unreliable) grade_level column.
eq('AP Physics C infers band 11-13', gradeGate.inferCourseBand(CATALOG[0]).max, 13);
eq('grade-8 math infers band 6-8', gradeGate.inferCourseBand(CATALOG[1]).max, 8);

// ------------------------------------------------------- (b) mastery maths
eq('level 0 below 0.2', mastery.levelFromP(0.19), 0);
eq('one tier-1 correct is level 1', mastery.levelFromP(0.2), 1);
eq('0.5 is level 2', mastery.levelFromP(0.5), 2);
eq('0.75 is level 3', mastery.levelFromP(0.75), 3);
eq('0.92 is level 4', mastery.levelFromP(0.92), 4);
eq('p clamps at 1', mastery.applyAttempt({ p: 0.95, correct: true, tier: 4 }).p, 1);
eq('wrong answers clamp at 0', mastery.applyAttempt({ p: 0, correct: false, tier: 1 }).p, 0);

const unaided = mastery.applyAttempt({ p: 0, correct: true, tier: 1, assistance: 0 });
eq('unaided tier-1 correct adds 0.2', Math.round(unaided.p * 100) / 100, 0.2);
const heavilyAided = mastery.applyAttempt({ p: 0, correct: true, tier: 1, assistance: 3 });
ok('a solution-assisted correct is worth less', heavilyAided.p < unaided.p);
ok('a solution-assisted correct does not level you up', mastery.levelFromP(heavilyAided.p) === 0);

const twoWeeksLater = mastery.decayedP(0.8, 2, Date.now() - 14 * 86400000);
ok('two weeks halves recall', Math.abs(twoWeeksLater - 0.4) < 0.02, `got ${twoWeeksLater}`);
const youngSkillLater = mastery.decayedP(0.8, 1, Date.now() - 14 * 86400000);
ok('a barely-started skill decays faster', youngSkillLater < twoWeeksLater);
eq('no last-seen date means no decay', mastery.decayedP(0.8, 2, null), 0.8);

eq('wrong answer is reviewed tomorrow', mastery.nextReview({ level: 1, correct: false }).intervalDays, 1);
ok(
    'reviews space out as the level rises',
    mastery.nextReview({ level: 4, correct: true, reps: 3 }).intervalDays >
        mastery.nextReview({ level: 1, correct: true, reps: 0 }).intervalDays
);

eq('dots(0)', JSON.stringify(mastery.dots(0)), JSON.stringify([false, false, false, false]));
eq('dots(2)', JSON.stringify(mastery.dots(2)), JSON.stringify([true, true, false, false]));
eq('dots(9) is capped', JSON.stringify(mastery.dots(9)), JSON.stringify([true, true, true, true]));

ok('a 10 minute session plans 2-3 items', mastery.itemsForMinutes(10) >= 2 && mastery.itemsForMinutes(10) <= 4);
ok('a 40 minute session plans more', mastery.itemsForMinutes(40) > mastery.itemsForMinutes(10));
// Completion is pinned to "unaided tier-1 work reaches the dot target":
// n corrects x 0.2 lands in the level-n band.
eq('dots 1 need 2 corrects', mastery.correctsNeeded(1), 2);
eq('dots 2 need 3 corrects', mastery.correctsNeeded(2), 3);
eq('dots 3 need 4 corrects', mastery.correctsNeeded(3), 4);
eq('dots 4 need 5 corrects', mastery.correctsNeeded(4), 5);

// ----------------------------------------------------------- (c) the seed
const seedPath = path.join(__dirname, 'seed', 'session_seed.json');
ok('seed file exists', fs.existsSync(seedPath));
const seed = JSON.parse(fs.readFileSync(seedPath, 'utf8'));

ok('seed has skills', Array.isArray(seed.skills) && seed.skills.length >= 20, `${seed.skills?.length} skills`);
ok(
    'seed has the phase 1 question count',
    Array.isArray(seed.questions) && seed.questions.length >= 90,
    `${seed.questions?.length} questions`
);

const skillIds = new Set(seed.skills.map((s) => s.code));
const perSkill = new Map();
let badQuestion = 0;
for (const q of seed.questions) {
    if (!skillIds.has(q.skill)) badQuestion += 1;
    perSkill.set(q.skill, (perSkill.get(q.skill) || 0) + 1);
    const opts = q.options || [];
    const keys = opts.map((o) => String(o.k).toUpperCase());
    if (!keys.includes(String(q.answer).toUpperCase())) badQuestion += 1;
    if (opts.length !== 4) badQuestion += 1;
    if ((q.hints || []).length < 1 || (q.steps || []).length < 1) badQuestion += 1;
    // Every wrong option needs its own rationale, or the "why" after a miss is blank.
    if (opts.some((o) => String(o.k).toUpperCase() !== String(q.answer).toUpperCase() && !o.why)) badQuestion += 1;
}
eq('every question is well formed', badQuestion, 0);
ok('every skill has questions', [...skillIds].every((code) => perSkill.get(code) > 0));
ok('prerequisites point at real skills', seed.skills.every((s) => !s.prereq || skillIds.has(s.prereq)));

const tracks = new Set(seed.skills.map((s) => s.track));
ok('all four tracks are seeded', tracks.size >= 4, [...tracks].join(','));

// --------------------------------------------- the card must not leak answers
const stubQBank = createQBank({ query: async () => [] });
const sample = seed.questions[0];
const distractorWhy = sample.options.find((o) => String(o.k).toUpperCase() !== String(sample.answer).toUpperCase() && o.why).why;
const RAW_ROW = {
    id: 101,
    skill_id: 7,
    tier: sample.tier,
    qtype: sample.qtype,
    stem: sample.stem,
    options: JSON.stringify(sample.options),
    answer: sample.answer,
    hints: JSON.stringify(sample.hints),
    solution_steps: JSON.stringify(sample.steps)
};
const card = stubQBank.toCard(RAW_ROW);
const serialised = JSON.stringify(card);
ok('card omits the answer key', !('answer' in card) && !serialised.includes('"answer"'));
ok('card omits distractor rationales', !serialised.includes(distractorWhy.slice(0, 24)));
ok('card keeps the options', Array.isArray(card.options) && card.options.length === 4);
ok(
    'card options carry only key and text',
    card.options.every((o) => Object.keys(o).sort().join(',') === 'k,t')
);
ok('card has a stable id', card.id === 101);

// After grading, the right rationale comes back — and only the right one.
const wrong = sample.options.find((o) => String(o.k).toUpperCase() !== String(sample.answer).toUpperCase());
eq('whyFor returns the chosen distractor rationale', stubQBank.whyFor(RAW_ROW, wrong.k), wrong.why);
eq('whyFor has nothing to say about the correct option', stubQBank.whyFor(RAW_ROW, sample.answer), '');
eq(
    'solutionFor releases steps and the key',
    JSON.stringify(stubQBank.solutionFor(RAW_ROW)),
    JSON.stringify({ steps: sample.steps, answer: sample.answer })
);

// ------------------------------------------------------------------ report
if (failures.length) {
    console.error(`\n${failures.length} FAILED of ${pass + failures.length}:`);
    for (const f of failures) console.error(`  ✗ ${f}`);
    process.exit(1);
}
console.log(`\nAll ${pass} checks passed.`);
