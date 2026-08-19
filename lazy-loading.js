/**
 * Veelearn Lazy Loading Utility
 * Lazy load simulators, course content, marketplace images, code splitting
 */

class LazyLoader {
    constructor() {
        this.observerOptions = {
            root: null,
            rootMargin: '50px',
            threshold: 0.1
        };
        this.observer = null;
        this.init();
    }

    init() {
        this.setupImageLazyLoading();
        this.setupContentLazyLoading();
        this.setupIntersectionObserver();
        console.log('Lazy loading initialized');
    }

    setupIntersectionObserver() {
        if ('IntersectionObserver' in window) {
            this.observer = new IntersectionObserver(
                this.handleIntersection.bind(this),
                this.observerOptions
            );
        }
    }

    handleIntersection(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const element = entry.target;
                this.loadElement(element);
                this.observer.unobserve(element);
            }
        });
    }

    loadElement(element) {
        if (element.dataset.src) {
            element.src = element.dataset.src;
            delete element.dataset.src;
        }

        if (element.dataset.bg) {
            element.style.backgroundImage = `url(${element.dataset.bg})`;
            delete element.dataset.bg;
        }

        if (element.dataset.content) {
            this.loadContent(element, element.dataset.content);
            delete element.dataset.content;
        }

        element.classList.add('loaded');
    }

    setupImageLazyLoading() {
        // Add loading="lazy" to all images
        const images = document.querySelectorAll('img:not([loading])');
        images.forEach(img => {
            img.loading = 'lazy';
            img.classList.add('lazy-image');
        });

        // Observe images with data-src
        const lazyImages = document.querySelectorAll('img[data-src], [data-bg]');
        lazyImages.forEach(img => {
            if (this.observer) {
                this.observer.observe(img);
            }
        });
    }

    setupContentLazyLoading() {
        // Find elements with lazy-content class
        const lazyContent = document.querySelectorAll('.lazy-content');
        lazyContent.forEach(element => {
            if (this.observer) {
                this.observer.observe(element);
            }
        });
    }

    async loadContent(element, url) {
        try {
            const response = await fetch(url);
            const html = await response.text();
            element.innerHTML = html;
            element.classList.add('content-loaded');
        } catch (error) {
            console.error('Error loading content:', error);
            element.innerHTML = '<p>Failed to load content</p>';
        }
    }

    loadImage(src, element) {
        const img = new Image();
        img.onload = () => {
            element.src = src;
            element.classList.add('loaded');
        };
        img.onerror = () => {
            element.classList.add('error');
        };
        img.src = src;
    }

    lazyLoadSimulator(simulatorId) {
        return new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = `/simulators/${simulatorId}.js`;
            script.async = true;
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
        });
    }

    lazyLoadCourse(courseId) {
        return new Promise((resolve, reject) => {
            const element = document.querySelector(`[data-course-id="${courseId}"]`);
            if (!element) {
                reject(new Error('Course element not found'));
                return;
            }

            if (this.observer) {
                element.dataset.content = `/api/courses/${courseId}/content`;
                this.observer.observe(element);
            } else {
                this.loadContent(element, `/api/courses/${courseId}/content`);
            }
        });
    }

    preloadCriticalResources() {
        // Preload critical CSS and JS
        const criticalResources = [
            '/styles.css',
            '/script.js'
        ];

        criticalResources.forEach(resource => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.as = resource.endsWith('.css') ? 'style' : 'script';
            link.href = resource;
            document.head.appendChild(link);
        });
    }

    observeElement(element) {
        if (this.observer && element) {
            this.observer.observe(element);
        }
    }

    unobserveElement(element) {
        if (this.observer && element) {
            this.observer.unobserve(element);
        }
    }

    disconnect() {
        if (this.observer) {
            this.observer.disconnect();
        }
    }
}

// Initialize global lazy loader
window.lazyLoader = new LazyLoader();

// Auto-initialize lazy loading on DOM content loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.lazyLoader.setupImageLazyLoading();
        window.lazyLoader.setupContentLazyLoading();
    });
} else {
    window.lazyLoader.setupImageLazyLoading();
    window.lazyLoader.setupContentLazyLoading();
}

console.log('Lazy loading utility loaded');
