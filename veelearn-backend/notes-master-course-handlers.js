/**
 * Notes → private draft master course, powered by Hack Club AI vision.
 */

const xss = require('xss');
const { hackClubChatCompletion, getHackClubKey } = require('./hackclub-ai');

const MAX_FILES = 8;
const MAX_FILE_BYTES = 8 * 1024 * 1024;
const MAX_UNITS = 6;
const MIN_UNITS = 2;
const MAX_EXTRACT_CHARS = 48000;
const MAX_IMAGES_TO_MODEL = 6;

const IMAGE_MIMES = new Set(['image/png', 'image/jpeg', 'image/jpg', 'image/webp', 'image/gif']);
const PDF_MIMES = new Set(['application/pdf']);
const DOCX_MIMES = new Set([
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
]);
const DOC_MIMES = new Set(['application/msword']);

const HTML_FILTER = new xss.FilterXSS({
    whiteList: {
        h1: ['class'],
        h2: ['class'],
        h3: ['class'],
        h4: ['class'],
        p: ['class'],
        ul: ['class'],
        ol: ['class'],
        li: ['class'],
        strong: [],
        b: [],
        em: [],
        i: [],
        u: [],
        code: ['class'],
        pre: ['class'],
        br: [],
        hr: ['class'],
        blockquote: ['class'],
        table: ['class'],
        thead: [],
        tbody: [],
        tr: [],
        th: ['class'],
        td: ['class'],
        span: ['class'],
        div: ['class', 'data-question-id', 'data-vl-kind'],
        img: ['src', 'alt', 'class']
    },
    stripIgnoreTag: true,
    stripIgnoreTagBody: ['script', 'style', 'iframe', 'object'],
    css: false,
    onTagAttr(tag, name, value) {
        if (name === 'src' && tag === 'img') {
            const v = String(value || '');
            if (v.startsWith('data:image/') || v.startsWith('https://')) return `${name}="${xss.escapeAttrValue(v)}"`;
            return '';
        }
        if (name === 'class') {
            const cleaned = String(value || '')
                .split(/\s+/)
                .filter((c) => /^[a-zA-Z][a-zA-Z0-9_-]{0,40}$/.test(c))
                .slice(0, 8)
                .join(' ');
            return cleaned ? `class="${cleaned}"` : '';
        }
        if (name === 'data-question-id') {
            const n = parseInt(value, 10);
            if (Number.isFinite(n) && n > 0) return `data-question-id="${n}"`;
            return '';
        }
        if (name === 'data-vl-kind') {
            const v = String(value || '').replace(/[^a-zA-Z0-9_-]/g, '').slice(0, 32);
            return v ? `data-vl-kind="${v}"` : '';
        }
        return undefined;
    }
});

function sanitizeCourseHtml(html) {
    return HTML_FILTER.process(String(html || ''));
}

function clip(s, n) {
    const t = String(s || '').trim();
    if (t.length <= n) return t;
    return t.slice(0, n);
}

function decodeBase64Payload(raw) {
    const s = String(raw || '').replace(/^data:[^;]+;base64,/i, '').replace(/\s+/g, '');
    if (!s) return Buffer.alloc(0);
    return Buffer.from(s, 'base64');
}

function guessMime(name, mime) {
    const m = String(mime || '').toLowerCase().split(';')[0].trim();
    if (m) return m;
    const lower = String(name || '').toLowerCase();
    if (lower.endsWith('.pdf')) return 'application/pdf';
    if (lower.endsWith('.png')) return 'image/png';
    if (lower.endsWith('.jpg') || lower.endsWith('.jpeg')) return 'image/jpeg';
    if (lower.endsWith('.webp')) return 'image/webp';
    if (lower.endsWith('.gif')) return 'image/gif';
    if (lower.endsWith('.docx')) return 'application/vnd.openxmlformats-officedocument.wordprocessingml.document';
    if (lower.endsWith('.doc')) return 'application/msword';
    return '';
}

function parseJsonFromModel(text) {
    if (!text) return null;
    let s = String(text)
        .replace(/^\s*```(?:json)?\s*/i, '')
        .replace(/\s*```\s*$/i, '')
        .trim();
    const tryParse = (chunk) => {
        try {
            return JSON.parse(chunk);
        } catch (_) {
            return null;
        }
    };
    let parsed = tryParse(s);
    if (parsed) return parsed;
    const objMatch = s.match(/\{[\s\S]*\}/);
    if (objMatch) {
        parsed = tryParse(objMatch[0]);
        if (parsed) return parsed;
    }
    return null;
}

