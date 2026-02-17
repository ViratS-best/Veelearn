const express = require('express');
const mysql = require('mysql2');
const dotenv = require('dotenv');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const cookieParser = require('cookie-parser');
const cors = require('cors');
const path = require('path');
const nodemailer = require('nodemailer');

const util = require('util');
const PDFDocument = require('pdfkit');
const fs = require('fs');
const axios = require('axios');
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
    console.log('✓ Brevo API key configured - using HTTP-based email delivery');
} else {
    console.log('ℹ️ No BREVO_API_KEY set, trying Gmail SMTP...');
}

if (process.env.SMTP_EMAIL && process.env.SMTP_PASSWORD) {
    smtpTransporter.verify()
        .then(() => { smtpReady = true; console.log('✓ SMTP email service ready (fallback)'); })
        .catch(err => console.warn('⚠️ SMTP unavailable:', err.message, '(port likely blocked)'));
} else if (!brevoApiKey) {
    console.warn('⚠️ No email provider configured. Set BREVO_API_KEY or SMTP_EMAIL+SMTP_PASSWORD.');
}

async function sendEmail({ to, subject, html }) {
    const senderEmail = process.env.SMTP_EMAIL || 'noreply@veelearn.com';
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
            }
        });
        if (response.status >= 400) throw new Error(`Brevo error: ${response.statusText}`);
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


// Check for critical environment variables
if (!process.env.JWT_SECRET) {
    console.error('❌ FATAL ERROR: JWT_SECRET is not defined.');
    console.error('   Please add JWT_SECRET to your environment variables.');
    process.exit(1);
}

