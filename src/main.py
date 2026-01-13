# src/main.py
import os
import json
from src.gmail_service import get_gmail_service, fetch_unread_message_ids, get_message, mark_as_read
from src.sheets_service import get_sheets_service, append_rows
from src.email_parser import parse_message
from config import STATE_FILE

os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)

def load_state():
    if not os.path.exists(STATE_FILE):
        return set()
    with open(STATE_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return set(data.get('processed_ids', []))

def save_state(processed_set):
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump({'processed_ids': list(processed_set)}, f, indent=2)

def main():
    gmail = get_gmail_service()
    sheets = get_sheets_service()

    processed = load_state()
    messages = fetch_unread_message_ids(gmail, max_results=200)
    if not messages:
        print("No unread messages found.")
        return

    rows_to_add = []
    processed_now = set()
    for m in messages:
        msg_id = m.get('id')
        if msg_id in processed:
            print(f"Skipping already processed message {msg_id}")
            continue
        full_msg = get_message(gmail, msg_id)
        parsed = parse_message(full_msg)
        rows_to_add.append([parsed['from'], parsed['subject'], parsed['date'], parsed['content']])
        # mark as read
        try:
            mark_as_read(gmail, msg_id)
        except Exception as e:
            print(f"Warning: failed to mark {msg_id} as read: {e}")
        processed_now.add(msg_id)

    if rows_to_add:
        result = append_rows(sheets, rows_to_add)
        print("Appended", len(rows_to_add), "rows. API response:", result.get('updates', {}))
    else:
        print("Nothing to append.")

    # update and persist processed ids
    processed.update(processed_now)
    save_state(processed)
    print("State saved. Total processed IDs:", len(processed))

if __name__ == '__main__':
    main()
