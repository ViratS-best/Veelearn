'use strict';

/**
 * Course -> outline builder.
 *
 * The body of a course is already a map: h2 sections are the topics, each has
 * teaching prose, a common slip and quiz questions. This module reads that
 * structure and returns the outline shape `outline.js` saves, with a teaching
 * brief and diagram/model suggestions on every skill.
 *
 * The "… Complete" index courses are the exception: their body only lists the
 * eight units, so `assembleFromSiblings` builds them from the matching Unit
 * courses that hold the real content and questions.
 *
 * Pure functions only — no database, no HTTP — so the batch endpoint, the CLI
 * script and the tests all share one implementation.
 */

const LETTERS = 'ABCDEFGH';

const META =
    /^(what you will learn|practice|practice set|summary|review|unit review|exercises?|answer key|answers|start here|how to work|you will move|final|stretch|mixed|self[- ]?check|check yourself|test|quiz)/i;

const META_LINE =
    /^(where this fits|this is step|work through|read (the|one|each)|do not|don'?t|look at|build the rule|cover the|do the quick|only move|say in one|explain, in your|name the mistake|check yourself|start here|how to work|you will move|remember to|try the|now try|pause|take a breath|this section contains|the (next|previous) stage|stop and|note:|tip:)/i;

const STOP = new Set(
    ('the a an and or of to in on for with from by as at is are was were be been being this that these those it its ' +
        'you your we our they their he she his her them then than so if but not no yes can could should would may might ' +
        'will shall do does did done have has had make makes made use used using one two more most less least very ' +
        'what which who whom whose when where why how all any both each few other some such only own same too also ' +
        'into over under about between through during before after above below out off again further once here there ' +
        'because while just like get got go goes going new now first second third step page unit section question ' +
        'answer choice problem solve solving find finding work works worked show shows shown see look read try')
        .split(/\s+/)
        .filter(Boolean)
);

function decode(text) {
    return String(text || '')
        .replace(/&nbsp;/gi, ' ')
        .replace(/&amp;/gi, '&')
        .replace(/&lt;/gi, '<')
        .replace(/&gt;/gi, '>')
        .replace(/&quot;/gi, '"')
        .replace(/&#39;|&apos;/gi, "'")
        .replace(/&mdash;/gi, '—')
        .replace(/&ndash;/gi, '–')
        .replace(/&hellip;/gi, '…')
        .replace(/&#(\d+);/g, (_m, n) => String.fromCharCode(Number(n)))
        .replace(/&[a-z]+;/gi, ' ');
}

function inline(html) {
    return decode(String(html || '').replace(/<[^>]+>/g, ' '))
        .replace(/\s+/g, ' ')
        .trim();
}

function toText(html) {
    const stripped = String(html || '')
        .replace(/<script[\s\S]*?<\/script>/gi, ' ')
        .replace(/<style[\s\S]*?<\/style>/gi, ' ')
        .replace(/<br\s*\/?>/gi, '\n')
        .replace(/<\/(p|div|li|h[1-6]|tr|blockquote|section)>/gi, '\n')
        .replace(/<li[^>]*>/gi, '\n');
    return decode(stripped.replace(/<[^>]+>/g, ' '))
        .split('\n')
        .map((line) => line.replace(/[ \t]+/g, ' ').trim())
        .filter(Boolean)
        .join('\n');
}

function words(text) {
    return String(text || '')
        .toLowerCase()
        .replace(/[^a-z0-9' ]+/g, ' ')
        .split(/\s+/)
        .filter((w) => w.length > 3 && !STOP.has(w));
}

function tokenSet(text) {
    return new Set(words(text));
}

function overlap(a, b) {
    let n = 0;
    for (const w of a) if (b.has(w)) n += 1;
    return n;
}

/* ------------------------------------------------------------------ parsing */

function h2Sections(html) {
    const parts = String(html || '').split(/<h2[^>]*>/i);
    const out = [];
    for (const part of parts.slice(1)) {
        const end = part.search(/<\/h2>/i);
        if (end < 0) continue;
        const title = inline(part.slice(0, end));
        const body = part.slice(end + 5);
        if (!title) continue;
        out.push({ title, body, text: toText(body) });
    }
    return out;
}

function h1Sections(html) {
    const parts = String(html || '').split(/<h1[^>]*>/i);
    const out = [];
    for (const part of parts.slice(1)) {
        const end = part.search(/<\/h1>/i);
        if (end < 0) continue;
        const title = inline(part.slice(0, end));
        const body = part.slice(end + 5);
        if (!title) continue;
        out.push({ title, body, text: toText(body) });
    }
    return out;
}

/** The real topics of a course body, in reading order. */
function topicsOf(course) {
    let sections = h2Sections(course.content).filter((s) => s.title && !META.test(s.title));
    if (sections.length < 2) {
        const h1 = h1Sections(course.content).filter((s) => s.title && !META.test(s.title));
        if (h1.length > sections.length) sections = h1;
    }
    if (!sections.length) {
        const text = toText(course.content);
        if (text.length > 120) sections = [{ title: course.title, body: course.content, text }];
    }
    return sections;
}

/** The teaching meat of a section, without the workbook stage directions. */
function coreOf(section) {
    const lines = String(section.text || '')
        .split('\n')
        .map((l) => l.replace(/\s+/g, ' ').trim())
        .filter(Boolean)
        .filter((line) => !META_LINE.test(line))
        .filter((line) => !/^\d+\s*[·.]\s*[A-Z]/.test(line))
        .filter((line) => !/^(unit|step)\s+\d+\b/i.test(line));
    const meaty = lines.filter((line) => line.length >= 40);
    const chosen = [];
    let used = 0;
    const scored = meaty
        .map((line) => {
            let score = 0;
            if (/[=+\-×÷]|\$|\\frac|\\sqrt/.test(line)) score += 3;
            if (/\d/.test(line)) score += 1;
            if (/means|because|so |therefore|rule|formula|equal|represents/i.test(line)) score += 2;
            if (/^(problem|worked example|answer)/i.test(line)) score += 2;
            return { line, score };
        })
        .sort((a, b) => b.score - a.score);
    for (const item of scored) {
        if (used + item.line.length > 760) continue;
        chosen.push(item.line);
        used += item.line.length + 1;
        if (used > 560) break;
    }
    if (!chosen.length) return '';
    return chosen.join(' ');
}

function slipOf(section) {
    const text = String(section.text || '');
    const at = text.search(/where people slip|common (mistake|error)|watch out/i);
    if (at < 0) return '';
    const tail = text
        .slice(at, at + 500)
        .split('\n')
        .map((l) => l.trim())
        .filter(Boolean)
        .slice(1, 3)
        .join(' ');
    const slip = inline(tail);
    if (slip.length < 12) return '';
    return slip.slice(0, 220);
}

/* -------------------------------------------------------------- diagrams */

const DIAGRAM_RULES = [
    [
        /fraction|ratio|proportion|percent|decimal|place value/i,
        ['fraction bars split into equal parts', 'a double number line with both quantities marked']
    ],
    [
        /equation|inequalit|variable|algebra|expression|factor|polynomial|simplif/i,
        ['a balance scale with the same operation done to both pans', 'a bar model where the unknown is one labelled block']
    ],
    [
        /quadratic|parabola|function|graph|slope|linear|exponential|logarithm|transform/i,
        ['a coordinate plot with intercepts and the key point labelled', 'an animation that slides one parameter and shows the graph change']
    ],
    [
        /angle|triangle|polygon|circle|geometr|trig|sine|cosine|tangent|vector/i,
        ['a labelled figure with every side and angle marked', 'a unit circle with the angle sweeping and the sine/cosine projections drawn']
    ],
    [
        /area|volume|perimeter|surface/i,
        ['a labelled solid with its dimensions, then a slice-by-slice animation', 'a grid tiled by unit squares or cubes']
    ],
    [
        /probability|combinat|permutation|count|chance/i,
        ['a tree diagram of the choices', 'a grid/area model with the favourable outcomes shaded']
    ],
    [
        /derivative|integral|limit|calculus|rate of change|series|sequence/i,
        ['a curve with a secant sliding into the tangent line', 'an area under the curve built from thinner and thinner rectangles']
    ],
    [
        /matrix|determinant|complex number/i,
        ['arrows on a grid with components projected onto the axes']
    ],
    [
        /atom|molecul|bond|reaction|acid|base|equilibri|kinetic|thermo|electrochem|periodic|stoichiometr/i,
        ['particle diagrams before, during and after the change', 'an energy profile with activation energy and ΔH labelled']
    ],
    [
        /force|motion|velocity|accelerat|momentum|energy|circuit|field|wave|optic|electric|magnet/i,
        ['a free-body diagram with every force arrow labelled', 'a motion graph drawn live as the quantity changes']
    ],
    [
        /cell|dna|gene|protein|ecosystem|evolution|organism|enzyme|photosynthes|respiration/i,
        ['a labelled cell/organism diagram with the key parts named', 'a flowchart tracing the process from input to output']
    ],
    [
        /code|loop|array|recursion|algorithm|complexity|data structure|variable scope/i,
        ['a trace table stepping through the code line by line', 'boxes for memory/array state at each step']
    ],
    [
        /grammar|sentence|essay|poem|text|author|rhetoric|reading|vocab|writing/i,
        ['a colour-coded annotation of one example sentence', 'a two-column quote → effect chart']
    ],
    [
        /history|revolution|war|empire|century|treaty|civilization|ancient/i,
        ['a timeline with causes above and consequences below', 'a map with regions and arrows of movement']
    ],
    [
        /econom|supply|demand|market|inflation|gdp|trade|money|budget/i,
        ['supply and demand curves with the shift animated', 'a circular flow diagram']
    ],
    [
        /statistic|mean|median|mode|distribution|data|survey|graph reading/i,
        ['a dot plot or histogram with the centre marked', 'a box plot with the quartiles labelled']
    ]
];

function diagramIdeas(course, topic, text) {
    const hay = `${course.title} ${topic} ${text}`;
    for (const [pattern, ideas] of DIAGRAM_RULES) {
        if (pattern.test(hay)) return ideas;
    }
    return [
        'a labelled diagram of the idea with the key quantities named',
        'a step-by-step animation that changes one quantity at a time'
    ];
}

/* ------------------------------------------------------------- questions */

function optionList(raw) {
    let list = raw;
    if (typeof list === 'string') {
        try {
            list = JSON.parse(list);
        } catch (_) {
            list = [];
        }
    }
    return Array.isArray(list) ? list.map((o) => (typeof o === 'string' ? o : o && (o.t || o.text || o.option_text))) : [];
}

function toOutlineQuestion(row) {
    const stem = inline(row.question_text || row.stem || row.question || '');
    if (stem.length < 8) return null;
    const options = optionList(row.options)
        .map((t, i) => ({ k: LETTERS[i], t: inline(t).slice(0, 300) }))
        .filter((o) => o.t);
    if (options.length < 2) return null;
    const correct = inline(row.correct_answer != null ? row.correct_answer : row.answer);
    let index = options.findIndex((o) => o.t === correct);
    if (index < 0 && /^[A-H]$/i.test(correct)) index = LETTERS.indexOf(correct.toUpperCase());
    if (index < 0) index = Number(row.correct_index);
    if (!(index >= 0 && index < options.length)) return null;
    return {
        stem: stem.slice(0, 1200),
        options: options.slice(0, 6),
        answer: options[index].k,
        hint: inline(row.hint || '').slice(0, 400),
        why: inline(row.explanation || row.why || '').slice(0, 700),
        visual: row.visual && typeof row.visual === 'object' ? row.visual : null,
        source: 'authored',
        attribution: ''
    };
}

function courseQuestions(course) {
    return (course.questions || []).map(toOutlineQuestion).filter(Boolean);
}

/* ----------------------------------------------------------- outline build */

function teachFor(course, topic, count) {
    const core = coreOf(topic);
    const slip = slipOf(topic);
    const ideas = diagramIdeas(course, topic.title, String(topic.text || '').slice(0, 1200));
    let teach = `${topic.title}. `;
    if (core) teach += `${core} `;
    teach +=
        'Teach it in plain words: begin with one concrete example, say the rule in a single sentence, ' +
        'then let the learner do the next step themselves. Ask one quick check before moving on.';
    if (slip) teach += ` Common slip to correct: ${slip}`;
    teach += ` Draw or show: ${ideas[0]}; or ${ideas[1]}.`;
    return { teach: teach.slice(0, 1600), ideas, count };
}

function buildUnit(course, topic, questions) {
    const { teach, ideas } = teachFor(course, topic, questions.length);
    return {
        id: `u${topic.index}`,
        title: topic.title.slice(0, 160),
        summary:
            (questions.length ? `${questions.length} question${questions.length === 1 ? '' : 's'} on ${topic.title.toLowerCase()}. ` : '') +
            (ideas[0] ? `Show it as ${ideas[0]}.` : ''),
        skills: [
            {
                id: `s${topic.index}`,
                name: topic.title.slice(0, 160),
                teach,
                questions
            }
        ]
    };
}

/** Assign the course's questions to its skills by keyword fit, then balance. */
function assignQuestions(topics, questions) {
    const skillTokens = topics.map((t) => ({
        title: tokenSet(t.title),
        body: tokenSet(String(t.text || '').slice(0, 2400))
    }));
    const questionTokens = questions.map((q) => tokenSet(`${q.stem} ${q.why}`));
    const buckets = topics.map(() => []);
    const taken = new Set();

    const score = (qi, si) => {
        const q = questionTokens[qi];
        return overlap(q, skillTokens[si].title) * 4 + overlap(q, skillTokens[si].body);
    };

    questions.forEach((_q, qi) => {
        let best = -1;
        let bestScore = 0;
        for (let si = 0; si < topics.length; si += 1) {
            if (buckets[si].length >= 5) continue;
            const s = score(qi, si);
            if (s > bestScore) {
                bestScore = s;
                best = si;
            }
        }
        if (best >= 0) {
            buckets[best].push(qi);
            taken.add(qi);
        }
    });

    // Every skill should have at least three questions when the course has them.
    for (let si = 0; si < topics.length; si += 1) {
        while (buckets[si].length < 3) {
            let pick = -1;
            let pickScore = -1;
            for (let qi = 0; qi < questions.length; qi += 1) {
                if (taken.has(qi)) continue;
                const s = score(qi, si);
                if (s > pickScore) {
                    pickScore = s;
                    pick = qi;
                }
            }
            if (pick < 0) break;
            buckets[si].push(pick);
            taken.add(pick);
        }
    }

    // Leftovers top up the thinnest skills, never beyond five per skill.
    const leftovers = questions.map((_q, i) => i).filter((i) => !taken.has(i));
    for (const qi of leftovers) {
        let best = -1;
        let bestCount = Infinity;
        for (let si = 0; si < topics.length; si += 1) {
            if (buckets[si].length >= 5) continue;
            const s = score(qi, si);
            if (s > 0 && buckets[si].length < bestCount) {
                bestCount = buckets[si].length;
                best = si;
            }
        }
        if (best < 0) {
            bestCount = Infinity;
            for (let si = 0; si < topics.length; si += 1) {
                if (buckets[si].length < 5 && buckets[si].length < bestCount) {
                    bestCount = buckets[si].length;
                    best = si;
                }
            }
        }
        if (best >= 0) buckets[best].push(qi);
    }

    return buckets.map((list) => list.sort((a, b) => a - b).map((i) => questions[i]));
}

function outlineForCourse(course) {
    const topics = topicsOf(course);
    if (!topics.length) return null;
    const questions = courseQuestions(course);
    const assigned = assignQuestions(topics, questions);
    const units = topics.map((topic, i) => {
        topic.index = i + 1;
        return buildUnit(course, topic, assigned[i] || []);
    });
    return { version: 1, units };
}

/* ----------------------------------------------- "… Complete" index courses */

function listedUnits(course) {
    const items = [];
    const li = /<li[^>]*>([\s\S]*?)<\/li>/gi;
    let m;
    while ((m = li.exec(course.content))) {
        const t = inline(m[1]);
        if (t && t.length < 160) items.push(t);
    }
    if (items.length) return items.map((t) => t.replace(/^unit\s+\d+\s*[—–:-]\s*/i, '').trim());
    const text = toText(course.content);
    const parts = text.split(/unit\s+\d+\s*[—–:-]\s*/i).slice(1);
    return parts.map((p) => p.split(/\n|\.\s/)[0].trim()).filter(Boolean).slice(0, 12);
}

function titleScore(a, b) {
    const A = tokenSet(a);
    const B = tokenSet(b);
    if (!A.size || !B.size) return 0;
    let hit = 0;
    for (const w of A) if (B.has(w)) hit += 1;
    return hit / Math.max(1, Math.min(A.size, B.size));
}

function assembleFromSiblings(stub, allCourses) {
    const base = String(stub.title || '').replace(/\s*complete\s*$/i, '').trim();
    const names = listedUnits(stub);
    if (!names.length) return null;
    const candidates = allCourses.filter(
        (c) => Number(c.id) !== Number(stub.id) && (c.questions || []).length >= 3 && !/complete\s*$/i.test(c.title)
    );
    const used = new Set();
    const units = [];

    names.forEach((name, i) => {
        let best = null;
        let bestScore = 0;
        for (const c of candidates) {
            if (used.has(c.id)) continue;
            const s = titleScore(name, String(c.title).split(base).join(' '));
            if (s > bestScore) {
                bestScore = s;
                best = c;
            }
        }
        if (!best || bestScore < 0.18) return;
        used.add(best.id);
        const topics = topicsOf(best).slice(0, 12);
        if (!topics.length) return;
        const assigned = assignQuestions(topics, courseQuestions(best));
        const skills = topics.map((topic, ti) => {
            topic.index = ti + 1;
            return buildUnit(best, topic, assigned[ti] || []).skills[0];
        });
        const count = skills.reduce((n, s) => n + s.questions.length, 0);
        units.push({
            id: `u${i + 1}`,
            title: `${i + 1}. ${name}`.slice(0, 160),
            summary: `${count} questions from ${best.title}.`.slice(0, 600),
            skills
        });
    });

    if (!units.length) return null;
    return { version: 1, units };
}

function stats(outline) {
    const units = outline.units || [];
    const skills = units.reduce((n, u) => n + u.skills.length, 0);
    const questions = units.reduce((n, u) => n + u.skills.reduce((m, s) => m + s.questions.length, 0), 0);
    const empty = units.reduce((n, u) => n + u.skills.filter((s) => !s.questions.length).length, 0);
    const thin = units.reduce((n, u) => n + u.skills.filter((s) => s.questions.length < 3).length, 0);
    return { units: units.length, skills, questions, emptySkills: empty, thinSkills: thin };
}

module.exports = {
    LETTERS,
    assignQuestions,
    assembleFromSiblings,
    coreOf,
    courseQuestions,
    diagramIdeas,
    inline,
    listedUnits,
    outlineForCourse,
    overlap,
    stats,
    toOutlineQuestion,
    toText,
    tokenSet,
    topicsOf
};
