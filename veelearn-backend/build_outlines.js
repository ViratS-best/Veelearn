'use strict';

/**
 * Convert approved courses into outlines, locally.
 *
 *   node build_outlines.js --dry                  build from the cache and report
 *   node build_outlines.js --only=795,796 --dry   a few courses
 *   node build_outlines.js --apply                save through the creator API
 *
 * The building rules live in `outline-builder.js`. Saving 232 outlines one PUT
 * at a time runs into the 100-writes-per-15-minutes limiter, so the normal way
 * to write them all is the superadmin batch endpoint:
 *
 *   POST /api/admin/outlines/build {mode:'stubs'}   then {mode:'courses'} in a loop
 */

const fs = require('fs');
const path = require('path');
const builder = require('./outline-builder');

const API = String(process.env.VEELEARN_API || 'https://api.veelearn.org').replace(/\/+$/, '');
const EMAIL = process.env.VEELEARN_EMAIL || 'viratsuper6@gmail.com';
const PASSWORD = process.env.VEELEARN_PASSWORD || 'Virat@123';
const CACHE = path.join(__dirname, 'tmp_courses.json');
const REPORT = path.join(__dirname, 'tmp_outline_report.json');

const args = process.argv.slice(2);
const has = (flag) => args.includes(flag);
const valueOf = (name, fallback) => {
    const found = args.find((a) => a.startsWith(`--${name}=`));
    return found ? found.slice(name.length + 3) : fallback;
};
const APPLY = has('--apply');
const ONLY = String(valueOf('only', '') || '')
    .split(',')
    .map((n) => Number(n))
    .filter(Boolean);
const LIMIT = Number(valueOf('limit', 0)) || 0;

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function api(pathname, options = {}) {
    const res = await fetch(`${API}${pathname}`, options);
    const text = await res.text();
    let body = null;
    try {
        body = text ? JSON.parse(text) : null;
    } catch (_) {
        body = { raw: text.slice(0, 300) };
    }
    return { status: res.status, body };
}

async function apiRetry(pathname, options = {}, tries = 5) {
    let out = null;
    for (let i = 0; i < tries; i += 1) {
        out = await api(pathname, options);
        if (out.status !== 429 && out.status < 500) return out;
        await sleep(Math.min(30000, 5000 * (i + 1)));
    }
    return out;
}

async function login() {
    const out = await apiRetry('/api/login', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ email: EMAIL, password: PASSWORD })
    });
    const token = out.body && out.body.data && out.body.data.token;
    if (!token) throw new Error(`login failed (${out.status})`);
    return token;
}

async function fetchCourses(token) {
    const headers = { authorization: `Bearer ${token}` };
    const list = await api('/api/courses?limit=1000', { headers });
    const rows = (list.body && list.body.data && (list.body.data.courses || list.body.data)) || [];
    const out = [];
    for (let i = 0; i < rows.length; i += 6) {
        const chunk = rows.slice(i, i + 6);
        const built = await Promise.all(
            chunk.map(async (row) => {
                try {
                    const detail = await api(`/api/courses/${row.id}`, { headers });
                    const questions = await api(`/api/courses/${row.id}/questions`, { headers });
                    const d = (detail.body && detail.body.data) || {};
                    return {
                        id: row.id,
                        title: row.title,
                        creator: row.creator_email,
                        grade: row.grade_level,
                        description: row.description || d.description || '',
                        content: d.content || '',
                        questions: (questions.body && questions.body.data) || []
                    };
                } catch (_) {
                    return { id: row.id, title: row.title, content: '', questions: [] };
                }
            })
        );
        out.push(...built);
        process.stdout.write('.');
    }
    process.stdout.write('\n');
    fs.writeFileSync(CACHE, JSON.stringify(out, null, 1));
    return out;
}

