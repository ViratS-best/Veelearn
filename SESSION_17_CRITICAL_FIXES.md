# SESSION 17 - CRITICAL FIXES NEEDED

## Status from SESSION 16 Testing
User tested all 6 issues. **3 CRITICAL FAILURES FOUND:**

### Failure #1: Cannot Publish Simulators (TEST 6)
**Error**: "ERROR: Not authenticated. Cannot publish simulator."
**File**: block-simulator.html line 461 - publishSimulator()
**Issue**: authToken from localStorage not being sent in POST request
**Location**: Line 478 gets token, but may not be sent in fetch headers

### Failure #2: Cannot View Simulator in Course (TEST 5)
**Error**: Simulator content not displaying in course view
**Files**: 
- script.js loadCourseSimulators() function
- simulator-view.html or course-simulators-section rendering
**Issue**: /api/courses/:id/simulators returns empty or not called

### Failure #3: Course Content Not Saving
**Error**: Only title + description saved, simulator content lost
**File**: script.js saveCourse() function
**Issue**: Simulators not being linked to course via course_simulator_usage table

---

## Fix Priority

1. **FIX #1: Auth Token in publishSimulator()** (30 minutes)
   - Check localStorage token exists
   - Add console.log to debug
   - Verify Authorization header sent in POST
   - Test publish works

2. **FIX #2: Course Content Saving** (45 minutes)
   - Verify saveCourse() links simulators to course
   - Check course_simulator_usage endpoint
   - Test course save persists simulator data

3. **FIX #3: Simulator Display in Course** (30 minutes)
   - Verify loadCourseSimulators() fetches data
   - Check /api/courses/:id/simulators returns data
   - Verify displayCourseSimulators() renders blocks
   - Test simulator displays in course

---

## Quick Debug Steps for Next Session

### To Debug Auth Token Issue:
1. Open block-simulator.html
2. Find publishSimulator() at line 461
3. Add after line 478:
   ```javascript
   console.log("Token:", authToken);
   console.log("Token exists?", !!authToken);
   ```
4. Test publish button
5. Check console for token value

### To Debug Course Save Issue:
1. Open script.js
2. Find saveCourse() function
3. Add console.log to show simulators being saved:
   ```javascript
   console.log("Saving simulators:", courseBlocks);
   ```
4. Create course with simulators
5. Check console for simulator data

### To Debug Simulator Display:
1. Open index.html Course Viewer section
2. Check if #course-simulators-section renders
3. Open browser Network tab
4. Go to view course
5. Check if GET /api/courses/:id/simulators called
6. Check if returns simulator data

---

## Files to Check

**block-simulator.html** - Line 478
```javascript
const authToken = localStorage.getItem("token");
// THIS NEEDS VERIFICATION - token may be null
```

**script.js** - saveCourse() function
```javascript
// Check if simulators are being saved with course
// Verify POST to /api/courses/:id/simulators
```

**script.js** - loadCourseSimulators() function  
```javascript
// Check if API call made and data returned
// Check if displayCourseSimulators() called
```

**server.js** - POST /api/simulators
```javascript
// Verify endpoint returns simulator ID
// Check Authorization check works
```

---

## Expected Results After Fixes

✅ Publish simulator → Success message, simulator saved
✅ View course → Shows embedded simulators
✅ Course content → All data persists (title, description, simulators)
✅ Simulators work end-to-end

---

## Test Cases for Verification

1. **Publish Simulator**
   - Add blocks to simulator
   - Click Publish button
   - Should see: "Simulator published! ID: [number]"
   - Not: "ERROR: Not authenticated"

2. **View Simulator in Course**
   - Create course with simulator
   - Save course
   - View course
   - Should see: Simulator card in course view
   - Can click "Run Simulator"

3. **Course Content Saves**
   - Create course with title, description, simulator
   - Save course
   - Logout/Login
   - View course
   - Should see: All content preserved

---

## Next Session Action Plan

1. Apply FIX #1 (Auth Token) - 30 min
2. Test publish simulator - 10 min
3. Apply FIX #2 (Course Save) - 45 min
4. Test course saving - 10 min
5. Apply FIX #3 (Simulator Display) - 30 min
6. Test simulator displays - 10 min
7. Full end-to-end test - 10 min

**Total**: ~2.5 hours to get all 3 fixes working

---

## Critical Context to Remember

- User is logged in (auth works)
- authToken IS in localStorage
- Issue is token not being SENT in publish request
- Course content save failing (simulators not linked)
- Simulator display broken (not fetching or rendering)

All 3 issues are in the fetch/API layer, not in database or core logic.

---

*Created: November 11, 2025 - End of Session 16*
*Ready for Session 17 fixes*
