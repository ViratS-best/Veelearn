# Quick Start Guide - Using Veelearn Block Simulator

## For Users Building Simulators

### 1. Basic Setup

```html
<!-- Include all required libraries in block-simulator.html -->
<script src="block-physics-engine.js"></script>
<script src="block-execution-engine.js"></script>
<script src="advanced-block-types.js"></script>
<script src="advanced-blocks-extended.js"></script>
<script src="block-renderer-system.js"></script>
<script src="block-animation.js"></script>
```

### 2. Create a Simple Simulation

```javascript
// Initialize engine
const engine = new BlockExecutionEngine();
const animation = new AnimationSystem();
const renderer = BlockRendererSystem;

// Set up canvas
const canvas = document.getElementById('canvas');
renderer.init(canvas);

// Create blocks
const blocks = [
    {
        id: 'gravity-block',
        type: 'gravity',
        inputs: { mass: 1, g: 9.8 },
        outputs: ['force'],
        connections: [],
        execute: (inputs, state) => ({
            force: inputs.mass * inputs.g,
            state
        })
    },
    {
        id: 'motion-block',
        type: 'motion',
        inputs: { x: 200, y: 100, vx: 5, vy: 0, dt: 0.016 },
        connections: [],
        execute: (inputs, state) => ({
            x: inputs.x + inputs.vx * inputs.dt,
            y: inputs.y + inputs.vy * inputs.dt,
            state
        })
    }
];

// Run simulation
animation.start((frameInfo) => {
    // Update and execute blocks
    engine.executeBlocks(blocks, frameInfo).then(state => {
        // Render
        renderer.clear();
        ctx.fillStyle = '#667eea';
        ctx.beginPath();
        ctx.arc(state.x || 200, state.y || 100, 10, 0, Math.PI * 2);
        ctx.fill();
    });
});
```

---

## Physics Simulation Examples

### Example 1: Bouncing Ball

```javascript
const blocks = [
    {
        id: 'gravity',
        type: 'gravity',
        inputs: { mass: 1, g: 9.8 },
        execute: AdvancedBlockTypes.physics.gravity.execute
    },
    {
        id: 'motion',
        type: 'motion',
        inputs: { x: 200, y: 50, vx: 2, vy: 0, dt: 0.016 },
        execute: AdvancedBlockTypes.physics.motion.execute
    },
    {
        id: 'collision',
        type: 'collision',
        inputs: { x1: 200, y1: 100, r1: 10, x2: 200, y2: 380, r2: 200 },
        execute: AdvancedBlockTypes.physics.collision.execute
    },
    {
        id: 'bounce',
        type: 'bounce',
        inputs: { vx: 2, vy: 0, elasticity: 0.8, hitX: 'bottom' },
        execute: AdvancedBlockTypes.physics.bounce.execute
    }
];
```

### Example 2: Particle System

```javascript
const blocks = [
    {
        id: 'particle-system',
        type: 'particleSystem',
        inputs: {
            x: 300, y: 200,
            vx: 10, vy: -10,
            count: 20,
            mass: 0.5,
            gravity: 5,
            lifetime: 2000,
            spread: 45
        },
        execute: AdvancedBlocksExtended.particles.particleSystem.execute
    },
    {
        id: 'particle-update',
        type: 'particleUpdate',
        inputs: { particles: [], dt: 0.016, damping: 0.98 },
        execute: AdvancedBlocksExtended.particles.particleUpdate.execute
    },
    {
        id: 'particle-renderer',
        type: 'particleRenderer',
        inputs: { particles: [], size: 5, color: '#667eea' },
        execute: BlockRendererSystem.blocks.particleRenderer.execute
    }
];
```

### Example 3: Spring Physics

```javascript
const blocks = [
    {
        id: 'spring',
        type: 'springPhysics',
        inputs: {
            x: 100,
            vx: 0,
            target_x: 300,
            k: 0.1,      // Spring constant
            c: 0.05,      // Damping coefficient
            dt: 0.016
        },
        execute: AdvancedBlocksExtended.physics.springPhysics.execute
    },
    {
        id: 'shape-renderer',
        type: 'shapeRenderer',
        inputs: {
            x: 0,  // Will be filled from spring block
            y: 200,
            width: 20,
            height: 20,
            shape: 'circle',
            color: '#667eea'
        },
        execute: BlockRendererSystem.blocks.shapeRenderer.execute
    }
];
```

---

## Animation Examples

### Example 1: Smooth Tween

```javascript
const animation = new AnimationSystem();

animation.start((frameInfo) => {
    const tweenValue = (frameInfo.elapsed / 2); // 2 second tween
    
    // Use easing
    const easeFunc = EasingFunctions.easeInOut;
    const easedValue = easeFunc(Math.min(1, tweenValue));
    
    // Apply to position
    const x = 100 + easedValue * 200;
    
    // Draw
    ctx.fillStyle = '#667eea';
    ctx.fillRect(x - 10, 200 - 10, 20, 20);
});
```

### Example 2: Keyframe Animation

```javascript
const timeline = new KeyframeTimeline();

// Add keyframes
timeline.addKeyframe(0, 100);      // At 0s, x = 100
timeline.addKeyframe(1, 300);      // At 1s, x = 300
timeline.addKeyframe(2, 100);      // At 2s, x = 100

timeline.play();

animation.start((frameInfo) => {
    timeline.update(frameInfo.deltaTime);
    const x = timeline.getValueAtTime(timeline.currentTime, 'easeInOut');
    
    // Draw at x position
    ctx.fillStyle = '#667eea';
    ctx.fillRect(x - 10, 200 - 10, 20, 20);
});
```

