const express = require('express');
const WebSocket = require('ws');
const mysql = require('mysql2');
const dotenv = require('dotenv');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const cookieParser = require('cookie-parser');
const cors = require('cors');
const helmet = require('helmet');
const xss = require('xss');
const rateLimit = require('express-rate-limit');
const path = require('path');
const nodemailer = require('nodemailer');

const util = require('util');
const PDFDocument = require('pdfkit');
const fs = require('fs');
const axios = require('axios');
const { openRouterChatCompletion, getOpenRouterKeys } = require('./openrouter');
const { debug, info, warn, error } = require('./logger');
// path is already required above

dotenv.config({ path: path.resolve(__dirname, '.env') });

// ===== EMAIL CONFIGURATION =====
// Primary: Brevo HTTP API (works on Render/Railway where SMTP ports are blocked, no domain needed)
// Fallback: Gmail SMTP (works locally or on hosts that allow outbound SMTP)

const smtpTransporter = nodemailer.createTransport({
    host: 'smtp.gmail.com',
    port: 465,
    secure: true,
    auth: {
        user: process.env.SMTP_EMAIL,
        pass: process.env.SMTP_PASSWORD
    },
    connectionTimeout: 10000,
    greetingTimeout: 10000,
    socketTimeout: 15000
});

let smtpReady = false;
const brevoApiKey = process.env.BREVO_API_KEY;

if (brevoApiKey) {
    info('✓ Brevo API key configured - using HTTP-based email delivery');
} else {
    info('ℹ️ No BREVO_API_KEY set, trying Gmail SMTP...');
}

if (process.env.SMTP_EMAIL && process.env.SMTP_PASSWORD) {
    smtpTransporter.verify()
        .then(() => { smtpReady = true; info('✓ SMTP email service ready (fallback)'); })
        .catch(err => warn('⚠️ SMTP unavailable:', err.message, '(port likely blocked)'));
} else if (!brevoApiKey) {
    warn('⚠️ No email provider configured. Set BREVO_API_KEY or SMTP_EMAIL+SMTP_PASSWORD.');
}

async function sendEmail({ to, subject, html }) {
    const senderEmail = process.env.SMTP_EMAIL || 'viratsuper@veelearn.org';
    const senderName = 'Veelearn';

    if (brevoApiKey) {
        const response = await axios.post('https://api.brevo.com/v3/smtp/email', {
            sender: { name: senderName, email: senderEmail },
            to: [{ email: to }],
            subject,
            htmlContent: html
        }, {
            headers: {
                'api-key': brevoApiKey,
                'Content-Type': 'application/json'
            },
            validateStatus: () => true
        });
        if (response.status >= 400) {
            const detail = JSON.stringify(response.data).slice(0, 300);
            throw new Error(`Brevo HTTP ${response.status}: ${detail}`);
        }
        return;
    }

    if (smtpReady) {
        await smtpTransporter.sendMail({
            from: `"${senderName}" <${senderEmail}>`,
            to,
            subject,
            html
        });
        return;
    }

    throw new Error('No email provider available. Configure BREVO_API_KEY or fix SMTP settings.');
}

const app = express();
app.set('trust proxy', 1); // Trust first proxy (Render/Nginx) for rate limiting


// Check for critical environment variables
if (!process.env.JWT_SECRET) {
    console.error('❌ FATAL ERROR: JWT_SECRET is not defined.');
    console.error('   Please add JWT_SECRET to your environment variables.');
    process.exit(1);
}

// ===== RATE LIMITING MIDDLEWARE =====

// General rate limiter for all endpoints
const generalLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 1000, // Limit each IP to 1000 requests per windowMs
    message: { success: false, message: 'Too many requests from this IP, please try again later.' },
    standardHeaders: true, // Return rate limit info in the `RateLimit-*` headers
    legacyHeaders: false,
});

// Strict rate limiter for authentication endpoints
const authLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 5, // Limit each IP to 5 requests per windowMs
    message: { success: false, message: 'Too many authentication attempts, please try again later.' },
    standardHeaders: true,
    legacyHeaders: false,
});

// Rate limiter for API endpoints that modify data
const writeLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // Limit each IP to 100 write requests per windowMs
    message: { success: false, message: 'Too many write requests, please try again later.' },
    standardHeaders: true,
    legacyHeaders: false,
});

// Rate limiter for search endpoints
const searchLimiter = rateLimit({
    windowMs: 1 * 60 * 1000, // 1 minute
    max: 30, // Limit each IP to 30 search requests per minute
    message: { success: false, message: 'Too many search requests, please try again later.' },
    standardHeaders: true,
    legacyHeaders: false,
});

// Apply general rate limiting to all routes
app.use(generalLimiter);

// ===== SECURITY HEADERS MIDDLEWARE =====
app.use(helmet({
    contentSecurityPolicy: {
        directives: {
            defaultSrc: ["'self'"],
            scriptSrc: ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net", "https://cdnjs.cloudflare.com"],
            styleSrc: ["'self'", "'unsafe-inline'"],
            imgSrc: ["'self'", "data:", "https:"],
            fontSrc: ["'self'", "data:"],
            connectSrc: ["'self'", "https://api.veelearn.org", "https://api.github.com", "https://api.brevo.com"]
        }
    },
    crossOriginEmbedderPolicy: false
}));

// XSS Mitigation Middleware
app.use((req, res, next) => {
    if (req.body) {
        for (let key in req.body) {
            if (typeof req.body[key] === 'string') {
                req.body[key] = xss(req.body[key]);
            }
        }
    }
    if (req.query) {
        for (let key in req.query) {
            if (typeof req.query[key] === 'string') {
                req.query[key] = xss(req.query[key]);
            }
        }
    }
    if (req.params) {
        for (let key in req.params) {
            if (typeof req.params[key] === 'string') {
                req.params[key] = xss(req.params[key]);
            }
        }
    }
    next();
});

app.use(cors({
    origin: [
        'https://veelearn.org',
        'https://www.veelearn.org',
        'http://localhost:5500',
        'http://127.0.0.1:5500',
        'http://localhost:5000',
        'http://127.0.0.1:5000',
        'https://virat-sisodiya.github.io',
        /\.github\.io$/
    ],
    credentials: true,
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization', 'Cookie', 'Cache-Control', 'Pragma']
}));
app.use(express.json({ limit: '50mb' }));
app.use(cookieParser());

// ===== DATABASE CONFIGURATION =====
const dbConfig = {
    host: process.env.DB_HOST || process.env.MYSQLHOST || 'localhost',
    port: process.env.DB_PORT || process.env.MYSQLPORT || 3306,
    user: process.env.DB_USER || process.env.MYSQLUSER || 'root',
    password: process.env.DB_PASSWORD || process.env.MYSQLPASSWORD || '',
    database: process.env.DB_NAME || process.env.MYSQL_DATABASE || process.env.MYSQLDATABASE || 'veelearn_db',
    ssl: process.env.DB_SSL_CA ? {
        ca: process.env.DB_SSL_CA.replace(/\\n/g, '\n'),
        rejectUnauthorized: true
    } : (process.env.MYSQLHOST ? { rejectUnauthorized: false } : null)
};

// Create a pool
const db = mysql.createPool({
    ...dbConfig,
    connectionLimit: 10,
    waitForConnections: true,
    queueLimit: 0,
    // DATE/DATETIME as 'YYYY-MM-DD...' strings (fixes daily check-in same-day compare)
    dateStrings: true
});

// Promisify for async/await
const query = util.promisify(db.query).bind(db);

// Database health check
setInterval(async () => {
    try {
        await query('SELECT 1');
    } catch (err) {
        console.error('Database connection error:', err);
    }
}, 60000);

// Initialize database and tables sequentially
const initializeDatabase = async () => {
    try {
        info(`📡 Attempting to connect to database at ${dbConfig.host}:${dbConfig.port}`);
        // 1. Ensure database exists
        const connection = mysql.createConnection({
            host: dbConfig.host,
            port: dbConfig.port,
            user: dbConfig.user,
            password: dbConfig.password
        });
        const connectionQuery = util.promisify(connection.query).bind(connection);

        await connectionQuery(`CREATE DATABASE IF NOT EXISTS ${dbConfig.database}`);
        connection.end();
        info(`Database '${dbConfig.database}' verified/created`);

        // 2. Create tables in proper order
        info('Initializing tables...');

        // Users table (Parent)
        await query(`
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                role ENUM('superadmin', 'admin', 'school_admin', 'teacher', 'student', 'parent', 'user') DEFAULT 'user',
                is_admin_approved BOOLEAN DEFAULT FALSE,
                shells INT DEFAULT 0,
                name VARCHAR(255),
                school_code VARCHAR(20) NULL,
                school_id INT NULL,
                parent_code VARCHAR(20) UNIQUE NULL,
                is_approved BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_email (email),
                INDEX idx_role (role),
                INDEX idx_school_code (school_code),
                INDEX idx_parent_code (parent_code)
            )
        `);
        info('✓ Users table ready');

        // Courses table (Parent)
        await query(`
            CREATE TABLE IF NOT EXISTS courses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                content LONGTEXT,
                blocks LONGTEXT,
                creator_id INT,
                status ENUM('pending', 'approved', 'rejected', 'draft') DEFAULT 'pending',
                is_paid BOOLEAN DEFAULT FALSE,
                shells_cost INT DEFAULT 50,
                feedback TEXT,
                grade_level INT CHECK (grade_level >= 1 AND grade_level <= 13),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (creator_id) REFERENCES users(id) ON DELETE CASCADE,
                INDEX idx_status (status),
                INDEX idx_creator (creator_id),
                INDEX idx_grade_level (grade_level)
            )
        `);
        info('✓ Courses table ready');

        // Helper to safely add column
        const addColumn = (table, column, definition) => {
            return new Promise((resolve) => {
                const checkQuery = `
            SELECT COUNT(*) as count 
            FROM information_schema.columns 
            WHERE table_schema = DATABASE() 
            AND table_name = ? 
            AND column_name = ?
        `;

                db.query(checkQuery, [table, column], (err, results) => {
                    if (err) {
                        console.error(`Error checking column ${column}:`, err);
                        return resolve();
                    }

                    if (results[0].count === 0) {
                        const alterQuery = `ALTER TABLE ${table} ADD COLUMN ${column} ${definition}`;
                        db.query(alterQuery, (alterErr) => {
                            if (alterErr) {
                                console.error(`Error adding column ${column}:`, alterErr);
                            } else {
                                info(`✓ Added column ${column} to ${table}`);
                            }
                            resolve();
                        });
                    } else {
                        resolve();
                    }
                });
            });
        };
        // Migration: Add blocks column if it doesn't exist
        await addColumn('courses', 'blocks', 'LONGTEXT');

        // Migration: Add creation_time column if it doesn't exist
        await addColumn('courses', 'creation_time', 'INT DEFAULT 0');

        // Migration: Add like_count column to courses
        await addColumn('courses', 'like_count', 'INT DEFAULT 0');

        // Migration: Add grade_level column if it doesn't exist
        await addColumn('courses', 'grade_level', 'INT CHECK (grade_level >= 1 AND grade_level <= 13)');

        // Migration: Add video_url column if it doesn't exist
        await addColumn('courses', 'video_url', 'VARCHAR(255)');

        // Migration: Add volunteer columns to users table
        await addColumn('users', 'total_volunteer_hours', 'FLOAT DEFAULT 0');
        await addColumn('users', 'is_verified_creator', 'BOOLEAN DEFAULT FALSE');

        // Migration: Add teacher-specific columns
        await addColumn('users', 'class_code', 'VARCHAR(20) UNIQUE');
        await addColumn('users', 'teacher_approved', 'BOOLEAN DEFAULT FALSE');
        info('✓ Teacher columns verified/added to users table');

        // ===== EDUCATIONAL MANAGEMENT SYSTEM (EMS) MIGRATIONS =====

        // Migration: Update users role ENUM to include new EMS roles
        // Note: MySQL doesn't support ALTER TABLE for ENUM modifications directly
        // We'll modify the CREATE TABLE statement above to include new roles
        // For existing databases, we'll use a manual ALTER TABLE approach
        try {
            await query(`ALTER TABLE users MODIFY COLUMN role ENUM('superadmin', 'admin', 'school_admin', 'teacher', 'student', 'parent', 'user') DEFAULT 'user'`);
            info('✓ Users role ENUM updated for EMS roles');
        } catch (e) {
            // Likely already updated or table doesn't exist yet
            info('ℹ️ Role ENUM update skipped (may already exist)');
        }

        // Migration: Add EMS-related columns to users table
        await addColumn('users', 'name', 'VARCHAR(255)');
        await addColumn('users', 'school_code', 'VARCHAR(20) NULL');
        await addColumn('users', 'school_id', 'INT NULL');
        await addColumn('users', 'parent_code', 'VARCHAR(20) UNIQUE NULL');
        await addColumn('users', 'is_approved', 'BOOLEAN DEFAULT FALSE');
        info('✓ EMS columns verified/added to users table');

        // ===== LEARNER SHELL GAMIFICATION =====
        await addColumn('users', 'display_name', 'VARCHAR(80) NULL');
        await addColumn('users', 'gems', 'INT DEFAULT 0');
        await addColumn('users', 'current_streak', 'INT DEFAULT 0');
        await addColumn('users', 'longest_streak', 'INT DEFAULT 0');
        await addColumn('users', 'last_active_date', 'DATE NULL');
        await addColumn('users', 'avatar_config', 'JSON NULL');
        await addColumn('users', 'dashboard_theme', "VARCHAR(40) DEFAULT 'warm'");
        info('✓ Learner gamification columns verified/added to users table');

        await query(`
            CREATE TABLE IF NOT EXISTS store_items (
                item_id VARCHAR(64) PRIMARY KEY,
                item_type VARCHAR(32) NOT NULL,
                name VARCHAR(120) NOT NULL,
                description VARCHAR(255),
                gem_cost INT DEFAULT 0,
                asset_key VARCHAR(64) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        `);
        await query(`
            CREATE TABLE IF NOT EXISTS user_inventory (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                item_id VARCHAR(64) NOT NULL,
                acquired_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE KEY uniq_user_item (user_id, item_id),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                INDEX idx_inventory_user (user_id)
            )
        `);
        await query(`
            CREATE TABLE IF NOT EXISTS user_feedback (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                message TEXT NOT NULL,
                emailed TINYINT(1) DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                INDEX idx_feedback_created (created_at)
            )
        `);
        info('✓ Learner store/inventory/feedback tables ready');

        // ===== COURSE NESTING SYSTEM MIGRATIONS =====
        
        // Migration: Add course_type column to courses table
        await addColumn('courses', 'course_type', "ENUM('single', 'master') DEFAULT 'single'");
        info('✓ Course type column verified/added');

        // Migration: Add is_master_enrollment column to enrollments table
        await addColumn('enrollments', 'is_master_enrollment', 'BOOLEAN DEFAULT FALSE');
        info('✓ Master enrollment column verified/added');

        // Course Units table - manages parent-child course relationships
        await query(`
            CREATE TABLE IF NOT EXISTS course_units (
                id INT AUTO_INCREMENT PRIMARY KEY,
                parent_course_id INT NOT NULL,
                child_course_id INT NOT NULL,
                order_index INT NOT NULL DEFAULT 0,
                is_draft BOOLEAN DEFAULT FALSE,
                prerequisite_unit_id INT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (parent_course_id) REFERENCES courses(id) ON DELETE CASCADE,
                FOREIGN KEY (child_course_id) REFERENCES courses(id) ON DELETE CASCADE,
                FOREIGN KEY (prerequisite_unit_id) REFERENCES course_units(id) ON DELETE SET NULL,
                UNIQUE KEY unique_parent_child (parent_course_id, child_course_id),
                INDEX idx_parent (parent_course_id),
                INDEX idx_child (child_course_id),
                INDEX idx_order (order_index)
            )
        `);
        info('✓ Course units table ready');

        // Course Enrollment Progress table - per-unit progress tracking
        await query(`
            CREATE TABLE IF NOT EXISTS course_enrollment_progress (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                course_id INT NOT NULL,
                unit_id INT NOT NULL,
                completed BOOLEAN DEFAULT FALSE,
                completed_at TIMESTAMP NULL,
                progress_percentage DECIMAL(5,2) DEFAULT 0,
                last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
                FOREIGN KEY (unit_id) REFERENCES course_units(id) ON DELETE CASCADE,
                UNIQUE KEY unique_user_unit (user_id, unit_id),
                INDEX idx_user_course (user_id, course_id)
            )
        `);
        info('✓ Course enrollment progress table ready');

        // Migration: Add linked_course_id to course_units for standalone progress sync
        await addColumn('course_units', 'linked_course_id', 'INT');
        info('✓ Course units linked_course_id column verified/added');

        // Classroom assignments table
        await query(`
            CREATE TABLE IF NOT EXISTS classroom_assignments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                teacher_id INT NOT NULL,
                course_id INT NOT NULL,
                class_code VARCHAR(20) NOT NULL,
                title VARCHAR(255) NOT NULL,
                due_date DATETIME,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (teacher_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
                INDEX idx_teacher (teacher_id),
                INDEX idx_class_code (class_code)
            )
        `);
        info('✓ Classroom assignments table ready');

        // Student enrollments in classes
        await query(`
            CREATE TABLE IF NOT EXISTS student_enrollments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT NOT NULL,
                class_code VARCHAR(20) NOT NULL,
                teacher_id INT NOT NULL,
                enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (teacher_id) REFERENCES users(id) ON DELETE CASCADE,
                UNIQUE KEY unique_enrollment (student_id, class_code),
                INDEX idx_student (student_id),
                INDEX idx_class_code (class_code)
            )
        `);
        info('✓ Student enrollments table ready');

        // Assignment submissions
        await query(`
            CREATE TABLE IF NOT EXISTS assignment_submissions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                assignment_id INT NOT NULL,
                student_id INT NOT NULL,
                submission_date DATETIME,
                completion_percentage INT DEFAULT 0,
                is_submitted BOOLEAN DEFAULT FALSE,
                is_late BOOLEAN DEFAULT FALSE,
                feedback TEXT,
                correct_answers INT DEFAULT 0,
                total_questions INT DEFAULT 0,
                quiz_accuracy DECIMAL(5,2) DEFAULT 0,
                current_status VARCHAR(255) DEFAULT 'Not Started',
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (assignment_id) REFERENCES classroom_assignments(id) ON DELETE CASCADE,
                FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
                UNIQUE KEY unique_submission (assignment_id, student_id),
                INDEX idx_student (student_id)
            )
        `);

        // Migration: Add columns to assignment_submissions if they don't exist
        await addColumn('assignment_submissions', 'correct_answers', 'INT DEFAULT 0');
        await addColumn('assignment_submissions', 'total_questions', 'INT DEFAULT 0');
        await addColumn('assignment_submissions', 'quiz_accuracy', 'DECIMAL(5,2) DEFAULT 0');
        await addColumn('assignment_submissions', 'current_status', "VARCHAR(255) DEFAULT 'Not Started'");
        info('✓ Assignment submission columns verified');
        // Migration: Add unique constraint to quiz attempts if not already present
        // Note: Generic try/catch because MySQL 8.0 doesn't support IF NOT EXISTS for ADD UNIQUE
        try {
            await query(`ALTER TABLE user_quiz_attempts ADD UNIQUE KEY unique_attempt (user_id, question_id)`);
            info('✓ Unique constraint added to user_quiz_attempts');
        } catch (e) {
            // Likely already exists
        }

        // ===== EDUCATIONAL MANAGEMENT SYSTEM (EMS) TABLES =====

        // Schools table
        await query(`
            CREATE TABLE IF NOT EXISTS schools (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                school_code VARCHAR(20) UNIQUE NULL,
                school_admin_id INT,
                is_approved BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (school_admin_id) REFERENCES users(id) ON DELETE SET NULL,
                INDEX idx_school_code (school_code),
                INDEX idx_school_admin (school_admin_id)
            )
        `);
        info('✓ Schools table ready');

        // Migration: Allow NULL for school_code (for existing tables)
        try {
            await query(`ALTER TABLE schools MODIFY COLUMN school_code VARCHAR(20) UNIQUE NULL`);
            info('✓ Schools table migrated: school_code now allows NULL');
        } catch (err) {
            // Migration may have already been applied, ignore error
            if (err.code !== 'ER_DUP_ENTRY' && err.code !== 'ER_KEY_COLUMN_DOES_NOT_EXIST') {
                warn('School table migration skipped (may already exist)');
            }
        }

        // Classes table
        await query(`
            CREATE TABLE IF NOT EXISTS classes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                school_id INT NOT NULL,
                name VARCHAR(255) NOT NULL,
                teacher_id INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE,
                FOREIGN KEY (teacher_id) REFERENCES users(id) ON DELETE SET NULL,
                INDEX idx_school (school_id),
                INDEX idx_teacher (teacher_id)
            )
        `);
        info('✓ Classes table ready');

        // Class enrollments table
        await query(`
            CREATE TABLE IF NOT EXISTS class_enrollments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                class_id INT NOT NULL,
                student_id INT NOT NULL,
                enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE,
                FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
                UNIQUE KEY unique_enrollment (class_id, student_id),
                INDEX idx_class (class_id),
                INDEX idx_student (student_id)
            )
        `);
        info('✓ Class enrollments table ready');

        // Parent-student links table
        await query(`
            CREATE TABLE IF NOT EXISTS parent_student_links (
                id INT AUTO_INCREMENT PRIMARY KEY,
                parent_id INT NOT NULL,
                student_id INT NOT NULL,
                linked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (parent_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
                UNIQUE KEY unique_link (parent_id, student_id),
                INDEX idx_parent (parent_id),
                INDEX idx_student (student_id)
            )
        `);
        info('✓ Parent-student links table ready');

        // Messages table
        await query(`
            CREATE TABLE IF NOT EXISTS messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                sender_id INT NOT NULL,
                recipient_id INT NOT NULL,
                class_id INT NULL,
                content TEXT NOT NULL,
                is_read BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (recipient_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE,
                INDEX idx_sender (sender_id),
                INDEX idx_recipient (recipient_id),
                INDEX idx_class (class_id),
                INDEX idx_created (created_at)
            )
        `);
        info('✓ Messages table ready');

        // Posts table
        await query(`
            CREATE TABLE IF NOT EXISTS posts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                author_id INT NOT NULL,
                class_id INT NULL,
                school_id INT NULL,
                content TEXT NOT NULL,
                post_type ENUM('announcement', 'homework', 'event') DEFAULT 'announcement',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE,
                FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE,
                INDEX idx_author (author_id),
                INDEX idx_class (class_id),
                INDEX idx_school (school_id),
                INDEX idx_created (created_at)
            )
        `);
        info('✓ Posts table ready');

        // Calendar events table
        await query(`
            CREATE TABLE IF NOT EXISTS calendar_events (
                id INT AUTO_INCREMENT PRIMARY KEY,
                post_id INT,
                class_id INT NULL,
                school_id INT NULL,
                title VARCHAR(255) NOT NULL,
                event_date DATE NOT NULL,
                event_type ENUM('homework', 'assignment', 'event') DEFAULT 'event',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE SET NULL,
                FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE,
                FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE,
                INDEX idx_post (post_id),
                INDEX idx_class (class_id),
                INDEX idx_school (school_id),
                INDEX idx_event_date (event_date)
            )
        `);
        info('✓ Calendar events table ready');

        // Assignments table
        await query(`
            CREATE TABLE IF NOT EXISTS assignments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                class_id INT NOT NULL,
                course_id INT NOT NULL,
                teacher_id INT NOT NULL,
                title VARCHAR(255) NOT NULL,
                due_date DATETIME NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
                FOREIGN KEY (teacher_id) REFERENCES users(id) ON DELETE CASCADE,
                INDEX idx_class (class_id),
                INDEX idx_course (course_id),
                INDEX idx_teacher (teacher_id),
                INDEX idx_due_date (due_date)
            )
        `);
        info('✓ Assignments table ready');

        // Assignment progress table
        await query(`
            CREATE TABLE IF NOT EXISTS assignment_progress (
                id INT AUTO_INCREMENT PRIMARY KEY,
                assignment_id INT NOT NULL,
                student_id INT NOT NULL,
                completion_percentage INT DEFAULT 0,
                score DECIMAL(5,2) DEFAULT 0,
                submitted_at TIMESTAMP NULL,
                FOREIGN KEY (assignment_id) REFERENCES assignments(id) ON DELETE CASCADE,
                FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
                UNIQUE KEY unique_progress (assignment_id, student_id),
                INDEX idx_assignment (assignment_id),
                INDEX idx_student (student_id)
            )
        `);
        info('✓ Assignment progress table ready');

        // Simulators table (Parent)
        await query(`
            CREATE TABLE IF NOT EXISTS simulators (
                id INT AUTO_INCREMENT PRIMARY KEY,
                creator_id INT NOT NULL,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                version VARCHAR(20) DEFAULT '1.0.0',
                blocks LONGTEXT NOT NULL,
                connections LONGTEXT NOT NULL,
                preview_image LONGTEXT,
                tags VARCHAR(500),
                downloads INT DEFAULT 0,
                rating DECIMAL(3,2) DEFAULT 0,
                is_public BOOLEAN DEFAULT FALSE,
                is_featured BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (creator_id) REFERENCES users(id) ON DELETE CASCADE,
                INDEX idx_public (is_public),
                INDEX idx_featured (is_featured),
                INDEX idx_rating (rating)
            )
        `);
        info('✓ Simulators table ready');

        // Migration: Add simulator fork and code mode columns
        await addColumn('simulators', 'forked_from', 'INT');
        await addColumn('simulators', 'fork_count', 'INT DEFAULT 0');
        await addColumn('simulators', 'code_mode', 'LONGTEXT');
        await addColumn('simulators', 'sim_type', "VARCHAR(50) DEFAULT 'block'");
        await addColumn('simulators', 'blocked_reason', 'TEXT');
        await addColumn('simulators', 'is_blocked', 'BOOLEAN DEFAULT FALSE');
        info('✓ Simulator fork/code columns verified/added');

        // Dependents on Users & Courses
        await query(`
            CREATE TABLE IF NOT EXISTS admin_favorites (
                admin_id INT,
                course_id INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (admin_id, course_id),
                FOREIGN KEY (admin_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
            )
        `);

        await query(`
            CREATE TABLE IF NOT EXISTS course_views (
                user_id INT,
                course_id INT,
                view_duration_hours DECIMAL(10,2) DEFAULT 0,
                last_viewed TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                completed BOOLEAN DEFAULT FALSE,
                PRIMARY KEY (user_id, course_id),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
            )
        `);

        await query(`
            CREATE TABLE IF NOT EXISTS enrollments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                course_id INT,
                enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
                UNIQUE KEY unique_enrollment (user_id, course_id)
            )
        `);

        await query(`
            CREATE TABLE IF NOT EXISTS ai_tutor_messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                role ENUM('user', 'assistant') NOT NULL,
                content TEXT NOT NULL,
                course_id INT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE SET NULL,
                INDEX idx_user_created (user_id, created_at)
            )
        `);
        await query(`
            CREATE TABLE IF NOT EXISTS user_learning_profile (
                user_id INT PRIMARY KEY,
                summary_text TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        `);
        info('✓ AI tutor tables ready');

        await query(`
            CREATE TABLE IF NOT EXISTS ai_editor_help_messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                course_id INT NOT NULL,
                role ENUM('user', 'assistant') NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_user_course_created (user_id, course_id, created_at),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
            )
        `);
        info('✓ AI editor help history table ready');

        // Course likes table
        await query(`
            CREATE TABLE IF NOT EXISTS course_likes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                course_id INT NOT NULL,
                user_id INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                UNIQUE KEY unique_like (course_id, user_id),
                INDEX idx_course (course_id),
                INDEX idx_user (user_id)
            )
        `);
        info('✓ User-Course relationship tables ready');

        // Dependents on Simulators
        await query(`
            CREATE TABLE IF NOT EXISTS simulator_ratings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                simulator_id INT NOT NULL,
                user_id INT NOT NULL,
                rating INT CHECK (rating >= 1 AND rating <= 5),
                review TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (simulator_id) REFERENCES simulators(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                UNIQUE KEY unique_rating (simulator_id, user_id),
                INDEX idx_simulator (simulator_id)
            )
        `);

        await query(`
            CREATE TABLE IF NOT EXISTS simulator_downloads (
                id INT AUTO_INCREMENT PRIMARY KEY,
                simulator_id INT NOT NULL,
                user_id INT NOT NULL,
                course_id INT,
                downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (simulator_id) REFERENCES simulators(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE SET NULL
            )
        `);

        await query(`
            CREATE TABLE IF NOT EXISTS simulator_comments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                simulator_id INT NOT NULL,
                user_id INT NOT NULL,
                comment TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (simulator_id) REFERENCES simulators(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        `);

        await query(`
            CREATE TABLE IF NOT EXISTS simulator_versions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                simulator_id INT NOT NULL,
                version_number INT DEFAULT 1,
                blocks LONGTEXT NOT NULL,
                connections LONGTEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (simulator_id) REFERENCES simulators(id) ON DELETE CASCADE,
                INDEX idx_simulator (simulator_id)
            )
        `);
        info('✓ Simulator dependent tables ready');

        // Integration tables
        await query(`
            CREATE TABLE IF NOT EXISTS course_simulator_usage (
                id INT AUTO_INCREMENT PRIMARY KEY,
                course_id INT NOT NULL,
                simulator_id INT NOT NULL,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
                FOREIGN KEY (simulator_id) REFERENCES simulators(id) ON DELETE CASCADE,
                UNIQUE KEY unique_course_sim (course_id, simulator_id)
            )
        `);

        await query(`
            CREATE TABLE IF NOT EXISTS course_questions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                course_id INT NOT NULL,
                question_text LONGTEXT NOT NULL,
                question_type ENUM('multiple_choice', 'true_false', 'short_answer', 'fill_in_blank_with_image') DEFAULT 'multiple_choice',
                options JSON,
                correct_answer TEXT NOT NULL,
                explanation TEXT,
                points INT DEFAULT 1,
                order_index INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
                INDEX idx_course (course_id)
            )
        `);

        // Migration 1: Upgrade question_text from TEXT to LONGTEXT for base64 image support
        try {
            await query(`ALTER TABLE course_questions MODIFY COLUMN question_text LONGTEXT NOT NULL`);
            console.log('[INFO] ✓ course_questions.question_text migrated to LONGTEXT');
        } catch (e) {
            console.error('[WARN] course_questions.question_text migration:', e.code, e.message);
        }

        // Migration 2: Add fill_in_blank_with_image to question_type ENUM
        try {
            await query(`ALTER TABLE course_questions MODIFY COLUMN question_type ENUM('multiple_choice', 'true_false', 'short_answer', 'fill_in_blank_with_image') DEFAULT 'multiple_choice'`);
            console.log('[INFO] ✓ course_questions.question_type ENUM migrated');
        } catch (e) {
            console.error('[WARN] course_questions.question_type migration:', e.code, e.message);
        }

        await query(`
            CREATE TABLE IF NOT EXISTS user_quiz_attempts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                question_id INT NOT NULL,
                user_answer TEXT,
                is_correct BOOLEAN,
                attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (question_id) REFERENCES course_questions(id) ON DELETE CASCADE,
                INDEX idx_user_question (user_id, question_id),
                UNIQUE KEY unique_attempt (user_id, question_id)
            )
        `);
        await addColumn('user_quiz_attempts', 'gems_awarded', 'TINYINT(1) DEFAULT 0');
        info('✓ user_quiz_attempts gems_awarded column ready');

        await query(`
            CREATE TABLE IF NOT EXISTS simulator_interactive_params (
                id INT AUTO_INCREMENT PRIMARY KEY,
                course_id INT NOT NULL,
                simulator_block_id BIGINT NOT NULL,
                block_id INT NOT NULL,
                param_name VARCHAR(100) NOT NULL,
                param_label VARCHAR(255),
                min_value DECIMAL(10,2) DEFAULT 0,
                max_value DECIMAL(10,2) DEFAULT 100,
                step_value DECIMAL(10,2) DEFAULT 1,
                default_value DECIMAL(10,2),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
                UNIQUE KEY unique_param (course_id, simulator_block_id, block_id, param_name)
            )
        `);
        await query(`
            CREATE TABLE IF NOT EXISTS sponsorships (
                id INT AUTO_INCREMENT PRIMARY KEY,
                sponsor_name VARCHAR(255) NOT NULL,
                logo_url VARCHAR(255),
                contribution_amount DECIMAL(10, 2),
                tier VARCHAR(50),
                expiry_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        `);
        info('✓ Sponsorships table ready');

        await query(`
            CREATE TABLE IF NOT EXISTS certificates (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                certificate_type ENUM('volunteer_hours', 'course_milestone', 'creator_verified') DEFAULT 'volunteer_hours',
                hours_certified FLOAT DEFAULT 0,
                courses_count INT DEFAULT 0,
                verification_code VARCHAR(64) UNIQUE,
                issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                INDEX idx_verification (verification_code)
            )
        `);
        info('✓ Certificates table ready');

        info('✓ All tables initialized successfully');

        // Check for superadmin
        const superadminEmail = process.env.SUPERADMIN_EMAIL || 'viratsuper6@gmail.com';
        const superadminPassword = process.env.SUPERADMIN_PASSWORD || 'Virat@123';

        const superadmins = await query('SELECT * FROM users WHERE email = ?', [superadminEmail]);
        if (superadmins.length === 0) {
            const hashedPassword = await bcrypt.hash(superadminPassword, 10);
            await query('INSERT INTO users (email, password, role, is_admin_approved) VALUES (?, ?, \'superadmin\', TRUE)',
                [superadminEmail, hashedPassword]);
            info('✓ Superadmin created successfully');
        } else {
            info('✓ Superadmin already exists');
        }

    } catch (err) {
        console.error('❌ Database initialization failed:', err);
    }
};

