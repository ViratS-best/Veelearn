# Veelearn Development Roadmap - Phase 2+

## Executive Summary

The Veelearn platform has completed Phase 1 (Core Platform) and Phase 2 (Basic Simulators). This roadmap focuses on:

1. **Fixing all existing errors and gaps** in block simulator execution
2. **Building complex simulation capabilities** (physics engine, advanced blocks)
3. **Completing the marketplace system** for sharing/discovering simulators
4. **Integrating marketplace into course editor** for one-click simulator usage

**Total Expected Code**: ~5000 additional lines of JavaScript
**Estimated Timeline**: 5-7 days of development

---

## Current Issues Identified

### Block Simulator Engine
- ❌ Block execution doesn't properly handle sequential dependencies
- ❌ No timeout protection for infinite loops
- ❌ Limited error handling and debugging
- ❌ Missing input validation for block types
- ❌ Physics calculations lack proper delta-time tracking
- ❌ Canvas rendering needs optimization

### Advanced Block Types
- ✅ Basic blocks exist (gravity, velocity, logic, math, rendering)
- ❌ Missing: particle systems, springs, constraints, raycasting
- ❌ No vector math utilities
- ❌ Limited rendering options

### Marketplace System
- ✅ Backend API endpoints created
- ✅ Database tables ready (simulators, ratings, downloads, comments)
- ❌ Frontend marketplace UI incomplete
- ❌ Simulator detail pages missing
- ❌ Fork/remix system not implemented
- ❌ Search/filter optimization needed
- ❌ Creator dashboard missing

### Course Integration
- ❌ Cannot import marketplace simulators into courses
- ❌ No simulator versioning tracking
- ❌ Missing update notifications

---

## Phase 1: Core Engine Fixes & Physics System (Days 1-2)

### 1.1 Block Execution Engine Refactor
**Files Modified**: block-simulator.html
**Lines**: ~300 new/modified

**Tasks**:
```
[x] Implement topological sort with dependency validation
[x] Add input validation for all block types
[x] Add try-catch error handling with detailed messages
[x] Implement execution timeout (5 second limit)
[x] Add JSON serialization for block state
[x] Implement block debugging interface
[ ] Add performance monitoring (execution time per block)
```

**Key Functions**:
```javascript
executeBlocks(blocks, initialState)          // Main execution engine
validateBlockConnection(from, to)             // Connection validation
getBlockDependencies(blockId)                 // Find prerequisites
executeWithTimeout(fn, timeout)               // Timeout protection
debugBlock(blockId, inputs, outputs)          // Debugging helper
```

### 1.2 Physics Engine Library
**Files Created**: veelearn-frontend/block-physics-engine.js
**Lines**: ~500

**Exports**:
```javascript
// Vector operations
Vector.add(v1, v2)
Vector.scale(v, scalar)
Vector.dot(v1, v2)
Vector.magnitude(v)
Vector.normalize(v)

// Collision detection
Collision.circleCircle(c1, c2)
Collision.aabb(rect1, rect2)
Collision.pointCircle(point, circle)

// Physics integration
Physics.eulerIntegrate(pos, vel, acc, dt)
Physics.verletIntegrate(pos, prevPos, acc, dt)
Physics.applyDamping(vel, damping, dt)

// Constraints
Constraint.clamp(value, min, max)
Constraint.pin(x, y, px, py, distance)
Constraint.spring(pos, target, stiffness, damping, dt)
```

### 1.3 Extended Block Types Library
**Files Created**: veelearn-frontend/advanced-blocks-extended.js
**Lines**: ~600

**New Blocks to Add**:

1. **Particle System Block**
   - Create/update particles with physics
   - Input: count, lifetime, gravity, vx, vy
   - Output: particles_array, alive_count

2. **Spring Physics Block**
   - Simulate spring forces
   - Input: x, vx, rest_length, stiffness, damping, target_x
   - Output: new_x, new_vx, force

3. **Constraint Block**
   - Clamp/pin positions
   - Input: x, y, constraint_type, min/max values
   - Output: constrained_x, constrained_y

4. **Raycast Block**
   - Basic raycasting for collision detection
   - Input: x, y, angle, length
   - Output: hit_distance, hit_x, hit_y

5. **Vector Operations**
   - Dot product, cross product, magnitude, normalize
   - Input: various vector components
   - Output: result values

6. **Advanced Math**
   - Lerp, easing functions, bezier curves
   - Input: t, start, end, easing_type
   - Output: interpolated_value

7. **2D Rotation Block**
   - Rotate points around pivot
   - Input: x, y, angle, pivot_x, pivot_y
   - Output: rotated_x, rotated_y

8. **Friction/Damping Block**
   - Apply velocity damping
   - Input: vx, vy, damping_factor, dt
   - Output: new_vx, new_vy

