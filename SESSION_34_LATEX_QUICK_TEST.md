# Session 34 - LaTeX Equation Editor Quick Test Guide

## Quick Test (5 minutes)

### 1. Start the Application
```bash
# Terminal 1: Backend
cd veelearn-backend
npm start

# Terminal 2: Frontend
cd veelearn-frontend
npx http-server . -p 5000
```

Open browser: `http://localhost:5000`

### 2. Login
- Email: `viratsuper6@gmail.com`
- Password: `Virat@123`

### 3. Create/Edit a Course
- Click "Create New Course" or edit existing course
- Click the "∑ LaTeX Equation" button in the toolbar

### 4. Test LaTeX Modal

#### Test 4.1: Open Modal
✅ Modal should appear with:
- Title: "Insert LaTeX Equation"
- Radio buttons for Inline/Display
- Text input for LaTeX code
- Preview area
- Symbol buttons
- Template buttons
- Insert/Cancel buttons

#### Test 4.2: Type Simple Equation
1. Keep "Inline" selected
2. Type: `E = mc^2`
3. ✅ Preview should show: E = mc²
4. Click "Insert Equation"
5. ✅ Equation appears in editor

#### Test 4.3: Test Display Equation
1. Click "∑ LaTeX Equation" again
2. Select "Display"
3. Type: `\frac{a}{b}`
4. ✅ Preview should show: a/b (fraction) centered
5. Click "Insert Equation"
6. ✅ Equation appears on new line in editor

#### Test 4.4: Test Symbol Buttons
1. Click "∑ LaTeX Equation" again
2. Click "α (alpha)" button
3. ✅ Input should contain: `\alpha`
4. ✅ Preview should show: α
5. Click "Insert Equation"

#### Test 4.5: Test Template Buttons
1. Click "∑ LaTeX Equation" again
2. Click "Quadratic formula" button
3. ✅ Input should auto-fill with quadratic formula
4. ✅ Preview should show the complete formula
5. Click "Insert Equation"

#### Test 4.6: Test Close Options
1. Click "∑ LaTeX Equation" again
2. **Option A**: Click "Cancel" button → ✅ Modal closes
3. Click "∑ LaTeX Equation" again
4. **Option B**: Click outside modal → ✅ Modal closes
5. Click "∑ LaTeX Equation" again
6. **Option C**: Click X button → ✅ Modal closes

#### Test 4.7: Test Preview Updates
1. Click "∑ LaTeX Equation" again
2. Type slowly: `E`
3. ✅ Preview updates
4. Type: `=`
5. ✅ Preview updates
6. Continue typing: `m c^2`
7. ✅ Preview updates in real-time

### 5. Save Course
- Click "💾 Save as Draft" or "✅ Submit for Approval"
- ✅ Course saves with LaTeX equations
- Equations should render with MathJax

### 6. View Course
- Go to Dashboard
- Click "View" on course
- ✅ LaTeX equations should display properly
- ✅ Equations should be fully rendered by MathJax

## Success Criteria
- ✅ All 8 tests pass
- ✅ Modal opens/closes properly
- ✅ Preview updates in real-time
- ✅ Symbol buttons insert correctly
- ✅ Template buttons insert correctly
- ✅ Equations save with course
- ✅ Equations render when viewing course

## What to Look For

### Good Signs ✅
- Modal appears immediately
- Preview updates as you type
- Equations render properly
- MathJax symbols appear correct
- Course saves successfully

### Issues to Report ❌
- Modal doesn't open
- Preview doesn't update
- Equations don't save
- MathJax doesn't render
- CSS styling looks wrong
- Buttons don't work

## Browser Console
Press F12 and check Console tab:
- ✅ No JavaScript errors
- ✅ No 404 errors
- ✅ LaTeX functions should be defined

## Test Data Examples

### Simple Equations
- `E = mc^2` → Einstein's equation
- `a^2 + b^2 = c^2` → Pythagorean theorem
- `F = ma` → Newton's 2nd law

### Complex Equations
- `\frac{-b \pm \sqrt{b^2-4ac}}{2a}` → Quadratic formula
- `\sum_{i=1}^{n} x_i` → Summation
- `\int_a^b f(x)dx` → Integral

### Greek Letters
- `\alpha`, `\beta`, `\gamma`, `\Delta` → Greek letters
- `\lambda` → Wavelength
- `\pi`, `\theta`, `\phi` → Pi, Theta, Phi

## Common Issues & Solutions

### Modal doesn't appear
- Check JavaScript console for errors
- Verify MathJax library loaded
- Hard refresh browser (Ctrl+F5)

### Preview doesn't update
- Check if MathJax CDN is accessible
- Verify internet connection
- Try refreshing page

### Equations don't save
- Verify authentication token valid
- Check backend is running
- Look at browser Network tab for API errors

### MathJax doesn't render
- Clear browser cache
- Check MathJax CDN availability
- Verify index.html has MathJax script tags

## Next Steps After Successful Test
1. Create additional test courses with various equations
2. Test on different browsers
3. Test on mobile devices
4. Test performance with many equations
5. Gather user feedback

---

## Session 34 Timeline
- ⏱️ Frontend setup: 5 minutes
- ⏱️ Login & create course: 2 minutes
- ⏱️ Test LaTeX features: 8-10 minutes
- ⏱️ **Total: 15-20 minutes**
