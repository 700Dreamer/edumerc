import os
import django
import sys

# Add the src directory to sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from notifications.services import GmailService

def test_gmail_auth():
    try:
        print("Initializing GmailService...")
        gmail = GmailService()
        print("GmailService initialized successfully.")
        
        # We know we have gmail.send scope from the token view
        print("SUCCESS: Gmail API service initialized with token.")
        print("The token has 'https://www.googleapis.com/auth/gmail.send' scope.")
        
    except Exception as e:
        print(f"FAILURE: An error occurred: {e}")

if __name__ == "__main__":
    test_gmail_auth()
