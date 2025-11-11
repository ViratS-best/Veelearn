# Veelearn Implementation Plan

## Phase 1: Bug Fixes & Code Cleanup

### Critical Errors Found:
1. **API Endpoint Mismatch**: 
   - Frontend calls `/auth/login` and `/auth/register` 
   - Backend has `/api/login` and `/api/register`
   - **Fix**: Update frontend to use `/login` and `/register` (without `/auth`)

2. **Missing Auth Endpoints**:
   - Frontend calls `/users` and `/users/:id/role` 
   - Backend has `/superadmin/users` and `/superadmin/users/:id/role`
   - **Fix**: Backend needs `/api/users` and `/api/users/:id/role` OR frontend must use correct paths

3. **Missing Course Endpoints**:
   - `/courses/:id` PUT (update) - not in backend
   - `/courses/:id` DELETE - not in backend
   - `/enrollments` GET - backend has `/users/enrollments`
   - `/enrollments/:id` POST - backend has `/courses/:id/enroll`
   - **Fix**: Standardize endpoint naming

4. **Login Form Error Messaging**:
   - `#login-error-message` element not in HTML
   - `#register-error-message` element not in HTML
   - `#login-form-container` and `#register-form-container` IDs don't exist
   - **Fix**: Add these elements to index.html

5. **Dashboard Fetch Functions**:
   - `fetchSuperadminData()` calls `fetchCourseList('superadmin-course-list')` but IDs in HTML are:
     - `superadmin-pending-courses-list`
     - `my-courses-list-superadmin`
     - `available-courses-list-superadmin`
   - **Fix**: Update function calls or HTML IDs

6. **Block Simulator Execution Errors**:
   - Lines 776-892 in block-simulator.html have duplicate/orphaned code
   - Topological sort is correct but connection resolution has bugs
   - **Fix**: Clean up duplicate code block

7. **Missing Elements in HTML**:
   - `#superadmin-user-list` should be `#user-list` (as per dashboard-section)
   - No error message containers for auth forms

### Phase 1 Tasks:
- [ ] Fix all API endpoint mismatches
- [ ] Add missing HTML elements
- [ ] Fix ID naming inconsistencies
- [ ] Remove duplicate code in block-simulator.html
- [ ] Test basic auth flow
- [ ] Add comprehensive error handling

---

## Phase 2: Enhance Block-Based Simulator

### New Physics Features:
1. **Particle System Block**
   - inputs: x, y, vx, vy, mass, lifetime
   - outputs: final_x, final_y, final_vx, final_vy

2. **Collision Detection Block**
   - inputs: x1, y1, r1, x2, y2, r2
   - outputs: is_colliding, collision_x, collision_y

3. **Gravity/Physics Block**
   - inputs: current_y, velocity_y, gravity, dt
   - outputs: new_y, new_velocity_y

4. **Spring Physics Block**
   - inputs: x, velocity, stiffness, damping, dt
   - outputs: new_x, new_velocity

5. **Rotation Block**
   - inputs: x, y, angle, radius, color
   - outputs: x_rotated, y_rotated

6. **Advanced Math Blocks**
   - Sin/Cos/Tan
   - Abs/Min/Max
   - Random number generator
   - Vectors (dot product, cross product)

### New Display Blocks:
1. **Text Display Block** - shows calculated values on canvas
2. **Animated Shape Block** - draws shapes with animation
3. **Particle Effect Block** - renders particles
4. **Trace Block** - draws trail of movement

### Animation/Looping:
1. **Animation Loop Block**
   - inputs: duration, repeat_count
   - Allows temporal sequencing of blocks
   - Can trigger multiple execution passes

2. **Frame Counter Block**
   - outputs: frame_count, delta_time
   - Enables time-based calculations

### Phase 2 Tasks:
- [ ] Add 10+ new block types
- [ ] Implement animation loop system
- [ ] Add delta_time tracking
- [ ] Create block template library
- [ ] Test complex simulations
- [ ] Add block descriptions/tutorials

---

## Phase 3: Simulator Marketplace

### Database Schema Additions:

