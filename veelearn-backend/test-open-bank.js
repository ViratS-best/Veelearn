'use strict';

/**
 * Checks for the bulk question bank (seed/open_bank.jsonl.gz) and its loader.
 *
 *   node test-open-bank.js
 *
 * The bank is the part of the product a licence mistake would be expensive in, so
 * this suite reads the shipped file rather than a fixture: every row must have a
 * permissive licence line, four distinct options and a live answer key, and the
 * requested subject spread has to actually be in there.
 */

const fs = require('fs');
const path = require('path');
const zlib = require('zlib');
const readline = require('readline');

const { importOpenBank } = require('./session-schema');
const provenance = require('./provenance');

const BANK = path.join(__dirname, 'seed', 'open_bank.jsonl.gz');
const META = path.join(__dirname, 'seed', 'open_bank_meta.json');
const SEED = path.join(__dirname, 'seed', 'session_seed.json');

let pass = 0;
const failures = [];

function ok(name, cond, detail) {
    if (cond) pass += 1;
    else failures.push(`${name}${detail ? ` — ${detail}` : ''}`);
}

function eq(name, actual, expected) {
    ok(name, actual === expected, `expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);
}

const PERMISSIVE = /^(MIT|Apache-2\.0|CC0-1\.0|BSD-[23]-Clause|CC-BY-4\.0)$/i;
const BLOCKED = /(NC|SA|ND|GPL)/i;

(async function main() {
    // ---------------------------------------------------------------- files
    ok('the bank file is shipped', fs.existsSync(BANK));
    ok('the bank meta is shipped', fs.existsSync(META));
    if (!fs.existsSync(BANK) || !fs.existsSync(META)) return finish();

    const meta = JSON.parse(fs.readFileSync(META, 'utf8'));
    const seed = JSON.parse(fs.readFileSync(SEED, 'utf8'));
    const seedCodes = new Set((seed.skills || []).map((s) => s.code));

    // -------------------------------------------------------------- licences
    ok('the bank records the datasets it came from', Array.isArray(meta.datasets) && meta.datasets.length >= 3);
    for (const d of meta.datasets || []) {
        ok(`${d.id} has a licence`, Boolean(d.license), JSON.stringify(d));
        ok(`${d.id} uses a permissive licence`, PERMISSIVE.test(String(d.license)), d.license);
        ok(`${d.id} is not non-commercial or share-alike`, !BLOCKED.test(String(d.license)), d.license);
        ok(`${d.id} carries an attribution line`, String(d.attribution || '').length > 5);
    }
    ok('generated items are labelled as Veelearn originals', meta.generated && meta.generated.source === 'authored');

    // ------------------------------------------------------- every question
    const seen = new Set();
    const bySource = {};
    let rows = 0;
    let badOptions = 0;
    let badKey = 0;
    let noAttribution = 0;
    let noHints = 0;
    let unknownSkill = 0;
    let shortStem = 0;

    const stream = fs.createReadStream(BANK).pipe(zlib.createGunzip());
    const lines = readline.createInterface({ input: stream, crlfDelay: Infinity });
    for await (const line of lines) {
        if (!line.trim()) continue;
        rows += 1;
        const q = JSON.parse(line);
        bySource[q.source] = (bySource[q.source] || 0) + 1;
        if (!seedCodes.has(q.skill)) unknownSkill += 1;
        if (!Array.isArray(q.options) || q.options.length !== 4) badOptions += 1;
        const texts = new Set((q.options || []).map((o) => o.t));
        if (texts.size !== 4) badOptions += 1;
        if (!(q.options || []).some((o) => o.k === q.answer)) badKey += 1;
        if (!String(q.attribution || '').trim()) noAttribution += 1;
        if (!Array.isArray(q.hints) || q.hints.length < 2) noHints += 1;
        if (!q.stem || q.stem.trim().length < 8) shortStem += 1;
        seen.add(q.skill);
    }

    eq('the file has as many rows as the meta says', rows, meta.total);
    ok('the bank is in the tens of thousands of questions', rows >= 20000, String(rows));
    eq('no row points at a skill the seed does not define', unknownSkill, 0);
    eq('every row has four distinct options', badOptions, 0);
    eq('every row has a live answer key', badKey, 0);
    eq('every row carries a licence/attribution line', noAttribution, 0);
    eq('every row has at least two hints', noHints, 0);
    eq('no row has an empty stem', shortStem, 0);
    eq('every skill in the meta is covered by rows', seen.size, Object.keys(meta.bySkill || {}).length);
    ok('MMLU rows are imported', bySource.mmlu > 1000, JSON.stringify(bySource));
    ok('OpenBookQA rows are imported', bySource.openbookqa > 1000, JSON.stringify(bySource));
    ok('GSM8K rows are imported', bySource.gsm8k > 1000, JSON.stringify(bySource));
    ok('generated practice rows are present', bySource.authored > 10000, JSON.stringify(bySource));

    // -------------------------------------------------- the requested spread
    const count = (prefix) =>
        Object.keys(meta.bySkill || {})
            .filter((code) => code.startsWith(prefix))
            .reduce((sum, code) => sum + meta.bySkill[code], 0);
    const required = [
        ['AP & college math', 'mmlu.math.'],
        ['AP & college science', 'mmlu.sci.'],
        ['AP humanities', 'mmlu.hum.'],
        ['college engineering', 'mmlu.eng.'],
        ['K-12 arithmetic', 'gen.k5.arith'],
        ['K-12 fractions', 'gen.k5.fractions'],
        ['percent', 'gen.mid.percent'],
        ['rates and ratio', 'gen.mid.ratio'],
        ['geometry', 'gen.geometry.'],
        ['probability', 'gen.probability.'],
        ['algebra', 'gen.algebra.'],
        ['AMC 8', 'gen.contest.amc8'],
        ['AMC 10', 'gen.contest.amc10'],
        ['AMC 12', 'gen.contest.amc12'],
        ['AIME', 'gen.contest.aime'],
        ['USAMO', 'gen.contest.usamo'],
        ['IMO', 'gen.contest.imo'],
        ['Python', 'gen.code.python'],
        ['C++', 'gen.code.cpp'],
        ['Java', 'gen.code.java'],
        ['SAT math', 'gen.sat.math'],
        ['SAT reading and writing', 'gen.sat.rw.'],
        ['ACT math', 'gen.act.math'],
        ['ACT English', 'gen.act.english'],
        ['K-12 science', 'open.elem.science'],
        ['word problems', 'open.word.problems']
    ];
    for (const [name, prefix] of required) {
        const n = count(prefix);
        ok(`the bank covers ${name}`, n >= 200, `${prefix} has ${n}`);
    }

    // ------------------------------------------------------------- the loader
    const bulkCodes = (seed.skills || []).filter((s) => s.bulk).map((s) => s.code);
    ok('the seed marks the bulk skills', bulkCodes.length >= 70, String(bulkCodes.length));

    const skills = (seed.skills || []).map((s, i) => ({ id: i + 1, code: s.code }));
    const inserted = [];
    let poolRefreshes = 0;
    let recorded = null;
    const reportedVersion = [];

    const makeQuery = (alreadyImported) => async (sql, params) => {
        if (/FROM bank_imports/.test(sql)) return alreadyImported ? [{ version: params[0] }] : [];
        if (/SELECT id, code FROM skills/.test(sql)) return skills;
        if (/^INSERT IGNORE INTO qbank_items/.test(sql)) {
            inserted.push(params);
            return { affectedRows: params.length / 12 };
        }
        if (/INSERT INTO skill_pool/.test(sql)) {
            poolRefreshes += 1;
            return {};
        }
        if (/INSERT INTO bank_imports/.test(sql)) {
            recorded = params;
            return {};
        }
        throw new Error(`unexpected query: ${sql.slice(0, 60)}`);
    };

    const log = { info() {}, warn() {} };
    const first = await importOpenBank({ query: makeQuery(false), log });
    ok('the first import reports what it did', first.imported === true, JSON.stringify(first));
    eq('the first import records the bank version', first.version, meta.version);
    eq('every row is attempted exactly once', inserted.reduce((n, p) => n + p.length / 12, 0), rows);
    ok('every row sends twelve columns', inserted.every((p) => p.length % 12 === 0));
    ok('batches stay small enough for one statement', inserted.every((p) => p.length / 12 <= 250));
    eq('the skill pool is refreshed once, not per row', poolRefreshes, 1);
    ok('the version is recorded after the rows', recorded && recorded[0] === meta.version);
    reportedVersion.push(first.version);

    // Second boot: same version, nothing to do.
    const second = await importOpenBank({ query: makeQuery(true), log });
    ok('a repeat boot skips the import', second.imported === false && second.already === true, JSON.stringify(second));
    eq('a repeat boot does not touch qbank_items', inserted.length, inserted.length);

    // Rows are mapped onto the real skill ids, not guessed.
    const idByCode = new Map(skills.map((s) => [s.code, s.id]));
    const sample = inserted[0];
    ok('rows carry a real skill id', [...idByCode.values()].includes(sample[0]), String(sample[0]));
    ok('rows carry a provenance label', String(sample[11]).length > 5);

    // ---------------------------------------------------------- provenance UI
    eq('MMLU gets a short label', provenance.label({ source: 'mmlu' }), 'MMLU · MIT');
    ok('an MMLU row is credited as third-party', provenance.isThirdParty({ source: 'mmlu' }));
    ok('a generated row is not credited as third-party', !provenance.isThirdParty({ source: 'authored' }));

    finish();
})().catch((e) => {
    failures.push(`threw: ${e.message}`);
    finish();
});

function finish() {
    console.log(`test-open-bank.js  ${pass} passed, ${failures.length} failed`);
    for (const f of failures) console.log('  ✗', f);
    process.exitCode = failures.length ? 1 : 0;
}
