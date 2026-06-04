import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Scopes needed for sending emails
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def main():
    creds = None
    
    # We will temporarily store the token in token.json locally
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                print("Attempting to refresh token...")
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing token: {e}")
                # Delete invalid token so it triggers a fresh login next time
                os.remove('token.json')
                print("Deleted old token.json. Re-authenticating...")
                creds = None
        
        if not creds:
            if not os.path.exists('credentials.json'):
                print("Error: 'credentials.json' not found!")
                print("To fix this:")
                print("1. Go to Google Cloud Console (https://console.cloud.google.com/)")
                print("2. Navigate to APIs & Services > Credentials")
                print("3. Download your OAuth 2.0 Client ID JSON file")
                print("4. Rename it to 'credentials.json' and place it in this folder.")
                print("5. Run this script again.")
                return
                
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=5574)
            
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    print("\n✅ Authentication successful!")
    print("\n--- COPY THE JSON BELOW AND PASTE IT AS YOUR 'GMAIL_TOKEN_JSON' ENVIRONMENT VARIABLE IN RAILWAY ---\n")
    print(creds.to_json())
    print("\n-----------------------------------------------------------------------------------------------------\n")

if __name__ == '__main__':
    main()