// Start initialization
initializeDatabase();

// ===== UTILITY FUNCTIONS =====
function apiResponse(res, statusCode, message, data = null) {
    const response = {
        success: statusCode < 400,
        message
    };
    if (data !== null) response.data = data;
    return res.status(statusCode).json(response);
}

// ===== MIDDLEWARE =====
// Input validation middleware
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePassword(password) {
    // At least 8 characters, 1 uppercase, 1 lowercase, 1 number
    const re = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;
    return re.test(password);
}

function generateUniqueCode(length = 6) {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let code = '';
    for (let i = 0; i < length; i++) {
        code += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return code;
}

// JWT authentication middleware
const authenticateToken = (req, res, next) => {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];

    // Try Authorization header first
    if (token) {
        return jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
            if (!err) {
                req.user = user;
                return next();
            }

            // If Authorization header token fails, try cookie fallback
            const cookieToken = req.cookies.token;
            if (cookieToken) {
                return jwt.verify(cookieToken, process.env.JWT_SECRET, (err2, user2) => {
                    if (!err2) {
                        req.user = user2;
                        return next();
                    }
                    console.error('❌ JWT Verification Error (header & cookie failed):', {
                        headerErr: err.message,
                        cookieErr: err2.message
                    });
                    return apiResponse(res, 403, 'Invalid or expired token');
                });
            }

            // Header token failed and no cookie available
            console.error('❌ JWT Header Verification Error:', err.message);
            return apiResponse(res, 403, 'Invalid or expired token');
        });
    }

    // No Authorization header, try cookie
    const cookieToken = req.cookies.token;
    if (cookieToken) {
        return jwt.verify(cookieToken, process.env.JWT_SECRET, (err, user) => {
            if (err) {
                console.error('❌ JWT Cookie Verification Error:', err.message);
                return apiResponse(res, 403, 'Invalid or expired session');
            }
            req.user = user;
            return next();
        });
    }

    // No token in header or cookie
    console.warn('⚠️ No authentication token provided (no Authorization header, no cookie)');
    return apiResponse(res, 401, 'Access token required. Please log in.');
};

// Alternative middleware that ONLY checks cookies (preferred for new flow)
const authenticateCookie = (req, res, next) => {
    const token = req.cookies.token;

    if (!token) {
        return apiResponse(res, 401, 'Authentication required');
    }

    jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
        if (err) {
            return apiResponse(res, 403, 'Invalid or expired session');
        }
        req.user = user;
        next();
    });
};

// Role-based authorization middleware
// ===== SANITIZATION FUNCTION (Defense in Depth) =====
const sanitizeHtml = (input) => {
    if (!input) return '';
    return String(input)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
};

const authorize = (...roles) => {
    return (req, res, next) => {
        if (!roles.includes(req.user.role)) {
            return apiResponse(res, 403, 'Insufficient permissions');
        }
        next();
    };
};

// AI Tutor rate limiter (kept separate as it has specific requirements)
const aiTutorLimiter = rateLimit({
    windowMs: 60 * 1000,
    max: 20,
    message: { success: false, message: 'Too many study coach requests. Please wait a moment and try again.' }
});

const aiEditorHelpLimiter = rateLimit({
    windowMs: 60 * 1000,
    max: 40,
    message: { success: false, message: 'Too many AI Help requests. Please wait a moment and try again.' }
});

const createAiTutorHandlers = require('./ai-tutor-handlers');
const aiTutorHandlers = createAiTutorHandlers({ query, openRouterChatCompletion, apiResponse });

const createAiEditorHelpHandlers = require('./ai-editor-help-handlers');
const aiEditorHelpHandlers = createAiEditorHelpHandlers({
    query,
    openRouterChatCompletion,
    apiResponse,
    getOpenRouterKeys
});

const { createLearnerGamificationHandlers } = require('./learner-gamification-handlers');
const learnerGamification = createLearnerGamificationHandlers({
    query,
    apiResponse,
    sendEmail: (to, subject, html) => sendEmail({ to, subject, html })
});
learnerGamification.ensureReady().catch((e) => console.error('Learner store seed error:', e.message));

// ===== SMART RATE LIMITING FOR SERVER WAKE-UP =====

// Track server response times to detect wake-up periods
let serverWakeUpMode = false;
let responseTimeHistory = [];
let wakeUpStartTime = null;

// Enhanced auth limiter that adjusts during server wake-up
const smartAuthLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: (req, res) => {
        // Return 15 requests during wake-up, 5 normally
        return serverWakeUpMode ? 15 : 5;
    },
    message: { success: false, message: 'Too many authentication attempts, please try again later.' },
    standardHeaders: true,
    legacyHeaders: false,
    keyGenerator: (req) => {
        // Include wake-up mode in key to prevent limit abuse
        return req.ip + (serverWakeUpMode ? '_wakeup' : '_normal');
    }
});

// Middleware to track response times and detect server wake-up
const trackResponseTime = (req, res, next) => {
    const startTime = Date.now();
    
    res.on('finish', () => {
        const responseTime = Date.now() - startTime;
        responseTimeHistory.push(responseTime);
        
        // Keep only last 20 responses
        if (responseTimeHistory.length > 20) {
            responseTimeHistory.shift();
        }
        
        // Detect server wake-up (average response time > 30 seconds)
        const avgResponseTime = responseTimeHistory.reduce((a, b) => a + b, 0) / responseTimeHistory.length;
        
        if (avgResponseTime > 30000 && !serverWakeUpMode) {
            serverWakeUpMode = true;
            wakeUpStartTime = Date.now();
            info('🔄 Server wake-up detected - Increasing auth rate limits');
        }
        
        // Auto-reset wake-up mode after 5 minutes of normal response times
        if (serverWakeUpMode && avgResponseTime < 5000 && (Date.now() - wakeUpStartTime > 300000)) {
            serverWakeUpMode = false;
            wakeUpStartTime = null;
            info('✅ Server fully awake - Normal rate limits restored');
        }
    });
    
    next();
};

// Apply response time tracking
app.use(trackResponseTime);

// Apply generic rate limiter to all /api/ routes
app.use('/api/', generalLimiter);

// ===== ROUTES =====

// Basic Route
app.get('/', (req, res) => {
    res.send('Veelearn Backend API is running!');
});

// Health Check Endpoint for Keep-Alive Bot
app.get('/api/health', (req, res) => {
    res.json({ 
        status: 'ok', 
        timestamp: new Date().toISOString(),
        uptime: process.uptime(),
        wakeUpMode: serverWakeUpMode
    });
});

// ===== AUTHENTICATION ROUTES =====
app.post('/api/register', smartAuthLimiter, async (req, res) => {
    const { email, password } = req.body;

    if (!email || !password) {
        return apiResponse(res, 400, 'Email and password are required');
    }

    if (!validateEmail(email)) {
        return apiResponse(res, 400, 'Invalid email format');
    }

    if (!validatePassword(password)) {
        return apiResponse(res, 400, 'Password must be at least 8 characters with uppercase, lowercase, and number');
    }

    try {
        const hashedPassword = await bcrypt.hash(password, 10);
        const insertUser = 'INSERT INTO users (email, password) VALUES (?, ?)';

        db.query(insertUser, [email, hashedPassword], (err, result) => {
            if (err) {
                if (err.code === 'ER_DUP_ENTRY') {
                    return apiResponse(res, 409, 'Email already registered');
                }
                console.error('Error during registration:', err);
                return apiResponse(res, 500, 'Server error during registration');
            }

            const newUser = {
                id: result.insertId,
                email,
                role: 'user',
                is_admin_approved: false,
                shells: 0
            };
            const token = jwt.sign(
                { id: newUser.id, role: newUser.role },
                process.env.JWT_SECRET,
                { expiresIn: '24h' }
            );

            // Set cookie
            res.cookie('token', token, {
                httpOnly: true,
                secure: process.env.NODE_ENV === 'production',
                sameSite: 'Lax',
                maxAge: 24 * 60 * 60 * 1000 // 24 hours
            });

            apiResponse(res, 201, 'User registered successfully', { token, user: newUser });
        });
    } catch (error) {
        console.error('Hashing error:', error);
        apiResponse(res, 500, 'Server error');
    }
});

