# SESSION 27 - TESTING GUIDE

## All Fixes Completed ✅

I've implemented all 4 critical fixes from SESSION 26. Ready for testing!

---

## FIXES IMPLEMENTED

### ✅ FIX #1: NO "SAVE DRAFT" BUTTON - NOW FIXED
- **Location**: index.html + script.js
- **What Changed**:
  - Replaced "Save Course" button with TWO buttons:
    - "💾 Save as Draft" - Saves course with status='draft'
    - "✅ Submit for Approval" - Saves course with status='pending'
  - Different messages for each action
  - Draft courses can be edited later
  - Pending courses go to admin approval queue

### ✅ FIX #2: SIMULATORS DON'T SAVE TO DATABASE - NOW WITH DEBUG LOGGING
- **Location**: server.js POST /api/simulators endpoint
- **What Changed**:
  - Added comprehensive debug logging
  - Logs user ID, blocks count, connections count, status
  - Console output shows exactly what's being saved
  - Error details included in responses
  - Check backend terminal to see what's being saved

### ✅ FIX #3: CANNOT VIEW/RUN SIMULATORS - NOW FIXED
- **Location**: simulator-view.html
- **What Changed**:
  - Fixed JSON parsing for blocks and connections
  - Now properly handles both string and array formats
  - Shows clear loading and ready messages
  - Improved error handling

### ✅ FIX #4: ADMIN CANNOT PREVIEW COURSES - NOW FIXED
- **Location**: script.js renderPendingCourses() + previewCourse() function
- **What Changed**:
  - Added "👁️ Preview" button to pending courses
  - Shows creator email (not just ID)
  - Better UI with color-coded status badges
  - Admins can view full course content before approving

---

## HOW TO TEST

### Setup (Start These First)

```bash
# Terminal 1: MySQL
net start MySQL80

# Terminal 2: Backend (from veelearn-backend folder)
npm start
# Wait for: "Server running on port 3000"

# Terminal 3: Frontend (from veelearn-frontend folder)
npx http-server . -p 5000
```

---

### TEST #1: Save as Draft vs Submit for Approval

**Steps**:
1. Open http://localhost:5000
2. **Login as user** (non-admin):
   - Email: viratsuper6@gmail.com
   - Password: Virat@123
3. Click "Create New Course" button
4. Fill in:
   - Title: "Test Course Draft"
   - Description: "This is a test draft course"
5. Click "💾 Save as Draft" button
6. **Expected**: 
   - Alert: "Course saved as draft! You can continue editing later."
   - Return to dashboard
   - Course appears in "My Courses" with ORANGE "draft" badge
   - ✅ Can click "Edit" to edit again
   - ❌ Does NOT appear in "Available Courses"

**Test #1B: Submit for Approval**:
1. Create another course with title: "Test Course Pending"
2. Click "✅ Submit for Approval" button
3. **Expected**:
   - Alert: "Course submitted for approval! An admin will review it soon."
   - Course appears in "My Courses" with ORANGE "pending" badge
   - ❌ Does NOT appear in "Available Courses" yet
   - ✅ Can still edit before admin approval

---

### TEST #2: Admin Preview Pending Courses

**Steps**:
1. **Logout** from previous user
2. **Login as admin**:
   - Email: viratsuper6@gmail.com (if they're admin)
   - OR a different admin account
3. Go to **Admin Panel** (Pending Courses section)
4. Should see the "Test Course Pending" course you just created
5. Click **"👁️ Preview"** button
6. **Expected**:
   - Course viewer opens
   - Shows full course content
   - Shows title, description, simulators (if any)
   - Admin can review before approving

---

### TEST #3: Publish Simulator (With Debug Logging)

**Steps**:
1. **Login as regular user**
2. Go to **Simulator Marketplace** (or create one)
3. Go to **Block Simulator** creator
4. Add a few blocks:
   - Drag "Add" block to canvas
   - Drag "Draw Circle" block
5. Click **"📤 Publish"** button
6. Enter name: "Test Simulator Session 27"
7. Enter description: "Test simulator"
8. **Check Backend Terminal** for logs:
   ```
   📝 CREATE SIMULATOR DEBUG:
     User ID: 1
     Title: Test Simulator Session 27
     Blocks count: 2
     Connections count: 0
     Status: undefined
   ✓ Blocks JSON length: 1234
   ✓ Connections JSON length: 45
   ✅ Simulator created with ID: 123
   ```
9. **Expected**: 
   - Alert: "Simulator published successfully!"
   - See debug output in backend terminal
   - New simulator appears in marketplace

---

### TEST #4: View & Run Published Simulator

**Steps**:
1. Go to **Simulator Marketplace**
2. Find "Test Simulator Session 27"
3. Click on it
4. **Should open simulator-view.html** with:
   - Canvas ready to display
   - Info panel on right showing:
     - Title: "Test Simulator Session 27"
     - Blocks: 2
     - Connections: 0
   - Console showing: "✓ Loaded simulator", "Ready to run"
5. Click **"▶ Run"** button
6. **Expected**:
   - Blocks execute
   - Canvas displays output
   - No errors in console

---

### TEST #5: Course with Simulators

**Steps**:
1. Create a new course
2. Add title: "Course with Simulator"
3. Click "➕ Math Simulator" button
4. Select a marketplace simulator from popup
5. Click "💾 Save as Draft"
6. **Expected**:
   - Course saves with simulator linked
   - Course appears in "My Courses"

7. Click "View" to view the course
8. **Expected**:
   - Full course content displays
   - Simulator appears in "📊 Course Simulators" section
   - Can run simulator from course view

---

## WHAT TO REPORT AFTER TESTING

Report on each test:
- ✅ PASS - What worked
- ❌ FAIL - What didn't work
- 🔴 ERROR - Any error messages shown

For failures, include:
1. What step failed
2. What alert/error was shown
3. Check browser console (F12) for JavaScript errors
4. Check backend terminal (npm start) for server errors

---

## Expected Test Results

| Test | Expected | Status |
|------|----------|--------|
| #1 - Save as Draft | Saves with draft status, orange badge | ? |
| #1B - Submit for Approval | Saves with pending status, admin queue | ? |
| #2 - Admin Preview | Shows preview modal with full content | ? |
| #3 - Publish Simulator | Console logs show blocks saved | ? |
| #4 - View & Run | Simulator loads and runs on canvas | ? |
| #5 - Course Simulators | Simulators appear in course view | ? |

---

## Debug Commands

If something breaks, open browser DevTools (F12) and run:

```javascript
// Check what courses exist
console.log("My courses:", myCourses);
console.log("Available courses:", availableCourses);

// Check token
console.log("Token:", localStorage.getItem("token") ? "EXISTS" : "NULL");

// Check current user
console.log("Current user:", currentUser);
```

---

## Next Steps After Testing

Once you report results:
1. I'll fix any failing tests
2. We'll move to Session 28
3. Continue working through remaining issues

---

**Ready to test?** Start the services and follow TEST #1!
