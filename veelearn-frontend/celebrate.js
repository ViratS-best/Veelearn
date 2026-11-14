/**
 * Celebration, two sizes.
 *
 *   item complete → small: the dots fill with a 90 ms stagger, the row strikes
 *                   through, +XP floats up. No confetti; that is saved for the goal.
 *   goal reached  → full screen: 90 emoji particles for 2.8 s, a mascot hop, and a
 *                   card with Keep going / I'm done.
 *
 * One animation budget, written once, reused by streak and level-up with a
 * different palette. All of it becomes a static banner under reduced motion.
 */
(function (global) {
  'use strict';

  const GOAL_EMOJI = ['🎉', '✨', '🧠', '⭐', '🏆'];
  const LEVEL_EMOJI = ['✨', '💫', '⭐', '🔥'];
  const PARTICLES = 90;

  const prefersReduced = () =>
    typeof global.matchMedia === 'function' && global.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function esc(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function root() {
    let el = document.getElementById('sx-celebrate');
    if (!el) {
      el = document.createElement('div');
      el.id = 'sx-celebrate';
      el.className = 'sx-celebrate';
      document.body.appendChild(el);
    }
    return el;
  }

  /**
   * Item complete: the earned dots fill (90 ms stagger), the row strikes, XP floats.
   * Purely cosmetic — the state has already been persisted by the server.
   *
   * `level` is the learner's dot level after this item. Pass it: pulsing all four
   * dots would claim mastery the learner has not earned.
   */
  function item(rowEl, opts) {
    const o = opts || {};
    const row = typeof rowEl === 'string' ? document.querySelector(rowEl) : rowEl;
    if (!row) return;

    row.classList.add('is-done');

    const target = Number.isFinite(Number(o.level)) ? Math.max(0, Math.min(4, Number(o.level))) : null;
    const dots = row.querySelectorAll('.sx-dots i');
    dots.forEach((dot, i) => {
      if (target != null) {
        if (i < target) {
          if (prefersReduced()) {
            dot.classList.add('is-on');
            return;
          }
          setTimeout(() => dot.classList.add('is-on'), 90 * (i + 1));
        } else {
          dot.classList.remove('is-on');
        }
        return;
      }
      if (prefersReduced()) {
        dot.classList.add('is-on');
        return;
      }
      setTimeout(() => dot.classList.add('is-on'), 90 * (i + 1));
    });

    const name = row.querySelector('.sx-focus-name');
    if (name) name.classList.add('is-struck');

    if (typeof o.xp === 'number' && o.xp > 0) {
      float(o.xp, row);
    }

    if (global.Mascot && global.Mascot.mood) global.Mascot.mood('happy');
  }

  function float(xp, anchor) {
    if (prefersReduced()) return;
    const rect = anchor.getBoundingClientRect();
    const chip = document.createElement('span');
    chip.className = 'sx-xp-float';
    chip.textContent = `+${xp} XP`;
    chip.style.left = `${rect.left + rect.width / 2}px`;
    chip.style.top = `${rect.top + rect.height / 2}px`;
    document.body.appendChild(chip);
    setTimeout(() => chip.remove(), 1100);
  }

  function particles(count, emojis) {
    const host = root();
    host.innerHTML = '';
    host.classList.add('is-on');
    if (prefersReduced()) return host;

    for (let i = 0; i < count; i += 1) {
      const span = document.createElement('span');
      span.className = 'sx-confetti';
      span.textContent = emojis[i % emojis.length];
      const angle = (Math.PI * 2 * i) / count;
      const dist = 110 + Math.random() * 220;
      span.style.setProperty('--dx', `${Math.cos(angle) * dist}px`);
      span.style.setProperty('--dy', `${Math.sin(angle) * dist - 40}px`);
      span.style.setProperty('--rot', `${Math.round(Math.random() * 720 - 360)}deg`);
      span.style.animationDelay = `${0.02 + Math.random() * 0.5}s`;
      host.appendChild(span);
    }
    return host;
  }

  /**
   * Goal reached. Returns a promise resolving to 'keep' | 'done' | 'timeout'.
   */
  function goal(opts) {
    const o = opts || {};
    const xp = Number(o.xp) || 0;
    const gems = Number(o.gems) || 0;
    const reduced = prefersReduced();

    if (global.Mascot && global.Mascot.mood) global.Mascot.mood('cheer');

    let host = root();
    if (!reduced) {
      particles(PARTICLES, GOAL_EMOJI);
      host = root();
      // particles() rebuilt the host; re-append the card container
    } else {
      host.innerHTML = '';
      host.classList.add('is-on', 'is-static');
    }

    const card = document.createElement('div');
    card.className = 'sx-celebrate-card';
    card.setAttribute('role', 'dialog');
    card.setAttribute('aria-modal', 'false');
    card.setAttribute('aria-label', 'Goal reached');
    card.innerHTML = `
      <p class="sx-celebrate-line">${reduced ? 'Goal reached.' : '🎉 Daily goal reached'}</p>
      <p class="sx-celebrate-stats">${xp ? `<strong>${xp} XP</strong>` : ''}${xp && gems ? ' · ' : ''}${
        gems ? `<strong>${gems} gems</strong>` : ''
      }</p>
      <div class="sx-celebrate-actions">
        <button type="button" class="sx-btn sx-primary" data-celebrate="keep">Keep going</button>
        <button type="button" class="sx-btn sx-ghost" data-celebrate="done">I'm done</button>
      </div>
    `;
    host.appendChild(card);

    const finish = (choice) => {
      host.classList.remove('is-on', 'is-static');
      host.innerHTML = '';
      if (typeof o.onChoose === 'function') o.onChoose(choice);
    };

    return new Promise((resolve) => {
      let settled = false;
      const settle = (choice) => {
        if (settled) return;
        settled = true;
        finish(choice);
        resolve(choice);
      };
      card.querySelectorAll('[data-celebrate]').forEach((btn) => {
        btn.addEventListener('click', () => settle(btn.getAttribute('data-celebrate')));
      });
      if (!reduced) setTimeout(() => settle('timeout'), 2800);
      else {
        const close = document.createElement('button');
        close.type = 'button';
        close.className = 'sx-celebrate-dismiss';
        close.setAttribute('aria-label', 'Dismiss');
        close.textContent = '×';
        close.addEventListener('click', () => settle('done'));
        card.appendChild(close);
      }
    });
  }

  /** A level-up or streak milestone: same budget, different palette, quieter. */
  function levelUp(opts) {
    const o = opts || {};
    if (global.Mascot && global.Mascot.mood) global.Mascot.mood('cheer');
    if (prefersReduced()) return;
    const host = particles(36, LEVEL_EMOJI);
    host.classList.add('is-quiet');
    setTimeout(() => {
      host.classList.remove('is-on', 'is-quiet');
      host.innerHTML = '';
    }, 1600);
    if (o.text) {
      const note = document.createElement('p');
      note.className = 'sx-levelup-note';
      note.textContent = String(o.text).slice(0, 80);
      document.body.appendChild(note);
      setTimeout(() => note.remove(), 1800);
    }
  }

  global.Celebrate = { item, goal, levelUp, float, PARTICLES };
})(window);
