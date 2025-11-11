# Integration Instructions - Veelearn Block Simulator

**How to integrate all new systems into block-simulator.html**

---

## Step 1: Update block-simulator.html

Add these script tags in the correct order (BEFORE your main script):

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Veelearn Block Simulator</title>
    <style>
        /* Your existing styles */
        body { font-family: Arial, sans-serif; }
        #canvas { border: 1px solid #ccc; }
        #error-container { color: red; padding: 10px; background: #ffe0e0; }
        #performance { font-size: 12px; color: #666; }
        .block-panel { display: flex; gap: 20px; }
        #block-list { flex: 1; }
        #canvas-container { flex: 2; }
    </style>
</head>
<body>
    <h1>Veelearn Block-Based Simulator</h1>
    
    <!-- Error display -->
    <div id="error-container" style="display: none;"></div>
    
    <!-- Performance monitor -->
    <div id="performance"></div>
    
    <!-- Main content -->
    <div class="block-panel">
        <div id="block-list">
            <h2>Blocks</h2>
            <div id="block-palette"></div>
            <button id="run-simulation">▶ Run Simulation</button>
            <button id="stop-simulation">⏹ Stop</button>
            <button id="clear-canvas">🗑 Clear</button>
        </div>
        
        <div id="canvas-container">
            <h2>Canvas</h2>
            <canvas id="canvas" width="600" height="400" style="border: 1px solid #333;"></canvas>
        </div>
    </div>

    <!-- PHYSICS & EXECUTION ENGINES -->
    <script src="block-physics-engine.js"></script>
    <script src="block-execution-engine.js"></script>
    
    <!-- BLOCK DEFINITIONS -->
    <script src="advanced-block-types.js"></script>
    <script src="advanced-blocks-extended.js"></script>
    
    <!-- RENDERING & ANIMATION -->
    <script src="block-renderer-system.js"></script>
    <script src="block-animation.js"></script>
    
    <!-- MARKETPLACE -->
    <script src="marketplace-api-client.js"></script>
    <script src="marketplace-ui.js"></script>
    
    <!-- YOUR MAIN APPLICATION SCRIPT -->
    <script src="block-simulator-app.js"></script>
</body>
</html>
```

---

## Step 2: Create block-simulator-app.js

This is your main application script that ties everything together:

```javascript
/**
 * Block Simulator Application
 * Main logic for the block-based simulator
 */

// ===== INITIALIZATION =====
let courseBlocks = [];
let currentEditingBlock = null;
let engine = null;
let animation = null;
let canvas = null;
let ctx = null;
let isRunning = false;

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeSimulator();
});

function initializeSimulator() {
    // Get canvas
    canvas = document.getElementById('canvas');
    ctx = canvas.getContext('2d');
    
    // Initialize systems
    engine = new BlockExecutionEngine();
    animation = new AnimationSystem();
    BlockRendererSystem.init(canvas);
    
    // Create marketplace API
    const api = new MarketplaceAPIClient('http://localhost:3000');
    
    // Render block palette
    renderBlockPalette();
    
    // Wire up event handlers
    setupEventHandlers();
    
    console.log('Simulator initialized');
}

// ===== BLOCK PALETTE =====

function renderBlockPalette() {
    const palette = document.getElementById('block-palette');
    const allBlocks = {
        ...AdvancedBlockTypes,
        ...AdvancedBlocksExtended,
        ...BlockRendererSystem.blocks,
        ...AnimationBlocks
    };
    
    let html = '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">';
    
    Object.entries(allBlocks).forEach(([category, blocks]) => {
        if (typeof blocks === 'object' && blocks.title) {
            // Single block
            html += `
                <div style="padding: 10px; border: 1px solid #ccc; cursor: pointer;" 
                     onclick="addBlockFromPalette('${blocks.category}', '${blocks.title}')">
                    <strong>${blocks.title}</strong>
                    <small>${blocks.category}</small>
                </div>
            `;
        } else if (typeof blocks === 'object') {
            // Category of blocks
            Object.entries(blocks).forEach(([name, block]) => {
                if (block.title) {
                    html += `
                        <div style="padding: 10px; border: 1px solid #ddd; cursor: pointer;"
                             onclick="addBlockFromPalette('${block.category}', '${block.title}')">
                            <strong>${block.title}</strong><br>
                            <small>${block.category}</small>
                        </div>
                    `;
                }
            });
        }
    });
    
    html += '</div>';
    palette.innerHTML = html;
}

