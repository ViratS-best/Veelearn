/**
 * Veelearn Loading States Utility
 * Global loading overlay, button loading states, skeleton loaders
 */

class LoadingManager {
    constructor() {
        this.overlay = null;
        this.activeLoaders = 0;
        this.init();
    }

    init() {
        // Create global loading overlay
        this.createOverlay();
    }

    createOverlay() {
        this.overlay = document.createElement('div');
        this.overlay.id = 'global-loading-overlay';
        this.overlay.className = 'global-loading-overlay';
        this.overlay.innerHTML = `
            <div class="loading-spinner"></div>
            <div class="loading-text">Loading...</div>
        `;
        document.body.appendChild(this.overlay);
    }

    show(message = 'Loading...') {
        this.activeLoaders++;
        if (this.overlay) {
            this.overlay.querySelector('.loading-text').textContent = message;
            this.overlay.classList.add('active');
        }
    }

    hide() {
        this.activeLoaders = Math.max(0, this.activeLoaders - 1);
        if (this.activeLoaders === 0 && this.overlay) {
            this.overlay.classList.remove('active');
        }
    }

    setButtonLoading(button, isLoading, originalText = '') {
        if (!button) return;

        if (isLoading) {
            button.dataset.originalText = originalText || button.textContent;
            button.dataset.loading = 'true';
            button.disabled = true;
            button.innerHTML = `
                <span class="btn-spinner"></span>
                <span class="btn-text">${originalText || 'Loading...'}</span>
            `;
        } else {
            button.dataset.loading = 'false';
            button.disabled = false;
            button.textContent = button.dataset.originalText || originalText;
        }
    }

    showSkeleton(container, count = 3, type = 'card') {
        if (!container) return;

        const skeletonHTML = Array(count).fill(0).map(() => {
            if (type === 'card') {
                return `
                    <div class="skeleton-card">
                        <div class="skeleton-image"></div>
                        <div class="skeleton-title"></div>
                        <div class="skeleton-text"></div>
                        <div class="skeleton-text short"></div>
                    </div>
                `;
            } else if (type === 'list') {
                return `
                    <div class="skeleton-list-item">
                        <div class="skeleton-avatar"></div>
                        <div class="skeleton-content">
                            <div class="skeleton-title"></div>
                            <div class="skeleton-text short"></div>
                        </div>
                    </div>
                `;
            }
            return '';
        }).join('');

        container.innerHTML = `<div class="skeleton-container">${skeletonHTML}</div>`;
    }

    hideSkeleton(container) {
        if (!container) return;
        container.innerHTML = '';
    }
}

// Initialize global loading manager
window.loadingManager = new LoadingManager();

// Helper functions for common loading patterns
window.withLoading = async (fn, message = 'Loading...') => {
    window.loadingManager.show(message);
    try {
        const result = await fn();
        return result;
    } finally {
        window.loadingManager.hide();
    }
};

window.withButtonLoading = async (button, fn, loadingText = 'Loading...') => {
    const originalText = button.textContent;
    window.loadingManager.setButtonLoading(button, true, loadingText);
    try {
        const result = await fn();
        return result;
    } finally {
        window.loadingManager.setButtonLoading(button, false, originalText);
    }
};
