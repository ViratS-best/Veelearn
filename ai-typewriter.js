/**
 * Shared character-by-character typewriter for Veelearn AI surfaces.
 * History loads should pass { instant: true }.
 */
(function (global) {
  'use strict';

  const DEFAULT_MS_PER_CHAR = 22;
  const FAST_MS_PER_CHAR = 8;

  function sleep(ms, signal) {
    return new Promise((resolve, reject) => {
      if (signal && signal.aborted) {
        reject(new DOMException('Aborted', 'AbortError'));
        return;
      }
      const t = setTimeout(resolve, ms);
      if (signal) {
        const onAbort = () => {
          clearTimeout(t);
          reject(new DOMException('Aborted', 'AbortError'));
        };
        signal.addEventListener('abort', onAbort, { once: true });
      }
    });
  }

  /**
   * Type text into an element. Clicking the element or pressing Escape finishes instantly.
   * @param {HTMLElement} el
   * @param {string} text
   * @param {{ msPerChar?: number, signal?: AbortSignal, instant?: boolean, scrollParent?: HTMLElement }} opts
   */
  async function typeIntoElement(el, text, opts) {
    const options = opts || {};
    const full = text == null ? '' : String(text);
    if (!el) return;

    if (options.instant || !full) {
      el.textContent = full;
      return;
    }

    const controller = new AbortController();
    const parentSignal = options.signal;
    if (parentSignal) {
      if (parentSignal.aborted) {
        el.textContent = full;
        return;
      }
      parentSignal.addEventListener('abort', () => controller.abort(), { once: true });
    }

    let skipped = false;
    const finish = () => {
      skipped = true;
      controller.abort();
    };

    const onKey = (e) => {
      if (e.key === 'Escape') finish();
    };
    const onClick = () => finish();

    el.addEventListener('click', onClick);
    document.addEventListener('keydown', onKey);
    el.style.cursor = 'pointer';
    el.title = 'Click to finish typing';

    el.textContent = '';
    const ms = options.msPerChar != null ? options.msPerChar : DEFAULT_MS_PER_CHAR;
    const scrollParent = options.scrollParent || null;

    try {
      for (let i = 0; i < full.length; i++) {
        if (skipped || controller.signal.aborted) break;
        el.textContent = full.slice(0, i + 1);
        if (scrollParent) scrollParent.scrollTop = scrollParent.scrollHeight;
        // Slightly faster for spaces/newlines so pacing feels natural
        const ch = full[i];
        const delay = ch === ' ' || ch === '\n' ? Math.max(4, ms * 0.45) : ms;
        try {
          await sleep(delay, controller.signal);
        } catch (_) {
          break;
        }
      }
    } finally {
      el.textContent = full;
      el.removeEventListener('click', onClick);
      document.removeEventListener('keydown', onKey);
      el.style.cursor = '';
      el.removeAttribute('title');
      if (scrollParent) scrollParent.scrollTop = scrollParent.scrollHeight;
    }
  }

  /**
   * Create a chat bubble and type assistant text into its body.
   * @returns {Promise<HTMLElement>}
   */
  async function typewriterAppendBubble(container, role, text, classNames, opts) {
    const options = opts || {};
    if (!container) return null;

    const wrap = document.createElement('div');
    if (classNames) {
      String(classNames)
        .split(/\s+/)
        .filter(Boolean)
        .forEach((c) => wrap.classList.add(c));
    }

    const label = document.createElement('strong');
    label.textContent = role === 'user' ? 'You' : options.label || 'Coach';
    const body = document.createElement('div');
    body.className = options.bodyClass || 'ai-typewriter-body';
    wrap.appendChild(label);
    wrap.appendChild(body);
    container.appendChild(wrap);
    container.scrollTop = container.scrollHeight;

    const instant = options.instant || role === 'user';
    if (instant) {
      body.textContent = text == null ? '' : String(text);
    } else {
      await typeIntoElement(body, text, {
        msPerChar: options.msPerChar,
        signal: options.signal,
        scrollParent: container
      });
    }

    if (typeof options.onDone === 'function') {
      await options.onDone(wrap, body);
    }
    return wrap;
  }

  /** Delay helper for sequencing whole-unit inserts (questions, sims, blocks). */
  function delay(ms) {
    return new Promise((r) => setTimeout(r, ms));
  }

  global.VeelearnTypewriter = {
    typeIntoElement,
    typewriterAppendBubble,
    delay,
    DEFAULT_MS_PER_CHAR,
    FAST_MS_PER_CHAR
  };
})(typeof window !== 'undefined' ? window : globalThis);
