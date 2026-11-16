'use strict';

/**
 * Server-side provenance labels.
 *
 * The browser uses veelearn-frontend/qbank-provenance.js for the picker and the
 * session card; the transcript is written here on the server, so it needs the
 * same words. test-bank-provenance.js asserts both implementations agree.
 */

const AUTHORED = 'authored';
const AUTHORED_LABEL = 'Veelearn original';

const KNOWN = {
    authored: AUTHORED_LABEL,
    openbookqa: 'OpenBookQA · Apache-2.0',
    gsm8k: 'GSM8K · MIT'
};

function sourceOf(item) {
    return String((item && item.source) || AUTHORED).trim().toLowerCase() || AUTHORED;
}

function creditOf(item) {
    return String((item && item.attribution) || '').trim();
}

function label(item) {
    const source = sourceOf(item);
    if (KNOWN[source]) return KNOWN[source];
    const credit = creditOf(item);
    if (!credit) return source === AUTHORED ? AUTHORED_LABEL : 'Third-party set';
    const split = credit.match(/^(.*?)\s*(?:\u2014|\u2013|--)\s*(.+)$/);
    if (split) return (split[1].trim() + ' · ' + split[2].trim()).slice(0, 80);
    return credit.slice(0, 80);
}

function detail(item) {
    const credit = creditOf(item);
    if (credit) return credit;
    return sourceOf(item) === AUTHORED ? 'Written for Veelearn' : 'Third-party question set';
}

function isThirdParty(item) {
    return sourceOf(item) !== AUTHORED;
}

// Rows written before provenance existed carry sources like 'course' or 'seed'
// with no credit line. Those are not third-party sets, so they get no label.
const LICENSED = new Set(Object.keys(KNOWN).filter((id) => id !== AUTHORED));

/**
 * Only a question we can actually name is credited: one of the licensed sets,
 * or a row that carries its own credit line. A Veelearn original — and a legacy
 * row with a bare internal source — shows nothing.
 */
function isThirdParty(item) {
    const source = sourceOf(item);
    if (source === AUTHORED) return false;
    return LICENSED.has(source) || Boolean(creditOf(item));
}

function shouldCredit(item) {
    return isThirdParty(item);
}

module.exports = { label, detail, isThirdParty, shouldCredit, KNOWN };
