# 🚀 RUN TESTS NOW - SESSION 28

## STEP 1: Start MySQL (Pick One Method)

### Method 1: Windows Service
```batch
net start MySQL80
```

### Method 2: Command Line
```batch
mysqld
```

**Verify it works**:
```batch
mysql -u root -p -e "SELECT 1"
# Type password when prompted
```

---

## STEP 2: Start Backend Server

**Open PowerShell/CMD Terminal #1**:
```batch
cd c:\Users\kalps\Documents\Veelearn\veelearn-backend
npm start
```

**WAIT until you see**:
```
✓ Connected to MySQL database
✓ Server running on port 3000
✓ Listening for requests...
```

---

## STEP 3: Start Frontend Server

**Open PowerShell/CMD Terminal #2**:
```batch
cd c:\Users\kalps\Documents\Veelearn\veelearn-frontend
npx http-server . -p 5000
```

**WAIT until you see**:
```
Starting up http-server, serving .
http://127.0.0.1:5000
```

---

## STEP 4: Open Browser

1. Open any browser (Chrome, Firefox, Edge, etc.)
2. Go to: `http://localhost:5000`

---

## STEP 5: Login

**Email**: `viratsuper6@gmail.com`  
**Password**: `Virat@123`

Click "Login"

---

## STEP 6: Run Test #1

### 📝 TEST 1: Save Course with Blocks

**Steps**:
1. Click "Dashboard" button
2. Click "Create New Course"
3. Enter title: `Test Course 1`
4. Click "Select Block-Based Simulator"
5. Browser opens simulator
6. In simulator: Drag some blocks (Add, Multiply, Circle) onto canvas
7. Click "✕ Exit" button (top right)
8. Click "Save Draft" button
9. See message: "Course saved as draft! You can continue editing later."

**Expected**: ✅ Course appears in "My Courses" list

**Result**: 
- [ ] PASS
- [ ] FAIL - Note error below

Error (if any): _______________________________________________

---

## STEP 7: Run Test #2

### 📝 TEST 2: Submit for Approval

**Steps**:
1. Click "Dashboard"
2. Click "Create New Course"
3. Enter title: `Test Course 2`
4. Click "Select Block-Based Simulator"
5. Add some blocks (Add, Multiply, Circle)
6. Click "✕ Exit"
7. Click "Submit for Approval" button
8. See message: "Course submitted for approval!"

**Expected**: ✅ Admin can see course in pending list

**Result**: 
- [ ] PASS
- [ ] FAIL - Note error below

Error (if any): _______________________________________________

---

## STEP 8: Run Test #3

### 📝 TEST 3: Admin Preview

**Steps**:
1. LOGOUT (click Logout button)
2. LOGIN AS ADMIN:
   - Email: `admin@example.com`
   - Password: `Admin@123`
   - (If doesn't exist, create account first)
3. Click "Admin Dashboard"
4. Click "Pending Courses"
5. Find "Test Course 2" from previous test
6. Click "Preview" button (should exist)
7. See course content with blocks displayed

**Expected**: ✅ Admin can see all blocks in course

**Result**: 
- [ ] PASS
- [ ] FAIL - Note error below

Error (if any): _______________________________________________

---

## STEP 9: Run Test #4

### 📝 TEST 4: Publish Simulator

**Steps**:
1. LOGOUT
2. LOGIN as user: `viratsuper6@gmail.com` / `Virat@123`
3. Go to Dashboard
4. Click "Open Block Simulator"
5. Drag blocks (Add, Multiply, Circle, Line) onto canvas
6. Connect them (optional)
7. Click "📤 Publish" button
8. Enter name: `Test Simulator 1`
9. Click OK
10. See message: "Simulator published successfully!"

**Expected**: ✅ Simulator appears in marketplace

**Result**: 
- [ ] PASS
- [ ] FAIL - Note error below

Error (if any): _______________________________________________

---

## STEP 10: Run Test #5

### 📝 TEST 5: Add Marketplace Sim to Course

**Steps**:
1. Dashboard → Create New Course
2. Title: `Test Course with Simulator`
3. Click "Add Marketplace Simulator" (if available)
4. Search: "Test Simulator 1"
5. Click to select
6. Click "Save Course"
7. See message: "Course saved as draft!"

**Expected**: ✅ Simulator linked to course

**Result**: 
- [ ] PASS
- [ ] FAIL - Note error below

Error (if any): _______________________________________________

---

## STEP 11: Run Test #6

### 📝 TEST 6: View Simulator in Course

**Steps**:
1. Dashboard → My Courses
2. Click "Test Course with Simulator"
3. See simulator embedded in course
4. Click simulator to open
5. See all blocks from Test Simulator 1

**Expected**: ✅ Simulator loads with all blocks

**Result**: 
- [ ] PASS
- [ ] FAIL - Note error below

Error (if any): _______________________________________________

---

## FINAL RESULTS TABLE

Fill this in:

| Test # | Description | Pass/Fail |
|--------|-------------|-----------|
| 1 | Save Course with Blocks | _____ |
| 2 | Submit for Approval | _____ |
| 3 | Admin Preview | _____ |
| 4 | Publish Simulator | _____ |
| 5 | Add Sim to Course | _____ |
| 6 | View Sim in Course | _____ |

**Total Passing**: _____ / 6

---

## 🐛 DEBUGGING HELP

### If Test Fails, Check These:

**1. Open DevTools (F12)**
- Go to "Console" tab
- Look for RED error messages
- Copy any errors and report them

**2. Check Backend**
- Look at Terminal #1 where backend is running
- Look for RED error messages
- Copy any SQL errors and report them

**3. Check Database**
- Terminal #1 should show "Connected to MySQL database"
- If not: MySQL not running - restart it

**4. Token Issue**
- Open DevTools → Storage tab → Local Storage
- Look for "token" key
- Should have long string value

---

## 📞 REPORT YOUR RESULTS

When done, provide:

1. **Which tests passed**: _______________
2. **Which tests failed**: _______________
3. **Error messages from console**: _______________
4. **Time taken**: _____ minutes

---

## ✅ SUCCESS = ALL 6 PASS

When all 6 tests pass:
1. System is production ready ✅
2. All critical bugs fixed ✅
3. Ready to deploy ✅

---

## 🎯 DO THIS NOW

```
1. Start MySQL → 2. Start Backend → 3. Start Frontend 
4. Login → 5-11. Run all 6 tests → Report results
```

**Estimated time: 30-45 minutes**

**Go!** 🚀
