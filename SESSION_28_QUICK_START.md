# SESSION 28 - QUICK START TESTING GUIDE

## 🚀 START HERE

All 4 critical bugs have been fixed. Follow this guide to test everything.

---

## STEP 1: Start MySQL Database

```bash
# Windows - Start MySQL Service
net start MySQL80

# Verify it's running
mysql -u root -p -e "SELECT 1"
# Enter password when prompted
```

---

## STEP 2: Start Backend Server

```bash
# Terminal 1
cd veelearn-backend
npm start

# You MUST see:
# ✓ Connected to MySQL database
# ✓ Server running on port 3000
```

---

## STEP 3: Start Frontend Server

```bash
# Terminal 2
cd veelearn-frontend
npx http-server . -p 5000
# OR
python -m http.server 5000

# You should see: Starting up http-server, serving .
```

---

## STEP 4: Open Browser and Login

1. Go to `http://localhost:5000`
2. Login with:
   - Email: `viratsuper6@gmail.com`
   - Password: `Virat@123`

---

## STEP 5: Run All 6 Tests

### ✅ TEST 1: Save Course with Blocks

1. Click "Dashboard"
2. Click "Create New Course"
3. Enter title: "Test Course 1"
4. Click "Block-Based Simulator"
5. In the simulator, drag some blocks onto the canvas
6. Click the X button to exit simulator
7. Click "Save Draft" button
8. **Expected Result**: 
   - Should see: "Course saved as draft"
   - Course appears in "My Courses" list with "Pending" status
   - **PASS if blocks are preserved** (you can edit and see them again)

---

### ✅ TEST 2: Submit Course for Approval

1. Click "Dashboard"
2. Create a new course with blocks (same as TEST 1)
3. Click "Submit for Approval" button
4. **Expected Result**:
   - Should see: "Course submitted for approval"
   - Admin can now see course in "Pending Courses" list
   - **PASS if course appears in pending list**

---

### ✅ TEST 3: Admin Preview Pending Course

1. Logout and login as ADMIN:
   - Email: `admin@example.com` (create if doesn't exist)
   - Or use superadmin: `superadmin@example.com`
2. Go to "Admin Dashboard" or "Pending Courses"
3. Find the course from TEST 2
4. Click "Preview" button (should now exist)
5. **Expected Result**:
   - Shows full course content
   - Shows all blocks that were added
   - Can see blocks JSON in developer console
   - **PASS if course content displays correctly**

---

### ✅ TEST 4: Publish Simulator to Marketplace

1. Login as regular user (not admin)
2. Go to "Dashboard"
3. Click "Go to Block Simulator" or open simulator directly
4. Create several blocks (Add, Multiply, Circle, etc.)
5. Connect them together
6. Click "📤 Publish" button
7. Enter simulator name: "Test Simulator 1"
8. Click OK
9. **Expected Result**:
   - Should see: "Simulator published successfully!"
   - Check browser console (F12) should show: "Simulator published! ID: [number]"
   - Simulator appears in "My Simulators" list
   - **PASS if simulator saves and appears in list**

---

### ✅ TEST 5: Add Marketplace Simulator to Course

1. Still logged in as regular user
2. Go to "Dashboard"
3. Click "Create New Course"
4. Enter title: "Test Course with Marketplace Sim"
5. Click "Add Marketplace Simulator" button
6. Search for "Test Simulator 1" (from TEST 4)
7. Click to select it
8. Click "Save Course"
9. **Expected Result**:
   - Should see: "Course saved successfully"
   - Course appears in "My Courses" list
   - Can click to view course and see the marketplace simulator included
   - **PASS if simulator is linked to course**

---

### ✅ TEST 6: View Simulator in Course

1. Go to "Dashboard" → "My Courses"
2. Click on "Test Course with Marketplace Sim" (from TEST 5)
3. Should see the marketplace simulator embedded in course
4. Click to open/run the simulator
5. **Expected Result**:
   - Simulator loads with all blocks
   - Blocks display correctly
   - Can run/execute the blocks
   - **PASS if simulator displays and executes**

---

## 📊 RESULTS TABLE

| Test # | Title | Expected | Result | Status |
|--------|-------|----------|--------|--------|
| 1 | Save Course with Blocks | Blocks persist | ✅/❌ | ____ |
| 2 | Submit for Approval | Course in pending list | ✅/❌ | ____ |
| 3 | Admin Preview | Shows full content | ✅/❌ | ____ |
| 4 | Publish Simulator | Appears in marketplace | ✅/❌ | ____ |
| 5 | Add Sim to Course | Simulator linked | ✅/❌ | ____ |
| 6 | View Sim in Course | Simulator loads & runs | ✅/❌ | ____ |

---

## 🐛 IF TESTS FAIL

### Open DevTools (F12) and Check:

1. **Console Tab** - Look for red errors
2. **Network Tab** - Check API calls (POST /api/courses, POST /api/simulators)
3. **Storage Tab** - Check if token is in localStorage

### Common Issues:

**Issue**: "Course saved but nothing happens"
- Check: Browser console for errors
- Check: Backend console for SQL errors
- Try: Reload page and check "My Courses" list

**Issue**: "Cannot publish simulator - not authenticated"
- Check: localStorage token exists (F12 → Storage → Local Storage → token)
- Try: Logout and login again
- Check: Token has correct format (long string starting with "eyJ")

**Issue**: "Course doesn't save"
- Check: Backend running on port 3000
- Check: MySQL database running
- Try: Restart backend with: `npm start`

**Issue**: "Blocks not saving"
- Check: Backend database has `blocks` column
- Try: Stop backend, restart, then test
- Check: Backend console shows "Blocks count: X"

---

## ✅ SUCCESS CRITERIA

All tests pass when:
- ✅ Courses save with blocks
- ✅ Courses submit for admin approval  
- ✅ Admins can preview pending courses
- ✅ Simulators publish to marketplace
- ✅ Marketplace simulators link to courses
- ✅ Simulators run in course view

---

## NEXT STEPS

After testing:
1. **If all pass**: Deployment ready! 🎉
2. **If some fail**: Report specific failures with console errors
3. **If backend crashes**: Check backend console for SQL errors

---

**Questions?** Check SESSION_28_CRITICAL_FIXES.md for detailed technical info.
