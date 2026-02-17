# Frontend Implementation Guide: PesaPal V3

This guide explains how to integrate the PesaPal payment flow into your frontend (React, Vue, mobile, etc.).

## 1. Initiate Payment
When the user clicks "Pay", call your backend's initiation endpoint.

**Endpoint**: `POST /api/v1/payments/initiate/`  
**Headers**: `Authorization: Bearer <your_jwt_token>`  
**Payload**:
```json
{
  "amount": 5000,
  "description": "Subscription for Math Club"
}
```

### Response Handling
The backend will return a `redirect_url`. You must redirect the user's browser to this URL.

```javascript
// Example using fetch in React/JS
const handlePayment = async () => {
    const response = await fetch('/api/v1/payments/initiate/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify({ amount: 5000, description: 'Math Club' })
    });
    
    const data = await response.json();
    if (data.redirect_url) {
        // Redirection to PesaPal Checkout
        window.location.href = data.redirect_url;
    }
};
```

## 2. Handling the Return (Callback)
After the user pays on PesaPal, they will be redirected back to the `PESAPAL_CALLBACK_URL` defined in the backend `settings.py`.

**PesaPal will append tracking IDs to your URL:**
`https://your-frontend.com/payment-success?OrderTrackingId=xxx-xxx&OrderMerchantReference=EDM-XXXX`

### Success/Failure Page
On this page, you should show a "Processing..." or "Checking Status..." spinner. 

**Wait!** Do not assume the payment succeeded just because the user reached this page. You must verify it with the backend.

## 3. Verifying Status
Since the backend updates the transaction status automatically via IPN, you should simply poll your backend to see if the transaction is now `COMPLETED`.

**Endpoint**: `GET /api/v1/payments/` (or a specific detail view for the transaction)

```javascript
// Pseudocode for polling
const checkStatus = setInterval(async () => {
    const res = await fetch(`/api/v1/payments/?ref=${merchantRef}`);
    const transaction = await res.json();
    
    if (transaction.status === 'COMPLETED') {
        clearInterval(checkStatus);
        alert("Payment Successful!");
    } else if (transaction.status === 'FAILED') {
        clearInterval(checkStatus);
        alert("Payment Failed.");
    }
}, 3000); // Check every 3 seconds
```

## Summary Flow Chart
1. **Frontend** → calls `POST /initiate/`
2. **Backend** → returns `redirect_url`
3. **Frontend** → redirects **User** to PesaPal
4. **User** → pays on PesaPal UI
5. **PesaPal** → redirects **User** back to your **Frontend** Success Page
6. **Backend (Background)** → Receives IPN from PesaPal and updates DB
7. **Frontend** → Checks backend for `status === 'COMPLETED'`
8. **Frontend** → Shows "Thank you!"
