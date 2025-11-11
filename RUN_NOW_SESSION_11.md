# SESSION 11 - RUN THIS NOW

## STEP 1: Open Two Terminal Windows

### Terminal 1: Backend Server

```bash
cd c:\Users\kalps\Documents\Veelearn\veelearn-backend
npm start
```

**You should see:**
```
Server running on port 3000
Connected to MySQL database
```

### Terminal 2: Frontend Server

```bash
cd c:\Users\kalps\Documents\Veelearn\veelearn-frontend
python -m http.server 5000
```

**You should see:**
```
Serving HTTP on 0.0.0.0 port 5000...
```

---

## STEP 2: Open Browser

Go to: **http://localhost:5000**

---

## STEP 3: Login

Use this account:
- **Email**: viratsuper6@gmail.com
- **Password**: Virat@123

---

## STEP 4: Test These 6 Issues

1. **Approved courses in public list** - Approve course in Admin Panel, check if it appears in Available Courses
2. **View own pending courses** - Go to "My Courses" - should see pending courses
3. **Drag blocks on canvas** - Click Block Simulator, try dragging blocks
4. **X button exists** - Look at top-right of block simulator
5. **View simulator** - Click a simulator in marketplace
6. **Publish simulator** - Look for publish/save button

---

## STEP 5: Check DevTools

Press **F12** in browser, go to **Console** tab

- Copy any red error messages
- Take screenshots if something is broken

---

## STEP 6: Report Results

Write down:
- Which tests **PASSED** ✅
- Which tests **FAILED** ❌
- What error messages you see
- What happens instead (if it breaks differently)

---

## Reference

Full details in: **AGENTS.md** (SESSION 11 - WHEN TO RUN & TEST)

Checklist: **SESSION_11_TEST_CHECKLIST.md**

---

**The 6 Confirmed Issues:**
1. ❌ Approved courses NOT showing in public list
2. ❌ Cannot drag blocks onto canvas
3. ❌ No X button to publish or go back
4. ❌ Cannot view course before approval
5. ❌ Simulators don't work (cannot view/execute)
6. ❌ Cannot publish simulators

**Status**: Ready to test and fix
