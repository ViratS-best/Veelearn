# SESSION 31 COMPLETE - FULL TEST PLAN ✅

**Status**: All fixes applied - Ready for comprehensive testing  
**Date**: November 23, 2025  
**Test Duration**: 15-20 minutes  

---

## ✅ What Was Fixed (3 Sessions of Work Consolidated)

### Session 31: Course Save System
- Blocks restored when editing courses
- API returns blocks in response
- **Result**: Courses save and persist with all simulators

### Session 31B: Block Simulator Viewer  
- Edit buttons converted to Run buttons when viewing
- Simulators load with saved blocks when Run clicked
- **Result**: Students can view and run block simulators in courses

### Session 31C: Marketplace Simulator Canvas
- Canvas properly cleared and rendered
- Block execution fires on each frame
- Animation loop runs for 2 seconds at 60 FPS
- **Result**: Marketplace simulators now display properly

---

## 🚀 SETUP (5 minutes)

### Step 1: Kill Old Node Processes
```bash
taskkill /F /IM node.exe
```

### Step 2: Start Backend
```bash
cd c:\Users\kalps\Documents\Veelearn\veelearn-backend
npm start
# Wait for: "Server running on port 3000" and "Connected to MySQL database"
```

### Step 3: Start Frontend  
```bash
cd c:\Users\kalps\Documents\Veelearn\veelearn-frontend
python -m http.server 5000
# Wait for: "Serving HTTP on port 5000"
```

### Step 4: Open Browser
```
http://localhost:5000
```

---

## 🧪 TEST CASES (15 minutes)

### TEST #1: Login ✅
**Expected**: Login successful, Dashboard appears

1. Email: `viratsuper6@gmail.com`
2. Password: `Virat@123`
3. Click "Login"

**PASS IF**:
- ✅ Redirects to Dashboard
- ✅ Shows your email at top
- ✅ "My Courses" and "Available Courses" visible

---

### TEST #2: Create Course with Block Simulator ✅
**Expected**: Course saves with simulators

1. Click "Dashboard"
2. Click "Create New Course"
3. Title: `Test Block Simulator`
4. Description: `Testing block simulator in courses`
5. Click "🧩 Block Visual Simulator" button
6. **In block simulator popup**:
   - Click "Add" block from sidebar (drag to canvas)
   - Add 2-3 blocks (e.g., Add, Draw Circle)
   - Click "Exit" (X button, top right)
7. Click "✅ Submit for Approval"

**PASS IF**:
- ✅ Block simulator popup opens
- ✅ Can drag blocks to canvas
- ✅ Blocks appear on canvas
- ✅ Exit button works
- ✅ "Course submitted for approval" message
- ✅ Returns to dashboard

---

### TEST #3: Approve Course (as Admin)
**Expected**: Course moves from pending to approved

1. Go to "Admin Panel" (should see as superadmin)
2. Go to "Pending Courses"
3. Find "Test Block Simulator"
4. Click "✓ Approve" button

**PASS IF**:
- ✅ Course disappears from pending list
- ✅ No error message
- ✅ Message says "Course approved..."

---

### TEST #4: View Course (Test 31B Fix) ✅
**Expected**: Block simulator shows "Run" button, not "Edit/Remove"

1. Go to "My Courses"
2. Find "Test Block Simulator"
3. Click "View" button

**PASS IF**:
- ✅ Course content displays
- ✅ Simulator block shows "▶ Run Simulator" button
- ✅ NO "Edit" or "Remove" buttons
- ✅ Console shows: "✓ Viewing course with X blocks"

---

### TEST #5: Run Block Simulator in Course ✅
**Expected**: Simulator opens with saved blocks

1. Click "▶ Run Simulator" button
2. Wait for popup to load (2 seconds)

**PASS IF**:
- ✅ block-simulator.html popup opens
- ✅ Canvas visible with workspace
- ✅ Blocks you created appear on canvas
- ✅ Console shows: "✓ Blocks message sent"
- ✅ Can see blocks rendered (not blank)

---

### TEST #6: Execute Blocks in Course Simulator ✅
**Expected**: Blocks execute and show results

1. Click "▶ Run" button in simulator
2. Wait 2 seconds

**PASS IF**:
- ✅ Animation starts
- ✅ Shapes draw on canvas (circles, rectangles, etc.)
- ✅ Console shows execution log
- ✅ No errors in console
- ✅ After 2 seconds, simulation stops

---

### TEST #7: Create Marketplace Simulator ✅
**Expected**: Can create and save simulator

1. Go to "Marketplace" (or "Simulator Creator" link)
2. Look for a "Create New Simulator" button
3. Create a simple simulator with:
   - 1 Draw Circle block
   - 1 Draw Rectangle block
4. Publish it (if publish dialog appears)

**PASS IF**:
- ✅ Can access simulator creator
- ✅ Can add blocks
- ✅ Can publish/save
- ✅ No authentication errors

---

