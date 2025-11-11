# Veelearn Quick Reference

## Files Created (This Session)

### Core Libraries
1. **block-physics-engine.js** - Physics calculations (Vector2, Particle, PhysicsEngine)
2. **advanced-block-types.js** - 12 block types (physics, math, transforms)
3. **block-animation.js** - Animation system (Timer, Loop, Keyframe, StateMachine, Timeline)
4. **block-renderer-system.js** - Canvas rendering (RenderSystem, RenderLayer, 9+ elements)
5. **marketplace-api.js** - API wrapper & manager (MarketplaceAPI, MarketplaceManager)

### UI Pages
6. **simulator-marketplace.html** - Full marketplace with browse, search, detail, create

### Documentation
7. **COMPREHENSIVE_FIX_PLAN.md** - 4-phase implementation plan
8. **PHASE1_COMPLETION_SUMMARY.md** - Technical component details
9. **INTEGRATION_GUIDE.md** - Step-by-step integration instructions
10. **ACCOMPLISHMENTS.md** - What was built and achieved
11. **QUICK_REFERENCE.md** - This file

---

## Quick Start (5 Minutes)

### Terminal 1: Start Backend
```bash
cd veelearn-backend
npm install
npm start
```

### Terminal 2: Start Frontend
```bash
cd veelearn-frontend
python -m http.server 5000
# OR: npx http-server -p 5000
```

### Browser
```
http://localhost:5000/simulator-marketplace.html
```

---

## Physics Engine Usage

```javascript
// Create engine
const engine = new PhysicsEngine();

// Gravity calculation
const result = engine.calculateGravity(
    y,        // current position
    vy,       // current velocity
    gravity,  // gravity acceleration
    mass,     // object mass
    dt,       // delta time
    damping   // friction (0-1)
);
// Returns: { new_y, new_vy, kinetic_energy }

// Spring physics
const spring = engine.calculateSpring(
    x,          // current position
    vx,         // current velocity
    restLength, // rest length
    stiffness,  // spring stiffness
    damping,    // damping coefficient
    dt,         // delta time
    targetX     // target position
);
// Returns: { new_x, new_vx, force, energy }

// Collision detection
const collision = engine.collideCircles(
    x1, y1, r1,  // circle 1
    x2, y2, r2   // circle 2
);
// Returns: { is_colliding, distance, overlap, collision_x/y, normal_x/y }
```

---

## Animation System Usage

```javascript
// Frame-accurate timing
const timer = new AnimationFrameTimer();
timer.start();
timer.addCallback(({frameCount, deltaTime, elapsedTime}) => {
    // Called every frame
});

// Animation loop with easing
const loop = new AnimationLoop(
    1000,      // duration ms
    3,         // repeat count
    'easeInOutQuad'  // easing function
);
loop.start();
loop.update(deltaTime);  // Call every frame
console.log(loop.progress);  // 0 to 1

// Keyframe triggers
const keyframe = new Keyframe(frameNumber, repeatCount);
if (keyframe.update(currentFrame)) {
    // Frame triggered!
}

// Animation state machine
const sm = new AnimationStateMachine();
sm.addState('idle', 
    () => console.log('enter idle'),
    (dt, time) => console.log('update'),
    () => console.log('exit idle')
);
sm.setState('idle');
sm.update(deltaTime);

// Timeline for sequencing
const timeline = new Timeline();
timeline.addTrack(0, 1000, (progress) => {
    // Animate something 0-1 seconds
});
timeline.start();
timeline.update(deltaTime);
```

---

## Renderer System Usage

```javascript
// Initialize
const canvas = document.getElementById('canvas');
const renderer = new RenderSystem(canvas);

// Create layers
const layer1 = renderer.createLayer('background', 0);
const layer2 = renderer.createLayer('objects', 1);
const layer3 = renderer.createLayer('ui', 2);

// Add render elements
const circle = new RenderCircle(x, y, radius, color);
renderer.getLayer('objects').addElement(circle);

const text = new RenderText(
    'Score: 100',
    10, 20,     // x, y
    16,         // font size
    '#000000'   // color
);
renderer.getLayer('ui').addElement(text);

// Draw each frame
function animate() {
    renderer.clear();
    renderer.render();  // Renders all layers in order
    requestAnimationFrame(animate);
}

// Grid
renderer.drawGrid(20, '#cccccc');
```

