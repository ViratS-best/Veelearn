# Session 22 - Quick Start Guide

## TL;DR - The Problem

All code exists but **6 critical features aren't working**. This is likely due to:
- Database not running
- Token not persisting
- Templates not loading
- CSS blocking interactions

## TL;DR - The Solution

1. **Start MySQL, Backend, Frontend** (3 commands)
2. **Login and test** (5 tests)
3. **Check console for errors** (F12)
4. **Apply fixes** from SESSION_22_CODE_FIXES.md
5. **Retest and report**

---

## 60-Second Setup

```bash
# Terminal 1: Start MySQL
net start MySQL80

# Terminal 2: Start Backend
cd veelearn-backend && npm start

# Terminal 3: Start Frontend
cd veelearn-frontend && npx http-server . -p 5000
```

Visit: **http://localhost:5000**

Login: **viratsuper6@gmail.com / Virat@123**

---

## 6 Quick Tests

### TEST 1: Token Storage ⏱️ 30 seconds
```
1. Login
2. F12 → Console
3. Type: localStorage.getItem('token')
4. Result: Should show long string starting with "eyJ"
```

### TEST 2: Block Drag ⏱️ 1 minute
```
1. Dashboard → Create Course → Block-Based
2. Try dragging "Add" block to canvas
3. Look in console: Should see "Drag started from palette"
4. Result: Block appears on canvas
```

### TEST 3: Block Drop ⏱️ 30 seconds
```
1. Continue from TEST 2
2. Drop block on canvas
3. Look in console: Should see "Drop detected"
4. Result: Block stays on canvas
```

### TEST 4: Courses Show ⏱️ 1 minute
```
1. Dashboard → My Courses
2. Result: Should see any pending courses you created
3. Dashboard → Available Courses
4. Result: Should see approved courses from others
```

### TEST 5: Simulator Publish ⏱️ 1 minute
```
1. With blocks on canvas, click "📤 Publish"
2. Enter name and description
3. Look in console: Check for token debug output
4. Result: "Simulator published successfully!"
```

### TEST 6: Simulator View ⏱️ 30 seconds
```
1. Go to Marketplace
2. Click any simulator
3. Result: Simulator displays with canvas
```

---

## 🚨 Critical Console Messages to Look For

### ✅ SUCCESS Messages
```
✓ Token stored successfully
✓ Block templates loaded successfully
✓ Drag started from palette
✓ Drop detected
✓ Block added successfully
✓ Simulator published successfully
```

### ❌ ERROR Messages  
```
❌ blockTemplates not loaded
❌ No authentication token found
❌ Template not found for block type
❌ Failed to publish simulator
❌ Cannot find property 'id' of undefined
```

---

## 🔧 If Tests Fail

| Test | Fails | Likely Cause | Fix |
|------|-------|--------------|-----|
| 1 | Token NULL | Session expired | Login again |
| 2 | Drag doesn't work | Templates not loaded | Check FIX #2 |
| 3 | Drop doesn't work | No handler attached | Check FIX #3 |
| 4 | No courses show | Database empty | Create courses first |
| 5 | Publish fails | No token or API error | Check console logs |
| 6 | Simulator blank | API error or rendering | Check simulator-view.html |

---

## 📋 Checklist

- [ ] MySQL started: `net start MySQL80`
- [ ] Backend started: `npm start`
- [ ] Frontend started: `npx http-server . -p 5000`
- [ ] Can access http://localhost:5000
- [ ] Can login successfully
- [ ] Token shows in localStorage
- [ ] Block can be dragged
- [ ] Block can be dropped on canvas
- [ ] Courses load and display
- [ ] Simulator publishes
- [ ] Simulator loads in marketplace

---

## 📊 Test Results Template

Copy and fill in:

```
SESSION 22 TEST RESULTS
======================

TEST 1 (Token Storage):   ☐ PASS  ☐ FAIL
TEST 2 (Block Drag):      ☐ PASS  ☐ FAIL
TEST 3 (Block Drop):      ☐ PASS  ☐ FAIL
TEST 4 (Courses):         ☐ PASS  ☐ FAIL
TEST 5 (Publish):         ☐ PASS  ☐ FAIL
TEST 6 (View):            ☐ PASS  ☐ FAIL

CONSOLE ERRORS:
[Paste any errors here]

TOKEN VALUE:
[Paste token value here]

COURSES LOADED:
[How many courses loaded?]

BLOCKS IN PALETTE:
[How many blocks available?]

NOTES:
[Any other observations]
```

---

## 🚀 Next Steps

1. **Run the 6 tests** above
2. **Document all failures** with console output
3. **Apply fixes** from SESSION_22_CODE_FIXES.md
4. **Retest** each fix
5. **Report back** with full test results

---

## 📞 Common Issues

**"Connection refused" on localhost:3000**
→ Backend not running or wrong port

**"Token is NULL"**
→ Login again or check localStorage storage code

**"No blocks in palette"**
→ block-templates-unified.js not loading

**"Block won't drag"**
→ Drag event handler not firing, check console

**"Courses don't show"**
→ Database empty or filtering wrong

**"Can't publish simulator"**
→ No token or /api/simulators endpoint error

---

## 💻 Browser DevTools (F12)

Essential tabs:
- **Console**: See all logs and errors
- **Network**: Check API calls
- **Application → Local Storage**: See token
- **Elements**: Inspect HTML structure

---

## 📖 Detailed Guides

- **SESSION_22_IMMEDIATE_FIXES.md** - Full testing guide
- **SESSION_22_CODE_FIXES.md** - Code changes to apply
- **AGENTS.md** - Complete development notes

---

**START HERE**: Run the 3 startup commands, then run the 6 tests! 🚀