function addBlockFromPalette(category, title) {
    // Create new block instance
    const blockDef = findBlockDefinition(category, title);
    if (!blockDef) {
        console.error(`Block not found: ${title}`);
        return;
    }
    
    const newBlock = {
        id: `block-${Date.now()}`,
        type: title.toLowerCase().replace(/\s+/g, '-'),
        category,
        inputs: {},
        connections: [],
        
        // Copy defaults
        ...blockDef,
        
        // Set default inputs
        inputs: blockDef.inputs ? blockDef.inputs.reduce((acc, input) => {
            acc[input.name] = input.default;
            return acc;
        }, {}) : {}
    };
    
    courseBlocks.push(newBlock);
    console.log('Added block:', newBlock);
}

function findBlockDefinition(category, title) {
    // Search in AdvancedBlockTypes
    for (const [catKey, blocks] of Object.entries(AdvancedBlockTypes)) {
        if (typeof blocks === 'object' && blocks.title === title) {
            return blocks;
        }
    }
    
    // Search in AdvancedBlocksExtended
    for (const [catKey, blocks] of Object.entries(AdvancedBlocksExtended)) {
        if (typeof blocks === 'object' && blocks.title === title) {
            return blocks;
        }
        
        if (typeof blocks === 'object') {
            for (const block of Object.values(blocks)) {
                if (block.title === title) {
                    return block;
                }
            }
        }
    }
    
    // Search in renderer blocks
    for (const block of Object.values(BlockRendererSystem.blocks)) {
        if (block.title === title) {
            return block;
        }
    }
    
    // Search in animation blocks
    for (const block of Object.values(AnimationBlocks)) {
        if (block.title === title) {
            return block;
        }
    }
    
    return null;
}

// ===== SIMULATION EXECUTION =====

async function runSimulation() {
    if (isRunning) return;
    isRunning = true;
    
    try {
        // Validate blocks
        engine.validateBlocks(courseBlocks);
        
        // Start animation loop
        animation.start((frameInfo) => {
            // Clear canvas
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Add frame info to state
            const state = frameInfo;
            
            // Execute blocks
            try {
                const result = engine.executeBlocks(courseBlocks, state);
                
                // Update performance display
                updatePerformanceDisplay();
            } catch (error) {
                showError('Block execution failed: ' + error.message);
                stopSimulation();
            }
        });
        
    } catch (error) {
        showError('Simulation error: ' + error.message);
        isRunning = false;
    }
}

function stopSimulation() {
    animation.stop();
    isRunning = false;
}

function clearCanvas() {
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    BlockRendererSystem.rendererState.trails = [];
}

// ===== PERFORMANCE MONITORING =====

function updatePerformanceDisplay() {
    const report = engine.getPerformanceReport();
    const perfDiv = document.getElementById('performance');
    
    if (perfDiv) {
        perfDiv.innerHTML = `
            FPS: ${report.fps.toFixed(1)} | 
            Blocks: ${report.blockCount} | 
            Time: ${report.totalTime.toFixed(2)}ms | 
            Avg: ${report.averageTime.toFixed(3)}ms
        `;
    }
}

// ===== ERROR HANDLING =====

