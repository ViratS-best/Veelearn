'use strict';

/**
 * Embed the question bank, in resumable pages.
 *
 *   node backfill_embeddings.js                 fill rows without an embedding
 *   node backfill_embeddings.js --stale         re-embed rows whose text changed
 *   node backfill_embeddings.js --progress      print counts only
 *   node backfill_embeddings.js --index         create the cosine index
 *
 * Work goes through `POST /api/admin/qbank/embed/backfill`, which embeds and
 * writes a page in one request; `afterId` makes an interrupted run resumable and
 * avoids reading a 50k-row table in one go.
 */

const API = String(process.env.VEELEARN_API || 'https://api.veelearn.org').replace(/\/+$/, '');
const EMAIL = process.env.VEELEARN_EMAIL || 'viratsuper6@gmail.com';
const PASSWORD = process.env.VEELEARN_PASSWORD || 'Virat@123';

const args = process.argv.slice(2);
const has = (f) => args.includes(f);
const valueOf = (name, fallback) => {
    const found = args.find((a) => a.startsWith(`--${name}=`));
    return found ? found.slice(name.length + 3) : fallback;
};
const MODE = has('--stale') ? 'stale' : 'missing';
const PAGE = Number(valueOf('limit', 512)) || 512;

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function call(pathname, options = {}) {
    for (let i = 0; i < 6; i += 1) {
        try {
            const res = await fetch(`${API}${pathname}`, options);
            const text = await res.text();
            let body = null;
            try {
                body = text ? JSON.parse(text) : null;
            } catch (_) {
                body = { message: text.slice(0, 160) };
            }
            if (res.status === 429 || res.status >= 500) {
                await sleep(4000 * (i + 1));
                continue;
            }
            return { status: res.status, body };
        } catch (err) {
            if (i === 5) throw err;
            await sleep(3000 * (i + 1));
        }
    }
    throw new Error(`request failed: ${pathname}`);
}

async function login() {
    const out = await call('/api/login', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ email: EMAIL, password: PASSWORD })
    });
    const token = out.body && out.body.data && out.body.data.token;
    if (!token) throw new Error(`login failed (${out.status})`);
    return token;
}

async function main() {
    const token = await login();
    const H = { authorization: `Bearer ${token}`, 'content-type': 'application/json' };
    const progress = async () => {
        const out = await call('/api/admin/qbank/embed/progress', { headers: H });
        return (out.body && out.body.data) || {};
    };

    const before = await progress();
    console.log(
        `bank ${before.total} | embedded ${before.embedded} | missing ${before.missing} | ${before.column} | extension ${before.extension || '?'} ${before.ready ? '' : `| ${before.error}`}`
    );
    if (!before.ready) {
        console.log('semantic search is not ready on this server; nothing to backfill');
        return;
    }
    if (has('--progress')) return;

    if (has('--index')) {
        const out = await call('/api/admin/qbank/embed/index', { method: 'POST', headers: H, body: '{}' });
        console.log('index:', JSON.stringify(out.body && out.body.data));
        return;
    }
    if (has('--drop-index')) {
        const out = await call('/api/admin/qbank/embed/index', { method: 'POST', headers: H, body: '{"drop":true}' });
        console.log('index:', JSON.stringify(out.body && out.body.data));
        return;
    }

    let afterId = 0;
    let embedded = 0;
    let last = before;
    for (;;) {
        const out = await call('/api/admin/qbank/embed/backfill', {
            method: 'POST',
            headers: H,
            body: JSON.stringify({ afterId, limit: PAGE, mode: MODE })
        });
        if (out.status !== 200 || !out.body || out.body.success === false) {
            console.log('backfill stopped:', out.status, JSON.stringify(out.body).slice(0, 300));
            break;
        }
        const d = out.body.data || {};
        embedded += d.embedded || 0;
        last = d;
        console.log(
            `page ${d.nextId}: +${d.embedded} embedded, ${d.skipped} unchanged | ${d.remaining} missing of ${d.total}`
        );
        if (!d.remaining) break;
        if (!d.scanned) break;
        afterId = d.nextId;
        // No forward progress (all rows on the page had empty text) would loop.
        if (d.embedded === 0 && d.skipped === 0) break;
        await sleep(150);
    }

    const after = await progress();
    console.log(
        `done: +${embedded} embedded this run | bank ${after.total} | embedded ${after.embedded} | missing ${after.missing} | ${after.column}`
    );
    if (after.missing === 0 && last.total) {
        const out = await call('/api/admin/qbank/embed/index', { method: 'POST', headers: H, body: '{}' });
        console.log('index:', JSON.stringify(out.body && out.body.data));
    }
}

main().catch((err) => {
    console.error(err && err.stack ? err.stack : err);
    process.exit(1);
});
