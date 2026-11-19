/**
 * Marketplace App - UI logic for browsing and managing simulators
 * ~550 lines
 */

class MarketplaceApp {
    constructor(api) {
        this.api = api;
        this.simulators = [];
        this.currentPage = 1;
        this.totalPages = 1;
        this.filters = {
            search: '',
            tags: [],
            difficulty: null,
            minRating: 0
        };
        this.sort = 'newest';
        this.itemsPerPage = 20;
        this.currentUser = null;
        this.selectedSimulator = null;
        this.isLoading = false;
    }

    /**
     * Initialize marketplace
     * @param {Object} user - Current user (optional)
     */
    async initialize(user = null) {
        this.currentUser = user;
        await this.loadFeaturedSimulators();
    }

    /**
     * Load featured simulators
     * @returns {Promise<Array>}
     */
    async loadFeaturedSimulators() {
        try {
            this.isLoading = true;
            return await this.api.getFeaturedSimulators(10);
        } catch (error) {
            console.error('Failed to load featured simulators:', error);
            return [];
        } finally {
            this.isLoading = false;
        }
    }

    /**
     * Browse simulators with filters
     * @param {Number} page - Page number
     * @returns {Promise<Object>} Paginated results
     */
    async browseSimulators(page = 1) {
        try {
            this.isLoading = true;
            this.currentPage = page;

            const result = await this.api.getSimulators(page, {
                search: this.filters.search,
                sort: this.sort,
                limit: this.itemsPerPage,
                filter: this.getActiveFilters()
            });

            this.simulators = result.data || result;
            this.totalPages = result.totalPages || Math.ceil(this.simulators.length / this.itemsPerPage);

            return {
                simulators: this.simulators,
                currentPage: this.currentPage,
                totalPages: this.totalPages
            };
        } catch (error) {
            console.error('Failed to browse simulators:', error);
            return { simulators: [], currentPage: page, totalPages: 1 };
        } finally {
            this.isLoading = false;
        }
    }

    /**
     * Search simulators
     * @param {String} query - Search query
     * @returns {Promise<Array>} Results
     */
    async searchSimulators(query) {
        try {
            this.isLoading = true;
            this.filters.search = query;
            this.currentPage = 1;

            return await this.browseSimulators(1);
        } catch (error) {
            console.error('Search failed:', error);
            return { simulators: [], currentPage: 1, totalPages: 1 };
        } finally {
            this.isLoading = false;
        }
    }

    /**
     * Apply filter
     * @param {String} filterType - Filter type (tags, difficulty, rating)
     * @param {*} value - Filter value
     */
    setFilter(filterType, value) {
        if (filterType === 'tags') {
            if (this.filters.tags.includes(value)) {
                this.filters.tags = this.filters.tags.filter(t => t !== value);
            } else {
                this.filters.tags.push(value);
            }
        } else {
            this.filters[filterType] = value;
        }
        this.currentPage = 1;
    }

    /**
     * Clear all filters
     */
    clearFilters() {
        this.filters = {
            search: '',
            tags: [],
            difficulty: null,
            minRating: 0
        };
        this.currentPage = 1;
    }

    /**
     * Get active filters as object
     * @returns {Object} Active filters
     */
    getActiveFilters() {
        const active = {};
        if (this.filters.search) active.search = this.filters.search;
        if (this.filters.tags.length > 0) active.tags = this.filters.tags.join(',');
        if (this.filters.difficulty) active.difficulty = this.filters.difficulty;
        if (this.filters.minRating > 0) active.minRating = this.filters.minRating;
        return active;
    }

    /**
     * Set sort order
     * @param {String} sortType - Sort type (newest, popular, trending, highest-rated)
     */
    setSort(sortType) {
        this.sort = sortType;
        this.currentPage = 1;
    }

    /**
     * Get simulator details
     * @param {Number} id - Simulator ID
     * @returns {Promise<Object>}
     */
    async getSimulatorDetails(id) {
        try {
            this.isLoading = true;
            const simulator = await this.api.getSimulatorById(id);
            const ratings = await this.api.getSimulatorRatings(id);
            const comments = await this.api.getSimulatorComments(id);

            this.selectedSimulator = {
                ...simulator,
                ratings,
                comments
            };

            return this.selectedSimulator;
        } catch (error) {
            console.error('Failed to get simulator details:', error);
            return null;
        } finally {
            this.isLoading = false;
        }
    }

    /**
     * Create new simulator
     * @param {Object} data - {title, description, blocks, connections, tags}
     * @returns {Promise<Object>}
     */
    async createSimulator(data) {
        try {
            this.isLoading = true;
            return await this.api.createSimulator(data);
        } catch (error) {
            console.error('Failed to create simulator:', error);
            throw error;
        } finally {
            this.isLoading = false;
        }
    }

    /**
     * Update simulator
     * @param {Number} id - Simulator ID
     * @param {Object} data - Updated data
     * @returns {Promise<Object>}
     */
    async updateSimulator(id, data) {
        try {
            this.isLoading = true;
            return await this.api.updateSimulator(id, data);
        } catch (error) {
            console.error('Failed to update simulator:', error);
            throw error;
        } finally {
            this.isLoading = false;
        }
    }

    /**
     * Delete simulator
     * @param {Number} id - Simulator ID
     * @returns {Promise}
     */
    async deleteSimulator(id) {
        try {
            this.isLoading = true;
            await this.api.deleteSimulator(id);
            this.simulators = this.simulators.filter(s => s.id !== id);
        } catch (error) {
            console.error('Failed to delete simulator:', error);
            throw error;
        } finally {
            this.isLoading = false;
        }
    }

