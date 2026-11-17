'use strict';

/**
 * What counts as a real course or outline.
 *
 * The `courses` table holds three things that look alike: legacy courses with a
 * body, outline-first maps, and whatever a creator typed while testing ("a",
 * "Outline Test 1794761977545"). The dashboard's tutor recommends from that
 * table, so a placeholder that reaches the catalog is a placeholder a learner
 * can be sent to. This module is the one place that decides whether a row is
 * worth recommending, so every surface can agree.
 *
 * Rules:
 *   - a test/placeholder title is never recommendable, whatever its content;
 *   - an outline must carry at least one unit, one skill and three questions
 *     (the same bar `POST /api/outlines/:id/submit` enforces);
 *   - a legacy course must have a body or a real description.
 */

function clean(value) {
    return String(value == null ? '' : value)
        .replace(/\s+/g, ' ')
        .trim();
}

/** Titles nobody means to publish. */
const JUNK_TITLES = [
    /^(untitled|untitled outline|new outline|my outline|blank|draft|test|testing|sample|demo|placeholder|n\/a|na|none|null|undefined)$/i,
    /^(asdf\w*|qwer\w*|abc\d*|test\d+|\d+)$/i,
    /^(outline\s*)?test(?:\s*(?:outline|course|\d+))*$/i,
    /\boutline\s*test\b/i
];

/**
 * A title a person would recognise as a course. Deliberately conservative:
 * "Test-taking strategies" survives, "Test 12" and "Outline Test 1794" do not.
 */
function isTestTitle(raw) {
    const title = clean(raw);
    if (!title) return true;
    if (title.length < 3) return true; // "a", "x"
    // "1794761977545", "..." — but any real letter counts, including Arabic,
    // Cyrillic, Devanagari and CJK (\W would call those punctuation).
    if (!/\p{L}/u.test(title)) return true;
    if (/^[a-z]{1,2}$/i.test(title)) return true;
    if (JUNK_TITLES.some((re) => re.test(title))) return true;
    // "Gate Test 1794768162860", "Picture Test 1794", "Outline Test 1794": a
    // harness naming its run by timestamp. Note the singular "test" + long
    // number, so "AP Calculus Unit 4: Sequences & Series Tests" survives.
    if (/\btest\b\s*[#-]?\s*\d{4,}\s*$/i.test(title)) return true;
    if (/^(gate|picture|outline|sample|demo|smoke|e2e|ui|api|integration)\s+test\b/i.test(title)) return true;
    // A bare "test…" title that never grows into a sentence: "test 2", "Test outline".
    if (/^test\b/i.test(title) && title.length < 18) return true;
    return false;
}

/** The map, parsed from a JSON string, an object, or nothing. */
function parseOutline(raw) {
    if (raw == null) return null;
    if (typeof raw === 'object') return raw;
    try {
        const parsed = JSON.parse(String(raw));
        return parsed && typeof parsed === 'object' ? parsed : null;
    } catch (_) {
        return null;
    }
}

function outlineStats(raw) {
    const outline = parseOutline(raw);
    if (!outline) return { units: 0, skills: 0, questions: 0, skillsWithQuestions: 0 };
    const units = Array.isArray(outline.units) ? outline.units : [];
    let skills = 0;
    let questions = 0;
    let skillsWithQuestions = 0;
    for (const unit of units) {
        const list = Array.isArray(unit && unit.skills) ? unit.skills : [];
        for (const skill of list) {
            skills += 1;
            const qs = Array.isArray(skill && skill.questions) ? skill.questions.length : 0;
            questions += qs;
            if (qs > 0) skillsWithQuestions += 1;
        }
    }
    return { units: units.length, skills, questions, skillsWithQuestions };
}

/**
 * @param {object} row        catalog row (title, description/desc_preview, content_length?)
 * @param {*} outline         `course_outlines.outline_json` for that course, if any
 */
function isRecommendableCourse(row, outline) {
    const title = clean(row && row.title);
    if (isTestTitle(title)) return false;

    const stats = outlineStats(outline);
    if (stats.units > 0) {
        // Same gate as submission: a map needs a skill and three questions.
        return stats.skills > 0 && stats.questions >= 3;
    }

    const bodyLength = Number(
        row && row.content_length != null ? row.content_length : String((row && row.content) || '').length
    );
    const desc = clean(row && (row.description || row.desc_preview));
    return bodyLength >= 80 || desc.length >= 40;
}

module.exports = {
    clean,
    outlineStats,
    parseOutline,
    isRecommendableCourse,
    isTestTitle
};
