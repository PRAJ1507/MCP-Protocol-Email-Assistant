from typing import Dict, List
import datetime
import re
import json
import os
import smtplib
from email.mime.text import MIMEText

SCHEDULED_MAIL_FILE = os.path.join(os.path.dirname(__file__), "scheduled_emails.json")

def extract_sender_name(sender: str) -> str:
    """
    Extracts the sender's name from the email address.
    Examples:
    - "John Doe <john@example.com>" -> "John"
    - "john@example.com" -> "John"
    - "John Doe" -> "John"
    """
    if not sender:
        return "Unknown Sender"
    
    # Remove email address if present
    sender_clean = re.sub(r'<[^>]+>', '', sender).strip()
    
    # If it's just an email address, extract the name part
    if '@' in sender_clean and ' ' not in sender_clean:
        name_part = sender_clean.split('@')[0]
        # Capitalize first letter
        return name_part.capitalize()
    
    # If it's a full name, take the first name
    if ' ' in sender_clean:
        first_name = sender_clean.split(' ')[0]
        return first_name
    
    # If it's a single word, use it as is
    return sender_clean

def load_scheduled_emails() -> List[Dict]:
    if not os.path.exists(SCHEDULED_MAIL_FILE):
        return []
    with open(SCHEDULED_MAIL_FILE, "r") as f:
        return json.load(f)

def save_scheduled_emails(emails: List[Dict]):
    with open(SCHEDULED_MAIL_FILE, "w") as f:
        json.dump(emails, f, indent=2, default=str)

def is_duplicate_email(email: Dict, send_time: str) -> bool:
    emails = load_scheduled_emails()
    for scheduled in emails:
        if (
            scheduled.get('from') == email.get('from') and
            scheduled.get('subject') == email.get('subject')
        ):
            return True
    return False

def schedule_email_send(email: Dict, send_time: str) -> bool:
    """
    Schedules the given email to be sent at the specified time.
    Persists the scheduled email in a JSON file.
    Returns True if scheduled successfully, False if duplicate.
    """
    if is_duplicate_email(email, send_time):
        print(f"[SKIP] Duplicate email not scheduled: {email.get('subject')} from {email.get('from')}")
        return False
    emails = load_scheduled_emails()
    # Assign a unique id
    email_id = len(emails) + 1
    scheduled_email = {
        "id": email_id,
        "to": email.get("to"),
        "from": email.get("from"),
        "subject": email.get("subject"),
        "body": email.get("draft"),
        "scheduled_time": send_time,
        "sent": False
    }
    emails.append(scheduled_email)
    save_scheduled_emails(emails)
    print(f"[SCHEDULE] Email to: {scheduled_email['to']} at {send_time}")
    return True

def get_due_emails() -> List[Dict]:
    """
    Returns a list of emails whose scheduled time is <= now and not sent.
    """
    emails = load_scheduled_emails()
    now = datetime.datetime.now(datetime.timezone.utc)
    due = []
    for email in emails:
        if not email["sent"]:
            scheduled_time = datetime.datetime.fromisoformat(email["scheduled_time"])
            if scheduled_time <= now:
                due.append(email)
    return due

def mark_email_sent(email_id: int):
    emails = load_scheduled_emails()
    for email in emails:
        if email["id"] == email_id:
            email["sent"] = True
    save_scheduled_emails(emails)

def send_email(smtp_server: str, email_address: str, password: str, to: str, subject: str, body: str):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = email_address
    msg["To"] = to
    with smtplib.SMTP_SSL(smtp_server) as server:
        server.login(email_address, password)
        server.sendmail(email_address, [to], msg.as_string())

def process_due_emails(smtp_server: str, email_address: str, password: str):
    due_emails = get_due_emails()
    for email in due_emails:
        try:
            send_email(
                smtp_server=smtp_server,
                email_address=email_address,
                password=password,
                to=email["to"],
                subject=email["subject"],
                body=email["body"]
            )
            mark_email_sent(email["id"])
            print(f"[SENT] Email to: {email['to']} (ID: {email['id']})")
        except Exception as e:
            print(f"[ERROR] Failed to send scheduled email to {email['to']}: {e}") 