# EduCoach API Usage Guide

This guide details how to book coaching sessions and complete payments using PesaPal.

## 1. Book a Session
Students can book a tutor by submitting a POST request with the session details.

**Endpoint**: `POST /api/v1/coach/sessions/`
**Body**:
```json
{
    "coach": 1,
    "date": "2026-03-01",
    "time": "10:00:00",
    "duration": 2,
    "note": "Need help with Calculus"
}
```

- Initial status: `pending`
- The system checks tutor availability before allowing the booking.

---

## 2. Tutor Approval
The tutor (coach) must confirm the booking. Once confirmed, the student receives an email notification with a payment link.

**Email Content**:
> Your booking with [Coach Name] has been confirmed.
> IMPORTANT: Please complete your payment to secure this slot.
> Click here to pay: https://edumerc.up.railway.app/pay-session/[booking_id]

---

## 3. Initiate Payment
When the student clicks the link in their email (or handles the redirect in the frontend), the frontend should call the `initiate-payment-by-booking` endpoint.

**Endpoint**: `POST /api/v1/coach/sessions/initiate-payment-by-booking/{booking_id}/`

**Response**:
```json
{
    "redirect_url": "https://cybqa.pesapal.com/pesapalv3/...",
    "merchant_reference": "EC-PMT-ABC12345",
    "order_tracking_id": "8765-4321-...",
    "booking_id": "BK-XYZ789"
}
```

The frontend should redirect the user to the `redirect_url` to complete the transaction.

---

## 4. Payment Auto-Fulfillment
Once the payment is successful:
1. PesaPal pings our Webhook (IPN).
2. The system automatically updates the `transaction.status` to `COMPLETED`.
3. The linked `CoachingSession.payment_status` is updated to `paid`.

---

## 5. Fields & Statuses
- **Status**: `pending`, `confirmed`, `cancelled`, `completed`.
- **Payment Status**: `pending`, `paid`, `cancelled`.
