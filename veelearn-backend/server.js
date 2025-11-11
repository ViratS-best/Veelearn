const express = require('express');
const mysql = require('mysql');
const dotenv = require('dotenv');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const cors = require('cors');
const path = require('path');

dotenv.config({ path: path.resolve(__dirname, '.env') });

const app = express();
app.use(express.json({ limit: '10mb' }));
app.use(cors());

// ===== DATABASE CONNECTION WITH POOLING =====
const db = mysql.createPool({
    host: process.env.DB_HOST || 'localhost',
    user: process.env.DB_USER || 'root',
    password: process.env.DB_PASSWORD || '',
    database: process.env.DB_NAME || 'veelearn_db',
    connectionLimit: 10,
    waitForConnections: true,
    queueLimit: 0
});

// Database health check
setInterval(() => {
    db.query('SELECT 1', (err) => {
        if (err) console.error('Database connection error:', err);
    });
}, 60000);

// Test database connection
db.getConnection((err, connection) => {
    if (err) {
        console.error('Error connecting to the database:', err);
        return;
    }
    console.log('Connected to MySQL database');
    connection.release();

    // Create tables if they don't exist
    const createUsersTable = `
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
    `;

    const createCoursesTable = `
        CREATE TABLE IF NOT EXISTS courses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            content LONGTEXT,
            creator_id INT,
            status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
            is_paid BOOLEAN DEFAULT FALSE,
            shells_cost INT DEFAULT 50,
            feedback TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (creator_id) REFERENCES users(id) ON DELETE CASCADE,
            INDEX idx_status (status),
            INDEX idx_creator (creator_id)
        )
    `;

    const createAdminFavoritesTable = `
        CREATE TABLE IF NOT EXISTS admin_favorites (
            admin_id INT,
            course_id INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (admin_id, course_id),
            FOREIGN KEY (admin_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
        )
    `;

    const createCourseViewsTable = `
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
    `;

    const createEnrollmentsTable = `
        CREATE TABLE IF NOT EXISTS enrollments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            course_id INT,
            enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
            UNIQUE KEY unique_enrollment (user_id, course_id)
        )
    `;

    const createSimulatorsTable = `
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
    `;

    const createSimulatorRatingsTable = `
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
    `;

    const createSimulatorDownloadsTable = `
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
    `;

    const createSimulatorCommentsTable = `
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
    `;

    db.query(createUsersTable, (err) => {
        if (err) console.error('Error creating users table:', err);
        else console.log('Users table checked/created');
    });
    
    db.query(createCoursesTable, (err) => {
        if (err) console.error('Error creating courses table:', err);
        else console.log('Courses table checked/created');
    });
    
    db.query(createAdminFavoritesTable, (err) => {
        if (err) console.error('Error creating admin_favorites table:', err);
        else console.log('Admin Favorites table checked/created');
    });
    
    db.query(createCourseViewsTable, (err) => {
        if (err) console.error('Error creating course_views table:', err);
        else console.log('Course Views table checked/created');
    });

    db.query(createEnrollmentsTable, (err) => {
        if (err) console.error('Error creating enrollments table:', err);
        else console.log('Enrollments table checked/created');
    });

    db.query(createSimulatorsTable, (err) => {
        if (err) console.error('Error creating simulators table:', err);
        else console.log('Simulators table checked/created');
    });

    db.query(createSimulatorRatingsTable, (err) => {
        if (err) console.error('Error creating simulator_ratings table:', err);
        else console.log('Simulator Ratings table checked/created');
    });

    db.query(createSimulatorDownloadsTable, (err) => {
        if (err) console.error('Error creating simulator_downloads table:', err);
        else console.log('Simulator Downloads table checked/created');
    });

    db.query(createSimulatorCommentsTable, (err) => {
        if (err) console.error('Error creating simulator_comments table:', err);
        else console.log('Simulator Comments table checked/created');
    });

    // Check for superadmin and create if not exists
    const superadminEmail = process.env.SUPERADMIN_EMAIL || 'viratsuper6@gmail.com';
    const superadminPassword = process.env.SUPERADMIN_PASSWORD || 'Virat@123';
    const superadminRole = 'superadmin';

    db.query('SELECT * FROM users WHERE email = ?', [superadminEmail], async (err, results) => {
        if (err) {
            console.error('Error checking for superadmin:', err);
            return;
        }
        if (results.length === 0) {
            const hashedPassword = await bcrypt.hash(superadminPassword, 10);
            const insertSuperadmin = 'INSERT INTO users (email, password, role, is_admin_approved) VALUES (?, ?, ?, TRUE)';
            db.query(insertSuperadmin, [superadminEmail, hashedPassword, superadminRole], (err) => {
                if (err) console.error('Error creating superadmin:', err);
                else console.log('Superadmin created successfully');
            });
        } else {
            console.log('Superadmin already exists');
        }
    });
});

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
            return apiResponse(res, 403, 'Invalid or expired token');
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
    const maxAttempts = 5;

    if (!loginAttempts.has(ip)) {
        loginAttempts.set(ip, { count: 1, resetTime: now + windowMs });
        return next();
    }

    const attempts = loginAttempts.get(ip);
    if (now > attempts.resetTime) {
        loginAttempts.set(ip, { count: 1, resetTime: now + windowMs });
        return next();
    }

    if (attempts.count >= maxAttempts) {
        return apiResponse(res, 429, 'Too many attempts. Please try again later.');
    }

    attempts.count++;
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

            const { password: _, ...userWithoutPassword } = user;
            apiResponse(res, 200, 'Logged in successfully', { token, user: userWithoutPassword });
        });
    } catch (error) {
        console.error('Login error:', error);
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
    db.query('SELECT id, email, role, is_admin_approved, shells, created_at FROM users', (err, results) => {
        if (err) {
            console.error('Error fetching users:', err);
            return apiResponse(res, 500, 'Server error fetching users');
        }
        apiResponse(res, 200, 'Users fetched successfully', results);
    });
});

