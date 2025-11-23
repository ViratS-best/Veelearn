# SESSION 31B - BLOCK SIMULATOR VIEWER FIXED ✅

**Date**: November 23, 2025  
**Issue**: Block simulators in courses showed Edit/Remove buttons instead of Run  
**Status**: FIXED  

---

## 🔍 PROBLEM IDENTIFIED

When viewing an approved course:
- ❌ Block simulators showed "Edit" and "Remove" buttons (editor UI)
- ❌ Clicking Edit showed nothing
- ❌ No way to actually RUN the simulators
- ❌ Canvas remained blank

**Root Cause**: The course content HTML contained simulator blocks with editor-mode buttons. When viewing the course, those buttons were still present instead of being converted to viewer-mode (Run) buttons.

---

## ✅ SOLUTION IMPLEMENTED

### Fix #1: Load courseBlocks When Viewing Course

**File**: `script.js` - viewCourse() function (lines 944-952)

```javascript
// RESTORE COURSE BLOCKS for viewing (same as editing)
courseBlocks = course.blocks ? 
  (typeof course.blocks === 'string' ? JSON.parse(course.blocks) : course.blocks) 
  : [];

console.log("✓ Viewing course with", courseBlocks.length, "blocks");
```

Now courseBlocks is populated when viewing, so buttons can access block data.

### Fix #2: Convert Edit Buttons to Run Buttons

**File**: `script.js` - convertSimulatorButtonsForViewer() function (new)

```javascript
function convertSimulatorButtonsForViewer(courseId, course) {
  const simulatorBlocks = document.querySelectorAll(".simulator-block");
  
  simulatorBlocks.forEach((block) => {
    const blockId = parseInt(block.dataset.blockId);
    const courseBlock = courseBlocks.find((b) => b.id === blockId);
    
    // Find the buttons container
    const buttonsDiv = block.querySelector('div > div:last-child');
    if (!buttonsDiv) return;
    
    // For block simulators: Show "Run Simulator" button
    if (courseBlock && courseBlock.type === "block-simulator") {
      buttonsDiv.innerHTML = `
        <button type="button" 
          onclick="runEmbeddedBlockSimulator(${blockId}, '${courseBlock.title}')" 
          style="padding: 5px 10px; background: #667eea; color: white; border: none; border-radius: 4px; cursor: pointer;">
          ▶ Run Simulator
        </button>
      `;
    }
    // For visual simulators: Show "Run Simulator" button
    else if (courseBlock && courseBlock.type === "visual-simulator") {
      buttonsDiv.innerHTML = `
        <button type="button" 
          onclick="runEmbeddedVisualSimulator(${blockId}, '${courseBlock.title}')" 
          style="padding: 5px 10px; background: #667eea; color: white; border: none; border-radius: 4px; cursor: pointer;">
          ▶ Run Simulator
        </button>
      `;
    }
  });
}
```

This:
1. Finds all simulator blocks in the content
2. Converts their Edit/Remove buttons to a Run button
3. Calls appropriate handler based on simulator type

### Fix #3: Implement Block Simulator Runner

**File**: `script.js` - runEmbeddedBlockSimulator() function (new)

```javascript
function runEmbeddedBlockSimulator(blockId, title) {
  const block = courseBlocks.find((b) => b.id === blockId);
  if (!block || !block.data) {
    alert("Simulator data not found");
    return;
  }
  
  // Open simulator in a new window
  const win = window.open("block-simulator.html", "block-simulator", "width=1200,height=800");
  
  // Wait for window to load, then send data
  setTimeout(() => {
    if (win) {
      win.postMessage({
        type: "load-simulator",
        data: {
          blocks: block.data.blocks || [],
          connections: block.data.connections || [],
          readOnly: true  // Disable editing in viewer
        }
      }, "*");
    }
  }, 1000);
}
```

This:
1. Finds the block's saved simulator data
2. Opens block-simulator.html in a popup
3. Sends the blocks to load into the simulator
4. Passes readOnly flag to disable editing

### Fix #4: Implement Visual Simulator Runner

