import os
import base64
import json
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from django.conf import settings

class GmailService:
    def __init__(self):
        self.token_path = os.path.join(settings.BASE_DIR, 'mailing_utilities', 'gmail_token.json')
        print(self.token_path ,"...............")
        self.creds = self._get_credentials()
        self.service = build('gmail', 'v1', credentials=self.creds)

    def _get_credentials(self):
        if not os.path.exists(self.token_path):
            raise FileNotFoundError(f"Gmail token file not found at {self.token_path}")
        
        with open(self.token_path, 'r') as f:
            token_data = json.load(f)
        
        creds = Credentials.from_authorized_user_info(token_data)
        
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            # Update the token file with the new token
            with open(self.token_path, 'w') as f:
                f.write(creds.to_json())
        
        return creds

    def send_email(self, to, subject, body):
        try:
            message = MIMEText(body)
            message['to'] = to
            message['subject'] = subject
            
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            create_message = {
                'raw': raw_message
            }
            
            send_message = self.service.users().messages().send(userId="me", body=create_message).execute()
            print(f"Message Id: {send_message['id']} sent to {to}")
            return send_message
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
