/**
 * Veelearn Keyboard Shortcuts Utility
 * Ctrl+K search, Ctrl+S save, Ctrl+/ shortcuts, Escape modals, Arrow navigation
 */

class KeyboardShortcuts {
    constructor() {
        this.shortcuts = {
            'Ctrl+K': { action: 'focusSearch', description: 'Focus search box' },
            'Ctrl+S': { action: 'save', description: 'Save current work' },
            'Ctrl+/': { action: 'toggleHelp', description: 'Show keyboard shortcuts help' },
            'Escape': { action: 'closeModal', description: 'Close modal or popup' },
            'ArrowUp': { action: 'navigateUp', description: 'Navigate up in lists' },
            'ArrowDown': { action: 'navigateDown', description: 'Navigate down in lists' },
            'Enter': { action: 'select', description: 'Select highlighted item' },
            'Ctrl+Enter': { action: 'submit', description: 'Submit form' },
            'Ctrl+Shift+S': { action: 'saveAs', description: 'Save as new version' }
        };
        
        this.currentFocus = null;
        this.init();
    }

    init() {
        document.addEventListener('keydown', this.handleKeyDown.bind(this));
        console.log('Keyboard shortcuts initialized');
    }

    handleKeyDown(event) {
        // Don't trigger shortcuts when typing in input fields (except specific ones)
        if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA') {
            // Allow Escape and Ctrl+K in input fields
            if (event.key !== 'Escape' && !(event.ctrlKey && event.key === 'k')) {
                return;
            }
        }

        const key = this.getKeyString(event);
        const shortcut = this.shortcuts[key];

        if (shortcut) {
            event.preventDefault();
            this.executeAction(shortcut.action, event);
        }
    }

    getKeyString(event) {
        let key = event.key;
        
        if (event.ctrlKey) {
            key = 'Ctrl+' + key;
        }
        if (event.shiftKey) {
            key = 'Shift+' + key;
        }
        if (event.altKey) {
            key = 'Alt+' + key;
        }
        
        return key;
    }

    executeAction(action, event) {
        switch (action) {
            case 'focusSearch':
                this.focusSearch();
                break;
            case 'save':
                this.saveCurrentWork();
                break;
            case 'toggleHelp':
                this.toggleHelp();
                break;
            case 'closeModal':
                this.closeModal();
                break;
            case 'navigateUp':
                this.navigateUp(event);
                break;
            case 'navigateDown':
                this.navigateDown(event);
                break;
            case 'select':
                this.selectItem(event);
                break;
            case 'submit':
                this.submitForm(event);
                break;
            case 'saveAs':
                this.saveAsNew();
                break;
            default:
                console.log('Unknown action:', action);
        }
    }

    focusSearch() {
        // Try to find and focus available courses search
        const availableSearch = document.getElementById('availableCoursesSearch');
        if (availableSearch) {
            availableSearch.focus();
            return;
        }

        // Try my courses search
        const myCoursesSearch = document.getElementById('myCoursesSearch');
        if (myCoursesSearch) {
            myCoursesSearch.focus();
            return;
        }

        // Try PhET search
        const phetSearch = document.getElementById('phet-search');
        if (phetSearch) {
            phetSearch.focus();
            return;
        }

        console.log('No search input found');
    }

    saveCurrentWork() {
        // Check if we're in course editor
        const saveButton = document.querySelector('#save-course-btn, .save-btn');
        if (saveButton) {
            saveButton.click();
        } else {
            console.log('No save button found');
        }
    }

    toggleHelp() {
        this.showHelpModal();
    }

    closeModal() {
        // Close any open modals
        const modals = document.querySelectorAll('.modal, .error-modal');
        modals.forEach(modal => {
            modal.style.display = 'none';
            modal.remove();
        });

        // Close dropdowns
        const dropdowns = document.querySelectorAll('.dropdown-content.show');
        dropdowns.forEach(dropdown => {
            dropdown.classList.remove('show');
        });
    }

    navigateUp(event) {
        // Navigate up in course lists or menus
        const focused = document.activeElement;
        if (focused && focused.previousElementSibling) {
            focused.previousElementSibling.focus();
        }
    }

    navigateDown(event) {
        // Navigate down in course lists or menus
        const focused = document.activeElement;
        if (focused && focused.nextElementSibling) {
            focused.nextElementSibling.focus();
        }
    }

    selectItem(event) {
        // Select the currently focused item
        const focused = document.activeElement;
        if (focused && focused.tagName === 'BUTTON') {
            focused.click();
        }
    }

    submitForm(event) {
        // Submit the current form
        const form = document.activeElement?.form;
        if (form) {
            form.dispatchEvent(new Event('submit'));
        }
    }

    saveAsNew() {
        console.log('Save as new - to be implemented');
    }

    showHelpModal() {
        // Remove existing help modal
        const existingModal = document.getElementById('keyboard-help-modal');
        if (existingModal) {
            existingModal.remove();
            return;
        }

        const modal = document.createElement('div');
        modal.id = 'keyboard-help-modal';
        modal.className = 'keyboard-help-modal';
        modal.innerHTML = `
            <div class="keyboard-help-content">
                <div class="keyboard-help-header">
                    <h2>⌨️ Keyboard Shortcuts</h2>
                    <button class="close-btn" onclick="document.getElementById('keyboard-help-modal').remove()">&times;</button>
                </div>
                <div class="keyboard-help-body">
                    ${Object.entries(this.shortcuts).map(([key, shortcut]) => `
                        <div class="shortcut-item">
                            <kbd>${this.escapeHtml(key)}</kbd>
                            <span>${this.escapeHtml(shortcut.description)}</span>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;

        document.body.appendChild(modal);
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    addShortcut(key, action, description) {
        this.shortcuts[key] = { action, description };
    }

    removeShortcut(key) {
        delete this.shortcuts[key];
    }
}

// Initialize global keyboard shortcuts
window.keyboardShortcuts = new KeyboardShortcuts();

console.log('Keyboard shortcuts utility loaded');
