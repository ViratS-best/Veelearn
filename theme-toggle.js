/**
 * Veelearn Theme Toggle Utility
 * Dark/Light mode toggle with localStorage persistence and transitions
 */

class ThemeToggle {
    constructor() {
        this.currentTheme = this.getStoredTheme() || this.getSystemTheme();
        this.init();
    }

    init() {
        this.applyTheme(this.currentTheme);
        this.createToggleButton();
        this.setupEventListeners();
        console.log('Theme toggle initialized:', this.currentTheme);
    }

    getStoredTheme() {
        return localStorage.getItem('veelearn-theme');
    }

    getSystemTheme() {
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }

    applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('veelearn-theme', theme);
        this.currentTheme = theme;
        
        // Update toggle button state
        const toggleButton = document.getElementById('theme-toggle');
        if (toggleButton) {
            toggleButton.setAttribute('aria-pressed', theme === 'dark');
            toggleButton.innerHTML = theme === 'dark' ? '☀️' : '🌙';
        }
    }

    toggleTheme() {
        const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.applyTheme(newTheme);
    }

    createToggleButton() {
        // Check if button already exists
        if (document.getElementById('theme-toggle')) {
            return;
        }

        const toggleButton = document.createElement('button');
        toggleButton.id = 'theme-toggle';
        toggleButton.className = 'theme-toggle';
        toggleButton.setAttribute('aria-label', 'Toggle dark/light mode');
        toggleButton.setAttribute('aria-pressed', this.currentTheme === 'dark');
        toggleButton.innerHTML = this.currentTheme === 'dark' ? '☀️' : '🌙';
        
        // Position the button in the header
        const header = document.querySelector('header, nav, .navbar');
        if (header) {
            header.appendChild(toggleButton);
        } else {
            // Fallback: add to body
            document.body.appendChild(toggleButton);
        }
    }

    setupEventListeners() {
        // Listen for system theme changes
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            if (!this.getStoredTheme()) {
                this.applyTheme(e.matches ? 'dark' : 'light');
            }
        });

        // Listen for toggle button clicks
        document.addEventListener('click', (e) => {
            if (e.target.id === 'theme-toggle' || e.target.closest('#theme-toggle')) {
                this.toggleTheme();
            }
        });
    }
}

// Initialize global theme toggle
window.themeToggle = new ThemeToggle();

console.log('Theme toggle utility loaded');
