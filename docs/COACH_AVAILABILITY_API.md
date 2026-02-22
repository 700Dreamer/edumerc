# EduCoach API Guide v1: Availability & Smart Booking

---

## Base Information
- **Base URL:** `/api/v1/coach/`
- **Authentication:** Bearer Token (JWT) is required for most endpoints.

---

## 1. Coach Availability Management (For Coaches)
These endpoints allow coaches to define and retrieve their recurring weekly working hours. Multiple time ranges per day are supported.

### `GET /api/v1/coach/availability/`
Fetch the logged-in coach's current weekly schedule.
- **Auth:** `TEACHER` (Requires an active `Coach` profile).

**Response (200 OK):**
```json
{
  "coach_id": 1,
  "weekly_schedule": [
    {
      "day_of_week": 1,
      "day_name": "Monday",
      "is_active": true,
      "ranges": [
        { "start": "09:00", "end": "12:00" },
        { "start": "14:00", "end": "17:00" }
      ]
    },
    {
      "day_of_week": 2,
      "day_name": "Tuesday",
      "is_active": false,
      "ranges": []
    }
  ]
}
```

### `PUT /api/v1/coach/availability/`
Update the coach's entire weekly schedule. This is a full replacement (upsert) of their weekly availability.
- **Auth:** `TEACHER` (Requires an active `Coach` profile).

**Request Body:**
```json
{
  "weekly_schedule": [
    {
      "day_of_week": 1,
      "is_active": true,
      "ranges": [
        { "start": "09:00", "end": "12:00" },
        { "start": "14:00", "end": "17:00" }
      ]
    },
    {
      "day_of_week": 2,
      "is_active": false,
      "ranges": []
    }
  ]
}
```

> **IMPORTANT:**
> - All `start` and `end` times must be exactly on the top of the hour (e.g., `"14:00"`, not `"14:15"`).
> - Ranges on the same day cannot overlap.
> - Maximum of 5 active ranges per day.

---

## 2. Smart Slot Generation (For Students)
Students use this endpoint when browsing a coach's calendar. It calculates exact available top-of-the-hour slots based on the coach's active schedule, the requested duration, and any existing bookings on that date.

### `GET /api/v1/coach/tutors/{id}/slots/`
Fetch available start times for a specific date and desired duration.
- **Auth:** Public / Any authenticated user.

**Query Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `date` | Yes | Target date in `YYYY-MM-DD` format. |
| `duration` | Yes | Booking duration in hours (integer between 1-8). |

**Example Request:**
`GET /api/v1/coach/tutors/1/slots/?date=2026-03-25&duration=2`

**Response (200 OK):**
```json
{
  "coach_id": 1,
  "date": "2026-03-25",
  "duration_hours": 2,
  "available_slots": [
    "09:00", 
    "10:00", 
    "14:00", 
    "15:00"
  ]
}
```
*Note: A returned slot like `"09:00"` means the coach is fully available from `09:00` to `11:00` (for a 2-hour session).*

---

## 3. Session Booking & Management (For Students)

### `POST /api/v1/coach/sessions/`
Safely book a 1-on-1 session with a coach. This endpoint uses a database lock (`SELECT FOR UPDATE`) to prevent double-booking race conditions natively.
- **Auth:** `STUDENT` or `PARENT`.

**Request Body:**
```json
{
  "tutor_id": 1,
  "date": "2026-03-25",
  "time": "09:00",
  "duration": 2,
  "note": "Help required with advanced mathematics."
}
```

**Responses:**
- **`201 Created`**: Booking successful.
```json
{
  "booking_id": "BK-FC7245",
  "status": "pending",
  "tutor_name": "Test Teacher",
  "date": "2026-03-25",
  "time": "09:00",
  "end_time": "11:00",
  "duration": 2,
  "total_price": 200.00,
  "note": "Help required with advanced mathematics."
}
```
- **`409 Conflict`**: Target slot was just booked by someone else natively (double booking prevented).
```json
{
  "error": "SLOT_UNAVAILABLE",
  "detail": "The selected slot (09:00 on 2026-03-25) is no longer available. Please choose a different time."
}
```
- **`422 Unprocessable Entity`**: The requested duration exceeds the coach's scheduled block.
- **`400 Bad Request`**: Date is in the past, or time format is invalid.

