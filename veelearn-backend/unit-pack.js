'use strict';

/**
 * A unit pack: the lesson a learner reads for one skill, and the practice
 * questions written from that lesson.
 *
 * The outline is the syllabus, not the script. It supplies the topic, the skill
 * names and the scope; the model writes its own teaching from that, decides how
 * many worked examples the idea needs, and then writes the questions from the
 * lesson it just wrote. That is what keeps the lesson and the cards at the same
 * difficulty — they used to be produced by two unrelated calls, so one was a
 * concept and the other a recall flashcard.
 *
 * Cached in `unit_packs` by (skill, learner level): a reload, a second learner,
 * or a resumed session re-reads the same pack instead of paying for it again.
 */

const LETTERS = 'ABCDEFGH';
const PACK_MIN = 8;
const PACK_MAX = 12;

const LESSON_MODEL = String(process.env.VEELEARN_LESSON_MODEL || '').trim() || 'openai/gpt-6-luna';
const LESSON_REASONING = /^openai\/gpt-6-luna/i.test(LESSON_MODEL) ? { effort: 'none' } : null;
const QUESTION_MODEL = String(process.env.VEELEARN_OUTLINE_MODEL || '').trim() || 'google/gemini-3.5-flash-lite';

/** The lesson's fixed sections, in the order the page draws them. */
const LESSON_HEADINGS = [
    '## What this is',
    '## The method',
    '## Worked examples',
    '## Where it goes wrong',
    '## Try it yourself'
];

/**
 * The lesson brief. The outline's own words are context for the model, never a
 * script to paraphrase: "write your own lesson" is the point of the pack.
 */
function lessonPrompt({
    title,
    scope,
    misconceptions,
    unitLabel,
    courseTitle,
    targetTier,
    level,
    fresh
} = {}) {
    const traps = (Array.isArray(misconceptions) ? misconceptions : []).filter(Boolean).slice(0, 4);
    return [
        `Write the learning section of a course for this skill: ${title}.`,
        unitLabel ? `It is part of ${unitLabel}.` : '',
        courseTitle ? `Course: ${courseTitle}.` : '',
        '',
        'The course outline below is the syllabus, not the lesson. It names the topic and the skills.',
        'Do NOT paraphrase it, quote it, restate it as a plan, or copy its sentences. Teach the idea',
        'yourself, in your own words, as a teacher would at a whiteboard.',
        '',
        scope ? `Outline scope (background only):\n${String(scope).slice(0, 4000)}` : '',
        traps.length ? `Traps the learner is likely to fall into (cover each one):\n- ${traps.join('\n- ')}` : '',
        '',
        `Write these sections, with these exact headings, and nothing before the first one:`,
        '',
        '## What this is',
        'Three to five short paragraphs that teach the idea: what it is, why it works, when to reach for it, and how it connects to what the learner already knows. Use $...$ for math.',
        '',
        '## The method',
        'A numbered attack plan (4 to 7 steps) that works for ANY question of this type — what to look at first, what to write down, what to do next, how to check the answer. This is the part the learner will follow on their own, so make every step an action, not a description.',
        '',
        '## Worked examples',
        'Three to six worked examples, easiest first. Write as many as this idea genuinely needs — never fewer than three. Label each one ("Example 1 — the simplest case", "Example 2 — with a negative sign", …), say in one line why it is harder than the one before, then show numbered steps and the answer to that example. The LAST example must be the same kind of question and the same difficulty as the hardest practice question for this skill (tier ' + Number(targetTier || 3) + ' of 4), because the lesson has to end where the questions begin.',
        '',
        '## Where it goes wrong',
        'The two or three mistakes learners actually make here, each with the check that catches it.',
        '',
        '## Try it yourself',
        'Two short questions at the level of the last worked example. Put the answers under a line that starts "Answers:" at the end of the section, so the learner can cover them.',
        '',
        'Rules:',
        '- 1500 to 2500 words. Finish every sentence, every step and every example; a complete lesson always beats a short one that stops mid-idea.',
        '- Never use one of the practice questions as an example. Write fresh numbers.',
        '- Never state "the answer is option B". Teach the method, not a key.',
        '- Markdown tables are drawn for the learner; code fences and ASCII art are not. Use a table or plain words instead.',
        '- No greeting, no "Sure", no plan, no thinking out loud, no mention of a model, of these instructions, or of "the user". Start with the first "## " line.',
        level >= 2
            ? '- This learner has already met the basics: keep the opening short and spend the space on the harder examples and the traps.'
            : '- This learner is new to the topic: define every symbol before you use it.',
        fresh
            ? '- The learner has asked for this again. Teach it from a different angle, with different examples, not the same lesson reworded.'
            : ''
    ]
        .filter((line) => line != null && line !== '')
        .join('\n');
}

