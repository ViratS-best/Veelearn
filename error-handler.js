/**
 * Veelearn Error Handler Utility
 * User-friendly error messages, actionable suggestions, error codes, report bug button
 */

class ErrorHandler {
    constructor() {
        this.errorCodes = {
            // Network errors
            NETWORK_ERROR: 'NETWORK_001',
            TIMEOUT_ERROR: 'NETWORK_002',
            SERVER_ERROR: 'SERVER_001',
            
            // Authentication errors
            UNAUTHORIZED: 'AUTH_001',
            TOKEN_EXPIRED: 'AUTH_002',
            SESSION_EXPIRED: 'AUTH_003',
            
            // Validation errors
            INVALID_INPUT: 'VALID_001',
            MISSING_FIELD: 'VALID_002',
            INVALID_EMAIL: 'VALID_003',
            
            // Course errors
            COURSE_NOT_FOUND: 'COURSE_001',
            COURSE_ACCESS_DENIED: 'COURSE_002',
            COURSE_SAVE_FAILED: 'COURSE_003',
            
            // Enrollment errors
            ENROLLMENT_FAILED: 'ENROLL_001',
            ALREADY_ENROLLED: 'ENROLL_002',
            
            // File errors
            FILE_TOO_LARGE: 'FILE_001',
            INVALID_FILE_TYPE: 'FILE_002',
            UPLOAD_FAILED: 'FILE_003'
        };
        
        this.errorMessages = {
            [this.errorCodes.NETWORK_ERROR]: {
                title: 'Network Connection Error',
                message: 'Unable to connect to the server. Please check your internet connection.',
                suggestion: 'Check your internet connection and try again. If the problem persists, the server might be temporarily unavailable.'
            },
            [this.errorCodes.TIMEOUT_ERROR]: {
                title: 'Request Timeout',
                message: 'The request took too long to complete.',
                suggestion: 'Try again. If this continues, check your internet connection or contact support.'
            },
            [this.errorCodes.SERVER_ERROR]: {
                title: 'Server Error',
                message: 'Something went wrong on our end.',
                suggestion: 'Please try again later. If the problem persists, please report this issue.'
            },
            [this.errorCodes.UNAUTHORIZED]: {
                title: 'Authentication Required',
                message: 'You need to be logged in to perform this action.',
                suggestion: 'Please log in and try again.'
            },
            [this.errorCodes.TOKEN_EXPIRED]: {
                title: 'Session Expired',
                message: 'Your session has expired. Please log in again.',
                suggestion: 'Click the login button to refresh your session.'
            },
            [this.errorCodes.INVALID_INPUT]: {
                title: 'Invalid Input',
                message: 'The information you entered is not valid.',
                suggestion: 'Please check your input and try again.'
            },
            [this.errorCodes.COURSE_NOT_FOUND]: {
                title: 'Course Not Found',
                message: 'The requested course could not be found.',
                suggestion: 'The course may have been deleted or you may not have access to it.'
            },
            [this.errorCodes.COURSE_ACCESS_DENIED]: {
                title: 'Access Denied',
                message: 'You do not have permission to access this course.',
                suggestion: 'Contact the course creator or an administrator for access.'
            },
            [this.errorCodes.ENROLLMENT_FAILED]: {
                title: 'Enrollment Failed',
                message: 'Unable to enroll in this course.',
                suggestion: 'Please try again. If the problem persists, contact support.'
            },
            [this.errorCodes.ALREADY_ENROLLED]: {
                title: 'Already Enrolled',
                message: 'You are already enrolled in this course.',
                suggestion: 'Go to your courses to continue learning.'
            },
            [this.errorCodes.FILE_TOO_LARGE]: {
                title: 'File Too Large',
                message: 'The file you are trying to upload is too large.',
                suggestion: 'Please upload a smaller file (max 10MB).'
            },
            [this.errorCodes.INVALID_FILE_TYPE]: {
                title: 'Invalid File Type',
                message: 'This file type is not supported.',
                suggestion: 'Please upload a supported file type (PNG, JPG, PDF).'
            }
        };
    }

    /**
     * Display user-friendly error message
     */
    showError(error, context = '') {
        const errorInfo = this.getErrorInfo(error, context);
        this.displayErrorModal(errorInfo);
        
        // Log to console for debugging
        if (window.logger) {
            window.logger.error('Error displayed:', errorInfo);
        }
    }

