/**
 * Veelearn Input Validation Utility
 * Client-side validation, sanitization, and schema validation
 */

class Validator {
    constructor() {
        this.rules = {
            email: {
                pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
                message: 'Please enter a valid email address'
            },
            password: {
                minLength: 8,
                pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/,
                message: 'Password must be at least 8 characters with uppercase, lowercase, and number'
            },
            title: {
                minLength: 1,
                maxLength: 255,
                message: 'Title must be between 1 and 255 characters'
            },
            description: {
                maxLength: 5000,
                message: 'Description must be less than 5000 characters'
            },
            courseContent: {
                maxLength: 100000,
                message: 'Content must be less than 100,000 characters'
            },
            gradeLevel: {
                pattern: /^(?:[1-9]|1[0-3])$/,
                message: 'Grade level must be between 1 and 13 (13 = College)'
            }
        };
    }

    /**
     * Validate email
     */
    validateEmail(email) {
        if (!email || typeof email !== 'string') {
            return { valid: false, message: 'Email is required' };
        }
        if (!this.rules.email.pattern.test(email.trim())) {
            return { valid: false, message: this.rules.email.message };
        }
        return { valid: true };
    }

    /**
     * Validate password
     */
    validatePassword(password) {
        if (!password || typeof password !== 'string') {
            return { valid: false, message: 'Password is required' };
        }
        if (password.length < this.rules.password.minLength) {
            return { valid: false, message: `Password must be at least ${this.rules.password.minLength} characters` };
        }
        if (!this.rules.password.pattern.test(password)) {
            return { valid: false, message: this.rules.password.message };
        }
        return { valid: true };
    }

    /**
     * Validate course title
     */
    validateTitle(title) {
        if (!title || typeof title !== 'string') {
            return { valid: false, message: 'Title is required' };
        }
        if (title.trim().length < this.rules.title.minLength) {
            return { valid: false, message: 'Title cannot be empty' };
        }
        if (title.length > this.rules.title.maxLength) {
            return { valid: false, message: this.rules.title.message };
        }
        return { valid: true };
    }

    /**
     * Validate description
     */
    validateDescription(description) {
        if (description && description.length > this.rules.description.maxLength) {
            return { valid: false, message: this.rules.description.message };
        }
        return { valid: true };
    }

    /**
     * Validate course content
     */
    validateCourseContent(content) {
        if (content && content.length > this.rules.courseContent.maxLength) {
            return { valid: false, message: this.rules.courseContent.message };
        }
        return { valid: true };
    }

    /**
     * Validate grade level
     */
    validateGradeLevel(gradeLevel) {
        if (gradeLevel !== undefined && gradeLevel !== null && gradeLevel !== '') {
            if (!this.rules.gradeLevel.pattern.test(gradeLevel.toString())) {
                return { valid: false, message: this.rules.gradeLevel.message };
            }
        }
        return { valid: true };
    }

    /**
     * Sanitize string input
     */
    sanitize(input) {
        if (typeof input !== 'string') {
            return input;
        }
        
        // Remove potentially dangerous characters
        return input
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#x27;')
            .replace(/\//g, '&#x2F;');
    }

    /**
     * Validate course form data
     */
    validateCourseForm(data) {
        const errors = {};

        if (data.title !== undefined) {
            const titleValidation = this.validateTitle(data.title);
            if (!titleValidation.valid) {
                errors.title = titleValidation.message;
            }
        }

        if (data.description !== undefined) {
            const descValidation = this.validateDescription(data.description);
            if (!descValidation.valid) {
                errors.description = descValidation.message;
            }
        }

        if (data.content !== undefined) {
            const contentValidation = this.validateCourseContent(data.content);
            if (!contentValidation.valid) {
                errors.content = contentValidation.message;
            }
        }

        if (data.grade_level !== undefined) {
            const gradeValidation = this.validateGradeLevel(data.grade_level);
            if (!gradeValidation.valid) {
                errors.grade_level = gradeValidation.message;
            }
        }

        return {
            valid: Object.keys(errors).length === 0,
            errors
        };
    }

    /**
     * Validate registration form
     */
    validateRegistration(data) {
        const errors = {};

        if (data.email !== undefined) {
            const emailValidation = this.validateEmail(data.email);
            if (!emailValidation.valid) {
                errors.email = emailValidation.message;
            }
        }

        if (data.password !== undefined) {
            const passwordValidation = this.validatePassword(data.password);
            if (!passwordValidation.valid) {
                errors.password = passwordValidation.message;
            }
        }

        return {
            valid: Object.keys(errors).length === 0,
            errors
        };
    }

    /**
     * Display validation errors
     */
    displayErrors(errors, container) {
        if (!container) return;

        container.innerHTML = Object.entries(errors)
            .map(([field, message]) => `
                <div class="validation-error" data-field="${field}">
                    <span class="error-icon">⚠️</span>
                    <span class="error-message">${this.escapeHtml(message)}</span>
                </div>
            `)
            .join('');
    }

    /**
     * Clear validation errors
     */
    clearErrors(container) {
        if (!container) return;
        container.innerHTML = '';
    }

    /**
     * Escape HTML to prevent XSS
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize global validator
window.validator = new Validator();

console.log('Validation utility loaded');
