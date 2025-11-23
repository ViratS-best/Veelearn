# SESSION 30 - START HERE

**Status**: Interactive simulator architecture missing - needs to be rebuilt
**Time**: ~5 hours
**Difficulty**: Medium
**Priority**: 🔴 CRITICAL

---

## THE PROBLEM IN 30 SECONDS

User asked: **"How are sims supposed to be interactive if there's nothing to interact with?"**

Answer: **There's nothing interactive. It's just a config editor.**

- ❌ No real-time execution
- ❌ No sliders to control shapes
- ❌ No live canvas updates
- ❌ No block connections

**But old code had all of this.**

---

## WHAT YOU NEED TO BUILD

### 1. Real-time Execution (When user moves slider)
```javascript
slider.addEventListener('input', (e) => {
  variables['radius'] = e.target.value;
  executeSimulation(); // RE-RUN IMMEDIATELY
});
```

### 2. Canvas Updates (Draw based on new values)
```javascript
function executeSimulation() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  blocks.forEach(block => {
    // ACTUALLY EXECUTE AND DRAW
    if (block.type === 'draw-circle') {
      ctx.fillStyle = block.color;
      ctx.arc(x, y, radius, 0, Math.PI * 2); // USE NEW RADIUS!
      ctx.fill();
    }
  });
}
```

### 3. Interactive Sliders (From block parameters)
```javascript
blocks.forEach(block => {
  if (block.type === 'slider') {
    const slider = document.createElement('input');
    slider.type = 'range';
    slider.addEventListener('input', (e) => {
      variables[block.name] = e.target.value;
      executeSimulation();
    });
  }
});
```

---

## THREE STEPS

### Step 1: Add Animation Loop
**File**: block-simulator.html
**What**: requestAnimationFrame loop for 60 FPS

### Step 2: Copy Old Code
**From**: User's old handleRunVisualSimulator() function
**To**: Current block-simulator.html
**Why**: It works!

### Step 3: Add Block Connections
**What**: Visual lines between blocks
**Why**: So blocks can pass data to each other

---

## KEY FILES

- **block-simulator.html** - Main simulator editor (needs executeSimulation)
- **block-templates-unified.js** - Block definitions (should be OK)
- **script.js** - Course management (should be OK)

---

## OLD CODE REFERENCE

User provided this working code:

```javascript
// THIS WORKS - use it as foundation
function handleRunVisualSimulator(event) {
  // Create canvas
  // Create interactive controls (sliders/buttons)
  // Create executeSimulation() function
  // Call executeSimulation() initially
  // On slider change: call executeSimulation() again
  // Canvas updates with new values
}

// THIS IS WHAT'S MISSING
function executeSimulation() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  
  blocks.forEach(simBlock => {
    switch(simBlock.type) {
      case 'draw-circle':
        // ACTUALLY DRAW WITH CURRENT VALUES
        ctx.fillStyle = currentValues['color'];
        ctx.arc(currentValues['x'], currentValues['y'], currentValues['radius'], 0, Math.PI*2);
        ctx.fill();
        break;
      // Add more block types
    }
  });
}
```

---

## QUICK CHECKLIST

- [ ] Read SESSION_30_CRITICAL_DISCOVERY.md
- [ ] Open block-simulator.html
- [ ] Find where "Run" button is clicked
- [ ] Implement executeSimulation() function
- [ ] Add animation loop (requestAnimationFrame)
- [ ] Add slider event listeners
- [ ] Test: drag block to canvas, click Run, move slider
- [ ] Verify: canvas updates in real-time as you move slider

---

## EXPECTED RESULT AFTER SESSION 30

**Before**: ❌ Static preview
**After**: ✅ Interactive canvas
- Drag slider → shape changes instantly
- Click button → action executes
- All parameters affect canvas in real-time

---

## TIME BREAKDOWN

| Task | Time |
|------|------|
| Understand problem | 15 mins |
| Add executeSimulation() | 45 mins |
| Add animation loop | 30 mins |
| Add slider controls | 45 mins |
| Test everything | 30 mins |
| Add block connections (bonus) | 1-2 hours |
| **Total** | **~4-5 hours** |

---

## SUCCESS = THIS WORKS

1. Create course with block simulator
2. Add blocks (circle, rectangle, etc.)
3. Click "Run"
4. Slider appears on left
5. Move slider → circle changes size on canvas
6. All in real-time

---

**Everything you need is documented.**
**Old code is the reference.**
**Go build it.**

---

_Session 30 Kickoff_
_November 23, 2025_
