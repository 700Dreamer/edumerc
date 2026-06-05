import os
import base64
import json
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request


class GmailService:
    def __init__(self):
        try:
            self.creds = self._get_credentials()
            self.service = build('gmail', 'v1', credentials=self.creds)
        except Exception as e:
            print(f"Failed to initialize GmailService: {e}")
            self.creds = None
            self.service = None

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

    def send_email(self, to, subject, body, is_html=False):
        if not self.service:
            print("GmailService not initialized, cannot send email.")
            return None

        try:
            if is_html:
                message = MIMEText(body, 'html')
            else:
                message = MIMEText(body, 'plain')
            
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

    def get_html_template(self, title, message, details, button_text=None, button_url=None, status="Pending"):
        """
        Generates an HTML email based on the design provided.
        details: list of dicts like {'label': 'Booking ID', 'value': 'BK-123'}
        """
        details_html = ""
        for item in details:
            details_html += f"""
            <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #eee; padding: 10px 0;">
                <span style="color: #666;">{item['label']}</span>
                <strong style="color: #333;">{item['value']}</strong>
            </div>
            """

        status_color = "#f39c12" # orange for pending
        if status.lower() in ["paid", "confirmed", "completed", "approved"]:
            status_color = "#27ae60" # green
        elif status.lower() in ["cancelled", "declined", "failed"]:
            status_color = "#e74c3c" # red

        button_html = ""
        if button_text and button_url:
            button_html = f"""
            <div style="margin-top: 30px; text-align: center;">
                <a href="{button_url}" style="background: #00695c; color: white; padding: 12px 25px; border-radius: 8px; text-decoration: none; font-weight: bold; display: block;">{button_text}</a>
            </div>
            """

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                .status-text {{ color: {status_color} !important; font-weight: bold !important; }}
            </style>
        </head>
        <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f9; margin: 0; padding: 20px;">
            <div style="max-width: 500px; margin: 0 auto; background: white; border-radius: 20px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #eee;">
                <div style="padding: 20px; border-bottom: 1px solid #f0f0f0;">
                    <h2 style="margin: 0; color: #1a202c; font-size: 20px;">{title}</h2>
                </div>
                <div style="padding: 30px; text-align: center;">
                    <div style="width: 60px; height: 60px; background: #e8f5e9; border-radius: 50%; display: inline-block; text-align: center; line-height: 60px; margin-bottom: 20px; color: #27ae60; font-size: 30px; font-weight: bold; vertical-align: middle;">✓</div>
                    <p style="color: #4a5568; line-height: 1.5; margin: 0; text-align: center;">{message}</p>
                    
                    <div style="background: #f8f9fa; border-radius: 15px; padding: 20px; text-align: left; margin-top: 20px;">
                        {details_html}
                        <div style="display: flex; justify-content: space-between; padding: 10px 0;">
                            <span style="color: #666;">Status</span>
                            <span style="color: {status_color}; font-weight: bold;">{status}</span>
                        </div>
                    </div>
                    
                    {button_html}
                </div>
            </div>
        </body>
        </html>
        """
        return html