app.get('/api/superadmin/users', authenticateToken, authorize('superadmin', 'admin'), (req, res) => {
    db.query('SELECT id, email, role, is_admin_approved, shells, created_at FROM users', (err, results) => {
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
    const { title, description, content } = req.body;
    const creator_id = req.user.id;

    if (!title || !content) {
        return apiResponse(res, 400, 'Course title and content are required');
    }

    if (title.length > 255) {
        return apiResponse(res, 400, 'Course title too long (max 255 characters)');
    }

    const insertCourseQuery = 'INSERT INTO courses (title, description, content, creator_id, status) VALUES (?, ?, ?, ?, ?)';
    db.query(insertCourseQuery, [title, description, content, creator_id, 'pending'], (err, result) => {
        if (err) {
            console.error('Error creating course:', err);
            return apiResponse(res, 500, 'Server error creating course');
        }
        apiResponse(res, 201, 'Course created successfully and is awaiting admin approval', { courseId: result.insertId });
    });
});

app.get('/api/courses/:id', authenticateToken, (req, res) => {
    const courseId = req.params.id;
    const userId = req.user.id;
    const userRole = req.user.role;

    const query = `
        SELECT id, title, description, content, creator_id, status, is_paid, shells_cost, feedback
        FROM courses
        WHERE id = ?
    `;

    db.query(query, [courseId], (err, results) => {
        if (err) {
            console.error('Error fetching single course:', err);
            return apiResponse(res, 500, 'Server error fetching course');
        }
        if (results.length === 0) {
            return apiResponse(res, 404, 'Course not found');
        }

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
    const { title, description, content } = req.body;

    if (!title || !content) {
        return apiResponse(res, 400, 'Course title and content are required');
    }

    db.query('SELECT creator_id FROM courses WHERE id = ?', [courseId], (err, results) => {
        if (err) {
            console.error('Error fetching course:', err);
            return apiResponse(res, 500, 'Server error');
        }
        if (results.length === 0) {
            return apiResponse(res, 404, 'Course not found');
        }

        const course = results[0];
        if (parseInt(course.creator_id) !== parseInt(userId)) {
            return apiResponse(res, 403, 'You can only edit your own courses');
        }

        const updateQuery = 'UPDATE courses SET title = ?, description = ?, content = ? WHERE id = ?';
        db.query(updateQuery, [title, description, content, courseId], (err, result) => {
            if (err) {
                console.error('Error updating course:', err);
                return apiResponse(res, 500, 'Server error updating course');
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
SELECT c.id, c.title, c.description, c.creator_id, c.status, c.is_paid, c.shells_cost, u.email as creator_email
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
         apiResponse(res, 200, 'Courses fetched successfully', results);
    });
});

app.get('/api/users/:userId/courses', authenticateToken, (req, res) => {
    const userId = req.params.userId;

    if (parseInt(req.user.id) !== parseInt(userId) && req.user.role !== 'admin' && req.user.role !== 'superadmin') {
        return apiResponse(res, 403, 'Access denied. You can only view your own courses');
    }

    const query = 'SELECT id, title, description, content, creator_id, status, is_paid, shells_cost, feedback FROM courses WHERE creator_id = ?';
    db.query(query, [userId], (err, results) => {
        if (err) {
            console.error('Error fetching user courses:', err);
            return apiResponse(res, 500, 'Server error fetching user courses');
        }
        apiResponse(res, 200, 'User courses fetched successfully', results);
    });
});

// ===== ADMIN ROUTES =====
app.get('/api/admin/courses/pending', authenticateToken, authorize('admin', 'superadmin'), (req, res) => {
    const query = 'SELECT c.id, c.title, c.description, c.content, c.creator_id, u.email as creator_email, c.created_at FROM courses c JOIN users u ON c.creator_id = u.id WHERE c.status = "pending"';
    
    db.query(query, (err, results) => {
        if (err) {
            console.error('Error fetching pending courses:', err);
            return apiResponse(res, 500, 'Server error fetching pending courses');
        }
        apiResponse(res, 200, 'Pending courses fetched successfully', results);
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

        const updateCourseQuery = 'UPDATE courses SET title = ?, description = ?, content = ?, status = "pending", feedback = NULL WHERE id = ?';
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
    db.query('SELECT * FROM courses WHERE id = ? AND status = "approved"', [courseId], (err, courseResults) => {
        if (err) {
            console.error('Error fetching course:', err);
            return apiResponse(res, 500, 'Server error');
        }
        if (courseResults.length === 0) {
            return apiResponse(res, 404, 'Course not found or not approved');
        }

        const course = courseResults[0];

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
                db.query('INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)', [userId, courseId], (err) => {
                    if (err) {
                        console.error('Error enrolling user:', err);
                        return apiResponse(res, 500, 'Server error enrolling in course');
                    }
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
    const { title, description, blocks, connections, tags, preview_image, is_public } = req.body;
    const creator_id = req.user.id;

    if (!title || !blocks) {
        return apiResponse(res, 400, 'Title and blocks are required');
    }

    if (title.length > 255) {
        return apiResponse(res, 400, 'Title too long (max 255 characters)');
    }

    try {
        const insertQuery = `
            INSERT INTO simulators (creator_id, title, description, blocks, connections, tags, preview_image, is_public)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        `;

        const blocksJson = typeof blocks === 'string' ? blocks : JSON.stringify(blocks);
        const connectionsJson = typeof connections === 'string' ? connections : JSON.stringify(connections || []);

        db.query(
            insertQuery,
            [creator_id, title, description, blocksJson, connectionsJson, tags, preview_image, is_public ? 1 : 0],
            (err, result) => {
                if (err) {
                    console.error('Error creating simulator:', err);
                    return apiResponse(res, 500, 'Error creating simulator');
                }
                apiResponse(res, 201, 'Simulator created successfully', { simulatorId: result.insertId });
            }
        );
    } catch (error) {
        console.error('Error:', error);
        apiResponse(res, 500, 'Server error');
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

// Create simulator_versions table if not exists (for version history)
const createSimulatorVersionsTable = `
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
`;

db.query(createSimulatorVersionsTable, (err) => {
    if (err) console.error('Error creating simulator_versions table:', err);
    else console.log('Simulator versions table checked/created');
});

// Create course_simulator_usage table
const createCourseSimulatorTable = `
    CREATE TABLE IF NOT EXISTS course_simulator_usage (
        id INT AUTO_INCREMENT PRIMARY KEY,
        course_id INT NOT NULL,
        simulator_id INT NOT NULL,
        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
        FOREIGN KEY (simulator_id) REFERENCES simulators(id) ON DELETE CASCADE,
        UNIQUE KEY unique_course_sim (course_id, simulator_id)
    )
`;

db.query(createCourseSimulatorTable, (err) => {
    if (err) console.error('Error creating course_simulator_usage table:', err);
    else console.log('Course simulator usage table checked/created');
});

// Add simulator to course
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

        if (results[0].creator_id !== userId && req.user.role !== 'superadmin') {
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

// ===== ERROR HANDLING =====
app.use((err, req, res, next) => {
    console.error('Unhandled error:', err);
    apiResponse(res, 500, 'Internal server error');
});

// ===== START SERVER =====
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
    console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
});