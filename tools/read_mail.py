import aioimaplib
from typing import List, Dict
import email
from email.header import decode_header

def decode_mime_words(s):
    if not s:
        return ""
    decoded = decode_header(s)
    return ''.join(
        part.decode(encoding or 'utf-8') if isinstance(part, bytes) else part
        for part, encoding in decoded
    )

async def read_inbox_emails(imap_server: str, email_address: str, password: str, max_emails: int = 10) -> List[Dict]:
    """
    Connects to the IMAP server and fetches the latest emails from the inbox.
    Returns a list of email metadata dicts: sender, subject, snippet.
    """
    emails = []
    try:
        client = aioimaplib.IMAP4_SSL(imap_server)
        await client.wait_hello_from_server()
        await client.login(email_address, password)
        print(f"✅ Connected to Gmail successfully! ({email_address})")
        select_resp = await client.select('Inbox')
        resp = await client.search('ALL')
        
        if resp.result != 'OK':
            await client.logout()
            return emails
            
        if not resp.lines:
            await client.logout()
            return emails
            
        msg_nums = resp.lines[0].decode().split()
        emails_to_fetch = msg_nums[-max_emails:] if len(msg_nums) > max_emails else msg_nums
        
        for num in reversed(emails_to_fetch):
            try:
                fetch_resp = await client.fetch(num, '(RFC822)')
                
                if fetch_resp.result == 'OK':
                    # Find the actual email content in fetch_resp.lines
                    email_bytes = None
                    for line in fetch_resp.lines:
                        if isinstance(line, (bytes, bytearray)) and b'From:' in line:
                            email_bytes = bytes(line)
                            break
                    if not email_bytes:
                        # Fallback: try the second element if it exists and is bytes/bytearray
                        if len(fetch_resp.lines) > 1 and isinstance(fetch_resp.lines[1], (bytes, bytearray)):
                            email_bytes = bytes(fetch_resp.lines[1])
                    if not email_bytes:
                        continue
                    try:
                        msg = email.message_from_bytes(email_bytes)
                        sender = decode_mime_words(msg.get('From', ''))
                        subject = decode_mime_words(msg.get('Subject', ''))
                        snippet = ''
                        if msg.is_multipart():
                            for part in msg.walk():
                                if part.get_content_type() == 'text/plain':
                                    payload = part.get_payload(decode=True)
                                    if payload:
                                        snippet = payload[:200].decode(errors='ignore')
                                    break
                        else:
                            payload = msg.get_payload(decode=True)
                            if payload:
                                snippet = payload[:200].decode(errors='ignore')
                        emails.append({
                            'from': sender,
                            'subject': subject,
                            'snippet': snippet
                        })
                    except Exception:
                        continue
            except Exception:
                continue
                
        await client.logout()
        
    except Exception:
        # Log or handle error as needed
        pass
    return emails 