async function remote(token) {
    const headers = { authorization: `Bearer ${token}`, 'content-type': 'application/json' };
    const post = (pathname, body) => apiRetry(pathname, { method: 'POST', headers, body: JSON.stringify(body || {}) });

    const progress = async () => {
        const out = await apiRetry('/api/admin/outlines/progress', { headers });
        return (out.body && out.body.data) || null;
    };

    for (const mode of ['stubs', 'courses']) {
        for (;;) {
            const out = await post('/api/admin/outlines/build', { mode, limit: 12 });
            if (out.status !== 200) {
                console.log(`build ${mode} failed: ${out.status} ${JSON.stringify(out.body).slice(0, 200)}`);
                break;
            }
            const d = out.body.data;
            const s = d.built.reduce(
                (a, r) => {
                    a.units += r.units;
                    a.skills += r.skills;
                    a.questions += r.questions;
                    a.empty += r.emptySkills;
                    return a;
                },
                { units: 0, skills: 0, questions: 0, empty: 0 }
            );
            console.log(
                `${mode}: +${d.built.length} courses (${s.units}u ${s.skills}s ${s.questions}q, ${s.empty} empty) | remaining ${d.remaining}`
            );
            if (d.failed.length) console.log('  failed:', JSON.stringify(d.failed.slice(0, 4)));
            if (!d.remaining) break;
            await sleep(400);
        }
    }

    const before = await progress();
    console.log('mapped:', before && `${before.mapped}/${before.approved}`);

    for (;;) {
        const out = await post('/api/admin/outlines/fill', { limit: 2 });
        if (out.status !== 200) {
            console.log(`fill failed: ${out.status} ${JSON.stringify(out.body).slice(0, 200)}`);
            break;
        }
        const d = out.body.data;
        console.log(`fill: ${d.filled.length} course(s), ${d.filled.reduce((n, r) => n + r.added, 0)} questions`);
        if (d.failed.length) console.log('  fill failures:', JSON.stringify(d.failed.slice(0, 4)));
        if (!d.processed) break;
        if (!d.filled.length && d.failed.length) break; // do not spin on the same gaps
        await sleep(400);
    }

    const after = await progress();
    console.log('FINAL mapped:', after && `${after.mapped}/${after.approved}`, 'stubs:', after && after.stubs);
}

async function main() {
    if (has('--remote')) {
        const token = await login();
        await remote(token);
        return;
    }
    console.log(APPLY ? 'Saving through the creator API' : 'Dry run (nothing is saved)');
    let courses = fs.existsSync(CACHE) && has('--cached') ? JSON.parse(fs.readFileSync(CACHE, 'utf8')) : null;
    let token = null;
    if (!courses) {
        token = await login();
        courses = await fetchCourses(token);
    }
    if (APPLY && !token) token = await login();

    const stubs = courses.filter((c) => String(c.content || '').length < 1000);
    const siblings = courses.filter((c) => String(c.content || '').length >= 1000);

    let targets = courses;
    if (ONLY.length) targets = courses.filter((c) => ONLY.includes(Number(c.id)));
    else if (LIMIT) targets = targets.slice(0, LIMIT);

    const results = [];
    for (const course of targets) {
        let outline = null;
        let how = 'course';
        if (stubs.some((s) => Number(s.id) === Number(course.id))) {
            outline = builder.assembleFromSiblings(course, siblings);
            how = 'siblings';
        } else {
            outline = builder.outlineForCourse(course);
            if (!outline || outline.units.length < 2) {
                const assembled = builder.assembleFromSiblings(course, siblings);
                if (assembled) {
                    outline = assembled;
                    how = 'siblings';
                }
            }
        }
        if (!outline) {
            results.push({ id: course.id, title: course.title, how: 'skipped' });
            console.log(`skip ${course.id} ${course.title}`);
            continue;
        }
        const stats = builder.stats(outline);
        results.push({ id: course.id, title: course.title, how, ...stats });

        if (APPLY) {
            const saved = await apiRetry(`/api/courses/${course.id}/outline`, {
                method: 'PUT',
                headers: { authorization: `Bearer ${token}`, 'content-type': 'application/json' },
                body: JSON.stringify({ outline })
            });
            await sleep(250);
            if (saved.status !== 200) {
                console.log(`FAIL ${course.id}: ${saved.status} ${JSON.stringify(saved.body).slice(0, 140)}`);
                results[results.length - 1].error = String(saved.status);
                continue;
            }
        }
        console.log(
            `${APPLY ? 'saved' : 'built'} ${course.id} ${course.title.slice(0, 48)} | ${how} | ` +
                `${stats.units}u ${stats.skills}s ${stats.questions}q` +
                (stats.emptySkills ? ` | ${stats.emptySkills} empty` : '') +
                (stats.thinSkills ? ` | ${stats.thinSkills} thin` : '')
        );
    }

    const sum = results.reduce(
        (a, r) => {
            a.courses += 1;
            a.units += r.units || 0;
            a.skills += r.skills || 0;
            a.questions += r.questions || 0;
            a.empty += r.emptySkills || 0;
            a.thin += r.thinSkills || 0;
            if (r.error) a.failed += 1;
            return a;
        },
        { courses: 0, units: 0, skills: 0, questions: 0, empty: 0, thin: 0, failed: 0 }
    );
    console.log('\nTOTAL', JSON.stringify(sum));
    fs.writeFileSync(REPORT, JSON.stringify(results, null, 1));
}

main().catch((err) => {
    console.error(err && err.stack ? err.stack : err);
    process.exit(1);
});
