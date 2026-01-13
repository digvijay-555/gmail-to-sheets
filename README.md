# Gmail to Google Sheets Automation

**Author:** Digvijay Rahul Deshmukh

## Overview

This project is a Python automation script that reads **unread emails** from a Gmail inbox and appends their details into a Google Sheet. Each email is stored as a new row with the following columns:

* From
* Subject
* Date
* Content

The script is designed to be **idempotent** — running it multiple times will not create duplicate rows. Emails processed successfully are marked as **read** in Gmail.

---

## 1. High-Level Architecture Diagram

```
┌──────────────┐
│   Gmail API  │
│ (Unread Msg)│
└──────┬───────┘
       │ OAuth 2.0
       ▼
┌──────────────┐
│ Python Script│
│  (main.py)   │
│              │
│ - Fetch mail │
│ - Parse data │
│ - Track IDs  │
└──────┬───────┘
       │
       │ Append Rows
       ▼
┌──────────────┐
│ Google Sheets│
│   API        │
└──────────────┘

Local Files:
- credentials/token.pickle (OAuth token)
- state/processed_ids.json (state persistence)
```

*A hand-drawn version of this diagram is included in the submission screenshots.*

---

## 2. Step-by-Step Setup Instructions

### Prerequisites

* Python 3.9+
* Google account with Gmail and Google Sheets access

### Clone and Setup Environment

```bash
git clone <your-repo-url>
cd gmail-to-sheets
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Google Cloud Configuration

1. Create a Google Cloud project
2. Enable **Gmail API** and **Google Sheets API**
3. Configure OAuth Consent Screen
4. Create OAuth Client ID (Desktop App)
5. Download `credentials.json`
6. Place it inside:

```
credentials/credentials.json
```

### Configure Project

Edit `config.py` and set:

```python
SPREADSHEET_ID = "your_google_sheet_id"
SHEET_NAME = "Sheet1"
```

### Run the Script

```bash
python -m src.main
```

On first run, a browser window will open for Google OAuth authorization.

---

## 3. Explanation of Core Concepts

### OAuth Flow Used

This project uses **OAuth 2.0 Installed App Flow** provided by Google.

* The user authenticates via a browser
* Google returns an access token
* Token is stored locally in `credentials/token.pickle`
* No service accounts are used

This approach is suitable for local scripts and personal automation.

---

### Duplicate Prevention Logic

Duplicates are prevented using **two layers of protection**:

1. **Unread filter**

   * Only emails with `is:unread` are fetched from Gmail

2. **Processed Message ID Tracking**

   * Every processed Gmail `messageId` is saved locally
   * If a message ID already exists, it is skipped

This ensures safe re-runs without duplicate sheet entries.

---

### State Persistence Method

State is stored in a local JSON file:

```
state/processed_ids.json
```

Example structure:

```json
{
  "processed_ids": ["18c9a...", "18c9b..."]
}
```

This allows the script to remember previously processed emails across executions.

---

## 4. Challenge Faced & Solution

### Challenge: Python Import Errors (`ModuleNotFoundError: No module named 'src'`)

**Problem:**
Running `python src/main.py` caused import resolution failures.

**Solution:**
The script is executed as a module:

```bash
python -m src.main
```

This ensures the project root is correctly added to Python's module path.

---

## 5. Limitations of the Solution

* State is stored locally; not ideal for distributed systems
* Gmail History API is not used (simpler but less scalable)
* Designed for personal or single-user use
* Large email bodies may exceed comfortable spreadsheet cell sizes
* No scheduling 

---

## Security Notes

* OAuth credentials and tokens are excluded using `.gitignore`
* No secrets are committed to version control

---

## Proof of Execution

The submission includes:

* Gmail inbox screenshots (before/after)
* OAuth consent screen
* Google Sheet with appended rows
* Screen recording demonstrating duplicate prevention

---

## Conclusion

This project demonstrates secure API usage, stateful automation, and safe data synchronization between Gmail and Google Sheets using Python.
