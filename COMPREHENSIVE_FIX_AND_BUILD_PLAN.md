# Veelearn: Comprehensive Fix & Build Plan
## Complex Simulator + Marketplace Complete System

**Date**: November 9, 2025  
**Scope**: Fix all errors, build full marketplace, integrate everything  
**Estimated Effort**: 2-3 full days of continuous development  

---

## PHASE 0: ANALYSIS & DIAGNOSIS (ONGOING)

### Current State Analysis
- **Backend**: Express server (server.js) - mostly complete but needs marketplace routes
- **Database**: 10 core tables exist, need 2 new tables for simulators
- **Frontend JS Libraries**: 8+ files created (physics, rendering, animation, execution)
- **Frontend HTML**: 6 pages exist (block-simulator.html, visual-simulator.html, etc.)
- **Integration**: Partial - libraries exist but not fully wired together

### Known Issues to Fix
1. **Block Execution Engine**: May have topological sort edge cases
2. **Physics Engine**: Collision detection needs stress testing
3. **Rendering System**: Canvas layer management incomplete
4. **Marketplace**: Backend APIs missing/incomplete
5. **Integration**: HTML pages don't import all required JS files
6. **Database**: No marketplace-specific tables yet

---

## PHASE 1: FIX CORE ENGINE (Days 1-2, ~8 hours)

### 1.1 Block Execution Engine Audit & Fix
**File**: `veelearn-frontend/block-execution-engine.js`

