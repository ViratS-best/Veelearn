# SESSION 26 - IMPLEMENTATION FIXES

## PRIORITY 1: Add "Save Draft" Button (30 minutes)

### Step 1: Update HTML with 2 buttons (in index.html)

Find the course editor buttons section and replace:
```html
<!-- OLD - Single publish button -->
<button onclick="publishCourse()">Publish Course</button>
```

With:
```html
<!-- NEW - Separate draft and publish buttons -->
<button onclick="saveCourse()" style="background: #666; color: white; padding: 10px 20px; margin-right: 10px;">💾 Save as Draft</button>
<button onclick="publishCourse()" style="background: #667eea; color: white; padding: 10px 20px;">📤 Submit for Approval</button>
```

### Step 2: Update saveCourse() in script.js (lines 777-865)

Current code sends to `/api/courses` POST endpoint. Need to:
1. Keep saveCourse() as-is for saving draft
2. Create new publishCourse() function

**Add this after saveCourse():**
```javascript
function publishCourse() {
  if (!confirm("Are you sure? Once submitted, admins must review and approve before it goes public.")) {
    return;
  }
  
  const title = document.getElementById("course-title").value;
  const description = document.getElementById("course-description").value;
  const content = document.getElementById("course-content-editor").innerHTML;

  if (!title.trim()) {
    alert("Please enter a course title");
    return;
  }

  const courseData = {
    title,
    description,
    content,
    blocks: courseBlocks,
  };

  const method = currentEditingCourseId ? "PUT" : "POST";
  const url = currentEditingCourseId
    ? `http://localhost:3000/api/courses/${currentEditingCourseId}`
    : "http://localhost:3000/api/courses";

  // NOTE: Backend already sets status='pending' by default
  // If we need draft status, backend must support it
  
  fetch(url, {
    method,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${authToken}`,
    },
    body: JSON.stringify(courseData),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        alert("Course submitted for admin approval! Admins will review and approve it.");
        showDashboard();
      } else {
        alert("Error: " + (data.message || "Unknown error"));
      }
    })
    .catch((err) => {
      console.error("Error publishing course:", err);
      alert("Error submitting course");
    });
}
```

### Step 3: Update backend if needed (server.js)

The backend already supports status='pending' but might need:
- Add status='draft' to schema
- Or clarify that pending is "submitted not approved"

---

## PRIORITY 2: Debug Simulator Save (1 hour)

### Step 1: Add logging to block-simulator.html publishSimulator()

Find the publishSimulator() function (around line 858) and add detailed logging:

```javascript
async function publishSimulator() {
  const simulatorName = prompt("Enter simulator name:");
  if (!simulatorName) return;

  const authToken = localStorage.getItem("token");
  
  console.log("=== PUBLISHING SIMULATOR ===");
  console.log("1. Auth token exists:", !!authToken);
  console.log("2. Blocks to save:", courseBlocks.length);
  console.log("3. Block data:", JSON.stringify(courseBlocks, null, 2));
  
  const simulatorData = {
    title: simulatorName,
    description: `Created with ${courseBlocks.length} blocks`,
    blocks: courseBlocks,
    connections: currentConnections || [],
  };
  
  console.log("4. Data being sent to server:", JSON.stringify(simulatorData, null, 2));

  fetch("http://localhost:3000/api/simulators", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${authToken}`,
    },
    body: JSON.stringify(simulatorData),
  })
    .then((res) => {
      console.log("5. Server response status:", res.status);
      return res.json();
    })
    .then((data) => {
      console.log("6. Server response:", data);
      if (data.success) {
        console.log("✅ Simulator published successfully. ID:", data.data?.id);
        alert("Simulator published successfully!");
      } else {
        console.error("❌ Publish failed:", data.message);
        alert("Error: " + data.message);
      }
    })
    .catch((err) => {
      console.error("7. Network error:", err);
      alert("Error publishing simulator");
    });
}
```

### Step 2: Verify backend receives and saves data (server.js)

Find POST /api/simulators endpoint (around line 1200) and verify:

```javascript
app.post('/api/simulators', authenticateToken, (req, res) => {
    const { title, description, blocks, connections } = req.body;
    const creatorId = req.user.id;
    
    console.log("BACKEND: Received simulator data:");
    console.log("- Title:", title);
    console.log("- Blocks:", blocks ? blocks.length : 0);
    console.log("- Connections:", connections ? connections.length : 0);
    
    // ... rest of endpoint
    
    // When inserting, make sure blocks and connections are saved:
    const query = `INSERT INTO simulators 
      (title, description, creator_id, blocks, connections, status)
      VALUES (?, ?, ?, ?, ?, 'published')`;
    
    db.query(query, 
      [title, description, creatorId, JSON.stringify(blocks), JSON.stringify(connections)],
      (err, result) => {
        if (err) {
          console.error("INSERT ERROR:", err);
          return apiResponse(res, 500, 'Error saving simulator');
        }
        console.log("✅ Simulator saved with ID:", result.insertId);
        apiResponse(res, 201, 'Simulator created', { id: result.insertId });
      }
    );
});
```

### Step 3: Test the flow

1. Start backend with logging visible
2. Create simulator with 3-4 blocks
3. Click Publish
4. **Check console** - should see all 7 log messages
5. Check browser DevTools Network tab - should see POST request
6. Check backend console - should see "Simulator saved with ID: X"
7. Check database: `SELECT * FROM simulators WHERE title LIKE '%test%'`

---

## PRIORITY 3: Fix Simulator View (1 hour)

### Step 1: Check simulator-view.html loads from API

The file should have something like:
```javascript
document.addEventListener('DOMContentLoaded', () => {
  const simulatorId = new URLSearchParams(location.search).get('id');
  
  // Fetch simulator
  fetch(`http://localhost:3000/api/simulators/${simulatorId}`, {
    headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
  })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        // Parse blocks and connections
        const blocks = JSON.parse(data.data.blocks);
        const connections = JSON.parse(data.data.connections);
        
        // Render to canvas
        renderSimulator(blocks, connections);
      }
    });
});
```

### Step 2: Verify block execution initializes

Must have:
```javascript
function renderSimulator(blocks, connections) {
  // Initialize canvas
  const canvas = document.getElementById('simulator-canvas');
  const ctx = canvas.getContext('2d');
  
  // Execute blocks
  executeBlocks(blocks).then(results => {
    // Render results to canvas
  });
}
```

### Step 3: Test the view

1. Go to marketplace
2. Click on a simulator that was published
3. Should navigate to: `simulator-view.html?id=123`
4. **Check console** for fetch errors
5. Should see blocks rendered on canvas
6. Can run simulation

---

## PRIORITY 4: Add Admin Course Preview (1.5 hours)

### Step 1: Create preview modal in admin dashboard

In index.html, find pending courses list and update buttons:

```html
<!-- OLD -->
<button onclick="approveCourse(${course.id})">Approve</button>

