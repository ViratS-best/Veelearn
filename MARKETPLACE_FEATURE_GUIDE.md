# Veelearn Simulator Marketplace - Feature Guide

## Overview

The Simulator Marketplace is a comprehensive feature that allows teachers and developers to create, share, rate, and reuse block-based simulators. This enables community-driven educational content creation and rapid course development.

## Features

### 1. Marketplace Discovery
- **Browse Simulators**: Public marketplace at `/marketplace.html`
- **Search & Filter**: Full-text search, filter by tags
- **Sort Options**: Newest, Most Popular, Highest Rated
- **Pagination**: 20 simulators per page
- **Trending**: Featured simulators based on downloads and ratings

### 2. Simulator Management
- **Create**: Build custom simulators using block-based editor
- **Edit**: Modify existing simulators (creator only)
- **Publish**: Share simulators publicly or keep private
- **Delete**: Remove simulators permanently
- **Version Control**: Track simulator versions

### 3. Social Features
- **Ratings & Reviews**: Users can rate (1-5 stars) and review simulators
- **Comments**: Community discussion on individual simulators
- **Download Tracking**: Track how many times a simulator is used
- **Creator Profile**: See all simulators from a creator

### 4. Advanced Blocks

#### Physics Blocks
- **Gravity**: Apply gravity force (F = m * g)
- **Velocity**: Set and track velocity vectors
- **Collision**: Detect collisions between objects
- **Bounce**: Simulate elastic bouncing with elasticity coefficient
- **Motion**: Apply motion with velocity and time delta

#### Logic & Control Flow
- **If/Then**: Conditional branching
- **Loop**: For loops with configurable range
- **Compare**: Comparison operators (>, <, ===, etc.)

#### Math Operations
- **Power**: Exponentiation (x^n)
- **Square Root**: Calculate square root
- **Trigonometry**: Sin, Cos, Tan functions
- **Random**: Generate random numbers in range
- **Clamp**: Constrain value within min/max bounds

#### Rendering
- **Draw Particle**: Render particles with alpha blending
- **Draw Trail**: Draw lines and trails for motion visualization
- **Draw Text**: Add text labels and values to canvas

#### Data Structures
- **Array**: Create and initialize arrays
- **Array Index**: Access array elements
- **Sort**: Sort arrays ascending/descending

## Database Schema

### simulators table
```sql
CREATE TABLE simulators (
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
);
```

### simulator_ratings table
```sql
CREATE TABLE simulator_ratings (
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
```

### simulator_downloads table
```sql
CREATE TABLE simulator_downloads (
    id INT AUTO_INCREMENT PRIMARY KEY,
    simulator_id INT NOT NULL,
    user_id INT NOT NULL,
    course_id INT,
    downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (simulator_id) REFERENCES simulators(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE SET NULL
);
```

### simulator_comments table
```sql
CREATE TABLE simulator_comments (
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

## API Endpoints

### Simulator Management

#### List Simulators (Public Marketplace)
```
GET /api/simulators?page=1&limit=20&search=query&tags=physics&sort=newest
```
**Parameters:**
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20)
- `search`: Search simulators by title/description
- `tags`: Filter by tags (comma-separated)
- `sort`: Sort by 'newest', 'popular', or 'rating'

**Response:**
```json
{
  "success": true,
  "data": {
    "simulators": [...],
    "total": 100,
    "page": 1,
    "pages": 5
  }
}
```

#### Get Simulator Details
```
GET /api/simulators/:id
```
Returns full simulator data including blocks and connections.

#### Create Simulator
```
POST /api/simulators
Authorization: Bearer token
Content-Type: application/json

{
  "title": "Gravity Simulator",
  "description": "Simulates gravity physics",
  "blocks": [],
  "connections": [],
  "tags": "physics,gravity",
  "preview_image": "base64_image_or_url",
  "is_public": true
}
```

#### Update Simulator
```
PUT /api/simulators/:id
Authorization: Bearer token

{
  "title": "Updated Title",
  "description": "Updated description",
  "blocks": [],
  "connections": [],
  "tags": "physics,gravity",
  "preview_image": "...",
  "is_public": true
}
```

#### Delete Simulator
```
DELETE /api/simulators/:id
Authorization: Bearer token
```

#### Publish/Unpublish
```
POST /api/simulators/:id/publish
Authorization: Bearer token

{
  "is_public": true
}
```

### Ratings & Reviews

#### Add/Update Rating
```
POST /api/simulators/:id/ratings
Authorization: Bearer token

{
  "rating": 5,
  "review": "Great simulator!"
}
```

#### Get All Ratings
```
GET /api/simulators/:id/ratings
```

#### Add Comment
```
POST /api/simulators/:id/comments
Authorization: Bearer token

{
  "comment": "This helped me understand gravity better!"
}
```

#### Get Comments
```
GET /api/simulators/:id/comments
```

### User Simulators

#### Get My Simulators
```
GET /api/my-simulators
Authorization: Bearer token
```

#### Record Download
```
POST /api/simulators/:id/download
Authorization: Bearer token