function stemKey(text) {
    return String(text || '')
        .replace(/<[^>]+>/g, ' ')
        .replace(/&[a-z]+;/gi, ' ')
        .replace(/\s+/g, ' ')
        .trim()
        .toLowerCase()
        .slice(0, 280);
}

function asInsertId(result) {
    if (!result) return null;
    const header = Array.isArray(result) ? result[0] : result;
    return header?.insertId ?? result.insertId ?? null;
}

async function extractPdfText(buffer) {
    let parser;
    try {
        const { PDFParse } = require('pdf-parse');
        parser = new PDFParse({ data: buffer });
        const data = await parser.getText();
        return String(data?.text || '').trim();
    } catch (e) {
        console.warn('[notes-course] pdf text extract failed:', e.message);
        return '';
    } finally {
        if (parser && typeof parser.destroy === 'function') {
            try {
                await parser.destroy();
            } catch (_) { /* ignore */ }
        }
    }
}

async function extractDocx(buffer) {
    try {
        const mammoth = require('mammoth');
        const images = [];
        const htmlResult = await mammoth.convertToHtml(
            { buffer },
            {
                convertImage: mammoth.images.imgElement(async (image) => {
                    try {
                        const imgBuf = await image.read();
                        const type = image.contentType || 'image/png';
                        if (images.length < 4 && imgBuf && imgBuf.length < MAX_FILE_BYTES) {
                            images.push({
                                mime: type,
                                dataUri: `data:${type};base64,${imgBuf.toString('base64')}`
                            });
                        }
                    } catch (_) { /* skip image */ }
                    return { src: '' };
                })
            }
        );
        const textResult = await mammoth.extractRawText({ buffer });
        const text = String(textResult?.value || '')
            .replace(/<[^>]+>/g, ' ')
            .replace(/\s+/g, ' ')
            .trim();
        const htmlText = String(htmlResult?.value || '')
            .replace(/<[^>]+>/g, ' ')
            .replace(/\s+/g, ' ')
            .trim();
        return { text: text || htmlText, images };
    } catch (e) {
        console.warn('[notes-course] docx extract failed:', e.message);
        return { text: '', images: [], error: e.message };
    }
}

async function ingestFiles(files) {
    const notes = [];
    const imageParts = [];
    const pdfParts = [];
    const warnings = [];

    const list = Array.isArray(files) ? files.slice(0, MAX_FILES) : [];
    for (const f of list) {
        const name = clip(f?.name || 'attachment', 120);
        const mime = guessMime(name, f?.mime || f?.type);
        const buf = decodeBase64Payload(f?.dataBase64 || f?.data || '');
        if (!buf.length) {
            warnings.push(`${name}: empty file skipped`);
            continue;
        }
        if (buf.length > MAX_FILE_BYTES) {
            warnings.push(`${name}: larger than 8MB, skipped`);
            continue;
        }

        if (IMAGE_MIMES.has(mime)) {
            const dataUri = `data:${mime === 'image/jpg' ? 'image/jpeg' : mime};base64,${buf.toString('base64')}`;
            if (imageParts.length < MAX_IMAGES_TO_MODEL) {
                imageParts.push({
                    type: 'image_url',
                    image_url: { url: dataUri }
                });
            }
            notes.push(`[Image: ${name}]`);
            continue;
        }

        if (PDF_MIMES.has(mime)) {
            const text = await extractPdfText(buf);
            if (text) notes.push(`[PDF ${name}]\n${clip(text, 20000)}`);
            else notes.push(`[PDF ${name}: scanned or unreadable text; use the attached file.]`);
            pdfParts.push({
                type: 'file',
                file: {
                    filename: name.endsWith('.pdf') ? name : `${name}.pdf`,
                    file_data: `data:application/pdf;base64,${buf.toString('base64')}`
                }
            });
            continue;
        }

        if (DOCX_MIMES.has(mime) || name.toLowerCase().endsWith('.docx')) {
            const extracted = await extractDocx(buf);
            if (extracted.text) notes.push(`[Word ${name}]\n${clip(extracted.text, 20000)}`);
            else notes.push(`[Word ${name}: little text extracted]`);
            if (extracted.error) warnings.push(`${name}: ${extracted.error}`);
            for (const img of extracted.images || []) {
                if (imageParts.length < MAX_IMAGES_TO_MODEL) {
                    imageParts.push({
                        type: 'image_url',
                        image_url: { url: img.dataUri }
                    });
                }
            }
            continue;
        }

        if (DOC_MIMES.has(mime) || name.toLowerCase().endsWith('.doc')) {
            warnings.push(`${name}: old .doc is not supported — export as .docx or PDF`);
            continue;
        }

        warnings.push(`${name}: unsupported type`);
    }

    return {
        extractedText: clip(notes.join('\n\n'), MAX_EXTRACT_CHARS),
        imageParts,
        pdfParts,
        warnings
    };
}