### `GET /api/v1/coach/sessions/my-bookings/`
Returns all sessions booked by the currently logged-in student user.
- **Auth:** `STUDENT` or `PARENT`.

**Response (200 OK):**
```json
[
  {
    "booking_id": "BK-FC7245",
    "status": "pending",
    "tutor_name": "Test Teacher",
    "date": "2026-03-25",
    "time": "09:00",
    "end_time": "11:00",
    "duration": 2,
    "total_price": 200.00
  }
]
```

---

## 4. Appointments Management (For Coaches)

### `GET /api/v1/coach/appointments/`
Returns all incoming sessions booked against the logged-in coach.
- **Auth:** `TEACHER` (Requires an active `Coach` profile).

**Response (200 OK):**
```json
[
  {
    "booking_id": "BK-FC7245",
    "status": "pending",
    "student_name": "Test Student",
    "student_email": "s@test.com",
    "date": "2026-03-25",
    "time": "09:00",
    "end_time": "11:00",
    "duration": 2,
    "total_price": 200.00,
    "meeting_link": null,
    "note": "Help required with advanced mathematics.",
    "created_at": "2026-02-21T11:45:00Z"
  }
]
```

### `PATCH /api/v1/coach/appointments/{booking_id}/`
Update an appointment's status (e.g., accept the booking and provide a meeting link). Valid statuses are `confirmed`, `completed`, or `cancelled`.
- **Auth:** `TEACHER` (Requires ownership of the session).

**Request Body:**
```json
{
  "status": "confirmed",
  "meeting_link": "https://meet.google.com/abc-xyz"
}
```

**Response (200 OK):**
```json
{
  "booking_id": "BK-FC7245",
  "status": "confirmed",
  "student_name": "Test Student",
  "student_email": "s@test.com",
  "date": "2026-03-25",
  "time": "09:00",
  "end_time": "11:00",
  "duration": 2,
  "total_price": 200.00,
  "meeting_link": "https://meet.google.com/abc-xyz",
  "note": "Help required with advanced mathematics."
}
```

---

## 5. Earnings Dashboard (For Coaches)
Coaches can track their revenue performance including completed, pending, and cashed-out amounts.

### `GET /api/v1/coach/tutors/earnings/`
Fetch the logged-in coach's financial ledger and aggregates.
- **Auth:** `TEACHER` (Requires an active `Coach` profile).

**Response (200 OK):**
```json
{
  "Budget": 120000.0,
  "earning": 150000.0,
  "withdrawn": 30000.0,
  "amount_expected": 45000.0,
  "currency": "UGX",
  "response_obj": [
    {
      "transaction_id": "BK-FC7245",
      "session_id": "BK-FC7245",
      "student_name": "Test Student",
      "amount": "200.00",
      "transaction_type": "EARNING",
      "status": "EARNED",
      "duration": 2,
      "price": "100.00",
      "date": "2026-03-25",
      "created_at": "2026-02-21T18:59:00Z"
    },
    {
      "transaction_id": "W-987654",
      "session_id": null,
      "student_name": null,
      "amount": "30000.00",
      "transaction_type": "WITHDRAWAL",
      "status": "WITHDRAWN",
      "duration": null,
      "price": null,
      "date": "2026-02-20",
      "created_at": "2026-02-20T12:00:00Z"
    }
  ]
}
```

**Field Descriptions:**
- `Budget`: Current available balance (Total Earned - Total Withdrawn).
- `earning`: Historical revenue from all sessions marked as **EARNED**.
- `withdrawn`: Historical funds successfully cashed out.
- `amount_expected`: Revenue from confirmed sessions scheduled for the future (**EXPECTED**).
- `response_obj`: A list of granular ledger entries for every transaction.

