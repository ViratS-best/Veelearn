'use strict';

/**
 * Semantic question-bank search.
 *
 * No database and no network: the embeddings client is exercised against a fake
 * fetch, and the schema / hybrid SQL are checked as source so a regression in the
 * column type, index or ranking weights fails here before a deploy.
 */

const fs = require('fs');
const path = require('path');

let pass = 0;
const failures = [];
function ok(name, condition, detail) {
    if (condition) {
        pass += 1;
        return;
    }
    failures.push(name + (detail ? ` — ${detail}` : ''));
}

const embeddings = require('./embeddings');
const outlineRoutesSrc = fs.readFileSync(path.join(__dirname, 'outline-routes.js'), 'utf8');
const serverSrc = fs.readFileSync(path.join(__dirname, 'server.js'), 'utf8');

/* --------------------------------------------------------------- schema */

ok('the vector column is 512-wide halfvec', /halfvec\(512\)/.test(fs.readFileSync(path.join(__dirname, 'embeddings.js'), 'utf8')));
ok('a cosine HNSW index is created', /USING hnsw \(embedding \$\{ops\}\)/.test(fs.readFileSync(path.join(__dirname, 'embeddings.js'), 'utf8')));
ok('halfvec uses the halfvec cosine operator class', /halfvec_cosine_ops/.test(fs.readFileSync(path.join(__dirname, 'embeddings.js'), 'utf8')));
ok('an older pgvector still gets a float vector fallback', /vector\(512\)/.test(fs.readFileSync(path.join(__dirname, 'embeddings.js'), 'utf8')));
ok('the embedded-text fingerprint is stored', /embedding_hash/.test(fs.readFileSync(path.join(__dirname, 'embeddings.js'), 'utf8')));
ok('the extension is created idempotently', /CREATE EXTENSION IF NOT EXISTS vector/.test(fs.readFileSync(path.join(__dirname, 'embeddings.js'), 'utf8')));

/* ------------------------------------------------------------ embeddings */

ok('the embedding model is OpenAI text-embedding-3-small', embeddings.EMBED_MODEL === 'openai/text-embedding-3-small', embeddings.EMBED_MODEL);
ok('dimensions are 512', embeddings.EMBED_DIMS === 512, String(embeddings.EMBED_DIMS));
ok('the endpoint is the Hack Club embeddings proxy', /ai\.hackclub\.com\/proxy\/v1\/embeddings/.test(fs.readFileSync(path.join(__dirname, 'embeddings.js'), 'utf8')));

const row = {
    stem: 'What is 5 + 5?',
    options: JSON.stringify([
        { k: 'A', t: '9' },
        { k: 'B', t: '10' },
        { k: 'C', t: '11' },
        { k: 'D', t: '12' }
    ]),
    answer: 'B',
    skill_name: 'Addition',
    track: 'math.elem'
};
const text = embeddings.questionText(row);
ok('the embedded text contains the question', /What is 5 \+ 5\?/.test(text));
ok('the embedded text contains the topic', /Topic: Addition/.test(text));
ok('the embedded text contains the correct answer text', /Answer: 10/.test(text));
ok('the answer letter alone is not embedded', !/\bB\b/.test(text.replace(/What is 5 \+ 5\?/, '')));
ok('the fingerprint changes when the text changes', embeddings.hashText(text) !== embeddings.hashText(`${text} `));
ok('a vector literal is bracketed and comma-separated', embeddings.toVectorLiteral([0.5, -0.25]) === '[0.5,-0.25]', embeddings.toVectorLiteral([0.5, -0.25]));

(async () => {
    const savedKey = process.env.HACKCLUBAI_KEY;
    const realFetch = global.fetch;
    let captured = null;
    process.env.HACKCLUBAI_KEY = 'hc-semantic-test';
    global.fetch = async (url, options) => {
        captured = { url, body: JSON.parse(options.body), headers: options.headers };
        return {
            ok: true,
            json: async () => ({ data: [{ embedding: Array.from({ length: 1536 }, (_, i) => Math.sin(i + 1)) }] })
        };
    };

    try {
        const [vector] = await embeddings.embedTexts(['addition word problem']);
        ok('embedding requests go to the Hack Club proxy', captured.url === 'https://ai.hackclub.com/proxy/v1/embeddings', captured.url);
        ok('the request carries the bearer key', captured.headers.authorization === 'Bearer hc-semantic-test');
        ok('the request asks for 512 dimensions', captured.body.dimensions === 512, JSON.stringify(captured.body.dimensions));
        ok('the request names the embedding model', captured.body.model === 'openai/text-embedding-3-small');
        ok('the model receives an array input', Array.isArray(captured.body.input));
        ok('a 1536-dimension reply is truncated to 512', vector.length === 512, String(vector.length));
        ok('the stored vector is unit length', Math.abs(Math.sqrt(vector.reduce((n, x) => n + x * x, 0)) - 1) < 1e-6);
    } catch (err) {
        failures.push(`embedding client threw: ${err.message}`);
    } finally {
        global.fetch = realFetch;
        if (savedKey === undefined) delete process.env.HACKCLUBAI_KEY;
        else process.env.HACKCLUBAI_KEY = savedKey;
    }

    /* ------------------------------------------------------- hybrid search */

    ok('search embeds the user query', /embeddings\.embedQuery\(q\)/.test(outlineRoutesSrc));
    ok('hybrid search ranks nearest vectors', /embedding <=> \?::/.test(outlineRoutesSrc));
    ok('hybrid search keeps exact keyword matching', /LOWER\(q\.stem\) LIKE \?/.test(outlineRoutesSrc));
    ok('both candidate sets are merged', /LEFT JOIN vec v ON v\.id = q\.id/.test(outlineRoutesSrc) && /LEFT JOIN kw k ON k\.id = q\.id/.test(outlineRoutesSrc));
    ok('semantic and keyword scores are weighted', /\* 0\.72/.test(outlineRoutesSrc) && /\* 0\.28/.test(outlineRoutesSrc));
    ok('the keyword path survives a missing embedding', /if \(!rows\) \{/.test(outlineRoutesSrc) && /ORDER BY q\.id DESC/.test(outlineRoutesSrc));
    ok('new outline questions are queued for embedding', /embeddings\.queueQuestions\(ids\)/.test(fs.readFileSync(path.join(__dirname, 'outline.js'), 'utf8')));
    ok(
        'the boot creates the schema and index off the request path',
        /\.ensureSchema\(\)/.test(serverSrc) && /\.ensureIndex\(\)/.test(serverSrc) && /\.startAutoSync\(\)/.test(serverSrc)
    );
    ok('superadmin can read embedding progress', /api\/admin\/qbank\/embed\/progress/.test(fs.readFileSync(path.join(__dirname, 'semantic-routes.js'), 'utf8')));
    ok('backfill is cursor-based', /afterId/.test(fs.readFileSync(path.join(__dirname, 'semantic-routes.js'), 'utf8')));

    if (failures.length) {
        console.log(`\n${failures.length} FAILED of ${pass + failures.length}:`);
        failures.forEach((f) => console.log('  ✗ ' + f));
        process.exit(1);
    }
    console.log(`\nAll ${pass} checks passed.`);
})();
