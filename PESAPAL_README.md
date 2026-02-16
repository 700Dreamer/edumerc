# PesaPal UG V3 Integration - Edumerk

This module provides a complete integration for PesaPal UG V3 payment processing, supporting Cards and Mobile Money (MTN & Airtel).

## Key Components

- **App**: `payments`
- **Service Layer**: `payments/pesapal_service.py` (Handles Auth, IPN, and Order Submission)
- **Models**: 
  - `Transaction`: Tracks payment amount, user, status, and tracking IDs.
  - `PesaPalIPN`: Stores registered IPN URLs and IDs.

## API Endpoints

### 1. Initiate Payment
**Endpoint**: `POST /api/v1/payments/initiate/`  
**Auth**: Required (JWT/Session)  
**Payload**:
```json
{
  "amount": "1000.00",
  "description": "Subscription for Math Club"
}
```
**Response**: returns a `redirect_url`. Redirect the user to this URL to complete payment.

### 2. IPN Handler (Internal)
**Endpoint**: `GET /api/v1/ipn/handler/`  
**Purpose**: Receives server-to-server notifications from PesaPal to update transaction status.

## Production Setup

Add the following credentials to your `config/settings.py` or environment variables:

```python
PESAPAL_CONSUMER_KEY = 'your_live_key'
PESAPAL_CONSUMER_SECRET = 'your_live_secret'
PESAPAL_CALLBACK_URL = 'https://your-frontend.com/payment-success'
```

## Payment Flow

1.  **Backend**: `initiate` endpoint creates a `PENDING` transaction.
2.  **PesaPal Service**: Registers the IPN URL and submits the order.
3.  **Frontend**: User is redirected to PesaPal's secure checkout.
4.  **User**: Selects Payment Method (e.g., MTN Mobile Money) and approves STK Push.
5.  **PesaPal**: Hits the IPN `handler` on your backend.
6.  **Backend**: Verifies status with PesaPal and updates `Transaction` to `COMPLETED`.

## Testing
Use the provided `test_pesapal.py` script to verify your credentials:
```bash
python test_pesapal.py
```
