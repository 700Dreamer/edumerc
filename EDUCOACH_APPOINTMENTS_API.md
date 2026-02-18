# EduCoach — Coach Appointments API

This document covers the two endpoints that allow a **coach/tutor** to manage
sessions booked against them.

> **Base URL prefix:** `/api/v1/coach/sessions/`  
> **Authentication:** All endpoints require `Authorization: Bearer <access_token>`  
> **Access guard:** The authenticated user must have `is_coach: true`

---

## 1. View My Appointments

Retrieve all coaching sessions that students have booked with the logged-in coach,
ordered by most recent first.

- **URL:** `/api/v1/coach/sessions/my-appointments/`
- **Method:** `GET`
- **Permission:** Authenticated · `is_coach = true`

### Success Response — `200 OK`

```json
[
  {
    "booking_id": "BK-12",
    "status": "pending",
    "student_name": "John Mukasa",
    "student_email": "john@example.com",
    "date": "2026-03-20",
    "time": "14:30:00",
    "duration": 1,
    "total_price": "45000.00",
    "meeting_link": null,
    "note": "I need help with the Circulatory System.",
    "created_at": "2026-02-18T18:00:00Z"
  }
]
```

### Error Responses

| Status | Reason |
| ------ | ------ |
| `401 Unauthorized` | No token / expired token |
| `403 Forbidden` | Authenticated user is not a coach (`is_coach = false`) |
| `404 Not Found` | Coach profile does not exist for this user |

---

## 2. Update a Booking Status

Allows the coach to **confirm**, **cancel**, or **complete** a specific session.
An optional `meeting_link` can be provided when confirming.

- **URL:** `/api/v1/coach/sessions/{id}/update-status/`
- **Method:** `PATCH`
- **Permission:** Authenticated · `is_coach = true` · session must belong to this coach

### Request Body

| Field | Type | Required | Description |
| ----- | ---- | -------- | ----------- |
| `status` | `string` | ✅ Yes | One of `"confirmed"`, `"cancelled"`, `"completed"` |
| `meeting_link` | `string (URL)` | ❌ No | Video call link (e.g. Zoom / Google Meet). Set when confirming. |

```json
{
  "status": "confirmed",
  "meeting_link": "https://meet.google.com/xyz-abc-def"
}
```

### Success Response — `200 OK`

Returns the full coach view of the updated session:

```json
{
  "booking_id": "BK-12",
  "status": "confirmed",
  "student_name": "John Mukasa",
  "student_email": "john@example.com",
  "date": "2026-03-20",
  "time": "14:30:00",
  "duration": 1,
  "total_price": "45000.00",
  "meeting_link": "https://meet.google.com/xyz-abc-def",
  "note": "I need help with the Circulatory System.",
  "created_at": "2026-02-18T18:00:00Z"
}
```

### Error Responses

| Status | Reason |
| ------ | ------ |
| `400 Bad Request` | Invalid `status` value, or session is already `cancelled` / `completed` |
| `401 Unauthorized` | No token / expired token |
| `403 Forbidden` | Authenticated user is not a coach (`is_coach = false`) |
| `404 Not Found` | Session not found, or it does not belong to this coach |

---

## Status Transition Rules

```
pending ──► confirmed
pending ──► cancelled
confirmed ──► completed
confirmed ──► cancelled

cancelled ──✖  (terminal — no further updates allowed)
completed ──✖  (terminal — no further updates allowed)
```

> Attempting to update a session that is already `cancelled` or `completed`
> will return a `400 Bad Request` with a descriptive error message.

---

## Why `PATCH`?

`PATCH` is used because the coach is updating **specific fields only** (`status`,
optionally `meeting_link`) on an existing session — not replacing the whole
resource. `PUT` would require sending the entire session object, which is
unnecessary here.
