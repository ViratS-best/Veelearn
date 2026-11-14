'use strict';

/**
 * Grade-level gate for course recommendations.
 *
 * The study coach prompt already tells the model to match the learner's grade,
 * but a prompt is not a guarantee: in production an 8th-grade request was
 * answered with "AP Physics C: Mechanics". This module is the server-side veto.
 *
 * Two rules, in order:
 *   1. If the learner explicitly asks for the subject ("I want to learn AP
 *      physics"), the subject wins and the grade band is ignored.
 *   2. Otherwise a course may not be more than one grade band above the
 *      learner. Reviewing easier material is always allowed.
 *
 * The course's own grade_level column is only a fallback, because seeded data
 * is unreliable — titles like "AP Physics C" carry a reliable band.
 */

/** Grade mentions inside a message or a course title. */
function extractGradeHints(text) {
    const msg = String(text || '').toLowerCase();
    const grades = new Set();

    const range = msg.match(/\b(?:grades?\s*)?(\d{1,2})\s*[-–to]+\s*(\d{1,2})(?:\s*(?:st|nd|rd|th)?\s*grade)?\b/);
    if (range) {
        const a = parseInt(range[1], 10);
        const b = parseInt(range[2], 10);
        if (!Number.isNaN(a) && !Number.isNaN(b)) {
            const lo = Math.min(a, b);
            const hi = Math.max(a, b);
            for (let g = lo; g <= hi && g <= 13; g++) grades.add(g);
        }
    }

    const singles = msg.matchAll(/\b(?:grade\s*)?(\d{1,2})(?:st|nd|rd|th)?\s*grade\b/g);
    for (const m of singles) {
        const g = parseInt(m[1], 10);
        if (!Number.isNaN(g) && g >= 1 && g <= 13) grades.add(g);
    }

    if (/\b(elementary|primary|k-?5|kindergarten)\b/.test(msg)) [1, 2, 3, 4, 5].forEach((g) => grades.add(g));
    if (/\b(middle\s*school|junior\s*high)\b/.test(msg)) [6, 7, 8].forEach((g) => grades.add(g));
    if (/\b(high\s*school|secondary)\b/.test(msg)) [9, 10, 11, 12].forEach((g) => grades.add(g));

    const ordinals = { first: 1, second: 2, third: 3, fourth: 4, fifth: 5, sixth: 6, seventh: 7, eighth: 8, ninth: 9, tenth: 10, eleventh: 11, twelfth: 12 };
    for (const [word, g] of Object.entries(ordinals)) {
        if (new RegExp(`\\b${word}\\s*grade\\b`).test(msg)) grades.add(g);
    }

    const gradeN = msg.matchAll(/\bgrade\s*(\d{1,2})\b/g);
    for (const m of gradeN) {
        const g = parseInt(m[1], 10);
        if (!Number.isNaN(g) && g >= 1 && g <= 13) grades.add(g);
    }

    return [...grades];
}

/**
 * Subject rules. `band` is the grade range the subject is normally taught in.
 * Order matters — the first match wins, so the most specific patterns go first.
 */
const SUBJECT_RULES = [
    { key: 'ap physics c', re: /\bap\s*physics\s*c\b|\bphysics\s*c\b/i, band: [11, 13] },
    { key: 'ap physics', re: /\bap\s*phys(?:ics)?\b/i, band: [10, 13] },
    { key: 'ap calculus', re: /\bap\s*calc(?:ulus)?\b/i, band: [11, 13] },
    { key: 'ap chemistry', re: /\bap\s*chem(?:istry)?\b/i, band: [10, 13] },
    { key: 'ap biology', re: /\bap\s*bio(?:logy)?\b/i, band: [10, 13] },
    { key: 'ap', re: /\bap[\s-][a-z]/i, band: [10, 13] },
    { key: 'sat', re: /\bsat\b|\bpsat\b/i, band: [10, 13] },
    { key: 'act', re: /\bact\b\s*(?:prep|math|reading|english|science)|act\s*prep/i, band: [10, 13] },
    { key: 'calculus', re: /\bcalculus\b|\bcalc\s*(?:ab|bc)\b/i, band: [11, 13] },
    { key: 'precalculus', re: /pre-?calc(?:ulus)?/i, band: [10, 12] },
    { key: 'algebra 2', re: /algebra\s*(?:2|ii)\b/i, band: [10, 12] },
    { key: 'trigonometry', re: /\btrig(?:onometry)?\b/i, band: [10, 12] },
    { key: 'mathcounts', re: /math\s*counts|\bamc\s*\d/i, band: [6, 9] },
    { key: 'algebra 1', re: /algebra\s*(?:1|i)\b|pre-?algebra/i, band: [8, 10] },
    { key: 'geometry', re: /\bgeometry\b/i, band: [9, 11] },
    { key: 'physics', re: /\bphysics\b/i, band: [10, 13] },
    { key: 'chemistry', re: /\bchem(?:istry)?\b/i, band: [9, 12] },
    { key: 'biology', re: /\bbio(?:logy)?\b/i, band: [9, 12] },
    { key: 'physical science', re: /physical\s*science/i, band: [8, 10] },
    { key: 'arithmetic', re: /\b(?:arithmetic|counting|number sense)\b/i, band: [1, 6] }
];