**Issues to Check & Fix**:
- [ ] Topological sort (Kahn's algorithm) handles circular dependencies correctly
- [ ] Block validation rejects invalid connections
- [ ] Timeout protection actually stops execution after 5s
- [ ] Error messages are meaningful, not generic
- [ ] State persists correctly between block calls
- [ ] Performance metrics are accurate

**Actions**:
```javascript
// 1. Add comprehensive logging
console.log(`[DEBUG] Executing ${blocks.length} blocks in order:`, sorted.map(b => b.id));

// 2. Add cycle detection
if (hasCycle) throw new Error('Circular dependency detected');

// 3. Verify timeout works
const timeoutPromise = new Promise((_, reject) =>
  setTimeout(() => reject(new Error('Execution timeout')), 5000)
);

// 4. Test with sample blocks
executeBlocks([
  { id: 'a', type: 'input', inputs: {}, outputs: ['x'], execute: () => ({ x: 5 }) },
  { id: 'b', type: 'math', inputs: { x: 'a.x' }, outputs: ['y'], execute: (i) => ({ y: i.x * 2 }) },
  { id: 'c', type: 'output', inputs: { y: 'b.y' }, outputs: [], execute: (i) => i }
]);
```

### 1.2 Physics Engine Validation
**File**: `veelearn-frontend/block-physics-engine.js`

**Tests to Run**:
- [ ] Vector operations (add, subtract, scale, normalize)
- [ ] Collision detection (circle-circle, AABB, ray-casting)
- [ ] Integrators (Euler, semi-implicit, Verlet) produce reasonable values
- [ ] Spring forces oscillate properly
- [ ] No NaN or Infinity values in calculations

**Actions**:
```javascript
// Test vector operations
const v1 = new Vector(3, 4);
console.assert(v1.magnitude() === 5, 'Magnitude calculation failed');
console.assert(v1.normalize().magnitude() === 1, 'Normalize failed');

// Test collisions
const circle1 = { x: 0, y: 0, r: 10 };
const circle2 = { x: 15, y: 0, r: 10 };
console.assert(Collision.circleCircle(circle1, circle2).colliding === true, 'Collision detection failed');

// Test integrator
const newPos = Physics.eulerIntegrate({ x: 0, y: 0 }, { x: 1, y: 0 }, { x: 0, y: -9.8 }, 0.016);
console.assert(newPos.y < 0, 'Gravity integration failed');
```

### 1.3 Rendering System Audit
**File**: `veelearn-frontend/block-renderer-system.js`

**Issues to Check**:
- [ ] Canvas context properly initialized
- [ ] Layer system prevents z-order conflicts
- [ ] Trail cleanup prevents memory leaks
- [ ] Shape rendering works (circle, rect, triangle, polygon)
- [ ] Text rendering readable at all sizes
- [ ] Particle rendering smooth at 60 FPS

**Actions**:
```javascript
// Initialize with proper canvas
const renderer = BlockRendererSystem.init({
  canvasId: 'simulation-canvas',
  width: 800,
  height: 600,
  fps: 60
});

// Test rendering shapes
renderer.drawShape('circle', { x: 100, y: 100, r: 20, color: '#ff0000' });
renderer.drawText('Test Text', { x: 100, y: 50, size: 16, color: '#ffffff' });
renderer.drawParticles(particleArray);
renderer.render(); // Render to canvas
```

---

## PHASE 2: BUILD MARKETPLACE BACKEND (Days 1-2, ~12 hours)

### 2.1 Database Schema Additions
**New Tables**:

```sql
CREATE TABLE IF NOT EXISTS simulators (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    blocks LONGTEXT NOT NULL,  -- JSON array of block objects
    thumbnail VARCHAR(255),
    creator_id INT NOT NULL,
    is_public BOOLEAN DEFAULT FALSE,
    download_count INT DEFAULT 0,
    rating DECIMAL(3,2) DEFAULT 0,
    rating_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (creator_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_creator (creator_id),
    INDEX idx_public (is_public),
    FULLTEXT INDEX ft_title_desc (title, description)
);

CREATE TABLE IF NOT EXISTS simulator_versions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    simulator_id INT NOT NULL,
    version_number INT DEFAULT 1,
    blocks LONGTEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (simulator_id) REFERENCES simulators(id) ON DELETE CASCADE,
    INDEX idx_simulator (simulator_id)
);

CREATE TABLE IF NOT EXISTS simulator_ratings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    simulator_id INT NOT NULL,
    user_id INT NOT NULL,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    review TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (simulator_id) REFERENCES simulators(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_simulator (user_id, simulator_id)
);

CREATE TABLE IF NOT EXISTS simulator_comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    simulator_id INT NOT NULL,
    user_id INT NOT NULL,
    comment TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (simulator_id) REFERENCES simulators(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_simulator (simulator_id)
);

CREATE TABLE IF NOT EXISTS simulator_forks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    original_id INT NOT NULL,
    fork_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (original_id) REFERENCES simulators(id) ON DELETE CASCADE,
    FOREIGN KEY (fork_id) REFERENCES simulators(id) ON DELETE CASCADE,
    INDEX idx_original (original_id)
);

CREATE TABLE IF NOT EXISTS course_simulator_usage (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    simulator_id INT NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    FOREIGN KEY (simulator_id) REFERENCES simulators(id) ON DELETE CASCADE,
    UNIQUE KEY unique_course_simulator (course_id, simulator_id)
);
```

### 2.2 Backend API Routes
**File**: Add to `veelearn-backend/server.js` (or create `simulators.js`)

**Endpoints to Implement** (60+ lines each):

```javascript
// ===== SIMULATOR CRUD =====

// Browse all simulators with pagination & search
app.get('/api/simulators', (req, res) => {
    const { page = 1, limit = 20, search = '', sort = 'newest' } = req.query;
    const offset = (page - 1) * limit;
    
    let query = 'SELECT * FROM simulators WHERE is_public = TRUE';
    let params = [];
    
    if (search) {
        query += ' AND (title LIKE ? OR description LIKE ?)';
        params.push(`%${search}%`, `%${search}%`);
    }
    
    // Sorting
    if (sort === 'popular') query += ' ORDER BY download_count DESC';
    else if (sort === 'highest-rated') query += ' ORDER BY rating DESC';
    else query += ' ORDER BY created_at DESC';
    
    query += ' LIMIT ? OFFSET ?';
    params.push(limit, offset);
    
    db.query(query, params, (err, results) => {
        if (err) return apiResponse(res, 500, 'Query failed', null);
        apiResponse(res, 200, 'Simulators retrieved', results);
    });
});

// Get single simulator with details
app.get('/api/simulators/:id', (req, res) => {
    const { id } = req.params;
    db.query(
        'SELECT * FROM simulators WHERE id = ?',
        [id],
        (err, results) => {
            if (err) return apiResponse(res, 500, 'Query failed', null);
            if (results.length === 0) return apiResponse(res, 404, 'Simulator not found', null);
            apiResponse(res, 200, 'Simulator retrieved', results[0]);
        }
    );
});

// Create simulator
app.post('/api/simulators', authenticateToken, (req, res) => {
    const { title, description, blocks } = req.body;
    const creator_id = req.user.id;
    
    if (!title || !blocks) return apiResponse(res, 400, 'Title and blocks required', null);
    
    db.query(
        'INSERT INTO simulators (title, description, blocks, creator_id) VALUES (?, ?, ?, ?)',
        [title, description || '', JSON.stringify(blocks), creator_id],
        (err, result) => {
            if (err) return apiResponse(res, 500, 'Insert failed', null);
            apiResponse(res, 201, 'Simulator created', { id: result.insertId });
        }
    );
});

// Update simulator
app.put('/api/simulators/:id', authenticateToken, (req, res) => {
    const { id } = req.params;
    const { title, description, blocks, is_public } = req.body;
    const user_id = req.user.id;
    
    // Check ownership
    db.query(
        'SELECT creator_id FROM simulators WHERE id = ?',
        [id],
        (err, results) => {
            if (err || results.length === 0) return apiResponse(res, 404, 'Not found', null);
            if (results[0].creator_id !== user_id) return apiResponse(res, 403, 'Not authorized', null);
            
            db.query(
                'UPDATE simulators SET title = ?, description = ?, blocks = ?, is_public = ? WHERE id = ?',
                [title, description, JSON.stringify(blocks), is_public ? 1 : 0, id],
                (err) => {
                    if (err) return apiResponse(res, 500, 'Update failed', null);
                    apiResponse(res, 200, 'Simulator updated', null);
                }
            );
        }
    );
});

// Publish simulator
app.post('/api/simulators/:id/publish', authenticateToken, (req, res) => {
    const { id } = req.params;
    const user_id = req.user.id;
    
    db.query(
        'UPDATE simulators SET is_public = TRUE WHERE id = ? AND creator_id = ?',
        [id, user_id],
        (err, result) => {
            if (err) return apiResponse(res, 500, 'Update failed', null);
            if (result.affectedRows === 0) return apiResponse(res, 403, 'Not authorized', null);
            apiResponse(res, 200, 'Simulator published', null);
        }
    );
});

// ===== RATINGS & COMMENTS =====

// Add or update rating
app.post('/api/simulators/:id/ratings', authenticateToken, (req, res) => {
    const { id } = req.params;
    const { rating, review } = req.body;
    const user_id = req.user.id;
    
    if (rating < 1 || rating > 5) return apiResponse(res, 400, 'Rating must be 1-5', null);
    
    db.query(
        'INSERT INTO simulator_ratings (simulator_id, user_id, rating, review) VALUES (?, ?, ?, ?) ON DUPLICATE KEY UPDATE rating = ?, review = ?',
        [id, user_id, rating, review || '', rating, review || ''],
        (err) => {
            if (err) return apiResponse(res, 500, 'Insert failed', null);
            // Update simulator rating average
            db.query(
                'UPDATE simulators SET rating = (SELECT AVG(rating) FROM simulator_ratings WHERE simulator_id = ?), rating_count = (SELECT COUNT(*) FROM simulator_ratings WHERE simulator_id = ?) WHERE id = ?',
                [id, id, id],
                (err) => {
                    if (err) return apiResponse(res, 500, 'Update failed', null);
                    apiResponse(res, 201, 'Rating saved', null);
                }
            );
        }
    );
});

// Get ratings for simulator
app.get('/api/simulators/:id/ratings', (req, res) => {
    const { id } = req.params;
    db.query(
        'SELECT sr.id, sr.rating, sr.review, sr.created_at, u.email FROM simulator_ratings sr JOIN users u ON sr.user_id = u.id WHERE sr.simulator_id = ? ORDER BY sr.created_at DESC',
        [id],
        (err, results) => {
            if (err) return apiResponse(res, 500, 'Query failed', null);
            apiResponse(res, 200, 'Ratings retrieved', results);
        }
    );
});

// Add comment
app.post('/api/simulators/:id/comments', authenticateToken, (req, res) => {
    const { id } = req.params;
    const { comment } = req.body;
    const user_id = req.user.id;
    
    if (!comment) return apiResponse(res, 400, 'Comment required', null);
    
    db.query(
        'INSERT INTO simulator_comments (simulator_id, user_id, comment) VALUES (?, ?, ?)',
        [id, user_id, comment],
        (err, result) => {
            if (err) return apiResponse(res, 500, 'Insert failed', null);
            apiResponse(res, 201, 'Comment added', { id: result.insertId });
        }
    );
});

// Get comments
app.get('/api/simulators/:id/comments', (req, res) => {
    const { id } = req.params;
    db.query(
        'SELECT sc.id, sc.comment, sc.created_at, u.email FROM simulator_comments sc JOIN users u ON sc.user_id = u.id WHERE sc.simulator_id = ? ORDER BY sc.created_at DESC',
        [id],
        (err, results) => {
            if (err) return apiResponse(res, 500, 'Query failed', null);
            apiResponse(res, 200, 'Comments retrieved', results);
        }
    );
});

// ===== USER SIMULATORS =====

// Get user's simulators
app.get('/api/my-simulators', authenticateToken, (req, res) => {
    const user_id = req.user.id;
    db.query(
        'SELECT id, title, description, is_public, rating, download_count, created_at FROM simulators WHERE creator_id = ? ORDER BY created_at DESC',
        [user_id],
        (err, results) => {
            if (err) return apiResponse(res, 500, 'Query failed', null);
            apiResponse(res, 200, 'Your simulators', results);
        }
    );
});

// ===== VERSION MANAGEMENT =====

// Get simulator versions
app.get('/api/simulators/:id/versions', (req, res) => {
    const { id } = req.params;
    db.query(
        'SELECT * FROM simulator_versions WHERE simulator_id = ? ORDER BY version_number DESC',
        [id],
        (err, results) => {
            if (err) return apiResponse(res, 500, 'Query failed', null);
            apiResponse(res, 200, 'Versions retrieved', results);
        }
    );
});

// ===== FORK SYSTEM =====

// Fork a simulator
app.post('/api/simulators/:id/fork', authenticateToken, (req, res) => {
    const { id } = req.params;
    const { title } = req.body;
    const creator_id = req.user.id;
    
    db.query(
        'SELECT blocks FROM simulators WHERE id = ?',
        [id],
        (err, results) => {
            if (err || results.length === 0) return apiResponse(res, 404, 'Original not found', null);
            
            const newTitle = title || `${results[0].title} (Fork)`;
            
            // Create fork
            db.query(
                'INSERT INTO simulators (title, description, blocks, creator_id, is_public) VALUES (?, ?, ?, ?, FALSE)',
                [newTitle, `Forked from simulator #${id}`, results[0].blocks, creator_id],
                (err, insertResult) => {
                    if (err) return apiResponse(res, 500, 'Fork failed', null);
                    
                    // Record fork relationship
                    db.query(
                        'INSERT INTO simulator_forks (original_id, fork_id) VALUES (?, ?)',
                        [id, insertResult.insertId],
                        (err) => {
                            if (err) console.error('Failed to record fork:', err);
                            apiResponse(res, 201, 'Simulator forked', { id: insertResult.insertId });
                        }
                    );
                }
            );
        }
    );
});

