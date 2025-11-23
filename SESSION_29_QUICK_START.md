# SESSION 29 - QUICK START GUIDE

**Status**: ✅ ALL FIXES IMPLEMENTED - START HERE

---

## 🚀 IMMEDIATE ACTION (60 seconds)

### Step 1: Start Backend (Terminal 1)
```bash
cd "c:\Users\kalps\Documents\Veelearn\veelearn-backend"
npm start
```

**Wait for**:
```
✓ Blocks column verified/added to courses table
Server running on port 3000
```

### Step 2: Start Frontend (Terminal 2)
```bash
cd "c:\Users\kalps\Documents\Veelearn\veelearn-frontend"
python -m http.server 5000
```

**Wait for**:
```
Serving HTTP on port 5000
```

### Step 3: Open Browser
```
http://localhost:5000
```

Login with: `viratsuper6@gmail.com` / `Virat@123`

---

## 📋 5-MINUTE QUICK TEST

### Test 1: Block Simulator Works
1. Dashboard → Create New Course
2. Click "Block-Based Simulator"
3. Drag "Add" block to canvas
4. **Expected**: Block appears with green outline

### Test 2: Save and Edit Blocks
1. Click "Save Draft"
2. Go to "My Courses" → Edit course
3. Click "Edit" on block simulator
4. **Expected**: New window opens, block visible on canvas
5. Close window
6. **Expected**: No "not saved" warning

### Test 3: Publish Works
1. In block simulator, click "📤 Publish"
2. Enter name and description
3. **Expected**: "Simulator published successfully!"

---

## 🔍 WHAT TO CHECK IN CONSOLE

Open DevTools: **F12**
Go to: **Console** tab

### When editing blocks:
Look for: `✓ Blocks message sent`
✅ = Success | ❌ = Problem

### When saving blocks:
Look for: `✓ Simulator data saved:`
✅ = Success | ❌ = Problem

### When publishing:
Look for: `✓ Simulator published successfully!`
✅ = Success | ❌ = Problem

---

## 🐛 QUICK TROUBLESHOOTING

**Problem**: Blocks don't appear when editing
**Fix**: F5 to hard refresh, then try again

**Problem**: "Not authenticated" error
**Fix**: Logout → Login again

**Problem**: Block simulator window won't open
**Fix**: Check if popup blocker is enabled

**Problem**: See "blockTemplates not ready" repeatedly
**Fix**: Reload page, check network tab

---

## 📚 FULL DOCUMENTATION

See these files for complete details:

1. **SESSION_29_TEST_AND_VERIFY.md** - Full 6-test plan
2. **SESSION_29_VERIFICATION_AND_FIXES.md** - Technical details
3. **SESSION_29_SUMMARY.md** - Overview of all changes

---

## ✅ SUCCESS INDICATORS

You'll know it's working when you see:

```
[in console]
✓ Window loaded, sending setup message
✓ Setup message sent
✓ Blocks message sent
Simulator loaded with 5/5 blocks
✓ Simulator data saved:
✓ Simulator published successfully!
```

---

## 🎯 NEXT STEPS

1. ✅ Start both servers
2. ✅ Run quick 5-minute test
3. ✅ Check console for success messages
4. ✅ If all good, run full test suite
5. ✅ Document any remaining issues

---

**Time to complete**: 5-10 minutes for quick test
**Time for full test**: 30-40 minutes
**Priority**: 🔴 CRITICAL - Core functionality