app.post('/api/login', smartAuthLimiter, async (req, res) => {
    const { email, password } = req.body;

    if (!email || !password) {
        return apiResponse(res, 400, 'Email and password are required');
    }

    try {
        db.query('SELECT * FROM users WHERE email = ?', [email], async (err, results) => {
            if (err) {
                console.error('Error during login:', err);
                return apiResponse(res, 500, 'Server error during login');
            }

            if (results.length === 0) {
                return apiResponse(res, 400, 'Invalid credentials');
            }

            const user = results[0];
            const isMatch = await bcrypt.compare(password, user.password);

            if (!isMatch) {
                return apiResponse(res, 400, 'Invalid credentials');
            }

            const token = jwt.sign(
                { id: user.id, role: user.role },
                process.env.JWT_SECRET,
                { expiresIn: '24h' }
            );

            // Set cookie
            res.cookie('token', token, {
                httpOnly: true,
                secure: process.env.NODE_ENV === 'production',
                sameSite: 'Lax',
                maxAge: 24 * 60 * 60 * 1000 // 24 hours
            });

            const { password: _, ...userWithoutPassword } = user;
            apiResponse(res, 200, 'Logged in successfully', { token, user: userWithoutPassword });
        });
    } catch (error) {
        console.error('Login error:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// ===== LOGOUT ROUTE =====
app.post('/api/logout', (req, res) => {
    res.clearCookie('token', {
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'Lax',
        path: '/'
    });
    apiResponse(res, 200, 'Logged out successfully');
});

// ===== EMS REGISTRATION ENDPOINTS =====

// School Admin Registration
app.post('/api/register/school-admin', smartAuthLimiter, async (req, res) => {
    const { email, password, name, school_name, school_address } = req.body;

    if (!email || !password || !name || !school_name) {
        return apiResponse(res, 400, 'Email, password, name, and school name are required');
    }

    if (!validateEmail(email)) {
        return apiResponse(res, 400, 'Invalid email format');
    }

    if (!validatePassword(password)) {
        return apiResponse(res, 400, 'Password must be at least 8 characters with uppercase, lowercase, and number');
    }

    try {
        const hashedPassword = await bcrypt.hash(password, 10);

        // Create user with school_admin role
        const insertUser = 'INSERT INTO users (email, password, name, role, is_approved) VALUES (?, ?, ?, \'school_admin\', FALSE)';
        db.query(insertUser, [email, hashedPassword, name], async (err, result) => {
            if (err) {
                if (err.code === 'ER_DUP_ENTRY') {
                    return apiResponse(res, 409, 'Email already registered');
                }
                console.error('Error during school admin registration:', err);
                return apiResponse(res, 500, 'Server error during registration');
            }

            const userId = result.insertId;

            // Create school record
            const insertSchool = 'INSERT INTO schools (name, school_admin_id, is_approved) VALUES (?, ?, FALSE)';
            db.query(insertSchool, [school_name, userId], (schoolErr) => {
                if (schoolErr) {
                    console.error('Error creating school:', schoolErr);
                    return apiResponse(res, 500, 'Server error creating school');
                }

                apiResponse(res, 201, 'School admin registered successfully. Pending approval from Superadmin.', {
                    user: { id: userId, email, name, role: 'school_admin' },
                    status: 'pending_approval'
                });
            });
        });
    } catch (error) {
        console.error('Hashing error:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// Teacher Registration with School Code
app.post('/api/register/teacher', smartAuthLimiter, async (req, res) => {
    const { email, password, name, school_code } = req.body;

    if (!email || !password || !name || !school_code) {
        return apiResponse(res, 400, 'Email, password, name, and school code are required');
    }

    if (!validateEmail(email)) {
        return apiResponse(res, 400, 'Invalid email format');
    }

    if (!validatePassword(password)) {
        return apiResponse(res, 400, 'Password must be at least 8 characters with uppercase, lowercase, and number');
    }

    try {
        // Validate school code and get school_id
        const schools = await query('SELECT id, is_approved FROM schools WHERE school_code = ?', [school_code]);
        if (schools.length === 0) {
            return apiResponse(res, 400, 'Invalid school code');
        }

        const school = schools[0];
        if (!school.is_approved) {
            return apiResponse(res, 400, 'School is not yet approved');
        }

        const hashedPassword = await bcrypt.hash(password, 10);

        // Create teacher user (pending approval)
        const insertUser = 'INSERT INTO users (email, password, name, role, school_id, school_code, is_approved) VALUES (?, ?, ?, \'teacher\', ?, ?, FALSE)';
        db.query(insertUser, [email, hashedPassword, name, school.id, school_code], (err, result) => {
            if (err) {
                if (err.code === 'ER_DUP_ENTRY') {
                    return apiResponse(res, 409, 'Email already registered');
                }
                console.error('Error during teacher registration:', err);
                return apiResponse(res, 500, 'Server error during registration');
            }

            const newUser = {
                id: result.insertId,
                email,
                name,
                role: 'teacher',
                school_id: school.id
            };

            apiResponse(res, 201, 'Teacher registered successfully. Pending approval from Superadmin.', { user: newUser });
        });
    } catch (error) {
        console.error('Registration error:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// Student Registration (with school code and optional class code)
app.post('/api/register/student', smartAuthLimiter, async (req, res) => {
    const { email, password, name, school_code, class_code } = req.body;

    if (!email || !password || !name || !school_code) {
        return apiResponse(res, 400, 'Email, password, name, and school code are required');
    }

    if (!validateEmail(email)) {
        return apiResponse(res, 400, 'Invalid email format');
    }

    if (!validatePassword(password)) {
        return apiResponse(res, 400, 'Password must be at least 8 characters with uppercase, lowercase, and number');
    }

    try {
        // Validate school code and get school_id
        const schools = await query('SELECT id, is_approved FROM schools WHERE school_code = ?', [school_code]);
        if (schools.length === 0) {
            return apiResponse(res, 400, 'Invalid school code');
        }

        const school = schools[0];
        if (!school.is_approved) {
            return apiResponse(res, 400, 'School is not yet approved');
        }

        const school_id = school.id;
        let class_id = null;

        // If class code provided, validate and get class_id
        if (class_code) {
            const classes = await query(`
                SELECT c.id 
                FROM classes c
                WHERE c.id = ?
            `, [class_code]);

            if (classes.length === 0) {
                return apiResponse(res, 400, 'Invalid class code');
            }

            class_id = classes[0].id;
        }

        const hashedPassword = await bcrypt.hash(password, 10);

        // Generate unique parent code for students
        const parent_code = generateUniqueCode(6).toUpperCase();

        // Create user
        const insertUser = 'INSERT INTO users (email, password, name, role, school_id, school_code, parent_code, is_approved) VALUES (?, ?, ?, \'student\', ?, ?, ?, TRUE)';
        db.query(insertUser, [email, hashedPassword, name, school_id, school_code, parent_code], async (err, result) => {
            if (err) {
                if (err.code === 'ER_DUP_ENTRY') {
                    return apiResponse(res, 409, 'Email already registered');
                }
                console.error('Error during student registration:', err);
                return apiResponse(res, 500, 'Server error during registration');
            }

            const userId = result.insertId;

            // If class code provided, auto-enroll student in class
            if (class_id) {
                try {
                    await query('INSERT INTO class_enrollments (class_id, student_id) VALUES (?, ?)', [class_id, userId]);
                } catch (enrollErr) {
                    console.error('Error enrolling student in class:', enrollErr);
                    // Continue even if enrollment fails
                }
            }

            const newUser = {
                id: userId,
                email,
                name,
                role: 'student',
                school_id,
                parent_code,
                class_id
            };

            apiResponse(res, 201, `Student registered successfully! Parent code: ${parent_code}`, { user: newUser });
        });
    } catch (error) {
        console.error('Registration error:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// Parent Registration with Student Code
app.post('/api/register/parent', smartAuthLimiter, async (req, res) => {
    const { email, password, name, student_code } = req.body;

    if (!email || !password || !name || !student_code) {
        return apiResponse(res, 400, 'Email, password, name, and student code are required');
    }

    if (!validateEmail(email)) {
        return apiResponse(res, 400, 'Invalid email format');
    }

    if (!validatePassword(password)) {
        return apiResponse(res, 400, 'Password must be at least 8 characters with uppercase, lowercase, and number');
    }

    try {
        // Validate student code and get student_id
        const students = await query('SELECT id FROM users WHERE parent_code = ? AND role = \'student\'', [student_code]);
        if (students.length === 0) {
            return apiResponse(res, 400, 'Invalid student code');
        }

        const student_id = students[0].id;

        const hashedPassword = await bcrypt.hash(password, 10);

        // Create parent user
        const insertUser = 'INSERT INTO users (email, password, name, role, is_approved) VALUES (?, ?, ?, \'parent\', TRUE)';
        db.query(insertUser, [email, hashedPassword, name], (err, result) => {
            if (err) {
                if (err.code === 'ER_DUP_ENTRY') {
                    return apiResponse(res, 409, 'Email already registered');
                }
                console.error('Error during parent registration:', err);
                return apiResponse(res, 500, 'Server error during registration');
            }

            const parent_id = result.insertId;

            // Link parent to student
            const insertLink = 'INSERT INTO parent_student_links (parent_id, student_id) VALUES (?, ?)';
            db.query(insertLink, [parent_id, student_id], (linkErr) => {
                if (linkErr) {
                    console.error('Error linking parent to student:', linkErr);
                    return apiResponse(res, 500, 'Server error linking parent to student');
                }

                const newUser = {
                    id: parent_id,
                    email,
                    name,
                    role: 'parent'
                };

                apiResponse(res, 201, 'Parent registered successfully', { user: newUser });
            });
        });
    } catch (error) {
        console.error('Registration error:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// ===== EMS SCHOOL MANAGEMENT ENDPOINTS =====

// Get pending school admin approvals (Superadmin only)
app.get('/api/schools/pending', authenticateToken, async (req, res) => {
    if (req.user.role !== 'superadmin') {
        return apiResponse(res, 403, 'Only superadmin can view pending approvals');
    }

    try {
        const pendingSchools = await query(`
            SELECT s.*, u.email, u.name as admin_name
            FROM schools s
            JOIN users u ON s.school_admin_id = u.id
            WHERE s.is_approved = FALSE
        `);
        apiResponse(res, 200, 'Pending schools retrieved', pendingSchools);
    } catch (error) {
        console.error('Error fetching pending schools:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// Approve school (Superadmin only)
app.put('/api/schools/:schoolId/approve', authenticateToken, async (req, res) => {
    if (req.user.role !== 'superadmin') {
        return apiResponse(res, 403, 'Only superadmin can approve schools');
    }

    const { schoolId } = req.params;

    try {
        // Generate unique school code
        const school_code = generateUniqueCode(6).toUpperCase();

        // Update school
        await query('UPDATE schools SET is_approved = TRUE, school_code = ? WHERE id = ?', [school_code, schoolId]);

        // Update school admin user approval
        await query('UPDATE users SET is_approved = TRUE WHERE id = (SELECT school_admin_id FROM schools WHERE id = ?)', [schoolId]);

        apiResponse(res, 200, 'School approved successfully', { school_code });
    } catch (error) {
        console.error('Error approving school:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// Approve teacher (Superadmin only)
app.put('/api/users/:userId/approve-teacher', authenticateToken, async (req, res) => {
    if (req.user.role !== 'superadmin') {
        return apiResponse(res, 403, 'Only superadmin can approve teachers');
    }

    const { userId } = req.params;

    try {
        // Verify user is a teacher
        const users = await query('SELECT id, role FROM users WHERE id = ? AND role = ?', [userId, 'teacher']);
        if (users.length === 0) {
            return apiResponse(res, 404, 'Teacher not found');
        }

        // Update teacher approval
        await query('UPDATE users SET is_approved = TRUE WHERE id = ?', [userId]);

        apiResponse(res, 200, 'Teacher approved successfully');
    } catch (error) {
        console.error('Error approving teacher:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// Get pending teachers (Superadmin only)
app.get('/api/users/pending-teachers', authenticateToken, async (req, res) => {
    if (req.user.role !== 'superadmin') {
        return apiResponse(res, 403, 'Only superadmin can view pending teachers');
    }

    try {
        const teachers = await query(`
            SELECT u.id, u.email, u.name, u.school_id, s.name as school_name
            FROM users u
            LEFT JOIN schools s ON u.school_id = s.id
            WHERE u.role = 'teacher' AND u.is_approved = FALSE
            ORDER BY u.created_at DESC
        `);

        apiResponse(res, 200, 'Pending teachers retrieved successfully', teachers);
    } catch (error) {
        console.error('Error fetching pending teachers:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// Get current user
app.get('/api/users/me', authenticateToken, async (req, res) => {
    try {
        const user = await query(`
            SELECT id, email, name, role, is_approved, school_id
            FROM users
            WHERE id = ?
        `, [req.user.id]);
        
        if (user.length === 0) {
            return apiResponse(res, 404, 'User not found');
        }
        
        apiResponse(res, 200, 'User retrieved successfully', user[0]);
    } catch (error) {
        console.error('Error fetching current user:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// Get teachers for parent messaging
app.get('/api/users/teachers', authenticateToken, async (req, res) => {
    if (req.user.role !== 'parent') {
        return apiResponse(res, 403, 'Only parents can view teachers');
    }

    try {
        const teachers = await query(`
            SELECT u.id, u.email, u.name, u.school_id, s.name as school_name
            FROM users u
            LEFT JOIN schools s ON u.school_id = s.id
            WHERE u.role = 'teacher' AND u.is_approved = TRUE
            ORDER BY u.name ASC
        `);

        apiResponse(res, 200, 'Teachers retrieved successfully', teachers);
    } catch (error) {
        console.error('Error fetching teachers:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// Get parents for teacher messaging
app.get('/api/users/parents', authenticateToken, async (req, res) => {
    if (req.user.role !== 'teacher') {
        return apiResponse(res, 403, 'Only teachers can view parents');
    }

    try {
        const parents = await query(`
            SELECT u.id, u.email, u.name
            FROM users u
            WHERE u.role = 'parent'
            ORDER BY u.name ASC
        `);

        apiResponse(res, 200, 'Parents retrieved successfully', parents);
    } catch (error) {
        console.error('Error fetching parents:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// Get school by code
app.get('/api/schools/by-code/:schoolCode', async (req, res) => {
    const { schoolCode } = req.params;

    try {
        const schools = await query('SELECT id, name, is_approved FROM schools WHERE school_code = ?', [schoolCode]);
        if (schools.length === 0) {
            return apiResponse(res, 404, 'School not found');
        }
        apiResponse(res, 200, 'School found', schools[0]);
    } catch (error) {
        console.error('Error fetching school:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// Get school info for school admin
app.get('/api/schools/my-school', authenticateToken, async (req, res) => {
    if (req.user.role !== 'school_admin') {
        return apiResponse(res, 403, 'Only school admin can view their school');
    }

    try {
        const schools = await query('SELECT * FROM schools WHERE school_admin_id = ?', [req.user.id]);
        if (schools.length === 0) {
            return apiResponse(res, 404, 'School not found');
        }
        apiResponse(res, 200, 'School found', schools[0]);
    } catch (error) {
        console.error('Error fetching school:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// Get all schools (Superadmin only)
app.get('/api/schools', authenticateToken, async (req, res) => {
    if (req.user.role !== 'superadmin') {
        return apiResponse(res, 403, 'Only superadmin can view all schools');
    }

    try {
        const schools = await query(`
            SELECT s.*, u.email, u.name as admin_name
            FROM schools s
            JOIN users u ON s.school_admin_id = u.id
            ORDER BY s.created_at DESC
        `);
        apiResponse(res, 200, 'Schools retrieved', schools);
    } catch (error) {
        console.error('Error fetching schools:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// ===== EMS CLASS MANAGEMENT ENDPOINTS =====

// Create class (School admin only)
app.post('/api/classes', authenticateToken, writeLimiter, async (req, res) => {
    if (req.user.role !== 'school_admin') {
        return apiResponse(res, 403, 'Only school admin can create classes');
    }

    const { name } = req.body;

    if (!name) {
        return apiResponse(res, 400, 'Class name is required');
    }

    try {
        // Get school_id for this school admin
        const schools = await query('SELECT id FROM schools WHERE school_admin_id = ?', [req.user.id]);
        if (schools.length === 0) {
            return apiResponse(res, 404, 'School not found');
        }

        const school_id = schools[0].id;

        const result = await query('INSERT INTO classes (school_id, name) VALUES (?, ?)', [school_id, name]);

        apiResponse(res, 201, 'Class created successfully', { id: result.insertId, name, school_id });
    } catch (error) {
        console.error('Error creating class:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// Lookup users (teachers) for school admin
app.get('/api/users/lookup', authenticateToken, async (req, res) => {
    if (req.user.role !== 'school_admin' && req.user.role !== 'superadmin') {
        return apiResponse(res, 403, 'Only school admin or superadmin can lookup users');
    }

    const { search, role } = req.query;

    try {
        let users = [];
        
        if (req.user.role === 'school_admin') {
            // Get school admin's school
            const schools = await query('SELECT id FROM schools WHERE school_admin_id = ?', [req.user.id]);
            if (schools.length === 0) {
                return apiResponse(res, 404, 'School not found');
            }
            const schoolId = schools[0].id;

            // Search teachers in the same school
            let queryStr = `
                SELECT id, name, email, role
                FROM users
                WHERE school_id = ?
            `;
            const params = [schoolId];

            if (role) {
                queryStr += ' AND role = ?';
                params.push(role);
            }

            if (search) {
                queryStr += ' AND (name LIKE ? OR email LIKE ?)';
                params.push(`%${search}%`, `%${search}%`);
            }

            queryStr += ' ORDER BY name ASC LIMIT 20';
            users = await query(queryStr, params);
        } else {
            // Superadmin can search all users
            let queryStr = `
                SELECT id, name, email, role, school_id
                FROM users
                WHERE 1=1
            `;
            const params = [];

            if (role) {
                queryStr += ' AND role = ?';
                params.push(role);
            }

            if (search) {
                queryStr += ' AND (name LIKE ? OR email LIKE ?)';
                params.push(`%${search}%`, `%${search}%`);
            }

            queryStr += ' ORDER BY name ASC LIMIT 20';
            users = await query(queryStr, params);
        }

        apiResponse(res, 200, 'Users retrieved', users);
    } catch (error) {
        console.error('Error looking up users:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// Assign teacher to class (School admin only)
app.put('/api/classes/:classId/teacher', authenticateToken, writeLimiter, async (req, res) => {
    if (req.user.role !== 'school_admin') {
        return apiResponse(res, 403, 'Only school admin can assign teachers');
    }

    const { classId } = req.params;
    const { teacher_id } = req.body;

    if (!teacher_id) {
        return apiResponse(res, 400, 'Teacher ID is required');
    }

    try {
        // Verify teacher belongs to same school
        const teachers = await query('SELECT school_id FROM users WHERE id = ? AND role = \'teacher\'', [teacher_id]);
        if (teachers.length === 0) {
            return apiResponse(res, 404, 'Teacher not found');
        }

        // Verify class belongs to this school admin's school
        const classes = await query(`
            SELECT c.id
            FROM classes c
            JOIN schools s ON c.school_id = s.id
            WHERE c.id = ? AND s.school_admin_id = ?
        `, [classId, req.user.id]);

        if (classes.length === 0) {
            return apiResponse(res, 404, 'Class not found or access denied');
        }

        await query('UPDATE classes SET teacher_id = ? WHERE id = ?', [teacher_id, classId]);

        apiResponse(res, 200, 'Teacher assigned to class successfully');
    } catch (error) {
        console.error('Error assigning teacher:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// Get classes for school admin
app.get('/api/classes/my-classes', authenticateToken, async (req, res) => {
    if (req.user.role !== 'school_admin') {
        return apiResponse(res, 403, 'Only school admin can view their classes');
    }

    try {
        const classes = await query(`
            SELECT c.*, u.name as teacher_name, u.email as teacher_email
            FROM classes c
            LEFT JOIN users u ON c.teacher_id = u.id
            JOIN schools s ON c.school_id = s.id
            WHERE s.school_admin_id = ?
            ORDER BY c.created_at DESC
        `, [req.user.id]);

        // Get student count for each class
        for (let cls of classes) {
            const countResult = await query('SELECT COUNT(*) as count FROM class_enrollments WHERE class_id = ?', [cls.id]);
            cls.student_count = countResult[0].count;
        }

        apiResponse(res, 200, 'Classes retrieved', classes);
    } catch (error) {
        console.error('Error fetching classes:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// Get students in school (School admin only)
app.get('/api/schools/my-school/students', authenticateToken, async (req, res) => {
    if (req.user.role !== 'school_admin') {
        return apiResponse(res, 403, 'Only school admin can view school students');
    }

    try {
        const schools = await query('SELECT id FROM schools WHERE school_admin_id = ?', [req.user.id]);
        if (schools.length === 0) {
            return apiResponse(res, 404, 'School not found');
        }

        const school_id = schools[0].id;

        const students = await query(`
            SELECT u.id, u.email, u.name
            FROM users u
            WHERE u.school_id = ? AND u.role = 'student'
            ORDER BY u.name ASC
        `, [school_id]);

        apiResponse(res, 200, 'Students retrieved', students);
    } catch (error) {
        console.error('Error fetching students:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// Enroll student in class (School admin only)
app.post('/api/class-enrollments', authenticateToken, writeLimiter, async (req, res) => {
    if (req.user.role !== 'school_admin') {
        return apiResponse(res, 403, 'Only school admin can enroll students');
    }

    const { class_id, student_id } = req.body;

    if (!class_id || !student_id) {
        return apiResponse(res, 400, 'Class ID and Student ID are required');
    }

    try {
        // Verify class belongs to this school admin's school
        const classes = await query(`
            SELECT c.id
            FROM classes c
            JOIN schools s ON c.school_id = s.id
            WHERE c.id = ? AND s.school_admin_id = ?
        `, [class_id, req.user.id]);

        if (classes.length === 0) {
            return apiResponse(res, 404, 'Class not found or access denied');
        }

        // Check if already enrolled
        const existing = await query('SELECT id FROM class_enrollments WHERE class_id = ? AND student_id = ?', [class_id, student_id]);
        if (existing.length > 0) {
            return apiResponse(res, 400, 'Student already enrolled in this class');
        }

        await query('INSERT INTO class_enrollments (class_id, student_id) VALUES (?, ?)', [class_id, student_id]);

        apiResponse(res, 201, 'Student enrolled successfully');
    } catch (error) {
        console.error('Error enrolling student:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// Remove student from class (School admin only)
app.delete('/api/class-enrollments/:enrollmentId', authenticateToken, writeLimiter, async (req, res) => {
    if (req.user.role !== 'school_admin') {
        return apiResponse(res, 403, 'Only school admin can remove students');
    }

    const { enrollmentId } = req.params;

    try {
        // Verify enrollment belongs to this school admin's school
        const enrollments = await query(`
            SELECT ce.id
            FROM class_enrollments ce
            JOIN classes c ON ce.class_id = c.id
            JOIN schools s ON c.school_id = s.id
            WHERE ce.id = ? AND s.school_admin_id = ?
        `, [enrollmentId, req.user.id]);

        if (enrollments.length === 0) {
            return apiResponse(res, 404, 'Enrollment not found or access denied');
        }

        await query('DELETE FROM class_enrollments WHERE id = ?', [enrollmentId]);

        apiResponse(res, 200, 'Student removed from class successfully');
    } catch (error) {
        console.error('Error removing student:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// Get unassigned students for a class (School admin only)
app.get('/api/classes/:classId/unassigned-students', authenticateToken, async (req, res) => {
    if (req.user.role !== 'school_admin') {
        return apiResponse(res, 403, 'Only school admin can view unassigned students');
    }

    const { classId } = req.params;

    try {
        // Verify class belongs to this school admin's school
        const classes = await query(`
            SELECT c.school_id
            FROM classes c
            JOIN schools s ON c.school_id = s.id
            WHERE c.id = ? AND s.school_admin_id = ?
        `, [classId, req.user.id]);

        if (classes.length === 0) {
            return apiResponse(res, 404, 'Class not found or access denied');
        }

        const school_id = classes[0].school_id;

        // Get students not enrolled in this specific class
        const students = await query(`
            SELECT u.id, u.email, u.name
            FROM users u
            WHERE u.school_id = ? AND u.role = 'student'
            AND u.id NOT IN (
                SELECT student_id FROM class_enrollments WHERE class_id = ?
            )
            ORDER BY u.name ASC
        `, [school_id, classId]);

        apiResponse(res, 200, 'Unassigned students retrieved', students);
    } catch (error) {
        console.error('Error fetching unassigned students:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// Get enrolled students for a class (School admin only)
app.get('/api/classes/:classId/enrolled-students', authenticateToken, async (req, res) => {
    if (req.user.role !== 'school_admin') {
        return apiResponse(res, 403, 'Only school admin can view enrolled students');
    }

    const { classId } = req.params;

    try {
        // Verify class belongs to this school admin's school
        const classes = await query(`
            SELECT c.id
            FROM classes c
            JOIN schools s ON c.school_id = s.id
            WHERE c.id = ? AND s.school_admin_id = ?
        `, [classId, req.user.id]);

        if (classes.length === 0) {
            return apiResponse(res, 404, 'Class not found or access denied');
        }

        const students = await query(`
            SELECT u.id, u.email, u.name, ce.enrolled_at
            FROM users u
            JOIN class_enrollments ce ON u.id = ce.student_id
            WHERE ce.class_id = ?
            ORDER BY u.name ASC
        `, [classId]);

        apiResponse(res, 200, 'Enrolled students retrieved', students);
    } catch (error) {
        console.error('Error fetching enrolled students:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// ===== EMS TEACHER ENDPOINTS =====

// Get teacher's classes
app.get('/api/teacher/my-classes', authenticateToken, async (req, res) => {
    if (req.user.role !== 'teacher') {
        return apiResponse(res, 403, 'Only teachers can view their classes');
    }

    try {
        const classes = await query(`
            SELECT c.*, s.name as school_name
            FROM classes c
            JOIN schools s ON c.school_id = s.id
            WHERE c.teacher_id = ?
            ORDER BY c.created_at DESC
        `, [req.user.id]);

        // Get student count for each class
        for (let cls of classes) {
            const countResult = await query('SELECT COUNT(*) as count FROM class_enrollments WHERE class_id = ?', [cls.id]);
            cls.student_count = countResult[0].count;
        }

        apiResponse(res, 200, 'Classes retrieved', classes);
    } catch (error) {
        console.error('Error fetching classes:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// Get students in teacher's class
app.get('/api/teacher/class/:classId/students', authenticateToken, async (req, res) => {
    if (req.user.role !== 'teacher') {
        return apiResponse(res, 403, 'Only teachers can view their class students');
    }

    const { classId } = req.params;

    try {
        // Verify class belongs to this teacher
        const classes = await query('SELECT id FROM classes WHERE id = ? AND teacher_id = ?', [classId, req.user.id]);
        if (classes.length === 0) {
            return apiResponse(res, 404, 'Class not found or access denied');
        }

        const students = await query(`
            SELECT u.id, u.email, u.name, ce.enrolled_at
            FROM users u
            JOIN class_enrollments ce ON u.id = ce.student_id
            WHERE ce.class_id = ?
            ORDER BY u.name ASC
        `, [classId]);

        apiResponse(res, 200, 'Students retrieved', students);
    } catch (error) {
        console.error('Error fetching students:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// Post school-wide announcement (School admin only)
app.post('/api/posts/school', authenticateToken, writeLimiter, async (req, res) => {
    if (req.user.role !== 'school_admin') {
        return apiResponse(res, 403, 'Only school admin can post school-wide announcements');
    }

    const { content, post_type } = req.body;

    if (!content) {
        return apiResponse(res, 400, 'Content is required');
    }

    try {
        const schools = await query('SELECT id FROM schools WHERE school_admin_id = ?', [req.user.id]);
        if (schools.length === 0) {
            return apiResponse(res, 404, 'School not found');
        }

        const school_id = schools[0].id;

        const result = await query(
            'INSERT INTO posts (author_id, school_id, content, post_type) VALUES (?, ?, ?, ?)',
            [req.user.id, school_id, content, post_type || 'announcement']
        );

        // Trigger AI calendar parsing
        // This will be implemented in Phase 5

        apiResponse(res, 201, 'Post created successfully', { id: result.insertId });
    } catch (error) {
        console.error('Error creating post:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// Post class announcement (Teacher only)
app.post('/api/posts/class', authenticateToken, writeLimiter, async (req, res) => {
    if (req.user.role !== 'teacher') {
        return apiResponse(res, 403, 'Only teachers can post class announcements');
    }

    const { class_id, content, post_type } = req.body;

    if (!class_id || !content) {
        return apiResponse(res, 400, 'Class ID and content are required');
    }

    try {
        // Verify class belongs to this teacher
        const classes = await query('SELECT id FROM classes WHERE id = ? AND teacher_id = ?', [class_id, req.user.id]);
        if (classes.length === 0) {
            return apiResponse(res, 404, 'Class not found or access denied');
        }

        const result = await query(
            'INSERT INTO posts (author_id, class_id, content, post_type) VALUES (?, ?, ?, ?)',
            [req.user.id, class_id, content, post_type || 'announcement']
        );

        // Trigger AI calendar parsing
        parsePostForCalendarEvents(result.insertId, content, class_id, req.user.id);

        apiResponse(res, 201, 'Post created successfully', { id: result.insertId });
    } catch (error) {
        console.error('Error creating post:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// Get posts for class
app.get('/api/posts/class/:classId', authenticateToken, async (req, res) => {
    const { classId } = req.params;

    try {
        // Verify user has access to this class
        if (req.user.role === 'teacher') {
            const classes = await query('SELECT id FROM classes WHERE id = ? AND teacher_id = ?', [classId, req.user.id]);
            if (classes.length === 0) {
                return apiResponse(res, 404, 'Class not found or access denied');
            }
        } else if (req.user.role === 'student') {
            const enrollments = await query('SELECT id FROM class_enrollments WHERE class_id = ? AND student_id = ?', [classId, req.user.id]);
            if (enrollments.length === 0) {
                return apiResponse(res, 404, 'Class not found or access denied');
            }
        } else {
            return apiResponse(res, 403, 'Access denied');
        }

        const posts = await query(`
            SELECT p.*, u.name as author_name
            FROM posts p
            JOIN users u ON p.author_id = u.id
            WHERE p.class_id = ?
            ORDER BY p.created_at DESC
        `, [classId]);

        apiResponse(res, 200, 'Posts retrieved', posts);
    } catch (error) {
        console.error('Error fetching posts:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// Get posts for school
app.get('/api/posts/school/:schoolId', authenticateToken, async (req, res) => {
    const { schoolId } = req.params;

    try {
        // Verify user belongs to this school
        const users = await query('SELECT school_id FROM users WHERE id = ?', [req.user.id]);
        if (users.length === 0 || users[0].school_id !== parseInt(schoolId)) {
            return apiResponse(res, 403, 'Access denied');
        }

        const posts = await query(`
            SELECT p.*, u.name as author_name
            FROM posts p
            JOIN users u ON p.author_id = u.id
            WHERE p.school_id = ?
            ORDER BY p.created_at DESC
        `, [schoolId]);

        apiResponse(res, 200, 'Posts retrieved', posts);
    } catch (error) {
        console.error('Error fetching posts:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// ===== EMS STUDENT ENDPOINTS =====

// Get student's classes
app.get('/api/student/my-classes', authenticateToken, async (req, res) => {
    if (req.user.role !== 'student') {
        return apiResponse(res, 403, 'Only students can view their classes');
    }

    try {
        const classes = await query(`
            SELECT c.*, u.name as teacher_name, u.email as teacher_email
            FROM classes c
            JOIN class_enrollments ce ON c.id = ce.class_id
            LEFT JOIN users u ON c.teacher_id = u.id
            WHERE ce.student_id = ?
            ORDER BY c.name ASC
        `, [req.user.id]);

        apiResponse(res, 200, 'Classes retrieved', classes);
    } catch (error) {
        console.error('Error fetching classes:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// Get student's parent code
app.get('/api/student/my-parent-code', authenticateToken, async (req, res) => {
    if (req.user.role !== 'student') {
        return apiResponse(res, 403, 'Only students can view their parent code');
    }

    try {
        const users = await query('SELECT parent_code, school_id FROM users WHERE id = ?', [req.user.id]);
        if (users.length === 0) {
            return apiResponse(res, 404, 'User not found');
        }

        apiResponse(res, 200, 'Parent code retrieved', { parent_code: users[0].parent_code, school_id: users[0].school_id });
    } catch (error) {
        console.error('Error fetching parent code:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// Get student's assignments
app.get('/api/student/my-assignments', authenticateToken, async (req, res) => {
    if (req.user.role !== 'student') {
        return apiResponse(res, 403, 'Only students can view their assignments');
    }

    try {
        const assignments = await query(`
            SELECT a.*, c.title as course_title, asub.completion_percentage, asub.correct_answers, asub.total_questions, asub.quiz_accuracy, asub.submitted_at
            FROM assignments a
            JOIN classes cl ON a.class_id = cl.id
            JOIN class_enrollments ce ON cl.id = ce.class_id
            JOIN courses c ON a.course_id = c.id
            LEFT JOIN assignment_submissions asub ON a.id = asub.assignment_id AND asub.student_id = ?
            WHERE ce.student_id = ?
            ORDER BY a.due_date ASC
        `, [req.user.id, req.user.id]);

        apiResponse(res, 200, 'Assignments retrieved', assignments);
    } catch (error) {
        console.error('Error fetching assignments:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// Submit assignment progress
app.post('/api/assignments/:assignmentId/submit', authenticateToken, writeLimiter, async (req, res) => {
    if (req.user.role !== 'student') {
        return apiResponse(res, 403, 'Only students can submit assignments');
    }

    const { assignmentId } = req.params;
    const { completion_percentage, score } = req.body;

    if (completion_percentage === undefined || score === undefined) {
        return apiResponse(res, 400, 'Completion percentage and score are required');
    }

    try {
        // Verify student is enrolled in the class for this assignment
        const assignments = await query(`
            SELECT a.id
            FROM assignments a
            JOIN class_enrollments ce ON a.class_id = ce.class_id
            WHERE a.id = ? AND ce.student_id = ?
        `, [assignmentId, req.user.id]);

        if (assignments.length === 0) {
            return apiResponse(res, 404, 'Assignment not found or access denied');
        }

        // Update or insert assignment progress
        await query(`
            INSERT INTO assignment_progress (assignment_id, student_id, completion_percentage, score, submitted_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON DUPLICATE KEY UPDATE
            completion_percentage = ?, score = ?, submitted_at = CURRENT_TIMESTAMP
        `, [assignmentId, req.user.id, completion_percentage, score, completion_percentage, score]);

        apiResponse(res, 200, 'Assignment progress updated successfully');
    } catch (error) {
        console.error('Error updating assignment progress:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// ===== EMS PARENT ENDPOINTS =====

// Get parent's linked children
app.get('/api/parent/my-children', authenticateToken, async (req, res) => {
    if (req.user.role !== 'parent') {
        return apiResponse(res, 403, 'Only parents can view their children');
    }

    try {
        const children = await query(`
            SELECT u.id, u.email, u.name, u.school_id, s.name as school_name
            FROM users u
            JOIN parent_student_links psl ON u.id = psl.student_id
            LEFT JOIN schools s ON u.school_id = s.id
            WHERE psl.parent_id = ?
            ORDER BY u.name ASC
        `, [req.user.id]);

        apiResponse(res, 200, 'Children retrieved', children);
    } catch (error) {
        console.error('Error fetching children:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// Link parent to additional student
app.post('/api/parent/link-student', authenticateToken, writeLimiter, async (req, res) => {
    if (req.user.role !== 'parent') {
        return apiResponse(res, 403, 'Only parents can link to students');
    }

    const { student_code } = req.body;

    if (!student_code) {
        return apiResponse(res, 400, 'Student code is required');
    }

    try {
        // Validate student code
        const students = await query('SELECT id FROM users WHERE parent_code = ? AND role = \'student\'', [student_code]);
        if (students.length === 0) {
            return apiResponse(res, 400, 'Invalid student code');
        }

        const student_id = students[0].id;

        // Check if already linked
        const existing = await query('SELECT id FROM parent_student_links WHERE parent_id = ? AND student_id = ?', [req.user.id, student_id]);
        if (existing.length > 0) {
            return apiResponse(res, 400, 'Already linked to this student');
        }

        await query('INSERT INTO parent_student_links (parent_id, student_id) VALUES (?, ?)', [req.user.id, student_id]);

        apiResponse(res, 201, 'Student linked successfully');
    } catch (error) {
        console.error('Error linking student:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// Get child's progress
app.get('/api/parent/child/:studentId/progress', authenticateToken, async (req, res) => {
    if (req.user.role !== 'parent') {
        return apiResponse(res, 403, 'Only parents can view child progress');
    }

    const { studentId } = req.params;

    try {
        // Verify parent is linked to this student
        const links = await query('SELECT id FROM parent_student_links WHERE parent_id = ? AND student_id = ?', [req.user.id, studentId]);
        if (links.length === 0) {
            return apiResponse(res, 403, 'Not linked to this student');
        }

        // Get child's classes
        const classes = await query(`
            SELECT c.*, u.name as teacher_name
            FROM classes c
            JOIN class_enrollments ce ON c.id = ce.class_id
            LEFT JOIN users u ON c.teacher_id = u.id
            WHERE ce.student_id = ?
            ORDER BY c.name ASC
        `, [studentId]);

        // Get child's assignments
        const assignments = await query(`
            SELECT a.*, c.title as course_title, asub.completion_percentage, asub.correct_answers, asub.total_questions, asub.quiz_accuracy, asub.submitted_at
            FROM assignments a
            JOIN classes cl ON a.class_id = cl.id
            JOIN class_enrollments ce ON cl.id = ce.class_id
            JOIN courses c ON a.course_id = c.id
            LEFT JOIN assignment_submissions asub ON a.id = asub.assignment_id AND asub.student_id = ?
            WHERE ce.student_id = ?
            ORDER BY a.due_date ASC
        `, [studentId, studentId]);

        // Get child's posts
        const posts = await query(`
            SELECT p.*, c.name as class_name
            FROM posts p
            JOIN classes c ON p.class_id = c.id
            JOIN class_enrollments ce ON c.id = ce.class_id
            WHERE ce.student_id = ?
            ORDER BY p.created_at DESC
            LIMIT 20
        `, [studentId]);

        apiResponse(res, 200, 'Child progress retrieved', { classes, assignments, posts });
    } catch (error) {
        console.error('Error fetching child progress:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// ===== EMS MESSAGING ENDPOINTS =====

// Send message
app.post('/api/messages/send', authenticateToken, writeLimiter, async (req, res) => {
    const { recipient_id, content, class_id } = req.body;

    if (!recipient_id || !content) {
        return apiResponse(res, 400, 'Recipient ID and content are required');
    }

    try {
        const result = await query(
            'INSERT INTO messages (sender_id, recipient_id, class_id, content) VALUES (?, ?, ?, ?)',
            [req.user.id, recipient_id, class_id || null, content]
        );

        apiResponse(res, 201, 'Message sent successfully', { id: result.insertId });
    } catch (error) {
        console.error('Error sending message:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// Get messages for user
app.get('/api/messages', authenticateToken, async (req, res) => {
    try {
        const messages = await query(`
            SELECT m.*,
                   sender.name as sender_name,
                   sender.role as sender_role,
                   recipient.name as recipient_name,
                   recipient.role as recipient_role
            FROM messages m
            JOIN users sender ON m.sender_id = sender.id
            JOIN users recipient ON m.recipient_id = recipient.id
            WHERE m.sender_id = ? OR m.recipient_id = ?
            ORDER BY m.created_at DESC
            LIMIT 50
        `, [req.user.id, req.user.id]);

        apiResponse(res, 200, 'Messages retrieved', messages);
    } catch (error) {
        console.error('Error fetching messages:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// Mark message as read
app.put('/api/messages/:messageId/read', authenticateToken, async (req, res) => {
    const { messageId } = req.params;

    try {
        // Verify message is for this user
        const messages = await query('SELECT id FROM messages WHERE id = ? AND recipient_id = ?', [messageId, req.user.id]);
        if (messages.length === 0) {
            return apiResponse(res, 404, 'Message not found or access denied');
        }

        await query('UPDATE messages SET is_read = TRUE WHERE id = ?', [messageId]);

        apiResponse(res, 200, 'Message marked as read');
    } catch (error) {
        console.error('Error marking message as read:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// ===== EMS ASSIGNMENT ENDPOINTS =====

// Create assignment (Teacher only)
app.post('/api/assignments', authenticateToken, writeLimiter, async (req, res) => {
    if (req.user.role !== 'teacher') {
        return apiResponse(res, 403, 'Only teachers can create assignments');
    }

    const { class_id, course_id, title, due_date } = req.body;

    if (!class_id || !course_id || !due_date) {
        return apiResponse(res, 400, 'Class ID, course ID, and due date are required');
    }

    try {
        // Verify class belongs to this teacher
        const classes = await query('SELECT id FROM classes WHERE id = ? AND teacher_id = ?', [class_id, req.user.id]);
        if (classes.length === 0) {
            return apiResponse(res, 404, 'Class not found or access denied');
        }

        // Get course title if not provided
        let assignmentTitle = title;
        if (!assignmentTitle) {
            const courses = await query('SELECT title FROM courses WHERE id = ?', [course_id]);
            if (courses.length > 0) {
                assignmentTitle = courses[0].title;
            } else {
                assignmentTitle = 'Assignment';
            }
        }

        const result = await query(
            'INSERT INTO assignments (class_id, course_id, teacher_id, title, due_date) VALUES (?, ?, ?, ?, ?)',
            [class_id, course_id, req.user.id, assignmentTitle, due_date]
        );

        // Create assignment progress records for all students in the class
        const students = await query('SELECT student_id FROM class_enrollments WHERE class_id = ?', [class_id]);
        for (const student of students) {
            await query(
                'INSERT INTO assignment_progress (assignment_id, student_id) VALUES (?, ?)',
                [result.insertId, student.student_id]
            );
        }

        apiResponse(res, 201, 'Assignment created successfully', { id: result.insertId });
    } catch (error) {
        console.error('Error creating assignment:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// Get assignment progress (Teacher only)
app.get('/api/assignments/:assignmentId/progress', authenticateToken, async (req, res) => {
    if (req.user.role !== 'teacher') {
        return apiResponse(res, 403, 'Only teachers can view assignment progress');
    }

    const { assignmentId } = req.params;

    try {
        // Verify assignment belongs to this teacher
        const assignments = await query('SELECT id, course_id FROM assignments WHERE id = ? AND teacher_id = ?', [assignmentId, req.user.id]);
        if (assignments.length === 0) {
            return apiResponse(res, 404, 'Assignment not found or access denied');
        }

        const assignment = assignments[0];
        const courseId = assignment.course_id;

        // Get total questions in the course
        const courseQuestions = await query('SELECT COUNT(*) as total FROM course_questions WHERE course_id = ?', [courseId]);
        const totalQuestions = courseQuestions[0].total || 1;

        const progress = await query(`
            SELECT asub.*, u.name as student_name, u.email as student_email
            FROM assignment_submissions asub
            JOIN users u ON asub.student_id = u.id
            WHERE asub.assignment_id = ?
            ORDER BY u.name ASC
        `, [assignmentId]);

        // Calculate percentage for each student
        const progressWithStats = progress.map(p => {
            const correctAnswers = p.correct_answers || 0;
            const totalAnswered = p.total_questions || 0;
            // Use quiz_accuracy from database or calculate it
            const percentage = p.quiz_accuracy || (totalAnswered > 0 ? Math.round((correctAnswers / totalAnswered) * 100) : 0);

            return {
                ...p,
                student_name: p.student_name,
                student_email: p.student_email,
                correct_answers: correctAnswers,
                total_questions: totalAnswered,
                total_possible: totalQuestions,
                percentage: percentage
            };
        });

        apiResponse(res, 200, 'Assignment progress retrieved', progressWithStats);
    } catch (error) {
        console.error('Error fetching assignment progress:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// Get teacher's assignments
app.get('/api/teacher/my-assignments', authenticateToken, async (req, res) => {
    if (req.user.role !== 'teacher') {
        return apiResponse(res, 403, 'Only teachers can view their assignments');
    }

    try {
        const assignments = await query(`
            SELECT a.*, c.name as class_name, co.title as course_title
            FROM assignments a
            JOIN classes c ON a.class_id = c.id
            JOIN courses co ON a.course_id = co.id
            WHERE a.teacher_id = ?
            ORDER BY a.due_date DESC
        `, [req.user.id]);

        apiResponse(res, 200, 'Assignments retrieved', assignments);
    } catch (error) {
        console.error('Error fetching assignments:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// ===== EMS CALENDAR ENDPOINTS =====

// Get calendar events for user
app.get('/api/calendar', authenticateToken, async (req, res) => {
    const { month, year } = req.query;

    try {
        let events = [];

        if (req.user.role === 'student') {
            // Get events from student's classes
            events = await query(`
                SELECT ce.*, c.name as class_name
                FROM calendar_events ce
                JOIN classes c ON ce.class_id = c.id
                JOIN class_enrollments ce2 ON c.id = ce2.class_id
                WHERE ce2.student_id = ?
                ${month && year ? 'AND MONTH(ce.event_date) = ? AND YEAR(ce.event_date) = ?' : ''}
                ORDER BY ce.event_date ASC
            `, month && year ? [req.user.id, month, year] : [req.user.id]);
        } else if (req.user.role === 'teacher') {
            // Get events from teacher's classes
            events = await query(`
                SELECT ce.*, c.name as class_name
                FROM calendar_events ce
                JOIN classes c ON ce.class_id = c.id
                WHERE c.teacher_id = ?
                ${month && year ? 'AND MONTH(ce.event_date) = ? AND YEAR(ce.event_date) = ?' : ''}
                ORDER BY ce.event_date ASC
            `, month && year ? [req.user.id, month, year] : [req.user.id]);
        } else if (req.user.role === 'parent') {
            // Get events from linked children's classes
            events = await query(`
                SELECT ce.*, c.name as class_name
                FROM calendar_events ce
                JOIN classes c ON ce.class_id = c.id
                JOIN class_enrollments ce2 ON c.id = ce2.class_id
                JOIN parent_student_links psl ON ce2.student_id = psl.student_id
                WHERE psl.parent_id = ?
                ${month && year ? 'AND MONTH(ce.event_date) = ? AND YEAR(ce.event_date) = ?' : ''}
                ORDER BY ce.event_date ASC
            `, month && year ? [req.user.id, month, year] : [req.user.id]);
        } else if (req.user.role === 'school_admin') {
            // Get events from school admin's school
            events = await query(`
                SELECT ce.*, c.name as class_name, s.name as school_name
                FROM calendar_events ce
                LEFT JOIN classes c ON ce.class_id = c.id
                LEFT JOIN schools s ON ce.school_id = s.id
                WHERE ce.school_id = (SELECT id FROM schools WHERE school_admin_id = ?)
                ${month && year ? 'AND MONTH(ce.event_date) = ? AND YEAR(ce.event_date) = ?' : ''}
                ORDER BY ce.event_date ASC
            `, month && year ? [req.user.id, month, year] : [req.user.id]);
        }

        apiResponse(res, 200, 'Calendar events retrieved', events);
    } catch (error) {
        console.error('Error fetching calendar events:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// Parse post content for calendar events (AI-powered)
app.post('/api/calendar/parse-post', authenticateToken, async (req, res) => {
    if (req.user.role !== 'teacher') {
        return apiResponse(res, 403, 'Only teachers can parse posts');
    }

    const { post_id } = req.body;

    if (!post_id) {
        return apiResponse(res, 400, 'Post ID is required');
    }

    try {
        // Get post details
        const posts = await query('SELECT content, class_id, author_id FROM posts WHERE id = ?', [post_id]);
        if (posts.length === 0) {
            return apiResponse(res, 404, 'Post not found');
        }

        const post = posts[0];

        // Verify post belongs to this teacher
        if (post.author_id !== req.user.id) {
            return apiResponse(res, 403, 'Access denied');
        }

        // Parse with AI
        await parsePostForCalendarEvents(post_id, post.content, post.class_id, post.author_id);

        // Get the created events
        const events = await query('SELECT * FROM calendar_events WHERE post_id = ?', [post_id]);

        apiResponse(res, 200, 'Calendar events parsed successfully', events);
    } catch (error) {
        console.error('Error parsing post:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// ===== FORGOT / RESET PASSWORD =====
const resetCodes = new Map(); // email -> { code, expiresAt }

app.post('/api/forgot-password', authLimiter, async (req, res) => {
    const { email } = req.body;

    if (!email) {
        return apiResponse(res, 400, 'Email is required');
    }
    if (!validateEmail(email)) {
        return apiResponse(res, 400, 'Invalid email format');
    }

    try {
        // Check if user exists (but don't reveal to client)
        const users = await query('SELECT id FROM users WHERE email = ?', [email]);

        if (users.length > 0) {
            // Generate 6-digit code
            const code = Math.floor(100000 + Math.random() * 900000).toString();
            const expiresAt = Date.now() + 10 * 60 * 1000; // 10 minutes

            resetCodes.set(email.toLowerCase(), { code, expiresAt });

            // Send email
            try {
                await sendEmail({
                    to: email,
                    subject: 'Veelearn - Password Reset Code',
                    html: `
                        <div style="font-family: Arial, sans-serif; max-width: 480px; margin: 0 auto; padding: 30px; background: #1a1a2e; color: #eee; border-radius: 10px;">
                            <h2 style="color: #667eea; text-align: center;">Veelearn Password Reset</h2>
                            <p>You requested a password reset. Use the code below to reset your password:</p>
                            <div style="text-align: center; margin: 25px 0;">
                                <span style="font-size: 32px; font-weight: bold; letter-spacing: 8px; color: #f093fb; background: rgba(102,126,234,0.2); padding: 12px 24px; border-radius: 8px;">${code}</span>
                            </div>
                            <p style="color: #999; font-size: 0.9em;">This code expires in <strong>10 minutes</strong>.</p>
                            <p style="color: #999; font-size: 0.9em;">If you didn't request this, please ignore this email.</p>
                            <hr style="border-color: #333; margin: 20px 0;">
                            <p style="color: #666; font-size: 0.8em; text-align: center;">&copy; 2026 Veelearn</p>
                        </div>
                    `
                });
                debug(`✓ Password reset code sent to ${email}`);
            } catch (emailErr) {
                console.error('❌ Failed to send reset email:', emailErr.message);
                return apiResponse(res, 500, 'Failed to send reset email. Please try again later.');
            }
        } else {
            debug(`⚠️ Password reset requested for non-existent email: ${email}`);
        }

        // Always return success (don't reveal if email exists)
        apiResponse(res, 200, 'If an account with that email exists, a reset code has been sent.');
    } catch (error) {
        console.error('Forgot password error:', error);
        apiResponse(res, 500, 'Server error');
    }
});

app.post('/api/reset-password', authLimiter, async (req, res) => {
    const { email, code, newPassword } = req.body;

    if (!email || !code || !newPassword) {
        return apiResponse(res, 400, 'Email, code, and new password are required');
    }

    if (!validatePassword(newPassword)) {
        return apiResponse(res, 400, 'Password must be at least 8 characters with uppercase, lowercase, and number');
    }

    const stored = resetCodes.get(email.toLowerCase());

    if (!stored) {
        return apiResponse(res, 400, 'No reset code found. Please request a new one.');
    }

    if (Date.now() > stored.expiresAt) {
        resetCodes.delete(email.toLowerCase());
        return apiResponse(res, 400, 'Reset code has expired. Please request a new one.');
    }

    if (stored.code !== code.trim()) {
        return apiResponse(res, 400, 'Invalid reset code');
    }

    try {
        const hashedPassword = await bcrypt.hash(newPassword, 10);
        await query('UPDATE users SET password = ? WHERE email = ?', [hashedPassword, email]);
        resetCodes.delete(email.toLowerCase());

        debug(`✓ Password reset successful for ${email}`);
        apiResponse(res, 200, 'Password reset successfully! You can now log in with your new password.');
    } catch (error) {
        console.error('Reset password error:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// ===== GLOBAL SEARCH ROUTE =====
app.get('/api/search', searchLimiter, async (req, res) => {
    try {
        const queryStr = String(req.query.q || '').trim();
        if (!queryStr) {
            return apiResponse(res, 200, 'Search results fetched successfully', {
                courses: [],
                simulators: []
            });
        }
        const searchPhrase = `%${queryStr}%`;
        const courses = await query(`
            SELECT c.id, c.title, c.description, c.course_type, c.grade_level, c.like_count,
                   c.status, c.created_at, u.email as creator_email, c.creator_id as user_id,
                   (SELECT COUNT(*) FROM course_units WHERE parent_course_id = c.id AND is_draft = FALSE) as units_count
            FROM courses c
            LEFT JOIN users u ON c.creator_id = u.id
            WHERE c.status = 'approved' AND (c.title LIKE ? OR c.description LIKE ?)
            ORDER BY
              CASE WHEN c.course_type = 'master' THEN 0 ELSE 1 END,
              c.like_count DESC,
              c.created_at DESC
            LIMIT 40
        `, [searchPhrase, searchPhrase]);

        const simulators = await query(`
            SELECT s.id, s.title, s.description, s.tags, s.downloads, s.rating, s.created_at,
                   s.is_public, u.email as creator_email,
                   (SELECT COUNT(*) FROM simulator_ratings sr WHERE sr.simulator_id = s.id) as like_count
            FROM simulators s
            LEFT JOIN users u ON s.creator_id = u.id
            WHERE (s.is_blocked IS NULL OR s.is_blocked = FALSE)
              AND (s.is_public = TRUE OR s.is_public IS NULL)
              AND (s.title LIKE ? OR s.description LIKE ? OR s.tags LIKE ?)
            ORDER BY s.downloads DESC, s.created_at DESC
            LIMIT 40
        `, [searchPhrase, searchPhrase, searchPhrase]);

        const coursesArr = Array.isArray(courses) ? courses : [];
        const simulatorsArr = Array.isArray(simulators) ? simulators : [];

        apiResponse(res, 200, 'Search results fetched successfully', {
            courses: coursesArr,
            simulators: simulatorsArr
        });
    } catch (error) {
        console.error('Search API error:', error);
        apiResponse(res, 500, 'Server error during search');
    }
});

// ===== USER ROUTES =====
app.get('/api/users/profile', authenticateToken, (req, res) => {
    const userId = req.user.id;

    db.query(
        'SELECT id, email, role, is_admin_approved, shells, created_at FROM users WHERE id = ?',
        [userId],
        (err, results) => {
            if (err) {
                console.error('Error fetching profile:', err);
                return apiResponse(res, 500, 'Server error');
            }
            if (results.length === 0) {
                return apiResponse(res, 404, 'User not found');
            }
            apiResponse(res, 200, 'Profile fetched successfully', results[0]);
        }
    );
});

// Get all users (admin/superadmin only)
// ===== SUPERADMIN ROUTES =====
app.get('/api/users', authenticateToken, authorize('superadmin', 'admin'), (req, res) => {
    db.query('SELECT id, email, role, is_admin_approved, shells, gems, total_volunteer_hours, is_verified_creator, created_at FROM users', (err, results) => {
        if (err) {
            console.error('Error fetching users:', err);
            return apiResponse(res, 500, 'Server error fetching users');
        }
        apiResponse(res, 200, 'Users fetched successfully', results);
    });
});

app.get('/api/superadmin/users', authenticateToken, authorize('superadmin', 'admin'), (req, res) => {
    db.query('SELECT id, email, role, is_admin_approved, shells, gems, total_volunteer_hours, is_verified_creator, created_at FROM users', (err, results) => {
        if (err) {
            console.error('Error fetching users:', err);
            return apiResponse(res, 500, 'Server error fetching users');
        }
        apiResponse(res, 200, 'Users fetched successfully', results);
    });
});

app.put('/api/users/:id/role', authenticateToken, authorize('superadmin'), (req, res) => {
    const userId = req.params.id;
    const { role, is_admin_approved } = req.body;

    const validRoles = ['user', 'admin', 'teacher', 'superadmin'];
    if (!validRoles.includes(role)) {
        return apiResponse(res, 400, 'Invalid role specified');
    }

    if (parseInt(userId) === req.user.id && role !== 'superadmin') {
        return apiResponse(res, 403, 'Superadmin cannot demote themselves');
    }

    db.query('SELECT role FROM users WHERE id = ?', [userId], (err, results) => {
        if (err) {
            console.error('Error fetching user role:', err);
            return apiResponse(res, 500, 'Server error');
        }
        if (results.length === 0) {
            return apiResponse(res, 404, 'User not found');
        }
        if (results[0].role === 'superadmin' && parseInt(userId) !== req.user.id) {
            return apiResponse(res, 403, 'Cannot modify another superadmin\'s role');
        }

        const updateQuery = 'UPDATE users SET role = ?, is_admin_approved = ? WHERE id = ?';
        db.query(updateQuery, [role, is_admin_approved || 0, userId], (err, result) => {
            if (err) {
                console.error('Error updating user role:', err);
                return apiResponse(res, 500, 'Server error updating user role');
            }
            if (result.affectedRows === 0) {
                return apiResponse(res, 404, 'User not found or no changes made');
            }
            apiResponse(res, 200, `User role updated to ${role}`);
        });
    });
});

// Change user role by email
app.put('/api/admin/users/:email/role', authenticateToken, authorize('superadmin', 'admin'), (req, res) => {
    const email = req.params.email;
    const { role } = req.body;

    const validRoles = ['user', 'admin', 'teacher', 'superadmin'];
    if (!validRoles.includes(role)) {
        return apiResponse(res, 400, 'Invalid role specified');
    }

    db.query('SELECT id, role FROM users WHERE email = ?', [email], (err, results) => {
        if (err) {
            console.error('Error fetching user:', err);
            return apiResponse(res, 500, 'Server error');
        }
        if (results.length === 0) {
            return apiResponse(res, 404, 'User not found');
        }

        const updateQuery = 'UPDATE users SET role = ? WHERE email = ?';
        db.query(updateQuery, [role, email], (err, result) => {
            if (err) {
                console.error('Error updating user role:', err);
                return apiResponse(res, 500, 'Server error updating user role');
            }
            apiResponse(res, 200, `User role updated to ${role}`);
        });
    });
});

// Also keep old endpoint for backwards compatibility
app.put('/api/superadmin/users/:id/role', authenticateToken, authorize('superadmin'), (req, res) => {
    const userId = req.params.id;
    const { role, is_admin_approved } = req.body;

    const validRoles = ['user', 'admin', 'teacher', 'superadmin'];
    if (!validRoles.includes(role)) {
        return apiResponse(res, 400, 'Invalid role specified');
    }

    if (parseInt(userId) === req.user.id && role !== 'superadmin') {
        return apiResponse(res, 403, 'Superadmin cannot demote themselves');
    }

    db.query('SELECT role FROM users WHERE id = ?', [userId], (err, results) => {
        if (err) {
            console.error('Error fetching user role:', err);
            return apiResponse(res, 500, 'Server error');
        }
        if (results.length === 0) {
            return apiResponse(res, 404, 'User not found');
        }
        if (results[0].role === 'superadmin' && parseInt(userId) !== req.user.id) {
            return apiResponse(res, 403, 'Cannot modify another superadmin\'s role');
        }

        const updateQuery = 'UPDATE users SET role = ?, is_admin_approved = ? WHERE id = ?';
        db.query(updateQuery, [role, is_admin_approved || 0, userId], (err, result) => {
            if (err) {
                console.error('Error updating user role:', err);
                return apiResponse(res, 500, 'Server error updating user role');
            }
            if (result.affectedRows === 0) {
                return apiResponse(res, 404, 'User not found or no changes made');
            }
            apiResponse(res, 200, `User role updated to ${role}`);
        });
    });
});

// ===== COURSE ROUTES =====
app.post('/api/courses', authenticateToken, writeLimiter, (req, res) => {
    const { title, description, content, blocks, status, creation_time, grade_level, video_url, course_type } = req.body;
    const creator_id = req.user.id;

    debug('📝 CREATE COURSE DEBUG:');
    debug('  User ID:', creator_id);
    debug('  Title:', title);
    debug('  Description:', description ? 'YES' : 'NO');
    debug('  Content length:', content ? content.length : 0, 'chars');
    debug('  Blocks count:', Array.isArray(blocks) ? blocks.length : 'NOT PROVIDED');
    debug('  Status:', status || 'draft');
    debug('  Grade Level:', grade_level || 'NOT PROVIDED');
    debug('  Course Type:', course_type || 'single');

    if (!title) {
        return apiResponse(res, 400, 'Course title is required');
    }

    if (title.length > 255) {
        return apiResponse(res, 400, 'Course title too long (max 255 characters)');
    }

    // Validate grade_level if provided
    if (grade_level !== undefined && grade_level !== null) {
        const gradeNum = parseInt(grade_level);
        if (isNaN(gradeNum) || gradeNum < 1 || gradeNum > 13) {
            return apiResponse(res, 400, 'Grade level must be an integer between 1 and 13 (13 = College)');
        }
    }

    // Use provided status or default to 'draft'
    const courseStatus = status || 'draft';
    const blocksJson = blocks ? (typeof blocks === 'string' ? blocks : JSON.stringify(blocks)) : '[]';

    const creationTime = parseInt(creation_time) || 0;
    const gradeLevelValue = grade_level !== undefined && grade_level !== null ? parseInt(grade_level) : null;
    debug('  Database:', dbConfig.database);
    debug('  Host:', dbConfig.host);

    const insertCourseQuery = 'INSERT INTO courses (title, description, content, blocks, creator_id, status, creation_time, grade_level, video_url, course_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)';
    db.query(insertCourseQuery, [title, description || '', content || '', blocksJson, creator_id, courseStatus, creationTime, gradeLevelValue, video_url || null, course_type || 'single'], (err, result) => {
        if (err) {
            console.error('❌ Error creating course:', err);
            return apiResponse(res, 500, 'Server error creating course', { details: err.message });
        }

        const newCourseId = result.insertId;
        debug('✅ Course created with ID:', newCourseId, 'Status:', courseStatus);

        // Auto-grant volunteer hours from tracked creation time
        if (creationTime > 0) {
            const addedHours = parseFloat((creationTime / 3600).toFixed(2));
            if (addedHours >= 0.01) {
                db.query(
                    'UPDATE users SET total_volunteer_hours = total_volunteer_hours + ? WHERE id = ?',
                    [addedHours, creator_id],
                    (volErr) => {
                        if (volErr) error('Error auto-granting volunteer hours:', volErr.message);
                        else debug(`✓ Auto-granted ${addedHours}h volunteer hours to user ${creator_id} from tracked time`);
                    }
                );
            }
        }

        // VERIFY the course was actually inserted
        debug('  Verifying course was inserted...');
        db.query('SELECT id, title FROM courses WHERE id = ?', [newCourseId], (verifyErr, verifyResults) => {
            if (verifyErr) {
                error('  ❌ Verification query failed:', verifyErr.message);
                return apiResponse(res, 500, 'Course created but verification failed', { details: verifyErr.message, id: newCourseId });
            }
            if (verifyResults.length === 0) {
                error('  ❌ CRITICAL: Course inserted but SELECT returned 0 rows!');
                debug('  Checking all courses:');
                db.query('SELECT COUNT(*) as count FROM courses', (countErr, countResults) => {
                    const count = countErr ? 'ERROR' : countResults[0].count;
                    debug('  Total courses in DB:', count);
                    apiResponse(res, 201, `Course created (ID: ${newCourseId}) but verification failed!`, { id: newCourseId, courseId: newCourseId });
                });
            } else {
                debug('  ✓ Verification successful - course exists in DB');
                apiResponse(res, 201, `Course created successfully with status: ${courseStatus}`, { id: newCourseId, courseId: newCourseId });
            }
        });
    });
});


// Get all courses in system for teacher assignment (with pagination/search/grade_level filter)
app.get('/api/courses/all', authenticateToken, (req, res) => {
    const { page = 1, limit = 10, search = '', grade_level } = req.query;
    const offset = (parseInt(page) - 1) * parseInt(limit);

    // Base query to get all approved courses + user's own courses
    const countQuery = `
        SELECT COUNT(*) as total FROM courses c
        LEFT JOIN users u ON c.creator_id = u.id
        WHERE (c.status = 'approved' OR c.creator_id = ?)
    ${search ? `AND (c.title LIKE ? OR c.description LIKE ?)` : ''}
    ${grade_level !== undefined && grade_level !== null ? `AND c.grade_level = ?` : ''}
`;

    const dataQuery = `
        SELECT c.id, c.title, c.description, c.creator_id, u.email as creator_email, c.status, c.created_at, c.grade_level
        FROM courses c
        LEFT JOIN users u ON c.creator_id = u.id
        WHERE (c.status = 'approved' OR c.creator_id = ?)
    ${search ? `AND (c.title LIKE ? OR c.description LIKE ?)` : ''}
    ${grade_level !== undefined && grade_level !== null ? `AND c.grade_level = ?` : ''}
        ORDER BY c.created_at DESC
LIMIT ? OFFSET ?
    `;

    const searchTerm = search ? `%${search}%` : null;
    const gradeNum = grade_level !== undefined && grade_level !== null ? parseInt(grade_level) : null;

    // Build parameter arrays dynamically
    const countParams = [];
    countParams.push(req.user.id);
    if (search) {
        countParams.push(searchTerm);
        countParams.push(searchTerm);
    }
    if (gradeNum !== null) {
        countParams.push(gradeNum);
    }

    const dataParams = [];
    dataParams.push(req.user.id);
    if (search) {
        dataParams.push(searchTerm);
        dataParams.push(searchTerm);
    }
    if (gradeNum !== null) {
        dataParams.push(gradeNum);
    }
    dataParams.push(parseInt(limit));
    dataParams.push(offset);

    db.query(countQuery, countParams, (err, countResults) => {
        if (err) return apiResponse(res, 500, 'Error fetching courses count');

        const total = countResults[0].total;

        db.query(dataQuery, dataParams, (err, courses) => {
            if (err) return apiResponse(res, 500, 'Error fetching courses');

            apiResponse(res, 200, 'All courses retrieved', {
                courses,
                pagination: {
                    page: parseInt(page),
                    limit: parseInt(limit),
                    total,
                    pages: Math.ceil(total / parseInt(limit))
                }
            });
        });
    });
});

// ===== COURSE NESTING SPECIFIC ROUTES (must be before /:id routes) =====

// Get course type
app.get('/api/courses/:id/type', authenticateToken, (req, res) => {
    const courseId = req.params.id;

    db.query('SELECT course_type FROM courses WHERE id = ?', [courseId], (err, results) => {
        if (err || results.length === 0) {
            return apiResponse(res, 404, 'Course not found');
        }
        apiResponse(res, 200, 'Course type fetched', { course_type: results[0].course_type || 'single' });
    });
});

// Toggle course type (single ↔ master)
app.put('/api/courses/:id/type', authenticateToken, (req, res) => {
    const courseId = req.params.id;
    const { course_type } = req.body;
    const userId = req.user.id;

    if (!['single', 'master'].includes(course_type)) {
        return apiResponse(res, 400, 'Invalid course type');
    }

    db.query('SELECT creator_id, course_type FROM courses WHERE id = ?', [courseId], (err, results) => {
        if (err || results.length === 0) {
            return apiResponse(res, 404, 'Course not found');
        }

        const course = results[0];
        if (course.creator_id !== userId) {
            return apiResponse(res, 403, 'Not authorized to modify this course');
        }

        db.query('UPDATE courses SET course_type = ? WHERE id = ?', [course_type, courseId], (err) => {
            if (err) {
                return apiResponse(res, 500, 'Server error updating course type');
            }
            apiResponse(res, 200, 'Course type updated successfully', { course_type });
        });
    });
});

// Get units of a master course
app.get('/api/courses/:id/units', authenticateToken, (req, res) => {
    const courseId = req.params.id;

    const query = `
        SELECT cu.id, cu.order_index, cu.is_draft, cu.prerequisite_unit_id,
               c.id as child_course_id, c.title, c.description, c.status, c.course_type,
               c2.title as prerequisite_title
        FROM course_units cu
        JOIN courses c ON cu.child_course_id = c.id
        LEFT JOIN course_units cu2 ON cu.prerequisite_unit_id = cu2.id
        LEFT JOIN courses c2 ON cu2.child_course_id = c2.id
        WHERE cu.parent_course_id = ?
        ORDER BY cu.order_index ASC
    `;

    db.query(query, [courseId], (err, results) => {
        if (err) {
            console.error('Error fetching course units:', err);
            return apiResponse(res, 500, 'Server error');
        }
        apiResponse(res, 200, 'Units fetched successfully', results);
    });
});

// Add unit to master course
app.post('/api/courses/:id/units', authenticateToken, (req, res) => {
    const parentCourseId = req.params.id;
    const { child_course_id, order_index, is_draft, prerequisite_unit_id } = req.body;
    const userId = req.user.id;

    db.query('SELECT creator_id, course_type FROM courses WHERE id = ?', [parentCourseId], (err, results) => {
        if (err || results.length === 0) {
            return apiResponse(res, 404, 'Parent course not found');
        }

        const parentCourse = results[0];
        if (parentCourse.creator_id !== userId) {
            return apiResponse(res, 403, 'Not authorized');
        }

        if (parentCourse.course_type !== 'master') {
            return apiResponse(res, 400, 'This course is not a Master Course. Convert it to Master first.');
        }

        if (!child_course_id) {
            return apiResponse(res, 400, 'Child course ID is required');
        }

        db.query('SELECT id, title FROM courses WHERE id = ?', [child_course_id], (childErr, childResults) => {
            if (childErr || childResults.length === 0) {
                return apiResponse(res, 404, 'Child course not found');
            }

            db.query('SELECT id FROM course_units WHERE parent_course_id = ? AND child_course_id = ?', 
                [parentCourseId, child_course_id], (existsErr, existsResults) => {
                if (existsErr) {
                    return apiResponse(res, 500, 'Server error');
                }

                if (existsResults.length > 0) {
                    return apiResponse(res, 400, 'This course is already a unit in this Master Course');
                }

                const getOrderIndex = (cb) => {
                    if (order_index !== undefined) {
                        return cb(order_index);
                    }
                    db.query('SELECT MAX(order_index) as max_order FROM course_units WHERE parent_course_id = ?', 
                        [parentCourseId], (maxErr, maxResults) => {
                        cb((maxResults[0].max_order || -1) + 1);
                    });
                };

                getOrderIndex((finalOrderIndex) => {
                    db.query(`
                        SELECT user_id, completed FROM enrollments WHERE course_id = ?
                    `, [child_course_id], (enrollErr, enrollments) => {
                        
                        db.query(`
                            INSERT INTO course_units (parent_course_id, child_course_id, order_index, is_draft, prerequisite_unit_id, linked_course_id)
                            VALUES (?, ?, ?, ?, ?, ?)
                        `, [parentCourseId, child_course_id, finalOrderIndex, is_draft || false, prerequisite_unit_id || null, child_course_id], 
                        (insertErr, insertResult) => {
                            if (insertErr) {
                                console.error('Error adding unit:', insertErr);
                                return apiResponse(res, 500, 'Server error adding unit');
                            }

                            const unitId = insertResult.insertId;

                            if (enrollments && enrollments.length > 0) {
                                const progressValues = enrollments.map(e => 
                                    `(${e.user_id}, ${parentCourseId}, ${unitId}, ${e.completed ? 'TRUE' : 'FALSE'}, ${e.completed ? 'CURRENT_TIMESTAMP' : 'NULL'})`
                                ).join(', ');

                                if (progressValues) {
                                    db.query(`
                                        INSERT INTO course_enrollment_progress (user_id, course_id, unit_id, completed, completed_at)
                                        VALUES ${progressValues}
                                        ON DUPLICATE KEY UPDATE completed = VALUES(completed), completed_at = VALUES(completed_at)
                                    `, [], (progressErr) => {
                                        if (progressErr) {
                                            console.error('Error carrying over progress:', progressErr);
                                        }
                                    });
                                }
                            }

                            apiResponse(res, 201, 'Unit added successfully', { 
                                unit_id: unitId,
                                child_course: childResults[0]
                            });
                        });
                    });
                });
            });
        });
    });
});

// Reorder units
app.put('/api/courses/:id/units/reorder', authenticateToken, (req, res) => {
    const courseId = req.params.id;
    const { unit_orders } = req.body;
    const userId = req.user.id;

    db.query('SELECT creator_id FROM courses WHERE id = ?', [courseId], (err, results) => {
        if (err || results.length === 0) {
            return apiResponse(res, 404, 'Course not found');
        }

        if (results[0].creator_id !== userId) {
            return apiResponse(res, 403, 'Not authorized');
        }

        if (!Array.isArray(unit_orders) || unit_orders.length === 0) {
            return apiResponse(res, 400, 'No units to reorder');
        }

        const updates = unit_orders.map((u) => {
            return new Promise((resolve) => {
                db.query('UPDATE course_units SET order_index = ? WHERE id = ? AND parent_course_id = ?', 
                    [u.order_index, u.unitId, courseId], (err) => {
                    resolve(err ? null : true);
                });
            });
        });

        Promise.all(updates).then(() => {
            apiResponse(res, 200, 'Units reordered successfully');
        }).catch(() => {
            apiResponse(res, 500, 'Error reordering units');
        });
    });
});

// Update unit
app.put('/api/courses/units/:unitId', authenticateToken, (req, res) => {
    const unitId = req.params.unitId;
    const { order_index, is_draft, prerequisite_unit_id } = req.body;
    const userId = req.user.id;

    db.query(`
        SELECT cu.*, c.creator_id 
        FROM course_units cu 
        JOIN courses c ON cu.parent_course_id = c.id 
        WHERE cu.id = ?
    `, [unitId], (err, results) => {
        if (err || results.length === 0) {
            return apiResponse(res, 404, 'Unit not found');
        }

        const unit = results[0];
        if (unit.creator_id !== userId) {
            return apiResponse(res, 403, 'Not authorized');
        }

        const updates = [];
        const params = [];

        if (order_index !== undefined) {
            updates.push('order_index = ?');
            params.push(order_index);
        }

        if (is_draft !== undefined) {
            updates.push('is_draft = ?');
            params.push(is_draft);
        }

        if (prerequisite_unit_id !== undefined) {
            updates.push('prerequisite_unit_id = ?');
            params.push(prerequisite_unit_id === 'null' ? null : prerequisite_unit_id);
        }

        if (updates.length === 0) {
            return apiResponse(res, 400, 'No valid fields to update');
        }

        params.push(unitId);

        db.query(`UPDATE course_units SET ${updates.join(', ')} WHERE id = ?`, params, (err) => {
            if (err) {
                return apiResponse(res, 500, 'Server error updating unit');
            }
            apiResponse(res, 200, 'Unit updated successfully');
        });
    });
});

// Delete unit
app.delete('/api/courses/units/:unitId', authenticateToken, (req, res) => {
    const unitId = req.params.unitId;
    const userId = req.user.id;

    db.query(`
        SELECT cu.*, c.creator_id 
        FROM course_units cu 
        JOIN courses c ON cu.parent_course_id = c.id 
        WHERE cu.id = ?
    `, [unitId], (err, results) => {
        if (err || results.length === 0) {
            return apiResponse(res, 404, 'Unit not found');
        }

        const unit = results[0];
        if (unit.creator_id !== userId) {
            return apiResponse(res, 403, 'Not authorized');
        }

        db.query('DELETE FROM course_units WHERE id = ?', [unitId], (err) => {
            if (err) {
                return apiResponse(res, 500, 'Server error removing unit');
            }
            apiResponse(res, 200, 'Unit removed successfully');
        });
    });
});

// Update unit progress
app.put('/api/courses/units/:unitId/progress', authenticateToken, (req, res) => {
    const unitId = req.params.unitId;
    const { progress_percentage } = req.body;
    const userId = req.user.id;

    db.query('SELECT parent_course_id, child_course_id FROM course_units WHERE id = ?', [unitId], (err, results) => {
        if (err || results.length === 0) {
            return apiResponse(res, 404, 'Unit not found');
        }

        const unit = results[0];

        db.query('SELECT id FROM enrollments WHERE user_id = ? AND course_id = ?', 
            [userId, unit.parent_course_id], (enrollErr, enrollResults) => {
            if (enrollErr || enrollResults.length === 0) {
                return apiResponse(res, 403, 'Not enrolled in this Master Course');
            }

            db.query(`
                INSERT INTO course_enrollment_progress (user_id, course_id, unit_id, progress_percentage)
                VALUES (?, ?, ?, ?)
                ON DUPLICATE KEY UPDATE progress_percentage = ?
            `, [userId, unit.parent_course_id, unitId, progress_percentage, progress_percentage], 
            (err) => {
                if (err) {
                    return apiResponse(res, 500, 'Server error updating progress');
                }
                apiResponse(res, 200, 'Progress updated successfully');
            });
        });
    });
});

// Mark unit as complete
app.post('/api/courses/units/:unitId/complete', authenticateToken, (req, res) => {
    const unitId = req.params.unitId;
    const userId = req.user.id;

    db.query('SELECT parent_course_id, prerequisite_unit_id, child_course_id FROM course_units WHERE id = ?', [unitId], (err, results) => {
        if (err || results.length === 0) {
            return apiResponse(res, 404, 'Unit not found');
        }

        const unit = results[0];

        if (unit.prerequisite_unit_id) {
            db.query(`
                SELECT completed FROM course_enrollment_progress 
                WHERE unit_id = ? AND user_id = ?
            `, [unit.prerequisite_unit_id, userId], (prereqErr, prereqResults) => {
                if (prereqErr || prereqResults.length === 0 || !prereqResults[0].completed) {
                    return apiResponse(res, 400, 'Complete the prerequisite unit first');
                }
                completeUnit();
            });
        } else {
            completeUnit();
        }

        function completeUnit() {
            db.query(`
                INSERT INTO course_enrollment_progress (user_id, course_id, unit_id, completed, completed_at)
                VALUES (?, ?, ?, TRUE, CURRENT_TIMESTAMP)
                ON DUPLICATE KEY UPDATE completed = TRUE, completed_at = CURRENT_TIMESTAMP
            `, [userId, unit.parent_course_id, unitId], (err) => {
                if (err) {
                    return apiResponse(res, 500, 'Server error completing unit');
                }

                db.query(`
                    INSERT INTO course_views (user_id, course_id, completed)
                    VALUES (?, ?, TRUE)
                    ON DUPLICATE KEY UPDATE completed = TRUE, last_viewed = CURRENT_TIMESTAMP
                `, [userId, unit.child_course_id], () => {});

                checkMasterComplete();
            });
        }

        function checkMasterComplete() {
            db.query(`
                SELECT COUNT(*) as total, 
                       SUM(CASE WHEN completed = TRUE THEN 1 ELSE 0 END) as completed
                FROM course_enrollment_progress
                WHERE user_id = ? AND course_id = ?
            `, [userId, unit.parent_course_id], (err, countResults) => {
                if (err) return;

                const { total, completed } = countResults[0];
                if (total > 0 && completed >= total) {
                    db.query(`
                        INSERT INTO course_views (user_id, course_id, completed)
                        VALUES (?, ?, TRUE)
                        ON DUPLICATE KEY UPDATE completed = TRUE, last_viewed = CURRENT_TIMESTAMP
                    `, [userId, unit.parent_course_id], () => {});
                }

                apiResponse(res, 200, 'Unit completed successfully', {
                    unit_complete: true,
                    all_units_complete: total > 0 && completed >= total
                });
            });
        }
    });
});

// Enroll in master course
app.post('/api/courses/:id/enroll-master', authenticateToken, (req, res) => {
    const courseId = req.params.id;
    const userId = req.user.id;

    db.query('SELECT id, title, course_type, is_paid, shells_cost FROM courses WHERE id = ? AND status = ?', 
        [courseId, 'approved'], (err, results) => {
        if (err || results.length === 0) {
            return apiResponse(res, 404, 'Course not found or not approved');
        }

        const course = results[0];

        if (course.course_type !== 'master') {
            return apiResponse(res, 400, 'This is not a Master Course. Use regular enrollment.');
        }

        db.query('SELECT id FROM enrollments WHERE user_id = ? AND course_id = ? AND is_master_enrollment = TRUE', 
            [userId, courseId], (err, enrolledResults) => {
            if (err || enrolledResults.length > 0) {
                return apiResponse(res, 400, 'Already enrolled in this Master Course');
            }

            db.query(`
                SELECT cu.id, cu.child_course_id, c.title
                FROM course_units cu
                JOIN courses c ON cu.child_course_id = c.id
                WHERE cu.parent_course_id = ? AND cu.is_draft = FALSE
                ORDER BY cu.order_index ASC
            `, [courseId], (err, units) => {
                if (err) {
                    return apiResponse(res, 500, 'Server error fetching units');
                }

                db.query('INSERT INTO enrollments (user_id, course_id, is_master_enrollment) VALUES (?, ?, TRUE)', 
                    [userId, courseId], (err) => {
                    if (err) {
                        return apiResponse(res, 500, 'Server error creating enrollment');
                    }

                    if (units && units.length > 0) {
                        const unitEnrollments = units.map(u => 
                            `(${userId}, ${u.child_course_id})`
                        ).join(', ');

                        db.query(`
                            INSERT IGNORE INTO enrollments (user_id, course_id) VALUES ${unitEnrollments}
                        `, [], (err) => {
                            if (err) {
                                console.error('Error creating unit enrollments:', err);
                            }

                            const progressValues = units.map(u => 
                                `(${userId}, ${courseId}, ${u.id}, 0)`
                            ).join(', ');

                            if (progressValues) {
                                db.query(`
                                    INSERT INTO course_enrollment_progress (user_id, course_id, unit_id, progress_percentage)
                                    VALUES ${progressValues}
                                `, [], (err) => {
                                    if (err) {
                                        console.error('Error initializing progress:', err);
                                    }
                                });
                            }
                        });
                    }

                    apiResponse(res, 201, 'Successfully enrolled in Master Course and all units', {
                        master_enrollment: true,
                        units_enrolled: units ? units.length : 0
                    });
                });
            });
        });
    });
});

// Get enrollment progress for master course (also accessible by creator for preview)
app.get('/api/users/enrollments/:courseId/progress', authenticateToken, (req, res) => {
    const courseId = req.params.courseId;
    const userId = req.user.id;

    // Allow creator access for preview, OR enrolled user access
    db.query(
        'SELECT id FROM enrollments WHERE user_id = ? AND course_id = ? UNION SELECT id FROM courses WHERE creator_id = ? AND id = ?',
        [userId, courseId, userId, courseId],
        (err, results) => {
        if (err || results.length === 0) {
            return apiResponse(res, 404, 'Not enrolled in this course and not the creator');
        }

        const query = `
            SELECT cu.id as unit_id, cu.order_index, cu.child_course_id,
                   c.title as unit_title,
                   cep.completed, cep.completed_at, cep.progress_percentage,
                   cu.prerequisite_unit_id,
                   CASE WHEN cep.completed = TRUE THEN TRUE 
                        WHEN cu.prerequisite_unit_id IS NULL THEN TRUE
                        ELSE EXISTS (
                            SELECT 1 FROM course_enrollment_progress cep2
                            WHERE cep2.unit_id = cu.prerequisite_unit_id
                            AND cep2.user_id = ?
                            AND cep2.completed = TRUE
                        )
                   END as is_unlocked
            FROM course_units cu
            JOIN courses c ON cu.child_course_id = c.id
            LEFT JOIN course_enrollment_progress cep ON cep.unit_id = cu.id AND cep.user_id = ?
            WHERE cu.parent_course_id = ? AND cu.is_draft = FALSE
            ORDER BY cu.order_index ASC
        `;

        db.query(query, [userId, userId, courseId], (err, units) => {
            if (err) {
                console.error('Error fetching unit progress:', err);
                return apiResponse(res, 500, 'Server error');
            }

            const completedCount = units.filter(u => u.completed).length;
            const totalUnits = units.length;
            const overallProgress = totalUnits > 0 ? Math.round((completedCount / totalUnits) * 100) : 0;
            const isComplete = totalUnits > 0 && completedCount === totalUnits;

            apiResponse(res, 200, 'Progress fetched successfully', {
                course_id: courseId,
                total_units: totalUnits,
                completed_units: completedCount,
                overall_progress: overallProgress,
                is_complete: isComplete,
                units: units
            });
        });
    });
});

// Get courses available for adding as units
app.get('/api/courses/available-for-units', authenticateToken, (req, res) => {
    const parentCourseId = req.query.exclude_parent;
    const userId = req.user.id;

    let query = `
        SELECT c.id, c.title, c.description, c.status, c.course_type, c.creator_id,
               u.email as creator_email
        FROM courses c
        JOIN users u ON c.creator_id = u.id
        WHERE c.status = 'approved' AND c.id != ?
    `;
    const params = [parentCourseId];

    query += ` OR c.creator_id = ?`;
    params.push(userId);

    query += ` ORDER BY c.created_at DESC LIMIT 100`;

    db.query(query, params, (err, results) => {
        if (err) {
            console.error('Error fetching available courses:', err);
            return apiResponse(res, 500, 'Server error');
        }
        apiResponse(res, 200, 'Available courses fetched', results);
    });
});

// Enhanced enrollments endpoint
app.get('/api/users/enrollments/enhanced', authenticateToken, (req, res) => {
    const userId = req.user.id;

    const query = `
        SELECT c.id, c.title, c.description, c.creator_id, c.course_type,
               e.enrolled_at, e.is_master_enrollment,
               cv.completed, cv.view_duration_hours,
               CASE 
                   WHEN cv.completed = TRUE THEN 'completed'
                   WHEN cv.view_duration_hours > 0 THEN 'in_progress'
                   ELSE 'enrolled'
               END as enrollment_status,
               CASE 
                   WHEN c.course_type = 'master' THEN (
                       SELECT COUNT(*) FROM course_units cu 
                       JOIN course_enrollment_progress cep ON cep.unit_id = cu.id 
                       WHERE cu.parent_course_id = c.id AND cep.user_id = e.user_id
                   )
                   ELSE NULL
               END as total_units,
               CASE 
                   WHEN c.course_type = 'master' THEN (
                       SELECT COUNT(*) FROM course_units cu 
                       JOIN course_enrollment_progress cep ON cep.unit_id = cu.id 
                       WHERE cu.parent_course_id = c.id AND cep.user_id = e.user_id AND cep.completed = TRUE
                   )
                   ELSE NULL
               END as completed_units
        FROM enrollments e
        JOIN courses c ON e.course_id = c.id
        LEFT JOIN course_views cv ON cv.user_id = e.user_id AND cv.course_id = c.id
        WHERE e.user_id = ?
        ORDER BY e.enrolled_at DESC
    `;

    db.query(query, [userId], (err, results) => {
        if (err) {
            console.error('Error fetching enhanced enrollments:', err);
            return apiResponse(res, 500, 'Server error');
        }
        apiResponse(res, 200, 'Enrollments fetched successfully', results);
    });
});

// ===== END COURSE NESTING SPECIFIC ROUTES =====

app.get('/api/courses/:id', authenticateToken, (req, res) => {
    const courseId = req.params.id;
    const userId = req.user.id;
    const userRole = req.user.role;

    debug('📖 GET COURSE DEBUG:');
    debug('  Course ID:', courseId);
    debug('  User ID:', userId);
    debug('  Database:', dbConfig.database);

    const query = `
        SELECT id, title, description, content, blocks, creator_id, status, is_paid, shells_cost, feedback, creation_time, grade_level, video_url, course_type
        FROM courses
        WHERE id = ?
    `;

    db.query(query, [courseId], (err, results) => {
        if (err) {
            console.error('❌ Error fetching single course:', err);
            return apiResponse(res, 500, 'Server error fetching course');
        }
        if (results.length === 0) {
            debug('  ❌ Course not found (query returned 0 results)');
            return apiResponse(res, 404, 'Course not found');
        }
        debug('  ✓ Course found:', results[0].title);

        const course = results[0];

        if (userRole === 'superadmin' || userRole === 'admin' || parseInt(course.creator_id) === parseInt(userId)) {
            return apiResponse(res, 200, 'Course fetched successfully', course);
        } else if (course.status === 'approved') {
            return apiResponse(res, 200, 'Course fetched successfully', course);
        } else {
            return apiResponse(res, 403, 'Access denied. You do not have permission to view this course');
        }
    });
});

// Update course
app.put('/api/courses/:id', authenticateToken, writeLimiter, (req, res) => {
    const courseId = req.params.id;
    const userId = req.user.id;
    const { title, description, content, blocks, status, creation_time, grade_level, video_url, course_type } = req.body;

    debug('📝 UPDATE COURSE DEBUG:');
    debug('  Course ID:', courseId);
    debug('  User ID:', userId);
    debug('  Title:', title);
    debug('  Content length:', content ? content.length : 0, 'chars');
    debug('  Blocks count:', Array.isArray(blocks) ? blocks.length : 'NOT PROVIDED');
    debug('  Status:', status || 'unchanged');
    debug('  Grade Level:', grade_level || 'unchanged');
    debug('  Course Type:', course_type || 'unchanged');
    debug('  Database:', dbConfig.database);
    debug('  Host:', dbConfig.host);

    if (!title) {
        return apiResponse(res, 400, 'Course title is required');
    }

    // Validate grade_level if provided
    if (grade_level !== undefined && grade_level !== null) {
        const gradeNum = parseInt(grade_level);
        if (isNaN(gradeNum) || gradeNum < 1 || gradeNum > 13) {
            return apiResponse(res, 400, 'Grade level must be an integer between 1 and 13 (13 = College)');
        }
    }

    // Check if course exists
    db.query('SELECT * FROM courses WHERE id = ?', [courseId], (err, results) => {
        if (err) {
            console.error('❌ Error fetching course:', err);
            console.error('  Full error:', err.message, err.code);
            return apiResponse(res, 500, 'Server error', { error: err.message });
        }
        if (results.length === 0) {
            debug('❌ Course not found in database. Query returned 0 results.');
            debug('  Querying all courses to debug:');
            db.query('SELECT id FROM courses LIMIT 5', (err2, allCourses) => {
                debug('  All courses in DB:', allCourses ? allCourses.map(c => c.id) : 'ERROR');
            });
            return apiResponse(res, 404, 'Course not found');
        }

        const course = results[0];
        debug('  Course found - creator_id:', course.creator_id, 'current user:', userId);
        if (parseInt(course.creator_id) !== parseInt(userId)) {
            debug('  ❌ Authorization failed - not course creator');
            return apiResponse(res, 403, 'You can only edit your own courses');
        }
        debug('  ✓ Authorization passed');

        // Prepare blocks JSON
        const blocksJson = blocks ? (typeof blocks === 'string' ? blocks : JSON.stringify(blocks)) : undefined;

        // Update with optional parameters
        let updateQuery = 'UPDATE courses SET title = ?, description = ?, content = ?';
        const params = [title, description || '', content || ''];

        if (blocksJson !== undefined) {
            updateQuery += ', blocks = ?';
            params.push(blocksJson);
        }

        if (status) {
            updateQuery += ', status = ?';
            params.push(status);
        }

        if (creation_time !== undefined) {
            updateQuery += ', creation_time = ?';
            params.push(parseInt(creation_time) || 0);
        }

        if (grade_level !== undefined && grade_level !== null) {
            updateQuery += ', grade_level = ?';
            params.push(parseInt(grade_level));
        }

        if (video_url !== undefined) {
            updateQuery += ', video_url = ?';
            params.push(video_url);
        }

        if (course_type !== undefined) {
            updateQuery += ', course_type = ?';
            params.push(course_type);
        }

        updateQuery += ' WHERE id = ?';
        params.push(courseId);

        db.query(updateQuery, params, (err, result) => {
            if (err) {
                console.error('❌ Error updating course:', err);
                return apiResponse(res, 500, 'Server error updating course', { details: err.message });
            }
            debug('✅ Course updated - ID:', courseId, 'Status:', status || 'unchanged');

            // Auto-grant volunteer hours from tracked creation time
            if (creation_time !== undefined) {
                const newSeconds = parseInt(creation_time) || 0;
                const oldSeconds = parseInt(course.creation_time) || 0;
                const addedSeconds = newSeconds - oldSeconds;
                if (addedSeconds > 0) {
                    const addedHours = parseFloat((addedSeconds / 3600).toFixed(2));
                    if (addedHours >= 0.01) {
                        db.query(
                            'UPDATE users SET total_volunteer_hours = total_volunteer_hours + ? WHERE id = ?',
                            [addedHours, userId],
                            (volErr) => {
                                if (volErr) console.error('Error auto-granting volunteer hours:', volErr.message);
                                else debug(`✓ Auto-granted ${addedHours}h volunteer hours to user ${userId} from tracked time`);
                            }
                        );
                    }
                }
            }

            apiResponse(res, 200, 'Course updated successfully');
        });
    });
});

// Delete course
app.delete('/api/courses/:id', authenticateToken, (req, res) => {
    const courseId = req.params.id;
    const userId = req.user.id;

    db.query('SELECT creator_id FROM courses WHERE id = ?', [courseId], (err, results) => {
        if (err) {
            console.error('Error fetching course:', err);
            return apiResponse(res, 500, 'Server error');
        }
        if (results.length === 0) {
            return apiResponse(res, 404, 'Course not found');
        }

        const course = results[0];
        debug(`DEBUG DELETE: Course ${courseId}, Creator: ${course.creator_id}, User: ${userId}, Role: ${req.user.role}`);

        if (parseInt(course.creator_id) !== parseInt(userId) && req.user.role !== 'superadmin' && req.user.role !== 'admin') {
            return apiResponse(res, 403, 'You can only delete your own courses');
        }

        db.query('DELETE FROM courses WHERE id = ?', [courseId], (err, result) => {
            if (err) {
                console.error('Error deleting course:', err);
                return apiResponse(res, 500, 'Server error deleting course');
            }
            apiResponse(res, 200, 'Course deleted successfully');
        });
    });
});

app.get('/api/courses', authenticateToken, (req, res) => {
    const userId = req.user.id;
    const sortBy = req.query.sort || 'newest'; // most_liked, newest, trending, popular
    const { grade_level } = req.query;

    // Determine ORDER BY clause based on sort parameter
    let orderByClause = 'c.created_at DESC'; // default newest
    if (sortBy === 'most_liked') {
        orderByClause = 'c.like_count DESC, c.created_at DESC';
    } else if (sortBy === 'trending') {
        orderByClause = '(c.like_count / DATEDIFF(NOW(), c.created_at) + 1) DESC, c.created_at DESC';
    } else if (sortBy === 'popular') {
        orderByClause = 'c.like_count DESC';
    }

    // Show approved courses from everyone + own courses (even if pending)
    let query = `
SELECT c.id, c.title, c.description, c.content, c.blocks, c.creator_id, c.status, c.is_paid, c.shells_cost, c.creation_time, c.grade_level, c.video_url,
       c.like_count, c.course_type, u.email as creator_email,
       CASE WHEN cl.user_id IS NOT NULL THEN true ELSE false END as is_liked,
       (SELECT COUNT(*) FROM course_units WHERE parent_course_id = c.id AND is_draft = FALSE) as units_count
FROM courses c
LEFT JOIN users u ON c.creator_id = u.id
LEFT JOIN course_likes cl ON c.id = cl.course_id AND cl.user_id = ?
WHERE (c.status = 'approved' OR c.creator_id = ?)
`;

    // Add grade_level filter if provided
    if (grade_level !== undefined && grade_level !== null) {
        query += `AND c.grade_level = ? `;
    }

    query += `ORDER BY ${orderByClause}`;

    const params = [userId, userId];
    if (grade_level !== undefined && grade_level !== null) {
        params.push(parseInt(grade_level));
    }

    db.query(query, params, (err, results) => {
        if (err) {
            console.error('Error fetching courses:', err);
            return apiResponse(res, 500, 'Server error fetching courses');
        }

        // Parse blocks JSON for each course
        const parsedResults = results.map(course => {
            if (course.blocks && typeof course.blocks === 'string') {
                try {
                    course.blocks = JSON.parse(course.blocks);
                } catch (e) {
                    console.error('Error parsing blocks for course', course.id, ':', e);
                    course.blocks = [];
                }
            } else if (!course.blocks) {
                course.blocks = [];
            }
            return course;
        });

        apiResponse(res, 200, 'Courses fetched successfully', parsedResults);
    });
});

// ===== COURSE LIKES ENDPOINTS =====

// POST /api/courses/:id/like - User likes a course
app.post('/api/courses/:id/like', authenticateToken, (req, res) => {
    const courseId = req.params.id;
    const userId = req.user.id;
    debug('✅ Like endpoint - User:', userId, 'Course:', courseId);

    // Insert like
    const insertQuery = 'INSERT INTO course_likes (course_id, user_id) VALUES (?, ?)';
    db.query(insertQuery, [courseId, userId], (err) => {
        if (err) {
            if (err.code === 'ER_DUP_ENTRY') {
                return apiResponse(res, 400, 'You have already liked this course');
            }
            console.error('Error liking course:', err);
            return apiResponse(res, 500, 'Server error liking course');
        }

        // Update like_count in courses table
        const updateQuery = 'UPDATE courses SET like_count = like_count + 1 WHERE id = ?';
        db.query(updateQuery, [courseId], (updateErr) => {
            if (updateErr) {
                console.error('Error updating like count:', updateErr);
                return apiResponse(res, 500, 'Server error updating like count');
            }

            apiResponse(res, 200, 'Course liked successfully', { liked: true });
        });
    });
});

// DELETE /api/courses/:id/like - User unlikes a course
app.delete('/api/courses/:id/like', authenticateToken, (req, res) => {
    const courseId = req.params.id;
    const userId = req.user.id;

    // Delete like
    const deleteQuery = 'DELETE FROM course_likes WHERE course_id = ? AND user_id = ?';
    db.query(deleteQuery, [courseId, userId], (err, results) => {
        if (err) {
            console.error('Error unliking course:', err);
            return apiResponse(res, 500, 'Server error unliking course');
        }

        if (results.affectedRows === 0) {
            return apiResponse(res, 400, 'You have not liked this course');
        }

        // Update like_count in courses table
        const updateQuery = 'UPDATE courses SET like_count = GREATEST(like_count - 1, 0) WHERE id = ?';
        db.query(updateQuery, [courseId], (updateErr) => {
            if (updateErr) {
                console.error('Error updating like count:', updateErr);
                return apiResponse(res, 500, 'Server error updating like count');
            }

            apiResponse(res, 200, 'Course unliked successfully', { liked: false });
        });
    });
});

// GET /api/courses/:id/likes - Get like count for a course
app.get('/api/courses/:id/likes', authenticateToken, (req, res) => {
    const courseId = req.params.id;

    const query = 'SELECT COUNT(*) as like_count FROM course_likes WHERE course_id = ?';
    db.query(query, [courseId], (err, results) => {
        if (err) {
            console.error('Error fetching like count:', err);
            return apiResponse(res, 500, 'Server error fetching like count');
        }

        const likeCount = results[0].like_count;
        apiResponse(res, 200, 'Like count fetched successfully', { like_count: likeCount });
    });
});

// GET /api/courses/:id/liked - Check if current user liked this course
app.get('/api/courses/:id/liked', authenticateToken, (req, res) => {
    const courseId = req.params.id;
    const userId = req.user.id;

    const query = 'SELECT id FROM course_likes WHERE course_id = ? AND user_id = ?';
    db.query(query, [courseId, userId], (err, results) => {
        if (err) {
            console.error('Error checking if course is liked:', err);
            return apiResponse(res, 500, 'Server error checking like status');
        }

        const isLiked = results.length > 0;
        apiResponse(res, 200, 'Like status fetched successfully', { is_liked: isLiked });
    });
});

app.get('/api/users/:userId/courses', authenticateToken, (req, res) => {
    const userId = req.params.userId;

    if (parseInt(req.user.id) !== parseInt(userId) && req.user.role !== 'admin' && req.user.role !== 'superadmin') {
        return apiResponse(res, 403, 'Access denied. You can only view your own courses');
    }

    const query = 'SELECT id, title, description, content, blocks, creator_id, status, is_paid, shells_cost, feedback, creation_time, grade_level, video_url FROM courses WHERE creator_id = ?';
    db.query(query, [userId], (err, results) => {
        if (err) {
            console.error('Error fetching user courses:', err);
            return apiResponse(res, 500, 'Server error fetching user courses');
        }

        // Parse blocks JSON for each course
        const parsedResults = results.map(course => {
            if (course.blocks) {
                try {
                    course.blocks = JSON.parse(course.blocks);
                } catch (e) {
                    console.error('Error parsing blocks for course', course.id, ':', e);
                    course.blocks = [];
                }
            } else {
                course.blocks = [];
            }
            return course;
        });

        apiResponse(res, 200, 'User courses fetched successfully', parsedResults);
    });
});

// ===== ADMIN ROUTES =====
app.get('/api/admin/courses/pending', authenticateToken, authorize('admin', 'superadmin'), (req, res) => {
    const query = "SELECT c.id, c.title, c.description, c.content, c.blocks, c.creator_id, u.email as creator_email, c.created_at, c.grade_level, c.video_url FROM courses c JOIN users u ON c.creator_id = u.id WHERE c.status = 'pending'";

    db.query(query, (err, results) => {
        if (err) {
            console.error('Error fetching pending courses:', err);
            return apiResponse(res, 500, 'Server error fetching pending courses');
        }
        apiResponse(res, 200, 'Pending courses fetched successfully', results);
    });
});

// Admin preview a pending course (with all content)
app.get('/api/admin/courses/:id/preview', authenticateToken, authorize('admin', 'superadmin'), (req, res) => {
    const courseId = req.params.id;

    const query = `
        SELECT c.id, c.title, c.description, c.content, c.blocks, c.creator_id, c.video_url,
               u.email as creator_email, c.status, c.created_at, c.feedback, c.grade_level
        FROM courses c
        JOIN users u ON c.creator_id = u.id
        WHERE c.id = ? AND c.status = 'pending'
    `;

    db.query(query, [courseId], (err, results) => {
        if (err) {
            console.error('Error fetching course preview:', err);
            return apiResponse(res, 500, 'Server error fetching course');
        }
        if (results.length === 0) {
            return apiResponse(res, 404, 'Course not found or is not pending approval');
        }

        const course = results[0];

        // Try to parse blocks JSON if it exists
        if (course.blocks) {
            try {
                course.blocks = JSON.parse(course.blocks);
            } catch (e) {
                console.error('Error parsing blocks JSON:', e);
                course.blocks = [];
            }
        } else {
            course.blocks = [];
        }

        apiResponse(res, 200, 'Course preview fetched successfully', course);
    });
});

app.put('/api/admin/courses/:id/status', authenticateToken, authorize('admin', 'superadmin'), (req, res) => {
    const courseId = req.params.id;
    const { status, feedback } = req.body;

    if (!['approved', 'rejected'].includes(status)) {
        return apiResponse(res, 400, 'Invalid status provided. Must be "approved" or "rejected"');
    }

    db.query('SELECT creator_id, status FROM courses WHERE id = ?', [courseId], (err, results) => {
        if (err) {
            console.error('Error fetching course for status update:', err);
            return apiResponse(res, 500, 'Server error');
        }
        if (results.length === 0) {
            return apiResponse(res, 404, 'Course not found');
        }

        const currentCourse = results[0];

        if (currentCourse.status !== 'pending') {
            return apiResponse(res, 400, `Course is already ${currentCourse.status}. Cannot change status from non-pending`);
        }

        const updateCourseQuery = 'UPDATE courses SET status = ?, feedback = ? WHERE id = ?';
        db.query(updateCourseQuery, [status, feedback, courseId], (err, result) => {
            if (err) {
                console.error('Error updating course status:', err);
                return apiResponse(res, 500, 'Server error updating course status');
            }

            if (status === 'approved') {
                const shellsAwarded = 100;
                const updateCreatorShellsQuery = 'UPDATE users SET shells = shells + ? WHERE id = ?';
                db.query(updateCreatorShellsQuery, [shellsAwarded, currentCourse.creator_id], (err) => {
                    if (err) {
                        console.error('Error awarding shells to creator:', err);
                    } else {
                        debug(`Awarded ${shellsAwarded} shells to user ${currentCourse.creator_id} for course approval.`);
                    }
                });
            }

            apiResponse(res, 200, `Course status updated to ${status}`);
        });
    });
});

// ===== COURSE RESUBMISSION =====
app.put('/api/courses/:id/resubmit', authenticateToken, (req, res) => {
    const courseId = req.params.id;
    const userId = req.user.id;
    const { title, description, content } = req.body;

    if (!title || !content) {
        return apiResponse(res, 400, 'Course title and content are required for resubmission');
    }

    db.query('SELECT creator_id, status FROM courses WHERE id = ?', [courseId], (err, results) => {
        if (err) {
            console.error('Error fetching course for resubmission:', err);
            return apiResponse(res, 500, 'Server error');
        }
        if (results.length === 0) {
            return apiResponse(res, 404, 'Course not found');
        }

        const course = results[0];

        if (parseInt(course.creator_id) !== parseInt(userId)) {
            return apiResponse(res, 403, 'Access denied. You are not the creator of this course');
        }

        if (course.status !== 'rejected') {
            return apiResponse(res, 400, 'Only rejected courses can be resubmitted');
        }

        const updateCourseQuery = "UPDATE courses SET title = ?, description = ?, content = ?, status = 'pending', feedback = NULL WHERE id = ?";
        db.query(updateCourseQuery, [title, description, content, courseId], (err, result) => {
            if (err) {
                console.error('Error resubmitting course:', err);
                return apiResponse(res, 500, 'Server error resubmitting course');
            }
            apiResponse(res, 200, 'Course resubmitted successfully and is awaiting admin approval');
        });
    });
});

// ===== COURSE ENROLLMENT & PURCHASE =====
app.post('/api/courses/:id/enroll', authenticateToken, (req, res) => {
    const courseId = req.params.id;
    const userId = req.user.id;

    // Check if course exists and is approved
    db.query('SELECT * FROM courses WHERE id = ? AND status = \'approved\'', [courseId], (err, courseResults) => {
        if (err) {
            console.error('Error fetching course:', err);
            return apiResponse(res, 500, 'Server error');
        }
        if (courseResults.length === 0) {
            return apiResponse(res, 404, 'Course not found or not approved');
        }

        const course = courseResults[0];

        // If it's a master course, redirect to enroll-master
        if (course.course_type === 'master') {
            return apiResponse(res, 400, 'This is a Master Course. Please use the Master Course enrollment endpoint.');
        }

        debug(`DEBUG ENROLL: Course found: ${course.title}, paid: ${course.is_paid}, cost: ${course.shells_cost}`);

        // Check if already enrolled
        db.query('SELECT * FROM enrollments WHERE user_id = ? AND course_id = ?', [userId, courseId], (err, enrollResults) => {
            if (err) {
                console.error('Error checking enrollment:', err);
                return apiResponse(res, 500, 'Server error');
            }
            if (enrollResults.length > 0) {
                return apiResponse(res, 400, 'Already enrolled in this course');
            }

            // If course is paid, check if user has enough shells
            if (course.is_paid) {
                db.query('SELECT shells FROM users WHERE id = ?', [userId], (err, userResults) => {
                    if (err) {
                        console.error('Error fetching user shells:', err);
                        return apiResponse(res, 500, 'Server error');
                    }

                    const userShells = userResults[0].shells;
                    if (userShells < course.shells_cost) {
                        return apiResponse(res, 400, `Insufficient shells. Required: ${course.shells_cost}, Available: ${userShells}`);
                    }

                    // Deduct shells and enroll
                    debug(`DEBUG ENROLL: Deducting ${course.shells_cost} shells from user ${userId}`);
                    db.query('UPDATE users SET shells = shells - ? WHERE id = ?', [course.shells_cost, userId], (err) => {
                        if (err) {
                            console.error('Error deducting shells:', err);
                            return apiResponse(res, 500, 'Server error');
                        }

                        // Add shells to course creator
                        db.query('UPDATE users SET shells = shells + ? WHERE id = ?', [course.shells_cost, course.creator_id], (err) => {
                            if (err) {
                                console.error('Error adding shells to creator:', err);
                            }
                        });

                        enrollUser();
                    });
                });
            } else {
                // Free course, just enroll
                enrollUser();
            }

            function enrollUser() {
                debug(`DEBUG ENROLL: Inserting enrollment for user ${userId}, course ${courseId}`);
                db.query('INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)', [userId, courseId], (err) => {
                    if (err) {
                        console.error('Error enrolling user:', err);
                        return apiResponse(res, 500, 'Server error enrolling in course');
                    }
                    debug(`DEBUG ENROLL: Successfully enrolled user ${userId}`);
                    apiResponse(res, 201, 'Successfully enrolled in course');
                });
            }
        });
    });
});

// Get enrolled courses
app.get('/api/users/enrollments', authenticateToken, (req, res) => {
    const userId = req.user.id;

    const query = `
        SELECT c.id, c.title, c.description, c.creator_id, e.enrolled_at,
               cv.completed, cv.view_duration_hours
        FROM enrollments e
        JOIN courses c ON e.course_id = c.id
        LEFT JOIN course_views cv ON cv.user_id = e.user_id AND cv.course_id = c.id
        WHERE e.user_id = ?
        ORDER BY e.enrolled_at DESC
    `;

    db.query(query, [userId], (err, results) => {
        if (err) {
            console.error('Error fetching enrollments:', err);
            return apiResponse(res, 500, 'Server error');
        }
        apiResponse(res, 200, 'Enrollments fetched successfully', results);
    });
});

// Mark course as complete
app.post('/api/courses/:id/complete', authenticateToken, (req, res) => {
    const courseId = req.params.id;
    const userId = req.user.id;

    const query = `
        INSERT INTO course_views (user_id, course_id, completed)
        VALUES (?, ?, TRUE)
        ON DUPLICATE KEY UPDATE completed = TRUE, last_viewed = CURRENT_TIMESTAMP
    `;

    db.query(query, [userId, courseId], (err) => {
        if (err) {
            console.error('Error marking course complete:', err);
            return apiResponse(res, 500, 'Server error');
        }
        apiResponse(res, 200, 'Course marked as completed');
    });
});

// ===== SIMULATOR MARKETPLACE ROUTES =====
app.put('/api/courses/:id/type', authenticateToken, (req, res) => {
    const courseId = req.params.id;
    const { course_type } = req.body;
    const userId = req.user.id;

    if (!['single', 'master'].includes(course_type)) {
        return apiResponse(res, 400, 'Invalid course type');
    }

    // First verify ownership
    db.query('SELECT creator_id, course_type FROM courses WHERE id = ?', [courseId], (err, results) => {
        if (err || results.length === 0) {
            return apiResponse(res, 404, 'Course not found');
        }

        const course = results[0];
        if (course.creator_id !== userId) {
            return apiResponse(res, 403, 'Not authorized to modify this course');
        }

        const oldType = course.course_type || 'single';

        // If converting from master to single, warn about detaching units
        if (oldType === 'master' && course_type === 'single') {
            // Check if there are units - if so, they'll be detached
            db.query('SELECT COUNT(*) as count FROM course_units WHERE parent_course_id = ?', [courseId], (countErr, countResults) => {
                if (countErr) {
                    return apiResponse(res, 500, 'Server error');
                }

                const hasUnits = countResults[0].count > 0;

                // Update course type
                db.query('UPDATE courses SET course_type = ? WHERE id = ?', [course_type, courseId], (updateErr) => {
                    if (updateErr) {
                        return apiResponse(res, 500, 'Server error updating course type');
                    }

                    // If there were units, detach them (delete unit associations but keep courses)
                    if (hasUnits) {
                        db.query('DELETE FROM course_units WHERE parent_course_id = ?', [courseId], (deleteErr) => {
                            if (deleteErr) {
                                console.error('Error detaching units:', deleteErr);
                            }
                            apiResponse(res, 200, 'Course converted to single-module. Units have been detached.', { 
                                course_type, 
                                units_detached: true 
                            });
                        });
                    } else {
                        apiResponse(res, 200, 'Course type updated successfully', { course_type });
                    }
                });
            });
        } else {
            // Simple type update
            db.query('UPDATE courses SET course_type = ? WHERE id = ?', [course_type, courseId], (err) => {
                if (err) {
                    return apiResponse(res, 500, 'Server error updating course type');
                }
                apiResponse(res, 200, 'Course type updated successfully', { course_type });
            });
        }
    });
});

// Get course type
app.get('/api/courses/:id/type', authenticateToken, (req, res) => {
    const courseId = req.params.id;

    db.query('SELECT course_type FROM courses WHERE id = ?', [courseId], (err, results) => {
        if (err || results.length === 0) {
            return apiResponse(res, 404, 'Course not found');
        }
        apiResponse(res, 200, 'Course type fetched', { course_type: results[0].course_type || 'single' });
    });
});

// Get units of a master course
app.get('/api/courses/:id/units', authenticateToken, (req, res) => {
    const courseId = req.params.id;

    const query = `
        SELECT cu.id, cu.order_index, cu.is_draft, cu.prerequisite_unit_id,
               c.id as child_course_id, c.title, c.description, c.status, c.course_type,
               c2.title as prerequisite_title
        FROM course_units cu
        JOIN courses c ON cu.child_course_id = c.id
        LEFT JOIN course_units cu2 ON cu.prerequisite_unit_id = cu2.id
        LEFT JOIN courses c2 ON cu2.child_course_id = c2.id
        WHERE cu.parent_course_id = ?
        ORDER BY cu.order_index ASC
    `;

    db.query(query, [courseId], (err, results) => {
        if (err) {
            console.error('Error fetching course units:', err);
            return apiResponse(res, 500, 'Server error');
        }
        apiResponse(res, 200, 'Units fetched successfully', results);
    });
});

// Add unit to master course
app.post('/api/courses/:id/units', authenticateToken, (req, res) => {
    const parentCourseId = req.params.id;
    const { child_course_id, order_index, is_draft, prerequisite_unit_id } = req.body;
    const userId = req.user.id;

    // Verify parent course exists and user owns it
    db.query('SELECT creator_id, course_type FROM courses WHERE id = ?', [parentCourseId], (err, results) => {
        if (err || results.length === 0) {
            return apiResponse(res, 404, 'Parent course not found');
        }

        const parentCourse = results[0];
        if (parentCourse.creator_id !== userId) {
            return apiResponse(res, 403, 'Not authorized');
        }

        if (parentCourse.course_type !== 'master') {
            return apiResponse(res, 400, 'This course is not a Master Course. Convert it to Master first.');
        }

        if (!child_course_id) {
            return apiResponse(res, 400, 'Child course ID is required');
        }

        // Verify child course exists
        db.query('SELECT id, title FROM courses WHERE id = ?', [child_course_id], (childErr, childResults) => {
            if (childErr || childResults.length === 0) {
                return apiResponse(res, 404, 'Child course not found');
            }

            // Check if already a unit
            db.query('SELECT id FROM course_units WHERE parent_course_id = ? AND child_course_id = ?', 
                [parentCourseId, child_course_id], (existsErr, existsResults) => {
                if (existsErr) {
                    return apiResponse(res, 500, 'Server error');
                }

                if (existsResults.length > 0) {
                    return apiResponse(res, 400, 'This course is already a unit in this Master Course');
                }

                // Get next order index if not provided
                const getOrderIndex = (cb) => {
                    if (order_index !== undefined) {
                        return cb(order_index);
                    }
                    db.query('SELECT MAX(order_index) as max_order FROM course_units WHERE parent_course_id = ?', 
                        [parentCourseId], (maxErr, maxResults) => {
                        cb((maxResults[0].max_order || -1) + 1);
                    });
                };

                getOrderIndex((finalOrderIndex) => {
                    // Check for progress carry-over: if child course has existing enrollments
                    db.query(`
                        SELECT user_id, completed FROM enrollments 
                        WHERE course_id = ?
                    `, [child_course_id], (enrollErr, enrollments) => {
                        
                        // Insert unit
                        db.query(`
                            INSERT INTO course_units (parent_course_id, child_course_id, order_index, is_draft, prerequisite_unit_id, linked_course_id)
                            VALUES (?, ?, ?, ?, ?, ?)
                        `, [parentCourseId, child_course_id, finalOrderIndex, is_draft || false, prerequisite_unit_id || null, child_course_id], 
                        (insertErr, insertResult) => {
                            if (insertErr) {
                                console.error('Error adding unit:', insertErr);
                                return apiResponse(res, 500, 'Server error adding unit');
                            }

                            const unitId = insertResult.insertId;

                            // Carry over progress from existing enrollments
                            if (enrollments && enrollments.length > 0) {
                                const progressValues = enrollments.map(e => 
                                    `(${e.user_id}, ${parentCourseId}, ${unitId}, ${e.completed ? 'TRUE' : 'FALSE'}, ${e.completed ? 'CURRENT_TIMESTAMP' : 'NULL'})`
                                ).join(', ');

                                if (progressValues) {
                                    db.query(`
                                        INSERT INTO course_enrollment_progress (user_id, course_id, unit_id, completed, completed_at)
                                        VALUES ${progressValues}
                                        ON DUPLICATE KEY UPDATE completed = VALUES(completed), completed_at = VALUES(completed_at)
                                    `, [], (progressErr) => {
                                        if (progressErr) {
                                            console.error('Error carrying over progress:', progressErr);
                                        }
                                    });
                                }
                            }

                            apiResponse(res, 201, 'Unit added successfully', { 
                                unit_id: unitId,
                                child_course: childResults[0]
                            });
                        });
                    });
                });
            });
        });
    });
});

// Update unit (order, draft, prerequisite)
app.put('/api/courses/units/:unitId', authenticateToken, (req, res) => {
    const unitId = req.params.unitId;
    const { order_index, is_draft, prerequisite_unit_id } = req.body;
    const userId = req.user.id;

    // Get the unit and verify ownership
    db.query(`
        SELECT cu.*, c.creator_id 
        FROM course_units cu 
        JOIN courses c ON cu.parent_course_id = c.id 
        WHERE cu.id = ?
    `, [unitId], (err, results) => {
        if (err || results.length === 0) {
            return apiResponse(res, 404, 'Unit not found');
        }

        const unit = results[0];
        if (unit.creator_id !== userId) {
            return apiResponse(res, 403, 'Not authorized');
        }

        // Build update query dynamically
        const updates = [];
        const params = [];

        if (order_index !== undefined) {
            updates.push('order_index = ?');
            params.push(order_index);
        }

        if (is_draft !== undefined) {
            updates.push('is_draft = ?');
            params.push(is_draft);
        }

        if (prerequisite_unit_id !== undefined) {
            updates.push('prerequisite_unit_id = ?');
            params.push(prerequisite_unit_id === 'null' ? null : prerequisite_unit_id);
        }

        if (updates.length === 0) {
            return apiResponse(res, 400, 'No valid fields to update');
        }

        params.push(unitId);

        db.query(`UPDATE course_units SET ${updates.join(', ')} WHERE id = ?`, params, (updateErr) => {
            if (updateErr) {
                return apiResponse(res, 500, 'Server error updating unit');
            }
            apiResponse(res, 200, 'Unit updated successfully');
        });
    });
});

// Delete/remove unit from master course
app.delete('/api/courses/units/:unitId', authenticateToken, (req, res) => {
    const unitId = req.params.unitId;
    const userId = req.user.id;

    // Get the unit and verify ownership
    db.query(`
        SELECT cu.*, c.creator_id 
        FROM course_units cu 
        JOIN courses c ON cu.parent_course_id = c.id 
        WHERE cu.id = ?
    `, [unitId], (err, results) => {
        if (err || results.length === 0) {
            return apiResponse(res, 404, 'Unit not found');
        }

        const unit = results[0];
        if (unit.creator_id !== userId) {
            return apiResponse(res, 403, 'Not authorized');
        }

        // Delete the unit
        db.query('DELETE FROM course_units WHERE id = ?', [unitId], (deleteErr) => {
            if (deleteErr) {
                return apiResponse(res, 500, 'Server error removing unit');
            }
            apiResponse(res, 200, 'Unit removed successfully');
        });
    });
});

// Reorder units (bulk update)
app.put('/api/courses/:id/units/reorder', authenticateToken, (req, res) => {
    const courseId = req.params.id;
    const { unit_orders } = req.body; // Array of { unitId, order_index }
    const userId = req.user.id;

    // Verify ownership
    db.query('SELECT creator_id FROM courses WHERE id = ?', [courseId], (err, results) => {
        if (err || results.length === 0) {
            return apiResponse(res, 404, 'Course not found');
        }

        if (results[0].creator_id !== userId) {
            return apiResponse(res, 403, 'Not authorized');
        }

        if (!Array.isArray(unit_orders) || unit_orders.length === 0) {
            return apiResponse(res, 400, 'No units to reorder');
        }

        // Update each unit's order
        const updates = unit_orders.map((u, index) => {
            return new Promise((resolve) => {
                db.query('UPDATE course_units SET order_index = ? WHERE id = ? AND parent_course_id = ?', 
                    [u.order_index, u.unitId, courseId], (err) => {
                    resolve(err ? null : true);
                });
            });
        });

        Promise.all(updates).then(() => {
            apiResponse(res, 200, 'Units reordered successfully');
        }).catch(() => {
            apiResponse(res, 500, 'Error reordering units');
        });
    });
});

// Enroll in master course (auto-enrolls in all units)
app.post('/api/courses/:id/enroll-master', authenticateToken, (req, res) => {
    const courseId = req.params.id;
    const userId = req.user.id;

    // Verify course exists and is a master course
    db.query('SELECT id, title, course_type, is_paid, shells_cost FROM courses WHERE id = ? AND status = ?', 
        [courseId, 'approved'], (err, results) => {
        if (err || results.length === 0) {
            return apiResponse(res, 404, 'Course not found or not approved');
        }

        const course = results[0];

        if (course.course_type !== 'master') {
            return apiResponse(res, 400, 'This is not a Master Course. Use regular enrollment.');
        }

        // Check if already enrolled in master
        db.query('SELECT id FROM enrollments WHERE user_id = ? AND course_id = ? AND is_master_enrollment = TRUE', 
            [userId, courseId], (enrolledErr, enrolledResults) => {
            if (enrolledErr) {
                return apiResponse(res, 500, 'Server error');
            }

            if (enrolledResults.length > 0) {
                return apiResponse(res, 400, 'Already enrolled in this Master Course');
            }

            // Get all units
            db.query(`
                SELECT cu.id, cu.child_course_id, c.title
                FROM course_units cu
                JOIN courses c ON cu.child_course_id = c.id
                WHERE cu.parent_course_id = ? AND cu.is_draft = FALSE
                ORDER BY cu.order_index ASC
            `, [courseId], (unitsErr, units) => {
                if (unitsErr) {
                    return apiResponse(res, 500, 'Server error fetching units');
                }

                // Create master enrollment
                db.query('INSERT INTO enrollments (user_id, course_id, is_master_enrollment) VALUES (?, ?, TRUE)', 
                    [userId, courseId], (masterErr) => {
                    if (masterErr) {
                        return apiResponse(res, 500, 'Server error creating enrollment');
                    }

                    // Create unit enrollments
                    if (units && units.length > 0) {
                        const unitEnrollments = units.map(u => 
                            `(${userId}, ${u.child_course_id})`
                        ).join(', ');

                        db.query(`
                            INSERT IGNORE INTO enrollments (user_id, course_id) VALUES ${unitEnrollments}
                        `, [], (unitErr) => {
                            if (unitErr) {
                                console.error('Error creating unit enrollments:', unitErr);
                            }

                            // Initialize progress for each unit
                            const progressValues = units.map(u => 
                                `(${userId}, ${courseId}, ${u.id}, 0)`
                            ).join(', ');

                            if (progressValues) {
                                db.query(`
                                    INSERT INTO course_enrollment_progress (user_id, course_id, unit_id, progress_percentage)
                                    VALUES ${progressValues}
                                `, [], (progressErr) => {
                                    if (progressErr) {
                                        console.error('Error initializing progress:', progressErr);
                                    }
                                });
                            }
                        });
                    }

                    apiResponse(res, 201, 'Successfully enrolled in Master Course and all units', {
                        master_enrollment: true,
                        units_enrolled: units ? units.length : 0
                    });
                });
            });
        });
    });
});

// Get enrollment progress for master course
app.get('/api/users/enrollments/:courseId/progress', authenticateToken, (req, res) => {
    const courseId = req.params.courseId;
    const userId = req.user.id;

    // Get master enrollment
    db.query('SELECT id FROM enrollments WHERE user_id = ? AND course_id = ?', 
        [userId, courseId], (err, results) => {
        if (err || results.length === 0) {
            return apiResponse(res, 404, 'Not enrolled in this course');
        }

        // Get all units with progress
        const query = `
            SELECT cu.id as unit_id, cu.order_index, cu.child_course_id,
                   c.title as unit_title,
                   cep.completed, cep.completed_at, cep.progress_percentage,
                   cu.prerequisite_unit_id,
                   CASE WHEN cep.completed = TRUE THEN TRUE 
                        WHEN cu.prerequisite_unit_id IS NULL THEN TRUE
                        ELSE EXISTS (
                            SELECT 1 FROM course_enrollment_progress cep2
                            WHERE cep2.unit_id = cu.prerequisite_unit_id
                            AND cep2.user_id = ?
                            AND cep2.completed = TRUE
                        )
                   END as is_unlocked
            FROM course_units cu
            JOIN courses c ON cu.child_course_id = c.id
            LEFT JOIN course_enrollment_progress cep ON cep.unit_id = cu.id AND cep.user_id = ?
            WHERE cu.parent_course_id = ? AND cu.is_draft = FALSE
            ORDER BY cu.order_index ASC
        `;

        db.query(query, [userId, userId, courseId], (unitErr, units) => {
            if (unitErr) {
                console.error('Error fetching unit progress:', unitErr);
                return apiResponse(res, 500, 'Server error');
            }

            const completedCount = units.filter(u => u.completed).length;
            const totalUnits = units.length;
            const overallProgress = totalUnits > 0 ? Math.round((completedCount / totalUnits) * 100) : 0;
            const isComplete = totalUnits > 0 && completedCount === totalUnits;

            apiResponse(res, 200, 'Progress fetched successfully', {
                course_id: courseId,
                total_units: totalUnits,
                completed_units: completedCount,
                overall_progress: overallProgress,
                is_complete: isComplete,
                units: units
            });
        });
    });
});

// Update unit progress
app.put('/api/courses/units/:unitId/progress', authenticateToken, (req, res) => {
    const unitId = req.params.unitId;
    const { progress_percentage } = req.body;
    const userId = req.user.id;

    // Get unit info
    db.query('SELECT parent_course_id, child_course_id FROM course_units WHERE id = ?', 
        [unitId], (err, results) => {
        if (err || results.length === 0) {
            return apiResponse(res, 404, 'Unit not found');
        }

        const unit = results[0];

        // Verify user is enrolled
        db.query('SELECT id FROM enrollments WHERE user_id = ? AND course_id = ?', 
            [userId, unit.parent_course_id], (enrollErr, enrollResults) => {
            if (enrollErr || enrollResults.length === 0) {
                return apiResponse(res, 403, 'Not enrolled in this Master Course');
            }

            // Update progress
            db.query(`
                INSERT INTO course_enrollment_progress (user_id, course_id, unit_id, progress_percentage)
                VALUES (?, ?, ?, ?)
                ON DUPLICATE KEY UPDATE progress_percentage = ?
            `, [userId, unit.parent_course_id, unitId, progress_percentage, progress_percentage], 
            (updateErr) => {
                if (updateErr) {
                    return apiResponse(res, 500, 'Server error updating progress');
                }
                apiResponse(res, 200, 'Progress updated successfully');
            });
        });
    });
});

// Mark unit as complete
app.post('/api/courses/units/:unitId/complete', authenticateToken, (req, res) => {
    const unitId = req.params.unitId;
    const userId = req.user.id;

    // Get unit info
    db.query('SELECT parent_course_id, prerequisite_unit_id, child_course_id FROM course_units WHERE id = ?', 
        [unitId], (err, results) => {
        if (err || results.length === 0) {
            return apiResponse(res, 404, 'Unit not found');
        }

        const unit = results[0];

        // Check prerequisite
        if (unit.prerequisite_unit_id) {
            db.query(`
                SELECT completed FROM course_enrollment_progress 
                WHERE unit_id = ? AND user_id = ?
            `, [unit.prerequisite_unit_id, userId], (prereqErr, prereqResults) => {
                if (prereqErr || prereqResults.length === 0 || !prereqResults[0].completed) {
                    return apiResponse(res, 400, 'Complete the prerequisite unit first');
                }
                completeUnit();
            });
        } else {
            completeUnit();
        }

        function completeUnit() {
            db.query(`
                INSERT INTO course_enrollment_progress (user_id, course_id, unit_id, completed, completed_at)
                VALUES (?, ?, ?, TRUE, CURRENT_TIMESTAMP)
                ON DUPLICATE KEY UPDATE completed = TRUE, completed_at = CURRENT_TIMESTAMP
            `, [userId, unit.parent_course_id, unitId], (updateErr) => {
                if (updateErr) {
                    return apiResponse(res, 500, 'Server error completing unit');
                }

                // Also mark the child course as complete in course_views
                db.query(`
                    INSERT INTO course_views (user_id, course_id, completed)
                    VALUES (?, ?, TRUE)
                    ON DUPLICATE KEY UPDATE completed = TRUE, last_viewed = CURRENT_TIMESTAMP
                `, [userId, unit.child_course_id], (viewErr) => {
                    if (viewErr) {
                        console.error('Error updating course view:', viewErr);
                    }

                    // Check if all units complete
                    checkMasterComplete();
                });
            });
        }

        function checkMasterComplete() {
            db.query(`
                SELECT COUNT(*) as total, 
                       SUM(CASE WHEN completed = TRUE THEN 1 ELSE 0 END) as completed
                FROM course_enrollment_progress
                WHERE user_id = ? AND course_id = ?
            `, [userId, unit.parent_course_id], (countErr, countResults) => {
                if (countErr) return;

                const { total, completed } = countResults[0];
                if (total > 0 && completed >= total) {
                    // Mark master course as complete
                    db.query(`
                        INSERT INTO course_views (user_id, course_id, completed)
                        VALUES (?, ?, TRUE)
                        ON DUPLICATE KEY UPDATE completed = TRUE, last_viewed = CURRENT_TIMESTAMP
                    `, [userId, unit.parent_course_id], () => {});
                }

                apiResponse(res, 200, 'Unit completed successfully', {
                    unit_complete: true,
                    all_units_complete: total > 0 && completed >= total
                });
            });
        }
    });
});

// Get courses available for adding as units
app.get('/api/courses/available-for-units', authenticateToken, (req, res) => {
    const parentCourseId = req.query.exclude_parent;
    const userId = req.user.id;

    let query = `
        SELECT c.id, c.title, c.description, c.status, c.course_type, c.creator_id,
               u.email as creator_email
        FROM courses c
        JOIN users u ON c.creator_id = u.id
        WHERE c.status = 'approved' AND c.id != ?
    `;
    const params = [parentCourseId];

    // If user has courses, also include their own courses (even if pending/draft)
    query += ` OR c.creator_id = ?`;
    params.push(userId);

    query += ` ORDER BY c.created_at DESC LIMIT 100`;

    db.query(query, params, (err, results) => {
        if (err) {
            console.error('Error fetching available courses:', err);
            return apiResponse(res, 500, 'Server error');
        }
        apiResponse(res, 200, 'Available courses fetched', results);
    });
});

// Enhanced enrollments endpoint with course type and status
app.get('/api/users/enrollments/enhanced', authenticateToken, (req, res) => {
    const userId = req.user.id;

    const query = `
        SELECT c.id, c.title, c.description, c.creator_id, c.course_type,
               e.enrolled_at, e.is_master_enrollment,
               cv.completed, cv.view_duration_hours,
               CASE 
                   WHEN cv.completed = TRUE THEN 'completed'
                   WHEN cv.view_duration_hours > 0 THEN 'in_progress'
                   ELSE 'enrolled'
               END as enrollment_status,
               CASE 
                   WHEN c.course_type = 'master' THEN (
                       SELECT COUNT(*) FROM course_units cu 
                       JOIN course_enrollment_progress cep ON cep.unit_id = cu.id 
                       WHERE cu.parent_course_id = c.id AND cep.user_id = e.user_id
                   )
                   ELSE NULL
               END as total_units,
               CASE 
                   WHEN c.course_type = 'master' THEN (
                       SELECT COUNT(*) FROM course_units cu 
                       JOIN course_enrollment_progress cep ON cep.unit_id = cu.id 
                       WHERE cu.parent_course_id = c.id AND cep.user_id = e.user_id AND cep.completed = TRUE
                   )
                   ELSE NULL
               END as completed_units
        FROM enrollments e
        JOIN courses c ON e.course_id = c.id
        LEFT JOIN course_views cv ON cv.user_id = e.user_id AND cv.course_id = c.id
        WHERE e.user_id = ?
        ORDER BY e.enrolled_at DESC
    `;

    db.query(query, [userId], (err, results) => {
        if (err) {
            console.error('Error fetching enhanced enrollments:', err);
            return apiResponse(res, 500, 'Server error');
        }
        apiResponse(res, 200, 'Enrollments fetched successfully', results);
    });
});

// ===== SIMULATOR MARKETPLACE ROUTES =====

// Get all public simulators (paginated)
app.get('/api/simulators', (req, res) => {
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 20;
    const offset = (page - 1) * limit;
    const search = req.query.search || '';
    const tags = req.query.tags || '';
    const sort = req.query.sort || 'newest'; // newest, popular, rating

    let whereClause = "WHERE (s.is_blocked IS NULL OR s.is_blocked = FALSE)";
    const params = [];
    let orderClause = "ORDER BY s.created_at DESC";

    if (search) {
        whereClause += ` AND (s.title LIKE ? OR s.description LIKE ?)`;
        params.push(`%${search}%`, `%${search}%`);
    }

    if (tags) {
        whereClause += ` AND s.tags LIKE ?`;
        params.push(`%${tags}%`);
    }

    if (sort === 'popular') {
        orderClause = "ORDER BY s.downloads DESC";
    } else if (sort === 'rating') {
        orderClause = "ORDER BY s.rating DESC";
    }

    const query = `
        SELECT 
            s.id, s.title, s.description, s.creator_id, u.email as creator_email,
            s.tags, s.downloads, s.rating, s.version, s.preview_image,
            s.forked_from, s.fork_count, s.sim_type,
            s.created_at, COUNT(DISTINCT sr.id) as review_count
        FROM simulators s
        LEFT JOIN users u ON s.creator_id = u.id
        LEFT JOIN simulator_ratings sr ON s.id = sr.simulator_id
        ${whereClause}
        GROUP BY s.id
        ${orderClause}
        LIMIT ? OFFSET ?
    `;

    const queryParams = [...params, limit, offset];

    db.query(query, queryParams, (err, results) => {
        if (err) {
            console.error('Error fetching simulators:', err);
            return apiResponse(res, 500, 'Error fetching simulators');
        }

        // Get total count for pagination
        const countQuery = `SELECT COUNT(*) as total FROM simulators s WHERE 1=1${whereClause.includes('WHERE') ? ' AND ' + whereClause.split('WHERE')[1] : ''}`;
        db.query(countQuery, params, (countErr, countResults) => {
            if (countErr) {
                console.error('Error counting simulators:', countErr);
                return apiResponse(res, 500, 'Error fetching simulators');
            }

            apiResponse(res, 200, 'Simulators fetched successfully', {
                simulators: results,
                total: countResults[0].total,
                page: page,
                pages: Math.ceil(countResults[0].total / limit)
            });
        });
    });
});

// Get simulator details
app.get('/api/simulators/:id', (req, res) => {
    const simulatorId = req.params.id;

    const query = `
        SELECT 
            s.id, s.title, s.description, s.creator_id, u.email as creator_email,
            s.blocks, s.connections, s.tags, s.downloads, s.rating, s.version,
            s.preview_image, s.is_public, s.forked_from, s.fork_count,
            s.code_mode, s.sim_type, s.is_blocked, s.blocked_reason,
            s.created_at, s.updated_at
        FROM simulators s
        LEFT JOIN users u ON s.creator_id = u.id
        WHERE s.id = ?
    `;

    db.query(query, [simulatorId], (err, results) => {
        if (err) {
            console.error('Error fetching simulator:', err);
            return apiResponse(res, 500, 'Error fetching simulator');
        }
        if (results.length === 0) {
            return apiResponse(res, 404, 'Simulator not found');
        }

        const simulator = results[0];

        // Parse JSON fields
        try {
            simulator.blocks = JSON.parse(simulator.blocks);
            simulator.connections = JSON.parse(simulator.connections);
        } catch (e) {
            console.error('Error parsing simulator JSON:', e);
        }

        // Parse code_mode if it's JSON
        if (simulator.code_mode) {
            try {
                simulator.code_mode = JSON.parse(simulator.code_mode);
            } catch (e) {
                // code_mode is plain text, keep as-is
            }
        }

        apiResponse(res, 200, 'Simulator fetched successfully', simulator);
    });
});

// Create new simulator
app.post('/api/simulators', authenticateToken, (req, res) => {
    const { title, description, blocks, connections, tags, preview_image, is_public, status, code_mode, sim_type, forked_from } = req.body;
    const creator_id = req.user.id;

    debug('📝 CREATE SIMULATOR DEBUG:');
    debug('  User ID:', creator_id);
    debug('  Title:', title);
    debug('  Blocks count:', Array.isArray(blocks) ? blocks.length : 'NOT AN ARRAY');
    debug('  Connections count:', Array.isArray(connections) ? connections.length : 'NOT AN ARRAY');
    debug('  Status:', status);

    if (!title) {
        console.error('❌ Missing title');
        return apiResponse(res, 400, 'Title is required');
    }

    if (!blocks) {
        console.error('❌ Missing blocks');
        return apiResponse(res, 400, 'Blocks are required');
    }

    if (title.length > 255) {
        return apiResponse(res, 400, 'Title too long (max 255 characters)');
    }

    try {
        const insertQuery = `
            INSERT INTO simulators (creator_id, title, description, blocks, connections, tags, preview_image, is_public, code_mode, sim_type, forked_from, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NOW(), NOW())
        `;

        const blocksJson = typeof blocks === 'string' ? blocks : JSON.stringify(blocks);
        const connectionsJson = typeof connections === 'string' ? connections : JSON.stringify(connections || []);
        const codeModeJson = code_mode ? (typeof code_mode === 'string' ? code_mode : JSON.stringify(code_mode)) : null;

        debug('✓ Blocks JSON length:', blocksJson.length);
        debug('✓ Connections JSON length:', connectionsJson.length);

        db.query(
            insertQuery,
            [creator_id, title, description || '', blocksJson, connectionsJson, tags || '', preview_image || '', is_public ? 1 : 0, codeModeJson, sim_type || 'block', forked_from || null],
            (err, result) => {
                if (err) {
                    console.error('❌ Database error:', err);
                    return apiResponse(res, 500, 'Error creating simulator', { details: err.message });
                }
                debug('✅ Simulator created with ID:', result.insertId);
                apiResponse(res, 201, 'Simulator created successfully', { simulatorId: result.insertId });
            }
        );
    } catch (error) {
        console.error('❌ Unexpected error:', error);
        apiResponse(res, 500, 'Server error', { details: error.message });
    }
});

// Update simulator
app.put('/api/simulators/:id', authenticateToken, (req, res) => {
    const simulatorId = req.params.id;
    const userId = req.user.id;
    const { title, description, blocks, connections, tags, preview_image, is_public, code_mode, sim_type } = req.body;

    if (!title) {
        return apiResponse(res, 400, 'Title is required');
    }

    // Check ownership
    db.query('SELECT creator_id FROM simulators WHERE id = ?', [simulatorId], (err, results) => {
        if (err) {
            console.error('Error fetching simulator:', err);
            return apiResponse(res, 500, 'Server error');
        }
        if (results.length === 0) {
            return apiResponse(res, 404, 'Simulator not found');
        }

        if (results[0].creator_id !== userId && req.user.role !== 'superadmin') {
            return apiResponse(res, 403, 'You can only edit your own simulators');
        }

        try {
            const blocksJson = blocks ? (typeof blocks === 'string' ? blocks : JSON.stringify(blocks)) : null;
            const connectionsJson = connections ? (typeof connections === 'string' ? connections : JSON.stringify(connections)) : null;
            const codeModeJson = code_mode ? (typeof code_mode === 'string' ? code_mode : JSON.stringify(code_mode)) : null;

            let setClauses = 'title = ?, description = ?';
            const params = [title, description];

            if (blocks) { setClauses += ', blocks = ?'; params.push(blocksJson); }
            if (connections) { setClauses += ', connections = ?'; params.push(connectionsJson); }

            setClauses += ', tags = ?, preview_image = ?, is_public = ?';
            params.push(tags, preview_image, is_public ? 1 : 0);

            if (code_mode !== undefined) { setClauses += ', code_mode = ?'; params.push(codeModeJson); }
            if (sim_type !== undefined) { setClauses += ', sim_type = ?'; params.push(sim_type); }

            params.push(simulatorId);

            const updateQuery = `UPDATE simulators SET ${setClauses} WHERE id = ?`;

            db.query(updateQuery, params, (err) => {
                if (err) {
                    console.error('Error updating simulator:', err);
                    return apiResponse(res, 500, 'Error updating simulator');
                }
                apiResponse(res, 200, 'Simulator updated successfully');
            });
        } catch (error) {
            console.error('Error:', error);
            apiResponse(res, 500, 'Server error');
        }
    });
});

// Delete simulator (owner: hard delete, superadmin on others: soft block)
app.delete('/api/simulators/:id', authenticateToken, (req, res) => {
    const simulatorId = req.params.id;
    const userId = req.user.id;
    const userRole = req.user.role;

    db.query('SELECT creator_id FROM simulators WHERE id = ?', [simulatorId], (err, results) => {
        if (err) return apiResponse(res, 500, 'Server error');
        if (results.length === 0) return apiResponse(res, 404, 'Simulator not found');

        const isOwner = results[0].creator_id === userId;
        const isSuperadmin = userRole === 'superadmin';

        if (!isOwner && !isSuperadmin) {
            return apiResponse(res, 403, 'You can only delete your own simulators');
        }

        if (isOwner) {
            // Owner deletes their own sim - hard delete
            db.query('DELETE FROM simulators WHERE id = ?', [simulatorId], (err) => {
                if (err) return apiResponse(res, 500, 'Error deleting simulator');
                apiResponse(res, 200, 'Simulator deleted successfully');
            });
        } else {
            // Superadmin blocking someone else's sim - soft delete with reason
            const reason = req.body && req.body.reason;
            if (!reason) {
                return apiResponse(res, 400, 'Reason is required when blocking a simulator');
            }
            db.query('UPDATE simulators SET is_blocked = TRUE, blocked_reason = ? WHERE id = ?', [reason, simulatorId], (err) => {
                if (err) return apiResponse(res, 500, 'Error blocking simulator');
                apiResponse(res, 200, 'Simulator blocked successfully');
            });
        }
    });
});

// Get user's blocked simulators
app.get('/api/my-blocked-simulators', authenticateToken, (req, res) => {
    db.query('SELECT id, title, blocked_reason, updated_at FROM simulators WHERE creator_id = ? AND is_blocked = TRUE', [req.user.id], (err, results) => {
        if (err) return apiResponse(res, 500, 'Server error');
        apiResponse(res, 200, 'Blocked simulators', results);
    });
});

// Fork simulator
app.post('/api/simulators/:id/fork', authenticateToken, (req, res) => {
    const simulatorId = req.params.id;
    const userId = req.user.id;

    db.query('SELECT * FROM simulators WHERE id = ?', [simulatorId], (err, results) => {
        if (err) {
            console.error('Error fetching simulator for fork:', err);
            return apiResponse(res, 500, 'Server error');
        }
        if (results.length === 0) {
            return apiResponse(res, 404, 'Simulator not found');
        }

        const source = results[0];

        const insertQuery = `
            INSERT INTO simulators (creator_id, title, description, blocks, connections, tags, preview_image, is_public, forked_from, code_mode, sim_type, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, 0, ?, ?, ?, NOW(), NOW())
        `;

        db.query(
            insertQuery,
            [userId, `Fork of ${source.title}`, source.description || '', source.blocks, source.connections, source.tags || '', source.preview_image || '', simulatorId, source.code_mode || null, source.sim_type || 'block'],
            (insertErr, insertResult) => {
                if (insertErr) {
                    console.error('Error forking simulator:', insertErr);
                    return apiResponse(res, 500, 'Error forking simulator');
                }

                // Increment fork_count on original
                db.query('UPDATE simulators SET fork_count = fork_count + 1 WHERE id = ?', [simulatorId], (updateErr) => {
                    if (updateErr) console.error('Error updating fork_count:', updateErr);
                });

                apiResponse(res, 201, 'Simulator forked successfully', { simulatorId: insertResult.insertId });
            }
        );
    });
});

// Get forks of a simulator
app.get('/api/simulators/:id/forks', (req, res) => {
    const simulatorId = req.params.id;

    const query = `
        SELECT 
            s.id, s.title, s.description, s.creator_id, u.email as creator_email,
            s.downloads, s.rating, s.sim_type, s.created_at
        FROM simulators s
        LEFT JOIN users u ON s.creator_id = u.id
        WHERE s.forked_from = ?
        ORDER BY s.created_at DESC
    `;

    db.query(query, [simulatorId], (err, results) => {
        if (err) {
            console.error('Error fetching forks:', err);
            return apiResponse(res, 500, 'Error fetching forks');
        }
        apiResponse(res, 200, 'Forks fetched successfully', results);
    });
});

// Publish/unpublish simulator
app.post('/api/simulators/:id/publish', authenticateToken, (req, res) => {
    const simulatorId = req.params.id;
    const userId = req.user.id;
    const { is_public } = req.body;

    db.query('SELECT creator_id FROM simulators WHERE id = ?', [simulatorId], (err, results) => {
        if (err) {
            console.error('Error fetching simulator:', err);
            return apiResponse(res, 500, 'Server error');
        }
        if (results.length === 0) {
            return apiResponse(res, 404, 'Simulator not found');
        }

        if (results[0].creator_id !== userId && req.user.role !== 'superadmin') {
            return apiResponse(res, 403, 'You can only publish your own simulators');
        }

        db.query(
            'UPDATE simulators SET is_public = ? WHERE id = ?',
            [is_public ? 1 : 0, simulatorId],
            (err) => {
                if (err) {
                    console.error('Error updating simulator:', err);
                    return apiResponse(res, 500, 'Error updating simulator');
                }
                apiResponse(res, 200, `Simulator ${is_public ? 'published' : 'unpublished'} successfully`);
            }
        );
    });
});

// Record download
app.post('/api/simulators/:id/download', authenticateToken, (req, res) => {
    const simulatorId = req.params.id;
    const userId = req.user.id;
    const { courseId } = req.body;

    try {
        db.query(
            'INSERT INTO simulator_downloads (simulator_id, user_id, course_id) VALUES (?, ?, ?)',
            [simulatorId, userId, courseId || null],
            (err) => {
                if (err && err.code !== 'ER_DUP_ENTRY') {
                    console.error('Error recording download:', err);
                    return apiResponse(res, 500, 'Error recording download');
                }

                // Increment download count
                db.query(
                    'UPDATE simulators SET downloads = downloads + 1 WHERE id = ?',
                    [simulatorId],
                    (updateErr) => {
                        if (updateErr) console.error('Error updating downloads:', updateErr);
                    }
                );

                apiResponse(res, 201, 'Download recorded successfully');
            }
        );
    } catch (error) {
        console.error('Error:', error);
        apiResponse(res, 500, 'Server error');
    }
});

// Get user's simulators
app.get('/api/my-simulators', authenticateToken, (req, res) => {
    const userId = req.user.id;

    const query = `
        SELECT 
            id, title, description, creator_id, tags, downloads, rating, 
            version, is_public, created_at, updated_at
        FROM simulators
        WHERE creator_id = ?
        ORDER BY created_at DESC
    `;

    db.query(query, [userId], (err, results) => {
        if (err) {
            console.error('Error fetching user simulators:', err);
            return apiResponse(res, 500, 'Error fetching simulators');
        }
        apiResponse(res, 200, 'User simulators fetched successfully', results);
    });
});

// Add rating/review
app.post('/api/simulators/:id/ratings', authenticateToken, (req, res) => {
    const simulatorId = req.params.id;
    const userId = req.user.id;
    const { rating, review } = req.body;

    if (!rating || rating < 1 || rating > 5) {
        return apiResponse(res, 400, 'Rating must be between 1 and 5');
    }

    db.query(
        'INSERT INTO simulator_ratings (simulator_id, user_id, rating, review) VALUES (?, ?, ?, ?) ON DUPLICATE KEY UPDATE rating = ?, review = ?',
        [simulatorId, userId, rating, review, rating, review],
        (err) => {
            if (err) {
                console.error('Error adding rating:', err);
                return apiResponse(res, 500, 'Error adding rating');
            }

            // Recalculate average rating
            db.query(
                'SELECT AVG(rating) as avg_rating FROM simulator_ratings WHERE simulator_id = ?',
                [simulatorId],
                (ratingErr, ratingResults) => {
                    if (!ratingErr && ratingResults.length > 0) {
                        const avgRating = parseFloat(ratingResults[0].avg_rating).toFixed(2);
                        db.query(
                            'UPDATE simulators SET rating = ? WHERE id = ?',
                            [avgRating, simulatorId],
                            (updateErr) => {
                                if (updateErr) console.error('Error updating rating:', updateErr);
                            }
                        );
                    }
                }
            );

            apiResponse(res, 201, 'Rating added successfully');
        }
    );
});

// Get ratings and reviews
app.get('/api/simulators/:id/ratings', (req, res) => {
    const simulatorId = req.params.id;

    const query = `
        SELECT 
            sr.id, sr.rating, sr.review, sr.created_at,
            u.email as user_email
        FROM simulator_ratings sr
        LEFT JOIN users u ON sr.user_id = u.id
        WHERE sr.simulator_id = ?
        ORDER BY sr.created_at DESC
    `;

    db.query(query, [simulatorId], (err, results) => {
        if (err) {
            console.error('Error fetching ratings:', err);
            return apiResponse(res, 500, 'Error fetching ratings');
        }
        apiResponse(res, 200, 'Ratings fetched successfully', results);
    });
});

// Add comment
app.post('/api/simulators/:id/comments', authenticateToken, (req, res) => {
    const simulatorId = req.params.id;
    const userId = req.user.id;
    const { comment } = req.body;

    if (!comment) {
        return apiResponse(res, 400, 'Comment is required');
    }

    db.query(
        'INSERT INTO simulator_comments (simulator_id, user_id, comment) VALUES (?, ?, ?)',
        [simulatorId, userId, comment],
        (err) => {
            if (err) {
                console.error('Error adding comment:', err);
                return apiResponse(res, 500, 'Error adding comment');
            }
            apiResponse(res, 201, 'Comment added successfully');
        }
    );
});

// Get comments
app.get('/api/simulators/:id/comments', (req, res) => {
    const simulatorId = req.params.id;

    const query = `
        SELECT 
            sc.id, sc.comment, sc.created_at,
            u.email as user_email
        FROM simulator_comments sc
        LEFT JOIN users u ON sc.user_id = u.id
        WHERE sc.simulator_id = ?
        ORDER BY sc.created_at DESC
    `;

    db.query(query, [simulatorId], (err, results) => {
        if (err) {
            console.error('Error fetching comments:', err);
            return apiResponse(res, 500, 'Error fetching comments');
        }
        apiResponse(res, 200, 'Comments fetched successfully', results);
    });
});

// Get trending simulators
app.get('/api/simulators/trending/all', (req, res) => {
    const query = `
        SELECT 
            id, title, description, creator_id, tags, downloads, 
            rating, is_public, created_at
        FROM simulators
        WHERE is_public = TRUE
        ORDER BY (downloads * 0.5 + rating * 10) DESC
        LIMIT 10
    `;

    db.query(query, (err, results) => {
        if (err) {
            console.error('Error fetching trending simulators:', err);
            return apiResponse(res, 500, 'Error fetching trending simulators');
        }
        apiResponse(res, 200, 'Trending simulators fetched successfully', results);
    });
});

// ===== COURSE-SIMULATOR INTEGRATION =====

// ===== COURSE-SIMULATOR INTEGRATION =====

// Add simulator to course - BOTH endpoint paths for compatibility
app.post('/api/courses/:courseId/simulators', authenticateToken, (req, res) => {
    const courseId = req.params.courseId;
    const userId = req.user.id;
    const { simulator_id } = req.body;

    if (!simulator_id) {
        return apiResponse(res, 400, 'Simulator ID is required');
    }

    // Verify course ownership
    db.query('SELECT creator_id FROM courses WHERE id = ?', [courseId], (err, results) => {
        if (err) {
            console.error('Error fetching course:', err);
            return apiResponse(res, 500, 'Server error');
        }
        if (results.length === 0) {
            return apiResponse(res, 404, 'Course not found');
        }

        if (parseInt(results[0].creator_id) !== parseInt(userId) && req.user.role !== 'superadmin') {
            return apiResponse(res, 403, 'You can only edit your own courses');
        }

        // Verify simulator exists
        db.query('SELECT id FROM simulators WHERE id = ?', [simulator_id], (err, simResults) => {
            if (err) {
                console.error('Error fetching simulator:', err);
                return apiResponse(res, 500, 'Server error');
            }
            if (simResults.length === 0) {
                return apiResponse(res, 404, 'Simulator not found');
            }

            // Add to course
            db.query(
                'INSERT INTO course_simulator_usage (course_id, simulator_id) VALUES (?, ?) ON DUPLICATE KEY UPDATE added_at = CURRENT_TIMESTAMP',
                [courseId, simulator_id],
                (err) => {
                    if (err) {
                        console.error('Error adding simulator to course:', err);
                        return apiResponse(res, 500, 'Error adding simulator to course');
                    }
                    apiResponse(res, 201, 'Simulator added to course successfully');
                }
            );
        });
    });
});

// Keep old endpoint for backwards compatibility
app.post('/api/courses/:courseId/add-simulator', authenticateToken, (req, res) => {
    const courseId = req.params.courseId;
    const userId = req.user.id;
    const { simulator_id } = req.body;

    if (!simulator_id) {
        return apiResponse(res, 400, 'Simulator ID is required');
    }

    // Verify course ownership
    db.query('SELECT creator_id FROM courses WHERE id = ?', [courseId], (err, results) => {
        if (err) {
            console.error('Error fetching course:', err);
            return apiResponse(res, 500, 'Server error');
        }
        if (results.length === 0) {
            return apiResponse(res, 404, 'Course not found');
        }

        if (parseInt(results[0].creator_id) !== parseInt(userId) && req.user.role !== 'superadmin') {
            return apiResponse(res, 403, 'You can only edit your own courses');
        }

        // Verify simulator exists
        db.query('SELECT id FROM simulators WHERE id = ?', [simulator_id], (err, simResults) => {
            if (err) {
                console.error('Error fetching simulator:', err);
                return apiResponse(res, 500, 'Server error');
            }
            if (simResults.length === 0) {
                return apiResponse(res, 404, 'Simulator not found');
            }

            // Add to course
            db.query(
                'INSERT INTO course_simulator_usage (course_id, simulator_id) VALUES (?, ?) ON DUPLICATE KEY UPDATE added_at = CURRENT_TIMESTAMP',
                [courseId, simulator_id],
                (err) => {
                    if (err) {
                        console.error('Error adding simulator to course:', err);
                        return apiResponse(res, 500, 'Error adding simulator to course');
                    }
                    apiResponse(res, 201, 'Simulator added to course successfully');
                }
            );
        });
    });
});

// Get simulators for a course
app.get('/api/courses/:courseId/simulators', authenticateToken, (req, res) => {
    const courseId = req.params.courseId;

    const query = `
        SELECT s.id, s.title, s.description, s.creator_id, u.email as creator_email,
               s.tags, s.downloads, s.rating, s.version, s.preview_image,
               csu.added_at
        FROM course_simulator_usage csu
        JOIN simulators s ON csu.simulator_id = s.id
        LEFT JOIN users u ON s.creator_id = u.id
        WHERE csu.course_id = ?
        ORDER BY csu.added_at DESC
    `;

    db.query(query, [courseId], (err, results) => {
        if (err) {
            console.error('Error fetching course simulators:', err);
            return apiResponse(res, 500, 'Error fetching simulators');
        }
        apiResponse(res, 200, 'Course simulators fetched successfully', results);
    });
});

// Remove simulator from course
app.delete('/api/courses/:courseId/simulators/:simulatorId', authenticateToken, (req, res) => {
    const courseId = req.params.courseId;
    const simulatorId = req.params.simulatorId;
    const userId = req.user.id;

    // Verify course ownership
    db.query('SELECT creator_id FROM courses WHERE id = ?', [courseId], (err, results) => {
        if (err) {
            console.error('Error fetching course:', err);
            return apiResponse(res, 500, 'Server error');
        }
        if (results.length === 0) {
            return apiResponse(res, 404, 'Course not found');
        }

        if (results[0].creator_id !== userId && req.user.role !== 'superadmin') {
            return apiResponse(res, 403, 'You can only edit your own courses');
        }

        db.query(
            'DELETE FROM course_simulator_usage WHERE course_id = ? AND simulator_id = ?',
            [courseId, simulatorId],
            (err) => {
                if (err) {
                    console.error('Error removing simulator from course:', err);
                    return apiResponse(res, 500, 'Error removing simulator');
                }
                apiResponse(res, 200, 'Simulator removed from course');
            }
        );
    });
});

// Save simulator version
app.post('/api/simulators/:id/versions', authenticateToken, (req, res) => {
    const simulatorId = req.params.id;
    const userId = req.user.id;
    const { blocks, connections } = req.body;

    // Verify ownership
    db.query('SELECT creator_id FROM simulators WHERE id = ?', [simulatorId], (err, results) => {
        if (err) {
            console.error('Error fetching simulator:', err);
            return apiResponse(res, 500, 'Server error');
        }
        if (results.length === 0) {
            return apiResponse(res, 404, 'Simulator not found');
        }

        if (results[0].creator_id !== userId && req.user.role !== 'superadmin') {
            return apiResponse(res, 403, 'You can only version your own simulators');
        }

        // Get current version count
        db.query(
            'SELECT MAX(version_number) as max_version FROM simulator_versions WHERE simulator_id = ?',
            [simulatorId],
            (err, versionResults) => {
                const newVersion = (versionResults[0].max_version || 0) + 1;

                db.query(
                    'INSERT INTO simulator_versions (simulator_id, version_number, blocks, connections) VALUES (?, ?, ?, ?)',
                    [simulatorId, newVersion, JSON.stringify(blocks), JSON.stringify(connections || [])],
                    (err, result) => {
                        if (err) {
                            console.error('Error saving version:', err);
                            return apiResponse(res, 500, 'Error saving version');
                        }
                        apiResponse(res, 201, 'Version saved', { versionNumber: newVersion });
                    }
                );
            }
        );
    });
});

// Get simulator versions
app.get('/api/simulators/:id/versions', (req, res) => {
    const simulatorId = req.params.id;

    db.query(
        'SELECT id, version_number, created_at FROM simulator_versions WHERE simulator_id = ? ORDER BY version_number DESC',
        [simulatorId],
        (err, results) => {
            if (err) {
                console.error('Error fetching versions:', err);
                return apiResponse(res, 500, 'Error fetching versions');
            }
            apiResponse(res, 200, 'Versions fetched successfully', results);
        }
    );
});

// Get specific version
app.get('/api/simulators/:id/versions/:versionNumber', (req, res) => {
    const simulatorId = req.params.id;
    const versionNumber = req.params.versionNumber;

    db.query(
        'SELECT version_number, blocks, connections, created_at FROM simulator_versions WHERE simulator_id = ? AND version_number = ?',
        [simulatorId, versionNumber],
        (err, results) => {
            if (err) {
                console.error('Error fetching version:', err);
                return apiResponse(res, 500, 'Error fetching version');
            }
            if (results.length === 0) {
                return apiResponse(res, 404, 'Version not found');
            }

            const version = results[0];
            try {
                version.blocks = JSON.parse(version.blocks);
                version.connections = JSON.parse(version.connections);
            } catch (e) {
                console.error('Error parsing version JSON:', e);
            }

            apiResponse(res, 200, 'Version fetched successfully', version);
        }
    );
});


// ===== QUIZ QUESTIONS API =====

// Create quiz question
app.post('/api/courses/:courseId/questions', authenticateToken, (req, res) => {
    const courseId = req.params.courseId;
    const userId = req.user.id;
    const { question_text, question_type, options, correct_answer, explanation, points, order_index } = req.body;

    // Verify user owns the course
    db.query('SELECT creator_id FROM courses WHERE id = ?', [courseId], (err, results) => {
        if (err) {
            console.error('Error fetching course:', err);
            return apiResponse(res, 500, 'Server error');
        }
        if (results.length === 0) {
            return apiResponse(res, 404, 'Course not found');
        }
        if (parseInt(results[0].creator_id) !== parseInt(userId)) {
            return apiResponse(res, 403, 'You can only add questions to your own courses');
        }

        // Insert question
        const insertQuery = `
            INSERT INTO course_questions 
            (course_id, question_text, question_type, options, correct_answer, explanation, points, order_index)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        `;
        const optionsJson = options ? JSON.stringify(options) : null;

        db.query(insertQuery, [
            courseId, question_text, question_type || 'multiple_choice',
            optionsJson, correct_answer, explanation, points || 1, order_index || 0
        ], (err, result) => {
            if (err) {
                console.error('Error creating question:', err);
                return apiResponse(res, 500, 'Server error creating question');
            }
            apiResponse(res, 201, 'Question created successfully', { questionId: result.insertId });
        });
    });
});

// Get all questions for a course
app.get('/api/courses/:courseId/questions', authenticateToken, (req, res) => {
    const courseId = req.params.courseId;
    debug(`DEBUG GET QUESTIONS: Course ${courseId}, User: ${req.user.id}, Role: ${req.user.role}`);

    const query = `
        SELECT id, course_id, question_text, question_type, options, correct_answer, 
               explanation, points, order_index, created_at
        FROM course_questions
        WHERE course_id = ?
        ORDER BY order_index ASC, created_at ASC
    `;

    db.query(query, [courseId], (err, results) => {
        if (err) {
            console.error('Error fetching questions:', err);
            return apiResponse(res, 500, 'Server error fetching questions');
        }

        // Parse options JSON
        const questions = results.map(q => {
            if (q.options && typeof q.options === 'string') {
                try {
                    q.options = JSON.parse(q.options);
                } catch (e) {
                    q.options = [];
                }
            }
            return q;
        });

        apiResponse(res, 200, 'Questions fetched successfully', questions);
    });
});

// Update quiz question
app.put('/api/courses/:courseId/questions/:questionId', authenticateToken, (req, res) => {
    const { courseId, questionId } = req.params;
    const userId = req.user.id;
    const { question_text, question_type, options, correct_answer, explanation, points, order_index } = req.body;

    // Verify user owns the course
    db.query('SELECT creator_id FROM courses WHERE id = ?', [courseId], (err, results) => {
        if (err) {
            console.error('Error fetching course:', err);
            return apiResponse(res, 500, 'Server error');
        }
        if (results.length === 0) {
            return apiResponse(res, 404, 'Course not found');
        }
        if (parseInt(results[0].creator_id) !== parseInt(userId)) {
            return apiResponse(res, 403, 'You can only edit questions in your own courses');
        }

        const updateQuery = `
            UPDATE course_questions
            SET question_text = ?, question_type = ?, options = ?, correct_answer = ?, 
                explanation = ?, points = ?, order_index = ?
            WHERE id = ? AND course_id = ?
        `;
        const optionsJson = options ? JSON.stringify(options) : null;

        db.query(updateQuery, [
            question_text, question_type, optionsJson, correct_answer,
            explanation, points, order_index, questionId, courseId
        ], (err, result) => {
            if (err) {
                console.error('Error updating question:', err);
                return apiResponse(res, 500, 'Server error updating question');
            }
            if (result.affectedRows === 0) {
                return apiResponse(res, 404, 'Question not found');
            }
            apiResponse(res, 200, 'Question updated successfully');
        });
    });
});

// Delete quiz question
app.delete('/api/courses/:courseId/questions/:questionId', authenticateToken, (req, res) => {
    const { courseId, questionId } = req.params;
    const userId = req.user.id;

    // Verify user owns the course
    db.query('SELECT creator_id FROM courses WHERE id = ?', [courseId], (err, results) => {
        if (err) {
            console.error('Error fetching course:', err);
            return apiResponse(res, 500, 'Server error');
        }
        if (results.length === 0) {
            return apiResponse(res, 404, 'Course not found');
        }
        if (parseInt(results[0].creator_id) !== parseInt(userId)) {
            return apiResponse(res, 403, 'You can only delete questions from your own courses');
        }

        db.query('DELETE FROM course_questions WHERE id = ? AND course_id = ?', [questionId, courseId], (err, result) => {
            if (err) {
                console.error('Error deleting question:', err);
                return apiResponse(res, 500, 'Server error deleting question');
            }
            if (result.affectedRows === 0) {
                return apiResponse(res, 404, 'Question not found');
            }
            apiResponse(res, 200, 'Question deleted successfully');
        });
    });
});

// Submit answer to quiz question
app.post('/api/courses/:courseId/questions/:questionId/answer', authenticateToken, (req, res) => {
    const { questionId } = req.params;
    const userId = req.user.id;
    const { user_answer } = req.body;

    // Get the question to check correct answer
    db.query('SELECT question_type, correct_answer, explanation FROM course_questions WHERE id = ?', [questionId], (err, results) => {
        if (err) {
            console.error('Error fetching question:', err);
            return apiResponse(res, 500, 'Server error');
        }
        if (results.length === 0) {
            return apiResponse(res, 404, 'Question not found');
        }

        const question = results[0];
        let isCorrect = false;
        
        if (question.question_type === 'fill_in_blank_with_image') {
            try {
                const parsedUser = JSON.parse(user_answer);
                const parsedCorrect = JSON.parse(question.correct_answer);
                
                // Check if all parts match
                isCorrect = true;
                for (const key in parsedCorrect) {
                    if (!parsedUser[key] || parsedUser[key].toString().trim().toLowerCase() !== parsedCorrect[key].toString().trim().toLowerCase()) {
                        isCorrect = false;
                        break;
                    }
                }
            } catch (e) {
                console.error("Error parsing fill_in_blank_with_image answers", e);
                isCorrect = false;
            }
        } else {
            isCorrect = user_answer.trim().toLowerCase() === question.correct_answer.trim().toLowerCase();
        }

        // Record the attempt (Update if already exists to prevent double-counting)
        const insertQuery = `
            INSERT INTO user_quiz_attempts (user_id, question_id, user_answer, is_correct)
            VALUES (?, ?, ?, ?)
            ON DUPLICATE KEY UPDATE 
            user_answer = VALUES(user_answer),
            is_correct = VALUES(is_correct),
            attempted_at = CURRENT_TIMESTAMP
        `;

        db.query(insertQuery, [userId, questionId, user_answer, isCorrect], (err, result) => {
            if (err) {
                console.error('Error recording answer:', err);
                return apiResponse(res, 500, 'Server error recording answer');
            }

            apiResponse(res, 200, 'Answer submitted successfully', {
                is_correct: isCorrect,
                correct_answer: question.correct_answer,
                explanation: question.explanation
            });
        });
    });
});

// Get user's attempts for a question
app.get('/api/courses/:courseId/questions/:questionId/attempts', authenticateToken, (req, res) => {
    const { questionId } = req.params;
    const userId = req.user.id;

    const query = `
        SELECT id, user_answer, is_correct, attempted_at
        FROM user_quiz_attempts
        WHERE user_id = ? AND question_id = ?
        ORDER BY attempted_at DESC
    `;

    db.query(query, [userId, questionId], (err, results) => {
        if (err) {
            console.error('Error fetching attempts:', err);
            return apiResponse(res, 500, 'Server error fetching attempts');
        }
        apiResponse(res, 200, 'Attempts fetched successfully', results);
    });
});

// ===== INTERACTIVE SIMULATOR PARAMETERS ROUTES =====
// Copy these routes into server.js BEFORE the "// ===== ERROR HANDLING =====" section

// Create interactive parameter for a simulator in a course
app.post('/api/courses/:courseId/simulators/:blockId/params', authenticateToken, (req, res) => {
    const { courseId, blockId } = req.params;
    const { block_id, param_name, param_label, min_value, max_value, step_value, default_value } = req.body;
    const userId = req.user.id;

    // Verify user owns the course
    db.query('SELECT creator_id FROM courses WHERE id = ?', [courseId], (err, results) => {
        if (err) {
            console.error('Error fetching course:', err);
            return apiResponse(res, 500, 'Server error');
        }
        if (results.length === 0) {
            return apiResponse(res, 404, 'Course not found');
        }
        if (parseInt(results[0].creator_id) !== parseInt(userId)) {
            return apiResponse(res, 403, 'You can only modify your own courses');
        }

        const insertQuery = `
            INSERT INTO simulator_interactive_params 
            (course_id, simulator_block_id, block_id, param_name, param_label, min_value, max_value, step_value, default_value)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        `;

        db.query(insertQuery, [
            courseId, blockId, block_id, param_name, param_label || param_name,
            min_value || 0, max_value || 100, step_value || 1, default_value
        ], (err, result) => {
            if (err) {
                if (err.code === 'ER_DUP_ENTRY') {
                    return apiResponse(res, 409, 'Parameter already exists');
                }
                console.error('Error creating parameter:', err);
                return apiResponse(res, 500, 'Server error creating parameter');
            }
            apiResponse(res, 201, 'Parameter created successfully', { id: result.insertId });
        });
    });
});

// Get all interactive parameters for a course
app.get('/api/courses/:courseId/params', authenticateToken, (req, res) => {
    const { courseId } = req.params;

    const query = `
        SELECT * FROM simulator_interactive_params
        WHERE course_id = ?
        ORDER BY simulator_block_id, created_at ASC
    `;

    db.query(query, [courseId], (err, results) => {
        if (err) {
            console.error('Error fetching parameters:', err);
            return apiResponse(res, 500, 'Server error fetching parameters');
        }
        apiResponse(res, 200, 'Parameters fetched successfully', results);
    });
});

// Delete interactive parameter
app.delete('/api/courses/:courseId/params/:paramId', authenticateToken, (req, res) => {
    const { courseId, paramId } = req.params;
    const userId = req.user.id;

    // Verify user owns the course
    db.query('SELECT creator_id FROM courses WHERE id = ?', [courseId], (err, results) => {
        if (err) {
            console.error('Error fetching course:', err);
            return apiResponse(res, 500, 'Server error');
        }
        if (results.length === 0) {
            return apiResponse(res, 404, 'Course not found');
        }
        if (parseInt(results[0].creator_id) !== parseInt(userId)) {
            return apiResponse(res, 403, 'You can only modify your own courses');
        }

        db.query('DELETE FROM simulator_interactive_params WHERE id = ? AND course_id = ?', [paramId, courseId], (err, result) => {
            if (err) {
                console.error('Error deleting parameter:', err);
                return apiResponse(res, 500, 'Server error deleting parameter');
            }
            if (result.affectedRows === 0) {
                return apiResponse(res, 404, 'Parameter not found');
            }
            apiResponse(res, 200, 'Parameter deleted successfully');
        });
    });
});


// ===== VOLUNTEER HOURS, CERTIFICATES & SPONSORSHIPS =====

app.get('/api/users/volunteer-stats', authenticateToken, (req, res) => {
    const userId = req.user.id;
    db.query(
        'SELECT total_volunteer_hours, is_verified_creator FROM users WHERE id = ?',
        [userId],
        (err, results) => {
            if (err) {
                console.error('volunteer-stats: user query error:', err.message);
                return apiResponse(res, 500, 'Server error');
            }
            if (results.length === 0) return apiResponse(res, 404, 'User not found');

            const totalHours = results[0].total_volunteer_hours || 0;

            db.query(
                'SELECT * FROM certificates WHERE user_id = ? AND certificate_type = ? ORDER BY issued_at DESC',
                [userId, 'volunteer_hours'],
                (err2, certs) => {
                    if (err2) {
                        console.error('volunteer-stats: certificates query error:', err2.message);
                        return apiResponse(res, 200, 'Stats retrieved (no certs table)', {
                            total_volunteer_hours: totalHours,
                            is_verified_creator: results[0].is_verified_creator,
                            certificates: []
                        });
                    }

                    const maxMilestone = Math.floor(totalHours / 5) * 5;
                    const existingHours = certs.map(c => Number(c.hours_certified));
                    const missingMilestones = [];
                    for (let i = 5; i <= maxMilestone; i += 5) {
                        if (!existingHours.includes(i)) {
                            missingMilestones.push(i);
                        }
                    }

                    if (missingMilestones.length > 0) {
                        debug(`Creating ${missingMilestones.length} missing certificates for user ${userId}:`, missingMilestones);
                        const crypto = require('crypto');
                        let inserted = 0;
                        missingMilestones.forEach(milestone => {
                            const verificationCode = crypto.randomBytes(16).toString('hex');
                            db.query(
                                'INSERT INTO certificates (user_id, certificate_type, hours_certified, verification_code) VALUES (?, ?, ?, ?)',
                                [userId, 'volunteer_hours', milestone, verificationCode],
                                (insertErr) => {
                                    inserted++;
                                    if (insertErr) console.error('Error creating certificate for milestone', milestone, insertErr.message);
                                    else debug(`✓ Created ${milestone}h certificate for user ${userId}`);

                                    if (inserted === missingMilestones.length) {
                                        db.query(
                                            'SELECT * FROM certificates WHERE user_id = ? ORDER BY hours_certified ASC',
                                            [userId],
                                            (err3, allCerts) => {
                                                if (err3) {
                                                    console.error('volunteer-stats: re-fetch certs error:', err3.message);
                                                    return apiResponse(res, 500, 'Server error');
                                                }
                                                apiResponse(res, 200, 'Stats retrieved', {
                                                    total_volunteer_hours: totalHours,
                                                    is_verified_creator: results[0].is_verified_creator,
                                                    certificates: allCerts
                                                });
                                            }
                                        );
                                    }
                                }
                            );
                        });
                    } else {
                        apiResponse(res, 200, 'Stats retrieved', {
                            total_volunteer_hours: totalHours,
                            is_verified_creator: results[0].is_verified_creator,
                            certificates: certs
                        });
                    }
                }
            );
        }
    );
});

app.post('/api/users/update-volunteer-hours', authenticateToken, authorize('admin', 'superadmin'), (req, res) => {
    const { user_id, hours_to_add } = req.body;
    if (!user_id || !hours_to_add) return apiResponse(res, 400, 'user_id and hours_to_add required');

    db.query(
        'UPDATE users SET total_volunteer_hours = total_volunteer_hours + ? WHERE id = ?',
        [hours_to_add, user_id],
        (err, result) => {
            if (err) return apiResponse(res, 500, 'Server error');
            if (result.affectedRows === 0) return apiResponse(res, 404, 'User not found');

            db.query('SELECT total_volunteer_hours, email FROM users WHERE id = ?', [user_id], (err2, users) => {
                if (err2 || users.length === 0) return apiResponse(res, 200, 'Hours updated');

                const totalHours = users[0].total_volunteer_hours;

                // Calculate all 5-hour milestones achieved
                const maxMilestone = Math.floor(totalHours / 5) * 5;
                const milestones = [];
                for (let i = 5; i <= maxMilestone; i += 5) {
                    milestones.push(i);
                }

                if (milestones.length > 0) {
                    // Check existing certificates to avoid duplicates
                    db.query(
                        'SELECT hours_certified FROM certificates WHERE user_id = ? AND certificate_type = "volunteer_hours"',
                        [user_id],
                        (certErr, existingCerts) => {
                            if (!certErr) {
                                const existingHours = existingCerts.map(c => c.hours_certified);

                                milestones.forEach(milestone => {
                                    if (!existingHours.includes(milestone)) {
                                        const verificationCode = require('crypto').randomBytes(16).toString('hex');
                                        db.query(
                                            'INSERT INTO certificates (user_id, certificate_type, hours_certified, verification_code) VALUES (?, "volunteer_hours", ?, ?)',
                                            [user_id, milestone, verificationCode]
                                        );
                                        debug(`Issued volunteer certificate for ${milestone} hours to user ${user_id}`);
                                    }
                                });
                            }
                        }
                    );
                }

                if (totalHours >= 20) {
                    db.query('UPDATE users SET is_verified_creator = TRUE WHERE id = ?', [user_id]);
                }

                apiResponse(res, 200, 'Volunteer hours updated', { new_total: totalHours });
            });
        }
    );
});

// Grant gems to a user (admin/superadmin) — mirrors volunteer hours grant
app.post('/api/users/grant-gems', authenticateToken, authorize('admin', 'superadmin'), (req, res) => {
    const userId = parseInt(req.body?.user_id, 10);
    const gemsToAdd = parseInt(req.body?.gems_to_add, 10);
    if (!userId || Number.isNaN(userId) || Number.isNaN(gemsToAdd) || gemsToAdd === 0) {
        return apiResponse(res, 400, 'user_id and non-zero gems_to_add required');
    }

    db.query(
        'UPDATE users SET gems = GREATEST(0, IFNULL(gems, 0) + ?) WHERE id = ?',
        [gemsToAdd, userId],
        (err, result) => {
            if (err) {
                console.error('grant-gems update error:', err);
                return apiResponse(res, 500, 'Server error');
            }
            if (result.affectedRows === 0) return apiResponse(res, 404, 'User not found');

            db.query('SELECT gems, email FROM users WHERE id = ?', [userId], (err2, users) => {
                if (err2 || !users.length) {
                    return apiResponse(res, 200, 'Gems updated');
                }
                return apiResponse(res, 200, 'Gems updated', {
                    new_total: users[0].gems || 0,
                    email: users[0].email
                });
            });
        }
    );
});

app.get('/api/certificates/verify/:code', async (req, res) => {
    const { code } = req.params;
    const { format } = req.query;

    db.query(
        `SELECT c.*, u.email, u.total_volunteer_hours FROM certificates c
         JOIN users u ON c.user_id = u.id
         WHERE c.verification_code = ?`,
        [code],
        async (err, results) => {
            if (err) return apiResponse(res, 500, 'Server error');
            if (results.length === 0) return apiResponse(res, 404, 'Certificate not found');

            const certificate = results[0];

            if (format === 'pdf') {
                try {
                    const doc = new PDFDocument({ layout: 'landscape', size: 'A4' });

                    res.setHeader('Content-Type', 'application/pdf');
                    res.setHeader('Content-Disposition', `attachment; filename=certificate_${code}.pdf`);

                    doc.pipe(res);

                    // --- PDF DESIGN ---
                    // Background border
                    doc.rect(20, 20, doc.page.width - 40, doc.page.height - 40).stroke('#667eea');
                    doc.rect(30, 30, doc.page.width - 60, doc.page.height - 60).stroke('#764ba2');

                    // Header
                    doc.font('Helvetica-Bold').fontSize(30).fillColor('#333333').text('CERTIFICATE OF ACHIEVEMENT', 0, 100, { align: 'center' });
                    doc.moveDown();

                    // Subheader
                    doc.font('Helvetica').fontSize(15).text('This is to certify that', { align: 'center' });
                    doc.moveDown();

                    // User Email/Name
                    doc.font('Helvetica-Bold').fontSize(25).fillColor('#667eea').text(certificate.email, { align: 'center' });
                    doc.moveDown();

                    // Body
                    doc.font('Helvetica').fontSize(15).fillColor('#333333').text('has successfully completed the requirements for', { align: 'center' });
                    doc.moveDown(0.5);

                    let certTypeDisplay = 'Volunteer Hours Milestone';
                    if (certificate.certificate_type === 'course_milestone') certTypeDisplay = 'Course Milestone';
                    if (certificate.certificate_type === 'creator_verified') certTypeDisplay = 'Verified Creator Status';

                    doc.font('Helvetica-Bold').fontSize(20).text(certTypeDisplay, { align: 'center' });
                    doc.moveDown();

                    if (certificate.hours_certified > 0) {
                        doc.font('Helvetica').fontSize(15).text(`Milestone: ${certificate.hours_certified} Hours`, { align: 'center' });
                        doc.moveDown(0.5);
                    }

                    if (certificate.total_volunteer_hours > 0) {
                        doc.font('Helvetica-Bold').fontSize(16).fillColor('#4a5568').text(`Total Lifetime Volunteer Hours: ${certificate.total_volunteer_hours}`, { align: 'center' });
                        doc.moveDown();
                    }

                    // Signature Line (Left Side)
                    const signatureY = 390;
                    doc.moveTo(100, signatureY + 50).lineTo(300, signatureY + 50).stroke('#999999');

                    // Load signature image - try multiple URLs as fallback
                    const signatureUrls = [
                        'https://virats-best.github.io/Veelearn/Signuture.png',
                        'https://virats-best.github.io/Veelearn/Signature.png'
                    ];
                    let signatureLoaded = false;
                    for (const signatureUrl of signatureUrls) {
                        if (signatureLoaded) break;
                        try {
                            debug('Trying signature from:', signatureUrl);
                            const response = await axios.get(signatureUrl, { responseType: 'arraybuffer', timeout: 8000 });
                            if (response.data && response.data.length > 100) {
                                doc.image(response.data, 120, signatureY - 15, { width: 150, height: 60 });
                                debug('✓ Signature loaded from:', signatureUrl);
                                signatureLoaded = true;
                            }
                        } catch (imgErr) {
                            console.error('Signature load failed from:', signatureUrl, imgErr.message);
                        }
                    }
                    if (!signatureLoaded) {
                        doc.font('Helvetica-BoldOblique').fontSize(18).fillColor('#333333').text('Virat Sisodiya', 120, signatureY + 5);
                    }

                    doc.font('Helvetica-Bold').fontSize(13).fillColor('#333333').text('Virat Sisodiya', 100, signatureY + 55, { align: 'left', width: 200 });
                    doc.font('Helvetica').fontSize(10).fillColor('#666666').text('Founder & Administrator, Veelearn', 100, signatureY + 72, { align: 'left', width: 250 });

                    // "Proof" section on right side
                    const proofX = 500;
                    doc.moveTo(proofX, signatureY + 50).lineTo(proofX + 250, signatureY + 50).stroke('#999999');
                    doc.font('Helvetica').fontSize(10).fillColor('#333333').text('Date of Issue', proofX, signatureY + 55, { align: 'center', width: 250 });
                    doc.font('Helvetica-Bold').fontSize(12).text(new Date(certificate.issued_at).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' }), proofX, signatureY + 35, { align: 'center', width: 250 });

                    // Footer / Verification (Moved to Absolute Bottom)
                    // Page height is ~595 in A4 Landscape (if inverted? pdfkit default is 72dpi, A4 is 595x842. Landscape 842x595)
                    // Let's position this near the bottom edge (e.g., Y=530)

                    doc.moveDown(5); // Just to reset flow if needed, but we use absolute pos below

                    const bottomY = 520;
                    doc.font('Helvetica').fontSize(10).fillColor('#333333');
                    doc.text(`Issued On: ${new Date(certificate.issued_at).toLocaleDateString()}`, 0, bottomY, { align: 'center' });
                    doc.text(`Verification Code: ${certificate.verification_code}`, 0, bottomY + 15, { align: 'center' });
                    const BASE_URL = process.env.APP_URL || 'https://veelearn.onrender.com';
                    doc.fillColor('#667eea').text('Verify at: ' + BASE_URL + '/api/certificates/verify/' + certificate.verification_code, 0, bottomY + 30, { align: 'center', link: BASE_URL + '/api/certificates/verify/' + certificate.verification_code });

                    doc.end();

                } catch (pdfErr) {
                    console.error('PDF Generation Error:', pdfErr);
                    return apiResponse(res, 500, 'Error generating PDF');
                }
            } else {
                apiResponse(res, 200, 'Certificate verified', certificate);
            }
        }
    );
});

app.get('/api/sponsorships', (req, res) => {
    db.query(
        'SELECT * FROM sponsorships WHERE expiry_date IS NULL OR expiry_date >= CURDATE() ORDER BY contribution_amount DESC',
        (err, results) => {
            if (err) return apiResponse(res, 500, 'Server error');
            apiResponse(res, 200, 'Sponsorships retrieved', results);
        }
    );
});

app.post('/api/sponsorships', authenticateToken, authorize('admin', 'superadmin'), (req, res) => {
    const { sponsor_name, logo_url, contribution_amount, tier, expiry_date } = req.body;
    if (!sponsor_name) return apiResponse(res, 400, 'Sponsor name required');

    db.query(
        'INSERT INTO sponsorships (sponsor_name, logo_url, contribution_amount, tier, expiry_date) VALUES (?, ?, ?, ?, ?)',
        [sponsor_name, logo_url || null, contribution_amount || 0, tier || 'silver', expiry_date || null],
        (err, result) => {
            if (err) return apiResponse(res, 500, 'Server error');
            apiResponse(res, 201, 'Sponsorship added', { id: result.insertId });
        }
    );
});

// ===== TEACHER/STUDENT SYSTEM =====

// Generate class code for teacher
const generateClassCode = () => {
    return Math.random().toString(36).substring(2, 8).toUpperCase();
};

// Request to become a teacher
app.post('/api/user/become-teacher', authenticateToken, (req, res) => {
    const userId = req.user.id;
    const classCode = generateClassCode();

    db.query(
        'UPDATE users SET role = ?, class_code = ?, teacher_approved = ? WHERE id = ?',
        ['teacher', classCode, false, userId],
        (err) => {
            if (err) return apiResponse(res, 500, 'Error updating role');

            // Send notification email (would be sent by admin)
            apiResponse(res, 200, 'Teacher request submitted. Awaiting superadmin approval.', { classCode });
        }
    );
});

// Superadmin approves teacher
app.put('/api/admin/approve-teacher/:userId', authenticateToken, authorize('superadmin'), (req, res) => {
    const { userId } = req.params;

    db.query(
        'UPDATE users SET teacher_approved = ? WHERE id = ?',
        [true, userId],
        (err) => {
            if (err) return apiResponse(res, 500, 'Error approving teacher');
            apiResponse(res, 200, 'Teacher approved');
        }
    );
});

// Get class code for teacher
app.get('/api/user/class-code', authenticateToken, (req, res) => {
    const userId = req.user.id;

    db.query(
        'SELECT class_code, teacher_approved FROM users WHERE id = ? AND role = ?',
        [userId, 'teacher'],
        (err, results) => {
            if (err) return apiResponse(res, 500, 'Error fetching class code');
            if (results.length === 0) return apiResponse(res, 404, 'Not a teacher');
            apiResponse(res, 200, 'Class code retrieved', {
                classCode: results[0].class_code,
                approved: results[0].teacher_approved
            });
        }
    );
});

// Student enrolls in class
app.post('/api/student/enroll-class', authenticateToken, (req, res) => {
    const { classCode } = req.body;
    const studentId = req.user.id;

    if (!classCode) return apiResponse(res, 400, 'Class code required');

    // Find teacher by class code
    db.query(
        'SELECT id FROM users WHERE class_code = ? AND role = ? AND teacher_approved = ?',
        [classCode, 'teacher', true],
        (err, teachers) => {
            if (err) return apiResponse(res, 500, 'Error finding teacher');
            if (teachers.length === 0) return apiResponse(res, 404, 'Invalid class code or teacher not approved');

            const teacherId = teachers[0].id;

            // Enroll student
            db.query(
                'INSERT INTO student_enrollments (student_id, class_code, teacher_id) VALUES (?, ?, ?) ON DUPLICATE KEY UPDATE enrolled_at = NOW()',
                [studentId, classCode, teacherId],
                (err) => {
                    if (err) {
                        if (err.code === 'ER_DUP_ENTRY') {
                            return apiResponse(res, 400, 'Already enrolled in this class');
                        }
                        return apiResponse(res, 500, 'Error enrolling in class');
                    }

                    // Update student role to 'student' if they were 'user'
                    db.query(
                        'UPDATE users SET role = ? WHERE id = ? AND role = ?',
                        ['student', studentId, 'user'],
                        (err) => {
                            if (err) {
                                console.warn('Warning: Could not update student role:', err);
                                // Don't fail the enrollment if role update fails
                            }
                            apiResponse(res, 200, 'Enrolled in class successfully');
                        }
                    );
                }
            );
        }
    );
});

// Teacher assigns course to class
app.post('/api/teacher/assign-course', authenticateToken, authorize('teacher'), (req, res) => {
    const { classCode, courseId, title, dueDate } = req.body;
    const teacherId = req.user.id;

    if (!classCode || !courseId) return apiResponse(res, 400, 'Class code and course ID required');

    // Verify teacher owns this class code
    db.query(
        'SELECT id FROM users WHERE id = ? AND class_code = ?',
        [teacherId, classCode],
        (err, results) => {
            if (err) return apiResponse(res, 500, 'Error verifying class');
            if (results.length === 0) return apiResponse(res, 403, 'Not authorized for this class');

            // Create assignment
            db.query(
                'INSERT INTO classroom_assignments (teacher_id, course_id, class_code, title, due_date) VALUES (?, ?, ?, ?, ?)',
                [teacherId, courseId, classCode, title || 'Course Assignment', dueDate || null],
                (err, result) => {
                    if (err) return apiResponse(res, 500, 'Error creating assignment');
                    apiResponse(res, 201, 'Assignment created', { assignmentId: result.insertId });
                }
            );
        }
    );
});

// Get assignments for student
app.get('/api/student/assignments', authenticateToken, (req, res) => {
    const studentId = req.user.id;

    db.query(`
        SELECT ca.*, u.email as teacher_email, c.title as course_title,
               asub.is_submitted
        FROM classroom_assignments ca
        JOIN student_enrollments se ON ca.class_code = se.class_code
        JOIN users u ON ca.teacher_id = u.id
        JOIN courses c ON ca.course_id = c.id
        LEFT JOIN assignment_submissions asub ON ca.id = asub.assignment_id AND asub.student_id = se.student_id
        WHERE se.student_id = ?
        ORDER BY ca.due_date ASC
    `, [studentId], (err, results) => {
        if (err) return apiResponse(res, 500, 'Error fetching assignments');
        apiResponse(res, 200, 'Assignments retrieved', results);
    });
});

// Submit assignment completion with quiz accuracy tracking
app.post('/api/student/submit-assignment', authenticateToken, (req, res) => {
    const { assignmentId, completionPercentage, correctAnswers, totalQuestions, quizAccuracy } = req.body;
    const studentId = req.user.id;

    if (!assignmentId) return apiResponse(res, 400, 'Assignment ID required');
    if (completionPercentage === undefined) return apiResponse(res, 400, 'Completion percentage required');

    // Get assignment details including course_id
    db.query(
        'SELECT due_date, course_id FROM classroom_assignments WHERE id = ?',
        [assignmentId],
        (err, assignments) => {
            if (err) return apiResponse(res, 500, 'Error fetching assignment');
            if (assignments.length === 0) return apiResponse(res, 404, 'Assignment not found');

            const assignment = assignments[0];
            const isLate = assignment.due_date && new Date() > new Date(assignment.due_date);
            const submissionDate = new Date();

            // If quiz score parameters are provided, use them directly
            if (correctAnswers !== undefined && totalQuestions !== undefined) {
                const finalQuizAccuracy = quizAccuracy !== undefined ? quizAccuracy : (totalQuestions > 0 ? (correctAnswers / totalQuestions) * 100 : 0);
                
                // Insert or update assignment submission with quiz score
                db.query(
                    `INSERT INTO assignment_submissions 
                     (assignment_id, student_id, submission_date, completion_percentage, is_submitted, is_late, correct_answers, total_questions, quiz_accuracy) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                     ON DUPLICATE KEY UPDATE 
                     completion_percentage = ?, submission_date = ?, is_submitted = ?, is_late = ?, correct_answers = ?, total_questions = ?, quiz_accuracy = ?`,
                    [assignmentId, studentId, submissionDate, completionPercentage, true, isLate, correctAnswers, totalQuestions, finalQuizAccuracy,
                        completionPercentage, submissionDate, true, isLate, correctAnswers, totalQuestions, finalQuizAccuracy],
                    (err) => {
                        if (err) {
                            console.error('Error submitting assignment:', err);
                            return apiResponse(res, 500, 'Error submitting assignment');
                        }
                        apiResponse(res, 200, 'Assignment submission recorded', {
                            isLate,
                            totalQuestions,
                            correctAnswers,
                            quizAccuracy: finalQuizAccuracy
                        });
                    }
                );
                return;
            }

            // Get total questions count for the course
            db.query(
                'SELECT COUNT(*) as totalQuestions FROM course_questions WHERE course_id = ?',
                [assignment.course_id],
                (err, countResults) => {
                    if (err) {
                        console.error('Error counting questions:', err);
                        const totalQuestions = 0;
                        const correctAnswers = 0;
                        const quizAccuracy = 0;
                        performSubmission(totalQuestions, correctAnswers, quizAccuracy);
                        return;
                    }

                    const totalQuestions = countResults[0].totalQuestions || 0;

                    // Get correct distinct answers count for this student on this course's questions
                    db.query(
                        `SELECT COUNT(DISTINCT uqa.question_id) as correctCount 
                         FROM user_quiz_attempts uqa
                         JOIN course_questions cq ON uqa.question_id = cq.id
                         WHERE uqa.user_id = ? AND cq.course_id = ? AND uqa.is_correct = TRUE`,
                        [studentId, assignment.course_id],
                        (err, accuracyResults) => {
                            if (err) {
                                console.error('Error counting correct answers:', err);
                                const correctAnswers = 0;
                                const quizAccuracy = 0;
                                performSubmission(totalQuestions, correctAnswers, quizAccuracy);
                                return;
                            }

                            const correctAnswers = accuracyResults[0].correctCount || 0;
                            const quizAccuracy = totalQuestions > 0 ? (correctAnswers / totalQuestions) * 100 : 0;

                            db.query(
                                `INSERT INTO assignment_submissions 
                                 (assignment_id, student_id, submission_date, completion_percentage, is_submitted, is_late, correct_answers, total_questions, quiz_accuracy) 
                                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                                 ON DUPLICATE KEY UPDATE 
                                 completion_percentage = ?, submission_date = ?, is_submitted = ?, is_late = ?, correct_answers = ?, total_questions = ?, quiz_accuracy = ?`,
                                [assignmentId, studentId, submissionDate, completionPercentage, true, isLate, correctAnswers, totalQuestions, quizAccuracy.toFixed(2),
                                    completionPercentage, submissionDate, true, isLate, correctAnswers, totalQuestions, quizAccuracy.toFixed(2)],
                                (err) => {
                                    if (err) {
                                        console.error('Error submitting assignment:', err);
                                        return apiResponse(res, 500, 'Error submitting assignment');
                                    }
                                    apiResponse(res, 200, 'Assignment submission recorded', {
                                        isLate,
                                        totalQuestions,
                                        correctAnswers,
                                        quizAccuracy: parseFloat(quizAccuracy.toFixed(2))
                                    });
                                }
                            );
                        }
                    );
                }
            );
        }
    );
});

// Get student's enrolled courses with progress tracking
// Uses the main 'enrollments' table (course-level enrollment), not 'student_enrollments' (classroom enrollment).
app.get('/api/student/enrolled-courses', authenticateToken, (req, res) => {
    const studentId = req.user.id;

    db.query(`
        SELECT 
            c.id as course_id, 
            c.title, 
            c.description,
            c.course_type,
            c.status,
            u.email as creator_email,
            e.enrolled_at,
            COUNT(DISTINCT ca.id) as total_assignments,
            COUNT(DISTINCT CASE WHEN asub.is_submitted = 1 THEN ca.id END) as completed_assignments,
            GROUP_CONCAT(DISTINCT JSON_OBJECT(
                'assignment_id', ca.id,
                'title', ca.title,
                'due_date', ca.due_date,
                'correct_answers', IFNULL(asub.correct_answers, 0),
                'total_questions', IFNULL(asub.total_questions, 0),
                'is_submitted', IFNULL(asub.is_submitted, 0)
            ) SEPARATOR '|||') as submissions_json,
            GROUP_CONCAT(DISTINCT JSON_OBJECT(
                'id', ca.id,
                'title', ca.title,
                'due_date', ca.due_date
            ) SEPARATOR '|||') as assignments_json
        FROM courses c
        JOIN enrollments e ON e.course_id = c.id AND e.user_id = ?
        LEFT JOIN users u ON u.id = c.creator_id
        LEFT JOIN classroom_assignments ca ON ca.course_id = c.id
        LEFT JOIN assignment_submissions asub ON ca.id = asub.assignment_id AND asub.student_id = e.user_id
        GROUP BY c.id, c.title, c.description, c.course_type, c.status, u.email, e.enrolled_at
        ORDER BY c.title ASC
    `, [studentId], (err, results) => {
        if (err) {
            console.error('Error fetching enrolled courses:', err);
            return apiResponse(res, 500, 'Error fetching enrolled courses');
        }

        // Parse JSON data and format response
        const formattedResults = results.map(row => ({
            course_id: row.course_id,
            title: row.title,
            description: row.description,
            course_type: row.course_type || 'single',
            status: row.status,
            creator_email: row.creator_email,
            enrolled_at: row.enrolled_at,
            total_assignments: row.total_assignments || 0,
            completed_assignments: row.completed_assignments || 0,
            assignments: row.assignments_json
                ? row.assignments_json.split('|||').map(a => JSON.parse(a))
                : [],
            submissions: row.submissions_json
                ? row.submissions_json.split('|||').map(s => JSON.parse(s))
                : []
        }));

        apiResponse(res, 200, 'Enrolled courses retrieved', formattedResults);
    });
});

// Get student submissions for teacher
app.get('/api/teacher/class/:classCode/submissions', authenticateToken, authorize('teacher'), (req, res) => {
    const { classCode } = req.params;
    const teacherId = req.user.id;

    db.query(`
SELECT
u.email,
    ca.title as assignment_title,
    asub.completion_percentage,
    asub.is_submitted,
    asub.is_late,
    asub.submission_date,
    ca.due_date,
    asub.correct_answers,
    asub.total_questions,
    asub.current_status
        FROM assignment_submissions asub
        JOIN users u ON asub.student_id = u.id
        JOIN classroom_assignments ca ON asub.assignment_id = ca.id
        WHERE ca.teacher_id = ? AND ca.class_code = ?
    ORDER BY ca.id, u.email
        `, [teacherId, classCode], (err, results) => {
        if (err) return apiResponse(res, 500, 'Error fetching submissions');

        // Format results with accuracy calculation
        const formatted = results.map(r => {
            let accuracy = null;
            let accuracyPercent = null;

            // Calculate accuracy if quiz questions exist
            if (r.total_questions > 0 && r.correct_answers !== null) {
                accuracy = r.correct_answers;
                accuracyPercent = Math.round((r.correct_answers / r.total_questions) * 100);
            }

            return {
                ...r,
                accuracy: accuracy,
                accuracy_percent: accuracyPercent,
                correct_answers: r.correct_answers,
                total_questions: r.total_questions,
                status: !r.is_submitted ? 'Not Started' : r.is_late ? 'Late' : 'On Time',
                current_status: r.current_status || 'Not Started',
                progressBar: `${r.completion_percentage}% `
            };
        });

        apiResponse(res, 200, 'Submissions retrieved', formatted);
    });
});

// Get teacher's classes and students
app.get('/api/teacher/my-classes', authenticateToken, authorize('teacher'), (req, res) => {
    const teacherId = req.user.id;

    // First get the teacher's class code from users table
    db.query(`
        SELECT class_code FROM users WHERE id = ? AND role = ?
    `, [teacherId, 'teacher'], (err, teacherResult) => {
        if (err) return apiResponse(res, 500, 'Error fetching teacher info');
        if (teacherResult.length === 0) return apiResponse(res, 404, 'Not a teacher');

        const classCode = teacherResult[0].class_code;
        if (!classCode) return apiResponse(res, 200, 'Classes retrieved', []);

        // Get all students in this teacher's class
        db.query(`
            SELECT DISTINCT u.id, u.email FROM student_enrollments se 
            JOIN users u ON se.student_id = u.id 
            WHERE se.class_code = ? AND se.teacher_id = ?
    `, [classCode, teacherId], (err, students) => {
            if (err) return apiResponse(res, 500, 'Error fetching students');

            const classData = [{
                classCode: classCode,
                studentCount: students?.length || 0,
                students: students || []
            }];

            apiResponse(res, 200, 'Classes retrieved', classData);
        });
    });
});

// Get student accuracy for a specific assignment
app.get('/api/student/:studentId/assignment/:assignmentId/accuracy', authenticateToken, (req, res) => {
    const { studentId, assignmentId } = req.params;
    const requestingUserId = req.user.id;

    // Verify user is requesting their own accuracy or is a teacher/admin
    if (parseInt(studentId) !== parseInt(requestingUserId) &&
        req.user.role !== 'teacher' && req.user.role !== 'admin' && req.user.role !== 'superadmin') {
        return apiResponse(res, 403, 'Unauthorized access to student accuracy');
    }

    // Get assignment course_id
    db.query(
        'SELECT course_id FROM classroom_assignments WHERE id = ?',
        [assignmentId],
        (err, assignments) => {
            if (err) return apiResponse(res, 500, 'Error fetching assignment');
            if (assignments.length === 0) return apiResponse(res, 404, 'Assignment not found');

            const courseId = assignments[0].course_id;

            // Get submission with accuracy data
            db.query(
                `SELECT correct_answers, total_questions, quiz_accuracy, completion_percentage,
    is_submitted, is_late, submission_date
                 FROM assignment_submissions 
                 WHERE assignment_id = ? AND student_id = ? `,
                [assignmentId, studentId],
                (err, submissions) => {
                    if (err) return apiResponse(res, 500, 'Error fetching submission');

                    if (submissions.length === 0) {
                        // No submission yet
                        return apiResponse(res, 200, 'No submission yet', {
                            assignmentId,
                            studentId,
                            correct_answers: 0,
                            total_questions: 0,
                            quiz_accuracy: 0,
                            is_submitted: false
                        });
                    }

                    const submission = submissions[0];
                    apiResponse(res, 200, 'Student accuracy retrieved', {
                        assignmentId,
                        studentId,
                        correct_answers: submission.correct_answers,
                        total_questions: submission.total_questions,
                        quiz_accuracy: submission.quiz_accuracy,
                        completion_percentage: submission.completion_percentage,
                        is_submitted: submission.is_submitted,
                        is_late: submission.is_late,
                        submission_date: submission.submission_date
                    });
                }
            );
        }
    );
});

// Get all students' accuracy for an assignment (teacher view)
app.get('/api/teacher/assignment/:assignmentId/student-accuracy', authenticateToken, authorize('teacher', 'admin', 'superadmin'), (req, res) => {
    const { assignmentId } = req.params;
    const teacherId = req.user.id;

    // Verify teacher owns this assignment
    db.query(
        'SELECT id, course_id FROM classroom_assignments WHERE id = ? AND teacher_id = ?',
        [assignmentId, teacherId],
        (err, assignments) => {
            if (err) return apiResponse(res, 500, 'Error fetching assignment');
            if (assignments.length === 0) return apiResponse(res, 403, 'Assignment not owned by this teacher');

            // Get all student submissions for this assignment
            db.query(
                `SELECT
asub.student_id,
    u.email as student_email,
    asub.correct_answers,
    asub.total_questions,
    asub.quiz_accuracy,
    asub.completion_percentage,
    asub.is_submitted,
    asub.is_late,
    asub.submission_date
                 FROM assignment_submissions asub
                 JOIN users u ON asub.student_id = u.id
                 WHERE asub.assignment_id = ?
    ORDER BY u.email ASC`,
                [assignmentId],
                (err, submissions) => {
                    if (err) return apiResponse(res, 500, 'Error fetching student submissions');

                    // Calculate aggregate statistics
                    const stats = {
                        totalStudents: submissions.length,
                        submittedCount: submissions.filter(s => s.is_submitted).length,
                        averageAccuracy: submissions.length > 0
                            ? (submissions.reduce((sum, s) => sum + (s.quiz_accuracy || 0), 0) / submissions.length).toFixed(2)
                            : 0,
                        lateSubmissions: submissions.filter(s => s.is_late).length
                    };

                    apiResponse(res, 200, 'Student accuracy for assignment retrieved', {
                        assignmentId,
                        statistics: stats,
                        students: submissions.map(s => ({
                            studentId: s.student_id,
                            studentEmail: s.student_email,
                            correctAnswers: s.correct_answers,
                            totalQuestions: s.total_questions,
                            quizAccuracy: s.quiz_accuracy,
                            completionPercentage: s.completion_percentage,
                            isSubmitted: s.is_submitted,
                            isLate: s.is_late,
                            submissionDate: s.submission_date
                        }))
                    });
                }
            );
        }
    );
});

// Update student active status/objective
app.post('/api/student/update-status', authenticateToken, (req, res) => {
    const { assignmentId, status } = req.body;
    const studentId = req.user.id;

    if (!assignmentId) return apiResponse(res, 400, 'Assignment ID required');
    if (!status) return apiResponse(res, 400, 'Status description required');

    // Check if a submission already exists for this student and assignment
    db.query(
        'SELECT id FROM assignment_submissions WHERE assignment_id = ? AND student_id = ?',
        [assignmentId, studentId],
        (err, results) => {
            if (err) return apiResponse(res, 500, 'Database error');

            if (results.length === 0) {
                // Insert a new record in assignment_submissions (not fully submitted, just tracking active status)
                db.query(
                    'INSERT INTO assignment_submissions (assignment_id, student_id, completion_percentage, is_submitted, current_status) VALUES (?, ?, ?, ?, ?)',
                    [assignmentId, studentId, 0, false, status],
                    (err) => {
                        if (err) return apiResponse(res, 500, 'Error setting status');
                        apiResponse(res, 200, 'Active status initialized', { status });
                    }
                );
            } else {
                // Update current_status on existing record
                db.query(
                    'UPDATE assignment_submissions SET current_status = ? WHERE assignment_id = ? AND student_id = ?',
                    [status, assignmentId, studentId],
                    (err) => {
                        if (err) return apiResponse(res, 500, 'Error updating status');
                        apiResponse(res, 200, 'Active status updated', { status });
                    }
                );
            }
        }
    );
});

// ===== SEARCH ROUTE =====
// Note: GET /api/search is defined earlier (with course_type, units_count, richer sim fields).

// ===== AI STUDY COACH (OpenRouter, Socratic) =====
// ===== LEARNER SHELL / GAMIFICATION =====
app.get('/api/learner/profile', authenticateToken, (req, res) => {
    learnerGamification.profile(req, res).catch((e) => {
        console.error('learner profile:', e);
        return apiResponse(res, 500, 'Failed to load profile');
    });
});
app.post('/api/learner/checkin', authenticateToken, writeLimiter, (req, res) => {
    learnerGamification.checkin(req, res).catch((e) => {
        console.error('learner checkin:', e);
        return apiResponse(res, 500, 'Check-in failed');
    });
});
app.post('/api/learner/reward-quiz', authenticateToken, writeLimiter, (req, res) => {
    learnerGamification.rewardQuiz(req, res).catch((e) => {
        console.error('learner reward-quiz:', e);
        return apiResponse(res, 500, 'Reward failed');
    });
});
app.get('/api/learner/store', authenticateToken, (req, res) => {
    learnerGamification.storeCatalog(req, res).catch((e) => {
        console.error('learner store:', e);
        return apiResponse(res, 500, 'Store failed');
    });
});
app.post('/api/learner/store/purchase', authenticateToken, writeLimiter, (req, res) => {
    learnerGamification.purchase(req, res).catch((e) => {
        console.error('learner purchase:', e);
        return apiResponse(res, 500, 'Purchase failed');
    });
});
app.post('/api/learner/equip', authenticateToken, writeLimiter, (req, res) => {
    learnerGamification.equip(req, res).catch((e) => {
        console.error('learner equip:', e);
        return apiResponse(res, 500, 'Equip failed');
    });
});
app.put('/api/learner/settings', authenticateToken, writeLimiter, (req, res) => {
    learnerGamification.updateSettings(req, res).catch((e) => {
        console.error('learner settings:', e);
        return apiResponse(res, 500, 'Settings failed');
    });
});
app.post('/api/learner/feedback', authenticateToken, writeLimiter, (req, res) => {
    learnerGamification.feedback(req, res).catch((e) => {
        console.error('learner feedback:', e);
        return apiResponse(res, 500, 'Feedback failed');
    });
});
app.get('/api/learner/feedback', authenticateToken, (req, res) => {
    learnerGamification.listFeedback(req, res).catch((e) => {
        console.error('learner feedback list:', e);
        return apiResponse(res, 500, 'Failed to load feedback');
    });
});

app.post('/api/ai/tutor/chat', aiTutorLimiter, authenticateToken, (req, res) => {
    aiTutorHandlers.chat(req, res).catch((e) => {
        console.error('ai tutor chat:', e);
        apiResponse(res, 500, 'Study coach error');
    });
});

app.get('/api/ai/tutor/history', aiTutorLimiter, authenticateToken, (req, res) => {
    aiTutorHandlers.history(req, res).catch((e) => {
        console.error('ai tutor history:', e);
        apiResponse(res, 500, 'Study coach error');
    });
});

// ===== AI EDITOR HELP (OpenRouter, structured actions) =====
app.post('/api/ai/editor-help', aiEditorHelpLimiter, authenticateToken, (req, res) => {
    aiEditorHelpHandlers.help(req, res).catch((e) => {
        console.error('ai editor help:', e);
        apiResponse(res, 500, 'AI Help error');
    });
});

app.get('/api/ai/editor-help/history', aiEditorHelpLimiter, authenticateToken, (req, res) => {
    aiEditorHelpHandlers.history(req, res).catch((e) => {
        console.error('ai editor help history:', e);
        apiResponse(res, 500, 'AI Help history error');
    });
});

app.delete('/api/ai/editor-help/history', aiEditorHelpLimiter, authenticateToken, (req, res) => {
    aiEditorHelpHandlers.clearHistory(req, res).catch((e) => {
        console.error('ai editor help clear:', e);
        apiResponse(res, 500, 'AI Help history error');
    });
});

// ===== SEO ENDPOINTS =====
// Sitemap.xml endpoint
app.get('/sitemap.xml', async (req, res) => {
    try {
        const baseUrl = 'https://veelearn.org';
        let sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n';
        sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n';
        
        // Static pages
        const staticPages = [
            { url: '/', priority: '1.0', changefreq: 'daily' },
            { url: '/blog.html', priority: '0.9', changefreq: 'daily' },
            { url: '/physics.html', priority: '0.8', changefreq: 'weekly' },
            { url: '/chemistry.html', priority: '0.8', changefreq: 'weekly' },
            { url: '/math.html', priority: '0.8', changefreq: 'weekly' },
            { url: '/simulators.html', priority: '0.8', changefreq: 'weekly' },
            { url: '/for-teachers.html', priority: '0.7', changefreq: 'weekly' },
            { url: '/for-students.html', priority: '0.7', changefreq: 'weekly' },
            { url: '/simulator-studio.html', priority: '0.7', changefreq: 'weekly' },
            { url: '/simulator-marketplace.html', priority: '0.8', changefreq: 'daily' },
        ];
        
        staticPages.forEach(page => {
            sitemap += `  <url>\n`;
            sitemap += `    <loc>${baseUrl}${page.url}</loc>\n`;
            sitemap += `    <lastmod>${new Date().toISOString().split('T')[0]}</lastmod>\n`;
            sitemap += `    <changefreq>${page.changefreq}</changefreq>\n`;
            sitemap += `    <priority>${page.priority}</priority>\n`;
            sitemap += `  </url>\n`;
        });
        
        // Dynamic courses
        const coursesQuery = 'SELECT id, updated_at FROM courses WHERE status = "approved"';
        pool.query(coursesQuery, (err, courses) => {
            if (err) {
                console.error('Error fetching courses for sitemap:', err);
                // Return sitemap with just static pages
                sitemap += '</urlset>';
                res.header('Content-Type', 'application/xml');
                res.send(sitemap);
                return;
            }
            
            courses.forEach(course => {
                sitemap += `  <url>\n`;
                sitemap += `    <loc>${baseUrl}/course-viewer.html?id=${course.id}</loc>\n`;
                sitemap += `    <lastmod>${course.updated_at ? course.updated_at.toISOString().split('T')[0] : new Date().toISOString().split('T')[0]}</lastmod>\n`;
                sitemap += `    <changefreq>weekly</changefreq>\n`;
                sitemap += `    <priority>0.7</priority>\n`;
                sitemap += `  </url>\n`;
            });
            
            sitemap += '</urlset>';
            res.header('Content-Type', 'application/xml');
            res.send(sitemap);
        });
    } catch (error) {
        console.error('Sitemap generation error:', error);
        res.status(500).send('Error generating sitemap');
    }
});

// Robots.txt endpoint
app.get('/robots.txt', (req, res) => {
    const robotsTxt = `User-agent: *
Allow: /
Disallow: /api/
Disallow: /dashboard
Disallow: /course-editor
Disallow: /auth

Sitemap: https://veelearn.org/sitemap.xml
`;
    res.header('Content-Type', 'text/plain');
    res.send(robotsTxt);
});

// ===== AI CALENDAR PARSING =====

async function parsePostForCalendarEvents(postId, content, classId, authorId) {
    try {
        const openRouterKeys = getOpenRouterKeys();
        if (!openRouterKeys.length) {
            console.warn('No OpenRouter keys for calendar parsing');
            return;
        }

        const prompt = `Extract dates and events from this post. Look for:
- Absolute dates: "Monday", "January 15", "2024-01-15"
- Relative dates: "tomorrow", "today", "next week", "next Monday", "in 2 days"
- Times: "4:59PM", "5:00 PM", "at 3pm"
- Keywords indicating events: "due", "deadline", "HW", "homework", "test", "exam", "assignment", "quiz", "project"

For relative dates like "tomorrow", calculate the actual date based on today's date (${new Date().toISOString().split('T')[0]}).

Return ONLY valid JSON in this format:
{
  "events": [
    {
      "title": "Event Title",
      "description": "Event description",
      "event_date": "YYYY-MM-DD",
      "event_type": "assignment|exam|event"
    }
  ]
}

Post: ${content}

If no dates are found, return {"events": []}.`;

        // Try multiple models as fallbacks (openRouterChatCompletion also has built-in fallbacks)
        const models = [
            process.env.OPENROUTER_MODEL || 'google/gemma-4-31b-it:free',
            'google/gemma-4-26b-a4b-it:free',
            'openrouter/free'
        ];

        let response = null;
        let lastError = null;

        for (const model of models) {
            try {
                console.log(`[Calendar AI] Trying model: ${model}`);
                response = await openRouterChatCompletion([{ role: 'user', content: prompt }], { max_tokens: 500, model });
                if (response) {
                    console.log(`[Calendar AI] Successfully got response from model: ${model}`);
                    break;
                }
            } catch (error) {
                console.error(`[Calendar AI] Model ${model} failed:`, error.message);
                lastError = error;
            }
        }

        if (!response) {
            console.error('[Calendar AI] All models failed, last error:', lastError?.message);
            console.error('[Calendar AI] Post will be created without calendar events');
            return;
        }

        const aiResponse = response.content || response;
        
        if (!aiResponse) {
            console.error('[Calendar AI] OpenRouter response content is empty');
            return;
        }
        
        if (typeof aiResponse !== 'string') {
            console.error('[Calendar AI] OpenRouter response is not a string:', typeof aiResponse);
            return;
        }

        console.log('[Calendar AI] AI Response:', aiResponse);

        // Strip markdown code blocks from response
        let cleanResponse = aiResponse;
        if (aiResponse.includes('```json')) {
            cleanResponse = aiResponse.replace(/```json\s*([\s\S]*?)\s*```/g, '$1');
        } else if (aiResponse.includes('```')) {
            cleanResponse = aiResponse.replace(/```\s*([\s\S]*?)\s*```/g, '$1');
        }

        let parsed;
        try {
            parsed = JSON.parse(cleanResponse);
        } catch (error) {
            console.error('[Calendar AI] Failed to parse response as JSON:', error);
            console.error('[Calendar AI] Response content:', aiResponse);
            console.error('[Calendar AI] Cleaned response:', cleanResponse);
            return;
        }

        if (parsed.events && parsed.events.length > 0) {
            for (const event of parsed.events) {
                try {
                    await query(
                        'INSERT INTO calendar_events (title, event_date, event_type, class_id, post_id) VALUES (?, ?, ?, ?, ?)',
                        [event.title, event.event_date, event.event_type, classId, postId]
                    );
                    console.log(`[Calendar AI] Added event: ${event.title} on ${event.event_date}`);
                } catch (dbError) {
                    console.error('[Calendar AI] Error inserting event:', dbError);
                }
            }
            console.log(`[Calendar AI] Added ${parsed.events.length} calendar events from post ${postId}`);
        } else {
            console.log(`[Calendar AI] No events found in post ${postId}`);
        }
    } catch (error) {
        console.error('[Calendar AI] Error parsing post for calendar events:', error);
    }
}

// ===== ERROR HANDLING =====
app.use((err, req, res, next) => {
    console.error('Unhandled error:', err);
    apiResponse(res, 500, 'Internal server error');
});

// ===== START SERVER =====
const PORT = process.env.PORT || 3000;
const server = app.listen(PORT, () => {
    info(`Server running on port ${PORT} `);
    info(`Environment: ${process.env.NODE_ENV || 'development'} `);
    if (getOpenRouterKeys().length) {
        debug('✓ OpenRouter API keys loaded for study coach');
    } else {
        console.warn('ℹ️ No OPENROUTER_API_KEYS — study coach disabled until keys are set (see .env.example)');
    }
});

// WebSocket Server for real-time messaging
const wss = new WebSocket.Server({ server });

// Store connected users with their userId
const connectedUsers = new Map();

wss.on('connection', (ws, req) => {
    // Extract token from query string
    const url = new URL(req.url, `http://${req.headers.host}`);
    const token = url.searchParams.get('token');

    if (!token) {
        ws.close(1008, 'No token provided');
        return;
    }

    // Verify token and get user info
    jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
        if (err) {
            ws.close(1008, 'Invalid token');
            return;
        }

        const userId = user.id;
        connectedUsers.set(userId, ws);

        ws.on('message', async (message) => {
            try {
                const data = JSON.parse(message);

                // Handle message sending
                if (data.type === 'send_message') {
                    const { recipient_id, content } = data;

                    // Save message to database
                    const insertMessage = 'INSERT INTO messages (sender_id, recipient_id, content) VALUES (?, ?, ?)';
                    db.query(insertMessage, [userId, recipient_id, content], (err, result) => {
                        if (err) {
                            ws.send(JSON.stringify({ type: 'error', message: 'Failed to send message' }));
                            return;
                        }

                        const messageData = {
                            type: 'new_message',
                            message_id: result.insertId,
                            sender_id: userId,
                            recipient_id,
                            content,
                            created_at: new Date().toISOString()
                        };

                        // Send to recipient if online
                        const recipientWs = connectedUsers.get(recipient_id);
                        if (recipientWs && recipientWs.readyState === WebSocket.OPEN) {
                            recipientWs.send(JSON.stringify(messageData));
                        }

                        // Confirm to sender
                        ws.send(JSON.stringify({ type: 'message_sent', message_id: result.insertId }));
                    });
                }

                // Handle typing indicator
                if (data.type === 'typing') {
                    const { recipient_id, is_typing } = data;
                    const recipientWs = connectedUsers.get(recipient_id);
                    if (recipientWs && recipientWs.readyState === WebSocket.OPEN) {
                        recipientWs.send(JSON.stringify({
                            type: 'typing',
                            sender_id: userId,
                            is_typing
                        }));
                    }
                }

                // Handle message read status
                if (data.type === 'mark_read') {
                    const { message_id } = data;
                    db.query('UPDATE messages SET is_read = TRUE WHERE id = ? AND recipient_id = ?', [message_id, userId]);
                }

                // Join a workspace module room
                if (data.type === 'join_module') {
                    const { moduleId } = data;
                    ws.moduleId = moduleId;
                    ws.userId = userId;
                    
                    wss.clients.forEach(client => {
                        if (client !== ws && client.moduleId === moduleId && client.readyState === WebSocket.OPEN) {
                            client.send(JSON.stringify({
                                type: 'user_joined',
                                userId: userId,
                                userEmail: user.email
                            }));
                        }
                    });
                    
                    ws.send(JSON.stringify({ type: 'joined_module', moduleId }));
                }

                // Sync block positions and connections
                if (data.type === 'sync_blocks') {
                    const { moduleId, blocks, connections } = data;
                    wss.clients.forEach(client => {
                        if (client !== ws && client.moduleId === moduleId && client.readyState === WebSocket.OPEN) {
                            client.send(JSON.stringify({
                                type: 'sync_blocks',
                                blocks,
                                connections,
                                userId
                            }));
                        }
                    });
                }

                // Lock individual blocks during edit
                if (data.type === 'lock_block') {
                    const { moduleId, blockId } = data;
                    wss.clients.forEach(client => {
                        if (client !== ws && client.moduleId === moduleId && client.readyState === WebSocket.OPEN) {
                            client.send(JSON.stringify({
                                type: 'lock_block',
                                blockId,
                                userId,
                                userEmail: user.email
                            }));
                        }
                    });
                }

                // Unlock individual blocks after edit
                if (data.type === 'unlock_block') {
                    const { moduleId, blockId } = data;
                    wss.clients.forEach(client => {
                        if (client !== ws && client.moduleId === moduleId && client.readyState === WebSocket.OPEN) {
                            client.send(JSON.stringify({
                                type: 'unlock_block',
                                blockId,
                                userId
                            }));
                        }
                    });
                }

                // Update active student status / objective
                if (data.type === 'update_status') {
                    const { assignmentId, status } = data;
                    db.query(
                        'INSERT INTO assignment_submissions (assignment_id, student_id, completion_percentage, is_submitted, current_status) VALUES (?, ?, 0, FALSE, ?) ON DUPLICATE KEY UPDATE current_status = ?',
                        [assignmentId, userId, status, status],
                        (err) => {
                            if (err) {
                                console.error('Error updating status via WS:', err);
                            } else {
                                wss.clients.forEach(client => {
                                    if (client.readyState === WebSocket.OPEN) {
                                        client.send(JSON.stringify({
                                            type: 'student_status_update',
                                            studentId: userId,
                                            studentEmail: user.email,
                                            assignmentId,
                                            status
                                        }));
                                    }
                                });
                            }
                        }
                    );
                }
            } catch (error) {
                console.error('WebSocket message error:', error);
            }
        });

        ws.on('close', () => {
            connectedUsers.delete(userId);
        });

        ws.on('error', (error) => {
            console.error('WebSocket error:', error);
        });
    });
});
