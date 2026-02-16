import requests
from django.conf import settings
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)


class PesaPalService:
    """
    Production-ready PesaPal v3 service.
    - Uses manual IPN registration
    - Supports sandbox & production
    - Caches auth tokens
    """

    def __init__(self):
        self.debug = getattr(settings, "DEBUG", False)

        # Environment URLs
        if self.debug:
            # Sandbox
            self.base_url = "https://pay.pesapal.com/v3"
            logger.info("[PesaPal] Environment: PRODUCTION")
        else:
            # Production
            self.base_url = "https://pay.pesapal.com/v3"
            logger.info("[PesaPal] Environment: PRODUCTION")

        # Credentials
        self.consumer_key = settings.PESAPAL_CONSUMER_KEY
        self.consumer_secret = settings.PESAPAL_CONSUMER_SECRET

        # Manually registered IPN ID (DO NOT re-register in production)
        self.ipn_id = settings.PESAPAL_IPN_ID

    # ------------------------------------------------------------------
    # AUTH TOKEN
    # ------------------------------------------------------------------
    def get_token(self):
        """
        Get and cache PesaPal access token (valid for 5 minutes).
        """
        token = cache.get("pesapal_token")
        if token:
            return token

        url = f"{self.base_url}/api/Auth/RequestToken"
        payload = {
            "consumer_key": self.consumer_key,
            "consumer_secret": self.consumer_secret,
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(
                url, json=payload, headers=headers, timeout=100
            )

            if response.status_code != 200:
                logger.error(
                    f"[PesaPal] Token request failed "
                    f"{response.status_code}: {response.text}"
                )
                return None
            

            token = response.json().get("token")

            if not token:
                logger.error("[PesaPal] Token missing in response")
                return None

            # Cache for 5 minutes
            cache.set("pesapal_token", token, timeout=300)
            return token

        except Exception as e:
            logger.exception(f"[PesaPal] Token request exception: {e}")
            return None

    # ------------------------------------------------------------------
    # SUBMIT ORDER
    # ------------------------------------------------------------------
    def submit_order(self, transaction, callback_url):
        """
        Submit a payment order and return redirect URL.
        """
        token = self.get_token()
        if not token:
            return None

        url = f"{self.base_url}/api/Transactions/SubmitOrderRequest"

        payload = {
            "id": str(transaction.merchant_reference),
            "currency": "UGX",
            "amount": int(transaction.amount),  # UGX must be integer
            "description": transaction.description,
            "callback_url": callback_url,
            "notification_id": self.ipn_id,
            "billing_address": {
                "email_address": transaction.user.email,
                "country_code": "UG",
                "first_name": transaction.user.username,
                "last_name": "User",
            },
        }

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(
                url, json=payload, headers=headers, timeout=10
            )

            if response.status_code != 200:
                logger.error(
                    f"[PesaPal] SubmitOrder failed "
                    f"{response.status_code}: {response.text}"
                )
                return None

            data = response.json()

            # Must contain redirect_url
            if "redirect_url" not in data:
                logger.error(f"[PesaPal] Invalid submit response: {data}")
                return None

            return data

        except Exception as e:
            logger.exception(f"[PesaPal] SubmitOrder exception: {e}")
            return None

    # ------------------------------------------------------------------
    # VERIFY TRANSACTION
    # ------------------------------------------------------------------
    def get_transaction_status(self, order_tracking_id):
        """
        Verify transaction status from PesaPal.
        """
        token = self.get_token()
        if not token:
            return None

        url = (
            f"{self.base_url}/api/Transactions/GetTransactionStatus"
            f"?orderTrackingId={order_tracking_id}"
        )

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code != 200:
                logger.error(
                    f"[PesaPal] Status check failed "
                    f"{response.status_code}: {response.text}"
                )
                return None

            return response.json()

        except Exception as e:
            logger.exception(f"[PesaPal] Status check exception: {e}")
            return None
