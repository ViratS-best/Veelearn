/**
 * Veelearn Accessibility Utility
 * ARIA labels, aria-live regions, keyboard navigation, focus management
 */

class Accessibility {
    constructor() {
        this.focusableElements = 'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])';
        this.init();
    }

    init() {
        this.addARIALabels();
        this.setupARIALiveRegions();
        this.setupKeyboardNavigation();
        this.setupFocusManagement();
        console.log('Accessibility utility initialized');
    }

    addARIALabels() {
        // Add ARIA labels to buttons without text
        const buttons = document.querySelectorAll('button:not([aria-label])');
        buttons.forEach(button => {
            if (!button.textContent.trim()) {
                const icon = button.querySelector('svg, i, span[class*="icon"]');
                if (icon) {
                    button.setAttribute('aria-label', this.generateLabelFromIcon(icon));
                }
            }
        });

        // Add ARIA labels to inputs without labels
        const inputs = document.querySelectorAll('input:not([aria-label]):not([aria-labelledby])');
        inputs.forEach(input => {
            const placeholder = input.getAttribute('placeholder');
            if (placeholder) {
                input.setAttribute('aria-label', placeholder);
            }
        });

        // Add ARIA labels to links without text
        const links = document.querySelectorAll('a:not([aria-label]):not([aria-labelledby])');
        links.forEach(link => {
            if (!link.textContent.trim()) {
                const img = link.querySelector('img');
                if (img) {
                    const alt = img.getAttribute('alt');
                    if (alt) {
                        link.setAttribute('aria-label', alt);
                    }
                }
            }
        });
    }

    generateLabelFromIcon(icon) {
        const className = icon.className || '';
        if (className.includes('close')) return 'Close';
        if (className.includes('menu') || className.includes('hamburger')) return 'Menu';
        if (className.includes('search')) return 'Search';
        if (className.includes('save')) return 'Save';
        if (className.includes('delete') || className.includes('remove')) return 'Delete';
        if (className.includes('edit') || className.includes('modify')) return 'Edit';
        if (className.includes('add') || className.includes('plus')) return 'Add';
        if (className.includes('arrow') || className.includes('chevron')) return 'Expand';
        return 'Button';
    }

    setupARIALiveRegions() {
        // Create live region for announcements
        if (!document.getElementById('aria-live-region')) {
            const liveRegion = document.createElement('div');
            liveRegion.id = 'aria-live-region';
            liveRegion.setAttribute('aria-live', 'polite');
            liveRegion.setAttribute('aria-atomic', 'true');
            liveRegion.className = 'sr-only';
            document.body.appendChild(liveRegion);
        }

        // Create live region for alerts
        if (!document.getElementById('aria-alert-region')) {
            const alertRegion = document.createElement('div');
            alertRegion.id = 'aria-alert-region';
            alertRegion.setAttribute('aria-live', 'assertive');
            alertRegion.setAttribute('aria-atomic', 'true');
            alertRegion.className = 'sr-only';
            document.body.appendChild(alertRegion);
        }
    }

    announce(message, type = 'polite') {
        const regionId = type === 'assertive' ? 'aria-alert-region' : 'aria-live-region';
        const region = document.getElementById(regionId);
        if (region) {
            region.textContent = message;
            setTimeout(() => {
                region.textContent = '';
            }, 1000);
        }
    }

    setupKeyboardNavigation() {
        // Trap focus in modals
        const modals = document.querySelectorAll('.modal, [role="dialog"]');
        modals.forEach(modal => {
            this.trapFocus(modal);
        });

        // Add keyboard shortcuts for common actions
        document.addEventListener('keydown', (e) => {
            // Tab navigation
            if (e.key === 'Tab') {
                this.handleTabNavigation(e);
            }
        });
    }

