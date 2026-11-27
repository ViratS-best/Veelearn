/**
 * Veelearn mobile navigation
 * ---------------------------------------------------------------------------
 * Collapses the site header's link row behind a menu button at <= 900px and
 * exposes the helpers the old script offered. It deliberately does not touch
 * every button's size or synthesise clicks on touchend: that broke toolbars and
 * fired each tap twice.
 */
(function () {
  'use strict';

  var MOBILE_QUERY = '(max-width: 900px)';

  function isMobile() {
    return window.matchMedia ? window.matchMedia(MOBILE_QUERY).matches : window.innerWidth <= 900;
  }

  function setVh() {
    // iOS reports the wrong 100vh while the address bar is showing.
    document.documentElement.style.setProperty('--vh', window.innerHeight * 0.01 + 'px');
  }

  function buildToggle() {
    var toggle = document.createElement('button');
    toggle.type = 'button';
    toggle.className = 'vl-nav-toggle';
    toggle.setAttribute('aria-label', 'Open menu');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-controls', 'vl-site-nav');
    toggle.innerHTML = '<span></span><span></span><span></span>';
    return toggle;
  }

  function initNav() {
    var header = document.querySelector('body > header');
    if (!header || header.classList.contains('vl-nav-ready')) return;

    var nav = header.querySelector('nav');
    if (!nav) return;

    // Give the panel a name only if the page does not already have one.
    if (!nav.id) nav.id = 'vl-site-nav';

    var toggle = buildToggle();
    header.appendChild(toggle);
    header.classList.add('vl-nav-ready');

    function open() {
      header.classList.add('vl-nav-open');
      toggle.setAttribute('aria-expanded', 'true');
      toggle.setAttribute('aria-label', 'Close menu');
    }

    function close() {
      header.classList.remove('vl-nav-open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.setAttribute('aria-label', 'Open menu');
    }

    function isOpen() {
      return header.classList.contains('vl-nav-open');
    }

    toggle.addEventListener('click', function (event) {
      event.stopPropagation();
      if (isOpen()) close();
      else open();
    });

    // A chosen link closes the panel; the navigation itself still happens.
    nav.addEventListener('click', function (event) {
      if (event.target.closest('a, button')) close();
    });

    document.addEventListener('click', function (event) {
      if (isOpen() && !header.contains(event.target)) close();
    });

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && isOpen()) {
        close();
        toggle.focus();
      }
    });

    // Leaving the phone layout must not leave a half-open panel behind.
    if (window.matchMedia) {
      var mq = window.matchMedia(MOBILE_QUERY);
      var onChange = function () {
        if (!mq.matches) close();
      };
      if (mq.addEventListener) mq.addEventListener('change', onChange);
      else if (mq.addListener) mq.addListener(onChange);
    }
  }

  function addTouchFeedback(element) {
    if (!element) return;
    element.addEventListener(
      'touchstart',
      function () {
        element.classList.add('touch-active');
      },
      { passive: true }
    );
    var clear = function () {
      element.classList.remove('touch-active');
    };
    element.addEventListener('touchend', clear, { passive: true });
    element.addEventListener('touchcancel', clear, { passive: true });
  }

  function start() {
    initNav();
    setVh();
    window.addEventListener('resize', setVh);
    window.addEventListener('orientationchange', setVh);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }

  window.MobileResponsive = {
    isMobile: isMobile,
    addTouchFeedback: addTouchFeedback,
    closeMenu: function () {
      var header = document.querySelector('body > header');
      if (header) header.classList.remove('vl-nav-open');
    }
  };
})();