app.use(express.json({ limit: '50mb' }));
app.use(cookieParser());
app.use(cors({
    origin: [
        'http://localhost:5500',
        'http://127.0.0.1:5500',
        'https://virat-sisodiya.github.io', // Assuming this based on common GH pages patterns
        /\.github\.io$/ // Allow any github.io subdomains
    ],
    credentials: true,
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization', 'Cookie']
}));

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
    queueLimit: 0
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
        console.log(`📡 Attempting to connect to database at ${dbConfig.host}:${dbConfig.port}`);
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
        console.log(`Database '${dbConfig.database}' verified/created`);

        // 2. Create tables in proper order
        console.log('Initializing tables...');

        // Users table (Parent)
        await query(`
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                role ENUM('superadmin', 'admin', 'teacher', 'user') DEFAULT 'user',
                is_admin_approved BOOLEAN DEFAULT FALSE,
                shells INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_email (email),
                INDEX idx_role (role)
            )
        `);
        console.log('✓ Users table ready');

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
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (creator_id) REFERENCES users(id) ON DELETE CASCADE,
                INDEX idx_status (status),
                INDEX idx_creator (creator_id)
            )
        `);
        console.log('✓ Courses table ready');

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
                                console.log(`✓ Added column ${column} to ${table}`);
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

        // Migration: Add volunteer columns to users table
        await addColumn('users', 'total_volunteer_hours', 'FLOAT DEFAULT 0');
        await addColumn('users', 'is_verified_creator', 'BOOLEAN DEFAULT FALSE');

        // Migration: Add teacher-specific columns
        await addColumn('users', 'class_code', 'VARCHAR(20) UNIQUE');
        await addColumn('users', 'teacher_approved', 'BOOLEAN DEFAULT FALSE');
        console.log('✓ Teacher columns verified/added to users table');

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
        console.log('✓ Classroom assignments table ready');

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
        console.log('✓ Student enrollments table ready');

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
        console.log('✓ Assignment submission columns verified');
        await query(`
            ALTER TABLE assignment_submissions ADD COLUMN IF NOT EXISTS quiz_accuracy DECIMAL(5,2) DEFAULT 0
        `);
        // Migration: Add unique constraint to quiz attempts if not already present
        // Note: Generic try/catch because MySQL 8.0 doesn't support IF NOT EXISTS for ADD UNIQUE
        try {
            await query(`ALTER TABLE user_quiz_attempts ADD UNIQUE KEY unique_attempt (user_id, question_id)`);
            console.log('✓ Unique constraint added to user_quiz_attempts');
        } catch (e) {
            // Likely already exists
        }

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
        console.log('✓ Simulators table ready');

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
        console.log('✓ User-Course relationship tables ready');

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
        console.log('✓ Simulator dependent tables ready');

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
                question_text TEXT NOT NULL,
                question_type ENUM('multiple_choice', 'true_false', 'short_answer') DEFAULT 'multiple_choice',
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
        console.log('✓ Sponsorships table ready');

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
        console.log('✓ Certificates table ready');

        console.log('✓ All tables initialized successfully');

        // Check for superadmin
        const superadminEmail = process.env.SUPERADMIN_EMAIL || 'viratsuper6@gmail.com';
        const superadminPassword = process.env.SUPERADMIN_PASSWORD || 'Virat@123';

        const superadmins = await query('SELECT * FROM users WHERE email = ?', [superadminEmail]);
        if (superadmins.length === 0) {
            const hashedPassword = await bcrypt.hash(superadminPassword, 10);
            await query('INSERT INTO users (email, password, role, is_admin_approved) VALUES (?, ?, \'superadmin\', TRUE)',
                [superadminEmail, hashedPassword]);
            console.log('✓ Superadmin created successfully');
        } else {
            console.log('✓ Superadmin already exists');
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

// JWT authentication middleware
const authenticateToken = (req, res, next) => {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];

    if (!token) {
        return apiResponse(res, 401, 'Access token required');
    }

    jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
        if (err) {
            // If token in header is invalid, try cookie
            const cookieToken = req.cookies.token;
            if (cookieToken) {
                return jwt.verify(cookieToken, process.env.JWT_SECRET, (err2, user2) => {
                    if (err2) {
                        console.error('❌ JWT Cookie Verification Error:', err2.message);
                        return apiResponse(res, 403, 'Invalid or expired session');
                    }
                    req.user = user2;
                    return next();
                });
            }
            console.error('❌ JWT Verification Error:', err.message);
            return apiResponse(res, 403, 'Invalid or expired token');
        }
        req.user = user;
        next();
    });
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
const authorize = (...roles) => {
    return (req, res, next) => {
        if (!roles.includes(req.user.role)) {
            return apiResponse(res, 403, 'Insufficient permissions');
        }
        next();
    };
};

// Rate limiting setup (basic implementation)
const loginAttempts = new Map();
const rateLimiter = (req, res, next) => {
    const ip = req.ip;
    const now = Date.now();
    const windowMs = 15 * 60 * 1000; // 15 minutes
    const maxAttempts = 50; // INCREASED for testing - was 5

    if (!loginAttempts.has(ip)) {
        loginAttempts.set(ip, { count: 1, resetTime: now + windowMs });
        console.log(`✓ Rate limiter: New IP ${ip}, attempts: 1/${maxAttempts}`);
        return next();
    }

    const attempts = loginAttempts.get(ip);
    if (now > attempts.resetTime) {
        loginAttempts.set(ip, { count: 1, resetTime: now + windowMs });
        console.log(`✓ Rate limiter: Reset for IP ${ip}, attempts: 1/${maxAttempts}`);
        return next();
    }

    if (attempts.count >= maxAttempts) {
        console.error(`❌ Rate limit exceeded for IP ${ip}: ${attempts.count}/${maxAttempts}`);
        return apiResponse(res, 429, 'Too many attempts. Please try again later.');
    }

    attempts.count++;
    console.log(`✓ Rate limiter: IP ${ip}, attempts: ${attempts.count}/${maxAttempts}`);
    next();
};

// ===== ROUTES =====

// Basic Route
app.get('/', (req, res) => {
    res.send('Veelearn Backend API is running!');
});

// ===== AUTHENTICATION ROUTES =====
app.post('/api/register', rateLimiter, async (req, res) => {
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
            app.post('/api/logout', (req, res) => {
                res.clearCookie('token');
                apiResponse(res, 200, 'Logged out successfully');
            });

            apiResponse(res, 201, 'User registered successfully', { token, user: newUser });
        });
    } catch (error) {
        console.error('Hashing error:', error);
        apiResponse(res, 500, 'Server error');
    }
});

app.post('/api/login', rateLimiter, async (req, res) => {
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

// ===== FORGOT / RESET PASSWORD =====
const resetCodes = new Map(); // email -> { code, expiresAt }

app.post('/api/forgot-password', rateLimiter, async (req, res) => {
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
                console.log(`✓ Password reset code sent to ${email}`);
            } catch (emailErr) {
                console.error('❌ Failed to send reset email:', emailErr.message);
                return apiResponse(res, 500, 'Failed to send reset email. Please try again later.');
            }
        } else {
            console.log(`⚠️ Password reset requested for non-existent email: ${email}`);
        }

        // Always return success (don't reveal if email exists)
        apiResponse(res, 200, 'If an account with that email exists, a reset code has been sent.');
    } catch (error) {
        console.error('Forgot password error:', error);
        apiResponse(res, 500, 'Server error');
    }
});

app.post('/api/reset-password', rateLimiter, async (req, res) => {
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

        console.log(`✓ Password reset successful for ${email}`);
        apiResponse(res, 200, 'Password reset successfully! You can now log in with your new password.');
    } catch (error) {
        console.error('Reset password error:', error);
        apiResponse(res, 500, 'Server error');
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
    db.query('SELECT id, email, role, is_admin_approved, shells, total_volunteer_hours, is_verified_creator, created_at FROM users', (err, results) => {
        if (err) {
            console.error('Error fetching users:', err);
            return apiResponse(res, 500, 'Server error fetching users');
        }
        apiResponse(res, 200, 'Users fetched successfully', results);
    });
});

app.get('/api/superadmin/users', authenticateToken, authorize('superadmin', 'admin'), (req, res) => {
    db.query('SELECT id, email, role, is_admin_approved, shells, total_volunteer_hours, is_verified_creator, created_at FROM users', (err, results) => {
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
app.post('/api/courses', authenticateToken, (req, res) => {
    const { title, description, content, blocks, status, creation_time } = req.body;
    const creator_id = req.user.id;

    console.log('📝 CREATE COURSE DEBUG:');
    console.log('  User ID:', creator_id);
    console.log('  Title:', title);
    console.log('  Description:', description ? 'YES' : 'NO');
    console.log('  Content length:', content ? content.length : 0, 'chars');
    console.log('  Blocks count:', Array.isArray(blocks) ? blocks.length : 'NOT PROVIDED');
    console.log('  Status:', status || 'draft');

    if (!title) {
        return apiResponse(res, 400, 'Course title is required');
    }

    if (title.length > 255) {
        return apiResponse(res, 400, 'Course title too long (max 255 characters)');
    }

    // Use provided status or default to 'draft'
    const courseStatus = status || 'draft';
    const blocksJson = blocks ? (typeof blocks === 'string' ? blocks : JSON.stringify(blocks)) : '[]';

    const creationTime = parseInt(creation_time) || 0;
    console.log('  Database:', dbConfig.database);
    console.log('  Host:', dbConfig.host);

    const insertCourseQuery = 'INSERT INTO courses (title, description, content, blocks, creator_id, status, creation_time) VALUES (?, ?, ?, ?, ?, ?, ?)';
    db.query(insertCourseQuery, [title, description || '', content || '', blocksJson, creator_id, courseStatus, creationTime], (err, result) => {
        if (err) {
            console.error('❌ Error creating course:', err);
            return apiResponse(res, 500, 'Server error creating course', { details: err.message });
        }

        const newCourseId = result.insertId;
        console.log('✅ Course created with ID:', newCourseId, 'Status:', courseStatus);
        console.log('  Database:', dbConfig.database);
        console.log('  Host:', dbConfig.host);

        // Auto-grant volunteer hours from tracked creation time
        if (creationTime > 0) {
            const addedHours = parseFloat((creationTime / 3600).toFixed(2));
            if (addedHours >= 0.01) {
                db.query(
                    'UPDATE users SET total_volunteer_hours = total_volunteer_hours + ? WHERE id = ?',
                    [addedHours, creator_id],
                    (volErr) => {
                        if (volErr) console.error('Error auto-granting volunteer hours:', volErr.message);
                        else console.log(`✓ Auto-granted ${addedHours}h volunteer hours to user ${creator_id} from tracked time`);
                    }
                );
            }
        }

        // VERIFY the course was actually inserted
        console.log('  Verifying course was inserted...');
        db.query('SELECT id, title FROM courses WHERE id = ?', [newCourseId], (verifyErr, verifyResults) => {
            if (verifyErr) {
                console.error('  ❌ Verification query failed:', verifyErr.message);
                return apiResponse(res, 500, 'Course created but verification failed', { details: verifyErr.message, id: newCourseId });
            }
            if (verifyResults.length === 0) {
                console.error('  ❌ CRITICAL: Course inserted but SELECT returned 0 rows!');
                console.log('  Checking all courses:');
                db.query('SELECT COUNT(*) as count FROM courses', (countErr, countResults) => {
                    const count = countErr ? 'ERROR' : countResults[0].count;
                    console.log('  Total courses in DB:', count);
                    apiResponse(res, 201, `Course created (ID: ${newCourseId}) but verification failed!`, { id: newCourseId, courseId: newCourseId });
                });
            } else {
                console.log('  ✓ Verification successful - course exists in DB');
                apiResponse(res, 201, `Course created successfully with status: ${courseStatus}`, { id: newCourseId, courseId: newCourseId });
            }
        });
    });
});


// Get all courses in system for teacher assignment (with pagination/search)
app.get('/api/courses/all', authenticateToken, (req, res) => {
    const { page = 1, limit = 10, search = '' } = req.query;
    const offset = (parseInt(page) - 1) * parseInt(limit);

    // Base query to get all approved courses + user's own courses
    const countQuery = `
        SELECT COUNT(*) as total FROM courses c
        LEFT JOIN users u ON c.creator_id = u.id
        WHERE c.status = 'approved' OR c.creator_id = ?
    ${search ? `AND (c.title LIKE ? OR c.description LIKE ?)` : ''}
