# Course Likes API Endpoints - Complete Reference

**Version**: 1.0
**Date**: February 26, 2026
**Status**: ✅ Ready for Use

---

## Summary

**Total Endpoints**: 5 (4 new + 1 modified)
**Authentication**: Required on all endpoints (Bearer token)
**Base URL**: `http://localhost:3000/api`

---

## Endpoint List

| Method | Endpoint | Purpose | Status |
|--------|----------|---------|--------|
| POST | `/courses/:id/like` | Like a course | ✅ NEW |
| DELETE | `/courses/:id/like` | Unlike a course | ✅ NEW |
| GET | `/courses/:id/likes` | Get like count | ✅ NEW |
| GET | `/courses/:id/liked` | Check if user liked | ✅ NEW |
| GET | `/courses?sort=X` | Get courses with sorting | ✅ MODIFIED |

---

## 1. POST /api/courses/:id/like

**Purpose**: Add a like from current user to a course

**Method**: `POST`

**URL Path**: `/api/courses/5/like`

**Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

**Request Body**: Empty (no body needed)

**Success Response (200 OK)**:
```json
{
  "success": true,
  "message": "Course liked successfully",
  "data": {
    "liked": true
  }
}
```

**Error Response (400 Bad Request)**:
```json
{
  "success": false,
  "message": "You have already liked this course",
  "data": null
}
```

**Error Response (500 Server Error)**:
```json
{
  "success": false,
  "message": "Server error liking course",
  "data": null
}
```

**What Happens**:
1. ✅ Inserts record into `course_likes` table
2. ✅ Increments `like_count` in `courses` table
3. ✅ Returns success response
4. ✅ UNIQUE constraint prevents duplicate likes

**cURL Example**:
```bash
curl -X POST http://localhost:3000/api/courses/5/like \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

**JavaScript Example**:
```javascript
const response = await fetch('http://localhost:3000/api/courses/5/like', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('token')}`,
    'Content-Type': 'application/json'
  }
});
const result = await response.json();
console.log(result.data.liked); // true
```

---

## 2. DELETE /api/courses/:id/like

**Purpose**: Remove a like from current user on a course

**Method**: `DELETE`

**URL Path**: `/api/courses/5/like`

**Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Request Body**: Empty (no body needed)

**Success Response (200 OK)**:
```json
{
  "success": true,
  "message": "Course unliked successfully",
  "data": {
    "liked": false
  }
}
```

**Error Response (400 Bad Request)**:
```json
{
  "success": false,
  "message": "You have not liked this course",
  "data": null
}
```

**Error Response (500 Server Error)**:
```json
{
  "success": false,
  "message": "Server error unliking course",
  "data": null
}
```

**What Happens**:
1. ✅ Deletes record from `course_likes` table
2. ✅ Decrements `like_count` in `courses` table
3. ✅ Validates record exists before deleting
4. ✅ Returns success response

