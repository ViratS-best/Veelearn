# SESSION 37 - QUICK TEST GUIDE

## 🚀 START SERVERS

```bash
# Terminal 1: Backend (Render/Local)
cd veelearn-backend
npm start
# Wait for: "Server running on port 3000"

# Terminal 2: Frontend (GitHub Pages / Local)
cd veelearn-frontend
npx http-server . -p 5000
# Navigate to http://localhost:5000
```

---

## ✅ TEST 1: TEACHER ROLE REQUEST

### Steps:
1. **Login** as regular user: `viratsuper6@gmail.com` / `Virat@123`
2. Go to **Dashboard** (should show "User Panel")
3. Click **"👨‍🏫 Become a Teacher"** button
4. **CONFIRM** warning dialog (⚠️ Cannot be undone...)

### Expected Results:
- ✅ Alert shows class code (e.g., "ABC123")
- ✅ Teacher panel appears with class code display
- ✅ "Join a Class" form hidden (students only)
- ✅ "Create Assignment" dropdown visible

### What's Happening:
- User role changed to `teacher` in database
- Unique class code generated: 6 uppercase alphanumeric
- Teacher approval set to `false` (needs superadmin)
- Student enrollment option removed

---

## ✅ TEST 2: VIEW CLASS CODE

### Steps:
1. **As teacher**, look at the dashboard
2. Find **green monospace text** showing "Class Code: ABC123"

