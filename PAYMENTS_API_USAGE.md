# Payments API Usage

This document outlines the API endpoints for the `payments` application, which handles PesaPal UG V3 integration.

## Base URL
`/api/v1/payments/`

## Endpoints

### 1. Initiate a Payment
Starts a new payment process and returns a PesaPal redirect URL.

*   **URL**: `POST /api/v1/payments/initiate/`
*   **Authentication**: Required (JWT)
*   **Request Body**:
    ```json
    {
        "amount": 1000.00,
        "description": "Club Subscription"
    }
    ```
*   **Success Response** (200 OK):
    ```json
    {
        "redirect_url": "https://pay.pesapal.com/v3/...",
        "merchant_reference": "EDM-XXXXXX",
        "order_tracking_id": "uuid-tracking-id"
    }
    ```

### 2. List Transactions
Retrieve a history of all payments made by the authenticated user.

*   **URL**: `GET /api/v1/payments/`
*   **Authentication**: Required (JWT)
*   **Success Response** (200 OK):
    ```json
    [
        {
            "id": "uuid",
            "amount": "1000.00",
            "status": "COMPLETED",
            "merchant_reference": "EDM-XXXXXX",
            "created_at": "2026-02-16T..."
        },
        ...
    ]
    ```

### 3. IPN Handler (Internal)
Used by PesaPal to notify the server of status changes.

*   **URL**: `GET /api/v1/ipn/handler/`
*   **Authentication**: None (Public)
*   **Query Parameters**: `OrderTrackingId`, `OrderMerchantReference`

## Payment Statuses
- `PENDING`: Payment started but not yet completed.
- `COMPLETED`: Payment successfully received.
- `FAILED`: Payment failed or was canceled.
- `REVERSED`: Payment was refunded/reversed.

---
> [!TIP]
> For a detailed guide on how to implement this in the frontend, see [FRONTEND_PESAPAL_GUIDE.md](./FRONTEND_PESAPAL_GUIDE.md).