**cURL Example**:
```bash
curl -X DELETE http://localhost:3000/api/courses/5/like \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**JavaScript Example**:
```javascript
const response = await fetch('http://localhost:3000/api/courses/5/like', {
  method: 'DELETE',
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('token')}`
  }
});
const result = await response.json();
console.log(result.data.liked); // false
```

---

## 3. GET /api/courses/:id/likes

**Purpose**: Get total like count for a specific course

**Method**: `GET`

**URL Path**: `/api/courses/5/likes`

**Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Query Parameters**: None

**Success Response (200 OK)**:
```json
{
  "success": true,
  "message": "Like count fetched successfully",
  "data": {
    "like_count": 42
  }
}
```

**Error Response (500 Server Error)**:
```json
{
  "success": false,
  "message": "Server error fetching like count",
  "data": null
}
```

**What Happens**:
1. ✅ Queries `COUNT(*)` from `course_likes` table
2. ✅ Filtered by course_id
3. ✅ Returns total count
4. ✅ Fast lookup with index

**Note**: This endpoint doesn't require the user to have liked the course themselves. It just returns the total count.

**cURL Example**:
```bash
curl http://localhost:3000/api/courses/5/likes \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**JavaScript Example**:
```javascript
const response = await fetch('http://localhost:3000/api/courses/5/likes', {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('token')}`
  }
});
const result = await response.json();
console.log(`Course has ${result.data.like_count} likes`); // Course has 42 likes
```

---

## 4. GET /api/courses/:id/liked

**Purpose**: Check if current user has liked a specific course

**Method**: `GET`

**URL Path**: `/api/courses/5/liked`

**Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Query Parameters**: None

**Success Response (200 OK) - Already Liked**:
```json
{
  "success": true,
  "message": "Like status fetched successfully",
  "data": {
    "is_liked": true
  }
}
```

**Success Response (200 OK) - Not Liked**:
```json
{
  "success": true,
  "message": "Like status fetched successfully",
  "data": {
    "is_liked": false
  }
}
```

**Error Response (500 Server Error)**:
```json
{
  "success": false,
  "message": "Server error checking like status",
  "data": null
}
```

**What Happens**:
1. ✅ Checks if record exists in `course_likes` table
2. ✅ Filtered by course_id AND user_id
3. ✅ Returns true if found, false if not found
4. ✅ User-specific to the authenticated user

**cURL Example**:
```bash
curl http://localhost:3000/api/courses/5/liked \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**JavaScript Example**:
```javascript
const response = await fetch('http://localhost:3000/api/courses/5/liked', {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('token')}`
  }
});
const result = await response.json();
if (result.data.is_liked) {
  console.log("You liked this course!");
} else {
  console.log("You haven't liked this course");
}
```

---

## 5. GET /api/courses?sort=X

**Purpose**: Get all courses with optional sorting by likes

**Method**: `GET`

**URL Path**: `/api/courses?sort=most_liked`

**Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Query Parameters**:

| Parameter | Values | Default | Description |
|-----------|--------|---------|-------------|
| sort | newest, most_liked, trending, popular | newest | Sort order for courses |

**Sort Options**:

| Value | Sorting Logic | Use Case |
|-------|---------------|----------|
| `newest` | `ORDER BY created_at DESC` | Show newest courses first |
| `most_liked` | `ORDER BY like_count DESC` | Show most liked courses |
| `trending` | `ORDER BY (like_count / DATEDIFF(NOW(), created_at) + 1) DESC` | Show trending (likes per day) |
| `popular` | `ORDER BY like_count DESC` | Show most popular courses |

**Success Response (200 OK)**:
```json
{
  "success": true,
  "message": "Courses fetched successfully",
  "data": [
    {
      "id": 5,
      "title": "Advanced Physics",
      "description": "Learn advanced physics concepts",
      "content": "...",
      "blocks": [...],
      "creator_id": 2,
      "status": "approved",
      "is_paid": false,
      "shells_cost": 50,
      "creation_time": 3600,
      "like_count": 42,
      "creator_email": "teacher@example.com",
      "is_liked": true
    },
    {
      "id": 3,
      "title": "Basic Chemistry",
      "description": "Introduction to chemistry",
      "content": "...",
      "blocks": [...],
      "creator_id": 1,
      "status": "approved",
      "is_paid": false,
      "shells_cost": 50,
      "creation_time": 1800,
      "like_count": 28,
      "creator_email": "prof@example.com",
      "is_liked": false
    }
  ]
}
```

**Error Response (500 Server Error)**:
```json
{
  "success": false,
  "message": "Server error fetching courses",
  "data": null
}
```

**New Fields in Response**:

| Field | Type | Description |
|-------|------|-------------|
| `like_count` | INT | Total number of likes for this course |
| `is_liked` | BOOLEAN | Whether current user has liked this course |

**What Happens**:
1. ✅ Queries all courses with status='approved' or creator_id=current_user
2. ✅ JOINs with `course_likes` to get is_liked status
3. ✅ Calculates like_count from courses table
4. ✅ Orders by selected sort parameter
5. ✅ Returns all courses with like information

**cURL Examples**:

Get newest courses:
```bash
curl "http://localhost:3000/api/courses?sort=newest" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Get most liked courses:
```bash
curl "http://localhost:3000/api/courses?sort=most_liked" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Get trending courses:
```bash
curl "http://localhost:3000/api/courses?sort=trending" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**JavaScript Example**:
```javascript
// Get most liked courses
const response = await fetch('http://localhost:3000/api/courses?sort=most_liked', {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('token')}`
  }
});
const result = await response.json();

result.data.forEach(course => {
  console.log(`${course.title}: ${course.like_count} likes (liked: ${course.is_liked})`);
});
```

---

## Common Patterns

### Workflow: User Likes a Course

```javascript
// 1. User clicks like button
async function likeButton_click() {
  // 2. Send POST request
  const likeResponse = await fetch(`/api/courses/5/like`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` }
  });
  const likeResult = await likeResponse.json();
  
  if (!likeResult.success) {
    alert('Error: ' + likeResult.message); // Already liked?
    return;
  }
  
  // 3. Get updated count
  const countResponse = await fetch(`/api/courses/5/likes`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  const countResult = await countResponse.json();
  
  // 4. Update UI
  likeButton.textContent = `❤️ ${countResult.data.like_count}`;
  likeButton.style.background = '#ec4899';
}
```

### Workflow: Load Sorted Courses

```javascript
// 1. User selects sort option
async function sortDropdown_change(sortBy) {
  // 2. Send GET request with sort parameter
  const response = await fetch(`/api/courses?sort=${sortBy}`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  const result = await response.json();
  
  // 3. Display courses in new order
  result.data.forEach(course => {
    displayCourse(course); // Show with like_count and is_liked
  });
}
```

### Workflow: Initialize Like Button

```javascript
// 1. Load if user liked this course
async function initializeLikeButton(courseId, buttonElement) {
  // 2. Check current like status
  const statusResponse = await fetch(`/api/courses/${courseId}/liked`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  const statusResult = await statusResponse.json();
  const isLiked = statusResult.data.is_liked;
  
  // 3. Get current like count
  const countResponse = await fetch(`/api/courses/${courseId}/likes`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  const countResult = await countResponse.json();
  const likeCount = countResult.data.like_count;
  
  // 4. Update button UI
  const icon = isLiked ? '❤️' : '🤍';
  buttonElement.textContent = `${icon} ${likeCount}`;
  buttonElement.style.background = isLiked ? '#ec4899' : '#475569';
}
```

---

## Response Format

All endpoints follow the standard API response format:

```json
{
  "success": true,
  "message": "Human readable message",
  "data": {
    // Endpoint-specific data
  }
}
```

**Fields**:
- `success` (BOOLEAN): Whether request succeeded
- `message` (STRING): Human-readable message
- `data` (OBJECT or ARRAY or NULL): Response data

---

## Error Handling

All errors return appropriate HTTP status codes:

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | Like added successfully |
| 400 | Bad Request | Already liked, not liked, invalid input |
| 401 | Unauthorized | Invalid or missing token |
| 403 | Forbidden | Access denied |
| 500 | Server Error | Database error |

**Always check `response.ok` or `result.success`**:

```javascript
const response = await fetch(url, options);
if (!response.ok) {
  const error = await response.json();
  console.error('Error:', error.message);
  return;
}

const result = await response.json();
if (!result.success) {
  console.error('API Error:', result.message);
  return;
}

// Success - use result.data
```

---

## Rate Limiting

These endpoints are subject to the global rate limit:
- **50 requests per minute** per user
- Limits reset every minute

---

## Performance Considerations

### Fast Endpoints (< 10ms)
- POST `/courses/:id/like` - Single INSERT
- DELETE `/courses/:id/like` - Single DELETE
- GET `/courses/:id/liked` - Indexed lookup

### Medium Speed (10-50ms)
- GET `/courses/:id/likes` - COUNT query with index

### Slower Endpoints (50-200ms)
- GET `/courses?sort=X` - Full course scan with JOINs

**Optimization Tips**:
1. Cache like status on frontend
2. Batch update like counts
3. Use indexed columns for filtering
4. Don't call GET /likes repeatedly

---

## Testing with Postman

### Setup

1. Create collection: "Veelearn - Likes"
2. Set variable `{{token}}` = your Bearer token
3. Set variable `{{courseId}}` = test course ID

### Test Requests

```
POST {{base_url}}/courses/{{courseId}}/like
DELETE {{base_url}}/courses/{{courseId}}/like
GET {{base_url}}/courses/{{courseId}}/likes
GET {{base_url}}/courses/{{courseId}}/liked
GET {{base_url}}/courses?sort=most_liked
```

---

## Changelog

### Version 1.0 (Feb 26, 2026)
- ✅ Initial release
- ✅ 4 new endpoints
- ✅ 1 modified endpoint
- ✅ Full sorting support
- ✅ User-specific like tracking

---

**Documentation Complete**
**Ready for: Integration & Testing**
**Last Updated: February 26, 2026**