// ===== TRENDING =====

// Get trending simulators
app.get('/api/simulators/trending/all', (req, res) => {
    const { limit = 10 } = req.query;
    db.query(
        'SELECT * FROM simulators WHERE is_public = TRUE ORDER BY download_count DESC, rating DESC LIMIT ?',
        [parseInt(limit)],
        (err, results) => {
            if (err) return apiResponse(res, 500, 'Query failed', null);
            apiResponse(res, 200, 'Trending simulators', results);
        }
    );
});
```

---

## PHASE 3: BUILD MARKETPLACE FRONTEND (Days 2-3, ~10 hours)

### 3.1 Marketplace API Client
**File**: `veelearn-frontend/marketplace-api.js` (UPDATE/EXPAND)

Needs full implementation of all API calls with proper error handling and caching.

### 3.2 Marketplace UI Pages

#### Page 1: Simulator Marketplace (Browse)
**File**: `veelearn-frontend/simulator-marketplace.html` (UPDATE)

Features:
- [ ] Grid layout with simulator cards
- [ ] Search bar
- [ ] Filter: category, rating, downloads
- [ ] Sort: newest, popular, highest-rated
- [ ] Pagination
- [ ] Creator profile hover

#### Page 2: Simulator Detail
**File**: `veelearn-frontend/simulator-detail.html` (UPDATE/CREATE)

Features:
- [ ] Full simulator info (title, description, creator)
- [ ] Preview/demo of blocks
- [ ] Statistics (downloads, rating, comments)
- [ ] Ratings/reviews section
- [ ] Comments section
- [ ] Action buttons:
  - "Add to Course"
  - "Fork/Remix"
  - "Download"
  - "Use in Simulator"

#### Page 3: Creator Dashboard
**File**: `veelearn-frontend/simulator-creator.html` (UPDATE/CREATE)

Features:
- [ ] List of user's simulators
- [ ] Create new simulator button
- [ ] Edit/delete/publish options
- [ ] View analytics (downloads, ratings)
- [ ] Version history

#### Page 4: Simulator Editor
**File**: `veelearn-frontend/simulator-editor.html` (UPDATE/CREATE)

Features:
- [ ] Full block editor (from block-simulator.html)
- [ ] Save simulator
- [ ] Publish to marketplace
- [ ] Save as version
- [ ] Import from marketplace

### 3.3 JavaScript Integration Layer
**New File**: `veelearn-frontend/integration-layer.js` (~500 lines)

```javascript
// Unified API for all simulator operations
class SimulatorIntegration {
    // Save simulator locally
    static saveLocal(blocks, metadata) {
        localStorage.setItem('current_simulator_blocks', JSON.stringify(blocks));
        localStorage.setItem('current_simulator_meta', JSON.stringify(metadata));
    }
    
