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
