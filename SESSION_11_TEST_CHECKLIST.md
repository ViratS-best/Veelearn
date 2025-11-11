# SESSION 11 - TEST CHECKLIST ✓

## CONFIRMED ISSUES (User Report)
> "When you approve a course nothing actually shows up to the public where courses are available and still simulators dont work you actually cant drag any blocks onto the board and then there is no x button to publish or to go back to creating your course and you cant view your sim either"

---

## BEFORE YOU START

### Prerequisites ✓
- [ ] Backend running: `npm start` in veelearn-backend
- [ ] Frontend running: `python -m http.server 5000` in veelearn-frontend
- [ ] Browser DevTools open (F12)
- [ ] Test account credentials: viratsuper6@gmail.com / Virat@123

---

## 6 CRITICAL TESTS

### TEST #1: Approved Courses Show in Public List
- [ ] Login to dashboard
- [ ] Go to Admin Panel
- [ ] Approve a pending course
- [ ] Check "Available Courses" 
- **Result**: ✅ Pass / ❌ Fail
- **Console Errors**: (note any errors)
- **Screenshot**: (if broken, take one)

### TEST #2: User Can View Their Own Course Before Approval
- [ ] Login as regular user
- [ ] Go to "My Courses" section
- [ ] See pending courses listed
- **Result**: ✅ Pass / ❌ Fail
- **Console Errors**: (note any errors)

### TEST #3: Block Simulator - Can Drag Blocks to Canvas
- [ ] Go to Dashboard → Create New Course → "Block-Based"
- [ ] Click "Block Simulator" button
- [ ] Try to drag a block from left sidebar to canvas
- [ ] Block should appear where dropped
- **Result**: ✅ Pass / ❌ Fail
- **Console Errors**: (note any errors)
- **What happens instead**: (describe behavior)

### TEST #4: Block Simulator - Has X & Publish Buttons
- [ ] Open Block Simulator
- [ ] Look at top-right corner
- [ ] Should see "✕ Exit" button
- [ ] Should see "📤 Publish" button
- **Result**: ✅ Pass / ❌ Fail
- **Buttons found**: (which ones?)

### TEST #5: Can View & Execute Simulator
- [ ] Go to Marketplace
- [ ] Click on a simulator to view it
- [ ] Simulator should display and be runnable
- **Result**: ✅ Pass / ❌ Fail
- **What happens instead**: (blank? error?)
- **Console Errors**: (note any errors)

### TEST #6: Can Publish/Save Simulator
- [ ] Create or open a simulator in editor
- [ ] Look for "Publish" or "Save" button
- [ ] Click it
- [ ] Status should change to "Published"
- **Result**: ✅ Pass / ❌ Fail
- **What happens instead**: (no button? error?)

---

## SUMMARY

Total Tests: 6
Passed: ___  (✅)
Failed: ___  (❌)

---

## CONSOLE ERROR LOG

Open DevTools (F12) → Console tab and paste any errors here:

```
[Paste console errors here]
```

---

## NOTES & OBSERVATIONS

```
[Write down anything unusual or important]
```

---

## WHEN YOU'RE DONE

Report your results:
1. How many tests passed/failed
2. Console errors (if any)
3. What fails and how

Then I will fix each issue!