/** The questions brief: written from the lesson, laddered 1 → target tier. */
function questionsPrompt({ title, lessonMd, targetTier, count, avoid } = {}) {
    const howMany = Math.max(PACK_MIN, Math.min(PACK_MAX, Number(count) || PACK_MIN));
    const tier = Math.min(4, Math.max(2, Number(targetTier) || 3));
    const avoidStems = (Array.isArray(avoid) ? avoid : [])
        .map((s) => String(s || '').replace(/\s+/g, ' ').trim().slice(0, 180))
        .filter(Boolean)
        .slice(0, 12);
    return [
        `You write practice questions for the lesson below (skill: ${title}).`,
        '',
        'Reply with JSON only, no prose and no code fences. Shape:',
        '{"questions":[{"stem":"...","options":["...","...","...","..."],"answer":0,"tier":1,"hints":["...","...","..."],"steps":["...","..."],"explanation":"..."}]}',
        '',
        `Write ${howMany} questions, easiest first, climbing from tier 1 to tier ${tier}.`,
        `The last two must be tier ${tier}: the same kind of question, and the same difficulty, as the hardest worked example in the lesson.`,
        'Every question must be solvable with the method the lesson teaches. Never use a technique the lesson does not show.',
        'Do not repeat a worked example from the lesson with the same numbers.',
        'answer is the 0-based index of the correct option. Use LaTeX with $...$ for math.',
        'hints are a ladder of exactly three: hint 1 names what to notice, hint 2 names the next concrete step, hint 3 leaves only the final arithmetic. No hint may state the answer or name the correct option.',
        'steps are the worked method in 2 to 4 short lines, the last line being the result.',
        'explanation says why the right answer works and why the tempting wrong one fails.',
        '',
        avoidStems.length ? `Do not repeat or paraphrase these existing questions:\n- ${avoidStems.join('\n- ')}` : '',
        '',
        `Lesson:\n${String(lessonMd || '').slice(0, 8000)}`
    ]
        .filter((line) => line != null && line !== '')
        .join('\n');
}

