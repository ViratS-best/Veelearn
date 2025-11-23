# Session 22 - Detailed Code Fixes

## Overview
All code exists but may need minor fixes. This document contains the exact fixes to apply if issues are confirmed.

---

## FIX #1: Token Storage Verification

### File: `veelearn-frontend/script.js` (Line 91)

**Current Code:**
```javascript
localStorage.setItem("token", authToken);
```

**Enhanced Code with Verification:**
```javascript
localStorage.setItem("token", authToken);
console.log("✓ Token stored successfully");
console.log("✓ Token value:", authToken.substring(0, 30) + "...");
console.log("✓ Token retrieved from localStorage:", localStorage.getItem("token") ? "EXISTS" : "NOT FOUND");
console.log("✓ All localStorage keys:", Object.keys(localStorage));
```

**Why:** Confirms token is stored with correct key "token" not "authToken"

---

## FIX #2: Block Templates Verification

### File: `veelearn-frontend/block-simulator.html` (Line 410-424)

**Current Code:**
```javascript
if (!blockTemplates || Object.keys(blockTemplates).length === 0) {
  console.error("ERROR: blockTemplates not loaded...");
}
```

**Enhanced Code:**
```javascript
if (!blockTemplates || Object.keys(blockTemplates).length === 0) {
  console.error("ERROR: blockTemplates not loaded! Make sure block-templates-unified.js is loaded.");
  console.error("Window blockTemplates:", typeof blockTemplates);
  console.error("blockTemplates value:", blockTemplates);
  logToConsole("CRITICAL ERROR: Block templates not loaded", "error");
} else {
  console.log("✓ Block templates loaded successfully");
  console.log("✓ Total templates:", Object.keys(blockTemplates).length);
  console.log("✓ Template names:", Object.keys(blockTemplates).slice(0, 10));
  logToConsole(`✓ ${Object.keys(blockTemplates).length} block templates loaded`, "info");
}
```

**Why:** Helps identify if templates file failed to load

---

## FIX #3: Drag Handler with Template Validation

### File: `veelearn-frontend/block-simulator.html` (Line 444-457)

**Current Code:**
```javascript
document.querySelectorAll(".block-palette .block").forEach((block) => {
  block.addEventListener("dragstart", (e) => {
    draggedBlockPalette = {
      type: e.target.dataset.type,
      title: e.target.textContent.trim(),
    };
    e.dataTransfer.effectAllowed = "copy";
    console.log("Drag started from palette:", draggedBlockPalette.type);
  });
});
```

**Enhanced Code with Validation:**
```javascript
document.querySelectorAll(".block-palette .block").forEach((block) => {
  block.addEventListener("dragstart", (e) => {
    const blockType = e.target.dataset.type;
    
    // Validate template exists
    if (!blockTemplates || !blockTemplates[blockType]) {
      console.error("❌ Template not found for block type:", blockType);
      console.error("Available templates:", Object.keys(blockTemplates || {}).slice(0, 10));
      e.preventDefault();
      return;
    }
    
    draggedBlockPalette = {
      type: blockType,
      title: e.target.textContent.trim(),
    };
    e.dataTransfer.effectAllowed = "copy";
    console.log("✓ Drag started from palette:", blockType);
    console.log("✓ Template found:", blockTemplates[blockType].title);
    logToConsole(`Starting drag: ${blockType}`, "info");
  });
  
  block.addEventListener("dragend", (e) => {
    console.log("Drag ended from palette");
    draggedBlockPalette = null;
  });
});
```

**Why:** Ensures template exists before allowing drag, prevents undefined errors

---

## FIX #4: Drop Handler with Position Logging

### File: `veelearn-frontend/block-simulator.html` (Line 472-517)

**Current Code:**
```javascript
workspaceEl.addEventListener("drop", (e) => {
  e.preventDefault();
  console.log("Drop detected, draggedBlockPalette:", draggedBlockPalette);
  
  if (!draggedBlockPalette) {
    console.log("No dragged block palette, returning");
    return;
  }
  // ... rest of code
});
```

