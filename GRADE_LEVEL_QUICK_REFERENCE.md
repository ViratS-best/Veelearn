# Grade Level Feature - Quick Reference

## Grade Level Values
- **1-12**: Elementary through Grade 12
- **13**: College level
- **NULL**: Unspecified (optional)

---

## API Endpoints Summary

| Endpoint | Method | New Param | Returns | Filter |
|----------|--------|-----------|---------|--------|
| `/api/courses` | GET | `?grade_level=9` | ✅ grade_level | ✅ Yes |
| `/api/courses/all` | GET | `?grade_level=9` | ✅ grade_level | ✅ Yes |
| `/api/courses/:id` | GET | - | ✅ grade_level | - |
| `/api/courses` | POST | `grade_level: 9` | - | - |
| `/api/courses/:id` | PUT | `grade_level: 9` | - | - |
| `/api/users/:userId/courses` | GET | - | ✅ grade_level | - |
| `/api/admin/courses/pending` | GET | - | ✅ grade_level | - |
| `/api/admin/courses/:id/preview` | GET | - | ✅ grade_level | - |

---

## Example Requests

### Create Course with Grade Level
```bash
curl -X POST http://localhost:3000/api/courses \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Physics 101",
    "description": "Introduction to Physics",
    "content": "...",
    "grade_level": 9,
    "status": "draft"
  }'
```

### Update Course Grade Level
```bash
curl -X PUT http://localhost:3000/api/courses/42 \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Physics 101",
    "grade_level": 10
  }'
```

### Get Courses for Grade 5
```bash
curl -X GET "http://localhost:3000/api/courses?grade_level=5" \
  -H "Authorization: Bearer TOKEN"
```

### Get Grade 9 Courses with Search
```bash
curl -X GET "http://localhost:3000/api/courses/all?search=physics&grade_level=9&page=1&limit=10" \
  -H "Authorization: Bearer TOKEN"
```

---

## Validation Rules

```javascript
// Grade level must be:
✅ Integer between 1-13 (inclusive)
✅ Optional (can be null/undefined)
✅ Returned in all course responses

❌ String numbers auto-converted
❌ Decimals rejected
❌ Outside 1-13 range rejected
❌ Required field? NO (optional)
```

**Error Response** (400):
```json
{
  "success": false,
  "message": "Grade level must be an integer between 1 and 13 (13 = College)"
}
```

---

## Database Schema

```sql
-- Column added to courses table
grade_level INT CHECK (grade_level >= 1 AND grade_level <= 13)

-- Index for fast filtering
INDEX idx_grade_level (grade_level)

-- Constraint ensures valid range
CHECK (grade_level >= 1 AND grade_level <= 13)
```

---

## Frontend Integration Points

### 1. Grade Level Dropdown
```html
<select name="grade_level" id="gradeLevel">
  <option value="">Select Grade Level (Optional)</option>
  <option value="1">Grade 1</option>
  <option value="2">Grade 2</option>
  <!-- ... -->
  <option value="12">Grade 12</option>
  <option value="13">College</option>
</select>
```

### 2. Display Grade Level Badge
```javascript
function getGradeLevelLabel(grade) {
  if (grade >= 1 && grade <= 12) return `Grade ${grade}`;
  if (grade === 13) return 'College';
  return 'All Grades';
}
```

### 3. Filter by Grade
```javascript
// In course search/filter UI
const gradeLevelFilter = document.querySelector('#gradeLevel').value;
const url = `/api/courses?grade_level=${gradeLevelFilter}`;
fetch(url, { headers: { 'Authorization': `Bearer ${token}` } });
```

---

## Response Examples

### Course Object (now includes grade_level)
```json
{
  "id": 42,
  "title": "Physics 101",
  "description": "Introduction to Physics",
  "status": "approved",
  "grade_level": 9,
  "creator_id": 5,
  "creator_email": "teacher@example.com"
}
```

### Filtered List Response
```bash
GET /api/courses?grade_level=5
```
Returns only courses where `grade_level = 5`

---

## Key Features

✅ **Validated**: 1-13 range checked on all inputs  
✅ **Optional**: Existing courses without grade_level continue to work  
✅ **Indexed**: Fast filtering with database index  
✅ **Searchable**: Combine with search parameter  
✅ **Paginated**: Works with pagination on /api/courses/all  
✅ **Backwards Compatible**: No breaking changes  

---

## Migration Info

**Auto-Migration**: Runs on server startup
- ✅ Checks if column exists
- ✅ Adds if missing
- ✅ Works on new & existing databases
- ✅ No manual SQL needed

---

## Testing Checklist

- [ ] Create course with grade_level
- [ ] Update course with grade_level
- [ ] Get courses filtered by grade_level
- [ ] Search with grade_level filter
- [ ] Display grade_level in UI
- [ ] Handle null grade_level gracefully
- [ ] Test validation (invalid range)
- [ ] Check backwards compatibility

---

_Last Updated: February 26, 2026_
