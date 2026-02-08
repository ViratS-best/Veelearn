const mysql = require('mysql');
const dotenv = require('dotenv');
const path = require('path');

// Load environment variables
dotenv.config({ path: path.resolve(__dirname, '.env') });

console.log('Testing DB Connection relying on .env configuration...');
console.log(`Host: ${process.env.DB_HOST}`);
console.log(`User: ${process.env.DB_USER}`);
console.log(`DB Name: ${process.env.DB_NAME}`);

const connection = mysql.createConnection({
    host: process.env.DB_HOST || 'localhost',
    user: process.env.DB_USER || 'root',
    password: process.env.DB_PASSWORD || '',
    database: process.env.DB_NAME || 'veelearn_db'
});

connection.connect((err) => {
    if (err) {
        console.error('Error connecting to database:', err);
        return;
    }
    console.log('Connected to MySQL database!');

    // Check users table structure
    connection.query('DESCRIBE users', (err, results) => {
        if (err) {
            console.error('Error describing users table:', err);
        } else {
            console.log('Users table structure:', JSON.stringify(results, null, 2));
        }

        // Try a dummy insertion to see if it fails (using a random email to avoid duplication error)
        const email = `test_debug_${Date.now()}@example.com`;
        const password = 'hashed_password_placeholder';
        // Note: server.js only inserts email and password.
        const query = 'INSERT INTO users (email, password) VALUES (?, ?)';

        console.log(`Attempting insert with email: ${email}`);
        connection.query(query, [email, password], (err, result) => {
            if (err) {
                console.error('INSERT FAILED:', err);
            } else {
                console.log('INSERT SUCCESS:', result);
            }
            connection.end();
        });
    });
});