function userContentParts({ promptText, extractedText, imageParts, pdfParts }) {
    const parts = [{ type: 'text', text: promptText }];
    if (extractedText) {
        parts.push({ type: 'text', text: `EXTRACTED_NOTES:\n${extractedText}` });
    }
    for (const p of pdfParts.slice(0, 3)) parts.push(p);
    for (const p of imageParts) parts.push(p);
    return parts;
}

const PLAN_SYSTEM = `You are a curriculum designer for Veelearn. Build a MASTER COURSE outline from a student's notes, homework, and stated struggles.

Rules:
- Combine standard knowledge of the topic with what appears in the notes/HW.
- At least 2 units, at most 6. Split a long chapter into multiple units.
- Units that cover stated struggles get struggle_depth true (those lessons will go much deeper).
- Do not invent a student name. Do not mention being an AI.
- Reply with ONLY JSON (no markdown fences):
{
  "title": "short course title",
  "description": "1-3 sentences",
  "grade_level": 1,
  "units": [
    {
      "title": "Unit title",
      "description": "what this unit covers",
      "struggle_depth": false,
      "concepts": ["concept 1", "concept 2"]
    }
  ]
}
grade_level must be an integer 1-13 (13 = college).`;

const UNIT_SYSTEM = `You write one Veelearn course UNIT as JSON. The student will study this HTML in a course viewer with MathJax.

Hard rules:
- Teach from first principles AND weave in the student's notes/HW wording and examples.
- If struggle_depth is true, go very deep on those weak spots: slower pace, why it is confusing, common mistakes, extra worked examples.
- Include at least 2 fully solved examples in the lesson HTML using <div class="vl-worked-example"> with <h4>Worked example</h4>, <p><strong>Problem:</strong> ...</p>, an ordered list of steps, and <p><strong>Answer:</strong> ...</p>.
- Worked examples MUST NOT be reused as homework. Homework must be new problems.
- Use $...$ or $$...$$ for math. No script tags. No iframes.
- Structure HTML as: <h1>unit title</h1>, audience line, <h2>What you will learn in this unit</h2> + ol, then <hr class="page-break"> between major concepts, each concept as <h2>, explanations, callouts <div class="vl-callout vl-callout-strategy"><div class="vl-callout-body">...</div></div>, worked examples, then <h2>Practice</h2> (homework is attached separately, not inside content_html).
- Homework: 5 to 8 items. Mostly multiple_choice with exactly 4 distinct options. 1-2 short_answer allowed. Include explanation and correct_answer matching one option for MC.
- Reply with ONLY JSON:
{
  "title": "unit title",
  "content_html": "<h1>...</h1>...",
  "homework": [
    {
      "question_text": "plain or simple HTML stem",
      "question_type": "multiple_choice",
      "options": ["A","B","C","D"],
      "correct_answer": "A",
      "explanation": "why",
      "points": 1,
      "difficulty": "easy"
    }
  ]
}
difficulty is easy|medium|hard. points 1-3.`;

