'use strict';

/**
 * Mastery maths for AI sessions.
 *
 * Deliberately small and explainable: a probability per skill, four evidence
 * dots, an assistance penalty, and a spaced-review interval. No training data
 * required, no extra service, and every number is reproducible in SQL for a
 * teacher or parent who asks "why is this skill at two dots?".
 */

/** Evidence weight of a correct answer at each tier (1 recall → 4 contest). */
const TIER_WEIGHT = { 1: 0.20, 2: 0.26, 3: 0.34, 4: 0.42 };

/**
 * How much a correct answer still counts, by help level.
 * 0 = unaided, 1 = hint, 2 = focused help, 3 = fully taught.
 */
const ASSISTANCE_MULT = [1, 0.6, 0, 0];

const WRONG_PENALTY = 0.12;
const LADDER_DAYS = [1, 3, 7, 18, 45, 90];

/** Correct answers needed inside one focus item, by its dot target. */
const CORRECTS_FOR_DOTS = { 1: 2, 2: 3, 3: 4, 4: 5 };

function clamp(n, lo, hi) {
    const v = Number(n);
    if (!Number.isFinite(v)) return lo;
    return Math.min(hi, Math.max(lo, v));
}

function clamp01(n) {
    return clamp(n, 0, 1);
}

function assistanceMultiplier(hintsOrLevel) {
    const level = Math.round(clamp(hintsOrLevel, 0, 3));
    return ASSISTANCE_MULT[level];
}

/**
 * Update the mastery probability for one attempt.
 * @param {{p:number, correct:boolean, tier:number, hints?:number, assistance?:number}} attempt
 * @returns {{p:number, delta:number, assistance:number}}
 */
function applyAttempt({ p, correct, tier, hints = 0, assistance } = {}) {
    const level = Math.round(clamp(assistance != null ? assistance : hints, 0, 3));
    const mult = assistanceMultiplier(level);
    const weight = TIER_WEIGHT[Math.round(clamp(tier || 1, 1, 4))] || TIER_WEIGHT[1];
    const before = clamp01(p || 0);
    const delta = correct ? weight * mult : -WRONG_PENALTY;
    return { p: clamp01(before + delta), delta, assistance: level };
}

function levelFromP(p) {
    const v = clamp01(p);
    // 0.2 is exactly one unaided tier-1 correct answer, which is what
    // "level 1 = introduced" means in the design.
    if (v < 0.2) return 0;
    if (v < 0.5) return 1;
    if (v < 0.75) return 2;
    if (v < 0.92) return 3;
    return 4;
}

/**
 * Forgetting, applied lazily at read time rather than by a nightly job.
 * Half-life is 14 days, or 7 for skills the learner has not really started.
 */
function decayedP(p, level, lastSeenMs, nowMs = Date.now()) {
    const halfLifeDays = (level || 0) <= 1 ? 7 : 14;
    if (!lastSeenMs) return clamp01(p);
    const days = Math.max(0, (nowMs - lastSeenMs) / 86400000);
    const factor = Math.pow(0.5, days / halfLifeDays);
    return clamp01(clamp01(p) * factor);
}

/**
 * Next review date for a skill.
 * @param {{level:number, ease:number, correct:boolean, reps:number, skipped?:boolean}} o
 * @returns {{intervalDays:number, ease:number, reps:number}}
 */
function nextReview({ level = 0, ease = 2.5, correct = true, reps = 0, skipped = false } = {}) {
    const safeEase = clamp(ease || 2.5, 1.3, 3.2);

    if (skipped) {
        return { intervalDays: 3, ease: clamp(safeEase - 0.1, 1.3, 3.2), reps: (reps || 0) + 1 };
    }
    if (!correct) {
        return { intervalDays: 1, ease: clamp(safeEase - 0.2, 1.3, 3.2), reps: 0 };
    }

    const ladderIndex = (level || 0) <= 1 ? Math.min(reps || 0, 2) : Math.min(reps || 0, LADDER_DAYS.length - 1);
    const base = LADDER_DAYS[ladderIndex] || 1;
    const scaled = Math.round(base * (safeEase / 2.5));
    return {
        intervalDays: clamp(scaled, 1, 90),
        ease: clamp(safeEase + ((level || 0) >= 2 ? 0.08 : 0.04), 1.3, 3.2),
        reps: (reps || 0) + 1
    };
}

/** XP / gems for a graded answer, an item, and a finished session. */
const REWARDS = {
    correct: { xp: 6, gems: 1 },
    item: { xp: 20, gems: 4 },
    goal: { xp: 25, gems: 8 }
};

/** Focus items for a contracted session length. */
function itemsForMinutes(minutes) {
    const m = clamp(minutes || 20, 5, 90);
    if (m <= 10) return 2;
    if (m <= 15) return 3;
    if (m <= 20) return 4;
    if (m <= 30) return 5;
    if (m <= 40) return 7;
    return 8;
}

function correctsNeeded(dotTarget) {
    return CORRECTS_FOR_DOTS[clamp(dotTarget || 2, 1, 4)] || 3;
}

/** Four dots for the UI, filled according to the current level. */
function dots(level) {
    const l = clamp(level || 0, 0, 4);
    return [1, 2, 3, 4].map((i) => i <= l);
}

module.exports = {
    TIER_WEIGHT,
    ASSISTANCE_MULT,
    REWARDS,
    LADDER_DAYS,
    applyAttempt,
    assistanceMultiplier,
    correctsNeeded,
    decayedP,
    dots,
    itemsForMinutes,
    levelFromP,
    nextReview,
    clamp,
    clamp01
};