function subjectRuleFor(text) {
    const s = String(text || '');
    return SUBJECT_RULES.find((r) => r.re.test(s)) || null;
}

/**
 * Grade band implied by a course's title, then description.
 * Returns { min, max } or null when nothing can be inferred.
 */
function inferCourseBand(course) {
    if (!course) return null;
    const title = String(course.title || '');

    const titleGrades = extractGradeHints(title);
    if (titleGrades.length) {
        return { min: Math.min(...titleGrades), max: Math.max(...titleGrades) };
    }

    const rule = subjectRuleFor(title) || subjectRuleFor(course.desc_preview || course.description || '');
    if (rule) return { min: rule.band[0], max: rule.band[1] };

    const descGrades = extractGradeHints(course.desc_preview || course.description || '');
    if (descGrades.length) {
        return { min: Math.min(...descGrades), max: Math.max(...descGrades) };
    }
    return null;
}

/** Did the learner name this course's subject explicitly? */
function subjectNamedInMessage(message, course) {
    const msg = String(message || '');
    const courseRule = subjectRuleFor(String(course?.title || '') + ' ' + String(course?.desc_preview || course?.description || ''));
    if (!courseRule) return false;
    // For AP courses, require the AP/level qualifier too ("ap physics", not just "physics").
    const key = courseRule.key;
    if (key.startsWith('ap ')) {
        return courseRule.re.test(msg);
    }
    return courseRule.re.test(msg);
}

/**
 * Resolve the learner's grade.
 * A grade named in the current message always beats the stored profile.
 */
function resolveLearnerGrade({ message, declaredGrade } = {}) {
    const fromMessage = extractGradeHints(message);
    if (fromMessage.length) {
        return { grade: Math.max(...fromMessage), source: 'message' };
    }
    const g = parseInt(declaredGrade, 10);
    if (!Number.isNaN(g) && g >= 1 && g <= 13) {
        return { grade: g, source: 'profile' };
    }
    return { grade: null, source: null };
}

function courseDeclaredGrade(course) {
    const g = course?.grade_level != null ? parseInt(course.grade_level, 10) : NaN;
    return Number.isNaN(g) ? null : g;
}

/**
 * The gate itself.
 * @param {object} course catalog row (id, title, grade_level, desc_preview?, course_type?)
 * @param {{ grade: number|null, message?: string }} ctx
 */
function courseAllowed(course, ctx = {}) {
    const grade = parseInt(ctx.grade, 10);
    if (Number.isNaN(grade) || grade < 1) return true; // nothing to enforce against

    // 1. explicit subject request wins ("I want to learn AP Physics C")
    if (ctx.message && subjectNamedInMessage(ctx.message, course)) return true;

    const band = inferCourseBand(course);
    const declared = courseDeclaredGrade(course);

    const lo = band ? band.min : declared;
    if (lo == null) return true; // unknown level — allow, rank later

    // 2. a course may not sit more than one grade above the learner.
    return grade >= lo - 1;
}

/** Filter a catalog and report what was hidden, for logging and the UI. */
function filterCatalog(catalog, ctx = {}) {
    const allowed = [];
    const blocked = [];
    for (const c of catalog || []) {
        if (courseAllowed(c, ctx)) allowed.push(c);
        else blocked.push(c);
    }
    return { allowed, blocked, grade: ctx.grade ?? null };
}

/** How far a course sits from the learner's grade — used for ranking. */
function gradeDistance(course, grade) {
    const g = parseInt(grade, 10);
    if (Number.isNaN(g)) return 0;
    const band = inferCourseBand(course);
    const declared = courseDeclaredGrade(course);
    const lo = band ? band.min : declared;
    if (lo == null) return 2; // unknown: rank behind known-good matches
    return Math.abs(lo - g);
}

/** A short, honest line the coach can say when the gate removed everything. */
function gateNote(ctx = {}) {
    if (!ctx.grade) return '';
    return `I kept the list to courses at or just above grade ${ctx.grade} level.`;
}

module.exports = {
    extractGradeHints,
    inferCourseBand,
    subjectRuleFor,
    subjectNamedInMessage,
    resolveLearnerGrade,
    courseAllowed,
    filterCatalog,
    gradeDistance,
    gateNote
};