---

## Marketplace API Usage

```javascript
const api = new MarketplaceAPI();
api.setToken(localStorage.getItem('token'));

// Get simulators
const response = await api.getSimulators(
    1,          // page
    20,         // limit per page
    'gravity',  // search
    'physics',  // tags
    'rating'    // sort: newest, popular, rating
);

// Create simulator
const sim = await api.createSimulator({
    title: 'My Simulator',
    description: 'A cool simulator',
    blocks: [...],      // JSON
    connections: [...], // JSON
    tags: 'physics,gravity',
    is_public: true
});

// Manage ratings
await api.addRating(simulatorId, 5, 'Excellent!');
const ratings = await api.getRatings(simulatorId);

// Comments
await api.addComment(simulatorId, 'Great work!');
const comments = await api.getComments(simulatorId);

// Downloads
await api.recordDownload(simulatorId, courseId);
```

---

## Advanced Blocks

### Physics Blocks
```javascript
// Particle System
ADVANCED_BLOCK_TYPES.PARTICLE_SYSTEM.execute({
    x: 100, y: 100,
    vx: 10, vy: 0,
    mass: 1,
    lifetime: 1000,
    gravity: 9.81,
    damping: 0.99
}, engine);

// Collision Detector
ADVANCED_BLOCK_TYPES.COLLISION_DETECTOR.execute({
    x1: 100, y1: 100, r1: 10,
    x2: 200, y2: 100, r2: 10
}, engine);

// Gravity Physics
ADVANCED_BLOCK_TYPES.GRAVITY_PHYSICS.execute({
    y: 100,
    vy: 0,
    gravity: 9.81,
    mass: 1,
    dt: 0.016,
    damping: 0.99
}, engine);

// Spring Physics
ADVANCED_BLOCK_TYPES.SPRING_PHYSICS.execute({
    x: 100,
    vx: 0,
    target_x: 200,
    stiffness: 100,
    damping: 5,
    dt: 0.016
}, engine);
```

### Math Blocks
```javascript
// Trigonometry
ADVANCED_BLOCK_TYPES.MATH_TRIG.execute({
    angle: 45,  // degrees
    operation: 'sin'  // sin, cos, tan, asin, acos, atan
}, engine);

// Vector Math
ADVANCED_BLOCK_TYPES.MATH_VECTOR.execute({
    v1x: 1, v1y: 0,
    v2x: 0, v2y: 1,
    operation: 'dot'  // dot, cross, magnitude, normalize, distance
}, engine);

// Random
ADVANCED_BLOCK_TYPES.RANDOM_NUMBER.execute({
    min: 0,
    max: 100,
    type: 'integer'  // integer or float
}, engine);
```

### Display Blocks
```javascript
// Text Display
DISPLAY_BLOCK_TYPES.TEXT_DISPLAY.render({
    x: 100,
    y: 100,
    text: 'Score: 1000',
    font_size: 24,
    color: '#ffffff'
}, renderer);

// Shape Renderer
DISPLAY_BLOCK_TYPES.SHAPE_RENDERER.render({
    x: 100,
    y: 100,
    type: 'circle',  // circle, rectangle, polygon
    size: 20,
    color: '#ff0000'
}, renderer);

// Trail Renderer
DISPLAY_BLOCK_TYPES.TRAIL_RENDERER.render({
    x: currentX,
    y: currentY,
    color: '#00ff00',
    max_points: 100
}, renderer);
```

---

## Marketplace Manager Usage

```javascript
const mgr = new MarketplaceManager();

// Load simulators with search/filter/sort
await mgr.loadSimulators(
    page = 1,
    search = 'gravity',
    sort = 'rating',  // newest, popular, rating
    tags = 'physics'
);

// View simulator details
const sim = await mgr.viewSimulator(id);

// Get trending
const trending = await mgr.getTrending();

// Create new
const newSim = await mgr.createSimulator({...});

// Fork simulator
const forkedId = await mgr.forkSimulator(originalId);

// Ratings
await mgr.addRating(id, 5, 'Awesome!');
const ratings = await mgr.loadRatings(id);

// Comments
await mgr.addComment(id, 'Great simulator!');
const comments = await mgr.loadComments(id);

// My simulators
const mySims = await mgr.loadMySimulators();

// Delete
await mgr.deleteSimulator(id);

// Publish/unpublish
await mgr.publishSimulator(id, isPublic = true);
```

