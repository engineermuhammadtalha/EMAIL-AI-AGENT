import time
from config import validate_config, EMAIL_ADDRESS
from email_utils import fetch_unread_emails, send_reply
from ai_reply import generate_reply

def run_agent():
    validate_config()
    print(f"📩 AI AutoReply Bot Started as {EMAIL_ADDRESS}")
    print("Press Ctrl+C to stop.\n")

    while True:
        try:
            emails = fetch_unread_emails()
            if not emails:
                print("💤 No new emails. Waiting 30s...")
            else:
                for email_data in emails:
                    sender = email_data.get("sender", "")
                    subject = email_data.get("subject", "(no subject)")
                    body = email_data.get("body", "")

                    print(f"📧 New Email from: {sender}")
                    print(f"   Subject: {subject}")
                    print(f"   Generating AI reply...")

                    try:
                        reply = generate_reply(body)
                        send_reply(sender, subject, reply)
                        print(f"   ✅ Reply sent!\n")
                    except Exception as e:
                        print(f"   ❌ Failed to reply: {e}\n")

        except Exception as e:
            print(f"⚠️  Error: {e}")

        time.sleep(30)

if __name__ == "__main__":
    try:
        run_agent()
    except KeyboardInterrupt:
        print("\n🛑 Agent stopped by user.")
