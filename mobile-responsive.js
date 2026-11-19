/**
 * Veelearn Mobile Responsiveness Utility
 * Touch controls, hamburger menu, swipe gestures
 */

class MobileResponsive {
    constructor() {
        this.touchStartX = 0;
        this.touchStartY = 0;
        this.touchEndX = 0;
        this.touchEndY = 0;
        this.minSwipeDistance = 50;
        this.init();
    }

    init() {
        this.setupTouchControls();
        this.createHamburgerMenu();
        this.setupSwipeGestures();
        this.adjustViewportHeight();
        console.log('Mobile responsiveness initialized');
    }

    setupTouchControls() {
        // Add touch-friendly classes to interactive elements
        const touchTargets = document.querySelectorAll('button, a, input[type="button"], input[type="submit"]');
        touchTargets.forEach(target => {
            target.classList.add('touch-target');
            target.style.minHeight = '44px';
            target.style.minWidth = '44px';
        });

        // Prevent double-tap zoom on buttons
        document.addEventListener('touchend', (e) => {
            if (e.target.tagName === 'BUTTON' || e.target.closest('button')) {
                e.preventDefault();
                e.target.click();
            }
        });
    }

    createHamburgerMenu() {
        // Check if hamburger menu already exists
        if (document.getElementById('hamburger-menu')) return;

        const hamburger = document.createElement('button');
        hamburger.id = 'hamburger-menu';
        hamburger.className = 'hamburger-menu';
        hamburger.setAttribute('aria-label', 'Toggle menu');
        hamburger.setAttribute('aria-expanded', 'false');
        hamburger.innerHTML = `
            <span class="hamburger-line"></span>
            <span class="hamburger-line"></span>
            <span class="hamburger-line"></span>
        `;

        // Add to header if exists, otherwise to body
        const header = document.querySelector('header, nav');
        if (header) {
            header.appendChild(hamburger);
        } else {
            document.body.appendChild(hamburger);
        }

        // Create mobile menu
        this.createMobileMenu();

        // Setup toggle
        hamburger.addEventListener('click', () => this.toggleMobileMenu());
    }

    createMobileMenu() {
        if (document.getElementById('mobile-menu')) return;

        const mobileMenu = document.createElement('div');
        mobileMenu.id = 'mobile-menu';
        mobileMenu.className = 'mobile-menu';
        mobileMenu.setAttribute('aria-hidden', 'true');
        
        // Add navigation links (customize based on actual navigation)
        mobileMenu.innerHTML = `
            <nav class="mobile-nav">
                <a href="#home" class="mobile-nav-link">Home</a>
                <a href="#courses" class="mobile-nav-link">Courses</a>
                <a href="#simulators" class="mobile-nav-link">Simulators</a>
                <a href="#marketplace" class="mobile-nav-link">Marketplace</a>
                <a href="#profile" class="mobile-nav-link">Profile</a>
            </nav>
        `;

        document.body.appendChild(mobileMenu);

        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('#hamburger-menu') && !e.target.closest('#mobile-menu')) {
                this.closeMobileMenu();
            }
        });

        // Close menu on link click
        mobileMenu.querySelectorAll('.mobile-nav-link').forEach(link => {
            link.addEventListener('click', () => this.closeMobileMenu());
        });
    }

    toggleMobileMenu() {
        const menu = document.getElementById('mobile-menu');
        const hamburger = document.getElementById('hamburger-menu');
        
        if (!menu || !hamburger) return;

        const isOpen = menu.classList.contains('open');
        
        if (isOpen) {
            this.closeMobileMenu();
        } else {
            this.openMobileMenu();
        }
    }

    openMobileMenu() {
        const menu = document.getElementById('mobile-menu');
        const hamburger = document.getElementById('hamburger-menu');
        
        if (!menu || !hamburger) return;

        menu.classList.add('open');
        menu.setAttribute('aria-hidden', 'false');
        hamburger.classList.add('open');
        hamburger.setAttribute('aria-expanded', 'true');
        document.body.style.overflow = 'hidden';
    }

    closeMobileMenu() {
        const menu = document.getElementById('mobile-menu');
        const hamburger = document.getElementById('hamburger-menu');
        
        if (!menu || !hamburger) return;

        menu.classList.remove('open');
        menu.setAttribute('aria-hidden', 'true');
        hamburger.classList.remove('open');
        hamburger.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
    }

    setupSwipeGestures() {
        document.addEventListener('touchstart', (e) => {
            this.touchStartX = e.changedTouches[0].screenX;
            this.touchStartY = e.changedTouches[0].screenY;
        }, { passive: true });

        document.addEventListener('touchend', (e) => {
            this.touchEndX = e.changedTouches[0].screenX;
            this.touchEndY = e.changedTouches[0].screenY;
            this.handleSwipe();
        }, { passive: true });
    }

    handleSwipe() {
        const deltaX = this.touchEndX - this.touchStartX;
        const deltaY = this.touchEndY - this.touchStartY;

        // Check if it's a horizontal swipe
        if (Math.abs(deltaX) > Math.abs(deltaY)) {
            if (Math.abs(deltaX) > this.minSwipeDistance) {
                if (deltaX > 0) {
                    this.handleSwipeRight();
                } else {
                    this.handleSwipeLeft();
                }
            }
        }
    }

    handleSwipeLeft() {
        // Swipe left - open menu or go back
        const menu = document.getElementById('mobile-menu');
        if (menu && !menu.classList.contains('open')) {
            this.openMobileMenu();
        }
    }

    handleSwipeRight() {
        // Swipe right - close menu
        const menu = document.getElementById('mobile-menu');
        if (menu && menu.classList.contains('open')) {
            this.closeMobileMenu();
        }
    }

    adjustViewportHeight() {
        // Fix viewport height on mobile browsers (especially iOS)
        const setVh = () => {
            const vh = window.innerHeight * 0.01;
            document.documentElement.style.setProperty('--vh', `${vh}px`);
        };

        setVh();
        window.addEventListener('resize', setVh);
        window.addEventListener('orientationchange', setVh);
    }

    isMobile() {
        return window.innerWidth <= 768;
    }

    addTouchFeedback(element) {
        element.addEventListener('touchstart', () => {
            element.classList.add('touch-active');
        }, { passive: true });

        element.addEventListener('touchend', () => {
            setTimeout(() => {
                element.classList.remove('touch-active');
            }, 100);
        }, { passive: true });

        element.addEventListener('touchcancel', () => {
            element.classList.remove('touch-active');
        }, { passive: true });
    }
}

// Initialize global mobile responsiveness
window.mobileResponsive = new MobileResponsive();

console.log('Mobile responsiveness utility loaded');
