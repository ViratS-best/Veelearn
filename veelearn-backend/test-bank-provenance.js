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
    const state = { outline: null, items: [], skills: new Map(), inserts: [], queries: [] };
    let skillSeq = 100;
    let itemSeq = 900;

    async function query(sql, params = []) {
        const s = String(sql).replace(/\s+/g, ' ').trim();
        state.queries.push({ sql: s, params: params.slice() });

        if (/FROM qbank_items q LEFT JOIN skills/.test(s)) return BANK_ROWS;
        if (/SELECT id, creator_id, title FROM courses/.test(s)) {
            return [{ id: Number(params[0]), creator_id: 1, title: 'Stars and Cells' }];
        }
        if (/SELECT id, creator_id FROM courses/.test(s)) return [{ id: Number(params[0]), creator_id: 1 }];
        if (/SELECT outline_json FROM course_outlines/.test(s)) {
            return state.outline ? [{ outline_json: state.outline }] : [];
        }
        if (/^UPDATE course_outlines/.test(s)) {
            const had = Boolean(state.outline);
            state.outline = params[0];
            return [{ affectedRows: had ? 1 : 0, rowCount: had ? 1 : 0 }];
        }
        if (/^INSERT INTO course_outlines/.test(s)) {
            state.outline = params[1];
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

function startServer(db) {
    const app = express();
    app.use(express.json());
    const noLimit = (req, res, next) => next();
    app.use(
        createOutlineRoutes({
            query: db.query,
            authenticateToken: (req, res, next) => {
                req.user = { id: 1, role: 'creator' };
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
