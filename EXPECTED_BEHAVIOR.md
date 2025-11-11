# EXPECTED BEHAVIOR - What Should Work When 6 Issues Are Fixed

## Issue #1: Approved Courses Show in Public List

### Current Behavior ❌
- Course created → shows in "My Courses" with "Pending" status
- Admin approves course → still doesn't appear in "Available Courses"
- Other users cannot enroll in approved courses

### Expected Behavior ✅
- Course created → shows in "My Courses" with "Pending" status
- Admin approves course → **immediately appears in "Available Courses"**
- Other users can **see and enroll** in approved courses
- Created course is NOT shown to creator in "Available Courses" (avoids duplicates)

### User Flow
```
1. Teacher creates course "Physics 101"
   → Status: PENDING
   → Visible to: Only teacher in "My Courses"

2. Admin goes to "Pending Courses"
   → Sees "Physics 101" by teacher
   → Clicks "Approve Course"

3. Teacher navigates to "Available Courses"
   → Doesn't see their own course (filter removes self)

4. Different student logs in
   → Goes to "Available Courses"
   → **SEES "Physics 101"**
   → Can click "Enroll"

5. Student enrolls
   → Can view course content
   → Can see assigned simulators
```

---

## Issue #2: Block Drag & Drop Works

### Current Behavior ❌
- Open Block Simulator
- Try to drag block from left sidebar to canvas
- Block doesn't move, no visual feedback
- Cannot create blocks on canvas

### Expected Behavior ✅
- Open Block Simulator
- **See blocks in left sidebar** (Math, Drawing, Physics, etc.)
- **Drag block to canvas** (smooth drag with visual feedback)
- **Block appears on canvas** where dropped
- **Block is selectable** and shows inputs/outputs
- **Can delete block** by clicking X on it
- **Can connect blocks** (output of one to input of another)
- **Can run simulation** with all blocks

### Visual Feedback
```
BEFORE DRAG:
[Left Sidebar]                [Canvas - Empty]
┌─────────────┐              ┌───────────────┐
│ + Circle    │              │               │
│ + Rectangle │              │               │
│ + Add       │              │               │
│ + Multiply  │              │               │
└─────────────┘              └───────────────┘

DURING DRAG:
[Left Sidebar]                [Canvas]
┌─────────────┐              ┌───────────────┐
│ + Circle    │              │               │
│ + Rectangle │    ⟹ ◘ (ghost)           │
│ + Add       │              │               │
│ + Multiply  │              └───────────────┘
└─────────────┘

AFTER DROP:
[Left Sidebar]                [Canvas - With Block]
┌─────────────┐              ┌───────────────┐
│ + Circle    │              │ ┌───────────┐ │
│ + Rectangle │              │ │ Circle    │ │
│ + Add       │              │ │ x: 10     │ │
│ + Multiply  │              │ │ y: 10     │ │
└─────────────┘              │ │ [x] Delete│ │
                             │ └───────────┘ │
                             └───────────────┘
```

---

## Issue #3: Exit & Publish Buttons Work

### Current Behavior ❌
- Open Block Simulator
- Look at toolbar - no visible buttons
- Cannot exit simulator editor
- Cannot publish simulator
- **User is trapped** in editor

### Expected Behavior ✅
- Open Block Simulator
- **See toolbar with buttons at top right:**
  - "📤 Publish" button (saves and publishes simulator)
  - "✕ Exit" button (goes back to course/dashboard)
- **Click "Publish":**
  - Confirms all blocks are valid
  - Saves simulator with title and description
  - Shows success: "Simulator published! ID: 12345"
  - Simulator appears in Marketplace
  - Redirect to Marketplace or Dashboard
- **Click "Exit":**
  - Warns if unsaved blocks: "You have unsaved changes. Exit anyway?"
  - Returns to previous page (course editor or dashboard)
  - Blocks are lost if not published

