# SESSION 29 - TEST PLAN FOR CRITICAL FIXES

**Status**: ✅ ALL 4 CRITICAL FIXES IMPLEMENTED

---

## FIXES APPLIED IN SESSION 29

### Fix #1: ✅ Added Validation to Save-Simulator Handler (DONE)
- **File**: script.js (lines 1084-1110)
- **What**: Added error checking before saving blocks back to parent
- **Benefit**: Prevents crashes if save is called in invalid context

### Fix #2: ✅ Added blockTemplates Validation in loadSimulator (DONE)
- **File**: block-simulator.html (lines 840-867)
- **What**: Check if blockTemplates are loaded before rendering
- **Benefit**: Prevents race condition where message arrives before templates load

### Fix #3: ✅ Added Error Handling to postMessage Calls (DONE)
- **File**: script.js (lines 1053-1090)
- **What**: Try/catch wrapper around window.open and postMessage calls
- **Benefit**: Better debugging, logs each step of the process

### Fix #4: ✅ Improved Error Handling in publishSimulator (BONUS)
- **File**: block-simulator.html (lines 909-924)
- **What**: Better error messages and response validation
- **Benefit**: Users see exactly what went wrong if publish fails

---

## DETAILED TESTING CHECKLIST

### Test 1: Create Course with Block Simulator ✅
```
1. Go to Dashboard → Create New Course
2. Click "Block-Based Simulator"
3. Drag 5+ blocks to canvas (add, multiply, circle, rectangle)
4. Connect blocks together
5. Click "Save Draft" button
6. EXPECTED: Course saved, blocks preserved
VERIFY: 
  - Console shows no errors
  - Course appears in "My Courses" list
  - Course status shows "Pending"
```

### Test 2: Edit Saved Course and View Blocks ✅
```
1. Go to "My Courses" 
2. Click on the course you just created
3. Click "Edit" on the block simulator
4. EXPECTED: New window opens and blocks appear on canvas
VERIFY:
  - Console shows "✓ Window loaded, sending setup message"
  - Console shows "✓ Setup message sent"
  - Console shows "✓ Blocks message sent"
  - Console shows "Simulator loaded with 5/5 blocks" (or similar)
  - All 5 blocks visible on canvas
  - No errors in console
```

### Test 3: Add More Blocks and Exit Properly ✅
```
1. In the open block simulator, drag 2 more blocks to canvas
2. Click X "Exit" button
3. EXPECTED: No warning about "not saved"
4. Window closes automatically
5. VERIFY:
  - Console shows no "ERROR: Cannot save simulator" messages
  - Console shows "✓ Simulator data saved:" with counts
  - Returns to course edit view
  - Edit course again to verify new blocks were saved
```

### Test 4: Publish Simulator ✅
```
1. In block simulator, click "📤 Publish" button
2. Enter simulator name: "Test Simulator"
3. Enter description
4. Click OK
5. EXPECTED: "Simulator published successfully!"
6. VERIFY:
  - Console shows "=== PUBLISH SIMULATOR DEBUG ===" section
  - Console shows token value (not NULL)
  - Console shows "✓ Simulator published successfully! ID: XXX"
  - No "Not authenticated" error
  - Alert shows success message
```

### Test 5: View Simulator in Marketplace ✅
```
1. Go to Marketplace
2. Find your published simulator
3. Click on it to view
4. EXPECTED: Simulator detail page loads
5. Click "Run" button
6. VERIFY:
  - Console shows "Simulator loaded with X blocks"
  - Shows "Simulator loaded with X blocks" message
  - Can see block execution happens
```

### Test 6: Verify Error Handling Works ✅
```
1. Open DevTools (F12)
2. Go to Network tab
3. Try to publish a simulator
4. If network error occurs:
5. EXPECTED: Console shows detailed error message
6. VERIFY:
  - Error message is user-friendly (not just "Failed")
  - HTTP status and reason shown
  - logToConsole shows error (appears in UI console too)
```

---

## DEBUG OUTPUT TO VERIFY

**When opening block simulator for editing, you should see in console:**

```
✓ Window loaded, sending setup message
✓ Setup message sent
✓ Sending block simulator data: {
  blocksCount: 5,
  connectionsCount: 2
}
✓ Blocks message sent
blockTemplates not ready, queuing load  [OR] Simulator loaded with 5/5 blocks
```

**When exiting block simulator, you should see:**

```
Saving blocks before closing course simulator...
✓ Simulator data saved: {
  blockId: 1,
  blocksCount: 5,
  connectionsCount: 2
}
```

**When publishing simulator, you should see:**

```
=== PUBLISH SIMULATOR DEBUG ===
All localStorage keys: ['token', 'email', ...]
Token key exists: true
Token value: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
✓ Simulator published successfully! ID: 42
```

---

## WHAT IF YOU SEE ERRORS?

### Error: "blockTemplates not ready, queuing load" repeating forever
- **Problem**: block-templates-unified.js didn't load
- **Fix**: Check network tab, reload page
- **Check**: Is block-templates-unified.js being loaded?

### Error: "Cannot save simulator: invalid context"
- **Problem**: currentEditingSimulatorBlockId is null
- **Fix**: Make sure you clicked "Edit" button on a block simulator
- **Check**: Are you in course edit mode?

### Error: "No auth token available"
- **Problem**: authToken variable is empty
- **Fix**: Logout and login again
- **Check**: localStorage has 'token' key?

### Error: "Window load event never fires"
- **Problem**: block-simulator.html is blocked or failed to load
- **Fix**: Check if popup blocker is active
- **Check**: Open block-simulator.html directly to test

### Error: "Failed to publish simulator: HTTP 401"
- **Problem**: Token expired or invalid
- **Fix**: Logout and login again
- **Check**: Token looks like valid JWT?

---

## QUICK COMMAND REFERENCE

**Start backend** (Terminal 1):
```bash
cd c:\Users\kalps\Documents\Veelearn\veelearn-backend
npm start
```

**Start frontend** (Terminal 2):
```bash
cd c:\Users\kalps\Documents\Veelearn\veelearn-frontend
python -m http.server 5000
# OR on Windows without Python:
npx http-server . -p 5000
```

**Open app**:
```
http://localhost:5000
```

**Open DevTools**:
```
F12 (or Ctrl+Shift+I)
```

---

## SUCCESS CRITERIA

✅ All 6 test cases pass
✅ No errors in console during any operation
✅ Debug messages show correct progression
✅ Can create, edit, save, publish, and run simulators
✅ Blocks persist when editing courses
✅ No false "not saved" warnings
✅ Error messages are clear and helpful

---

## NEXT ACTIONS AFTER TESTING

If all tests pass:
1. Update AGENTS.md with SESSION 29 completion
2. Create summary document
3. Ready for production testing

If tests fail:
1. Document which test failed
2. Check console for specific error
3. Debug and apply targeted fix
4. Re-run that specific test

---

**Status**: READY FOR TESTING
**Time to Test**: ~30 minutes for all tests
**Priority**: 🔴 CRITICAL - These are core features
