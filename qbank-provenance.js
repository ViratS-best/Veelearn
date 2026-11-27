/**
 * Plain-language provenance for question-bank items.
 *
 * Every bank row carries `source` and `attribution` (see
 * seed/THIRD_PARTY_NOTICES.txt). A creator pulling a question should be able to
 * tell at a glance whether it is a Veelearn original or a third-party set, and
 * under which licence, without reading an id like "openbookqa".
 *
 * Browser: window.QBankProvenance. Node (tests): module.exports.
 */
(function (root, factory) {
    const api = factory();
    if (typeof module === 'object' && module.exports) module.exports = api;
    if (root) root.QBankProvenance = api;
})(typeof window !== 'undefined' ? window : null, function () {
    const AUTHORED = 'authored';
    const AUTHORED_LABEL = 'Veelearn original';

    // Short, human labels for the sets we ship. Ids come from
    // build_session_seed.py's SOURCES allowlist.
    const KNOWN = {
        authored: AUTHORED_LABEL,
        openbookqa: 'OpenBookQA · Apache-2.0',
        gsm8k: 'GSM8K · MIT',
        mmlu: 'MMLU · MIT'
    };

    function sourceOf(item) {
        return String((item && item.source) || AUTHORED).trim().toLowerCase() || AUTHORED;
    }

    function creditOf(item) {
        return String((item && item.attribution) || '').trim();
    }

    /** One short label: "Veelearn original", "OpenBookQA · Apache-2.0", … */
    function label(item) {
        const source = sourceOf(item);
        if (KNOWN[source]) return KNOWN[source];
        const credit = creditOf(item);
        if (!credit) return source === AUTHORED ? AUTHORED_LABEL : 'Third-party set';
        // "OpenBookQA (Mihaylov et al. 2018), Allen Institute for AI — Apache-2.0"
        // reads better as "OpenBookQA · Apache-2.0" in a chip.
        const split = credit.match(/^(.*?)\s*(?:\u2014|\u2013|--)\s*(.+)$/);
        if (split) return (split[1].trim() + ' · ' + split[2].trim()).slice(0, 80);
        return credit.slice(0, 80);
    }

    /** The full attribution, for a tooltip. */
    function detail(item) {
        const credit = creditOf(item);
        if (credit) return credit;
        return sourceOf(item) === AUTHORED ? 'Written for Veelearn' : 'Third-party question set';
    }

    // Rows written before provenance existed carry sources like 'course' with no
    // credit line. Those are not third-party sets, so they get no chip.
    const LICENSED = Object.keys(KNOWN).filter(function (id) {
        return id !== AUTHORED;
    });

    function isThirdParty(item) {
        const source = sourceOf(item);
        if (source === AUTHORED) return false;
        return LICENSED.indexOf(source) !== -1 || Boolean(creditOf(item));
    }

    return { label: label, detail: detail, isThirdParty: isThirdParty, KNOWN: KNOWN };
});
