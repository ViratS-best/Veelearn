# SESSION 31 - QUICK START GUIDE 🚀

## 3-Minute Setup

**Step 1**: Start Backend (Terminal 1)
```bash
cd c:\Users\kalps\Documents\Veelearn\veelearn-backend
npm start
```

Wait for: `Server running on port 3000` + `Connected to MySQL database`

**Step 2**: Start Frontend (Terminal 2)
```bash
cd c:\Users\kalps\Documents\Veelearn\veelearn-frontend
python -m http.server 5000
```

Wait for: `Serving HTTP on port 5000`

**Step 3**: Open Browser
```
http://localhost:5000
```

---

## Quick Test (5 minutes)

### Test 1: Login
- Email: `viratsuper6@gmail.com`
- Password: `Virat@123`
- Expected: Dashboard appears

### Test 2: Create Course with Block Simulator
1. Click "Dashboard"
2. Click "Create New Course"
3. Enter title: "Test Course"
4. Click "🧩 Block Visual Simulator" button
5. Add a block (e.g., "Add" block)
6. Close simulator (X button)
7. Click "✅ Submit for Approval"
8. Expected: "Course submitted for approval!" message

### Test 3: View Course (as Admin)
1. Login as superadmin if needed
2. Go to "Admin Panel" → "Pending Courses"
3. Click "✓ Approve" on test course
4. Expected: Course moves to approved list

### Test 4: Edit Course
1. Go to "My Courses"
2. Click "Edit" on your test course
3. Expected: **All simulators you added should appear**
4. Can add more simulators or modify
5. Click "✅ Submit for Approval" again
6. Expected: All changes saved

### Test 5: View as Enrolled Student
1. Go to "Available Courses"
2. Click "Enroll" on approved course
3. Click "Preview"
4. Expected: **All simulators visible with their content**

---

## ✅ Success Criteria

If all this works, then Session 31 is complete:

- ✅ Courses save with blocks
- ✅ Blocks persist when editing
- ✅ Blocks visible after approval
- ✅ Blocks visible when viewing course
- ✅ Can edit course multiple times and keep blocks

---

## 🐛 If Something Fails

### If Backend Crashes
```
Check console for MySQL connection error
Verify MySQL is running:
  tasklist | findstr mysqld
Start MySQL if needed:
  net start MySQL80
```

### If Blocks Don't Appear When Editing
```
Open DevTools (F12) → Console
Look for errors like:
  "Cannot read property 'blocks' of undefined"
  "Failed to parse blocks JSON"
Report exact error message
```

### If Course Won't Save
```
In DevTools Console, check:
  - Is authToken present? 
    localStorage.getItem('token')
  - Does it show a token string or NULL?
  - Any network errors in Network tab?
Report findings
```

---

## 📋 Files That Changed

1. **veelearn-frontend/script.js** - editCourse() now restores blocks
2. **veelearn-backend/server.js** - GET /api/courses now returns blocks

No other files changed - everything else stays the same.

---

## 💡 What's Different

**Before Session 31**:
- User creates course with simulator
- Saves course ✓
- Edits course
- Simulator is gone ✗

**After Session 31**:
- User creates course with simulator
- Saves course ✓
- Edits course
- Simulator appears again ✓
- Can add more simulators
- All saved ✓

---

**Ready to test? Start at Step 1 above!**