function showError(message) {
    const errorContainer = document.getElementById('error-container');
    if (errorContainer) {
        errorContainer.textContent = message;
        errorContainer.style.display = 'block';
        setTimeout(() => {
            errorContainer.style.display = 'none';
        }, 5000);
    }
}

// ===== EVENT HANDLERS =====

function setupEventHandlers() {
    // Run button
    document.getElementById('run-simulation')?.addEventListener('click', runSimulation);
    
    // Stop button
    document.getElementById('stop-simulation')?.addEventListener('click', stopSimulation);
    
    // Clear button
    document.getElementById('clear-canvas')?.addEventListener('click', clearCanvas);
    
    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        if (e.code === 'Space' && e.ctrlKey) {
            e.preventDefault();
            isRunning ? stopSimulation() : runSimulation();
        }
    });
}

// ===== BLOCK MANAGEMENT =====

function deleteBlock(blockId) {
    courseBlocks = courseBlocks.filter(b => b.id !== blockId);
    console.log('Deleted block:', blockId);
}

function updateBlockInput(blockId, inputName, value) {
    const block = courseBlocks.find(b => b.id === blockId);
    if (block) {
        block.inputs[inputName] = value;
        console.log(`Updated ${blockId}.${inputName} = ${value}`);
    }
}

function connectBlocks(fromBlockId, outputName, toBlockId, inputName) {
    const fromBlock = courseBlocks.find(b => b.id === fromBlockId);
    if (fromBlock) {
        if (!fromBlock.connections) fromBlock.connections = [];
        fromBlock.connections.push({
            sourceBlockId: fromBlockId,
            sourceOutput: outputName,
            targetBlockId: toBlockId,
            targetInput: inputName
        });
        console.log(`Connected ${fromBlockId}.${outputName} -> ${toBlockId}.${inputName}`);
    }
}

// ===== SAVE/LOAD =====

function saveCourse() {
    const courseData = JSON.stringify(courseBlocks, null, 2);
    localStorage.setItem('veelearn-course-blocks', courseData);
    console.log('Course saved');
}

function loadCourse() {
    const courseData = localStorage.getItem('veelearn-course-blocks');
    if (courseData) {
        try {
            courseBlocks = JSON.parse(courseData);
            console.log('Course loaded:', courseBlocks.length, 'blocks');
        } catch (error) {
            console.error('Failed to load course:', error);
        }
    }
}

// Auto-save periodically
setInterval(() => {
    if (courseBlocks.length > 0) {
        saveCourse();
    }
}, 30000); // Every 30 seconds
```

---

## Step 3: Integration Test

### 1. Test Physics Simulation

```javascript
// In browser console
const testBlocks = [
    {
        id: 'grav',
        type: 'gravity',
        inputs: { mass: 1, g: 9.8 },
        connections: [],
        execute: AdvancedBlockTypes.physics.gravity.execute
    }
];

engine.executeBlocks(testBlocks);
// Should return { force: 9.8, state: ... }
```

### 2. Test Animation Loop

```javascript
let frameCount = 0;
animation.start((frameInfo) => {
    frameCount++;
    console.log(`Frame ${frameCount}, FPS: ${frameInfo.fps.toFixed(1)}`);
    if (frameCount > 60) animation.stop();
});
```

### 3. Test Renderer

```javascript
BlockRendererSystem.init(canvas);
BlockRendererSystem.blocks.shapeRenderer.execute({
    x: 300,
    y: 200,
    width: 50,
    height: 50,
    shape: 'circle',
    color: '#667eea',
    rotation: 0,
    alpha: 1,
    outline_color: '#333',
    outline_width: 2
}, {}, ctx);
// Should draw circle on canvas
```

### 4. Test Marketplace

```javascript
const api = new MarketplaceAPIClient('http://localhost:3000');
const simulators = await api.getSimulators(1, 10);
console.log('Found', simulators.length, 'simulators');
```

---

## Step 4: Add CSS Styling

```css
/* block-simulator.css */

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    padding: 20px;
    background: #f5f5f5;
}

