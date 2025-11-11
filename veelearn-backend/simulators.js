// ===== SIMULATOR MARKETPLACE ROUTES =====
// This module exports all simulator-related routes

module.exports = function(app, db, authenticateToken, authorize, apiResponse) {

    // GET all public simulators (paginated, with search/filter)
    app.get('/api/simulators', (req, res) => {
        const page = parseInt(req.query.page) || 1;
        const limit = 20;
        const offset = (page - 1) * limit;
        const search = req.query.search || '';
        const sortBy = req.query.sort || 'newest'; // newest, popular, rated
        const tag = req.query.tag || '';

        let query = 'SELECT id, creator_id, title, description, version, tags, downloads, rating, created_at FROM simulators WHERE is_public = TRUE';
        let countQuery = 'SELECT COUNT(*) as total FROM simulators WHERE is_public = TRUE';
        const params = [];

        if (search) {
            query += ' AND (title LIKE ? OR description LIKE ?)';
            countQuery += ' AND (title LIKE ? OR description LIKE ?)';
            params.push(`%${search}%`, `%${search}%`);
        }

        if (tag) {
            query += ' AND tags LIKE ?';
            countQuery += ' AND tags LIKE ?';
            params.push(`%${tag}%`);
        }

        // Sorting
        if (sortBy === 'popular') {
            query += ' ORDER BY downloads DESC';
        } else if (sortBy === 'rated') {
            query += ' ORDER BY rating DESC';
        } else {
            query += ' ORDER BY created_at DESC';
        }

        query += ` LIMIT ${limit} OFFSET ${offset}`;

        // Get total count
        db.query(countQuery, params.length > 0 ? params : [], (err, countResults) => {
            if (err) {
                console.error('Error counting simulators:', err);
                return apiResponse(res, 500, 'Server error');
            }

            const total = countResults[0].total;
            const totalPages = Math.ceil(total / limit);

            // Get simulators
            db.query(query, params, (err, results) => {
                if (err) {
                    console.error('Error fetching simulators:', err);
                    return apiResponse(res, 500, 'Server error');
                }

                apiResponse(res, 200, 'Simulators fetched successfully', {
                    simulators: results,
                    pagination: {
                        page,
                        limit,
                        total,
                        totalPages
                    }
                });
            });
        });
    });

    // GET featured simulators
    app.get('/api/simulators/featured', (req, res) => {
        const query = 'SELECT id, creator_id, title, description, version, tags, downloads, rating, created_at FROM simulators WHERE is_public = TRUE AND is_featured = TRUE ORDER BY created_at DESC LIMIT 10';

        db.query(query, (err, results) => {
            if (err) {
                console.error('Error fetching featured simulators:', err);
                return apiResponse(res, 500, 'Server error');
            }
            apiResponse(res, 200, 'Featured simulators fetched', results);
        });
    });

    // GET trending simulators
    app.get('/api/simulators/trending', (req, res) => {
        const query = 'SELECT id, creator_id, title, description, version, tags, downloads, rating, created_at FROM simulators WHERE is_public = TRUE ORDER BY downloads DESC LIMIT 10';

        db.query(query, (err, results) => {
            if (err) {
                console.error('Error fetching trending simulators:', err);
                return apiResponse(res, 500, 'Server error');
            }
            apiResponse(res, 200, 'Trending simulators fetched', results);
        });
    });

    // GET single simulator details
    app.get('/api/simulators/:id', (req, res) => {
        const simulatorId = req.params.id;

        const query = `
            SELECT s.*, u.email as creator_email
            FROM simulators s
            JOIN users u ON s.creator_id = u.id
            WHERE s.id = ?
        `;

        db.query(query, [simulatorId], (err, results) => {
            if (err) {
                console.error('Error fetching simulator:', err);
                return apiResponse(res, 500, 'Server error');
            }

            if (results.length === 0) {
                return apiResponse(res, 404, 'Simulator not found');
            }

            const simulator = results[0];

            if (!simulator.is_public && (!req.user || parseInt(simulator.creator_id) !== req.user.id)) {
                return apiResponse(res, 403, 'Access denied');
            }

            apiResponse(res, 200, 'Simulator fetched successfully', simulator);
        });
    });

    // CREATE new simulator
    app.post('/api/simulators', authenticateToken, (req, res) => {
        const { title, description, blocks, connections, tags, preview_image } = req.body;
        const creator_id = req.user.id;

        if (!title || !blocks || !connections) {
            return apiResponse(res, 400, 'Title, blocks, and connections are required');
        }

        const query = `
            INSERT INTO simulators (creator_id, title, description, blocks, connections, tags, preview_image)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        `;

        db.query(query, [creator_id, title, description || '', blocks, connections, tags || '', preview_image || ''], (err, result) => {
            if (err) {
                console.error('Error creating simulator:', err);
                return apiResponse(res, 500, 'Server error creating simulator');
            }

            apiResponse(res, 201, 'Simulator created successfully', { simulatorId: result.insertId });
        });
    });

    // UPDATE simulator
    app.put('/api/simulators/:id', authenticateToken, (req, res) => {
        const simulatorId = req.params.id;
        const userId = req.user.id;
        const { title, description, blocks, connections, tags, preview_image } = req.body;

        db.query('SELECT creator_id FROM simulators WHERE id = ?', [simulatorId], (err, results) => {
            if (err) {
                console.error('Error fetching simulator:', err);
                return apiResponse(res, 500, 'Server error');
            }

            if (results.length === 0) {
                return apiResponse(res, 404, 'Simulator not found');
            }

            if (parseInt(results[0].creator_id) !== userId) {
                return apiResponse(res, 403, 'You can only edit your own simulators');
            }

            const query = 'UPDATE simulators SET title = ?, description = ?, blocks = ?, connections = ?, tags = ?, preview_image = ? WHERE id = ?';
            db.query(query, [title || '', description || '', blocks || '', connections || '', tags || '', preview_image || '', simulatorId], (err) => {
                if (err) {
                    console.error('Error updating simulator:', err);
                    return apiResponse(res, 500, 'Server error updating simulator');
                }
                apiResponse(res, 200, 'Simulator updated successfully');
            });
        });
    });

    // DELETE simulator
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

            if (parseInt(results[0].creator_id) !== userId && req.user.role !== 'superadmin') {
                return apiResponse(res, 403, 'You can only delete your own simulators');
            }

            db.query('DELETE FROM simulators WHERE id = ?', [simulatorId], (err) => {
                if (err) {
                    console.error('Error deleting simulator:', err);
                    return apiResponse(res, 500, 'Server error deleting simulator');
                }
                apiResponse(res, 200, 'Simulator deleted successfully');
            });
        });
    });

    // PUBLISH simulator (make it public)
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

            if (parseInt(results[0].creator_id) !== userId) {
                return apiResponse(res, 403, 'You can only publish your own simulators');
            }

            db.query('UPDATE simulators SET is_public = ? WHERE id = ?', [is_public ? 1 : 0, simulatorId], (err) => {
                if (err) {
                    console.error('Error updating simulator visibility:', err);
                    return apiResponse(res, 500, 'Server error');
                }
                apiResponse(res, 200, `Simulator ${is_public ? 'published' : 'unpublished'} successfully`);
            });
        });
    });

    // RECORD download
    app.post('/api/simulators/:id/download', authenticateToken, (req, res) => {
        const simulatorId = req.params.id;
        const userId = req.user.id;
        const { course_id } = req.body;

        const query = 'INSERT INTO simulator_downloads (simulator_id, user_id, course_id) VALUES (?, ?, ?)';
        db.query(query, [simulatorId, userId, course_id || null], (err) => {
            if (err) {
                console.error('Error recording download:', err);
                return apiResponse(res, 500, 'Server error');
            }

            // Increment download count
            db.query('UPDATE simulators SET downloads = downloads + 1 WHERE id = ?', [simulatorId], (err) => {
                if (err) console.error('Error updating download count:', err);
            });

            apiResponse(res, 200, 'Download recorded');
        });
    });

    // GET simulator reviews/ratings
    app.get('/api/simulators/:id/reviews', (req, res) => {
        const simulatorId = req.params.id;

        const query = `
            SELECT sr.id, sr.rating, sr.review, sr.created_at, u.email as user_email
            FROM simulator_ratings sr
            JOIN users u ON sr.user_id = u.id
            WHERE sr.simulator_id = ?
            ORDER BY sr.created_at DESC
        `;

        db.query(query, [simulatorId], (err, results) => {
            if (err) {
                console.error('Error fetching reviews:', err);
                return apiResponse(res, 500, 'Server error');
            }
            apiResponse(res, 200, 'Reviews fetched', results);
        });
    });

    // POST simulator review/rating
    app.post('/api/simulators/:id/reviews', authenticateToken, (req, res) => {
        const simulatorId = req.params.id;
        const userId = req.user.id;
        const { rating, review } = req.body;

        if (!rating || rating < 1 || rating > 5) {
            return apiResponse(res, 400, 'Rating must be between 1 and 5');
        }

        const query = `
            INSERT INTO simulator_ratings (simulator_id, user_id, rating, review)
            VALUES (?, ?, ?, ?)
            ON DUPLICATE KEY UPDATE rating = ?, review = ?, updated_at = CURRENT_TIMESTAMP
        `;

        db.query(query, [simulatorId, userId, rating, review || '', rating, review || ''], (err) => {
            if (err) {
                console.error('Error submitting review:', err);
                return apiResponse(res, 500, 'Server error');
            }

            // Recalculate average rating
            db.query(
                'SELECT AVG(rating) as avg_rating FROM simulator_ratings WHERE simulator_id = ?',
                [simulatorId],
                (err, results) => {
                    if (err) {
                        console.error('Error calculating average rating:', err);
                        return;
                    }

                    const avgRating = results[0].avg_rating || 0;
                    db.query('UPDATE simulators SET rating = ? WHERE id = ?', [avgRating, simulatorId], (err) => {
                        if (err) console.error('Error updating simulator rating:', err);
                    });
                }
            );

            apiResponse(res, 201, 'Review submitted successfully');
        });
    });

    // GET simulator comments
    app.get('/api/simulators/:id/comments', (req, res) => {
        const simulatorId = req.params.id;

        const query = `
            SELECT sc.id, sc.comment, sc.created_at, u.email as user_email
            FROM simulator_comments sc
            JOIN users u ON sc.user_id = u.id
            WHERE sc.simulator_id = ?
            ORDER BY sc.created_at DESC
        `;

        db.query(query, [simulatorId], (err, results) => {
            if (err) {
                console.error('Error fetching comments:', err);
                return apiResponse(res, 500, 'Server error');
            }
            apiResponse(res, 200, 'Comments fetched', results);
        });
    });

    // POST simulator comment
    app.post('/api/simulators/:id/comments', authenticateToken, (req, res) => {
        const simulatorId = req.params.id;
        const userId = req.user.id;
        const { comment } = req.body;

        if (!comment || comment.trim() === '') {
            return apiResponse(res, 400, 'Comment cannot be empty');
        }

        const query = 'INSERT INTO simulator_comments (simulator_id, user_id, comment) VALUES (?, ?, ?)';
        db.query(query, [simulatorId, userId, comment], (err, result) => {
            if (err) {
                console.error('Error adding comment:', err);
                return apiResponse(res, 500, 'Server error');
            }
            apiResponse(res, 201, 'Comment added successfully', { commentId: result.insertId });
        });
    });

    // DELETE comment
    app.delete('/api/simulators/:id/comments/:commentId', authenticateToken, (req, res) => {
        const simulatorId = req.params.id;
        const commentId = req.params.commentId;
        const userId = req.user.id;

        db.query('SELECT user_id FROM simulator_comments WHERE id = ? AND simulator_id = ?', [commentId, simulatorId], (err, results) => {
            if (err) {
                console.error('Error fetching comment:', err);
                return apiResponse(res, 500, 'Server error');
            }

            if (results.length === 0) {
                return apiResponse(res, 404, 'Comment not found');
            }

            if (parseInt(results[0].user_id) !== userId && req.user.role !== 'superadmin') {
                return apiResponse(res, 403, 'You can only delete your own comments');
            }

            db.query('DELETE FROM simulator_comments WHERE id = ?', [commentId], (err) => {
                if (err) {
                    console.error('Error deleting comment:', err);
                    return apiResponse(res, 500, 'Server error');
                }
                apiResponse(res, 200, 'Comment deleted');
            });
        });
    });

    // GET user's simulators
    app.get('/api/my-simulators', authenticateToken, (req, res) => {
        const userId = req.user.id;

        const query = 'SELECT * FROM simulators WHERE creator_id = ? ORDER BY created_at DESC';
        db.query(query, [userId], (err, results) => {
            if (err) {
                console.error('Error fetching user simulators:', err);
                return apiResponse(res, 500, 'Server error');
            }
            apiResponse(res, 200, 'User simulators fetched', results);
        });
    });

};
