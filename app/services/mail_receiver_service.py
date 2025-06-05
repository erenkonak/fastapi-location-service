import imaplib
import email
from email.header import decode_header
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def read_unseen_emails():
    username = os.getenv("SMTP_SENDER_EMAIL")
    password = os.getenv("SMTP_PASSWORD")
    imap_server = "imap.gmail.com"

    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(username, password)

    mail.select("inbox")

    status, messages = mail.search(None, 'UNSEEN')
    email_ids = messages[0].split()

    results = []

    for e_id in email_ids:
        # 👇 Important: PEEK instead of FETCH
        res, msg = mail.fetch(e_id, "(BODY.PEEK[])")

        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])

                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")

                from_ = msg.get("From")

                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        try:
                            part_body = part.get_payload(decode=True).decode()
                        except:
                            part_body = None
                        if part_body:
                            body = part_body
                            break
                else:
                    body = msg.get_payload(decode=True).decode()

                results.append({
                    "subject": subject,
                    "from": from_,
                    "body": body
                })

    mail.logout()
    return results

def mark_email_as_seen_by_subject(subject_to_mark: str):
    username = os.getenv("SMTP_SENDER_EMAIL")
    password = os.getenv("SMTP_PASSWORD")
    imap_server = "imap.gmail.com"

    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(username, password)
    mail.select("inbox")

    # Search for all unseen mails
    status, messages = mail.search(None, 'UNSEEN')
    email_ids = messages[0].split()

    for e_id in email_ids:
        res, msg = mail.fetch(e_id, "(BODY.PEEK[])")

        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")

                if subject == subject_to_mark:
                    # Found the email, mark as Seen
                    mail.store(e_id, '+FLAGS', '\\Seen')
                    mail.logout()
                    return f"Email with subject '{subject}' marked as seen."

    mail.logout()
    return f"No unseen email found with subject '{subject_to_mark}'."