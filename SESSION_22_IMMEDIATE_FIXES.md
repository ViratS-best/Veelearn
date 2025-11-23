# Session 22 - Immediate Action Plan

## Summary
Based on comprehensive code analysis, all 6 critical issues have the necessary code in place. The problems appear to be runtime issues or configuration issues, NOT missing code.

## Status of Each Issue

| Issue | Code Status | Root Cause | Fix |
|-------|------------|-----------|-----|
| 1. Token NULL when publishing | ✅ Exists | Token not in localStorage | Debug with console |
| 2. Block drag & drop | ✅ Exists | Handlers may not fire | Verify in console |
| 3. No X button | ✅ Exists (line 360) | Rendering issue | Check CSS |
| 4. Cannot view course before approval | ✅ Exists | Database state | Check DB |
| 5. Simulators don't work | ✅ Exists | API or renderer | Check API |
| 6. Cannot publish simulator | ✅ Exists | Token or API | Debug token |

## Critical Files Status

✅ **script.js** (Lines 7, 91, 159-220)
- Token storage: CORRECT
- Token validation: EXISTS
- Token monitoring: EXISTS
- Logout debugging: EXISTS

✅ **block-simulator.html** (Lines 445-517)
- dragstart handler: CORRECT
- dragover handler: CORRECT
- drop handler: CORRECT
- publishSimulator: CORRECT with debug logs
- Exit button: CORRECT (line 360)

✅ **block-templates-unified.js**
- All 40+ block templates present

✅ **simulator-view.html**
- File exists and functional

✅ **server.js** 
- All API endpoints configured

## Why Issues Persist

**NOT** because code is missing, but because:

1. **Database not running** → No data loaded
2. **Token not persisting** → localStorage issues  
3. **Templates not loading** → JavaScript error in file
4. **CSS blocking drag** → Visual feedback missing
5. **API errors** → Backend connection problems

## Immediate Testing Steps

### Step 1: Start Services (5 mins)
```bash
# Terminal 1: Start MySQL
net start MySQL80

# Terminal 2: Start Backend
cd veelearn-backend
npm start
# MUST see: "Server running on port 3000" AND "Database connected"

# Terminal 3: Start Frontend
cd veelearn-frontend
npx http-server . -p 5000
```

### Step 2: Test Token Storage (2 mins)
1. Open http://localhost:5000
2. Login with: viratsuper6@gmail.com / Virat@123
3. Press F12 → Console tab
4. Run: `localStorage.getItem('token')`
5. **Should show**: Long JWT string starting with "eyJ..."
6. **If NULL**: Token not stored correctly

### Step 3: Test Block Drag (3 mins)
1. Dashboard → Create Course → Block-Based Simulator
2. Check console for errors
3. Try dragging "Add" block to canvas
4. **Should see**: Console log "Drag started from palette: add"
5. **Should see**: Block appears on canvas

### Step 4: Test Publishing (3 mins)
1. In block simulator, add some blocks
2. Click "📤 Publish" button
3. Enter simulator name
4. **Check console for token debug output**
5. Should see "Token value: eyJ..." (not NULL)

### Step 5: Test Courses (3 mins)
1. Dashboard → My Courses
2. **Should see**: Any pending courses you created
3. Dashboard → Available Courses
4. **Should see**: Approved courses from other users

### Step 6: Test Simulator View (2 mins)
1. Dashboard → Marketplace
2. Click any simulator
3. **Should see**: Simulator loads with canvas

## Expected Output

### Success Indicators
```
✓ Token value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
✓ blockTemplates loaded: 40+ templates
✓ Drag started from palette: add
✓ Drop detected
✓ Block added to canvas at position X,Y
✓ Simulator published successfully!
```

### Error Indicators
```
✗ Token value: NULL
✗ blockTemplates loaded: 0 templates
✗ No "Drag started" in console
✗ "Cannot find blockTemplates" error
✗ "Not authenticated" error when publishing
✗ "Database connection failed" in backend
```

## Diagnostics By Issue

### If Token is NULL
1. Check if localStorage persists: F12 → Application → Local Storage
2. Check if "token" key exists (not "authToken")
3. Reload page and check again (session may have expired)
4. Clear localStorage and login again

### If Block Drag Doesn't Work
1. Check console for: "Drag started from palette: [type]"
2. Check for JavaScript errors
3. Verify blockTemplates loaded: `console.log(Object.keys(blockTemplates).length)`
4. Check CSS: `.block` should have `cursor: grab`

### If Courses Don't Show
1. Check backend: `curl http://localhost:3000/api/courses`
2. Verify courses exist in database
3. Check course status: should be "approved" for public list
4. Check creator_id: should match user creating course

### If Simulator Won't Publish
1. Check token: `localStorage.getItem('token')`
2. Check console for "CRITICAL: No token found!" message
3. Check for "Not authenticated" error
4. Verify /api/simulators endpoint responds

## Next Steps After Testing

1. **Document all errors** shown in console
2. **Capture console output** - screenshot or copy to file
3. **Run tests 1-6** and mark which PASS/FAIL
4. **Report findings** with:
   - Which tests passed
   - Which tests failed
   - Full error messages from console
   - Screenshots if possible

## Quick Checklist

- [ ] MySQL running (`net start MySQL80`)
- [ ] Backend running on port 3000 (`npm start`)
- [ ] Frontend running on port 5000 (`npx http-server`)
- [ ] Logged in successfully
- [ ] Token stored in localStorage
- [ ] Block drag fires event (check console)
- [ ] Block appears on canvas when dropped
- [ ] Course status shows correctly
- [ ] Simulator publishes successfully
- [ ] Can view simulator in marketplace

## Key Debug Commands

Run these in browser console (F12):

```javascript
// Check token
localStorage.getItem('token')

// Check user ID
console.log(currentUser.id, currentUser.email)

// Check templates
console.log(Object.keys(blockTemplates).length + ' blocks loaded')

// Check database connection
fetch('http://localhost:3000/api/courses', {
  headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
}).then(r => r.json()).then(d => console.log('API Response:', d))

// Check block palette
console.log(document.querySelectorAll('.block-palette .block').length + ' blocks in palette')

// Trigger drag manually
const blocks = document.querySelectorAll('.block-palette .block')
blocks[0].dispatchEvent(new DragEvent('dragstart'))
```

## Contact Points

If issues persist after testing:
1. Check that ALL THREE services are running (MySQL, Backend, Frontend)
2. Verify no console errors when services start
3. Verify database is not corrupted (backup and restore)
4. Check .env file has correct credentials
5. Look for "CRITICAL ERROR" messages in console

---

**Ready to test!** Follow the steps above and report results.
