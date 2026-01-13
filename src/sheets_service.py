# src/sheets_service.py
from googleapiclient.discovery import build
from src.gmail_service import authenticate
from config import SPREADSHEET_ID, SHEET_NAME

def get_sheets_service():
    creds = authenticate()
    return build('sheets', 'v4', credentials=creds)

def append_rows(service, rows):
    """
    rows: list of rows where each row is a list e.g. [['from','subj','date','content'], ...]
    """
    body = {'values': rows}
    range_name = f"{SHEET_NAME}!A:D"
    result = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name,
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()
    return result
