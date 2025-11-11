# Session 10 - Run and Test Instructions

## Step 1: Start Backend (Terminal 1)

```bash
cd "c:\Users\kalps\Documents\Veelearn\veelearn-backend"
npm start
```

**Expected Output**:
```
Connected to MySQL database
Server running on port 3000
```

**Wait until you see**: Server running on port 3000

---

## Step 2: Start Frontend (Terminal 2)

```bash
cd "c:\Users\kalps\Documents\Veelearn\veelearn-frontend"
python -m http.server 5000
```

**Expected Output**:
```
Serving HTTP on 0.0.0.0 port 5000
```

**Alternative** (if Python not available):
```bash
npx http-server . -p 5000
```

---

## Step 3: Open Browser

Open: **http://localhost:5000**

---

## Step 4: Test Flow

### Test A: Login & Dashboard
1. Click "Login"
2. Email: `viratsuper6@gmail.com`
3. Password: `Virat@123`
4. Click "Login"
5. Should see dashboard with course management

**Check Console** (F12 → Console tab):
- No red errors
- Should show dashboard loaded

---

### Test B: Course Visibility (CRITICAL)
1. Login as admin user (if available) or use test account
2. Go to "Pending Courses" section (if admin)
3. Create a new course OR find an existing pending course
4. If admin, approve a course
5. Logout and login as different user
6. Check "Available Courses" - should see approved course
7. **Check Console** for debug logs:
   ```
   === LOAD AVAILABLE COURSES DEBUG ===
   Current user ID: [should show]
   All courses from API: [should show array]
   Filtered approved courses (others): [should show filtered]
   ```

**If nothing appears in console**: Backend might not be running

**If courses don't appear**: Check filtering logic at line 568 in script.js

---

### Test C: Block Simulator Drag & Drop (CRITICAL)
1. In course editor, click "Add Block Simulator"
2. Window opens to block-simulator.html
3. **Open DevTools** (F12)
4. Go to **Elements** tab
5. Drag a block from left sidebar to canvas area
6. **Check Console** for events:
   - Should see block styling changes
   - Should see "dragstart" events
   - Should see "dragover" events
   - Should see "drop" event
7. Block should appear on canvas
8. **If block doesn't appear**: Check drag/drop handlers at lines 631-696

**Debug**: If drag events not firing:
- Open DevTools Console
- Type: `document.querySelectorAll('.block').length`
- Should return number of block elements

---

### Test D: View Course Before Approval (CRITICAL)
1. Login as teacher who created a course
2. Go to "My Courses"
3. Should see courses with "Pending" status badge
4. Pending courses should be editable/viewable
5. **Check Console**:
   ```
   === LOAD USER COURSES DEBUG ===
   Current user ID: [should match your ID]
   All courses from API: [should include pending courses]
   Filtered user courses: [should include your pending courses]
   ```

**If pending courses don't appear**: Check filter at line 553 in script.js

---

### Test E: Simulator Publishing (CRITICAL)
1. In block simulator, create 1-2 sample blocks
2. Click "Publish" button (green, top right)
3. Enter simulator title and description
4. Should show "Simulator published!" message
5. Should redirect to index.html
6. **Check Console** for:
   - POST request to /api/simulators
   - Success response with simulator ID

**If publish fails**: Check:
- authToken is set (localStorage)
- Backend is running
- /api/simulators endpoint exists

---

### Test F: Block Simulator UI (CRITICAL)
1. In block simulator
2. Should see:
   - Block palette on left ✓
   - Canvas in middle ✓
   - Preview panel on right ✓
   - Toolbar at top with: Run, Stop, Clear, Save, Publish, Exit ✓
3. Click "Exit" button (red X, top right)
4. Should return to course editor
5. **Check**: No console errors

---

## Expected Results

| Test | Expected | Actual | Pass |
|------|----------|--------|------|
| A: Login | Dashboard appears | | |
| B: Course Visibility | Approved courses appear to other users | | |
| C: Block Drag & Drop | Blocks draggable to canvas | | |
| D: View Course | Pending courses visible to creator | | |
| E: Publish Simulator | Simulator published successfully | | |
| F: Block Simulator UI | All UI elements present | | |

---

## Debug Checklist

- [ ] Backend running on port 3000
- [ ] Frontend running on port 5000
- [ ] DevTools Console open for logs
- [ ] No 404 errors for JS files
- [ ] No CORS errors
- [ ] Auth token in localStorage
- [ ] Database has test data

---

## If Something Breaks

1. **Backend won't start**: Check MySQL is running
2. **Frontend shows blank**: Check console for JS errors
3. **Courses don't load**: Check network tab for 500 errors
4. **Can't login**: Check credentials or database
5. **Drag doesn't work**: Check dragstart/drop handlers exist

---

## Quick Fixes to Try

### Fix #1: Clear localStorage
```javascript
// In DevTools Console:
localStorage.clear();
location.reload();
```

### Fix #2: Check authToken
```javascript
// In DevTools Console:
console.log(localStorage.getItem('authToken'));
// Should show JWT token, not null
```

### Fix #3: Check Backend Response
```javascript
// In DevTools Console:
fetch('http://localhost:3000/api/courses', {
  headers: { 'Authorization': `Bearer ${localStorage.getItem('authToken')}` }
}).then(r => r.json()).then(d => console.log(d));
// Should show courses array
```

### Fix #4: Test Drag Events
```javascript
// In DevTools Console, on block-simulator.html:
document.querySelectorAll('.block-palette .block').forEach(b => {
  b.addEventListener('dragstart', () => console.log('Drag started!'));
});
// Then drag a block - should log to console
```

---

## Files Modified in Session 10

1. `/script.js` - Added console.log to course loading functions
2. `/AGENTS.md` - Updated with Session 10 status and analysis
3. `/CRITICAL_FIXES_SESSION_10.md` - Created this document

---

**Last Updated**: Session 10 - November 9, 2025
**Status**: Ready for testing
**Next**: Start backend and frontend, run through test flow
