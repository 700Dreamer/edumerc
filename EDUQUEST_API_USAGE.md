# EduQuest Order API Usage Guide

This guide details how to create and pay for EduQuest Material Orders.

## Base URL
`/api/v1/quest/orders/`

## Authentication
All endpoints require a valid JWT token:
```
Authorization: Bearer <token>
```

---

## 1. Create a Material Order (PENDING)
When a user finishes selecting materials, submit the payload to the backend. The backend will automatically link the order to the logged-in user, set its status to `PENDING`, and generate a tracked `reference` ID.

**Endpoint**: `POST /api/v1/quest/orders/`
**Auth**: Required

**Example Payload**:
```json
{
  "material": 1,
  "session": "MID",
  "total_sets": 25,
  "estimated_amount": 125000.00,
  "school": {
    "name": "St. Mary's High School",
    "representative": "John Doe",
    "location": "Kampala Central",
    "address": "123 School Road, P.O Box 456",
    "phone": "+256 700 123456",
    "email": "info@stmarys.edu.ug",
    "delivery_date": "2026-03-01"
  },
  "levels": [
    {
      "level": "P.4",
      "subjects": [
        "Mathematics",
        "Science",
        "SST",
        "English"
      ]
    }
  ]
}
```

**Successful Response Overview**:
The backend returns your entire order, including a guaranteed `reference` ID.
```json
{
    "id": 15,
    "reference": "EQ-B5F1G7C3",
    "username": "johndoe",
    "status": "PENDING",
    ...
}
```

---

## 2. Admin Approval
By default, newly created orders have a `PENDING` status. 
An administrator must review the order manually on the **Django Admin (Unfold)** interface, update/verify the `estimated_amount`, and update the order Status to **`APPROVED`**.

---

## 3. Initiate Payment
Once the order status is `APPROVED`, the user should be prompted to pay. Hitting this endpoint will build a protected PesaPal checkout token and give you a frame URL.

**Endpoint**: `POST /api/v1/quest/orders/{id}/initiate-payment/`
**Auth**: Required

**Example Payload**:
*(Empty payload required)*
```json
{}
```

**Important**: This will ONLY work if the order is `APPROVED`.

**Successful Response Overview**:
Redirect the user's browser or iframe to the `redirect_url` to securely capture their transaction details.
```json
{
    "redirect_url": "https://pay.pesapal.com/iframe/PesapalIframe3/Index?OrderTrackingId=...",
    "merchant_reference": "EQ-PMT-A1B2C3D4",
    "order_tracking_id": "7abc-1234-xyz",
    "order_id": 15
}
```

---

## 4. Payment Auto-Fulfillment via IPN
Once the user pays on the PesaPal Checkout UI:
1. PesaPal silently pings Edumerk's Webhook URL (`/api/v1/payments/ipn-handler/`).
2. Edumerk automatically identifies the linked `MaterialOrder`.
3. Edumerk flips the `MaterialOrder.status` to **`PAID`** (or `CANCELLED` if it fails).
4. The user is redirected back to your frontend! (e.g., `/payment-success`).

**Note on Frontend Polling**:
On your frontend `/payment-success` page, you should poll or fetch the order details via `GET /api/v1/quest/orders/{id}/` until you see `"status": "PAID"`.