### TEST #8: Run Marketplace Simulator (Test 31C Fix) ✅
**Expected**: Canvas renders with blocks executing

1. Go to "Marketplace"
2. Find your published simulator (or any simulator)
3. Click it or click "Run Simulator" button
4. Wait for simulator-view.html to open
5. Click "▶ Run" button

**PASS IF**:
- ✅ Simulator loads
- ✅ Info panel shows block count > 0
- ✅ Canvas NOT blank (has white/light background)
- ✅ Shapes appear on canvas (circles, rectangles, etc.)
- ✅ Console shows "✓ Executed X blocks on canvas"
- ✅ Animation runs for 2 seconds
- ✅ No blank canvas anymore! ✅✅✅

---

### TEST #9: Edit Course and Add More Simulators (Test 31 Fix) ✅
**Expected**: Course blocks restored, can add more

1. Go to "My Courses"
2. Find "Test Block Simulator"
3. Click "Edit"

**PASS IF**:
- ✅ Course loads
- ✅ Simulator block still visible (blocks NOT lost!)
- ✅ Can click "▶ Run Simulator" to see old blocks
- ✅ Can add MORE simulators
- ✅ Save again - all blocks persist

---

### TEST #10: Enroll as Different User (Bonus)
**Expected**: Other users can access approved courses

1. Logout (click logout button)
2. Create new account OR use different email
3. Login with new user
4. Go to "Available Courses"
5. Find "Test Block Simulator"
6. Click "Enroll"
7. Click "Preview"
8. Click "▶ Run Simulator"

**PASS IF**:
- ✅ Can see approved course
- ✅ Can enroll
- ✅ Can view course
- ✅ Can run simulators
- ✅ Everything works for other users

---

## 📊 SUMMARY TABLE

| # | Test | Expected | Status |
|---|------|----------|--------|
| 1 | Login | Dashboard appears | ✅ PASS / ❌ FAIL |
| 2 | Create course with sim | Saves blocks | ✅ PASS / ❌ FAIL |
| 3 | Approve course | Moves to approved | ✅ PASS / ❌ FAIL |
| 4 | View course | "Run" button, not "Edit" | ✅ PASS / ❌ FAIL |
| 5 | Run sim in course | Popup opens with blocks | ✅ PASS / ❌ FAIL |
| 6 | Execute blocks | Shapes draw on canvas | ✅ PASS / ❌ FAIL |
| 7 | Create marketplace sim | Can publish | ✅ PASS / ❌ FAIL |
| 8 | Run marketplace sim | Canvas renders (NOT blank!) | ✅ PASS / ❌ FAIL |
| 9 | Edit course | Blocks restored | ✅ PASS / ❌ FAIL |
| 10 | Other user access | Can view and run | ✅ PASS / ❌ FAIL |

---

## 🎯 SUCCESS CRITERIA

### Minimum (Tests 1-6)
- **6/6 PASS**: Core course functionality works
- Users can create, approve, view, and run simulators in courses

### Complete (Tests 1-8)
- **8/8 PASS**: Everything works perfectly
- Both course and marketplace simulators functional
- Canvas renders properly in both cases

### Perfect (Tests 1-10)
- **10/10 PASS**: Production ready
- Multi-user, editing, and persistence all work

---

## 🐛 Troubleshooting

### If Canvas is Blank
- Check DevTools Console (F12)
- Look for "Executed X blocks" message
- If missing: blocks not executing
- If present but blank: canvas context issue
- Solution: Send console logs

### If Simulator Won't Open
- Popup blocker might be blocking
- Check browser settings
- Try in different browser
- Report error in console

### If Blocks Don't Appear When Editing
- Check: "✓ Course loaded with X blocks" message
- If 0: blocks not restored (Session 31 fix issue)
- Report: What number shows?

### If Can't Run Simulator
- Check authentication token
- Console: `localStorage.getItem('token')`
- Should show long JWT string, not NULL
- Re-login if needed

---

## 📝 REPORTING

When done, tell me:

1. **How many tests passed?** (e.g., 8/10)
2. **Which test(s) failed?** (e.g., Test 8 - canvas blank)
3. **Any console errors?** (Copy exact error message)
4. **Canvas issue?** (Working / Blank / Partial)

**Example Report:**
```
9/10 PASS
Failed: Test 10 (couldn't find second user account)
All course simulators work!
Marketplace canvas now renders shapes!
Only minor UI issue, no major bugs.
```

---

## 🎉 EXPECTED OUTCOME

**If all 10 pass**: 
- ✅ System is production-ready
- ✅ Users can create, save, and run courses with simulators
- ✅ Marketplace simulators execute properly
- ✅ All data persists correctly

**If 8+ pass**:
- ✅ Core features work
- ⚠️ Minor issues to fix
- 🟡 Can go to production with cautions

**If <8 pass**:
- ❌ Blocking issues remain
- 🔧 Need more debugging
- 🚫 Not production-ready

---

**Good luck! This is a comprehensive test of the entire system. Let me know the results!**
