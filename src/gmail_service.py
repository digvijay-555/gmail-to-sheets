# src/gmail_service.py
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from config import SCOPES, CREDENTIALS_PATH, TOKEN_PATH

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import json

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/spreadsheets",
]

TOKEN_FILE = "token.json"
CREDENTIALS_FILE = "credentials.json"


from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import json

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/spreadsheets",
]

TOKEN_FILE = "token.json"
CREDENTIALS_FILE = "credentials/credentials.json"


def authenticate():
    creds = None

    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH,
                SCOPES
            )

            # ✅ Correct Desktop OAuth flow
            creds = flow.run_local_server(
                port=0,
                open_browser=False,
                prompt="consent"
            )

        with open(TOKEN_PATH, "wb") as token:
            pickle.dump(creds, token)

    return creds


def get_gmail_service():
    creds = authenticate()
    service = build('gmail', 'v1', credentials=creds)
    return service

def fetch_unread_message_ids(service, max_results=100):
    # q: unread in inbox
    result = service.users().messages().list(userId='me', q='in:inbox is:unread', maxResults=max_results).execute()
    return result.get('messages', [])

def get_message(service, msg_id):
    return service.users().messages().get(userId='me', id=msg_id, format='full').execute()

def mark_as_read(service, msg_id):
    service.users().messages().modify(userId='me', id=msg_id, body={'removeLabelIds': ['UNREAD']}).execute()
