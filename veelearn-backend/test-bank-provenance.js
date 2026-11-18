'use strict';

/**
 * Bank provenance, end to end and against the real code.
 *
 *   node test-bank-provenance.js
 *
 * Walks the path a creator actually takes: search the bank over HTTP, pick a
 * result the way outline.html's picker does, save the outline, read it back, and
 * turn it into session items. A licensed item (OpenBookQA / GSM8K) must keep its
 * source and attribution the whole way; a Veelearn original must keep saying so.
 */

const fs = require('fs');
const path = require('path');
const express = require('express');
const createOutlineRoutes = require('./outline-routes');
const createOutlines = require('./outline');
const createQBank = require('./qbank');
const courseQuality = require('./course-quality');
const provenance = require('../veelearn-frontend/qbank-provenance');

let pass = 0;
const failures = [];

function ok(name, cond, detail) {
    if (cond) pass += 1;
    else failures.push(`${name}${detail ? ` — ${detail}` : ''}`);
}
function eq(name, actual, expected) {
    ok(name, actual === expected, `expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);
}

const OBQA_ATTRIBUTION = 'OpenBookQA (Mihaylov et al. 2018), Allen Institute for AI — Apache-2.0';
const GSM8K_ATTRIBUTION = 'GSM8K (Cobbe et al. 2021), OpenAI — MIT';
const AUTHORED_ATTRIBUTION = 'Veelearn original — written for Veelearn';

const BANK_ROWS = [
    {
        id: 501,
        stem: 'Stars are',
        options: JSON.stringify([{ k: 'A', t: 'great balls of gas burning billions of miles away' }, { k: 'B', t: 'warm lights that float' }]),
        answer: 'A',
        hints: JSON.stringify(['What is the Sun made of?']),
        solution_steps: JSON.stringify(['Stars are huge, hot spheres of gas.']),
        visual: null,
        source: 'openbookqa',
        attribution: OBQA_ATTRIBUTION,
        skill_name: 'Everyday science concepts'
    },
    {
        id: 502,
        stem: 'Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did she sell altogether?',
        options: JSON.stringify([{ k: 'A', t: '72' }, { k: 'B', t: '96' }]),
        answer: 'A',
        hints: JSON.stringify(['How many did she sell in May?']),
        solution_steps: JSON.stringify(['24 in May, so 72 in total.']),
        visual: null,
        source: 'gsm8k',
        attribution: GSM8K_ATTRIBUTION,
        skill_name: 'Multi-step word problems'
    },
    {
        id: 503,
        stem: 'Solve 3x + 5 = 20 for x.',
        options: JSON.stringify([{ k: 'A', t: '5' }, { k: 'B', t: '3' }]),
        answer: 'A',
        hints: JSON.stringify(['Subtract 5 first.']),
        solution_steps: JSON.stringify(['3x = 15, so x = 5.']),
        visual: null,
        source: 'authored',
        attribution: AUTHORED_ATTRIBUTION,
        skill_name: 'One-variable equations'
    }
];

// ---------------------------------------------------------- fake database
function makeDb() {
    const state = { outline: null, items: [], skills: new Map(), inserts: [], queries: [], courseInserts: [], courseStatus: 'draft' };
    let skillSeq = 100;
    let itemSeq = 900;

    async function query(sql, params = []) {
        const s = String(sql).replace(/\s+/g, ' ').trim();
        state.queries.push({ sql: s, params: params.slice() });

        if (/FROM qbank_items q LEFT JOIN skills/.test(s)) return BANK_ROWS;
        if (/SELECT id, creator_id, title(, status, feedback)? FROM courses/.test(s)) {
            return [{ id: Number(params[0]), creator_id: 1, title: 'Stars and Cells', status: state.courseStatus, feedback: '' }];
        }
        if (/SELECT id, creator_id, status FROM courses/.test(s)) {
            return [{ id: Number(params[0]), creator_id: 1, status: state.courseStatus }];
        }
        if (/SELECT id, creator_id FROM courses/.test(s)) return [{ id: Number(params[0]), creator_id: 1 }];
        // Outline-first creation: the row is a draft course with no body.
        if (/^INSERT INTO courses/.test(s)) {
            state.courseInserts.push({ sql: s, params: params.slice() });
            return { insertId: 4242, affectedRows: 1 };
        }
        if (/^UPDATE courses SET status = 'pending'/.test(s)) {
            state.courseStatus = 'pending';
            return { affectedRows: 1 };
        }
        if (/SELECT outline_json FROM course_outlines/.test(s)) {
            return state.outline ? [{ outline_json: state.outline }] : [];
        }
        if (/^UPDATE course_outlines/.test(s)) {
            const had = Boolean(state.outline);
            state.outline = params[0];
            return [{ affectedRows: had ? 1 : 0, rowCount: had ? 1 : 0 }];
        }
        if (/^INSERT INTO course_outlines/.test(s)) {
            // Creating a brand-new outline pre-creates an empty map; the fake keeps
            // the one saved above so the two flow tests stay independent.
            if (!state.outline) state.outline = params[1];
            return { affectedRows: 1 };
        }
        if (/^INSERT IGNORE INTO skills/.test(s)) {
            if (!state.skills.has(params[0])) state.skills.set(params[0], (skillSeq += 1));
            return { affectedRows: 1 };
        }
        if (/^UPDATE skills SET/.test(s)) return { affectedRows: 1 };
        if (/SELECT id FROM skills WHERE code/.test(s)) {
            if (!state.skills.has(params[0])) state.skills.set(params[0], (skillSeq += 1));
            return [{ id: state.skills.get(params[0]) }];
        }
        if (/SELECT id, stem_hash FROM qbank_items/.test(s)) {
            const hashes = new Set(params.map(String));
            return state.items.filter((i) => hashes.has(String(i.stem_hash)));
        }
        if (/^INSERT IGNORE INTO qbank_items/.test(s)) {
            state.inserts.push({ sql: s, params: params.slice() });
            // 11 params per row: skillId, stem, hash, options, answer, hints, steps,
            // visual, source, attribution, courseId.
            for (let i = 0; i + 10 < params.length; i += 11) {
                const hash = String(params[i + 2]);
                if (state.items.some((it) => String(it.stem_hash) === hash)) continue;
                itemSeq += 1;
                state.items.push({ id: itemSeq, stem_hash: hash });
            }
            return { affectedRows: 1 };
        }
        return [];
    }

    return { query, state };
}

function startServer(db, userId = 1) {
    const app = express();
    app.use(express.json());
    const noLimit = (req, res, next) => next();
    app.use(
        createOutlineRoutes({
            query: db.query,
            authenticateToken: (req, res, next) => {
                req.user = { id: userId, role: userId === 1 ? 'creator' : 'superadmin' };
                next();
            },
            writeLimiter: noLimit,
            log: { warn() {}, info() {} }
        })
    );
    return new Promise((resolve) => {
        const server = app.listen(0, '127.0.0.1', () => resolve(server));
    });
}

async function call(base, method, path, body) {
    const res = await fetch(base + path, {
        method,
        headers: Object.assign({ Authorization: 'Bearer test' }, body ? { 'Content-Type': 'application/json' } : {}),
        body: body ? JSON.stringify(body) : undefined
    });
    const json = await res.json();
    return { status: res.status, json };
}

// ---------------------------------------------------- (a0) real courses only
// Test outlines used to be recommendable: they are approved `courses` rows.
const REAL_MAP = { units: [{ skills: [{ questions: [{}, {}, {}] }] }] };
ok('a placeholder title is a test title', courseQuality.isTestTitle('a') && courseQuality.isTestTitle('Outline Test 1794761977545'));
ok(
    'a harness timestamp is a test title',
    courseQuality.isTestTitle('Gate Test 1794768162860') && courseQuality.isTestTitle('Picture Test 1794768529760')
);
ok('a real exam title survives', !courseQuality.isTestTitle('AP Calculus Unit 4: Sequences & Series Tests'));
ok(
    'a non-Latin title is a real title',
    !courseQuality.isTestTitle('مهارات توظيف أجهزة المحاكاة والمختبرات الافتراضية في التدريس'),
    'Arabic letters must count as letters'
);
ok('a filled outline is recommendable', courseQuality.isRecommendableCourse({ title: 'Stars and Cells' }, REAL_MAP));
ok(
    'an outline with fewer than three questions is not',
    !courseQuality.isRecommendableCourse({ title: 'Stars and Cells' }, { units: [{ skills: [{ questions: [{}] }] }] })
);
ok(
    'a placeholder title is never recommendable, however full the map',
    !courseQuality.isRecommendableCourse({ title: 'Outline Test 1794761977545' }, REAL_MAP)
);
ok(
    'an empty legacy course is not recommendable',
    !courseQuality.isRecommendableCourse({ title: 'Blank Course', description: '', content_length: 0 }, null)
);
ok(
    'a legacy course with a real body is recommendable',
    courseQuality.isRecommendableCourse({ title: 'Waves and Sound', content_length: 240 }, null)
);

// ---------------------------------------------------- (a) picker labels
eq('an OpenBookQA row is labelled with its licence', provenance.label({ source: 'openbookqa', attribution: OBQA_ATTRIBUTION }), 'OpenBookQA · Apache-2.0');
eq('a GSM8K row is labelled with its licence', provenance.label({ source: 'gsm8k', attribution: GSM8K_ATTRIBUTION }), 'GSM8K · MIT');
eq('an authored row reads as a Veelearn original', provenance.label({ source: 'authored', attribution: AUTHORED_ATTRIBUTION }), 'Veelearn original');
eq('a row with no provenance still reads as authored', provenance.label({}), 'Veelearn original');
ok('a third-party row is marked as such', provenance.isThirdParty({ source: 'openbookqa' }) && !provenance.isThirdParty({ source: 'authored' }));
ok('the tooltip keeps the full credit', provenance.detail({ source: 'gsm8k', attribution: GSM8K_ATTRIBUTION }) === GSM8K_ATTRIBUTION);
eq(
    'an unknown licensed set is shortened from its credit line',
    provenance.label({ source: 'some-set', attribution: 'Example Bank (2024), Some Org — CC BY 4.0' }),
    'Example Bank (2024), Some Org · CC BY 4.0'
);
eq('a third-party row with no credit at all is still named', provenance.label({ source: 'some-set' }), 'Third-party set');
// Legacy rows predate provenance: an internal source with no credit line is not
// a licensed set and must never be labelled as one.
eq('a legacy internal source gets no chip', provenance.isThirdParty({ source: 'course' }), false);
eq('an < 16-char internal source with no credit gets no chip', provenance.isThirdParty({ source: 'seed' }), false);
ok('a licensed source is credited', provenance.isThirdParty({ source: 'openbookqa' }));
ok('an unknown source with a credit line is credited', provenance.isThirdParty({ source: 'x-set', attribution: 'X — CC BY 4.0' }));

// ------------------------------------------------------ (b) real HTTP flow
(async () => {
    const db = makeDb();
    const server = await startServer(db);
    const base = `http://127.0.0.1:${server.address().port}`;

    try {
        // 1. Search the bank exactly as the picker does.
        const search = await call(base, 'GET', '/api/question-bank/search?q=stars&limit=12');
        eq('search answers 200', search.status, 200);
        const results = search.json.data || [];
        eq('search returns the bank rows', results.length, 3);
        const obqa = results.find((r) => r.source === 'openbookqa');
        const gsm8k = results.find((r) => r.source === 'gsm8k');
        const authored = results.find((r) => r.source === 'authored');
        ok('the OpenBookQA item comes back with its attribution', obqa && obqa.attribution === OBQA_ATTRIBUTION);
        ok('the GSM8K item comes back with its attribution', gsm8k && gsm8k.attribution === GSM8K_ATTRIBUTION);
        ok('the authored item comes back as a Veelearn original', authored && provenance.label(authored) === 'Veelearn original');
        ok('the picker names the OpenBookQA item in plain language', provenance.label(obqa) === 'OpenBookQA · Apache-2.0');

        // 2. Pick them exactly as addFromBank() does.
        const picked = [obqa, gsm8k, authored].map((item, i) => ({
            id: `q${i}`,
            bankId: item.id,
            stem: item.stem,
            options: item.options.map((o) => ({ k: o.k, t: o.t })),
            answer: item.answer,
            hint: item.hint || '',
            why: item.why || '',
            visual: item.visual || null,
            source: item.source || 'authored',
            attribution: item.attribution || ''
        }));

        const outlineBody = {
            outline: {
                version: 1,
                units: [
                    {
                        id: 'u1',
                        title: 'Stars and number stories',
                        summary: 'A licensed look at space, then a word problem.',
                        skills: [
                            { id: 's1', name: 'What stars are', teach: 'Start from the Sun.', questions: [picked[0], picked[2]] },
                            { id: 's2', name: 'Two-step totals', teach: 'Name each step first.', questions: [picked[1]] }
                        ]
                    }
                ]
            }
        };

        // 3. Save the outline, then read it back.
        const put = await call(base, 'PUT', '/api/courses/7/outline', outlineBody);
        eq('outline save answers 200', put.status, 200);
        const savedQs = put.json.data.outline.units[0].skills.flatMap((s) => s.questions);
        const savedObqa = savedQs.find((q) => q.bankId === 501);
        const savedGsm = savedQs.find((q) => q.bankId === 502);
        const savedAuthored = savedQs.find((q) => q.bankId === 503);
        ok('the saved outline keeps the OpenBookQA source', savedObqa && savedObqa.source === 'openbookqa', JSON.stringify(savedObqa));
        ok('the saved outline keeps the OpenBookQA attribution', savedObqa && savedObqa.attribution === OBQA_ATTRIBUTION);
        ok('the saved outline keeps the GSM8K source and credit', savedGsm && savedGsm.source === 'gsm8k' && savedGsm.attribution === GSM8K_ATTRIBUTION);
        ok('the saved outline keeps the authored question as authored', savedAuthored && savedAuthored.source === 'authored');

        const get = await call(base, 'GET', '/api/courses/7/outline');
        const reloaded = get.json.data.outline.units[0].skills.flatMap((s) => s.questions);
        ok(
            'a reloaded outline still carries provenance',
            reloaded.some((q) => q.source === 'openbookqa' && q.attribution === OBQA_ATTRIBUTION) &&
                reloaded.some((q) => q.source === 'gsm8k' && q.attribution === GSM8K_ATTRIBUTION) &&
                reloaded.some((q) => q.source === 'authored')
        );

        // 4. Turn the outline into session items — the seed the planner builds.
        const outlines = createOutlines({ query: db.query, log: { warn() {} } });
        const plan = await outlines.planFromOutline({ id: 7, grade_level: 8 });
        ok('the outline produces a session plan', plan.length >= 2, `${plan.length} items`);

        const seedParams = db.state.inserts.reduce((all, i) => all.concat(i.params), []);
        const rows = [];
        for (let i = 0; i + 10 < seedParams.length; i += 11) {
            rows.push({ stem: String(seedParams[i + 1]), source: seedParams[i + 8], attribution: seedParams[i + 9] });
        }
        const seededObqa = rows.find((r) => r.source === 'openbookqa');
        const seededGsm = rows.find((r) => r.source === 'gsm8k');
        const seededAuthored = rows.find((r) => r.source === 'authored');
        ok('the OpenBookQA question reaches the question seed with its source', Boolean(seededObqa), JSON.stringify(rows.map((r) => r.source)));
        ok('the OpenBookQA seed row keeps its attribution', seededObqa && seededObqa.attribution === OBQA_ATTRIBUTION);
        ok('the GSM8K seed row keeps its attribution', seededGsm && seededGsm.attribution === GSM8K_ATTRIBUTION);
        ok('the authored seed row stays a Veelearn original', seededAuthored && seededAuthored.attribution === AUTHORED_ATTRIBUTION);

        // 5. The card the learner is served also names where it came from.
        const qbank = createQBank({ query: db.query });
        const card = qbank.toCard({ id: 1, skill_id: 2, tier: 1, qtype: 'mcq', stem: 'Stars are', options: '[]', source: 'openbookqa', attribution: OBQA_ATTRIBUTION });
        eq('the served card carries the source', card.source, 'openbookqa');
        eq('the served card carries the attribution', card.attribution, OBQA_ATTRIBUTION);
        ok('the served card still hides the answer key', !('answer' in card));

        // 6. The two defects the live site turned up.
        const page = fs.readFileSync(path.join(__dirname, '..', 'veelearn-frontend', 'outline.html'), 'utf8');
        ok('the outline page lets a caller choose the verb', /method:\s*opts\.method \|\|/.test(page));
        ok('saving an outline sends PUT', /\/outline',\s*\{\s*method:\s*'PUT'/.test(page));
        ok('the always-POST helper is gone', !/method:\s*opts\.body \? 'POST' : 'GET'/.test(page));

        const searchCall = db.state.queries.find((q) => /FROM qbank_items q LEFT JOIN skills/.test(q.sql));
        ok('bank search is case-insensitive', searchCall && /LOWER\(q\.stem\) LIKE \?/.test(searchCall.sql), searchCall && searchCall.sql.slice(0, 140));
        ok(
            'the search term is lower-cased',
            searchCall && searchCall.params.every((p) => String(p) === String(p).toLowerCase()),
            searchCall && JSON.stringify(searchCall.params)
        );

        // 7. The learner-facing side: session card + transcript.
        const sessionHtml = fs.readFileSync(path.join(__dirname, '..', 'veelearn-frontend', 'session.html'), 'utf8');
        const sessionApp = fs.readFileSync(path.join(__dirname, '..', 'veelearn-frontend', 'session', 'session-app.js'), 'utf8');
        ok('the session page loads the provenance module', /qbank-provenance\.js/.test(sessionHtml));
        ok('the question card has a source chip', /id="sx-q-src"/.test(sessionHtml));
        ok('the card renders provenance for every question', /renderProvenance\(question\)/.test(sessionApp));
        ok('the chip is hidden for originals', /if \(!third\)/.test(sessionApp));

        // The start button must win the hit test at its own coordinates: the
        // stage's cards, Vee's clickable dock (z-index 3) and the board (5)
        // share a stacking context, so controls are lifted above them and a
        // hidden card can never paint over a button.
        const sessionCss = fs.readFileSync(path.join(__dirname, '..', 'veelearn-frontend', 'session.css'), 'utf8');
        ok('a hidden stage card never paints', /\.sx-stage > \[hidden\] \{\s*display: none !important;/.test(sessionCss));
        ok(
            'card controls sit above the mascot dock',
            ['.sx-intro-actions', '.sx-q-actions', '.sx-options'].every((sel) => sessionCss.includes(sel)) &&
                /z-index: 4;/.test(sessionCss)
        );

        const serverProv = require('./provenance');
        [
            { source: 'authored', attribution: AUTHORED_ATTRIBUTION },
            { source: 'openbookqa', attribution: OBQA_ATTRIBUTION },
            { source: 'gsm8k', attribution: GSM8K_ATTRIBUTION },
            { source: 'other', attribution: 'Example Bank (2024), Some Org — CC BY 4.0' },
            { source: 'other' },
            {}
        ].forEach((fixture, i) =>
            eq(`server and browser labels agree #${i}`, serverProv.label(fixture), provenance.label(fixture))
        );
        eq('a Veelearn original is not credited', serverProv.shouldCredit({ source: 'authored' }), false);
        ok('a licensed question is credited', serverProv.shouldCredit({ source: 'gsm8k' }));
        eq('the server does not credit a legacy internal source', serverProv.shouldCredit({ source: 'course' }), false);
        eq(
            'server and browser agree on a legacy row',
            serverProv.shouldCredit({ source: 'course' }),
            provenance.isThirdParty({ source: 'course' })
        );

        // The transcript is written server-side from the ledger, so it needs the credit too.
        const createPhase5 = require('./phase5');
        const transcriptQuery = async (sql) => {
            const s = String(sql).replace(/\s+/g, ' ').trim();
            if (/FROM sessions s/.test(s)) return [{ id: 9, started_at: new Date().toISOString(), mode: 'focus' }];
            if (/FROM session_focus_items f/.test(s)) {
                return [{ ord: 1, status: 'done', attempts: 2, correct_count: 1, name: 'Everyday science concepts' }];
            }
            if (/FROM practice_attempts a/.test(s)) {
                return [
                    { question_id: 1, correct: 1, stem: 'Stars are', answer: 'A', source: 'openbookqa', attribution: OBQA_ATTRIBUTION },
                    { question_id: 2, correct: 0, stem: 'Solve 3x + 5 = 20', answer: 'A', source: 'authored', attribution: AUTHORED_ATTRIBUTION }
                ];
            }
            return [];
        };
        const marks = await createPhase5({ query: transcriptQuery, log: { warn() {}, info() {} } }).transcript({
            userId: 1,
            sessionId: 9
        });
        ok(
            'the transcript credits the licensed question',
            /correct — Stars are _\(source: OpenBookQA · Apache-2\.0\)_/.test(marks.markdown),
            marks.markdown.slice(0, 400)
        );
        ok('the transcript leaves the original uncredited', marks.markdown.includes('- wrong — Solve 3x + 5 = 20\n'));
        ok('the transcript never says "Veelearn original"', !/Veelearn original/.test(marks.markdown));

        // 8. The shipped seed gives licensed questions a diagram, so a learner can
        // see the figure and the credit at the same time.
        const seedJson = JSON.parse(fs.readFileSync(path.join(__dirname, 'seed', 'session_seed.json'), 'utf8'));
        const licensedWithVisual = seedJson.questions.filter((q) => q.source !== 'authored' && q.visual);
        ok('licensed questions carry diagrams', licensedWithVisual.length >= 2, String(licensedWithVisual.length));
        ok(
            'their diagrams are SVGs with alt text',
            licensedWithVisual.every((q) => typeof q.visual.svg === 'string' && q.visual.svg.startsWith('<svg') && q.visual.alt)
        );

        // 9. Outlines are the thing a creator makes now, and they go through the
        // same review queue a course used.
        const create = await call(base, 'POST', '/api/outlines', { title: '  Stars and Cells  ', gradeLevel: 8 });
        eq('creating an outline answers 201', create.status, 201);
        eq('the new outline starts as a draft', create.json.data && create.json.data.status, 'draft');
        eq('the new outline gets the id the database returned', create.json.data && create.json.data.id, 4242);
        const courseRow = db.state.courseInserts[0];
        ok(
            'the outline row has a title, an empty body and draft status',
            courseRow && /'draft'/.test(courseRow.sql) && courseRow.params[0] === 'Stars and Cells',
            courseRow && JSON.stringify(courseRow.params)
        );

        const noTitle = await call(base, 'POST', '/api/outlines', {});
        eq('an untitled outline is refused', noTitle.status, 400);

        const junkTitle = await call(base, 'POST', '/api/outlines', { title: 'a' });
        eq('a one-letter outline title is refused', junkTitle.status, 400);
        const timestampTitle = await call(base, 'POST', '/api/outlines', {
            title: 'Outline Test 1794761977545'
        });
        eq('a timestamped test outline is refused', timestampTitle.status, 400);
        eq('the refused outlines never reach the database', db.state.courseInserts.length, 1);

        const submit = await call(base, 'POST', '/api/outlines/7/submit');
        eq('submitting a complete map answers 200', submit.status, 200);
        eq('submission moves the outline into review', db.state.courseStatus, 'pending');
        eq('the review payload counts the map', submit.json.data && submit.json.data.questions, 3);

        const emptyOutline = db.state.outline;
        db.state.outline = null;
        db.state.courseStatus = 'draft';
        const empty = await call(base, 'POST', '/api/outlines/7/submit');
        eq('an empty map is not submittable', empty.status, 400);
        db.state.outline = emptyOutline;

        const scriptSrc = fs.readFileSync(path.join(__dirname, '..', 'veelearn-frontend', 'script.js'), 'utf8');
        ok('the review queue marks outlines with the map they carry', /AS has_outline/.test(fs.readFileSync(path.join(__dirname, 'server.js'), 'utf8')));
        ok('an admin opens the map instead of an empty course body', /openOutlineForReview/.test(scriptSrc));

        // A superadmin is not the creator, so the reviewed id is never in their
        // own course list. The page must open the id it was given instead of
        // falling back to one of the reviewer's older courses (which had no map
        // and rendered blank).
        ok('the outline page opens the id it was given', /courseId = Number\(wanted \|\| list\[0\]\.id\)/.test(page));
        ok('it never substitutes the viewer\'s first course for a requested id', !/courseId = Number\(match \? match\.id : list\[0\.id\)/.test(page));
        ok('a reviewer with no outlines of their own is not pushed into the create card', /if \(!list\.length && !wanted\)/.test(page));
        ok('the bar names the map that is actually open', /querySelector\('option\[value="' \+ courseId/.test(page));

        // The reviewer's read must actually carry the map, read-only.
        const reviewer = await startServer(db, 99);
        const reviewerBase = `http://127.0.0.1:${reviewer.address().port}`;
        try {
            const asReviewer = await call(reviewerBase, 'GET', '/api/courses/7/outline');
            eq('a reviewer can open a map they did not write', asReviewer.status, 200);
            eq('the reviewer sees the submitted units', asReviewer.json.data.outline.units.length, 1);
            eq(
                'the reviewer sees the submitted skills and questions',
                asReviewer.json.data.outline.units[0].skills.length,
                2
            );
            eq('the map carries its real title', asReviewer.json.data.title, 'Stars and Cells');
            eq('the reviewer cannot edit it', asReviewer.json.data.canEdit, false);
        } finally {
            reviewer.close();
        }
        ok('the outline page can start a new outline', /id="new-outline"/.test(page) && /\/api\/outlines'/.test(page));
        ok('the outline page can submit for approval', /\/submit'/.test(page) && /Submit for approval/.test(page));
        ok('a submitted outline locks its editor', /review\.status === 'pending'/.test(page));
        ok('the outline page autosaves drafts', /setTimeout\(autoSave, 1500\)/.test(page));
        ok('the page shows the review checklist before submitting', /id="checks"/.test(page) && /renderReadiness\(\)/.test(page));
        ok('the map can be tried as a session', /session\.html\?course=/.test(page));
        ok(
            'pages and skills can be reordered and duplicated',
            /move-unit-up/.test(page) && /move-skill-down/.test(page) && /duplicate-skill/.test(page)
        );

        // Course -> outline builder: structure, teaching briefs, diagram ideas,
        // question mapping and the index-course assembly each get a check.
        const builder = require('./outline-builder');
        const mcq = (stem, correct, options) => ({
            question_text: stem,
            options,
            correct_answer: correct,
            explanation: `${stem}: ${correct}`
        });
        const demoCourse = {
            id: 9001,
            title: 'Algebra',
            content:
                '<h2>Linear equations</h2><p>A linear equation has the form ax + b = c. Solve 3x - 7 = 11 by adding 7 to both sides, then dividing both sides by 3.</p>' +
                '<h2>Ratios</h2><p>A ratio compares two quantities. The ratio 2:3 means for every 2 of the first there are 3 of the second.</p>',
            questions: [
                mcq('Solve 3x - 7 = 11', '6', ['6', '5', '4', '7']),
                mcq('Solve 2x + 3 = 11', '4', ['4', '5', '6', '7']),
                mcq('Solve 5x = 45', '9', ['9', '8', '7', '6']),
                mcq('A ratio of 2:3 means what?', 'two parts to three parts', ['two parts to three parts', 'three parts to two parts', 'two plus three', 'two times three']),
                mcq('Which ratio matches 4:6?', '2:3', ['2:3', '3:4', '4:3', '1:2']),
                mcq('Divide 20 in the ratio 2:3', '8 and 12', ['8 and 12', '10 and 10', '12 and 8', '5 and 15'])
            ]
        };
        const demoOutline = builder.outlineForCourse(demoCourse);
        ok('the builder makes one unit per course topic', demoOutline && demoOutline.units.length === 2);
        ok(
            'each skill gets a teaching brief, a plain-words instruction and diagram ideas',
            demoOutline &&
                demoOutline.units.every(
                    (u) =>
                        /Teach it in plain words/.test(u.skills[0].teach) &&
                        /Draw or show: /.test(u.skills[0].teach) &&
                        u.skills[0].teach.length > 120
                )
        );
        ok(
            'the course questions are mapped three per skill',
            demoOutline && demoOutline.units.every((u) => u.skills[0].questions.length >= 3),
            demoOutline && JSON.stringify(demoOutline.units.map((u) => u.skills[0].questions.length))
        );
        ok(
            'an equation skill gets a balance-scale model',
            demoOutline && /balance scale/.test(demoOutline.units[0].skills[0].teach)
        );
        ok(
            'a question keeps its correct answer letter',
            demoOutline &&
                demoOutline.units[0].skills[0].questions.every((q) => q.options.some((o) => o.k === q.answer))
        );

        const indexCourse = {
            id: 9002,
            title: 'Algebra Complete',
            content: '<h2>The units</h2><ol><li>Linear equations</li><li>Ratios</li></ol>',
            questions: []
        };
        const unitOne = {
            id: 9003,
            title: 'Algebra Unit 1: Linear equations',
            content: '<h2>Balancing equations</h2><p>Keep both sides equal. Solve 3x = 12 by dividing both sides by 3.</p>',
            questions: [
                mcq('Solve 3x = 12', '4', ['4', '3', '6', '12']),
                mcq('Solve x + 5 = 9', '4', ['4', '5', '9', '14']),
                mcq('Solve 2x = 10', '5', ['5', '2', '10', '20'])
            ]
        };
        const unitTwo = {
            id: 9004,
            title: 'Algebra Unit 2: Ratios',
            content: '<h2>Comparing quantities</h2><p>A ratio compares two amounts. 3:4 means three of one for four of the other.</p>',
            questions: [
                mcq('Which ratio matches 6:8?', '3:4', ['3:4', '4:3', '6:4', '2:3']),
                mcq('Simplify 10:15', '2:3', ['2:3', '3:2', '10:15', '5:3']),
                mcq('A 2:5 mix uses 4 parts of the first; how many of the second?', '10', ['10', '8', '5', '2'])
            ]
        };
        const assembled = builder.assembleFromSiblings(indexCourse, [unitOne, unitTwo]);
        ok('an index course is assembled from its unit courses', assembled && assembled.units.length === 2);
        ok(
            'the assembled map carries the unit questions',
            assembled && assembled.units.every((u) => u.skills.some((s) => s.questions.length >= 3))
        );

        const serverSrc = fs.readFileSync(path.join(__dirname, 'server.js'), 'utf8');
        ok('the catalog tells the UI which courses are outlines', /AS has_outline/.test(serverSrc));
        ok(
            'my-courses exposes the same flag',
            /AS has_outline FROM courses WHERE creator_id/.test(serverSrc),
            'the dashboard needs it to route an outline to a session'
        );
        ok('deleting a course removes its map too', /DELETE FROM course_outlines WHERE course_id = \?/.test(serverSrc));
    } finally {
        server.close();
    }

    if (failures.length) {
        console.log(`\n${failures.length} FAILED of ${pass + failures.length}:`);
        failures.forEach((f) => console.log('  ✗ ' + f));
        process.exit(1);
    }
    console.log(`\nAll ${pass} checks passed.`);
})();
