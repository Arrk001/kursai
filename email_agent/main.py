import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
load_dotenv()
PASS = os.getenv("GMAILKEY")
ME = os.getenv("ADDRESS")

msg = EmailMessage()
msg['Subject'] = 'Test'
msg['From'] = 'lukaskostiugovas@gmail.com'
msg['To'] = 'silwzz@gmail.com'
msg.set_content('Hello! This is a test.')

try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        # Use app password, not your Gmail password
        smtp.login(ME, PASS)
        smtp.send_message(msg)
    print("Email sent successfully.")
except Exception as e:
    print(f"Failed to send email: {e}")