    // Publish to marketplace
    static async publishToMarketplace(blocks, metadata) {
        const data = {
            title: metadata.title,
            description: metadata.description,
            blocks: blocks
        };
        return await MarketplaceAPI.createSimulator(data);
    }
    
    // Fork existing simulator
    static async forkSimulator(simulatorId, newTitle) {
        return await MarketplaceAPI.forkSimulator(simulatorId, newTitle);
    }
    
    // Add simulator to course
    static async addToCourse(courseId, simulatorId) {
        // Backend call to link simulator to course
        return fetch(`/api/courses/${courseId}/add-simulator`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ simulator_id: simulatorId })
        }).then(r => r.json());
    }
    
    // Load simulator from marketplace into editor
    static async loadFromMarketplace(simulatorId) {
        const simulator = await MarketplaceAPI.getSimulatorById(simulatorId);
        return JSON.parse(simulator.blocks);
    }
}
```

---

## PHASE 4: INTEGRATION & WIRING (Days 3, ~6 hours)

### 4.1 Update Block Simulator HTML
**File**: `veelearn-frontend/block-simulator.html` (MAJOR UPDATE)

Add to `<head>`:
```html
<!-- Physics & Animation Libraries -->
<script src="block-physics-engine.js"></script>
<script src="block-animation.js"></script>
<script src="block-renderer-system.js"></script>
<script src="block-execution-engine.js"></script>

