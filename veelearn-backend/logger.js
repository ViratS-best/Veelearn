/**
 * Veelearn Backend Logger Utility
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
    return process.env.NODE_ENV === 'development' || 
           process.env.NODE_ENV === undefined ||
           process.env.NODE_ENV === 'test';
};

// Check if debug logging is enabled
const isDebugEnabled = () => {
    return isDevelopment() && process.env.DEBUG_LOGGING !== 'false';
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
    process.env.DEBUG_LOGGING = enabled.toString();
};

module.exports = {
    debug,
    info,
    warn,
    error,
    setDebugLogging,
    isDevelopment,
    isDebugEnabled,
    LogLevel
};