### Visual
```
┌──────────────────────────────────────────────────┐
│ Block Simulator Creator           [📤 Publish] [✕]│  ← Buttons here
├──────────────────────────────────────────────────┤
│                                                  │
│  [Left Sidebar with Blocks]  [Canvas Area]      │
│                                                  │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## Issue #4: Can View Course Before Admin Approval

### Current Behavior ❌
- Teacher creates course
- Course status is PENDING (not approved by admin)
- Course creator **CANNOT see their own course** in "My Courses"
- Must wait for admin approval to preview
- **Cannot edit** course that creator can't see

### Expected Behavior ✅
- Teacher creates course "Math 101"
- Course appears in **"My Courses"** immediately with **orange "Pending" badge**
- Teacher can:
  - **View** course content
  - **Edit** course
  - **Delete** course
  - **Preview** how it looks
- Course does NOT appear in "Available Courses" (for other users)
- After admin approves:
  - Badge changes from orange "Pending" to green "Approved"
  - Course becomes visible in "Available Courses" for other users

### User View
```
MY COURSES (As Course Creator):
┌──────────────────────────────────────┐
│ [Pending] Math 101 by You            │
│ Description: Learn math basics       │
│ [Edit] [View] [Delete]               │
│                                      │
│ [Approved] Physics 101 by You        │
│ Description: Learn physics concepts  │
│ [Edit] [View] [Delete]               │
└──────────────────────────────────────┘

AVAILABLE COURSES (As Other User):
┌──────────────────────────────────────┐
│ Physics 101 by You                   │
│ Description: Learn physics concepts  │
│ [Enroll] [Preview]                   │
│                                      │
│ (No Math 101 - still pending)        │
└──────────────────────────────────────┘
```

---

## Issue #5: Simulators Display & Work

### Current Behavior ❌
- Go to Marketplace
- See simulator listed
- Click on simulator
- Page shows blank or error
- Simulator doesn't load or display
- **Cannot view simulator**

### Expected Behavior ✅
- Go to Marketplace → "Browse Simulators"
- See list of simulators:
  ```
  - Physics Gravity Simulator (5.0 stars, 342 downloads)
  - Math Fraction Game (4.2 stars, 189 downloads)
  - Visual Shape Tool (4.8 stars, 567 downloads)
  ```
- Click simulator → Opens **simulator-view.html**
- Simulator loads and displays:
  - **Title**: "Physics Gravity Simulator"
  - **Description**: "Drop objects and watch gravity in action"
  - **Canvas**: Shows visual simulation running
  - **Controls**: Run, Pause, Reset buttons work
  - **Statistics**: Rating, downloads, created date
- **Click "Run"**: Simulator executes all blocks in proper order
- **Canvas shows results**: Objects falling, colliding, moving as expected
- **Click "Back"**: Returns to Marketplace
- **Can Rate/Comment**: Leave review for simulator

### Visual
```
SIMULATOR VIEWER:
┌─────────────────────────────────────────────────┐
│ Physics Gravity Simulator              [←] [Run] │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │                                          │  │
│  │     ◊ (falling object)                  │  │
│  │                                          │  │
│  │                ◊                         │  │
│  │                                          │  │
│  │  ════════════════════════════════════   │  │ ← Canvas
│  │                                          │  │
│  │  Gravity: 9.8 m/s²                      │  │
│  │  Objects: 3                              │  │
│  │  Collisions: 5                           │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│ ⭐ 5.0 (24 ratings) | 👥 342 downloads         │
│                                                 │
│ Created by: Teacher Name | Published: Nov 2025│
└─────────────────────────────────────────────────┘
```

---

## Issue #6: Can Publish Simulators

### Current Behavior ❌
- Create blocks in Block Simulator
- Look for publish button - not visible or doesn't work
- Click publish - nothing happens
- Simulator never saved
- **Cannot release simulator to marketplace**

### Expected Behavior ✅
- Add blocks to Block Simulator canvas
- Click **"📤 Publish"** button
- Dialog appears:
  ```
  Enter Simulator Details:
  Title: [Physics Gravity Demo      ]
  Description: [Drop objects and ... ]
  [Cancel] [Publish]
  ```
- Click "Publish"
- **Simulator saves** with status "Published"
- **Alert shows**: `"Simulator published! ID: 12345"`
- **Redirect to**: Marketplace or Dashboard
- **Can find simulator**: Go to Marketplace → Search for title
- **Simulator appears**: In public list with:
  - Your title and description
  - Rating: "New" (0 stars)
  - Downloads: 0
  - "Run Simulator" button
- **Other users can**: View, rate, comment, fork, download

### User Flow
```
1. Create simulator in Block Simulator
   [Add blocks to canvas]
   
