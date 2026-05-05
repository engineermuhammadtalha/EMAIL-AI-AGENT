import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_ADDRESS, EMAIL_PASSWORD

IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"


def fetch_unread_emails():
    emails = []
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        mail.select("inbox")

        _, message_ids = mail.search(None, "UNSEEN")
        for mid in message_ids[0].split():
            try:
                _, msg_data = mail.fetch(mid, "(RFC822)")
                raw = msg_data[0][1]
                msg = email.message_from_bytes(raw)

                sender  = msg.get("From", "")
                subject = msg.get("Subject", "(no subject)")
                body    = ""

                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            charset = part.get_content_charset() or "utf-8"
                            payload = part.get_payload(decode=True)
                            if payload:
                                body = payload.decode(charset, errors="replace")
                            break
                else:
                    charset = msg.get_content_charset() or "utf-8"
                    payload = msg.get_payload(decode=True)
                    if payload:
                        body = payload.decode(charset, errors="replace")

                emails.append({"sender": sender, "subject": subject, "body": body})
            except Exception as e:
                print(f"Skipping email: {e}")

        mail.logout()
    except Exception as e:
        print(f"IMAP error: {e}")
        raise

    return emails


def send_reply(to: str, subject: str, body: str):
    subject_line = f"Re: {subject}" if not subject.startswith("Re:") else subject

    msg = MIMEMultipart()
    msg["From"]    = EMAIL_ADDRESS
    msg["To"]      = to
    msg["Subject"] = subject_line
    msg.attach(MIMEText(body, "plain"))

    error_587 = None
    error_465 = None

    # Try port 587 with STARTTLS first
    try:
        with smtplib.SMTP(SMTP_SERVER, 587, timeout=30) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to, msg.as_string())
            return
    except Exception as e:
        error_587 = str(e)

    # Fallback: port 465 with SSL
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, 465, timeout=30) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to, msg.as_string())
            return
    except Exception as e:
        error_465 = str(e)

    raise Exception(f"Both ports failed. 587: {error_587} | 465: {error_465}")