**Enhanced Code with Detailed Logging:**
```javascript
workspaceEl.addEventListener("drop", (e) => {
  e.preventDefault();
  e.stopPropagation();
  workspaceEl.style.backgroundColor = "#1a1a2e";
  
  console.log("=== DROP EVENT FIRED ===");
  console.log("draggedBlockPalette:", draggedBlockPalette);
  
  if (!draggedBlockPalette) {
    console.warn("⚠️ No dragged block palette, drop ignored");
    return;
  }
  
  const rect = workspaceEl.getBoundingClientRect();
  const x = Math.max(0, e.clientX - rect.left);
  const y = Math.max(0, e.clientY - rect.top);
  
  console.log("✓ Drop position:", { x: Math.round(x), y: Math.round(y) });
  console.log("✓ Block type:", draggedBlockPalette.type);
  
  const blockType = draggedBlockPalette.type;
  const template = blockTemplates[blockType];
  
  if (!template) {
    console.error("❌ Template not found for block type:", blockType);
    logToConsole(`Block type '${blockType}' not found`, "error");
    return;
  }
  
  console.log("✓ Creating block:", { type: blockType, x, y });
  
  const newBlock = {
    id: blockIdCounter++,
    type: blockType,
    x: x,
    y: y,
    inputs: {},
  };
  
  if (template.inputs) {
    template.inputs.forEach((input) => {
      newBlock.inputs[input.name] = input.default !== undefined ? input.default : "";
    });
  }
  
  blocks.push(newBlock);
  renderBlocks();
  draggedBlockPalette = null;
  
  console.log("✓ Block added successfully, total blocks:", blocks.length);
  logToConsole(`✓ Added ${template.title || blockType} block`);
});
```

**Why:** Tracks exact position where block is dropped and validates template

---

## FIX #5: Publish Simulator with Better Error Messages

### File: `veelearn-frontend/block-simulator.html` (Line 858-918)

**Current Code** (already has debug, but enhance it):
```javascript
async function publishSimulator() {
  try {
    const authToken = localStorage.getItem("token");
    console.log("Token value:", authToken ? authToken.substring(0, 30) + "..." : "NULL");
    
    if (!authToken) {
      alert("ERROR: Not authenticated. Cannot publish simulator. Please login again.");
      return;
    }
    // ... rest of code
  }
}
```

**Enhanced Code:**
```javascript
async function publishSimulator() {
  try {
    console.log("=== PUBLISH SIMULATOR INITIATED ===");
    console.log("All localStorage keys:", Object.keys(localStorage));
    
    const authToken = localStorage.getItem("token");
    
    console.log("Token check result:");
    console.log("  - Token exists:", !!authToken);
    console.log("  - Token length:", authToken ? authToken.length : 0);
    console.log("  - Token preview:", authToken ? authToken.substring(0, 50) + "..." : "NULL");
    
    if (!authToken) {
      console.error("❌ CRITICAL: No authentication token found!");
      console.log("User should login first");
      alert("ERROR: Not authenticated. Cannot publish simulator. Please login again.");
      logToConsole("ERROR: No authentication token - login required", "error");
      return;
    }
    
    const simulatorName = prompt("Enter simulator name:", "My Simulator");
    if (!simulatorName) {
      console.log("User cancelled simulator name prompt");
      return;
    }
    
    const simulatorData = {
      title: simulatorName,
      description: prompt("Enter simulator description:", "") || "No description",
      blocks: blocks,
      connections: connections,
      status: "published",
    };
    
    console.log("Sending publish request:", simulatorData);
    
    const response = await fetch("http://localhost:3000/api/simulators", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${authToken}`,
      },
      body: JSON.stringify(simulatorData),
    });
    
    console.log("Response status:", response.status, response.statusText);
    
    if (!response.ok) {
      const error = await response.json();
      console.error("API Error:", error);
      throw new Error(error.message || "Failed to publish simulator");
    }
    
    const result = await response.json();
    console.log("✓ Simulator published successfully!");
    console.log("Simulator ID:", result.data.simulatorId);
    logToConsole(`✓ Simulator published! ID: ${result.data.simulatorId}`, "info");
    alert("✓ Simulator published successfully!");
    
  } catch (error) {
    console.error("❌ Publish failed:", error);
    console.error("Error details:", error.message);
    logToConsole(`Publish failed: ${error.message}`, "error");
    alert(`Failed to publish simulator: ${error.message}`);
  }
}
```

**Why:** Shows exactly where the publish process fails with detailed logging

---

## FIX #6: Add Course Status Debug

### File: `veelearn-frontend/script.js` - in `loadAvailableCourses()` function

**Add After Course Load:**
```javascript
// After fetching courses from API
console.log("=== COURSE LOADING DEBUG ===");
console.log("Total courses from API:", courses.length);
console.log("Current user ID:", currentUser.id);
console.log("Course details:");
courses.forEach(c => {
  console.log({
    id: c.id,
    title: c.title,
    status: c.status,
    creator_id: c.creator_id,
    isOwn: c.creator_id === currentUser.id,
    shouldShow: (c.status === 'approved' && c.creator_id !== currentUser.id) || c.creator_id === currentUser.id
  });
});

