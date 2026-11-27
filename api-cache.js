/**
 * Veelearn API Response Caching Utility
 * Cache course lists, simulator data, user profiles, cache invalidation
 */

class ApiCache {
    constructor() {
        this.cache = new Map();
        this.defaultTTL = 5 * 60 * 1000; // 5 minutes
        this.storagePrefix = 'veelearn_cache_';
        this.init();
    }

    init() {
        this.loadCacheFromStorage();
        this.setupCacheInvalidation();
        console.log('API cache initialized');
    }

    loadCacheFromStorage() {
        try {
            const keys = Object.keys(localStorage);
            keys.forEach(key => {
                if (key.startsWith(this.storagePrefix)) {
                    const data = JSON.parse(localStorage.getItem(key));
                    if (data && data.expires > Date.now()) {
                        this.cache.set(key.replace(this.storagePrefix, ''), data);
                    } else {
                        localStorage.removeItem(key);
                    }
                }
            });
        } catch (error) {
            console.error('Error loading cache from storage:', error);
        }
    }

    set(key, value, ttl = this.defaultTTL) {
        const cacheEntry = {
            value: value,
            timestamp: Date.now(),
            expires: Date.now() + ttl
        };
        
        this.cache.set(key, cacheEntry);
        this.saveToStorage(key, cacheEntry);
    }

    get(key) {
        const entry = this.cache.get(key);
        
        if (!entry) return null;
        
        if (Date.now() > entry.expires) {
            this.delete(key);
            return null;
        }
        
        return entry.value;
    }

    delete(key) {
        this.cache.delete(key);
        localStorage.removeItem(this.storagePrefix + key);
    }

    clear() {
        this.cache.clear();
        this.clearStorage();
    }

    saveToStorage(key, entry) {
        try {
            localStorage.setItem(this.storagePrefix + key, JSON.stringify(entry));
        } catch (error) {
            console.error('Error saving to storage:', error);
            // If storage is full, clear old entries
            if (error.name === 'QuotaExceededError') {
                this.clearOldEntries();
            }
        }
    }

    clearStorage() {
        try {
            const keys = Object.keys(localStorage);
            keys.forEach(key => {
                if (key.startsWith(this.storagePrefix)) {
                    localStorage.removeItem(key);
                }
            });
        } catch (error) {
            console.error('Error clearing storage:', error);
        }
    }

    clearOldEntries() {
        const now = Date.now();
        this.cache.forEach((entry, key) => {
            if (entry.expires < now) {
                this.delete(key);
            }
        });
    }

    setupCacheInvalidation() {
        // Invalidate cache when user logs out
        window.addEventListener('user-logout', () => {
            this.clear();
        });

        // Invalidate cache periodically
        setInterval(() => {
            this.clearOldEntries();
        }, 60000); // Every minute
    }

    async fetchWithCache(url, options = {}, ttl = this.defaultTTL) {
        const cacheKey = this.generateCacheKey(url, options);
        const cached = this.get(cacheKey);
        
        if (cached) {
            if (window.logger) {
                window.logger.debug('Cache hit:', cacheKey);
            }
            return cached;
        }
        
        if (window.logger) {
            window.logger.debug('Cache miss:', cacheKey);
        }
        
        try {
            const response = await fetch(url, options);
            const data = await response.json();
            
            if (data.success) {
                this.set(cacheKey, data, ttl);
            }
            
            return data;
        } catch (error) {
            console.error('Fetch error:', error);
            throw error;
        }
    }

    generateCacheKey(url, options) {
        const method = options.method || 'GET';
        const body = options.body ? JSON.stringify(options.body) : '';
        return `${method}:${url}:${body}`;
    }

    invalidatePattern(pattern) {
        const regex = new RegExp(pattern);
        this.cache.forEach((entry, key) => {
            if (regex.test(key)) {
                this.delete(key);
            }
        });
    }

    getCacheSize() {
        return this.cache.size;
    }

    getCacheStats() {
        const now = Date.now();
        let total = 0;
        let expired = 0;
        
        this.cache.forEach((entry) => {
            total++;
            if (entry.expires < now) {
                expired++;
            }
        });
        
        return {
            total,
            expired,
            valid: total - expired
        };
    }
}

// Initialize global API cache
window.apiCache = new ApiCache();

// Cached fetch wrapper
window.cachedFetch = (url, options = {}, ttl) => {
    return window.apiCache.fetchWithCache(url, options, ttl);
};

console.log('API cache utility loaded');