2. Click "📤 Publish" button
   ↓
3. Dialog asks for title/description
   ↓
4. Click "Publish"
   ↓
5. Success! "Simulator published! ID: 12345"
   ↓
6. Redirect to Marketplace
   ↓
7. Search: "Physics Gravity Demo"
   ↓
8. See your simulator in list! ✅
```

---

## Complete System Flow

### Best Case Scenario - Everything Works ✅

```
1. TEACHER CREATES COURSE
   Open index.html → Login → Dashboard → Create Course
   "Add course title and description" → Save
   ✅ Course appears in "My Courses" with orange "Pending"

2. TEACHER ADDS SIMULATORS
   Edit Course → "Add Block Simulator"
   Open simulator → Drag blocks → Publish
   ✅ Simulator saved and appears in course

3. TEACHER PREVIEWS
   Click "View" on course
   ✅ Sees course with embedded simulators

4. ADMIN APPROVES
   Login as admin → Pending Courses → Approve
   ✅ Course status changes to green "Approved"

5. STUDENT ENROLLS
   Login as different user → Available Courses
   ✅ Sees teacher's approved course
   Click "Enroll" → Course added to my courses
   
6. STUDENT LEARNS
   Click "View" on enrolled course
   ✅ Sees course content and simulators
   Click "Run Simulator" → Simulator executes
   ✅ Sees visual results on canvas

7. STUDENT PROVIDES FEEDBACK
   Rate simulator → 5 stars ⭐
   Comment: "Great learning tool!"
   ✅ Feedback saved and visible to others
```

---

## Test Checklist - What Should Happen

### ✅ TEST COURSE APPROVAL FLOW
- [ ] Create course → appears in "My Courses" (Pending)
- [ ] Approve course → appears in "Available Courses"
- [ ] Other user sees approved course
- [ ] Other user can enroll

### ✅ TEST BLOCK SIMULATOR
- [ ] Open Block Simulator
- [ ] Drag block to canvas → block appears
- [ ] Drag multiple blocks → all appear
- [ ] Click Run → all blocks execute
- [ ] See results on canvas

### ✅ TEST EXIT/PUBLISH
- [ ] See "Exit" button → can click it
- [ ] See "Publish" button → can click it
- [ ] Publish → saves simulator
- [ ] Exit → returns to previous page

### ✅ TEST VIEW PENDING
- [ ] Create course as teacher
- [ ] See in "My Courses" → Pending badge
- [ ] Can Edit, View, Delete course
- [ ] Not visible to other users

### ✅ TEST SIMULATOR VIEW
- [ ] Create and publish simulator
- [ ] Go to Marketplace
- [ ] Click simulator → opens viewer
- [ ] Canvas shows simulator
- [ ] Can run/pause/reset

### ✅ TEST PUBLISH
- [ ] Create blocks in simulator
- [ ] Click "Publish"
- [ ] Enter title and description
- [ ] Success message appears
- [ ] Can find in Marketplace

---

## Performance Expectations

| Action | Expected Time | Status |
|--------|---------------|--------|
| Login | < 1 second | ✅ |
| Load Dashboard | < 2 seconds | ✅ |
| Load Marketplace | < 2 seconds | ✅ |
| Create Course | < 1 second | ✅ |
| Approve Course | < 1 second | ✅ |
| Drag block | Immediate | ✅ |
| Run simulator | < 2 seconds | ✅ |
| Publish simulator | < 2 seconds | ✅ |

---

## Error Messages (What NOT to See)

❌ **Should NOT see these:**
```
- "blockTemplates is not defined"
- "Cannot read property 'style' of null"
- "ReferenceError: publishSimulator is not defined"
- "404 Not Found"
- "Unauthorized" (when logged in)
- "Cannot GET /api/courses"
```

✅ **These are OK:**
```
- "No courses available to enroll in" (if DB empty)
- "No simulators found" (if none created yet)
- Network errors if backend down (expected)
```

---

## Success = All 6 Issues Fixed & Working

When you test and **all 6 items show ✅**, the system is complete and ready!

---

*Last Updated: November 11, 2025*
*For testing, see SESSION_16_QUICK_START.md*
