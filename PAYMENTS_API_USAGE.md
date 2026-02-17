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

### 2. Cart Checkout & Initiate Payment
Checkout from cart: reads user's Cart, creates Order, and initiates payment in one step.

*   **URL**: `POST /api/v1/payments/cart_checkout/initiate/`
*   **Authentication**: Required (JWT)
*   **Request Body**: `{}` (empty - cart is read from database)
*   **Success Response** (200 OK):
    ```json
    {
        "total": 50000.00,
        "redirect_url": "https://pay.pesapal.com/v3/...",
        "merchant_reference": "EDM-XXXXXX",
        "order_tracking_id": "uuid-tracking-id",
        "order_id": 5
    }
    ```
*   **Error Responses**:
    - `400 Bad Request`: `{"error": "Cart is empty"}` or `{"error": "Cart not found"}`

> **Note**: The cart is **NOT** cleared immediately. It will only be cleared when PesaPal confirms the payment was successful via the IPN callback. If payment fails, the cart remains intact so the user can retry.

### 3. List Transactions
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

### 4. IPN Handler (Internal)
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
