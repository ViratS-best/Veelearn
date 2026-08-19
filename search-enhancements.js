/**
 * Veelearn Search Enhancements Utility
 * Highlight matches, advanced filters, search history
 */

class SearchEnhancements {
    constructor() {
        this.searchHistory = this.loadSearchHistory();
        this.maxHistoryItems = 10;
        this.init();
    }

    init() {
        this.setupSearchHistory();
        console.log('Search enhancements initialized');
    }

    loadSearchHistory() {
        const stored = localStorage.getItem('veelearn-search-history');
        return stored ? JSON.parse(stored) : [];
    }

    saveSearchHistory() {
        localStorage.setItem('veelearn-search-history', JSON.stringify(this.searchHistory));
    }

    addToSearchHistory(query) {
        if (!query || query.trim().length === 0) return;
        
        // Remove if already exists
        this.searchHistory = this.searchHistory.filter(item => item.query !== query);
        
        // Add to beginning
        this.searchHistory.unshift({
            query: query,
            timestamp: new Date().toISOString()
        });
        
        // Keep only max items
        this.searchHistory = this.searchHistory.slice(0, this.maxHistoryItems);
        
        this.saveSearchHistory();
    }

    getSearchHistory() {
        return this.searchHistory;
    }

    clearSearchHistory() {
        this.searchHistory = [];
        this.saveSearchHistory();
    }

    setupSearchHistory() {
        // Add to history when search is performed
        const originalSearch = window.renderAvailableCourses || window.renderUserCourses;
        
        if (originalSearch) {
            // This would be integrated with existing search functions
            console.log('Search history integration ready');
        }
    }

    highlightText(text, query) {
        if (!query || query.trim().length === 0) return text;
        
        const regex = new RegExp(`(${this.escapeRegex(query)})`, 'gi');
        return text.replace(regex, '<mark class="search-highlight">$1</mark>');
    }

    escapeRegex(text) {
        return text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    applyHighlight(element, query) {
        if (!element || !query) return;
        
        const walker = document.createTreeWalker(
            element,
            NodeFilter.SHOW_TEXT,
            null,
            false
        );
        
        const nodesToReplace = [];
        let node;
        
        while (node = walker.nextNode()) {
            if (node.nodeValue.toLowerCase().includes(query.toLowerCase())) {
                nodesToReplace.push(node);
            }
        }
        
        nodesToReplace.forEach(node => {
            const span = document.createElement('span');
            span.innerHTML = this.highlightText(node.nodeValue, query);
            node.parentNode.replaceChild(span, node);
        });
    }

    removeHighlight(element) {
        if (!element) return;
        
        const highlights = element.querySelectorAll('.search-highlight');
        highlights.forEach(highlight => {
            const parent = highlight.parentNode;
            parent.replaceChild(document.createTextNode(highlight.textContent), highlight);
            parent.normalize();
        });
    }

    createAdvancedFilters(container) {
        if (!container) return;

        const filtersHTML = `
            <div class="advanced-filters">
                <div class="filter-group">
                    <label>Grade Level</label>
                    <select class="filter-select" data-filter="grade-level">
                        <option value="">All</option>
                        <option value="1">Grade 1</option>
                        <option value="2">Grade 2</option>
                        <option value="3">Grade 3</option>
                        <option value="4">Grade 4</option>
                        <option value="5">Grade 5</option>
                        <option value="6">Grade 6</option>
                        <option value="7">Grade 7</option>
                        <option value="8">Grade 8</option>
                        <option value="9">Grade 9</option>
                        <option value="10">Grade 10</option>
                        <option value="11">Grade 11</option>
                        <option value="12">Grade 12</option>
                        <option value="13">College</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label>Status</label>
                    <select class="filter-select" data-filter="status">
                        <option value="">All</option>
                        <option value="approved">Approved</option>
                        <option value="draft">Draft</option>
                        <option value="pending">Pending</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label>Sort By</label>
                    <select class="filter-select" data-filter="sort">
                        <option value="newest">Newest First</option>
                        <option value="oldest">Oldest First</option>
                        <option value="title">Title A-Z</option>
                        <option value="title-desc">Title Z-A</option>
                    </select>
                </div>
                <button class="clear-filters-btn">Clear Filters</button>
            </div>
        `;

        container.insertAdjacentHTML('afterbegin', filtersHTML);
        
        // Setup event listeners
        container.querySelectorAll('.filter-select').forEach(select => {
            select.addEventListener('change', () => this.applyFilters(container));
        });
        
        container.querySelector('.clear-filters-btn')?.addEventListener('click', () => {
            container.querySelectorAll('.filter-select').forEach(select => {
                select.value = '';
            });
            this.applyFilters(container);
        });
    }

    applyFilters(container) {
        const gradeLevel = container.querySelector('[data-filter="grade-level"]')?.value;
        const status = container.querySelector('[data-filter="status"]')?.value;
        const sortBy = container.querySelector('[data-filter="sort"]')?.value;
        
        // This would integrate with existing filter logic
        console.log('Filters applied:', { gradeLevel, status, sortBy });
    }

    showSearchHistoryDropdown(inputElement) {
        if (!inputElement) return;

        const existingDropdown = document.getElementById('search-history-dropdown');
        if (existingDropdown) existingDropdown.remove();

        if (this.searchHistory.length === 0) return;

        const dropdown = document.createElement('div');
        dropdown.id = 'search-history-dropdown';
        dropdown.className = 'search-history-dropdown';
        dropdown.innerHTML = `
            <div class="search-history-header">
                <span>Recent Searches</span>
                <button class="clear-history-btn">Clear</button>
            </div>
            <ul class="search-history-list">
                ${this.searchHistory.map(item => `
                    <li class="search-history-item" data-query="${this.escapeHtml(item.query)}">
                        ${this.escapeHtml(item.query)}
                    </li>
                `).join('')}
            </ul>
        `;

        inputElement.parentNode.appendChild(dropdown);

        // Setup event listeners
        dropdown.querySelector('.clear-history-btn')?.addEventListener('click', () => {
            this.clearSearchHistory();
            dropdown.remove();
        });

        dropdown.querySelectorAll('.search-history-item').forEach(item => {
            item.addEventListener('click', () => {
                const query = item.dataset.query;
                inputElement.value = query;
                inputElement.dispatchEvent(new Event('input'));
                dropdown.remove();
            });
        });

        // Close on click outside
        document.addEventListener('click', (e) => {
            if (!dropdown.contains(e.target) && e.target !== inputElement) {
                dropdown.remove();
            }
        });
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize global search enhancements
window.searchEnhancements = new SearchEnhancements();

console.log('Search enhancements utility loaded');