---

## Phase 2: Rendering & Animation System (Days 2-3)

### 2.1 Renderer System
**Files Created**: veelearn-frontend/block-renderer-system.js
**Lines**: ~400

**New Rendering Blocks**:

1. **Shape Renderer**
   - Draw rectangles, circles, polygons
   - Support color, outline, rotation

2. **Text Renderer**
   - Render text with custom font/size
   - Support alignment and color

3. **Trail System**
   - Draw motion trails (line trails from moving objects)
   - Configurable lifetime and fade

4. **Grid Renderer**
   - Background grid for reference
   - Configurable cell size and color

5. **Sprite/Image Renderer**
   - Draw images or colored rectangles
   - Support scaling and rotation

6. **Layer Management**
   - Z-index based rendering
   - Order: background → shapes → text → effects

### 2.2 Animation & Frame System
**Files Created**: veelearn-frontend/block-animation.js
**Lines**: ~300

**Features**:
- **Frame Counter Block**: Global frame tracking, delta-time calculation
- **Animation Loop**: RequestAnimationFrame-based execution
- **Easing Functions**: ease-in, ease-out, ease-in-out, spring, bounce
- **Keyframe Block**: Time-based triggering of actions
- **Timeline Control**: Play, pause, seek, speed control

**Key Functions**:
```javascript
startAnimationLoop(callback)
stopAnimationLoop()
getFrameInfo()          // { frameCount, deltaTime, elapsed }
getEasingFunction(type) // ease-in, spring, etc.
```

### 2.3 Canvas Rendering Optimization
**Files Modified**: block-simulator.html
**Focus**: 
- Double-buffering for smooth animation
- Layer-based rendering
- Clear-only-necessary-areas optimization
- Performance monitoring (FPS counter)

---

## Phase 3: Marketplace System (Days 3-4)

### 3.1 Marketplace Pages & UI
**Files Created**:
- veelearn-frontend/simulator-marketplace.html (enhanced)
- veelearn-frontend/simulator-detail.html
- veelearn-frontend/simulator-creator.html
- veelearn-frontend/marketplace-app.js

**Lines**: ~800

**Pages**:

1. **Marketplace Browse** (simulator-marketplace.html)
   - Grid of 20 simulators per page
   - Search with autocomplete
   - Filters: tags, rating, downloads, difficulty
   - Sort: newest, popular, trending
   - Categories: Physics, Math, Chemistry, Biology, etc.
   - Featured simulators carousel

2. **Simulator Detail** (simulator-detail.html)
   - Full metadata display
   - Live preview/demo
   - Creator profile card
   - Ratings & reviews (5-star with comments)
   - Download/import button
   - Fork/remix button
   - Statistics: views, downloads, rating, created date

3. **Creator Dashboard** (simulator-creator.html)
   - List user's simulators
   - Create new, edit, delete options
   - Public/private toggle
   - Download statistics
   - Fork history

### 3.2 Marketplace API Client
**Files Created**: veelearn-frontend/marketplace-api.js
**Lines**: ~200

**Functions**:
```javascript
// Browse
getSimulators(page, search, filters, sort)
getSimulatorById(id)
getTrendingSimulators()
searchSimulators(query, filters)

// Create/Edit
createSimulator(data)
updateSimulator(id, data)
deleteSimulator(id)
publishSimulator(id)
unpublishSimulator(id)

// Interact
rateSimulator(id, rating)
commentOnSimulator(id, comment)
getSimulatorComments(id)
downloadSimulator(id)

// Fork
forkSimulator(id, newTitle)
getForkHistory(id)

// User
getMySimulators()
getCreatorProfile(userId)
```

### 3.3 Fork/Remix System
**Files Created**: veelearn-frontend/simulator-fork-system.js
**Lines**: ~150

**Features**:
- Copy simulator with new ID
- Version tracking (1.0 → 1.1)
- "Forked from" attribution
- Link to original
- Edit independently after fork

### 3.4 Backend Enhancements
**Files Modified**: veelearn-backend/server.js
**Additions**:
- Trending algorithm (downloads + ratings + recency)
- Search optimization with proper indexing
- Download tracking API
- Rating/comment moderation prep
- Pagination validation
- Error response standardization

---

## Phase 4: Course Integration (Days 4-5)

### 4.1 Marketplace Integration in Course Editor
**Files Modified**: veelearn-frontend/script.js, index.html
**Changes**:

1. **Add "Insert Simulator" Button** in course editor toolbar
2. **Simulator Browser Modal** in course editor
3. **Quick Import Flow**
   - Preview simulator
   - Choose to use as-is or customize
   - Add to course as new block
4. **Store Simulator Snapshot** in course content
5. **Update Course Editor UI** to show imported simulators

