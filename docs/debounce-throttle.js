/**
 * Veelearn Debounce & Throttle Utility
 * Debounce search (300ms), auto-save (1s), scroll events (100ms), rate limit API
 */

/**
 * Debounce function - delays execution until after wait time has elapsed
 * since the last time the debounced function was invoked
 */
function debounce(func, wait = 300, immediate = false) {
    let timeout;
    
    return function executedFunction(...args) {
        const context = this;
        
        const later = () => {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        
        const callNow = immediate && !timeout;
        
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        
        if (callNow) func.apply(context, args);
    };
}

/**
 * Throttle function - ensures function is called at most once in wait period
 */
function throttle(func, wait = 100) {
    let inThrottle;
    let lastFunc;
    let lastRan;
    
    return function executedFunction(...args) {
        const context = this;
        
        if (!inThrottle) {
            func.apply(context, args);
            lastRan = Date.now();
            inThrottle = true;
        } else {
            clearTimeout(lastFunc);
            lastFunc = setTimeout(() => {
                if ((Date.now() - lastRan) >= wait) {
                    func.apply(context, args);
                    lastRan = Date.now();
                }
            }, wait - (Date.now() - lastRan));
        }
    };
}

/**
 * Rate limit API calls - ensures API is called at most once in wait period
 */
function rateLimit(func, wait = 1000) {
    let lastCall = 0;
    let timeout;
    
    return function executedFunction(...args) {
        const context = this;
        const now = Date.now();
        const timeSinceLastCall = now - lastCall;
        
        if (timeSinceLastCall >= wait) {
            lastCall = now;
            return func.apply(context, args);
        } else {
            clearTimeout(timeout);
            return new Promise((resolve) => {
                timeout = setTimeout(() => {
                    lastCall = Date.now();
                    resolve(func.apply(context, args));
                }, wait - timeSinceLastCall);
            });
        }
    };
}

/**
 * Debounced search input handler
 */
const debouncedSearch = debounce((query, callback) => {
    callback(query);
}, 300);

/**
 * Throttled scroll handler
 */
const throttledScroll = throttle((callback) => {
    callback();
}, 100);

/**
 * Debounced auto-save
 */
const debouncedAutoSave = debounce((saveFunction) => {
    saveFunction();
}, 1000);

/**
 * Rate-limited API call
 */
const rateLimitedApiCall = rateLimit((apiCall) => {
    return apiCall();
}, 500);

// Export to window for global access
window.debounce = debounce;
window.throttle = throttle;
window.rateLimit = rateLimit;
window.debouncedSearch = debouncedSearch;
window.throttledScroll = throttledScroll;
window.debouncedAutoSave = debouncedAutoSave;
window.rateLimitedApiCall = rateLimitedApiCall;

// Utility to apply debounce to existing functions
window.applyDebounce = (obj, funcName, wait = 300) => {
    if (obj[funcName] && typeof obj[funcName] === 'function') {
        const originalFunc = obj[funcName];
        obj[funcName] = debounce(originalFunc, wait);
        return true;
    }
    return false;
};

// Utility to apply throttle to existing functions
window.applyThrottle = (obj, funcName, wait = 100) => {
    if (obj[funcName] && typeof obj[funcName] === 'function') {
        const originalFunc = obj[funcName];
        obj[funcName] = throttle(originalFunc, wait);
        return true;
    }
    return false;
};

// Utility to apply rate limit to existing functions
window.applyRateLimit = (obj, funcName, wait = 1000) => {
    if (obj[funcName] && typeof obj[funcName] === 'function') {
        const originalFunc = obj[funcName];
        obj[funcName] = rateLimit(originalFunc, wait);
        return true;
    }
    return false;
};

console.log('Debounce & Throttle utilities loaded');