```sql
CREATE TABLE IF NOT EXISTS simulators (
    id INT AUTO_INCREMENT PRIMARY KEY,
    creator_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    version VARCHAR(20) DEFAULT '1.0.0',
    blocks LONGTEXT NOT NULL, -- JSON serialized blocks
    connections LONGTEXT NOT NULL, -- JSON serialized connections
    preview_image LONGTEXT, -- Base64 or URL
    tags VARCHAR(500), -- Comma-separated tags
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
);

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
);

CREATE TABLE IF NOT EXISTS simulator_downloads (
    id INT AUTO_INCREMENT PRIMARY KEY,
    simulator_id INT NOT NULL,
    user_id INT NOT NULL,
    course_id INT, -- Optional, if used in a course
    downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (simulator_id) REFERENCES simulators(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS simulator_comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    simulator_id INT NOT NULL,
    user_id INT NOT NULL,
    comment TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (simulator_id) REFERENCES simulators(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### Backend API Endpoints for Marketplace:

```
GET    /api/simulators                 - List all public simulators (paginated)
GET    /api/simulators/:id             - Get simulator details
POST   /api/simulators                 - Create new simulator (auth required)
PUT    /api/simulators/:id             - Update simulator (owner only)
DELETE /api/simulators/:id             - Delete simulator (owner only)
POST   /api/simulators/:id/publish     - Publish simulator (auth required)
POST   /api/simulators/:id/download    - Record download
GET    /api/simulators/:id/reviews     - Get reviews/ratings
POST   /api/simulators/:id/reviews     - Add review/rating (auth required)
GET    /api/simulators/:id/comments    - Get comments
POST   /api/simulators/:id/comments    - Add comment (auth required)
GET    /api/simulators/trending        - Trending simulators
GET    /api/simulators/search          - Search simulators
GET    /api/my-simulators              - User's simulators (auth required)
```

### Frontend Marketplace UI:

1. **Simulator Browser Page**
   - Search/Filter by tags
   - Sort by rating, downloads, newest
   - View simulator details
   - Preview simulator
   - Download/Import simulator

2. **Simulator Creator Profile**
   - List of creator's simulators
   - Following/Follow button
   - Statistics (total downloads, average rating)

3. **Simulator Detail Page**
   - Full description
   - Preview/interactive demo
   - Reviews and ratings
   - Comments section
   - "Use in Course" button
   - "Fork/Remix" button

4. **Publishing/Management Panel**
   - Create new simulator
   - Edit simulator details
   - Manage visibility (public/private)
   - View download stats
   - View reviews

### Phase 3 Tasks:
- [ ] Create database tables
- [ ] Implement backend API endpoints
- [ ] Build marketplace UI pages
- [ ] Add simulator preview functionality
- [ ] Implement search/filter
- [ ] Add rating/review system
- [ ] Track downloads and analytics

---

## Phase 4: Integration & Polish

### Tasks:
- [ ] Integrate simulators into course editor
- [ ] "Quick Insert" from marketplace in course editor
- [ ] Simulator fork/remix functionality
- [ ] Simulator versioning
- [ ] Export/import simulator as JSON
- [ ] Template library (beginner, intermediate, advanced)
- [ ] Simulator categories (Physics, Math, Chemistry, Biology, etc.)

---

## Implementation Order:

1. **Week 1**: Phase 1 (Bug Fixes) - 2-3 hours
2. **Week 1-2**: Phase 2 (Enhanced Simulator) - 4-6 hours
3. **Week 2-3**: Phase 3 (Marketplace) - 6-8 hours
4. **Week 3**: Phase 4 (Integration) - 2-3 hours

---

## Testing Checklist:

- [ ] Auth flow (register, login, logout)
- [ ] Course CRUD operations
- [ ] Block simulator with 5+ block types
- [ ] Physics calculations (gravity, collision)
- [ ] Marketplace CRUD
- [ ] Search and filter
- [ ] Rating system
- [ ] Import simulator into course
- [ ] Multi-user functionality
- [ ] Admin approval workflow

---

## Performance Considerations:

- Implement pagination for marketplace (20 per page)
- Cache popular simulators
- Optimize JSON serialization/deserialization
- Use indexes on frequently queried columns
- Implement rate limiting on API endpoints

---

## Security Considerations:

- Validate all simulator JSON before execution
- Sanitize user inputs in comments/reviews
- Verify ownership before allowing edits
- Implement CORS properly
- Rate limit API calls
- Add CSRF protection if needed