function createNotesMasterCourseHandlers({ query, apiResponse }) {
    async function ensureReady() {
        await query(`
            CREATE TABLE IF NOT EXISTS notes_course_jobs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                status ENUM('queued','running','done','error') DEFAULT 'queued',
                step VARCHAR(255) DEFAULT 'queued',
                course_id INT NULL,
                error TEXT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_user (user_id),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE SET NULL
            )
        `);
    }

    async function setJob(id, fields) {
        const cols = [];
        const vals = [];
        for (const [k, v] of Object.entries(fields)) {
            cols.push(`${k} = ?`);
            vals.push(v);
        }
        if (!cols.length) return;
        vals.push(id);
        await query(`UPDATE notes_course_jobs SET ${cols.join(', ')} WHERE id = ?`, vals);
    }

    async function insertCourse({ title, description, content, creatorId, courseType, gradeLevel }) {
        const sql = `INSERT INTO courses (title, description, content, blocks, creator_id, status, creation_time, grade_level, video_url, course_type, gamification_json)
                     VALUES (?, ?, ?, '[]', ?, 'draft', 0, ?, NULL, ?, NULL)`;
        const result = await query(sql, [
            clip(title, 255) || 'Untitled course',
            clip(description, 4000),
            content || '',
            creatorId,
            gradeLevel,
            courseType
        ]);
        return asInsertId(result);
    }

    async function insertQuestion(courseId, q, orderIndex) {
        const type = ['multiple_choice', 'true_false', 'short_answer'].includes(q.question_type)
            ? q.question_type
            : 'multiple_choice';
        let options = Array.isArray(q.options) ? q.options.map((o) => String(o).slice(0, 500)) : null;
        if (type === 'multiple_choice') {
            if (!options || options.length < 2) options = ['A', 'B', 'C', 'D'];
            options = options.slice(0, 6);
        }
        const difficulty = ['easy', 'medium', 'hard', 'stretch'].includes(q.difficulty) ? q.difficulty : 'medium';
        const points = Math.min(4, Math.max(1, parseInt(q.points, 10) || 1));
        const sql = `INSERT INTO course_questions
            (course_id, question_text, question_type, options, correct_answer, explanation, points, order_index, difficulty)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`;
        const result = await query(sql, [
            courseId,
            clip(String(q.question_text || 'Question'), 20000) || 'Question',
            type,
            options ? JSON.stringify(options) : null,
            clip(String(q.correct_answer || (options && options[0]) || ''), 2000) || ' ',
            clip(String(q.explanation || ''), 4000),
            points,
            orderIndex,
            difficulty
        ]);
        return asInsertId(result);
    }

    async function generatePlan(ingest, prompt, struggles, gradeHint) {
        const promptText = [
            'Create a master-course outline from this student material.',
            prompt ? `STUDENT_PROMPT:\n${clip(prompt, 6000)}` : '',
            struggles ? `STRUGGLES (explain these in extra depth):\n${clip(struggles, 4000)}` : '',
            gradeHint ? `GRADE_HINT: ${gradeHint}` : '',
            'Read every attached image/PDF. Use EXTRACTED_NOTES plus visuals.'
        ].filter(Boolean).join('\n\n');

        const content = userContentParts({
            promptText,
            extractedText: ingest.extractedText,
            imageParts: ingest.imageParts,
            pdfParts: ingest.pdfParts
        });

        const raw = await hackClubChatCompletion(
            [
                { role: 'system', content: PLAN_SYSTEM },
                { role: 'user', content }
            ],
            { temperature: 0.3, max_tokens: 4096 }
        );
        const plan = parseJsonFromModel(raw);
        if (!plan || !Array.isArray(plan.units)) {
            const err = new Error('Could not parse a course outline from the model');
            err.code = 'HACKCLUB_PARSE';
            throw err;
        }
        let units = plan.units
            .filter((u) => u && (u.title || u.description))
            .slice(0, MAX_UNITS)
            .map((u) => ({
                title: clip(u.title, 180) || 'Unit',
                description: clip(u.description, 800),
                struggle_depth: Boolean(u.struggle_depth) || Boolean(struggles),
                concepts: Array.isArray(u.concepts) ? u.concepts.map((c) => clip(c, 120)).filter(Boolean).slice(0, 10) : []
            }));
        if (units.length === 1) {
            units.push({
                title: `${units[0].title}: practice and applications`,
                description: 'Deeper practice, applications, and the topics you struggle with.',
                struggle_depth: true,
                concepts: units[0].concepts.slice(0, 4)
            });
        }
        if (units.length < MIN_UNITS) {
            const err = new Error('The outline did not contain at least 2 units');
            err.code = 'HACKCLUB_PARSE';
            throw err;
        }
        let grade = parseInt(plan.grade_level != null ? plan.grade_level : gradeHint, 10);
        if (!Number.isFinite(grade) || grade < 1 || grade > 13) grade = null;
        return {
            title: clip(plan.title, 255) || 'Master course from notes',
            description: clip(plan.description, 2000) || 'A private course built from your notes.',
            grade_level: grade,
            units
        };
    }

    async function generateUnit(ingest, plan, unitSpec, prompt, struggles) {
        const promptText = [
            `Write UNIT JSON for: ${unitSpec.title}`,
            unitSpec.description ? `Unit description: ${unitSpec.description}` : '',
            unitSpec.concepts?.length ? `Concepts: ${unitSpec.concepts.join('; ')}` : '',
            `struggle_depth: ${unitSpec.struggle_depth ? 'true' : 'false'}`,
            `Course title: ${plan.title}`,
            `Other units: ${plan.units.map((u) => u.title).join(' | ')}`,
            prompt ? `STUDENT_PROMPT:\n${clip(prompt, 4000)}` : '',
            struggles ? `STRUGGLES:\n${clip(struggles, 3000)}` : '',
            'Incorporate the attached notes/images/PDFs. Do not copy homework from worked examples.'
        ].filter(Boolean).join('\n\n');

        const content = userContentParts({
            promptText,
            extractedText: ingest.extractedText,
            imageParts: ingest.imageParts,
            pdfParts: ingest.pdfParts
        });

        const call = async () => {
            const raw = await hackClubChatCompletion(
                [
                    { role: 'system', content: UNIT_SYSTEM },
                    { role: 'user', content }
                ],
                { temperature: 0.4, max_tokens: 8192 }
            );
            return parseJsonFromModel(raw);
        };

        let unit = await call();
        if (!unit || !unit.content_html) {
            unit = await call();
        }
        if (!unit || !unit.content_html) {
            const err = new Error(`Could not generate unit: ${unitSpec.title}`);
            err.code = 'HACKCLUB_PARSE';
            throw err;
        }

        const homework = Array.isArray(unit.homework) ? unit.homework : [];
        const exampleKey = stemKey(unit.content_html);
        const cleanedHw = homework
            .filter((q) => q && q.question_text)
            .filter((q) => {
                const k = stemKey(q.question_text);
                return k.length > 8 && !exampleKey.includes(k.slice(0, 80));
            })
            .slice(0, 10);

        return {
            title: clip(unit.title || unitSpec.title, 180),
            content_html: String(unit.content_html),
            homework: cleanedHw
        };
    }

    async function persistPlan(userId, plan, generatedUnits) {
        const overviewParts = [
            `<h1>${clip(plan.title, 255).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')}</h1>`,
            `<p>${clip(plan.description, 2000).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')}</p>`,
            '<h2>Units</h2>',
            '<ol>',
            ...plan.units.map((u) => {
                const t = clip(u.title, 180).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
                const d = clip(u.description || '', 800).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
                return `<li><strong>${t}</strong> — ${d}</li>`;
            }),
            '</ol>',
            '<p>This private course was built from your notes. Open a unit in the sidebar to study worked examples and practice questions.</p>'
        ];
        const masterId = await insertCourse({
            title: plan.title,
            description: plan.description,
            content: overviewParts.join('\n'),
            creatorId: userId,
            courseType: 'master',
            gradeLevel: plan.grade_level
        });
        if (!masterId) throw new Error('Failed to save the master course');

        let prevUnitRowId = null;
        for (let i = 0; i < generatedUnits.length; i++) {
            const u = generatedUnits[i];
            let html = sanitizeCourseHtml(u.content_html);
            const childId = await insertCourse({
                title: u.title,
                description: plan.units[i]?.description || u.title,
                content: html,
                creatorId: userId,
                courseType: 'single',
                gradeLevel: plan.grade_level
            });
            if (!childId) throw new Error(`Failed to save unit: ${u.title}`);

            const placeholders = [];
            const hw = Array.isArray(u.homework) ? u.homework : [];
            for (let qi = 0; qi < hw.length; qi++) {
                const qid = await insertQuestion(childId, hw[qi], qi + 1);
                placeholders.push(
                    `<div class="quiz-question-placeholder" data-question-id="${qid}"></div>`
                );
            }
            if (placeholders.length) {
                html += `\n<hr class="page-break" />\n<h2>Practice</h2>\n${placeholders.join('\n')}`;
                html = sanitizeCourseHtml(html);
                await query('UPDATE courses SET content = ? WHERE id = ?', [html, childId]);
            }

            const unitInsert = await query(
                `INSERT INTO course_units (parent_course_id, child_course_id, order_index, is_draft, prerequisite_unit_id, linked_course_id)
                 VALUES (?, ?, ?, FALSE, ?, ?)`,
                [masterId, childId, i, prevUnitRowId, childId]
            );
            prevUnitRowId = asInsertId(unitInsert);
        }

        return masterId;
    }

    async function runJob(jobId, userId, payload) {
        await setJob(jobId, { status: 'running', step: 'Reading notes…', error: null });
        try {
            const ingest = await ingestFiles(payload.files);
            if (!ingest.extractedText && !ingest.imageParts.length && !ingest.pdfParts.length && !clip(payload.prompt, 20)) {
                throw new Error('Add notes, an attachment, or describe what the course should cover.');
            }

            await setJob(jobId, { step: 'Planning units…' });
            const plan = await generatePlan(
                ingest,
                payload.prompt,
                payload.struggles,
                payload.grade_level
            );

            const generatedUnits = [];
            for (let i = 0; i < plan.units.length; i++) {
                const spec = plan.units[i];
                await setJob(jobId, { step: `Writing ${spec.title}…` });
                const unit = await generateUnit(ingest, plan, spec, payload.prompt, payload.struggles);
                generatedUnits.push(unit);
            }
            if (generatedUnits.length < MIN_UNITS) {
                throw new Error('Need at least 2 units. Try adding more notes or a clearer topic.');
            }

            await setJob(jobId, { step: 'Adding homework and saving…' });
            const courseId = await persistPlan(userId, plan, generatedUnits);
            await setJob(jobId, { status: 'done', step: 'Done', course_id: courseId, error: null });
        } catch (e) {
            const message =
                e.code === 'HACKCLUB_NOT_CONFIGURED'
                    ? 'Hack Club AI is not configured on the server.'
                    : e.code === 'HACKCLUB_RATE_LIMITED'
                      ? 'The AI is busy. Please try again in a few minutes.'
                      : clip(e.message, 500) || 'Course generation failed.';
            console.error('[notes-course] job', jobId, e);
            await setJob(jobId, { status: 'error', step: 'Failed', error: message }).catch(() => {});
        }
    }

    async function startJob(req, res) {
        if (!getHackClubKey()) {
            return apiResponse(res, 503, 'Hack Club AI is not configured');
        }
        const userId = req.user.id;
        const prompt = clip(req.body?.prompt, 8000);
        const struggles = clip(req.body?.struggles, 4000);
        let grade_level = req.body?.grade_level;
        if (grade_level != null && grade_level !== '') {
            grade_level = parseInt(grade_level, 10);
            if (!Number.isFinite(grade_level) || grade_level < 1 || grade_level > 13) {
                return apiResponse(res, 400, 'Grade level must be 1–13');
            }
        } else {
            grade_level = null;
        }
        const files = Array.isArray(req.body?.files) ? req.body.files : [];
        if (files.length > MAX_FILES) {
            return apiResponse(res, 400, `At most ${MAX_FILES} files`);
        }
        if (!prompt && !struggles && files.length === 0) {
            return apiResponse(res, 400, 'Type a topic or attach notes');
        }

        await ensureReady();
        const result = await query(
            `INSERT INTO notes_course_jobs (user_id, status, step) VALUES (?, 'queued', 'queued')`,
            [userId]
        );
        const jobId = asInsertId(result);
        if (!jobId) {
            return apiResponse(res, 500, 'Could not start course generation');
        }
        setImmediate(() => {
            runJob(jobId, userId, { prompt, struggles, grade_level, files }).catch((e) => {
                console.error('[notes-course] runJob', e);
            });
        });
        return apiResponse(res, 202, 'Course generation started', { jobId });
    }

    async function getJob(req, res) {
        const userId = req.user.id;
        const jobId = parseInt(req.params.jobId, 10);
        if (!Number.isFinite(jobId)) {
            return apiResponse(res, 400, 'Invalid job');
        }
        await ensureReady();
        const rows = await query(
            'SELECT id, status, step, course_id, error, created_at, updated_at FROM notes_course_jobs WHERE id = ? AND user_id = ? LIMIT 1',
            [jobId, userId]
        );
        if (!Array.isArray(rows) || !rows.length) {
            return apiResponse(res, 404, 'Job not found');
        }
        const row = rows[0];
        return apiResponse(res, 200, 'Job status', {
            jobId: row.id,
            status: row.status,
            step: row.step,
            courseId: row.course_id,
            error: row.error
        });
    }

    return { ensureReady, startJob, getJob };
}

module.exports = { createNotesMasterCourseHandlers };
