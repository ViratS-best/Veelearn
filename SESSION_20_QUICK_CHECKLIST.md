# Session 20 - Quick Start Checklist

## 🚀 START ALL SERVICES (5 mins)

### Terminal 1: MySQL
```bash
net start MySQL80
# Verify: wmic service where name="MySQL80" get state
```

### Terminal 2: Backend
```bash
cd veelearn-backend
npm start
# MUST see: "Server running on port 3000" AND "Database connected successfully"
```

### Terminal 3: Frontend
```bash
cd veelearn-frontend
npx http-server . -p 5000
# Should see: "Starting up http-server"
```

---

## ✅ QUICK HEALTH CHECK (2 mins)

```bash
# Terminal 4: Test API
curl http://localhost:3000/api/courses
# Expected: {"success":true,"message":"Courses retrieved","data":[...]}
```

---

## 🧪 RUN 6 TESTS (10 mins)

**Browser**: Open http://localhost:5000

1. **Login Test**
   - Email: `viratsuper6@gmail.com`
   - Password: `Virat@123`
   - Result: ✅ Logged in or ❌ Failed

2. **DevTools Console** (F12)
   - Run: `localStorage.getItem('token')`
   - Result: ✅ Long token string or ❌ NULL

3. **Dashboard Test**
   - Run: `console.log('Courses:', myCourses.length, availableCourses.length)`
   - Result: ✅ Numbers > 0 or ❌ All zeros

4. **Block Drag Test**
   - Go to: Dashboard → Create Course → Block-Based
   - Try: Drag "Add" block to canvas
   - Result: ✅ Block appears or ❌ No response

5. **Publish Test**
   - Click: "📤 Publish" button
   - Enter: Simulator name
   - Result: ✅ Success message or ❌ "Not authenticated"

6. **Marketplace Test**
   - Go to: Simulator Marketplace
   - Click: Any simulator
   - Result: ✅ Opens and displays or ❌ Blank page

---

## 📋 EXPECTED RESULTS

### ✅ All Tests Pass
- Database is running correctly
- Token storage is working
- All 6 features functional
- Ready for production testing

### ❌ Some Tests Fail
1. Note which test(s) failed
2. Check error in DevTools Console
3. Report errors to continue debugging
4. Provide console output for diagnosis

---

## 🔧 COMMON QUICK FIXES

| Issue | Fix |
|-------|-----|
| Backend won't start | `net start MySQL80` first |
| Courses show 0 | Check MySQL is running |
| Token is NULL | Logout → Login → Check localStorage |
| Blocks won't drag | Refresh page, check console |
| Can't publish | Check token with F12 console |

---

## 📞 REPORT FORMAT

```
Test Results (Date: ___):

✅/❌ TEST #1: Token stored?
✅/❌ TEST #2: Courses loaded?
✅/❌ TEST #3: Block drag works?
✅/❌ TEST #4: Can publish simulator?
✅/❌ TEST #5: Can publish course?
✅/❌ TEST #6: Can view simulator?

Console Errors:
[paste any errors here]

Notes:
[any additional observations]
```

---

## 🎯 Next Steps

1. Complete all 6 tests
2. Report results
3. I will fix any failing tests
4. Repeat testing cycle until all pass
5. Move to enhanced features

---

**Time Estimate**: 20 minutes total
**Difficulty**: Easy (mostly copy-paste commands)
**Success Rate**: Should be 90%+ if setup correct