/** The model's JSON, forgivingly parsed. */
function parseJsonLoose(text) {
    const raw = String(text || '')
        .replace(/```(?:json)?/gi, '')
        .trim();
    const a = raw.indexOf('{');
    const b = raw.lastIndexOf('}');
    if (a === -1 || b === -1) return null;
    try {
        return JSON.parse(raw.slice(a, b + 1));
    } catch (_) {
        return null;
    }
}

function normaliseOptionText(value) {
    return String(value == null ? '' : value)
        .replace(/\s+/g, ' ')
        .trim();
}

/**
 * Validate one model-written question. Anything that cannot be graded
 * deterministically is dropped rather than shown with a guessed key.
 */
function cleanQuestion(raw, { tierMax = 3 } = {}) {
    if (!raw || typeof raw !== 'object') return null;
    const stem = normaliseOptionText(raw.stem).slice(0, 900);
    if (stem.length < 8) return null;
    const texts = (Array.isArray(raw.options) ? raw.options : [])
        .map(normaliseOptionText)
        .filter(Boolean)
        .slice(0, 6);
    if (texts.length < 3) return null;
    const uniq = new Set(texts.map((t) => t.toLowerCase()));
    if (uniq.size < 3) return null;

    let key = null;
    if (typeof raw.answer === 'number' && texts[raw.answer] != null) key = raw.answer;
    else if (typeof raw.answer === 'string') {
        const want = normaliseOptionText(raw.answer).toLowerCase();
        const at = texts.findIndex((t) => t.toLowerCase() === want);
        if (at >= 0) key = at;
        else if (want.length === 1 && LETTERS.toLowerCase().includes(want)) {
            const i = LETTERS.toLowerCase().indexOf(want);
            if (i < texts.length) key = i;
        }
    }
    if (key == null) return null;

    // Shuffle so the key is not always A: a bank where A is always right teaches
    // learners to click A.
    const order = texts.map((t, i) => i);
    for (let i = order.length - 1; i > 0; i -= 1) {
        const j = Math.floor(Math.random() * (i + 1));
        const tmp = order[i];
        order[i] = order[j];
        order[j] = tmp;
    }
    const options = order.map((from, i) => ({ k: LETTERS[i], t: texts[from] }));
    const answerAt = order.indexOf(key);

    const hints = (Array.isArray(raw.hints) ? raw.hints : [])
        .map(normaliseOptionText)
        .filter(Boolean)
        .slice(0, 3);
    const steps = (Array.isArray(raw.steps) ? raw.steps : [])
        .map(normaliseOptionText)
        .filter(Boolean)
        .slice(0, 4);
    const explanation = normaliseOptionText(raw.explanation).slice(0, 700);

    return {
        stem,
        options,
        answer: options[answerAt] ? options[answerAt].k : 'A',
        tier: Math.min(tierMax, Math.max(1, parseInt(raw.tier, 10) || 1)),
        hints: hints.length ? hints : steps.slice(0, 2),
        steps: steps.length ? steps : explanation ? [explanation] : [],
        explanation
    };
}

function createUnitPack({ query, log, chatStream, clean } = {}) {
    const info = (log && log.info) || (() => {});
    const warn = (log && log.warn) || ((m) => console.warn(m));
    const cleanLesson = typeof clean === 'function' ? clean : (t) => String(t || '').trim();

    // One lesson and one question batch in flight per (skill, level). Two tabs
    // opening the same unit must not write two packs, and the question writer
    // must not start a second lesson while the first one is still streaming.
    const running = new Map();
    const lessonInflight = new Map();

    async function loadRow(skillId, learnerLevel) {
        try {
            const rows = await query(
                'SELECT id, skill_id, learner_level, lesson_md, question_ids, lesson_at FROM unit_packs WHERE skill_id = ? AND learner_level = ? LIMIT 1',
                [Number(skillId), Number(learnerLevel || 0)]
            );
            return rows[0] || null;
        } catch (e) {
            info(`[unit-pack] cache read skipped: ${e.message}`);
            return null;
        }
    }

    async function saveRow(skillId, learnerLevel, { lessonMd, questionIds } = {}) {
        const level = Number(learnerLevel || 0);
        try {
            await query(
                `INSERT IGNORE INTO unit_packs (skill_id, learner_level, lesson_md, question_ids, lesson_at)
                 VALUES (?, ?, ?, ?, NOW())`,
                [
                    Number(skillId),
                    level,
                    lessonMd != null ? String(lessonMd).slice(0, 40000) : null,
                    questionIds ? JSON.stringify(questionIds.slice(0, 40)) : null
                ]
            );
            if (lessonMd != null) {
                await query('UPDATE unit_packs SET lesson_md = ?, lesson_at = NOW() WHERE skill_id = ? AND learner_level = ?', [
                    String(lessonMd).slice(0, 40000),
                    Number(skillId),
                    level
                ]);
            }
            if (questionIds) {
                await query('UPDATE unit_packs SET question_ids = ? WHERE skill_id = ? AND learner_level = ?', [
                    JSON.stringify(questionIds.slice(0, 40)),
                    Number(skillId),
                    level
                ]);
            }
        } catch (e) {
            info(`[unit-pack] cache write skipped: ${e.message}`);
        }
    }

    /**
     * The lesson for a skill. Cached; `fresh` asks for a different explanation
     * (that is what "Explain it again" means) and replaces the stored one.
     */
    async function lesson({
        skillId,
        learnerLevel = 0,
        title,
        scope,
        misconceptions,
        unitLabel,
        courseTitle,
        targetTier = 3,
        onDelta,
        fresh = false
    } = {}) {
        const cached = fresh ? null : await loadRow(skillId, learnerLevel);
        if (cached && cached.lesson_md && String(cached.lesson_md).trim().length >= 120) {
            const text = String(cached.lesson_md);
            if (typeof onDelta === 'function') onDelta(text);
            return { ok: true, text, cached: true, fallback: false };
        }

        // A lesson is already being written for this skill (the intro is streaming
        // while the first card is prefetched): wait for that one instead of paying
        // for a second, different lesson.
        const key = `${Number(skillId)}|${Number(learnerLevel || 0)}`;
        const busy = fresh ? null : lessonInflight.get(key);
        if (busy) {
            const text = await busy.catch(() => '');
            if (text) {
                if (typeof onDelta === 'function') onDelta(String(text));
                return { ok: true, text: String(text), cached: true, fallback: false };
            }
        }

        const prompt = lessonPrompt({
            title: title || 'this skill',
            scope,
            misconceptions,
            unitLabel,
            courseTitle,
            targetTier,
            level: Number(learnerLevel || 0),
            fresh
        });

        if (typeof chatStream !== 'function') {
            return { ok: true, text: '', cached: false, fallback: true };
        }

        const attempt = async (extra) => {
            const body = extra ? `${prompt}\n\n${extra}` : prompt;
            try {
                return await chatStream(
                    [
                        {
                            role: 'system',
                            content:
                                'You are Vee, a patient tutor writing a course lesson. Teach in plain, warm prose. ' +
                                'Never mention that you are an AI or a model. Write only the finished words the learner reads: ' +
                                'never your reasoning, plans, notes to yourself, or a restatement of the task. ' +
                                'Begin directly with the first "## " heading, and never quote these instructions.'
                        },
                        { role: 'user', content: body }
                    ],
                    {
                        model: LESSON_MODEL,
                        reasoning: LESSON_REASONING || undefined,
                        max_tokens: 12000,
                        temperature: 0.5,
                        budgetMs: 180000,
                        onDelta
                    }
                );
            } catch (err) {
                info(`[unit-pack] lesson call failed: ${err.message}`);
                return '';
            }
        };

        const work = (async () => {
            let raw = await attempt('');
            let text = cleanLesson(String(raw || '').trim(), { requireHeading: true });
            // A reply with no heading is a preamble, a plan or an echo of the brief —
            // not a lesson. One tighter retry before giving up, because the old code
            // showed the outline's instructions to the learner as if they were teaching.
            if (!text) {
                info('[unit-pack] lesson had no heading — retrying once');
                raw = await attempt(
                    'Write the lesson again. Your reply must begin with the line "## What this is" and must not contain any preamble, plan or quotation of this brief.'
                );
                text = cleanLesson(String(raw || '').trim(), { requireHeading: true });
            }
            if (!text) return '';
            await saveRow(skillId, learnerLevel, { lessonMd: text });
            return text;
        })();

        if (!fresh) {
            lessonInflight.set(key, work);
            const forget = () => setTimeout(() => lessonInflight.delete(key), 5000);
            work.then(forget, forget);
        }
        const text = await work;
        if (!text) return { ok: true, text: '', cached: false, fallback: true };
        return { ok: true, text, cached: false, fallback: false };
    }

    /** The cached question ids for a pack, in the order they were written. */
    async function cachedQuestions(skillId, learnerLevel) {
        const row = await loadRow(skillId, learnerLevel);
        if (!row || !row.question_ids) return [];
        try {
            const ids = JSON.parse(row.question_ids);
            return Array.isArray(ids) ? ids.map(Number).filter(Boolean) : [];
        } catch (_) {
            return [];
        }
    }

    async function insertQuestion(skillId, courseId, item) {
        const crypto = require('crypto');
        const stemHash = crypto.createHash('sha256').update(item.stem).digest('hex');
        try {
            await query(
                `INSERT IGNORE INTO qbank_items
                    (skill_id, tier, qtype, stem, stem_hash, options, answer, hints, solution_steps, source, course_id, live)
                 VALUES (?, ?, 'mcq', ?, ?, ?, ?, ?, ?, ?, ?, 1)`,
                [
                    Number(skillId),
                    Number(item.tier || 1),
                    item.stem,
                    stemHash,
                    JSON.stringify(item.options),
                    item.answer,
                    JSON.stringify(item.hints || []),
                    JSON.stringify(item.steps || []),
                    courseId ? 'course' : 'authored',
                    courseId ? Number(courseId) : null
                ]
            );
            const rows = await query('SELECT id FROM qbank_items WHERE stem_hash = ? LIMIT 1', [stemHash]);
            return rows[0] ? Number(rows[0].id) : null;
        } catch (e) {
            warn(`[unit-pack] question skipped: ${e.message}`);
            return null;
        }
    }

    /**
     * Write (or reuse) the practice questions for a pack. They are written from
     * the lesson, so a card can never test something the lesson did not teach.
     */
    async function questions({
        skillId,
        learnerLevel = 0,
        title,
        scope,
        misconceptions,
        unitLabel,
        courseTitle,
        courseId,
        targetTier = 3,
        count = PACK_MIN,
        force = false
    } = {}) {
        const key = `${Number(skillId)}|${Number(learnerLevel || 0)}`;
        if (!force) {
            const have = await cachedQuestions(skillId, learnerLevel);
            // A usable pack is not rewritten just because the model returned fewer
            // questions than asked: four is enough to teach and practise with.
            if (have.length >= 4) return have;
        }
        const busy = running.get(key);
        if (busy) return busy;

        const work = (async () => {
            // The questions are written from the lesson, so a pack with no lesson
            // yet writes one first (no streaming: nobody is watching this one).
            let row = await loadRow(skillId, learnerLevel);
            let lessonMd = row && row.lesson_md ? String(row.lesson_md) : '';
            if (!lessonMd) {
                // The intro may be streaming this lesson right now; take its text
                // rather than starting a competing one.
                const streaming = lessonInflight.get(key);
                if (streaming) lessonMd = await streaming.catch(() => '');
            }
            if (!lessonMd) {
                const made = await lesson({
                    skillId,
                    learnerLevel,
                    title,
                    scope,
                    misconceptions,
                    unitLabel,
                    courseTitle,
                    targetTier
                });
                lessonMd = made && made.text ? String(made.text) : '';
            }
            if (!lessonMd) return cachedQuestions(skillId, learnerLevel);

            const existing = await cachedQuestions(skillId, learnerLevel);
            let raw = '';
            try {
                raw = await require('./ai-chat').aiChatCompletion(
                    [
                        {
                            role: 'system',
                            content:
                                'You write practice questions for a study app. Reply with JSON only, no prose, no code fences.'
                        },
                        {
                            role: 'user',
                            content: questionsPrompt({
                                title: title || 'this skill',
                                lessonMd,
                                targetTier,
                                count,
                                avoid: existing
                            })
                        }
                    ],
                    {
                        model: QUESTION_MODEL,
                        max_tokens: Math.min(4000, 1200 + Math.max(PACK_MIN, count) * 420),
                        temperature: 0.4,
                        jsonMust: true,
                        timeoutMs: 45000
                    }
                );
            } catch (err) {
                warn(`[unit-pack] question call failed: ${err.message}`);
                return existing;
            }
            const payload = parseJsonLoose(raw) || {};
            const list = Array.isArray(payload.questions) ? payload.questions : [];
            const tierMax = Math.min(4, Math.max(2, Number(targetTier) || 3));
            const seen = new Set();
            const ids = existing.slice();
            for (const rawQuestion of list) {
                const item = cleanQuestion(rawQuestion, { tierMax });
                if (!item) continue;
                const dedupe = item.stem.toLowerCase();
                if (seen.has(dedupe)) continue;
                seen.add(dedupe);
                const id = await insertQuestion(skillId, courseId, item);
                if (id && !ids.includes(id)) ids.push(id);
            }
            if (ids.length) {
                await saveRow(skillId, learnerLevel, { questionIds: ids });
                try {
                    require('./embeddings').queueQuestions(ids);
                } catch (_) {
                    /* semantic search is optional */
                }
            }
            return ids;
        })();

        running.set(key, work);
        const done = () => setTimeout(() => running.delete(key), 5000);
        work.then(done, done);
        return work;
    }

    /** Make sure the pack exists (lesson + questions) before a card is served. */
    async function ensureQuestions(opts = {}) {
        return questions(opts);
    }

    /** Three more of the same type, for a unit that is not solid yet. */
    async function moreQuestions(opts = {}) {
        return questions({ ...opts, count: 3, force: true });
    }

    return { lesson, questions, ensureQuestions, moreQuestions, cachedQuestions, loadRow, saveRow };
}

module.exports = createUnitPack;
module.exports.lessonPrompt = lessonPrompt;
module.exports.questionsPrompt = questionsPrompt;
module.exports.cleanQuestion = cleanQuestion;
module.exports.parseJsonLoose = parseJsonLoose;
module.exports.LESSON_HEADINGS = LESSON_HEADINGS;
module.exports.LESSON_MODEL = LESSON_MODEL;
module.exports.PACK_MIN = PACK_MIN;
module.exports.PACK_MAX = PACK_MAX;
