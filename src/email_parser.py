# src/email_parser.py
import base64
from bs4 import BeautifulSoup

def get_header(headers, name):
    for h in headers:
        if h.get('name', '').lower() == name.lower():
            return h.get('value', '')
    return ''

def _get_text_from_payload(payload):
    """
    Handle multipart and singlepart, prefer text/plain; fallback to html
    payload is message['payload'] from Gmail message resource
    """
    if 'parts' in payload:
        # iterate parts to find text/plain first
        for part in payload['parts']:
            mimeType = part.get('mimeType', '')
            if mimeType == 'text/plain':
                data = part.get('body', {}).get('data', '')
                return _decode_base64(data)
        # fallback to html
        for part in payload['parts']:
            mimeType = part.get('mimeType', '')
            if mimeType == 'text/html':
                data = part.get('body', {}).get('data', '')
                html = _decode_base64(data)
                return _html_to_text(html)
        # deeper nesting
        for part in payload['parts']:
            if 'parts' in part:
                text = _get_text_from_payload(part)
                if text:
                    return text
        return ''
    else:
        # single part
        mimeType = payload.get('mimeType', '')
        data = payload.get('body', {}).get('data', '')
        if mimeType == 'text/plain':
            return _decode_base64(data)
        elif mimeType == 'text/html':
            html = _decode_base64(data)
            return _html_to_text(html)
        else:
            return ''

def _decode_base64(data):
    if not data:
        return ''
    # Gmail uses URL-safe base64
    decoded_bytes = base64.urlsafe_b64decode(data + '==')
    try:
        return decoded_bytes.decode('utf-8')
    except UnicodeDecodeError:
        return decoded_bytes.decode('latin-1')

def _html_to_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text(separator='\n')
    return text

def parse_message(msg):
    payload = msg.get('payload', {})
    headers = payload.get('headers', [])
    sender = get_header(headers, 'From')
    subject = get_header(headers, 'Subject')
    date = get_header(headers, 'Date')
    content = _get_text_from_payload(payload)
    # sanitize: strip leading/trailing whitespace
    return {
        'id': msg.get('id'),
        'from': sender,
        'subject': subject,
        'date': date,
        'content': content.strip()
    }
