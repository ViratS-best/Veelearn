# SESSION 18 - REMAINING ISSUES TO FIX 🚨

## Issue #1: Course Simulators Not Displaying in Course View

### Problem
- User creates course and adds simulators
- Course is saved successfully
- But when viewing the course, simulators don't appear

### Root Cause Analysis
**Code Location**: `script.js` - Functions `loadCourseSimulators()` and `displayCourseSimulators()`

**Current Flow**:
1. User creates course and adds simulators via marketplace selector
2. `saveCourse()` calls `POST /api/courses/:id/simulators` for each simulator
3. Course is created/updated successfully
4. When viewing course, `viewCourse()` calls `loadCourseSimulators(courseId)`
5. `loadCourseSimulators()` calls `GET /api/courses/:courseId/simulators`
6. Data is supposed to be returned by backend...
7. BUT simulators don't display in the UI

### Code That Needs Debugging

**In script.js - loadCourseSimulators() function (Line 820)**:
```javascript
function loadCourseSimulators(courseId) {
  const authToken = localStorage.getItem("token");
  
  fetch(`http://localhost:3000/api/courses/${courseId}/simulators`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      ...(authToken ? { Authorization: `Bearer ${authToken}` } : {}),
    },
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success && data.data && data.data.length > 0) {
        displayCourseSimulators(data.data);  // ← THIS LINE NOT EXECUTING?
      } else {
        document.getElementById("course-simulators-section").style.display = "none";
      }
    })
    .catch((err) => {
      console.error("Error loading course simulators:", err);
      document.getElementById("course-simulators-section").style.display = "none";
    });
}
```

### Debugging Steps

1. **Check Backend Response**:
   - Add console.log in `loadCourseSimulators()` after fetch
   - Check what data is being returned from `/api/courses/:courseId/simulators`
   - Verify response format matches expected: `{ success: true, data: [...] }`

2. **Check DisplayCourseSimulators()**:
   - Verify HTML elements exist with correct IDs:
     - `course-simulators-section` (container div)
     - `course-simulators-list` (list element)
   - Add console.log to see if function is being called

3. **Check saveCourse()**:
   - Verify `POST /api/courses/:id/simulators` is being called
   - Check if simulator_id is being sent correctly in request body
   - Verify backend creates records in `course_simulator_usage` table

### Fix Needed

Add debug logging to `script.js`:

```javascript
function loadCourseSimulators(courseId) {
  const authToken = localStorage.getItem("token");
  console.log("🔍 Loading simulators for course:", courseId);  // DEBUG
  
  fetch(`http://localhost:3000/api/courses/${courseId}/simulators`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      ...(authToken ? { Authorization: `Bearer ${authToken}` } : {}),
    },
  })
    .then((res) => res.json())
    .then((data) => {
      console.log("🔍 API Response:", data);  // DEBUG
      if (data.success && data.data && data.data.length > 0) {
        console.log("🔍 Displaying", data.data.length, "simulators");  // DEBUG
        displayCourseSimulators(data.data);
      } else {
        console.log("🔍 No simulators found or API error");  // DEBUG
        document.getElementById("course-simulators-section").style.display = "none";
      }
    })
    .catch((err) => {
      console.error("❌ Error loading course simulators:", err);
      document.getElementById("course-simulators-section").style.display = "none";
    });
}
```

---

## Issue #2: Course Content Only Saving Title/Description

### Problem
- User creates course with title and description
- User adds simulators to course
- When course is saved, only title and description are stored
- Simulator content is not visible in the `content` field

### Root Cause Analysis

**Code Location**: `script.js` - Function `saveCourse()` (Line 732)

**Current Code**:
```javascript
function saveCourse() {
  const title = document.getElementById("course-title").value;
  const description = document.getElementById("course-description").value;
  const content = document.getElementById("course-content-editor").innerHTML;
  
  const courseData = {
    title,
    description,
    content,
    blocks: courseBlocks,  // ← This is array of blocks being sent
  };
  
  // ... sends to API
  
  // Then separately saves simulators
  const simulatorPromises = courseBlocks
    .filter((block) => block.simulatorId)
    .map((block) =>
      fetch(`http://localhost:3000/api/courses/${courseId}/simulators`, {
        // ... POST to link simulator to course
      })
    );
}
```

### The Problem

1. **Two-Step Save Process**:
   - Step 1: Save course basic info (title, description, content)
   - Step 2: Link simulators via separate API call to `/api/courses/:id/simulators`

2. **Issue**: 
   - The `courseBlocks` array is being sent but backend may not be storing it
   - The simulators are linked in step 2, but the `content` field doesn't include simulator info
   - So when viewing course, there's no reference to simulators in the main `content` field

### Fix Needed

**Option 1: Store Simulator IDs in Course Content**
```javascript
function saveCourse() {
  const title = document.getElementById("course-title").value;
  const description = document.getElementById("course-description").value;
  let content = document.getElementById("course-content-editor").innerHTML;
  
  // Add simulator references to content
  if (courseBlocks && courseBlocks.length > 0) {
    const simulatorRefs = courseBlocks
      .map(block => `<simulator-id>${block.simulatorId}</simulator-id>`)
      .join('');
    content += `\n<!-- Linked Simulators -->\n${simulatorRefs}`;
  }
  
  const courseData = {
    title,
    description,
    content,
    blocks: courseBlocks,
  };
  // ... rest of save logic
}
```

**Option 2: Verify Backend /api/courses/:id/simulators**
- Make sure endpoint properly links simulators
- When loading course, fetch both course content AND linked simulators
- Display them together in UI

### Recommended Solution

**Use Option 2** - it's cleaner:
1. Keep save logic as-is
2. In `viewCourse()`, after loading course content, also load simulators
3. Display both content and simulators together
4. This is already implemented in `loadCourseSimulators()`!

So the issue is likely that `loadCourseSimulators()` is failing silently and returning no data.

---

## Testing Steps for Both Issues

### Test Course Simulator Display

1. **Create a course**:
   - Go to Dashboard → Create New Course
   - Enter title: "Test Course"
   - Enter description: "Testing simulator display"
   - Don't add any simulators yet
   - Click Save

2. **Add Simulators**:
   - After saving, go back to edit course
   - Click one of the "Add Math/Coding/Visual/Block" buttons
   - Select a simulator from marketplace
   - Confirm it's added to course
   - Click Save again

3. **View Course**:
   - Go back to Dashboard
   - Find your course in "My Courses"
   - Click View Course
   - **SHOULD SEE**: Simulators displayed under "Simulators" section
   - **IF BUG**: No simulators section visible

4. **Debug**:
   - Open DevTools (F12)
   - Go to Console tab
   - Look for "🔍 Loading simulators" debug message
   - Check what API response shows
   - Report the exact error message

### Expected Behavior

```
Course Page Should Show:
├─ Title
├─ Description  
└─ Simulators Section
   ├─ Simulator 1
   │  ├─ Title
   │  ├─ Description
   │  └─ Run Simulator button
   ├─ Simulator 2
   │  ...
```

---

## Files to Check/Modify

- **script.js**: Functions `saveCourse()`, `loadCourseSimulators()`, `displayCourseSimulators()`
- **server.js**: Endpoint `GET /api/courses/:courseId/simulators`
- **simulator-view.html**: Should load and display simulator when clicked

---

*Generated: November 11, 2025 - Session 18*