<!-- NEW -->
<button onclick="previewCourse(${course.id})">Preview</button>
<button onclick="approveCourse(${course.id})">Approve</button>
<button onclick="rejectCourse(${course.id})">Reject</button>
```

### Step 2: Add previewCourse() function in script.js

```javascript
function previewCourse(courseId) {
  const course = myCourses.find(c => c.id === courseId) || availableCourses.find(c => c.id === courseId);
  
  if (!course) {
    alert("Course not found");
    return;
  }
  
  const modalHTML = `
    <div style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.7); display: flex; align-items: center; justify-content: center; z-index: 9999;">
      <div style="background: white; padding: 30px; border-radius: 8px; max-width: 800px; max-height: 80vh; overflow-y: auto;">
        <h2>${course.title}</h2>
        <p><strong>Creator:</strong> ${course.creator_email}</p>
        <p><strong>Description:</strong> ${course.description}</p>
        
        <h3>Course Content</h3>
        <div style="background: #f5f5f5; padding: 15px; border-radius: 4px; margin: 10px 0;">
          ${course.content || '<em>No content</em>'}
        </div>
        
        <h3>Linked Simulators</h3>
        <div id="preview-simulators" style="margin: 10px 0;">Loading...</div>
        
        <div style="margin-top: 20px; display: flex; gap: 10px;">
          <button onclick="approveCourseFromPreview(${courseId})" style="background: #4caf50; color: white; padding: 10px 20px; border-radius: 4px; cursor: pointer;">✅ Approve</button>
          <button onclick="rejectCourseFromPreview(${courseId})" style="background: #f44336; color: white; padding: 10px 20px; border-radius: 4px; cursor: pointer;">❌ Reject</button>
          <button onclick="closePreviewModal()" style="background: #999; color: white; padding: 10px 20px; border-radius: 4px; cursor: pointer;">Close</button>
        </div>
      </div>
    </div>
  `;
  
  document.body.insertAdjacentHTML('beforeend', modalHTML);
  
  // Load simulators for this course
  loadCourseSimulators(courseId);
}

function approveCourseFromPreview(courseId) {
  approveCourse(courseId);
  closePreviewModal();
}

function rejectCourseFromPreview(courseId) {
  const feedback = prompt("Enter rejection feedback:");
  if (!feedback) return;
  
  rejectCourse(courseId, feedback);
  closePreviewModal();
}

function closePreviewModal() {
  const modal = document.querySelector('[style*="position: fixed"]');
  if (modal) modal.remove();
}
```

### Step 3: Verify approve/reject endpoints exist

Backend should have:
```javascript
app.put('/api/admin/courses/:id/status', authenticateToken, authorize('admin', 'superadmin'), (req, res) => {
  // Existing code at line 742
})
```

---

## TESTING CHECKLIST AFTER FIXES

- [ ] Create course → Click "Save as Draft" → Verify in database status='draft' (if implemented)
- [ ] Create course → Click "Submit for Approval" → Verify status='pending'
- [ ] Create simulator → Click "📤 Publish" → Check console logs
- [ ] Check database: simulators table has blocks and connections
- [ ] Go to marketplace → Click simulator → Should load and render
- [ ] As admin, click "Preview" on pending course → Should see all content
- [ ] Admin clicks "Approve" → Course appears in public list
- [ ] Admin clicks "Reject" → Can enter feedback

---

## SUMMARY OF CHANGES

| File | Change | Priority |
|------|--------|----------|
| index.html | Add "Save Draft" button | HIGH |
| script.js | Add publishCourse() function | HIGH |
| block-simulator.html | Add debug logging | HIGH |
| server.js | Verify POST /api/simulators saves all data | HIGH |
| simulator-view.html | Verify loads and renders simulator | HIGH |
| index.html | Add preview button for admin | MEDIUM |
| script.js | Add previewCourse() function | MEDIUM |
| server.js | Verify PUT /api/admin/courses/:id/status works | MEDIUM |