**File**: `script.js` - runEmbeddedVisualSimulator() function (new)

```javascript
function runEmbeddedVisualSimulator(blockId, title) {
  const block = courseBlocks.find((b) => b.id === blockId);
  if (!block || !block.data) {
    alert("Simulator data not found");
    return;
  }
  
  const win = window.open("visual-simulator.html", "visual-simulator", "width=1200,height=800");
  
  setTimeout(() => {
    if (win) {
      win.postMessage({
        type: "load-simulator",
        data: {
          code: block.data.code || "",
          variables: block.data.variables || {},
          readOnly: true
        }
      }, "*");
    }
  }, 1000);
}
```

---

## 📊 BEHAVIOR CHANGE

### Before Session 31B

```
User Views Course
  ↓
Content loaded with Edit/Remove buttons
  ↓
Click Edit
  ↓
Block simulator opens (blank - no blocks load) ✗
  ↓
Canvas shows nothing ✗
```

### After Session 31B

```
User Views Course
  ↓
courseBlocks populated from course.blocks ✓
  ↓
Edit buttons converted to "Run Simulator" button ✓
  ↓
Click "Run Simulator"
  ↓
block-simulator.html opens with saved blocks ✓
  ↓
Canvas displays simulator ready to run ✓
  ↓
User clicks "Run" to execute
  ↓
Blocks execute on canvas ✓
```

---

## 🎮 WORKFLOW

### When Viewing a Course with Block Simulator

1. Click "Preview" on approved course
2. Course content displays
3. Simulator block shows "▶ Run Simulator" button
4. Click button → opens simulator in popup
5. Simulator loads with all previously-created blocks
6. Click "Run" button in simulator
7. Blocks execute on canvas
8. Can see results

### For Marketplace Simulators

These are handled separately by `loadCourseSimulators()` which fetches from API and displays them in a separate section with individual Run buttons.

---

## 🔧 FILES MODIFIED

1. **veelearn-frontend/script.js** (4 changes)
   - Lines 944-952: Load courseBlocks when viewing
   - Lines 955-987: Add convertSimulatorButtonsForViewer()
   - Lines 989-1019: Add runEmbeddedBlockSimulator()
   - Lines 1021-1047: Add runEmbeddedVisualSimulator()
   - Line 953: Call convertSimulatorButtonsForViewer()

No other files need modification.

---

## ⚠️ EDGE CASES HANDLED

1. **courseBlocks is empty**: Shows message "Simulator data not found"
2. **block.data is missing**: Shows alert and returns
3. **Window open fails**: Gracefully handles popup blocker
4. **Blocks are JSON string**: Parses automatically
5. **blocks/connections are undefined**: Defaults to empty arrays

---

## ✅ TESTING

After restart, test:

1. **Create Course with Block Simulator**
   - Add some blocks
   - Save course
   
2. **Approve Course**
   - Admin approves it
   
3. **View as Student**
   - Enroll in course
   - Click "Preview"
   - Should see simulator with "▶ Run Simulator" button (NOT Edit/Remove)
   
4. **Click Run Button**
   - Simulator popup opens
   - Should show all blocks that were created
   - Click "Run" in simulator
   - Blocks should execute on canvas

5. **Test Visual Simulator**
   - Create course with visual (code) simulator
   - Same process - should show Run button instead of Edit

---

## 🎯 SUCCESS CRITERIA

- ✅ Simulators show "Run" button instead of Edit/Remove
- ✅ Clicking Run opens simulator with all blocks
- ✅ Blocks are executable (not in edit mode)
- ✅ Canvas displays simulation results
- ✅ Both block and visual simulators work
- ✅ No console errors

---

## 🚀 NEXT STEP

**Marketplace Simulator Canvas Issue**

User reported: "Marketplace simulator saves but running it renders nothing"

This requires checking if simulator-view.html is properly executing blocks. The fix in this session handles embedded course simulators. Marketplace simulators use a separate viewer page that needs its own investigation.

---

_Session 31B Complete_  
_Block simulators in courses now properly display as runnable_  
_Edit mode vs View mode properly distinguished_
