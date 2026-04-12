/**
 * Veelearn Auto-Save Utility
 * Saving indicator, last saved timestamp, manual save Ctrl+S, conflict resolution
 */

class AutoSaveManager {
    constructor() {
        this.saveInterval = 30000; // 30 seconds
        this.autoSaveEnabled = true;
        this.lastSaved = null;
        this.saveIndicator = null;
        this.pendingSave = false;
        this.conflictDetected = false;
        this.init();
    }

    init() {
        this.createSaveIndicator();
        this.setupEventListeners();
        console.log('Auto-save manager initialized');
    }

    createSaveIndicator() {
        // Remove existing indicator if present
        const existing = document.getElementById('auto-save-indicator');
        if (existing) existing.remove();

        this.saveIndicator = document.createElement('div');
        this.saveIndicator.id = 'auto-save-indicator';
        this.saveIndicator.className = 'auto-save-indicator';
        this.saveIndicator.innerHTML = `
            <span class="save-status">Ready</span>
            <span class="save-timestamp"></span>
        `;
        document.body.appendChild(this.saveIndicator);
    }

    setupEventListeners() {
        // Listen for Ctrl+S for manual save
        document.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 's') {
                e.preventDefault();
                this.triggerManualSave();
            }
        });

        // Listen for editor activity
        document.addEventListener('input', this.handleEditorActivity.bind(this));
    }

    handleEditorActivity() {
        if (this.autoSaveEnabled && !this.pendingSave) {
            this.pendingSave = true;
            this.updateStatus('Unsaved changes...');
            
            // Debounce auto-save
            clearTimeout(this.saveTimeout);
            this.saveTimeout = setTimeout(() => {
                this.triggerAutoSave();
            }, 5000); // 5 seconds of inactivity
        }
    }

    async triggerAutoSave() {
        if (!this.autoSaveEnabled || this.conflictDetected) return;

        this.updateStatus('Saving...');
        
        try {
            // Call the save function if available
            if (typeof saveCourse === 'function') {
                await saveCourse();
            }
            
            this.lastSaved = new Date();
            this.updateStatus('Saved', this.lastSaved);
            this.pendingSave = false;
            
            if (window.logger) {
                window.logger.debug('Auto-save completed at:', this.lastSaved);
            }
        } catch (error) {
            this.updateStatus('Save failed');
            console.error('Auto-save error:', error);
            
            if (window.errorHandler) {
                window.errorHandler.showError(error, 'Auto-save failed');
            }
        }
    }

    async triggerManualSave() {
        this.updateStatus('Saving...');
        
        try {
            // Call the save function if available
            if (typeof saveCourse === 'function') {
                await saveCourse();
            }
            
            this.lastSaved = new Date();
            this.updateStatus('Saved', this.lastSaved);
            this.pendingSave = false;
            
            // Show brief success message
            this.showSaveNotification('Manual save successful');
            
            if (window.logger) {
                window.logger.debug('Manual save completed at:', this.lastSaved);
            }
        } catch (error) {
            this.updateStatus('Save failed');
            console.error('Manual save error:', error);
            
            if (window.errorHandler) {
                window.errorHandler.showError(error, 'Manual save failed');
            }
        }
    }

    updateStatus(status, timestamp = null) {
        if (!this.saveIndicator) return;

        const statusEl = this.saveIndicator.querySelector('.save-status');
        const timestampEl = this.saveIndicator.querySelector('.save-timestamp');

        if (statusEl) {
            statusEl.textContent = status;
            statusEl.className = 'save-status ' + status.toLowerCase().replace(' ', '-');
        }

        if (timestampEl && timestamp) {
            timestampEl.textContent = this.formatTimestamp(timestamp);
        } else if (timestampEl) {
            timestampEl.textContent = '';
        }
    }

    formatTimestamp(date) {
        const now = new Date();
        const diff = now - date;
        
        if (diff < 60000) {
            return 'Just now';
        } else if (diff < 3600000) {
            const minutes = Math.floor(diff / 60000);
            return `${minutes}m ago`;
        } else {
            const hours = Math.floor(diff / 3600000);
            return `${hours}h ago`;
        }
    }

    showSaveNotification(message) {
        const notification = document.createElement('div');
        notification.className = 'save-notification';
        notification.textContent = message;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('fade-out');
            setTimeout(() => notification.remove(), 300);
        }, 2000);
    }

    enableAutoSave() {
        this.autoSaveEnabled = true;
        console.log('Auto-save enabled');
    }

    disableAutoSave() {
        this.autoSaveEnabled = false;
        console.log('Auto-save disabled');
    }

    handleConflict() {
        this.conflictDetected = true;
        this.updateStatus('Conflict detected');
        
        // Show conflict resolution modal
        this.showConflictModal();
    }

    showConflictModal() {
        const modal = document.createElement('div');
        modal.id = 'conflict-modal';
        modal.className = 'conflict-modal';
        modal.innerHTML = `
            <div class="conflict-content">
                <h2>⚠️ Save Conflict</h2>
                <p>Your changes conflict with another version of this document.</p>
                <div class="conflict-actions">
                    <button class="conflict-btn conflict-btn-primary" onclick="window.autoSaveManager.keepLocal()">
                        Keep My Changes
                    </button>
                    <button class="conflict-btn conflict-btn-secondary" onclick="window.autoSaveManager.keepRemote()">
                        Use Server Version
                    </button>
                    <button class="conflict-btn conflict-btn-tertiary" onclick="window.autoSaveManager.mergeChanges()">
                        Merge Changes
                    </button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }

    keepLocal() {
        this.conflictDetected = false;
        this.removeConflictModal();
        this.triggerManualSave();
    }

    keepRemote() {
        this.conflictDetected = false;
        this.removeConflictModal();
        location.reload(); // Reload to get server version
    }

    mergeChanges() {
        this.conflictDetected = false;
        this.removeConflictModal();
        // Merge logic would go here
        console.log('Merge changes - to be implemented');
    }

    removeConflictModal() {
        const modal = document.getElementById('conflict-modal');
        if (modal) modal.remove();
    }
}

// Initialize global auto-save manager
window.autoSaveManager = new AutoSaveManager();

console.log('Auto-save utility loaded');
