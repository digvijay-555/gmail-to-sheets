# config.py
SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/spreadsheets'
]

CREDENTIALS_PATH = 'credentials/credentials.json'
TOKEN_PATH = 'credentials/token.pickle'   # stored locally after first OAuth
SPREADSHEET_ID = '1BxRflhd4v7lyjJxQNlbXQU7qsyBGX9pV63wy87ipZKs'  # <<-- put your spreadsheet id
SHEET_NAME = 'Sheet1'                        # name of the sheet/tab
STATE_FILE = 'state/processed_ids.json'