{
  "courseId": 123  // optional
}
```

#### Get Trending Simulators
```
GET /api/simulators/trending/all
```

## Usage Workflows

### 1. Creating & Publishing a Simulator

1. In the course editor, click "Insert Block-based Simulator"
2. Use the block editor to design your simulator
3. Add blocks from physics, logic, math, and rendering categories
4. Connect blocks to create data flow
5. Test in the preview
6. Save to course
7. In "My Simulators", click "Publish" to make it public
8. Add tags and description for discoverability

### 2. Using a Marketplace Simulator

1. Open `/marketplace.html` or click "Simulator Marketplace" link
2. Search or browse simulators
3. Click "View Details" to see full information and ratings
4. Click "Preview" to see it in action
5. Click "Use in Course" to add to your current course
6. The simulator data is automatically imported

### 3. Rating a Simulator

1. View simulator details in marketplace
2. Scroll to "Ratings" section (coming soon in enhanced version)
3. Click on star rating
4. Optionally add a review comment
5. Submit

## Advanced Block Configuration

### Physics Example: Bouncing Ball

**Blocks:**
1. **Variable**: x = 300
2. **Variable**: y = 200
3. **Variable**: vx = 5
4. **Variable**: vy = 0
5. **Apply Gravity**: mass=1, g=9.8 → force
6. **Set Velocity**: uses output from Gravity
7. **Apply Motion**: uses position and velocity
8. **Detect Collision**: check if hits canvas edge
9. **Bounce**: if collision, reverse velocity
10. **Draw Circle**: render the ball

**Connections:**
- Gravity force → Velocity block
- Velocity vx, vy → Motion block
- Motion x, y → Draw Circle
- Collision result → Bounce condition

### Logic Example: Conditional Physics

**Blocks:**
1. **If/Then**: check if x > 400
2. **Then branch**: Apply Gravity (higher)
3. **Else branch**: Apply Gravity (lower)
4. **Merge results**: Use conditional to select gravity value

## Performance Optimization

- **Block Caching**: Compiled block functions are cached
- **Lazy Rendering**: Only visible blocks are rendered
- **Connection Optimization**: Direct data flow without intermediates
- **Canvas Batching**: Multiple draw calls batched together

## Security Considerations

- **Ownership**: Only creator can edit/delete their simulator
- **Validation**: All inputs validated server-side
- **Code Injection**: Block execution uses safe Function constructor
- **Rate Limiting**: Download tracking prevents abuse

## Future Enhancements

1. **Multiplayer Simulation**: Real-time collaborative simulator editing
2. **Advanced Editor UI**: Drag-drop interface for block connections
3. **Simulator Forking**: Create derivative simulators from public ones
4. **Performance Profiling**: Built-in performance monitoring
5. **Custom Block Creation**: Allow users to create custom block types
6. **Export/Import**: Download simulators as JSON files
7. **API Documentation Generator**: Auto-generate docs from block definitions
8. **Machine Learning Blocks**: Neural network and ML training blocks
9. **3D Rendering**: WebGL-based 3D physics simulations
10. **Real-time Collaboration**: Multiple users editing simultaneously

## Testing

### Test Cases

1. **Discovery**: Search, filter, sort simulators
2. **Creation**: Create new simulator with various blocks
3. **Publishing**: Publish and unpublish simulators
4. **Ratings**: Add, update, view ratings and reviews
5. **Downloads**: Track simulator usage
6. **Permissions**: Verify ownership and access control

### Test Simulators

Included in the system:
- Physics Simulation (gravity, velocity, collision)
- Mathematics Visualizer (sine waves, fractals)
- Animation Sequencer (timeline-based animation)
- Data Visualizer (charts, graphs, arrays)

## Troubleshooting

### Simulator Won't Save
- Check authentication token is valid
- Verify blocks JSON is properly formatted
- Check database connection

### Marketplace Won't Load
- Verify API server is running on port 3000
- Check CORS settings
- Clear browser cache

### Preview Shows Blank Canvas
- Verify canvas dimensions are correct
- Check block execution for errors
- Ensure drawing blocks are included

### Download Count Not Updating
- Check if user is authenticated
- Verify simulator exists
- Check database permissions

## API Response Examples

### Successful Simulator Creation
```json
{
  "success": true,
  "message": "Simulator created successfully",
  "data": {
    "simulatorId": 42
  }
}
```

### Error Response
```json
{
  "success": false,
  "message": "You can only edit your own simulators"
}
```

### Marketplace List Response
```json
{
  "success": true,
  "data": {
    "simulators": [
      {
        "id": 1,
        "title": "Gravity Simulator",
        "description": "Simulate gravity effects",
        "creator_email": "teacher@example.com",
        "downloads": 150,
        "rating": "4.50",
        "review_count": 12,
        "tags": "physics,gravity",
        "created_at": "2025-11-09T00:00:00.000Z"
      }
    ],
    "total": 50,
    "page": 1,
    "pages": 3
  }
}
```

## File Structure

```
veelearn-frontend/
├── index.html                    (Main app)
├── script.js                     (Core logic)
├── marketplace.html              (Marketplace UI)
├── block-simulator.html          (Block editor)
├── visual-simulator.html         (Code-based editor)
├── advanced-block-types.js       (Block library)
└── styles/                       (CSS files)

veelearn-backend/
├── server.js                     (Express API)
├── .env                          (Configuration)
└── package.json                  (Dependencies)
```

## Dependencies

**Frontend:**
- Vanilla JavaScript (no framework required)
- HTML5 Canvas API
- Fetch API for HTTP requests

**Backend:**
- Express.js
- MySQL
- JWT for authentication
- Bcryptjs for password hashing

## License

Veelearn Simulator Marketplace is part of the Veelearn platform.

## Support

For issues or feature requests, contact the development team or file an issue in the repository.
