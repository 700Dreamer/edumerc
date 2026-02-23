# Coach Earnings Ledger API Usage Guide

This guide details how coaches can track their earnings, expected income, and withdrawals using the EduCoach Ledger system.

## Base URL
`/api/v1/coach/earnings/`

## Authentication
All endpoints require a valid JWT token from a user with a **Coach profile**.
```
Authorization: Bearer <token>
```

---

## 1. View Earnings Summary & History
Retrieves the coach's current balance, total earnings, expected income, and a list of recent transactions.

**Endpoint**: `GET /api/v1/coach/earnings/`
**Auth**: Required (Coach only)

### Response Overview
| Field | Description |
| :--- | :--- |
| `Budget` | Current withdrawable balance (Earned - Withdrawn). |
| `earning` | Total amount from all `COMPLETED` sessions. |
| `withdrawn` | Total amount successfully withdrawn by the coach. |
| `amount_expected` | Income from upcoming `PENDING` or `CONFIRMED` sessions. |
| `currency` | The currency code (default: `UGX`). |
| `response_obj` | A list of recent ledger transactions. |

### Example Response
```json
{
    "Budget": 150000.00,
    "earning": 200000.00,
    "withdrawn": 50000.00,
    "amount_expected": 75000.00,
    "currency": "UGX",
    "response_obj": [
        {
            "transaction_id": "BK-A1B2C3",
            "session_id": "BK-A1B2C3",
            "student_name": "Jane Smith",
            "amount": "50000.00",
            "transaction_type": "EARNING",
            "status": "EARNED",
            "duration": 2,
            "price": "25000.00",
            "date": "2026-02-20",
            "created_at": "2026-02-20T10:00:00Z"
        },
        {
            "transaction_id": "WD-998877",
            "session_id": null,
            "student_name": null,
            "amount": "50000.00",
            "transaction_type": "WITHDRAWAL",
            "status": "WITHDRAWN",
            "duration": null,
            "price": null,
            "date": "2026-02-21",
            "created_at": "2026-02-21T15:30:00Z"
        }
    ]
}
```

---

## 2. Ledger Transaction Statuses
The ledger automatically synchronizes with session and payment events.

| Status | Meaning |
| :--- | :--- |
| `EXPECTED` | Session is booked/confirmed but not yet done. |
| `EARNED` | Session is marked as `COMPLETED`. Funds move to Budget. |
| `WITHDRAWN` | A withdrawal request was successfully processed. |
| `CANCELLED` | The session was cancelled; no earnings will be received. |

---

## 3. Automation Details (Internal)
- **Automatic Booking Sync**: Whenever a student books a session or a coach confirms it, a `CoachEarnings` record is created/updated with status `EXPECTED`.
- **Completion Trigger**: When a coach marks a session as `COMPLETED`, the ledger status flips to `EARNED`, updating the coach's `Budget`.
- **Withdrawal Sync**: When a withdrawal request in the `payments` app is marked as `COMPLETED`, it automatically creates a `WITHDRAWAL` entry in the coach's ledger.
