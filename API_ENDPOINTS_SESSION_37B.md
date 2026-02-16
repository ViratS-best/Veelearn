# New API Endpoints - Session 37B

## Quick Reference

### 1. GET /api/courses/all
**Get all courses in system (for teacher assignment)**

| Aspect | Details |
|--------|---------|
| **Method** | GET |
| **Auth** | Required |
| **Parameters** | `?page=1&limit=10&search=physics` |
| **Purpose** | Teachers browse all courses to assign to class |
| **Returns** | Courses array + pagination metadata |

**Query Parameters**:
- `page` (1+): Page number (default: 1)
- `limit` (1-100): Results per page (default: 10)
- `search`: Text search in title/description

**Response Data**:
```json
{
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
```

---

### 2. GET /api/student/:studentId/assignment/:assignmentId/accuracy
**Get student's quiz accuracy on specific assignment**

| Aspect | Details |
|--------|---------|
| **Method** | GET |
| **Auth** | Required |
| **URL Params** | `:studentId`, `:assignmentId` |
| **Purpose** | Student views own accuracy OR teacher views student accuracy |
| **Returns** | Accuracy metrics for one student-assignment pair |

**Access Control**:
- ✅ Student can view own accuracy (studentId matches token user)
- ✅ Teacher/Admin can view any student's accuracy
- ❌ Student cannot view other students' accuracy

**Response Data**:
```json
{
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
```

---

### 3. GET /api/teacher/assignment/:assignmentId/student-accuracy
**Get ALL students' accuracy for assignment (class view)**

| Aspect | Details |
|--------|---------|
| **Method** | GET |
| **Auth** | Required |
| **Auth Role** | teacher, admin, superadmin |
| **URL Params** | `:assignmentId` |
| **Purpose** | Teacher views entire class performance |
| **Returns** | Statistics + all student submissions |

**Response Data**:
```json
{
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
    }
  ]
}
```

---

## Updated Endpoint

### POST /api/student/submit-assignment
**Submit assignment with auto-calculated quiz accuracy**

**Request**:
```json
{
  "assignmentId": 3,
  "completionPercentage": 85
}
```

**Response**:
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

## Database Schema

### assignment_submissions table

| Column | Type | Purpose |
|--------|------|---------|
| id | INT | Primary key |
| assignment_id | INT | FK to classroom_assignments |
| student_id | INT | FK to users |
| submission_date | DATETIME | When submitted |
| completion_percentage | INT | % of assignment done (0-100) |
| is_submitted | BOOLEAN | Has submitted flag |
| is_late | BOOLEAN | Late submission flag |
| correct_answers | INT | **NEW**: # questions correct |
| total_questions | INT | **NEW**: Total questions in course |
| quiz_accuracy | DECIMAL(5,2) | **NEW**: Accuracy % (0-100) |
| submitted_at | TIMESTAMP | Auto timestamp |

---

## Code Examples

### JavaScript/Fetch

```javascript
// Get all courses
const response = await fetch('/api/courses/all?page=1&limit=20', {
  headers: { 'Authorization': `Bearer ${token}` }
});
const { data } = await response.json();
console.log(data.courses);

// Get student accuracy
const response = await fetch('/api/student/15/assignment/3/accuracy', {
  headers: { 'Authorization': `Bearer ${token}` }
});
const { data } = await response.json();
console.log(`Accuracy: ${data.quiz_accuracy}%`);

// Get class accuracy
const response = await fetch('/api/teacher/assignment/3/student-accuracy', {
  headers: { 'Authorization': `Bearer ${token}` }
});
const { data } = await response.json();
console.log(`Average: ${data.statistics.averageAccuracy}%`);
```

### cURL

```bash
# Get all courses
curl http://localhost:3000/api/courses/all?page=1 \
  -H "Authorization: Bearer $TOKEN"

# Get student accuracy
curl http://localhost:3000/api/student/15/assignment/3/accuracy \
  -H "Authorization: Bearer $TOKEN"

# Get class accuracy  
curl http://localhost:3000/api/teacher/assignment/3/student-accuracy \
  -H "Authorization: Bearer $TOKEN"
```

---

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Missing required parameters |
| 403 | Access denied / Unauthorized role |
| 404 | Resource not found |
| 500 | Server error |

---

## Response Format

All endpoints return:
```json
{
  "success": true/false,
  "message": "Description of result",
  "data": {
    // Response data
  }
}
```

---

## Error Examples

### Missing Authentication
```
Status: 401
{
  "success": false,
  "message": "No token provided",
  "data": null
}
```

### Unauthorized Access
```
Status: 403
{
  "success": false,
  "message": "Unauthorized access to student accuracy",
  "data": null
}
```

### Resource Not Found
```
Status: 404
{
  "success": false,
  "message": "Assignment not found",
  "data": null
}
```

---

## Key Features

✅ **Pagination**: /api/courses/all supports page/limit for large datasets
✅ **Search**: /api/courses/all supports full-text search
✅ **Authorization**: All endpoints check JWT token + roles
✅ **Privacy**: Students can only view their own data (or teacher/admin can view all)
✅ **Accuracy Calculation**: Auto-calculated from quiz attempt records
✅ **Statistics**: Class-wide analytics with aggregations
✅ **Error Handling**: Comprehensive error messages
✅ **Timestamps**: All submissions tracked with dates

---

**Created**: Session 37B
**Status**: ✅ Ready for Implementation
**Backend File**: `veelearn-backend/server.js`

