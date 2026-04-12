/**
 * Veelearn Logger Utility
 * Environment-based logging with different levels
 * Debug logs only shown in development environment
 */

const LogLevel = {
    DEBUG: 'debug',
    INFO: 'info',
    WARN: 'warn',
    ERROR: 'error'
};

// Determine if we're in development environment
const isDevelopment = () => {
    return window.location.hostname === 'localhost' || 
           window.location.hostname === '127.0.0.1' ||
           window.location.port === '5500' ||
           window.location.port === '3000';
};

// Check if debug logging is enabled
const isDebugEnabled = () => {
    return isDevelopment() && localStorage.getItem('debugLogging') !== 'false';
};

/**
 * Log debug messages (only in development)
 */
const debug = (message, ...args) => {
    if (isDebugEnabled()) {
        console.log(`[DEBUG] ${message}`, ...args);
    }
};

/**
 * Log info messages
 */
const info = (message, ...args) => {
    console.log(`[INFO] ${message}`, ...args);
};

/**
 * Log warning messages
 */
const warn = (message, ...args) => {
    console.warn(`[WARN] ${message}`, ...args);
};

/**
 * Log error messages (always shown)
 */
const error = (message, ...args) => {
    console.error(`[ERROR] ${message}`, ...args);
};

/**
 * Enable/disable debug logging (for testing)
 */
const setDebugLogging = (enabled) => {
    localStorage.setItem('debugLogging', enabled.toString());
};

// Export as window.logger for global access
if (typeof window !== 'undefined') {
    window.logger = {
        debug,
        info,
        warn,
        error,
        setDebugLogging,
        isDevelopment,
        isDebugEnabled
    };
}

// For module usage
export { debug, info, warn, error, setDebugLogging, isDevelopment, isDebugEnabled, LogLevel };
