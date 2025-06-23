from email.message import EmailMessage
import smtplib
from dotenv import load_dotenv
import os


load_dotenv()

GMAIL_USER = 'lukaskostiugovas@gmail.com'
GMAILKEY = os.getenv("GMAILKEY")


def send_email(email_content, recipient, subject):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = GMAIL_USER
    msg['To'] = recipient

    msg.add_alternative(f"""
    <html>
    <body>
       {email_content}
    </body>
    </html>
    """, subtype='html')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            # Use app password, not your Gmail password
            smtp.login(GMAIL_USER, GMAILKEY)
            smtp.send_message(msg)
        print("Email sent successfully.")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


send_email_definition = {
    "type": "function",
    "function": {
        "name": "send_email",
        "description": "Sends an email to a certain person via SMTP",
        "parameters": {
            "type": "object",
            "properties": {
                "email_content": {"type": "string", "description": "The html markup of email message"},
                "recipient": {"type": "string", "description": "The email address of recipient for the email message"},
                "subject": {"type": "string", "description": "the title or subject for an email message"},
            },
            "required": ["email_content", "recipient"]
        }
    }
}
