# START TESTING NOW ✅

## Quick Setup (Copy & Paste)

Open 3 terminals and run these commands in order:

### Terminal 1: Start MySQL
```powershell
net start MySQL80
```

### Terminal 2: Start Backend
```powershell
cd C:\Users\kalps\Documents\Veelearn\veelearn-backend
npm start
```
Wait for: `Server running on port 3000`

### Terminal 3: Start Frontend
```powershell
cd C:\Users\kalps\Documents\Veelearn\veelearn-frontend
npx http-server . -p 5000
```

---

## Browser: Open and Test

1. Go to: http://localhost:5000
2. Login with:
   - Email: `viratsuper6@gmail.com`
   - Password: `Virat@123`

---

## Run Tests (5 Minutes Each)

### TEST 1: Save as Draft
1. Create new course
2. Click "💾 Save as Draft"
3. ✅ Should see orange "draft" badge in My Courses
4. ✅ Can click Edit to continue editing

### TEST 2: Submit for Approval
1. Create new course
2. Click "✅ Submit for Approval"
3. ✅ Should see orange "pending" badge
4. ✅ Goes to admin queue

### TEST 3: Admin Preview
1. Logout → Login as admin (same account)
2. Go to Admin Panel → Pending Courses
3. Click "👁️ Preview"
4. ✅ See full course content

### TEST 4: Publish Simulator
1. Go to Block Simulator
2. Add some blocks (Add, Draw Circle, etc.)
3. Click "📤 Publish"
4. Check Terminal 2 - should show:
   ```
   📝 CREATE SIMULATOR DEBUG:
     Blocks count: 2
   ✅ Simulator created with ID: [number]
   ```

### TEST 5: View & Run Simulator
1. Go to Marketplace
2. Click your published simulator
3. Click "▶ Run"
4. ✅ Canvas should display simulator

---

## Report Results

After tests, tell me:

```
TEST 1: ✅ or ❌
TEST 2: ✅ or ❌
TEST 3: ✅ or ❌
TEST 4: ✅ or ❌
TEST 5: ✅ or ❌

Any errors? (paste error message)
```

---

## Detailed Testing

Want more detailed tests? See: **SESSION_27_TESTING_GUIDE.md**

---

**Start now! Good luck!** 🚀