### 4.2 Simulator Versioning
**Database Changes** (new table):
```sql
CREATE TABLE simulator_versions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    simulator_id INT,
    version VARCHAR(10),
    data LONGTEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (simulator_id) REFERENCES simulators(id)
)
```

**Features**:
- Track version used in each course
- Notify when new versions available
- Option to update or keep current
- Rollback capability

### 4.3 Backend Version APIs
**New Endpoints**:
```
GET /api/simulators/:id/versions           - List all versions
GET /api/simulators/:id/versions/:version  - Get specific version
POST /api/simulators/:id/versions          - Create new version
GET /api/course/:id/simulator/:blockId/update-available
```

---

## Database Schema Additions

### New Tables Needed

```sql
-- Simulator versions tracking (optional but recommended)
CREATE TABLE simulator_versions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    simulator_id INT NOT NULL,
    version VARCHAR(10) NOT NULL,
    data LONGTEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (simulator_id) REFERENCES simulators(id) ON DELETE CASCADE,
    UNIQUE KEY unique_version (simulator_id, version)
);

-- Course simulator usage tracking (optional)
CREATE TABLE course_simulator_usage (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    block_id INT NOT NULL,
    simulator_id INT NOT NULL,
    simulator_version VARCHAR(10),
    used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    FOREIGN KEY (simulator_id) REFERENCES simulators(id) ON DELETE SET NULL
);
```

---

## Code Structure & Files Summary

### New JavaScript Files (3000+ lines total)

| File | Lines | Purpose |
|------|-------|---------|
| block-physics-engine.js | 500 | Physics calculations, vectors, collision |
| advanced-blocks-extended.js | 600 | 8+ new block types |
| block-renderer-system.js | 400 | Canvas rendering helpers |
| block-animation.js | 300 | Animation loop & easing |
| marketplace-app.js | 500 | Marketplace UI logic |
| marketplace-api.js | 200 | API client functions |
| simulator-fork-system.js | 150 | Fork/remix logic |
| block-execution-engine.js | 300 | Block execution refactor |

### Modified Files

| File | Changes |
|------|---------|
| block-simulator.html | Refactor execution, add animation loop, integrate physics |
| script.js | Add marketplace integration, simulator import flow |
| simulator-marketplace.html | Enhance UI, add search/filter |
| server.js | Add versioning endpoints, optimize queries |
| index.html | Add marketplace link, modal structure |

---

## Implementation Priority

### Week 1 - Core & Physics (Days 1-2)
1. ✅ Fix block execution engine
2. ✅ Create physics library
3. ✅ Add 8 new advanced blocks
4. ✅ Test basic physics simulations

### Week 1 - Rendering & Animation (Days 3-4)
5. ✅ Create renderer system
6. ✅ Implement animation loop
7. ✅ Add easing functions
8. ✅ Test complex animations

### Week 1-2 - Marketplace (Days 4-5)
9. ✅ Build marketplace pages
10. ✅ Create API client
11. ✅ Implement fork system
12. ✅ Test marketplace flows

### Week 2 - Integration (Days 5-7)
13. ✅ Integrate marketplace with course editor
14. ✅ Add versioning system
15. ✅ Full end-to-end testing
16. ✅ Performance optimization

---

## Success Metrics

- **Block Execution**: <16ms per frame for 50+ blocks
- **Physics Accuracy**: Correct gravity, collision, spring calculations
- **Animation**: 60 FPS with 1000+ particles
- **Marketplace Load**: <2s for 20 simulators
- **Search**: <500ms for results
- **Canvas Rendering**: 60 FPS with complex visuals
- **No Infinite Loops**: 5-second timeout protection
- **Error Handling**: All errors logged, user-friendly messages

---

## Code Quality Standards

**Must Follow AGENTS.md Conventions**:
- camelCase for functions/variables
- `handle*` prefix for event handlers
- `render*` prefix for rendering functions
- `get*` prefix for getters
- Parameterized queries (no SQL injection)
- Error handling with try-catch
- Comments for complex logic
- No console logs (use proper logging)

---

## Testing Plan

### Unit Tests
- [ ] Block execution with dependencies
- [ ] Physics calculations (all block types)
- [ ] Vector operations
- [ ] Collision detection
- [ ] Easing functions

### Integration Tests
- [ ] Block simulation with 10+ blocks
- [ ] Physics chain reactions
- [ ] Animation loop timing
- [ ] Marketplace API calls
- [ ] Simulator import into course

### Performance Tests
- [ ] 50+ blocks execution
- [ ] 1000 particles rendering
- [ ] 100 simulators in marketplace
- [ ] Search with 1000 simulators
- [ ] Memory usage tracking

---

*Last Updated: November 9, 2025*
*Status: Planning Complete - Ready for Implementation*
