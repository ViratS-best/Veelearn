/**
 * The mastery map: every skill in a track with its four evidence dots.
 *
 * Deliberately not a graph. Phase 1 has one prerequisite chain per track and the
 * useful question is "where am I in this?" — a small list answers it in a glance
 * on a phone, which a node graph does not.
 */
(function () {
  const TRACK_NAMES = {
    'math.g8': 'Grade 8 math',
    algebra1: 'Algebra 1',
    apcmech: 'AP Physics C: Mechanics',
    'sat.math': 'SAT Math'
  };

  function esc(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function trackName(track) {
    return TRACK_NAMES[track] || String(track || 'Practice');
  }

  function dotsHtml(level) {
    const n = Math.max(0, Math.min(4, Number(level) || 0));
    let out = '<span class="sx-dots" aria-hidden="true">';
    for (let i = 1; i <= 4; i += 1) out += `<i${i <= n ? ' class="is-on"' : ''}></i>`;
    return `${out}</span>`;
  }

  /**
   * @param {HTMLElement} container
   * @param {Array<{track:string, percent:number, skills:Array}>} map
   * @param {string} currentTrack
   */
  function render(container, map, currentTrack) {
    if (!container) return;
    if (!Array.isArray(map) || !map.length) {
      container.innerHTML = '<p class="sx-map-empty">No skills loaded yet.</p>';
      return;
    }

    container.innerHTML = map
      .map((t) => {
        const skills = (t.skills || [])
          .map(
            (s) => `<li class="sx-map-skill is-l${Number(s.level) || 0}" title="${esc(s.name)} — level ${Number(s.level) || 0} of 4">
              ${dotsHtml(s.level)}<span>${esc(s.name)}</span></li>`
          )
          .join('');
        return `<section class="sx-map-track${t.track === currentTrack ? ' is-current' : ''}">
          <header><h2>${esc(trackName(t.track))}</h2><span>${Number(t.percent) || 0}%</span></header>
          <ul>${skills}</ul>
        </section>`;
      })
      .join('');
  }

  window.SessionMap = { render, dotsHtml, trackName, esc };
})();