`;

    const dataQuery = `
        SELECT c.id, c.title, c.description, c.creator_id, u.email as creator_email, c.status, c.created_at
        FROM courses c
        LEFT JOIN users u ON c.creator_id = u.id
        WHERE c.status = 'approved' OR c.creator_id = ?
    ${search ? `AND (c.title LIKE ? OR c.description LIKE ?)` : ''}
        ORDER BY c.created_at DESC
LIMIT ? OFFSET ?
    `;

    const searchTerm = search ? `%${search}%` : null;
    const countParams = search ? [req.user.id, searchTerm, searchTerm] : [req.user.id];
    const dataParams = search
        ? [req.user.id, searchTerm, searchTerm, parseInt(limit), offset]
        : [req.user.id, parseInt(limit), offset];

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

app.get('/api/courses/:id', authenticateToken, (req, res) => {
    const courseId = req.params.id;
    const userId = req.user.id;
    const userRole = req.user.role;

    console.log('📖 GET COURSE DEBUG:');
    console.log('  Course ID:', courseId);
    console.log('  User ID:', userId);
    console.log('  Database:', dbConfig.database);

    const query = `
        SELECT id, title, description, content, blocks, creator_id, status, is_paid, shells_cost, feedback, creation_time
        FROM courses
        WHERE id = ?
    `;

    db.query(query, [courseId], (err, results) => {
        if (err) {
            console.error('❌ Error fetching single course:', err);
            return apiResponse(res, 500, 'Server error fetching course');
        }
        if (results.length === 0) {
            console.log('  ❌ Course not found (query returned 0 results)');
            return apiResponse(res, 404, 'Course not found');
        }
        console.log('  ✓ Course found:', results[0].title);

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
app.put('/api/courses/:id', authenticateToken, (req, res) => {
    const courseId = req.params.id;
    const userId = req.user.id;
    const { title, description, content, blocks, status, creation_time } = req.body;

    console.log('📝 UPDATE COURSE DEBUG:');
    console.log('  Course ID:', courseId);
    console.log('  User ID:', userId);
    console.log('  Title:', title);
    console.log('  Content length:', content ? content.length : 0, 'chars');
    console.log('  Blocks count:', Array.isArray(blocks) ? blocks.length : 'NOT PROVIDED');
    console.log('  Status:', status || 'unchanged');
    console.log('  Database:', dbConfig.database);
    console.log('  Host:', dbConfig.host);

    if (!title) {
        return apiResponse(res, 400, 'Course title is required');
    }

    // Check if course exists
    db.query('SELECT * FROM courses WHERE id = ?', [courseId], (err, results) => {
        if (err) {
            console.error('❌ Error fetching course:', err);
            console.error('  Full error:', err.message, err.code);
            return apiResponse(res, 500, 'Server error', { error: err.message });
        }
        if (results.length === 0) {
            console.log('❌ Course not found in database. Query returned 0 results.');
            console.log('  Querying all courses to debug:');
            db.query('SELECT id FROM courses LIMIT 5', (err2, allCourses) => {
                console.log('  All courses in DB:', allCourses ? allCourses.map(c => c.id) : 'ERROR');
            });
            return apiResponse(res, 404, 'Course not found');
        }

        const course = results[0];
        console.log('  Course found - creator_id:', course.creator_id, 'current user:', userId);
        if (parseInt(course.creator_id) !== parseInt(userId)) {
            console.log('  ❌ Authorization failed - not course creator');
            return apiResponse(res, 403, 'You can only edit your own courses');
        }
        console.log('  ✓ Authorization passed');

        // Prepare blocks JSON
        const blocksJson = blocks ? (typeof blocks === 'string' ? blocks : JSON.stringify(blocks)) : undefined;

        // Update with optional status parameter
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

        updateQuery += ' WHERE id = ?';
        params.push(courseId);

        db.query(updateQuery, params, (err, result) => {
            if (err) {
                console.error('❌ Error updating course:', err);
                return apiResponse(res, 500, 'Server error updating course', { details: err.message });
            }
            console.log('✅ Course updated - ID:', courseId, 'Status:', status || 'unchanged');

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
                                else console.log(`✓ Auto-granted ${addedHours}h volunteer hours to user ${userId} from tracked time`);
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
        console.log(`DEBUG DELETE: Course ${courseId}, Creator: ${course.creator_id}, User: ${userId}, Role: ${req.user.role}`);

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
    // Show approved courses from everyone + own courses (even if pending)
    const query = `