---

## Marketplace Integration

### Example 1: Browse Simulators

```javascript
const api = new MarketplaceAPIClient('http://localhost:3000');
const ui = new MarketplaceUI(api);

// Initialize marketplace
await ui.init();

// Search
ui.search('physics');

// Filter
ui.applyFilters({ category: 'Physics', difficulty: 'advanced' });

// Sort
ui.sort('highest-rated');
```

### Example 2: Use Simulator in Course

```javascript
// From marketplace detail page
const sim = await api.getSimulatorById(123);

// Add to course
const blocks = JSON.parse(sim.data);
courseBlocks = [...courseBlocks, ...blocks];

// Save to course
saveCourse({
    id: courseId,
    blocks: courseBlocks,
    simulators: [{ id: 123, version: sim.version }]
});
```

### Example 3: Create & Publish Simulator

```javascript
// Create simulator
const newSim = await api.createSimulator({
    title: 'My Particle Explosion',
    description: 'Creates an explosion effect with particles',
    data: JSON.stringify(blocks),
    category: 'Particles',
    difficulty: 'intermediate',
    tags: 'particles,physics,animation'
});

// Publish to marketplace
await api.publishSimulator(newSim.id);

// Get my simulators
const mySims = await api.getMySimulators();
```

---

## For Developers - Integration Checklist

### 1. Add to HTML Page

```html
<script src="block-physics-engine.js"></script>
<script src="block-execution-engine.js"></script>
<script src="advanced-block-types.js"></script>
<script src="advanced-blocks-extended.js"></script>
<script src="block-renderer-system.js"></script>
<script src="block-animation.js"></script>
<script src="marketplace-api-client.js"></script>
<script src="marketplace-ui.js"></script>
<script src="your-main-script.js"></script>
```

### 2. Initialize Everything

```javascript
// Physics & Execution
const engine = new BlockExecutionEngine();
const api = new MarketplaceAPIClient('http://localhost:3000');
const animation = new AnimationSystem();
const ui = new MarketplaceUI(api);

// Canvas
const canvas = document.getElementById('canvas');
BlockRendererSystem.init(canvas);
```

### 3. Wire Up Events

```javascript
// When block executes
engine.executeBlocks(blocks).then(state => {
    // Update simulation state
    currentState = state;
});

// When simulator selected from marketplace
document.addEventListener('use-in-course', (e) => {
    const simulator = e.detail;
    importSimulator(simulator);
});

// Animation loop
animation.start((frameInfo) => {
    // Update and render
    updateSimulation(frameInfo);
    render();
});
```

### 4. Error Handling

```javascript
try {
    const result = await engine.executeBlocks(blocks);
    console.log('Execution successful', result);
} catch (error) {
    console.error('Execution failed:', error);
    showError('Simulation error: ' + error.message);
}

try {
    const simulators = await api.getSimulators();
    ui.simulators = simulators;
    ui.render();
} catch (error) {
    console.error('API error:', error);
    showError('Failed to load simulators');
}
```

---

## Advanced: Creating Custom Blocks

```javascript
const MyCustomBlock = {
    title: 'Custom Physics',
    category: 'Physics',
    inputs: [
        { name: 'value1', type: 'number', default: 0 },
        { name: 'value2', type: 'number', default: 0 }
    ],
    outputs: ['result'],
    
    execute: (inputs, state) => {
        // Your custom logic here
        const result = inputs.value1 + inputs.value2;
        
        return {
            result,
            state: { ...state, lastResult: result }
        };
    }
};

// Add to simulator
const blocks = [
    {
        id: 'custom-1',
        type: 'customPhysics',
        inputs: { value1: 10, value2: 20 },
        execute: MyCustomBlock.execute
    }
];
```

---

## Performance Tips

1. **Use easing functions for smooth animations**
   ```javascript
   const eased = EasingFunctions.easeInOutCubic(progress);
   ```

2. **Limit particle count for performance**
   ```javascript
   count: Math.min(particles.length, 1000) // Cap at 1000
   ```

3. **Cache frequently used objects**
   ```javascript
   const vector = new Vector(x, y);
   const cached = vector.clone(); // Reuse
   ```

4. **Use appropriate delta-time**
   ```javascript
   dt: frameInfo.deltaTime, // Auto-adjust to frame rate
   ```

5. **Clear trails regularly**
   ```javascript
   BlockRendererSystem.rendererState.trails = []; // When needed
   ```

---

## Debugging

### Check Execution
```javascript
const report = engine.getPerformanceReport();
console.log(report);
// { totalTime, averageTime, slowestBlocks, blockCount, fps }
```

### Debug Specific Block
```javascript
const debug = engine.debugBlock('my-block-id');
console.log(debug);
// { blockId, state, executionTime, history, errors }
```

### Monitor Physics
```javascript
const v1 = new Vector(10, 5);
const v2 = new Vector(3, 4);
console.log('Magnitude:', v1.magnitude()); // 11.18
console.log('Dot product:', v1.dot(v2));  // 50
```

---

## Links & References

- **Block Execution**: BlockExecutionEngine class
- **Physics**: Vector, Collision, Physics, Constraint classes
- **Rendering**: BlockRendererSystem.blocks
- **Animation**: AnimationSystem, EasingFunctions classes
- **Marketplace**: MarketplaceAPIClient, MarketplaceUI classes

---

*For complete documentation, see IMPLEMENTATION_SUMMARY.md*