<!-- Block Definitions -->
<script src="advanced-block-types.js"></script>
<script src="advanced-blocks-extended.js"></script>

<!-- Marketplace Integration -->
<script src="marketplace-api.js"></script>
<script src="integration-layer.js"></script>
```

Add to toolbar:
```html
<button onclick="publishToMarketplace()">📤 Publish to Marketplace</button>
<button onclick="openMarketplace()">🛍️ Browse Simulators</button>
<button onclick="forkSimulator()">🍴 Fork Simulator</button>
<button onclick="addToCourse()">📚 Add to Course</button>
```

### 4.2 Wire Event Handlers
**Update**: `veelearn-frontend/script.js` (ADD ~200 lines)

```javascript
async function publishToMarketplace() {
    const title = prompt('Simulator name:');
    if (!title) return;
    
    const description = prompt('Description:');
    
    try {
        const result = await SimulatorIntegration.publishToMarketplace(
            courseBlocks,
            { title, description }
        );
        alert(`Published! Simulator ID: ${result.id}`);
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

function openMarketplace() {
    window.location.href = '/simulator-marketplace.html';
}

async function forkSimulator() {
    const id = prompt('Simulator ID to fork:');
    if (!id) return;
    
    const newTitle = prompt('New simulator name:');
    
    try {
        const result = await SimulatorIntegration.forkSimulator(id, newTitle);
        alert(`Forked! New ID: ${result.id}`);
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

async function addToCourse() {
    const courseId = prompt('Course ID:');
    if (!courseId) return;
    
    const simulatorId = prompt('Simulator ID:');
    if (!simulatorId) return;
    
    try {
        await SimulatorIntegration.addToCourse(courseId, simulatorId);
        alert('Simulator added to course!');
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}
```

### 4.3 Wire Marketplace Pages Together
**Update**: `veelearn-frontend/simulator-marketplace.html`

```javascript
// Load marketplace UI on page load
document.addEventListener('DOMContentLoaded', async () => {
    await MarketplaceUI.renderGrid(1);
    setupSearchFilter();
    setupSorting();
    setupPagination();
});

function setupSearchFilter() {
    document.getElementById('search-input').addEventListener('input', async (e) => {
        const query = e.target.value;
        const results = await MarketplaceAPI.searchSimulators(query);
        await MarketplaceUI.renderGrid(results);
    });
}

// When simulator card clicked
async function onSimulatorClick(simulatorId) {
    window.location.href = `simulator-detail.html?id=${simulatorId}`;
}
```

---

## PHASE 5: TESTING & DEBUGGING (Days 3-4, ~8 hours)

### 5.1 Unit Tests

```javascript
// Test block execution
function testBlockExecution() {
    const blocks = [
        {
            id: 'input',
            type: 'input',
            inputs: {},
            outputs: ['x'],
            execute: () => ({ x: 10 })
        },
        {
            id: 'double',
            type: 'math',
            inputs: { x: 'input.x' },
            outputs: ['y'],
            execute: (inputs) => ({ y: inputs.x * 2 })
        }
    ];
    
    executeBlocks(blocks, {}).then(result => {
        console.assert(result.double.y === 20, 'Block execution failed');
        console.log('✓ Block execution test passed');
    });
}

// Test physics
function testPhysics() {
    const v1 = new Vector(3, 4);
    console.assert(v1.magnitude() === 5, 'Vector magnitude failed');
    
    const v2 = Vector.dot(new Vector(1, 0), new Vector(0, 1));
    console.assert(v2 === 0, 'Dot product failed');
    
    console.log('✓ Physics tests passed');
}

// Test rendering
function testRendering() {
    const renderer = BlockRendererSystem.init({
        canvasId: 'test-canvas',
        width: 800,
        height: 600
    });
    
    renderer.drawShape('circle', { x: 100, y: 100, r: 20, color: '#ff0000' });
    renderer.render();
    
    console.log('✓ Rendering test passed');
}
```

### 5.2 Integration Tests

```javascript
// Test marketplace flow
async function testMarketplaceFlow() {
    // 1. Create simulator
    const sim1 = await MarketplaceAPI.createSimulator({
        title: 'Test Sim',
        description: 'Test',
        blocks: []
    });
    console.log('✓ Created simulator:', sim1.id);
    
    // 2. Publish it
    await MarketplaceAPI.publishSimulator(sim1.id);
    console.log('✓ Published simulator');
    
    // 3. Rate it
    await MarketplaceAPI.rateSimulator(sim1.id, 5, 'Great!');
    console.log('✓ Rated simulator');
    
    // 4. Fork it
    const sim2 = await MarketplaceAPI.forkSimulator(sim1.id, 'Forked');
    console.log('✓ Forked simulator:', sim2.id);
    
    // 5. Search it
    const results = await MarketplaceAPI.searchSimulators('Test');
    console.log('✓ Searched simulators:', results.length);
}

// Test block execution with rendering
async function testSimulationFlow() {
    const blocks = buildComplexSimulation();
    
    const renderer = BlockRendererSystem.init({
        canvasId: 'canvas',
        width: 800,
        height: 600
    });
    
    let frameCount = 0;
    const animation = new AnimationSystem();
    
    animation.onFrame((frameInfo) => {
        // Execute blocks
        executeBlocks(blocks, frameInfo).then(result => {
            // Render result
            const particles = result.particleSystem.particles;
            renderer.drawParticles(particles);
            renderer.render();
            
            if (frameCount++ > 300) animation.stop();
        });
    });
    
    animation.play();
}
```

### 5.3 Manual Testing Checklist

- [ ] Create block simulator with 5+ blocks
- [ ] Run simulation, see particles/shapes render
- [ ] Publish to marketplace
- [ ] Search for simulator in marketplace
- [ ] View simulator details page
- [ ] Rate and comment on simulator
- [ ] Fork simulator
- [ ] Add simulator to course
- [ ] Edit simulator in creator dashboard
- [ ] View analytics

---

## PHASE 6: OPTIMIZATION & POLISH (Days 4, ~4 hours)

### 6.1 Performance Optimizations

```javascript
// Cache simulator list
const simulatorCache = new Map();
const CACHE_TTL = 5 * 60 * 1000; // 5 minutes

async function getSimulatorsWithCache(page) {
    const key = `simulators_${page}`;
    
    if (simulatorCache.has(key)) {
        const cached = simulatorCache.get(key);
        if (Date.now() - cached.timestamp < CACHE_TTL) {
            return cached.data;
        }
    }
    
    const data = await MarketplaceAPI.getSimulators(page);
    simulatorCache.set(key, { data, timestamp: Date.now() });
    return data;
}

// Lazy load images
function lazyLoadImages() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                observer.unobserve(img);
            }
        });
    });
    
    document.querySelectorAll('img[data-src]').forEach(img => {
        observer.observe(img);
    });
}

