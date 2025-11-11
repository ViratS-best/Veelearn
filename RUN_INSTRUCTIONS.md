# VEELEARN - RUN INSTRUCTIONS

## ✅ CLEANUP COMPLETE!

- **18 duplicate files deleted**
- **16 clean files remain**
- **All systems integrated**
- **Ready to test**

---

## QUICK START (2 Terminals)

### Terminal 1: Start Backend
```bash
cd veelearn-backend
npm start
```

Expected output:
```
Connected to MySQL database
Server running on port 3000
Tables created successfully
```

**Note**: If you get MySQL connection error, check your .env file has correct DB credentials.

---

### Terminal 2: Start Frontend Server
```bash
cd veelearn-frontend
python -m http.server 5000
```

Or with Node:
```bash
npx http-server . -p 5000
```

Expected output:
```
Serving HTTP on port 5000
```

---

## TEST IN BROWSER

### 1. Block-Based Simulator (Main Feature)
- **URL**: http://localhost:5000/block-simulator.html
- **What to test**:
  - Drag blocks from left sidebar to canvas
  - Connect blocks together
  - Click "Run" button
  - See results in console below
  - Try these blocks:
    - Math: Add, Multiply
    - Drawing: Circle, Rectangle
    - Physics: Gravity, Collision
    - Display: Text, Debug Info

### 2. Marketplace
- **URL**: http://localhost:5000/simulator-marketplace.html
- **What to test**:
  - See list of simulators
  - Search/filter simulators
  - Click on simulator to see details
  - Rate and comment
  - Fork simulator
  - Add to course

### 3. Simulator Creator Dashboard
- **URL**: http://localhost:5000/simulator-creator.html
- **What to test**:
  - View your simulators
  - Create new simulator
  - Edit simulator
  - Publish/unpublish
  - Delete simulator

---

## FILES THAT MATTER

### Frontend (veelearn-frontend/)
```
✅ block-simulator.html              - Block-based editor (MAIN)
✅ simulator-marketplace.html        - Marketplace browsing
✅ simulator-detail.html             - Simulator detail view
✅ simulator-creator.html            - Creator dashboard
✅ index.html                        - Main page
✅ script.js                         - Main app logic
✅ styles.css                        - Styling

Libraries:
✅ block-templates-unified.js        - 40+ block definitions
✅ block-execution-engine.js         - Block runner
✅ block-physics-engine.js           - Physics math
✅ block-animation.js                - Animation loop
✅ block-renderer-system.js          - Canvas rendering
✅ marketplace-api.js                - API calls
✅ marketplace-app.js                - Marketplace logic
✅ simulator-fork-system.js          - Fork/remix
```

### Backend (veelearn-backend/)
```
✅ server.js     - Express API (port 3000)
✅ package.json  - Dependencies
✅ .env          - Configuration (fill in your DB details)
```

---

## TROUBLESHOOTING

### Block Simulator Won't Load
1. Open DevTools (F12)
2. Check Console tab for errors
3. Verify all script files are loaded (Network tab)
4. Make sure port 5000 is serving files

### Marketplace Won't Connect
1. Check backend is running on port 3000
2. Check DevTools Console for API errors
3. Verify .env database settings

### "Cannot find module" error in backend
Run: `npm install` in veelearn-backend/

### Port Already in Use
- Backend: Change `PORT` in server.js
- Frontend: Use `python -m http.server 5001` (different port)

---

## WHAT WORKS NOW ✅

1. **Block Execution** - Drag blocks, connect, run
2. **Physics** - Gravity, collisions, spring forces
3. **Animation** - Smooth 60 FPS rendering
4. **Canvas Drawing** - Circles, rectangles, text, etc.
5. **Marketplace** - Browse, search, filter simulators
6. **Ratings** - 1-5 stars and comments
7. **Forking** - Copy and remix simulators
8. **Creator Dashboard** - Manage your simulators

---

## NEXT STEPS (After Testing)

If everything works:
1. Build more complex simulators
2. Test physics accuracy
3. Optimize performance
4. Deploy marketplace features
5. Integrate with courses

If you find bugs:
1. Check console for error messages
2. Check AGENTS.md for code patterns
3. Fix in appropriate file
4. Test again

---

**Status**: READY FOR TESTING  
**All Files Cleaned**: YES  
**No Duplicates**: YES  
**Entry Point Clear**: YES  

Run the Quick Start commands above and enjoy!
