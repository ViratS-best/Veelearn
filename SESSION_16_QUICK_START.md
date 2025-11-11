# SESSION 16 - QUICK START GUIDE

## 🚀 Ready to Test? Start Here!

### Prerequisites ✅
- [ ] Backend running: `npm start` in veelearn-backend/
- [ ] Frontend running: HTTP server on port 5000
- [ ] Browser open: http://localhost:5000
- [ ] DevTools open: F12 (Console tab)

---

## ⚡ Quick Test (5 minutes)

### 1. Login
- Email: `viratsuper6@gmail.com`
- Password: `Virat@123`

### 2. Test Each Feature

#### TEST #1: Approve course → see in public list (30 seconds)
1. Go to Dashboard
2. Admin: Go "Pending Courses" → Click "Approve"
3. Switch user OR logout/login as different user
4. Go "Available Courses"
5. **✅ PASS** if approved course appears
6. **❌ FAIL** if course doesn't show

#### TEST #2: Drag blocks to canvas (30 seconds)
1. Create New Course → "Block-Based"
2. Open Block Simulator
3. Drag **any block** from left sidebar to canvas
4. **✅ PASS** if block appears on canvas
5. **❌ FAIL** if block stays in sidebar

#### TEST #3: See Exit/Publish buttons (10 seconds)
1. In Block Simulator, look at **top toolbar**
2. **✅ PASS** if see "📤 Publish" and "✕ Exit" buttons
3. **❌ FAIL** if buttons not visible

#### TEST #4: View pending courses as creator (30 seconds)
1. Create New Course (as regular user)
2. Go to "My Courses"
3. **✅ PASS** if new course appears with orange "Pending" badge
4. **❌ FAIL** if course not showing

#### TEST #5: View simulator (30 seconds)
1. Go to Marketplace (navbar)
2. Click any simulator card
3. **✅ PASS** if simulator page opens and loads
4. **❌ FAIL** if page blank or error

#### TEST #6: Publish simulator (30 seconds)
1. In Block Simulator, add blocks to canvas
2. Click "📤 Publish" button
3. **✅ PASS** if alert shows "Simulator published! ID: [number]"
4. **❌ FAIL** if button does nothing or error

---

## 📊 Results Template

```
ISSUE #1: ❌ or ✅
ISSUE #2: ❌ or ✅
ISSUE #3: ❌ or ✅
ISSUE #4: ❌ or ✅
ISSUE #5: ❌ or ✅
ISSUE #6: ❌ or ✅
```

**If any ❌, copy error from DevTools Console and report:**

---

## 🔧 If Tests Fail

### Check Console for Errors
1. DevTools (F12) → Console tab
2. Look for red error messages
3. Copy **exact error message**
4. Example: `"blockTemplates is not defined at line 1484"`

### Check Network Requests
1. DevTools → Network tab
2. Reload page
3. Look for red (failed) requests
4. Click request → see error response
5. Example: `{"success":false,"message":"Not authenticated"}`

### Hard Refresh & Retry
1. Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
2. Wait for page to load
3. Retry test

### Check if Logged In
1. DevTools → Application → localStorage
2. Look for `token` key
3. If empty: logout and login again

---

## 📚 Full Documentation

For detailed test procedures:
- See: **SESSION_16_TEST_PLAN.md**

For debugging each issue:
- See: **SESSION_16_NEXT_STEPS.md**

For code details:
- See: **AGENTS.md** (Search for "SESSION 16")

---

## 💾 Test Results Checklist

```
[ ] Issue #1 Tested
[ ] Issue #2 Tested  
[ ] Issue #3 Tested
[ ] Issue #4 Tested
[ ] Issue #5 Tested
[ ] Issue #6 Tested
[ ] All results recorded with ✅ or ❌
[ ] Error messages copied for any ❌
```

---

## 📞 Questions?

1. **Page doesn't load?** → Check backend running (port 3000)
2. **Buttons not visible?** → Press F12, check CSS
3. **API errors?** → Check Network tab for error response
4. **Not logged in?** → Check localStorage for token
5. **Block simulator broken?** → Check console for JavaScript errors

---

## Next Steps

1. **Run through Quick Test (5 minutes)**
2. **Record which tests pass/fail**
3. **Copy any error messages from console**
4. **Report results + error messages**
5. **I'll provide fixes for failures**
6. **Retest after fixes**

---

## 🎯 Goal

Get all 6 issues to show ✅ PASS and the system fully functional!

**Estimated Time**: 30 minutes testing + variable time for fixes

---

*Ready? Open http://localhost:5000 and start testing!*