// Debounce search
const debounceSearch = debounce((query) => {
    MarketplaceAPI.searchSimulators(query);
}, 300);
```

### 6.2 UI Polish

- [ ] Responsive design for mobile
- [ ] Dark theme (already have it!)
- [ ] Loading spinners
- [ ] Error messages with recovery options
- [ ] Animations on card hover
- [ ] Smooth transitions between pages

### 6.3 Documentation

Create in-app help:
- Tooltips on all buttons
- Getting started guide
- Block type reference
- Keyboard shortcuts

---

## File Checklist

### Backend (veelearn-backend/)
- [ ] server.js - Update with simulator routes
- [ ] .env - Ensure DB credentials set
- [ ] simulators.js - Optional separate file for simulator routes

### Frontend Libraries (veelearn-frontend/)
- [x] block-execution-engine.js
- [x] block-physics-engine.js
- [x] advanced-blocks-extended.js
- [x] block-renderer-system.js
- [x] block-animation.js
- [x] marketplace-api.js
- [x] marketplace-ui.js
- [ ] integration-layer.js (NEW - need to create)
- [ ] simulator-manager.js (UPDATE if exists)

### Frontend Pages (veelearn-frontend/)
- [ ] block-simulator.html - ADD marketplace buttons
- [ ] visual-simulator.html - Keep as-is
- [ ] simulator-marketplace.html - UPDATE/CREATE full marketplace
- [ ] simulator-detail.html - UPDATE/CREATE detail page
- [ ] simulator-creator.html - UPDATE/CREATE creator dashboard
- [ ] simulator-editor.html - UPDATE/CREATE editor page
- [ ] index.html - Link all pages

### Styles (veelearn-frontend/)
- [ ] styles.css - UPDATE with marketplace styles
- [ ] marketplace.css - CREATE (optional, if separating)

---

## Success Criteria

### Functionality
- ✅ Block execution engine works with 10+ blocks
- ✅ Physics engine calculates collisions correctly
- ✅ Rendering displays particles at 60 FPS
- ✅ Marketplace CRUD operations work
- ✅ Search/filter finds simulators
- ✅ Rating/comment system functional
- ✅ Fork system creates copies
- ✅ Course integration links simulators

### Performance
- ✅ Block execution < 16ms per frame
- ✅ Marketplace load < 2s
- ✅ Search < 500ms
- ✅ API responses < 200ms
- ✅ 60 FPS rendering with 1000+ particles

### Quality
- ✅ Zero console errors
- ✅ All edge cases handled
- ✅ Input validation on all forms
- ✅ Graceful error messages
- ✅ Mobile responsive

---

## Quick Start Commands

```bash
# Terminal 1: Backend
cd veelearn-backend
npm install  # if needed
npm run dev  # Runs on port 3000

# Terminal 2: Frontend
cd veelearn-frontend
python -m http.server 5000 --directory .
# OR
npx http-server . -p 5000
```

Visit:
- Block Simulator: http://localhost:5000/block-simulator.html
- Marketplace: http://localhost:5000/simulator-marketplace.html
- Creator Dashboard: http://localhost:5000/simulator-creator.html

---

## Development Priority

1. **CRITICAL** (Do First):
   - Fix block execution engine
   - Fix physics engine
   - Add database tables
   - Implement marketplace CRUD

2. **HIGH** (Do Next):
   - Build marketplace UI pages
   - Wire integration layer
   - Test end-to-end flows

3. **MEDIUM** (Do After):
   - Performance optimization
   - Polish and animations
   - Documentation

4. **LOW** (Do Last):
   - Advanced features
   - Analytics
   - Admin tools

---

*This plan assumes continuous development and is designed to create a complete, production-ready marketplace simulator system.*

**Estimated Total Time**: 40-50 hours of focused development
**Recommended Approach**: Work through phases sequentially, testing each phase before moving to the next.