    /**
     * Get error information from error object or message
     */
    getErrorInfo(error, context = '') {
        let errorCode = this.errorCodes.SERVER_ERROR;
        let customMessage = null;

        if (typeof error === 'string') {
            customMessage = error;
        } else if (error && error.message) {
            // Try to determine error code from message
            if (error.message.includes('network') || error.message.includes('fetch')) {
                errorCode = this.errorCodes.NETWORK_ERROR;
            } else if (error.message.includes('timeout')) {
                errorCode = this.errorCodes.TIMEOUT_ERROR;
            } else if (error.message.includes('unauthorized') || error.message.includes('401')) {
                errorCode = this.errorCodes.UNAUTHORIZED;
            } else if (error.message.includes('expired') || error.message.includes('token')) {
                errorCode = this.errorCodes.TOKEN_EXPIRED;
            } else if (error.message.includes('not found') || error.message.includes('404')) {
                errorCode = this.errorCodes.COURSE_NOT_FOUND;
            } else if (error.message.includes('access denied') || error.message.includes('403')) {
                errorCode = this.errorCodes.COURSE_ACCESS_DENIED;
            }
        }

        const template = this.errorMessages[errorCode] || this.errorMessages[this.errorCodes.SERVER_ERROR];
        
        return {
            code: errorCode,
            title: template.title,
            message: customMessage || template.message,
            suggestion: template.suggestion,
            context: context,
            timestamp: new Date().toISOString()
        };
    }

    /**
     * Display error modal
     */
    displayErrorModal(errorInfo) {
        // Remove existing error modal if present
        const existingModal = document.getElementById('error-modal');
        if (existingModal) {
            existingModal.remove();
        }

        const modal = document.createElement('div');
        modal.id = 'error-modal';
        modal.className = 'error-modal';
        modal.innerHTML = `
            <div class="error-modal-content">
                <div class="error-modal-header">
                    <div class="error-icon">⚠️</div>
                    <h2 class="error-title">${this.escapeHtml(errorInfo.title)}</h2>
                    <button class="error-close-btn" onclick="document.getElementById('error-modal').remove()">&times;</button>
                </div>
                <div class="error-modal-body">
                    <p class="error-message">${this.escapeHtml(errorInfo.message)}</p>
                    <div class="error-suggestion">
                        <strong>💡 Suggestion:</strong>
                        <p>${this.escapeHtml(errorInfo.suggestion)}</p>
                    </div>
                    ${errorInfo.context ? `<div class="error-context"><small>Context: ${this.escapeHtml(errorInfo.context)}</small></div>` : ''}
                    <div class="error-code">Error Code: ${errorInfo.code}</div>
                </div>
                <div class="error-modal-footer">
                    <button class="error-btn error-btn-primary" onclick="document.getElementById('error-modal').remove()">OK</button>
                    <button class="error-btn error-btn-secondary" onclick="window.errorHandler.reportError('${errorInfo.code}', '${this.escapeHtml(errorInfo.message)}')">Report Bug</button>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
    }

    /**
     * Report error (opens email or issue tracker)
     */
    reportError(code, message) {
        const subject = `Bug Report: ${code}`;
        const body = `
Error Code: ${code}
Message: ${message}
Timestamp: ${new Date().toISOString()}
URL: ${window.location.href}
User Agent: ${navigator.userAgent}

Please describe what you were doing when this error occurred:
`;

        const mailtoLink = `mailto:support@veelearn.org?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
        window.location.href = mailtoLink;
    }

    /**
     * Escape HTML to prevent XSS
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Handle fetch errors with user-friendly messages
     */
    async handleFetchError(error, context = '') {
        if (error.name === 'AbortError') {
            // Request was cancelled, don't show error
            return;
        }

        if (!navigator.onLine) {
            this.showError(this.errorCodes.NETWORK_ERROR, context);
            return;
        }

        this.showError(error, context);
    }
}

// Initialize global error handler
window.errorHandler = new ErrorHandler();

// Global error listener
window.addEventListener('error', (event) => {
    if (window.errorHandler) {
        window.errorHandler.showError(event.error, 'Unexpected error occurred');
    }
});

// Unhandled promise rejection listener
window.addEventListener('unhandledrejection', (event) => {
    if (window.errorHandler) {
        window.errorHandler.showError(event.reason, 'Async operation failed');
    }
});
