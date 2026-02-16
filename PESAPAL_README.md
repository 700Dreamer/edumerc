# PesaPal UG V3 Integration - Edumerk

This module provides a production-ready integration for PesaPal UG V3 payment processing.

## Configuration

Add the following to your `settings.py`:

```python
PESAPAL_CONSUMER_KEY = 'your_production_key'
PESAPAL_CONSUMER_SECRET = 'your_production_secret'
PESAPAL_IPN_ID = 'your_manually_registered_ipn_id'
PESAPAL_CALLBACK_URL = 'https://your-frontend.com/payment-success'
```

> [!NOTE]
> The `PESAPAL_IPN_ID` must be registered once via the PesaPal dashboard or a one-time script for your production URL.

## API Usage

### 1. Initiate Payment
**Endpoint**: `POST /api/v1/payments/initiate/`  
**Payload**:
```json
{
  "amount": "5000.00",
  "description": "Payment for Math Club"
}
```
**Success Response**:
```json
{
  "redirect_url": "https://pay.pesapal.com/v3/...",
  "merchant_reference": "EDM-XXXX",
  "order_tracking_id": "xxxx-xxxx"
}
```

### 2. IPN Handler
**Endpoint**: `GET /api/v1/ipn/handler/`  
**Purpose**: Internal endpoint for PesaPal to notify your backend of payment status changes. It automatically verifies status and updates your local `Transaction` model.

## Implementation Details

- **Environment**: Automatically switches between Sandbox (`DEBUG=True`) and Production (`DEBUG=False`).
- **Currency**: Hardcoded to `UGX`. Amounts are sent as integers.
- **Models**: Uses the `Transaction` model to keep a local record of all payment attempts.