---

## Block Type Properties

### All Blocks Have:
```javascript
{
    id: 'unique-id',
    name: 'Display Name',
    category: 'Category',  // Physics, Math, Display, etc.
    color: '#hexcolor',
    description: 'What it does',
    inputs: [
        { name: 'input_name', type: 'number', default: 0 }
    ],
    outputs: [
        { name: 'output_name', type: 'number' }
    ],
    execute(inputs, engine) {
        // Calculate and return outputs
        return { output_name: value };
    }
}
```

---

## Easing Functions Available

```
linear
easeInQuad, easeOutQuad, easeInOutQuad
easeInCubic, easeOutCubic, easeInOutCubic
easeInQuart, easeOutQuart, easeInOutQuart
easeInQuint, easeOutQuint, easeInOutQuint
easeInSine, easeOutSine, easeInOutSine
easeInExpo, easeOutExpo, easeInOutExpo
easeInCirc, easeOutCirc, easeInOutCirc
easeInBack, easeOutBack, easeInOutBack
easeInElastic, easeOutElastic, easeInOutElastic
easeInBounce, easeOutBounce, easeInOutBounce
```

---

## API Endpoints

```
GET  /api/simulators?page=1&limit=20&search=&tags=&sort=newest
GET  /api/simulators/:id
POST /api/simulators
PUT  /api/simulators/:id
DELETE /api/simulators/:id
POST /api/simulators/:id/publish (body: {is_public: true})
GET  /api/my-simulators
POST /api/simulators/:id/download
GET  /api/simulators/:id/ratings
POST /api/simulators/:id/ratings (body: {rating: 5, review: ''})
GET  /api/simulators/:id/comments
POST /api/simulators/:id/comments (body: {comment: ''})
GET  /api/simulators/trending/all
```

---

## Common Patterns

### Physics Simulation Loop
```javascript
const engine = new PhysicsEngine();
const timer = new AnimationFrameTimer();
const renderer = new RenderSystem(canvas);

timer.start();
timer.addCallback(({deltaTime}) => {
    // Execute blocks
    const gravity = engine.calculateGravity(y, vy, 9.81, 1, deltaTime, 0.99);
    
    // Render
    renderer.clear();
    const circle = new RenderCircle(x, gravity.new_y, 10, '#ff0000');
    renderer.defaultLayer.addElement(circle);
    renderer.render();
    
    y = gravity.new_y;
    vy = gravity.new_vy;
});
```

### Marketplace Integration
```javascript
// In course editor
function importSimulator() {
    const mgr = new MarketplaceManager();
    mgr.viewSimulator(simulatorId).then(sim => {
        // Add to course
        courseBlocks.push({
            type: 'marketplace-simulator',
            data: {
                blocks: sim.blocks,
                connections: sim.connections
            }
        });
    });
}
```

---

## Performance Tips

- **Physics**: Reuse Vector2 objects, cache calculations
- **Animation**: Use RAF, batch updates, reduce draw calls
- **Rendering**: Use layers, batch similar shapes, lazy-load images
- **Marketplace**: Cache trending (5min TTL), paginate (20/page), use IndexedDB offline

---

## Debugging

### Physics
```javascript
// Check vector math
const v = new Vector2(1, 2);
console.log(v.magnitude());  // Should be ~2.236

// Check collision
const c = engine.collideCircles(0, 0, 10, 15, 0, 10);
console.log(c.is_colliding);  // true if 15 < 20
```

### Animation
```javascript
const timer = new AnimationFrameTimer();
timer.addCallback(({frameCount, deltaTime}) => {
    console.log(`Frame ${frameCount}, Delta: ${deltaTime.toFixed(4)}s`);
});
```

### Rendering
```javascript
renderer.defaultLayer.elements.forEach(el => {
    console.log(el.constructor.name);  // Check what's being rendered
});
```

---

## Getting Help

1. Check the **INTEGRATION_GUIDE.md** for step-by-step setup
2. Review **PHASE1_COMPLETION_SUMMARY.md** for technical details
3. Look at JSDoc comments in source files
4. Check **ACCOMPLISHMENTS.md** for overview

All files are well-documented and ready for production use!

---

**Happy Coding! 🚀**
