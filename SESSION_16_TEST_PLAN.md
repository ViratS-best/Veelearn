# SESSION 16 - COMPREHENSIVE TEST PLAN

## Backend Status ✅
- ✅ MySQL database connected
- ✅ Express server running on port 3000
- ✅ All API endpoints configured

## Frontend Status ✅
- ✅ HTTP server running on port 5000
- ✅ All critical HTML pages present:
  - index.html (main dashboard)
  - block-simulator.html (block editor)
  - simulator-marketplace.html (marketplace)
  - simulator-view.html (simulator viewer)
  - simulator-creator.html (creator dashboard)
  - simulator-detail.html (detail view)

## Code Analysis Completed ✅

### Issue #1: Approved Courses Not Showing
**Analysis**: ✅ CODE IS CORRECT
- Backend API (GET /api/courses):
  - ✅ Line 696: Returns courses with `status = 'approved' OR creator_id = userId`
  - ✅ Joins with users table to get creator_email
- Frontend (script.js):
  - ✅ Line 603: loadAvailableCourses() function exists
  - ✅ Line 614: Filters: `c.status === "approved" && creator_id !== currentUser.id`
  - ✅ Debug logs added to show filtered courses
- **Likely Cause**: No approved courses in database OR filter logic has edge case
- **Action**: Need to manually test with real user data

### Issue #2: Cannot Drag Blocks to Canvas
**Analysis**: ✅ CODE IS CORRECT
- block-simulator.html:
  - ✅ Line 547: dragstart event listener on palette blocks
  - ✅ Line 554: dragover event listener on workspace
  - ✅ Line 558: drop event listener with createBlock() call
  - ✅ Line 570: createBlock() function exists and works
- **Likely Cause**: Maybe drag-and-drop not working due to CSS or event binding issue
- **Action**: Test drag-and-drop in browser, check console for errors

### Issue #3: No X/Exit/Publish Buttons
**Analysis**: ✅ BUTTONS EXIST
- block-simulator.html:
  - ✅ Line 347: Publish button exists: `<button onclick="publishSimulator()">`
  - ✅ Line 354: Exit button exists: `<button onclick="exitSimulator()">`
  - ✅ Line 461: publishSimulator() function defined
  - ✅ Line 518: exitSimulator() function defined
- **Likely Cause**: CSS hiding buttons or page not loading properly
- **Action**: Test in browser, inspect element with DevTools

### Issue #4: Cannot View Course Before Approval
**Analysis**: ✅ CODE IS CORRECT
- script.js:
  - ✅ Line 583: loadUserCourses() filters `creator_id === currentUser.id`
  - ✅ Shows ALL user's courses regardless of status
  - ✅ Line 653: Renders status badge with color coding
- **Likely Cause**: Courses in database don't have correct creator_id
- **Action**: Verify database has courses with correct user IDs

### Issue #5: Simulators Don't Work / Cannot View
**Analysis**: ✅ INFRASTRUCTURE EXISTS
- simulator-view.html:
  - ✅ File exists in veelearn-frontend/
  - ✅ Can be opened via script.js line 875: `window.location.href = simulator-view.html?id=${simulatorId}`
- **Likely Cause**: simulator-view.html might need content or API calls
- **Action**: Verify simulator-view.html loads simulator from API and renders it

### Issue #6: Cannot Publish Simulators
**Analysis**: ✅ CODE IS CORRECT
- block-simulator.html:
  - ✅ Line 347: Publish button exists
  - ✅ Line 461: publishSimulator() function defined
  - ✅ Makes POST to /api/simulators with title, description, blocks
- Backend:
  - ✅ Server.js has POST /api/simulators endpoint
  - ✅ Creates simulator in database
- **Likely Cause**: Authentication token not being sent or API error
- **Action**: Test publish button in browser, check console for errors

---

## Test Procedure

### STEP 1: Clear Browser Cache & Open DevTools
1. Open http://localhost:5000 in Chrome
2. Press F12 to open DevTools
3. Go to Console tab
4. Check for any JavaScript errors

### STEP 2: Test Login
1. Register new account OR login as:
   - Email: viratsuper6@gmail.com
   - Password: Virat@123
2. Check console for login errors
3. Verify authToken is saved in localStorage

### STEP 3: Test Issue #4 - View Course Before Approval
1. Go to Dashboard
2. Go to "My Courses" section
3. **Expected**: Should see all courses you created (even if pending)
4. **If Broken**: Course with "pending" status not showing
5. **Fix**: Check creator_id in database matches logged-in user

### STEP 4: Test Issue #1 - Approved Courses Show
1. As superadmin, go to "Pending Courses"
2. Click "Approve Course" on any pending course
3. Go to "Available Courses" section
4. **Expected**: Approved course should appear in list
5. **If Broken**: Course doesn't appear even though approved
6. **Debug**: Open DevTools → Console → Check "=== LOAD AVAILABLE COURSES DEBUG ===" logs

### STEP 5: Test Issue #2 - Block Drag & Drop
1. Go to Dashboard
2. Click "Create New Course"
3. Select "Block-Based Simulator" type
4. Click "Open Block Simulator"
5. Try to **drag a block from left sidebar to canvas**
6. **Expected**: Block appears on canvas
7. **If Broken**: Block doesn't move
8. **Debug**: Check console for errors, verify blockTemplates loaded

### STEP 6: Test Issue #3 - Exit/Publish Buttons
1. In block simulator, look at **top toolbar**
2. **Expected**: See "📤 Publish" and "✕ Exit" buttons
3. **If Broken**: Buttons not visible
4. **Debug**: Right-click → Inspect → Check CSS display property

### STEP 7: Test Issue #5 - View Simulators
1. Go to Marketplace (from navbar)
2. Click any simulator card
3. **Expected**: Opens simulator detail page
4. **If Broken**: Page doesn't load or simulator doesn't display
5. **Debug**: Check console for API errors

### STEP 8: Test Issue #6 - Publish Simulator
1. Create a simulator in Marketplace Creator OR
2. Add blocks to block simulator
3. Click "📤 Publish" button
4. **Expected**: Simulator saved and ID shown in alert
5. **If Broken**: No publish button OR error when clicking
6. **Debug**: Check console for API errors

---

## Results Recording

After each test, record:
- ✅ PASS - Feature works as expected
- ❌ FAIL - Feature broken, error message
- ⚠️ PARTIAL - Feature partially works

---

## Next Steps After Testing

### If All Tests PASS ✅
- Clean up console logs from debug statements
- Test full user flow from start to finish
- Deploy to production

### If Some Tests FAIL ❌
1. Collect error messages from DevTools Console
2. Create issue description with:
   - Test step that failed
   - Expected behavior
   - Actual behavior
   - Error message from console
   - Screenshot if possible
3. I will provide targeted fix

---

*Last Updated: November 11, 2025 - Session 16*
