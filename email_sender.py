import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")

if not EMAIL or not PASSWORD:
    raise ValueError("EMAIL and PASSWORD must be set in .env file")

def send_email(jobs):
    msg = EmailMessage()
    msg["Subject"] = "New Opportunities for You"
    msg["From"] = EMAIL
    msg["To"] = EMAIL

    if not jobs:
        # Default content when no new jobs
        content = """Hello Akshita,

There are no new opportunities today in your domains.

Keep learning and stay tuned for tomorrow!

Regards,
JOBLIST Team"""
    else:
        content = "Hello Akshita,\n\nHere are the new opportunities for you:\n\n"
        for job in jobs:
            domain = job.get("domain", "General")
            content += f"[{domain}]\n"
            content += f"Title: {job.get('title', 'N/A')}\n"
            content += f"Company/Organizer: {job.get('company', 'N/A')}\n"
            content += f"Location: {job.get('location', 'N/A')}\n"
            content += f"Link: {job.get('link', 'N/A')}\n"
            content += "-" * 40 + "\n"
        content += "\nRegards,\nJOBLIST Team"

    msg.set_content(content)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL, PASSWORD)
            smtp.send_message(msg)
        print("[SUCCESS] Email sent successfully")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")
