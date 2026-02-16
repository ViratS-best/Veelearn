# SESSION 37B - Quick Testing Guide

**Time**: 5 minutes
**What**: Test the 3 new API endpoints

---

## Step 1: Start Backend

```bash
cd veelearn-backend
npm start
```

Wait for:
```
✓ Server running on port 3000
✓ Database connected successfully
```

---

## Step 2: Get Authentication Token

### Option A: cURL
```bash
curl -X POST http://localhost:3000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"viratsuper6@gmail.com","password":"Virat@123"}'
```

### Option B: Postman
1. POST to `http://localhost:3000/api/login`
2. Body (JSON):
```json
{
  "email": "viratsuper6@gmail.com",
  "password": "Virat@123"
}
```

**Save the token** from response:
```json
{
  "success": true,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {...}
  }
}
```

---

## Step 3: Test Endpoint #1 - Get All Courses

### Test 3a: List All Courses
```bash
curl "http://localhost:3000/api/courses/all?page=1&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Expected Response**:
```json
{
  "success": true,
  "message": "All courses retrieved",
  "data": {
    "courses": [
      {
        "id": 1,
        "title": "Physics 101",
        "description": "...",
        "creator_id": 5,
        "creator_email": "teacher@example.com",
        "status": "approved",
        "created_at": "2026-02-15T10:30:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 42,
      "pages": 5
    }
  }
}
```

### Test 3b: Search Courses
```bash
curl "http://localhost:3000/api/courses/all?page=1&limit=10&search=physics" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Expected**: Only courses with "physics" in title/description

---

## Step 4: Test Endpoint #2 - Get Student Accuracy

### Test 4a: Student Views Own Accuracy
```bash
curl "http://localhost:3000/api/student/15/assignment/3/accuracy" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Expected Response** (if submission exists):
```json
{
  "success": true,
  "message": "Student accuracy retrieved",
  "data": {
    "assignmentId": 3,
    "studentId": 15,
    "correct_answers": 7,
    "total_questions": 10,
    "quiz_accuracy": 70.0,
    "completion_percentage": 85,
    "is_submitted": true,
    "is_late": false,
    "submission_date": "2026-02-16T14:22:00Z"
  }
}
```

**Expected Response** (if no submission):
```json
{
  "success": true,
  "message": "No submission yet",
  "data": {
    "assignmentId": 3,
    "studentId": 15,
    "correct_answers": 0,
    "total_questions": 0,
    "quiz_accuracy": 0,
    "is_submitted": false
  }
}
```

---

## Step 5: Test Endpoint #3 - Get Class Accuracy

### Test 5a: Teacher Views Class Performance
```bash
curl "http://localhost:3000/api/teacher/assignment/3/student-accuracy" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Expected Response**:
```json
{
  "success": true,
  "message": "Student accuracy for assignment retrieved",
  "data": {
    "assignmentId": 3,
    "statistics": {
      "totalStudents": 25,
      "submittedCount": 22,
      "averageAccuracy": "78.40",
      "lateSubmissions": 3
    },
    "students": [
      {
        "studentId": 5,
        "studentEmail": "alice@student.com",
        "correctAnswers": 9,
        "totalQuestions": 10,
        "quizAccuracy": 90.0,
        "completionPercentage": 100,
        "isSubmitted": true,
        "isLate": false,
        "submissionDate": "2026-02-15T09:30:00Z"
      },
      {
        "studentId": 8,
        "studentEmail": "bob@student.com",
        "correctAnswers": 6,
        "totalQuestions": 10,
        "quizAccuracy": 60.0,
        "completionPercentage": 85,
        "isSubmitted": true,
        "isLate": true,
        "submissionDate": "2026-02-16T22:15:00Z"
      }
    ]
  }
}
```

---

## Step 6: Test Updated Endpoint - Submit Assignment

### Test 6a: Submit Assignment
```bash
curl -X POST http://localhost:3000/api/student/submit-assignment \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "assignmentId": 3,
    "completionPercentage": 85
  }'
```

**Expected Response**:
```json
{
  "success": true,
  "message": "Assignment submission recorded",
  "data": {
    "isLate": false,
    "totalQuestions": 10,
    "correctAnswers": 8,
    "quizAccuracy": 80.0
  }
}
```

---

## Postman Collection (Optional)

Save as `.json` and import into Postman:

```json
{
  "info": {
    "name": "Veelearn Session 37B API Tests",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Login",
      "request": {
        "method": "POST",
        "url": "http://localhost:3000/api/login",
        "body": {
          "raw": "{\"email\":\"viratsuper6@gmail.com\",\"password\":\"Virat@123\"}"
        }
      }
    },
    {
      "name": "Get All Courses",
      "request": {
        "method": "GET",
        "url": "http://localhost:3000/api/courses/all?page=1&limit=10",
        "header": {
          "key": "Authorization",
          "value": "Bearer {{token}}"
        }
      }
    },
    {
      "name": "Get Student Accuracy",
      "request": {
        "method": "GET",
        "url": "http://localhost:3000/api/student/15/assignment/3/accuracy",
        "header": {
          "key": "Authorization",
          "value": "Bearer {{token}}"
        }
      }
    },
    {
      "name": "Get Class Accuracy",
      "request": {
        "method": "GET",
        "url": "http://localhost:3000/api/teacher/assignment/3/student-accuracy",
        "header": {
          "key": "Authorization",
          "value": "Bearer {{token}}"
        }
      }
    },
    {
      "name": "Submit Assignment",
      "request": {
        "method": "POST",
        "url": "http://localhost:3000/api/student/submit-assignment",
        "header": {
          "key": "Authorization",
          "value": "Bearer {{token}}"
        },
        "body": {
          "raw": "{\"assignmentId\":3,\"completionPercentage\":85}"
        }
      }
    }
  ]
}
```

---

## Troubleshooting

### "No token provided" Error
- Make sure to include `Authorization: Bearer TOKEN` header
- Get token from login endpoint first

### "Unauthorized access" Error
- Verify you're a teacher trying to access /api/teacher endpoint
- Or ensure you're accessing student/assignment with right studentId

### "Assignment not found" Error
- Verify assignment ID exists in your database
- Check classroom_assignments table has the ID

### "No courses" Returned
- Make sure courses exist in database
- Verify course status is 'approved' or you're the creator

---

## Test Results Template

```
✓ TEST 1: Get All Courses - PASS/FAIL
  - Pagination: Works?
  - Search: Works?
  - Creator info: Returned?

✓ TEST 2: Get Student Accuracy - PASS/FAIL
  - Data returned: Yes?
  - Accuracy calculated: Yes?
  - Metadata included: Yes?

✓ TEST 3: Get Class Accuracy - PASS/FAIL
  - Statistics returned: Yes?
  - Student list: Correct count?
  - Average accuracy: Calculated?

✓ TEST 4: Submit Assignment - PASS/FAIL
  - Accuracy stored: Yes?
  - Response includes metrics: Yes?

✓ TEST 5: Database - PASS/FAIL
  - New columns exist: Yes?
  - Data persists: Yes?
```

---

## Success Criteria

All 3 endpoints should:
- ✅ Return 200 OK status
- ✅ Have `success: true` in response
- ✅ Return data in expected format
- ✅ Handle errors with proper status codes
- ✅ Require valid JWT token
- ✅ Enforce authorization rules

---

**Status**: Ready to test
**File**: SESSION_37B_BACKEND_API_ENHANCEMENTS.md for full documentation