// Show filtering logic
const filtered = courses.filter(c => c.status === 'approved' && c.creator_id !== currentUser.id);
console.log("Courses after filter (approved, not own):", filtered.length);
```

**Why:** Shows exactly which courses are being filtered and why

---

## FIX #7: Add Script Loading Error Handlers

### File: `veelearn-frontend/block-simulator.html` (Around Line 370-385)

**Add After Script Tags:**
```html
<script>
  // Global error handler for script loading
  window.addEventListener('error', (event) => {
    if (event.filename && event.filename.includes('.js')) {
      console.error('❌ Script Error:', {
        file: event.filename,
        message: event.message,
        line: event.lineno,
        column: event.colno
      });
    }
  });
  
  // Check if all required libraries are loaded
  document.addEventListener('DOMContentLoaded', () => {
    const required = ['blockTemplates', 'BlockExecutionEngine'];
    const missing = required.filter(lib => typeof window[lib] === 'undefined');
    
    if (missing.length > 0) {
      console.error('❌ Missing libraries:', missing);
    } else {
      console.log('✓ All required libraries loaded');
    }
  });
</script>
```

**Why:** Catches script loading errors that would silently fail

---

## FIX #8: Ensure Drag-Drop is Ready

### File: `veelearn-frontend/block-simulator.html` (Line 410-425)

**Wrap Drag Setup:**
```javascript
// Wait for DOM and templates to be ready
setTimeout(() => {
  // Check if templates are ready
  if (!blockTemplates || Object.keys(blockTemplates).length === 0) {
    console.error("ERROR: blockTemplates not loaded");
    setTimeout(arguments.callee, 500); // Retry
    return;
  }
  
  console.log("✓ Block templates ready, setting up drag/drop");
  
  // Now setup drag listeners
  document.querySelectorAll(".block-palette .block").forEach((block) => {
    block.addEventListener("dragstart", handleDragStart);
    block.addEventListener("dragend", handleDragEnd);
  });
  
  console.log("✓ Drag/drop event listeners attached");
  console.log("✓ Ready for block dragging");
  
}, 500);
```

**Why:** Ensures templates are loaded before setting up drag handlers

---

## Quick Apply Guide

### To Apply All Fixes at Once:

1. **Backup current files**:
   ```bash
   copy veelearn-frontend\script.js veelearn-frontend\script.js.backup
   copy veelearn-frontend\block-simulator.html veelearn-frontend\block-simulator.html.backup
   ```

2. **Make code changes** (from above)

3. **Test in browser**:
   - F12 → Console
   - Perform each action
   - Check console for ✓ or ❌ indicators

4. **Document all console output**

5. **Report back with full console logs**

---

## Testing Command

Run in browser console after each fix:

```javascript
// Test 1: Token
console.log("TEST 1 - Token:", localStorage.getItem('token') ? '✓ EXISTS' : '❌ NULL');

// Test 2: Templates  
console.log("TEST 2 - Templates:", Object.keys(blockTemplates || {}).length + " loaded");

// Test 3: Palette blocks
console.log("TEST 3 - Palette:", document.querySelectorAll('.block-palette .block').length + " blocks");

// Test 4: User
console.log("TEST 4 - User:", currentUser ? currentUser.email : '❌ NOT LOGGED IN');

// Test 5: Courses
console.log("TEST 5 - Courses:", myCourses ? myCourses.length + ' courses' : '❌ NOT LOADED');

// Test 6: API
fetch('http://localhost:3000/api/courses', {
  headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
}).then(r => r.json()).then(d => console.log("TEST 6 - API:", d.success ? '✓ WORKS' : '❌ FAILED'));
```

---

## Success Indicators

After applying fixes, you should see in console:

```
✓ Token stored successfully
✓ Token value: eyJhbGciOiJIUzI1NiIs...
✓ Block templates loaded successfully
✓ Total templates: 40+
✓ Drag started from palette: add
✓ Template found: Add Numbers
✓ Drop position: {x: 123, y: 456}
✓ Creating block: {type: "add", x: 123, y: 456}
✓ Block added successfully, total blocks: 1
✓ Simulator published successfully!
✓ Simulator ID: 42
```

---

## If Issues Persist

1. **Check backend is running**: `curl http://localhost:3000/api/courses`
2. **Check MySQL is running**: `mysql -u root -p -e "SELECT 1"`
3. **Clear browser cache**: Ctrl+Shift+Del → All time
4. **Hard refresh page**: Ctrl+Shift+R
5. **Check for console errors**: F12 → Console tab
6. **Check Network tab**: F12 → Network → Look for failed requests

---

**Ready to apply fixes!** Start with FIX #1 and test each one.