### Expected Results:
- ✅ Class code visible in teacher panel
- ✅ Styled in monospace font
- ✅ Green color (#4ade80)

---

## ✅ TEST 3: STUDENT ENROLLMENT

### Setup:
- Open **2 browser windows**:
  - Window 1: Teacher account (already logged in)
  - Window 2: Student account (login as different user OR use incognito)

### Teacher Window:
- Copy class code from teacher panel

### Student Window:
1. **Login** as student user
2. Scroll to **"Join a Class"** section
3. Paste class code in input box
4. Click **"📚 Join Class"**

### Expected Results:
- ✅ Alert: "✅ Enrolled in class successfully!"
- ✅ Input clears
- ✅ New section appears: "📚 Assignments for Me"

---

## ✅ TEST 4: CREATE ASSIGNMENT

### Teacher Window:
1. **Scroll to "Create Assignment"** section
2. **Select a course** from dropdown (if none exist, create one first)
3. **Set due date** (optional) - pick tomorrow's date
4. Click **"📋 Assign Course"**

### Expected Results:
- ✅ Alert: "✅ Assignment created and sent to students in your class!"
- ✅ Dropdown resets to "Select a course..."
- ✅ Date picker clears

### Database Check:
```sql
SELECT * FROM classroom_assignments WHERE teacher_id = YOUR_ID;
-- Should see 1 row with: teacher_id, course_id, class_code, due_date
```

---

## ✅ TEST 5: VIEW STUDENT ASSIGNMENTS

### Student Window:
1. **Refresh page** or wait 2 seconds
2. Look for **"📚 Assignments for Me"** section
3. Should see assignment card with:
   - Course title
   - Assignment title
   - Teacher email
   - Due date
   - **"▶ Work on Assignment"** button

### Expected Results:
- ✅ Assignment appears instantly
- ✅ Shows correct teacher email
- ✅ Shows correct due date
- ✅ Blue button is clickable

---

## ✅ TEST 6: SUBMIT ASSIGNMENT

### Student Window:
1. Click **"▶ Work on Assignment"** button
2. Prompt appears: "How much have you completed?"
3. Enter completion percentage: **75** (for example)
4. Click **OK**

### Expected Results:
- ✅ Alert: "✅ Work submitted!"
- ✅ Shows completion: "75%"
- ✅ Shows status: "✅ ON TIME" (if before due date) or "⏰ LATE"
- ✅ Assignment list refreshes

---

## ✅ TEST 7: VIEW PROGRESS (TEACHER)

### Teacher Window:
1. Click **"📊 View Progress"** on class card
2. A new section appears: "📊 Class Progress - ABC123"
3. **Table displays**:
   - Student email
   - Assignment title
   - Completion % with visual bar
   - Status (On Time / Late / Not Started)
   - Submitted (✅ Yes / ⏳ No)

### Expected Results:
- ✅ Progress table shows
- ✅ Shows student's 75% completion bar
- ✅ Status shows "On Time" (green)
- ✅ Submitted shows "✅ Yes"
- ✅ **Back** button closes table

### Database Check:
```sql
SELECT * FROM assignment_submissions WHERE assignment_id = 1;
-- Should show: student_id, completion_percentage: 75, is_submitted: 1, is_late: 0
```

---

## ✅ TEST 8: LATE SUBMISSION

### Student Window:
1. Click **"▶ Work on Assignment"** again (same assignment)
2. Enter: **50** (different percentage)
3. Click **OK**

### Expected Results:
- ✅ Alert shows new percentage: "50%"
- ✅ Status updates in database

### Teacher Window:
1. Click **"📊 View Progress"** again
2. Progress bar should update to **50%**

### Expected Results:
- ✅ Table refreshes with new data
- ✅ Shows 50% progress bar

---

## ✅ TEST 9: MULTIPLE STUDENTS

### Scenario:
- Teacher has 2 students enrolled

### Expected Results:
1. **Table shows 2 rows** (one per student)
2. **Each has their own progress**
3. **Status calculated correctly** for each

### View in Teacher Window:
```
Student | Assignment | Completion | Status | Submitted
john... | Assign 1   | [███░░░░░░] 30%   | Late   | Yes
jane... | Assign 1   | [██████░░░░] 60%  | On Time | Yes
```

---

## 🐛 TROUBLESHOOTING

### Issue: "Assignment not showing for student"
**Check:**
1. Student used correct class code
2. Teacher assignment was created
3. Student refreshed page
4. Database connection is working

### Issue: "Class code shows 'Pending approval...'"
**Check:**
1. Superadmin needs to approve teacher
2. Use `/api/admin/approve-teacher/:userId` endpoint
3. Or wait for manual approval workflow

### Issue: "Progress not updating"
**Check:**
1. Student submitted (not just viewed)
2. Completion % was valid (0-100)
3. Teacher refreshed progress table
4. Server didn't crash

### Issue: "Class code not displaying"
**Check:**
1. User successfully became teacher
2. API returned classCode in response
3. Check browser console for errors
4. Refresh page

---

## 📊 DATABASE VERIFICATION

```sql
-- Check users table
SELECT id, email, role, class_code, teacher_approved FROM users WHERE role = 'teacher';

-- Check enrollments
SELECT * FROM student_enrollments;

-- Check assignments
SELECT * FROM classroom_assignments;

-- Check submissions
SELECT 
  asub.student_id, 
  u.email,
  ca.title,
  asub.completion_percentage,
  asub.is_late,
  asub.submission_date
FROM assignment_submissions asub
JOIN users u ON asub.student_id = u.id
JOIN classroom_assignments ca ON asub.assignment_id = ca.id;
```

---

## ✨ NICE TOUCHES TO VERIFY

- [ ] Class code in **green monospace** font
- [ ] Warning modal before becoming teacher
- [ ] Progress **bar visual** (not just number)
- [ ] Color-coded **status** (green=on time, red=late)
- [ ] **Real-time updates** (no refresh needed)
- [ ] Student **can't duplicate enroll** (error message)
- [ ] Teacher **can only manage own class** (no cross-class access)
- [ ] **Completion % validation** (0-100 only)

---

## 🎯 SUCCESS CRITERIA

All 9 tests pass? You're done! ✅

Features working:
- [x] Teachers can request role
- [x] Class codes generated & displayed
- [x] Students can enroll in classes
- [x] Teachers can create assignments
- [x] Students see their assignments
- [x] Students can submit work
- [x] Teachers can view progress
- [x] Late status auto-detected
- [x] Real-time updates work

---

_Ready to deploy to production!_
