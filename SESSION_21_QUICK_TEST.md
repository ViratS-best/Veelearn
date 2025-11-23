# Session 21 - Quick Token Fix Test (5 Minutes)

## 🚀 FAST START

### 1️⃣ Open 3 Terminals

```bash
# Terminal 1: MySQL
net start MySQL80

# Terminal 2: Backend  
cd veelearn-backend && npm start

# Terminal 3: Frontend
cd veelearn-frontend && npx http-server . -p 5000
```

Wait for both to say "running"

---

## 2️⃣ Test in Browser (3 minutes)

1. Open http://localhost:5000
2. Login: viratsuper6@gmail.com / Virat@123
3. Press F12 (DevTools)
4. Click Console tab
5. Go to Dashboard
6. Click "Create New Course"
7. Select "Block-Based Simulator"
8. Drag "Add" block to canvas
9. Click "📤 Publish" button
10. Look at Console tab

---

## 3️⃣ What You Should See

### ✅ SUCCESS (Token found):
```
=== PUBLISH SIMULATOR DEBUG ===
All localStorage keys: ['token', 'email', ...]
Token key exists: true
Token value: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### ❌ FAILED (Token NULL):
```
=== PUBLISH SIMULATOR DEBUG ===
All localStorage keys: ['email']
Token key exists: false
Token value: "NULL"
CRITICAL: No token found!
```

---

## 4️⃣ Report Back

**Copy-paste this and fill in:**

```
Token Test Results:

Token shows in console? YES / NO

If YES - what did it show?
[copy first 50 chars]

If NO - did you see "LOGOUT CALLED"? YES / NO

Any error messages?
[copy error]

When did it fail?
- At login?
- At Publish click?
- Somewhere else?

Can you login? YES / NO

Can you see your courses? YES / NO
```

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Backend won't start | `net start MySQL80` first |
| Token is NULL | Logout → Login again |
| Publish doesn't work | Check console output first |
| Page blank | Refresh browser |
| Can't drag blocks | Check console for errors |

---

## ⏱️ Time: 5 minutes
**Difficulty**: Easy (mostly clicking)
**Don't be shy**: Report exactly what you see!