SELECT c.id, c.title, c.description, c.content, c.blocks, c.creator_id, c.status, c.is_paid, c.shells_cost, c.creation_time, u.email as creator_email
FROM courses c
LEFT JOIN users u ON c.creator_id = u.id
WHERE c.status = 'approved' OR c.creator_id = ?
ORDER BY c.created_at DESC
`;

    db.query(query, [userId], (err, results) => {
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

app.get('/api/users/:userId/courses', authenticateToken, (req, res) => {
    const userId = req.params.userId;

    if (parseInt(req.user.id) !== parseInt(userId) && req.user.role !== 'admin' && req.user.role !== 'superadmin') {
        return apiResponse(res, 403, 'Access denied. You can only view your own courses');
    }

    const query = 'SELECT id, title, description, content, blocks, creator_id, status, is_paid, shells_cost, feedback, creation_time FROM courses WHERE creator_id = ?';
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
    const query = "SELECT c.id, c.title, c.description, c.content, c.blocks, c.creator_id, u.email as creator_email, c.created_at FROM courses c JOIN users u ON c.creator_id = u.id WHERE c.status = 'pending'";

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
        SELECT c.id, c.title, c.description, c.content, c.blocks, c.creator_id, 
               u.email as creator_email, c.status, c.created_at, c.feedback
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
                        console.log(`Awarded ${shellsAwarded} shells to user ${currentCourse.creator_id} for course approval.`);
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
        console.log(`DEBUG ENROLL: Course found: ${course.title}, paid: ${course.is_paid}, cost: ${course.shells_cost}`);

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
                    console.log(`DEBUG ENROLL: Deducting ${course.shells_cost} shells from user ${userId}`);
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
                console.log(`DEBUG ENROLL: Inserting enrollment for user ${userId}, course ${courseId}`);
                db.query('INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)', [userId, courseId], (err) => {
                    if (err) {
                        console.error('Error enrolling user:', err);
                        return apiResponse(res, 500, 'Server error enrolling in course');
                    }
                    console.log(`DEBUG ENROLL: Successfully enrolled user ${userId}`);
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

// Get all public simulators (paginated)
app.get('/api/simulators', (req, res) => {
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 20;
    const offset = (page - 1) * limit;
    const search = req.query.search || '';
    const tags = req.query.tags || '';
    const sort = req.query.sort || 'newest'; // newest, popular, rating

    let whereClause = "WHERE 1=1";
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
            s.preview_image, s.is_public, s.created_at, s.updated_at
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

        apiResponse(res, 200, 'Simulator fetched successfully', simulator);
    });
});

// Create new simulator
app.post('/api/simulators', authenticateToken, (req, res) => {
    const { title, description, blocks, connections, tags, preview_image, is_public, status } = req.body;
    const creator_id = req.user.id;

    console.log('📝 CREATE SIMULATOR DEBUG:');
    console.log('  User ID:', creator_id);
    console.log('  Title:', title);
    console.log('  Blocks count:', Array.isArray(blocks) ? blocks.length : 'NOT AN ARRAY');
    console.log('  Connections count:', Array.isArray(connections) ? connections.length : 'NOT AN ARRAY');
    console.log('  Status:', status);

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
            INSERT INTO simulators (creator_id, title, description, blocks, connections, tags, preview_image, is_public, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, NOW(), NOW())
        `;

        const blocksJson = typeof blocks === 'string' ? blocks : JSON.stringify(blocks);
        const connectionsJson = typeof connections === 'string' ? connections : JSON.stringify(connections || []);

        console.log('✓ Blocks JSON length:', blocksJson.length);
        console.log('✓ Connections JSON length:', connectionsJson.length);

        db.query(
            insertQuery,
            [creator_id, title, description || '', blocksJson, connectionsJson, tags || '', preview_image || '', is_public ? 1 : 0],
            (err, result) => {
                if (err) {
                    console.error('❌ Database error:', err);
                    return apiResponse(res, 500, 'Error creating simulator', { details: err.message });
                }
                console.log('✅ Simulator created with ID:', result.insertId);
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
    const { title, description, blocks, connections, tags, preview_image, is_public } = req.body;

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

            const updateQuery = `
                UPDATE simulators 
                SET title = ?, description = ?, ${blocks ? 'blocks = ?,' : ''} ${connections ? 'connections = ?,' : ''} tags = ?, preview_image = ?, is_public = ?
                WHERE id = ?
            `;

            const params = [title, description];
            if (blocks) params.push(blocksJson);
            if (connections) params.push(connectionsJson);
            params.push(tags, preview_image, is_public ? 1 : 0, simulatorId);

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

// Delete simulator
app.delete('/api/simulators/:id', authenticateToken, (req, res) => {
    const simulatorId = req.params.id;
    const userId = req.user.id;

    db.query('SELECT creator_id FROM simulators WHERE id = ?', [simulatorId], (err, results) => {
        if (err) {
            console.error('Error fetching simulator:', err);
            return apiResponse(res, 500, 'Server error');
        }
        if (results.length === 0) {
            return apiResponse(res, 404, 'Simulator not found');
        }

        if (results[0].creator_id !== userId && req.user.role !== 'superadmin') {
            return apiResponse(res, 403, 'You can only delete your own simulators');
        }

        db.query('DELETE FROM simulators WHERE id = ?', [simulatorId], (err) => {
            if (err) {
                console.error('Error deleting simulator:', err);
                return apiResponse(res, 500, 'Error deleting simulator');
            }
            apiResponse(res, 200, 'Simulator deleted successfully');
        });
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
    console.log(`DEBUG GET QUESTIONS: Course ${courseId}, User: ${req.user.id}, Role: ${req.user.role}`);

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
    db.query('SELECT correct_answer, explanation FROM course_questions WHERE id = ?', [questionId], (err, results) => {
        if (err) {
            console.error('Error fetching question:', err);
            return apiResponse(res, 500, 'Server error');
        }
        if (results.length === 0) {
            return apiResponse(res, 404, 'Question not found');
        }

        const question = results[0];
        const isCorrect = user_answer.trim().toLowerCase() === question.correct_answer.trim().toLowerCase();

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
                        console.log(`Creating ${missingMilestones.length} missing certificates for user ${userId}:`, missingMilestones);
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
                                    else console.log(`✓ Created ${milestone}h certificate for user ${userId}`);

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
                                        console.log(`Issued volunteer certificate for ${milestone} hours to user ${user_id}`);
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
                            console.log('Trying signature from:', signatureUrl);
                            const response = await axios.get(signatureUrl, { responseType: 'arraybuffer', timeout: 8000 });
                            if (response.data && response.data.length > 100) {
                                doc.image(response.data, 120, signatureY - 15, { width: 150, height: 60 });
                                console.log('✓ Signature loaded from:', signatureUrl);
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
    const { assignmentId, completionPercentage } = req.body;
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
app.get('/api/student/enrolled-courses', authenticateToken, (req, res) => {
    const studentId = req.user.id;

    db.query(`
        SELECT 
            c.id as course_id, 
            c.title, 
            c.description, 
            u.email as teacher_email,
            COUNT(DISTINCT ca.id) as total_assignments,
            COUNT(DISTINCT CASE WHEN asub.is_submitted = 1 THEN ca.id END) as completed_assignments,
            GROUP_CONCAT(DISTINCT JSON_OBJECT(
                'assignment_id', ca.id,
                'title', ca.title,
                'due_date', ca.due_date,
                'correct_answers', asub.correct_answers,
                'total_questions', asub.total_questions,
                'is_submitted', asub.is_submitted
            ) SEPARATOR '|||') as submissions_json,
            GROUP_CONCAT(DISTINCT JSON_OBJECT(
                'id', ca.id,
                'title', ca.title,
                'due_date', ca.due_date
            ) SEPARATOR '|||') as assignments_json
        LEFT JOIN classroom_assignments ca ON ca.course_id = c.id AND (se.assignment_id IS NULL OR se.assignment_id = ca.id)
        LEFT JOIN assignment_submissions asub ON (ca.id = asub.assignment_id OR (se.assignment_id IS NULL AND asub.assignment_id IS NULL)) AND asub.student_id = se.student_id
        WHERE se.student_id = ?
        GROUP BY c.id, c.title, c.description, u.email
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
            teacher_email: row.teacher_email,
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
    asub.total_questions
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

// ===== ERROR HANDLING =====
app.use((err, req, res, next) => {
    console.error('Unhandled error:', err);
    apiResponse(res, 500, 'Internal server error');
});

// ===== START SERVER =====
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT} `);
    console.log(`Environment: ${process.env.NODE_ENV || 'development'} `);
});