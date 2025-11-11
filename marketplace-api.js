/**
 * Marketplace API Client - Frontend API communication
 * ~250 lines
 */

class MarketplaceAPI {
    constructor(baseURL = 'http://localhost:3000/api') {
        this.baseURL = baseURL;
        this.token = localStorage.getItem('auth_token') || null;
        this.cache = new Map();
        this.cacheTimeout = 5 * 60 * 1000; // 5 minutes
    }

    /**
     * Set authentication token
     * @param {String} token - JWT token
     */
    setToken(token) {
        this.token = token;
        localStorage.setItem('auth_token', token);
    }

    /**
     * Make API request
     * @param {String} method - HTTP method
     * @param {String} endpoint - API endpoint
     * @param {Object} data - Request body
     * @returns {Promise<Object>} Response data
     */
    async request(method, endpoint, data = null) {
        const url = `${this.baseURL}${endpoint}`;
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json'
            }
        };

        if (this.token) {
            options.headers['Authorization'] = `Bearer ${this.token}`;
        }

        if (data) {
            options.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(url, options);
            const json = await response.json();

            if (!response.ok) {
                throw new Error(json.message || 'API error');
            }

            return json.data || json;
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    // ===== SIMULATOR BROWSING =====
    /**
     * Get simulators with pagination
     * @param {Number} page - Page number
     * @param {Object} options - {search, filter, sort, limit}
     * @returns {Promise<Array>} Simulators
     */
    async getSimulators(page = 1, options = {}) {
        const params = new URLSearchParams({
            page,
            limit: options.limit || 20,
            ...(options.search && { search: options.search }),
            ...(options.sort && { sort: options.sort })
        });

        if (options.filter) {
            Object.entries(options.filter).forEach(([key, value]) => {
                params.append(`filter_${key}`, value);
            });
        }

        return this.request('GET', `/simulators?${params}`);
    }

    /**
     * Get single simulator
     * @param {Number} id - Simulator ID
     * @returns {Promise<Object>} Simulator data
     */
    async getSimulatorById(id) {
        return this.request('GET', `/simulators/${id}`);
    }

    /**
     * Search simulators
     * @param {String} query - Search query
     * @param {Object} options - {page, limit, sort, filter}
     * @returns {Promise<Array>} Search results
     */
    async searchSimulators(query, options = {}) {
        return this.getSimulators(options.page || 1, {
            search: query,
            ...options
        });
    }

    /**
     * Get trending simulators
     * @param {Number} limit - How many to return
     * @returns {Promise<Array>} Trending simulators
     */
    async getTrendingSimulators(limit = 10) {
        return this.request('GET', `/simulators/trending/all?limit=${limit}`);
    }

    /**
     * Get featured simulators
     * @param {Number} limit - How many to return
     * @returns {Promise<Array>} Featured simulators
     */
    async getFeaturedSimulators(limit = 10) {
        return this.request('GET', `/simulators?featured=true&limit=${limit}`);
    }

    // ===== SIMULATOR CREATION & EDITING =====
    /**
     * Create simulator
     * @param {Object} data - {title, description, blocks, connections, tags}
     * @returns {Promise<Object>} Created simulator
     */
    async createSimulator(data) {
        return this.request('POST', '/simulators', data);
    }

    /**
     * Update simulator
     * @param {Number} id - Simulator ID
     * @param {Object} data - Updated data
     * @returns {Promise<Object>} Updated simulator
     */
    async updateSimulator(id, data) {
        return this.request('PUT', `/simulators/${id}`, data);
    }

    /**
     * Delete simulator
     * @param {Number} id - Simulator ID
     * @returns {Promise} Deletion result
     */
    async deleteSimulator(id) {
        return this.request('DELETE', `/simulators/${id}`);
    }

    /**
     * Publish simulator
     * @param {Number} id - Simulator ID
     * @returns {Promise<Object>} Published simulator
     */
    async publishSimulator(id) {
        return this.request('POST', `/simulators/${id}/publish`);
    }

    /**
     * Unpublish simulator
     * @param {Number} id - Simulator ID
     * @returns {Promise<Object>} Unpublished simulator
     */
    async unpublishSimulator(id) {
        return this.request('POST', `/simulators/${id}/unpublish`);
    }

    /**
     * Get user's simulators
     * @returns {Promise<Array>} User's simulators
     */
    async getMySimulators() {
        return this.request('GET', '/my-simulators');
    }

    // ===== RATINGS & COMMENTS =====
    /**
     * Rate simulator
     * @param {Number} id - Simulator ID
     * @param {Number} rating - Rating (1-5)
     * @param {String} review - Review text
     * @returns {Promise<Object>} Rating data
     */
    async rateSimulator(id, rating, review = '') {
        return this.request('POST', `/simulators/${id}/ratings`, {
            rating,
            review
        });
    }

    /**
     * Get simulator ratings
     * @param {Number} id - Simulator ID
     * @returns {Promise<Array>} Ratings
     */
    async getSimulatorRatings(id) {
        return this.request('GET', `/simulators/${id}/ratings`);
    }

    /**
     * Comment on simulator
     * @param {Number} id - Simulator ID
     * @param {String} comment - Comment text
     * @returns {Promise<Object>} Comment data
     */
    async commentOnSimulator(id, comment) {
        return this.request('POST', `/simulators/${id}/comments`, {
            comment
        });
    }

    /**
     * Get simulator comments
     * @param {Number} id - Simulator ID
     * @returns {Promise<Array>} Comments
     */
    async getSimulatorComments(id) {
        return this.request('GET', `/simulators/${id}/comments`);
    }

    // ===== DOWNLOADS & INTERACTIONS =====
    /**
     * Download simulator
     * @param {Number} id - Simulator ID
     * @returns {Promise<Object>} Download record
     */
    async downloadSimulator(id) {
        return this.request('POST', `/simulators/${id}/download`);
    }

    /**
     * Get simulator versions
     * @param {Number} id - Simulator ID
     * @returns {Promise<Array>} Version history
     */
    async getSimulatorVersions(id) {
        return this.request('GET', `/simulators/${id}/versions`);
    }

    /**
     * Get specific simulator version
     * @param {Number} id - Simulator ID
     * @param {String} version - Version number
     * @returns {Promise<Object>} Simulator version
     */
    async getSimulatorVersion(id, version) {
        return this.request('GET', `/simulators/${id}/versions/${version}`);
    }

    // ===== FORK & REMIX =====
    /**
     * Fork simulator
     * @param {Number} id - Simulator ID
     * @param {String} newTitle - Title for fork
     * @returns {Promise<Object>} Forked simulator
     */
    async forkSimulator(id, newTitle) {
        return this.request('POST', `/simulators/${id}/fork`, {
            newTitle
        });
    }

    /**
     * Get simulator forks
     * @param {Number} id - Original simulator ID
     * @returns {Promise<Array>} Forks of simulator
     */
    async getSimulatorForks(id) {
        return this.request('GET', `/simulators/${id}/forks`);
    }

    /**
     * Get original simulator (for forked simulators)
     * @param {Number} forkedId - Forked simulator ID
     * @returns {Promise<Object>} Original simulator
     */
    async getOriginalSimulator(forkedId) {
        return this.request('GET', `/simulators/${forkedId}/original`);
    }

    // ===== USER PROFILE =====
    /**
     * Get creator profile
     * @param {Number} userId - User ID
     * @returns {Promise<Object>} Creator profile
     */
    async getCreatorProfile(userId) {
        return this.request('GET', `/users/${userId}/profile`);
    }

    /**
     * Get creator's simulators
     * @param {Number} userId - User ID
     * @returns {Promise<Array>} Creator's simulators
     */
    async getCreatorSimulators(userId) {
        return this.request('GET', `/users/${userId}/simulators`);
    }

    // ===== COURSE INTEGRATION =====
    /**
     * Add simulator to course
     * @param {Number} courseId - Course ID
     * @param {Number} simulatorId - Simulator ID
     * @returns {Promise<Object>} Course simulator usage record
     */
    async addSimulatorToCourse(courseId, simulatorId) {
        return this.request('POST', `/courses/${courseId}/simulators`, {
            simulatorId
        });
    }

    /**
     * Get course simulators
     * @param {Number} courseId - Course ID
     * @returns {Promise<Array>} Simulators in course
     */
    async getCourseSimulators(courseId) {
        return this.request('GET', `/courses/${courseId}/simulators`);
    }

    /**
     * Remove simulator from course
     * @param {Number} courseId - Course ID
     * @param {Number} blockId - Block ID in course
     * @returns {Promise} Removal result
     */
    async removeSimulatorFromCourse(courseId, blockId) {
        return this.request('DELETE', `/courses/${courseId}/simulators/${blockId}`);
    }

    // ===== CACHING UTILITIES =====
    /**
     * Get from cache
     * @param {String} key - Cache key
     * @returns {Object|null} Cached data or null
     */
    getFromCache(key) {
        const cached = this.cache.get(key);
        if (cached && Date.now() - cached.timestamp < this.cacheTimeout) {
            return cached.data;
        }
        this.cache.delete(key);
        return null;
    }

    /**
     * Save to cache
     * @param {String} key - Cache key
     * @param {Object} data - Data to cache
     */
    saveToCache(key, data) {
        this.cache.set(key, {
            data,
            timestamp: Date.now()
        });
    }

    /**
     * Clear cache
     */
    clearCache() {
        this.cache.clear();
    }

    /**
     * Clear specific cache entry
     * @param {String} key - Cache key
     */
    clearCacheEntry(key) {
        this.cache.delete(key);
    }

    /**
     * Check if authenticated
     * @returns {Boolean} Is authenticated
     */
    isAuthenticated() {
        return !!this.token;
    }

    /**
     * Logout
     */
    logout() {
        this.token = null;
        localStorage.removeItem('auth_token');
        this.clearCache();
    }
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MarketplaceAPI;
}
