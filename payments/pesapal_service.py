import requests
import json
from django.conf import settings
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

class PesaPalService:
    def __init__(self):
        self.debug = getattr(settings, 'DEBUG', True)
        
        # Automatically switch URL based on DEBUG flag
        if self.debug:
            # Sandbox URL
            self.base_url = "https://pay.pesapal.com/v3"
            logger.info("[PesaPal] Using Production Environment")
        else:
            # Production URL
            self.base_url = "https://pay.pesapal.com/v3"
            logger.info("[PesaPal] Using Production Environment")
            
        self.consumer_key = getattr(settings, 'PESAPAL_CONSUMER_KEY', '')
        self.consumer_secret = getattr(settings, 'PESAPAL_CONSUMER_SECRET', '')

    def get_token(self):
        """Request PesaPal Access Token and cache it."""
        token = cache.get('pesapal_token')
        if token:
            return token

        url = f"{self.base_url}/api/Auth/RequestToken"
        payload = {
            "consumer_key": self.consumer_key,
            "consumer_secret": self.consumer_secret
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                token = response.json().get('token')
                # Token expires in 5 minutes
                cache.set('pesapal_token', token, timeout=300)
                return token
            else:
                logger.error(f"[PesaPal] Token Request Failed: {response.status_code} - {response.text}")
        except Exception as e:
            logger.error(f"[PesaPal] Token Request Exception: {e}")
            
        return None

    def register_ipn(self, callback_url):
        """Register IPN URL and return IPN_ID."""
        # PesaPal CANNOT register localhost/127.0.0.1. 
        # For local development, we return a dummy ID if DEBUG is True.
        if self.debug and ("localhost" in callback_url or "127.0.0.1" in callback_url):
            logger.info(f"[PesaPal] Localhost detected. Returning dummy IPN ID for development.")
            return "local_dev_ipn_id_99999"

        token = self.get_token()
        if not token: 
            return None

        url = f"{self.base_url}/api/URLRegister/RegisterIPN"
        payload = {
            "url": callback_url,
            "ipn_notification_type": "GET"
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json().get('ipn_id')
            elif response.status_code == 401:
                # Unauthorized - clear cache and return None so next try fetches new token
                cache.delete('pesapal_token')
                logger.error("[PesaPal] IPN Registration 401: Cleared token cache.")
            else:
                logger.error(f"[PesaPal] IPN Registration Failed: {response.status_code} - {response.text}")
        except Exception as e:
            logger.error(f"[PesaPal] IPN Registration Exception: {e}")
        
        return None

    def submit_order(self, transaction, ipn_id, callback_url):
        """Submit order and return redirect_url."""
        token = self.get_token()
        if not token: return None

        url = f"{self.base_url}/api/Transactions/SubmitOrderRequest"
        payload = {
            "id": str(transaction.merchant_reference),
            "currency": transaction.currency,
            "amount": float(transaction.amount),
            "description": transaction.description,
            "callback_url": callback_url,
            "notification_id": ipn_id,
            "billing_address": {
                "email_address": transaction.user.email or "guest@edumerk.com",
                "phone_number": "",
                "country_code": "UG",
                "first_name": transaction.user.username,
                "last_name": "User",
                "line_1": "Kampala",
                "city": "Kampala"
            }
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"[PesaPal] Order Submission Failed: {response.status_code} - {response.text}")
        except Exception as e:
            logger.error(f"[PesaPal] Order Submission Error: {e}")
            
        return None

    def get_transaction_status(self, order_tracking_id):
        """Verify transaction status live."""
        token = self.get_token()
        if not token: return None

        url = f"{self.base_url}/api/Transactions/GetTransactionStatus?orderTrackingId={order_tracking_id}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"[PesaPal] Status Check Failed: {response.status_code} - {response.text}")
        except Exception as e:
            logger.error(f"[PesaPal] Status Check Error: {e}")
        
        return None