    trapFocus(element) {
        const focusableElements = element.querySelectorAll(this.focusableElements);
        const firstFocusable = focusableElements[0];
        const lastFocusable = focusableElements[focusableElements.length - 1];

        element.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                if (e.shiftKey) {
                    if (document.activeElement === firstFocusable) {
                        e.preventDefault();
                        lastFocusable.focus();
                    }
                } else {
                    if (document.activeElement === lastFocusable) {
                        e.preventDefault();
                        firstFocusable.focus();
                    }
                }
            }
        });

        // Focus first element when modal opens
        if (firstFocusable) {
            firstFocusable.focus();
        }
    }

    handleTabNavigation(e) {
        // Handle tab navigation for custom components
        if (document.activeElement.closest('[role="listbox"]')) {
            this.handleListboxNavigation(e);
        }
    }

    handleListboxNavigation(e) {
        const listbox = document.activeElement.closest('[role="listbox"]');
        if (!listbox) return;

        const items = listbox.querySelectorAll('[role="option"]');
        const currentIndex = Array.from(items).indexOf(document.activeElement);

        if (e.key === 'ArrowDown') {
            e.preventDefault();
            const nextIndex = (currentIndex + 1) % items.length;
            items[nextIndex].focus();
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            const prevIndex = (currentIndex - 1 + items.length) % items.length;
            items[prevIndex].focus();
        } else if (e.key === 'Home') {
            e.preventDefault();
            items[0].focus();
        } else if (e.key === 'End') {
            e.preventDefault();
            items[items.length - 1].focus();
        }
    }

    setupFocusManagement() {
        // Add skip to content link
        if (!document.getElementById('skip-to-content')) {
            const skipLink = document.createElement('a');
            skipLink.id = 'skip-to-content';
            skipLink.href = '#main-content';
            skipLink.textContent = 'Skip to main content';
            skipLink.className = 'skip-to-content';
            document.body.insertBefore(skipLink, document.body.firstChild);
        }

        // Add main landmark if missing
        if (!document.querySelector('main')) {
            const main = document.querySelector('[role="main"]') || document.createElement('main');
            main.id = 'main-content';
            if (!document.querySelector('main, [role="main"]')) {
                document.body.appendChild(main);
            }
        }

        // Manage focus when elements are shown/hidden
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'childList') {
                    mutation.addedNodes.forEach((node) => {
                        if (node.nodeType === 1) {
                            if (node.classList.contains('modal') || node.getAttribute('role') === 'dialog') {
                                this.trapFocus(node);
                            }
                        }
                    });
                }
            });
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    setFocus(element) {
        if (element) {
            element.focus();
            this.announce(`Focused on ${element.tagName.toLowerCase()}`);
        }
    }

    restoreFocus(previousElement) {
        if (previousElement && document.body.contains(previousElement)) {
            previousElement.focus();
        }
    }

    addLandmarks() {
        // Ensure proper landmark regions
        if (!document.querySelector('header, [role="banner"]')) {
            const header = document.querySelector('header') || document.createElement('header');
            header.setAttribute('role', 'banner');
        }

        if (!document.querySelector('nav, [role="navigation"]')) {
            const nav = document.querySelector('nav') || document.createElement('nav');
            nav.setAttribute('role', 'navigation');
        }

        if (!document.querySelector('footer, [role="contentinfo"]')) {
            const footer = document.querySelector('footer') || document.createElement('footer');
            footer.setAttribute('role', 'contentinfo');
        }
    }

    setRole(element, role) {
        if (element) {
            element.setAttribute('role', role);
        }
    }

    setHidden(element, isHidden) {
        if (element) {
            element.setAttribute('aria-hidden', isHidden.toString());
        }
    }

    setExpanded(element, isExpanded) {
        if (element) {
            element.setAttribute('aria-expanded', isExpanded.toString());
        }
    }

    setLabel(element, label) {
        if (element) {
            element.setAttribute('aria-label', label);
        }
    }

    setLabelledBy(element, labelledById) {
        if (element) {
            element.setAttribute('aria-labelledby', labelledById);
        }
    }

    setDescribedBy(element, describedById) {
        if (element) {
            element.setAttribute('aria-describedby', describedById);
        }
    }
}

// Initialize global accessibility
window.accessibility = new Accessibility();

console.log('Accessibility utility loaded');
