# BookClick API Documentation

## Base URL
```
http://localhost:8000/api/
```

## Authentication

### Register
```http
POST /api/auth/register/
Content-Type: application/json

{
  "email": "user@university.edu",
  "username": "username",
  "password": "password123",
  "password_confirm": "password123",
  "first_name": "John",
  "last_name": "Doe",
  "role": "STUDENT",
  "department": "Computer Science"
}
```

### Login
```http
POST /api/auth/login/
Content-Type: application/json

{
  "email": "user@university.edu",
  "password": "password123"
}

Response:
{
  "user": {...},
  "token": "your-auth-token",
  "message": "Login successful"
}
```

### Logout
```http
POST /api/auth/logout/
Authorization: Token your-auth-token
```

### Get Profile
```http
GET /api/auth/profile/
Authorization: Token your-auth-token
```

## Rooms

### List All Rooms
```http
GET /api/rooms/
Authorization: Token your-auth-token

Query Parameters:
- room_type: CLASSROOM, LABORATORY, AUDITORIUM, etc.
- building: Building name
- status: AVAILABLE, MAINTENANCE, UNAVAILABLE
- capacity: Minimum capacity
- search: Search term
- has_projector: true/false
- has_wifi: true/false
- has_computer: true/false
```

### Get Room Details
```http
GET /api/rooms/{id}/
Authorization: Token your-auth-token
```

### Create Room (Admin only)
```http
POST /api/rooms/
Authorization: Token your-auth-token
Content-Type: application/json

{
  "name": "Room 101",
  "room_type": "CLASSROOM",
  "building": "Main Building",
  "floor": "1st Floor",
  "capacity": 30,
  "description": "Standard classroom",
  "status": "AVAILABLE",
  "has_projector": true,
  "has_whiteboard": true,
  "has_wifi": true
}
```

### Update Room (Admin only)
```http
PUT /api/rooms/{id}/
Authorization: Token your-auth-token
Content-Type: application/json

{
  "name": "Room 101 Updated",
  "capacity": 35,
  ...
}
```

### Delete Room (Admin only)
```http
DELETE /api/rooms/{id}/
Authorization: Token your-auth-token
```

## Bookings

### List Bookings
```http
GET /api/bookings/
Authorization: Token your-auth-token

Query Parameters:
- status: PENDING, APPROVED, REJECTED, CANCELLED
- room: Room ID
- date: YYYY-MM-DD
- start_date: YYYY-MM-DD
- end_date: YYYY-MM-DD
- upcoming: true (filter upcoming bookings)
```

### Get Booking Details
```http
GET /api/bookings/{id}/
Authorization: Token your-auth-token
```

### Create Booking
```http
POST /api/bookings/
Authorization: Token your-auth-token
Content-Type: application/json

{
  "room": 1,
  "title": "Math Class",
  "description": "Advanced mathematics lecture",
  "date": "2025-10-25",
  "start_time": "09:00",
  "end_time": "11:00",
  "number_of_attendees": 25
}
```

### Update Booking
```http
PUT /api/bookings/{id}/
Authorization: Token your-auth-token
Content-Type: application/json

{
  "title": "Updated Title",
  "date": "2025-10-26",
  ...
}
```

### Cancel Booking
```http
POST /api/bookings/{id}/cancel/
Authorization: Token your-auth-token
```

### Approve Booking (Admin only)
```http
POST /api/bookings/{id}/approve/
Authorization: Token your-auth-token
```

### Reject Booking (Admin only)
```http
POST /api/bookings/{id}/reject/
Authorization: Token your-auth-token
Content-Type: application/json

{
  "action": "reject",
  "rejection_reason": "Room not available"
}
```

### Check Availability
```http
GET /api/bookings/check_availability/
Authorization: Token your-auth-token

Query Parameters:
- room_id: Room ID
- date: YYYY-MM-DD
- start_time: HH:MM
- end_time: HH:MM

Response:
{
  "available": true/false,
  "conflicting_bookings": [...]
}
```

### Get My Bookings
```http
GET /api/bookings/my_bookings/
Authorization: Token your-auth-token
```

### Get Pending Bookings (Admin only)
```http
GET /api/bookings/pending/
Authorization: Token your-auth-token
```

## Response Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Permission denied
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Error Response Format
```json
{
  "error": "Error message",
  "details": {...}
}
```

## Pagination

List endpoints support pagination:
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/rooms/?page=2",
  "previous": null,
  "results": [...]
}
```

## Filtering & Search

Most list endpoints support:
- **Filtering:** `?field=value`
- **Search:** `?search=term`
- **Ordering:** `?ordering=field` or `?ordering=-field` (descending)

## Examples with cURL

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@university.edu","password":"admin123"}'
```

### List Rooms
```bash
curl -X GET http://localhost:8000/api/rooms/ \
  -H "Authorization: Token YOUR_TOKEN"
```

### Create Booking
```bash
curl -X POST http://localhost:8000/api/bookings/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "room": 1,
    "title": "Meeting",
    "date": "2025-10-25",
    "start_time": "14:00",
    "end_time": "16:00",
    "number_of_attendees": 10
  }'
```

## Rate Limiting

Currently no rate limiting is implemented. For production, consider adding rate limiting.

## Versioning

Current API version: v1
Base URL includes version: `/api/v1/` (optional)

## Support

For API support: api-support@university.edu