    /**
     * Publish simulator
     * @param {Number} id - Simulator ID
     * @returns {Promise<Object>}
     */
    async publishSimulator(id) {
        try {
            this.isLoading = true;
            return await this.api.publishSimulator(id);
        } catch (error) {
            console.error('Failed to publish simulator:', error);
            throw error;
        } finally {
            this.isLoading = false;
        }
    }

    /**
     * Rate simulator
     * @param {Number} id - Simulator ID
     * @param {Number} rating - Rating (1-5)
     * @param {String} review - Review text
     * @returns {Promise<Object>}
     */
    async rateSimulator(id, rating, review = '') {
        try {
            if (!this.api.isAuthenticated()) {
                throw new Error('Must be logged in to rate');
            }
            return await this.api.rateSimulator(id, rating, review);
        } catch (error) {
            console.error('Failed to rate simulator:', error);
            throw error;
        }
    }

    /**
     * Comment on simulator
     * @param {Number} id - Simulator ID
     * @param {String} comment - Comment text
     * @returns {Promise<Object>}
     */
    async commentOnSimulator(id, comment) {
        try {
            if (!this.api.isAuthenticated()) {
                throw new Error('Must be logged in to comment');
            }
            return await this.api.commentOnSimulator(id, comment);
        } catch (error) {
            console.error('Failed to comment:', error);
            throw error;
        }
    }

    /**
     * Download simulator
     * @param {Number} id - Simulator ID
     * @returns {Promise<Object>}
     */
    async downloadSimulator(id) {
        try {
            if (!this.api.isAuthenticated()) {
                throw new Error('Must be logged in to download');
            }
            return await this.api.downloadSimulator(id);
        } catch (error) {
            console.error('Failed to download simulator:', error);
            throw error;
        }
    }

    /**
     * Fork simulator
     * @param {Number} id - Simulator ID
     * @param {String} newTitle - Title for fork
     * @returns {Promise<Object>}
     */
    async forkSimulator(id, newTitle) {
        try {
            if (!this.api.isAuthenticated()) {
                throw new Error('Must be logged in to fork');
            }
            return await this.api.forkSimulator(id, newTitle);
        } catch (error) {
            console.error('Failed to fork simulator:', error);
            throw error;
        }
    }

    /**
     * Get user's simulators
     * @returns {Promise<Array>}
     */
    async getMySimulators() {
        try {
            if (!this.api.isAuthenticated()) {
                throw new Error('Must be logged in');
            }
            this.isLoading = true;
            return await this.api.getMySimulators();
        } catch (error) {
            console.error('Failed to load my simulators:', error);
            return [];
        } finally {
            this.isLoading = false;
        }
    }

    /**
     * Get creator profile
     * @param {Number} userId - User ID
     * @returns {Promise<Object>}
     */
    async getCreatorProfile(userId) {
        try {
            this.isLoading = true;
            const profile = await this.api.getCreatorProfile(userId);
            const simulators = await this.api.getCreatorSimulators(userId);
            return {
                ...profile,
                simulators
            };
        } catch (error) {
            console.error('Failed to load creator profile:', error);
            return null;
        } finally {
            this.isLoading = false;
        }
    }

    /**
     * Add simulator to course
     * @param {Number} courseId - Course ID
     * @param {Number} simulatorId - Simulator ID
     * @returns {Promise<Object>}
     */
    async addSimulatorToCourse(courseId, simulatorId) {
        try {
            if (!this.api.isAuthenticated()) {
                throw new Error('Must be logged in');
            }
            return await this.api.addSimulatorToCourse(courseId, simulatorId);
        } catch (error) {
            console.error('Failed to add simulator to course:', error);
            throw error;
        }
    }

    /**
     * Get trending simulators
     * @param {Number} limit - Number to return
     * @returns {Promise<Array>}
     */
    async getTrendingSimulators(limit = 10) {
        try {
            this.isLoading = true;
            return await this.api.getTrendingSimulators(limit);
        } catch (error) {
            console.error('Failed to load trending simulators:', error);
            return [];
        } finally {
            this.isLoading = false;
        }
    }

    /**
     * Get simulator versions
     * @param {Number} id - Simulator ID
     * @returns {Promise<Array>}
     */
    async getSimulatorVersions(id) {
        try {
            this.isLoading = true;
            return await this.api.getSimulatorVersions(id);
        } catch (error) {
            console.error('Failed to load versions:', error);
            return [];
        } finally {
            this.isLoading = false;
        }
    }

    /**
     * Get specific simulator version
     * @param {Number} id - Simulator ID
     * @param {String} version - Version number
     * @returns {Promise<Object>}
     */
    async getSimulatorVersion(id, version) {
        try {
            this.isLoading = true;
            return await this.api.getSimulatorVersion(id, version);
        } catch (error) {
            console.error('Failed to load version:', error);
            return null;
        } finally {
            this.isLoading = false;
        }
    }

    /**
     * Clear cache and reload
     */
    clearCacheAndReload() {
        this.api.clearCache();
        this.simulators = [];
        this.currentPage = 1;
    }

    /**
     * Get statistics
     * @returns {Object} App statistics
     */
    getStats() {
        return {
            totalSimulators: this.simulators.length,
            currentPage: this.currentPage,
            totalPages: this.totalPages,
            itemsPerPage: this.itemsPerPage,
            isLoading: this.isLoading,
            activeFilters: this.getActiveFilters(),
            sortOrder: this.sort
        };
    }
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MarketplaceApp;
}