h1 {
    color: #333;
    margin-bottom: 20px;
}

h2 {
    font-size: 18px;
    color: #555;
    margin-top: 0;
}

.block-panel {
    display: flex;
    gap: 20px;
    margin-bottom: 20px;
}

#block-list {
    flex: 0 0 300px;
    background: white;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

#canvas-container {
    flex: 1;
    background: white;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

#canvas {
    width: 100%;
    height: 400px;
    border: 1px solid #ddd;
    background: white;
    display: block;
}

#error-container {
    background: #fee;
    color: #c33;
    border: 1px solid #fcc;
    padding: 15px;
    border-radius: 4px;
    margin-bottom: 20px;
}

#performance {
    font-size: 13px;
    color: #666;
    background: #f9f9f9;
    padding: 10px;
    border-radius: 4px;
    margin-bottom: 15px;
    font-family: monospace;
}

button {
    background: #667eea;
    color: white;
    border: none;
    padding: 10px 15px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    margin-right: 10px;
    margin-bottom: 10px;
}

button:hover {
    background: #5568d3;
}

button#stop-simulation {
    background: #f56565;
}

button#stop-simulation:hover {
    background: #e53e3e;
}

button#clear-canvas {
    background: #ed8936;
}

button#clear-canvas:hover {
    background: #dd6b20;
}

[style*="grid-template-columns"] > div {
    background: #fafafa;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    padding: 10px;
    cursor: pointer;
    transition: all 0.2s;
}

[style*="grid-template-columns"] > div:hover {
    background: #f0f0f0;
    border-color: #667eea;
    box-shadow: 0 2px 4px rgba(102, 126, 234, 0.2);
}
```

---

## Step 5: Verify Integration

```javascript
// In browser console, verify all systems loaded:

console.log('BlockExecutionEngine:', typeof BlockExecutionEngine);
console.log('Vector:', typeof Vector);
console.log('Collision:', typeof Collision);
console.log('Physics:', typeof Physics);
console.log('Constraint:', typeof Constraint);
console.log('AdvancedBlockTypes:', typeof AdvancedBlockTypes);
console.log('AdvancedBlocksExtended:', typeof AdvancedBlocksExtended);
console.log('BlockRendererSystem:', typeof BlockRendererSystem);
console.log('AnimationSystem:', typeof AnimationSystem);
console.log('EasingFunctions:', typeof EasingFunctions);
console.log('KeyframeTimeline:', typeof KeyframeTimeline);
console.log('MarketplaceAPIClient:', typeof MarketplaceAPIClient);
console.log('MarketplaceUI:', typeof MarketplaceUI);

// All should be "function" or "object"
```

---

## Troubleshooting

### Issue: Scripts not loading
- **Check**: Console errors (F12 -> Console tab)
- **Fix**: Verify script paths are correct
- **Fix**: Ensure scripts are in correct order

### Issue: Canvas not rendering
- **Check**: `BlockRendererSystem.init(canvas)` called
- **Check**: Canvas element exists with id="canvas"
- **Fix**: Verify ctx is not null

### Issue: Blocks not executing
- **Check**: Block inputs have default values
- **Check**: execute function is defined
- **Fix**: Use block definitions from AdvancedBlockTypes

### Issue: Performance issues
- **Check**: Check `getPerformanceReport()`
- **Fix**: Reduce number of blocks
- **Fix**: Reduce particle count
- **Fix**: Reduce canvas size

---

## Next Steps

1. ✅ Add HTML pages (simulator-detail.html, simulator-creator.html)
2. ✅ Create CSS file (block-simulator.css)
3. ✅ Add more block types as needed
4. ✅ Implement block connection UI
5. ✅ Add course integration
6. ✅ Deploy to production

---

*For questions or issues, refer to QUICK_START_GUIDE.md or IMPLEMENTATION_SUMMARY.md*
