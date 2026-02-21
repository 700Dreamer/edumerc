import os
import base64
import json
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request


class GmailService:
    def __init__(self):
        self.creds = self._get_credentials()
        self.service = build('gmail', 'v1', credentials=self.creds)

    def _get_credentials(self):
        token_json = os.getenv("GMAIL_TOKEN_JSON")

        if not token_json:
            raise ValueError("GMAIL_TOKEN_JSON environment variable not set")

        token_data = json.loads(token_json)
        creds = Credentials.from_authorized_user_info(token_data)

        # Refresh token if expired
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

            # OPTIONAL: Print new token JSON for manual update in Railway
            print("Token refreshed. Update Railway variable with:")
            print(creds.to_json())

        return creds

    def send_email(self, to, subject, body):
        try:
            message = MIMEText(body)
            message['to'] = to
            message['subject'] = subject

            raw_message = base64.urlsafe_b64encode(
                message.as_bytes()
            ).decode()

            create_message = {'raw': raw_message}

            send_message = (
                self.service.users()
                .messages()
                .send(userId="me", body=create_message)
                .execute()
            )

            print(f"Message Id: {send_message['id']} sent to {to}")
            return send_message

        except Exception as e:
            print(f"An error occurred: {e}")
            return None