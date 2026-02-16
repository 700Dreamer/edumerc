import os
import django
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.core.cache import cache

def test_pesapal_flow():
    """
    Tests the PesaPal payment initiation flow.
    If real credentials are valid, it will return a real PesaPal redirect URL.
    """
    print("=== PesaPal Integration Test ===")
    cache.clear() # Force fresh token request
    
    client = APIClient()
    User = get_user_model()
    user, _ = User.objects.get_or_create(username='test_payer', email='test@edumerk.com')
    client.force_authenticate(user=user)
    
    payload = {
        "amount": "500.00",
        "description": "Edumerk Test Payment"
    }
    
    print("\n[Step 1] Initiating Payment...")
    try:
        response = client.post('/api/v1/payments/initiate/', payload, format='json')
        if response.status_code == 200:
            print("[SUCCESS] Payment initiated successfully!")
            print(json.dumps(response.data, indent=2))
            
            ref = response.data.get('merchant_reference')
            tracking_id = response.data.get('order_tracking_id')
            
            print(f"\n[Step 2] Simulating IPN Callback for {tracking_id}...")
            # Simulate PesaPal calling our /handler/ endpoint
            ipn_url = f'/api/v1/payments/ipn/handler/?OrderTrackingId={tracking_id}&OrderMerchantReference={ref}'
            ipn_response = client.get(ipn_url)
            
            if ipn_response.status_code == 200:
                print("[SUCCESS] IPN Handler processed callback!")
            else:
                print(f"[FAIL] IPN Handler failed: {ipn_response.status_code}")
                print(ipn_response.data)
                
        else:
            print(f"[FAIL] Payment initiation failed: {response.status_code}")
            print(response.data)
            
    except Exception as e:
        print(f"[ERROR] An exception occurred: {e}")

if __name__ == "__main__":
    test_pesapal_flow()
