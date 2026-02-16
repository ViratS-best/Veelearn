# Session 38 - Automatic Progress Tracking Test Guide

## Quick Start Testing

### Prerequisites
- Backend running: `npm start` in veelearn-backend/
- Frontend served on port 5000
- Student user enrolled in a class
- Course with quiz questions assigned to that class

### Test Steps

#### Test 1: Auto-Calculate Progress
1. Login as student user
2. Go to "Assignments for Me" section
3. See assignment listed
4. Click "▶ Work on Assignment" button
5. **Expected**: Course opens and shows quiz questions
6. Answer some quiz questions (select radio button answers)
7. Click "Work on Assignment" button again (or close and reopen)
8. **Expected**: A dialog appears showing:
   - "📊 Progress Detected:"
   - "X out of Y questions answered correctly"
   - "Completion: Z%"
   - Buttons: [OK] [Cancel]
9. Click OK
10. **Expected**: Alert shows "✅ Work submitted!" with progress details

#### Test 2: Enrolled Courses Display
1. After submitting assignment (Test 1)
2. Dashboard should auto-refresh
3. Look for "📈 Enrolled Courses (with Progress)" section
4. **Expected**: See course card with:
   - Course title
   - Teacher: email
   - "📊 Progress: X/Y questions answered (Z%)"
   - Progress bar showing Z% filled
   - Status indicator (⏳ Not Started / ▶️ In Progress / ✅ Completed)
   - "👁️ View" button

#### Test 3: Progress Bar Visual Feedback
1. In Enrolled Courses section
2. Look at progress bars
3. **Expected**:
   - Bar background is dark (#111)
   - Bar fill is gradient (purple → pink)
   - Percentage displayed in center
   - If Z=0%, bar should be empty, status "⏳ Not Started" (gray)
   - If 0% < Z < 100%, bar partially filled, status "▶️ In Progress" (blue)
   - If Z=100%, bar full, status "✅ Completed" (green)
4. Hover over bar or wait a moment
5. **Expected**: Bar should have smooth animation (0.3s transition)

#### Test 4: View Enrolled Course
1. In Enrolled Courses section
2. Click "👁️ View" button on any course
3. **Expected**: Course viewer opens showing all content
4. Quiz questions should be visible and interactive
5. Previous answers should be remembered (if session persists)

#### Test 5: Multiple Enrolled Courses
1. Login as student enrolled in multiple classes
2. Go to dashboard
3. Scroll to "📈 Enrolled Courses (with Progress)"
4. **Expected**: See all courses listed
5. Each course should show:
   - Own progress bar with correct percentage
   - Own teacher name
   - Own assignment count
6. Verify each progress bar is unique and correct

#### Test 6: No Enrolled Courses
1. Login as student NOT enrolled in any class
2. Go to dashboard
3. Scroll down
4. **Expected**: "📈 Enrolled Courses (with Progress)" section should NOT be visible
5. No broken divs or empty sections shown

#### Test 7: API Response Check (DevTools)
1. Login as student
2. Open DevTools (F12) → Network tab
3. Go to dashboard or click "Work on Assignment"
4. Look for request: `GET /api/student/enrolled-courses`
5. Click on it → Preview tab
6. **Expected**: JSON response with structure:
   ```json
   {
     "success": true,
     "message": "Enrolled courses retrieved",
     "data": [
       {
         "course_id": 3,
         "title": "Physics 101",
         "teacher_email": "teacher@example.com",
         "total_assignments": 5,
         "completed_assignments": 3,
         "assignments": [...],
         "submissions": [...]
       }
     ]
   }
   ```

#### Test 8: Progress Accuracy
1. Create a course with 5 quiz questions
2. Assign to class
3. Student answers:
   - Question 1: Correct
   - Question 2: Correct
   - Question 3: Wrong (selected different answer)
   - Question 4: Correct
   - Question 5: Not answered
4. Click "Work on Assignment"
5. **Expected**: Dialog shows "3 out of 4 answered" or "3 out of 5 total"
   - If counting "answered": 3/4 = 75%
   - If counting "total": 3/5 = 60%
   - Verify logic matches implementation

#### Test 9: Resubmission Updates Progress
1. Login as student with previous submission
2. Go to "Work on Assignment"
3. Add more correct answers
4. Click submit again
5. **Expected**: Progress bar in Enrolled Courses section updates
6. Percentage increases based on newly answered questions
7. Status might change from "⏳" to "▶️" or "▶️" to "✅"

#### Test 10: UI Responsiveness
1. Enrolled Courses section should be responsive
2. On mobile (resize browser to mobile width):
   - Course cards should stack vertically
   - Progress bars should fit in viewport
   - "View" buttons should be clickable
   - Text should not wrap awkwardly
3. On desktop:
   - Course cards should have proper padding
   - Progress bars should be wide enough to read percentage
   - Layout should match screenshot

### Debugging Checklist

#### If Progress Shows 0% or Wrong Value
1. Check DevTools Console for errors
2. Verify quiz questions have `data-question-id` attribute
3. Verify question elements have radio buttons with `value` attribute
4. Check that `courseQuestions` array is populated
5. Verify `question.correct_answer` field exists
6. Log values in browser console:
   ```javascript
   console.log('courseQuestions:', courseQuestions);
   courseQuestions.forEach(q => {
     console.log(`Q${q.id}: correct_answer = ${q.correct_answer}`);
   });
   ```

#### If Enrolled Courses Section Not Showing
1. Check Network tab → look for `/api/student/enrolled-courses`
2. If 404: Backend endpoint not running or path wrong
3. If 401: Authentication token missing or invalid
4. If 200: Check response data
5. If error: Backend may have crashed, restart with `npm start`

#### If Progress Bar Doesn't Animate
1. Browser may not support CSS transitions
2. Try different browser
3. Check browser DevTools → Elements → Computed styles
4. Verify `transition: width 0.3s ease;` is applied
5. Check for CSS conflicting rules

#### If API Shows No Results
1. Verify student is enrolled in at least one class
2. Verify class has assignments created
3. Check database:
   ```sql
   SELECT * FROM student_enrollments WHERE student_id = [ID];
   SELECT * FROM classroom_assignments WHERE class_code = [CODE];
   ```
4. Verify course data exists in courses table

### Expected Console Logs

When features work correctly, you should see:
```javascript
// When trackQuizAnswers is called
"Progress calculated: 3/5 correct = 60%"

// When loadEnrolledCourses is called
"Loaded enrolled courses..."

// When quiz submitted
"Assignment submission recorded"
```

### Performance Notes

- Progress calculation should be < 100ms
- API request should complete < 500ms
- UI should be responsive throughout
- No lag when scrolling through enrolled courses

### Success Criteria

✅ Progress auto-calculates from quiz answers
✅ Enrolled courses display with correct progress
✅ Progress bars show visual feedback
✅ Status indicators show correct colors
✅ Multiple courses handle correctly
✅ Empty state handled (no courses = section hidden)
✅ No manual percentage input prompt
✅ Smooth animations and transitions
✅ API sends correct data structure
✅ All tests pass without errors
