import smtplib
import os
from email.message import EmailMessage

# SMTP Configuration
SMTP_SERVER = "mail.clarksresortnepal.com"  # SMTP server address
SMTP_PORT = 587  # Common SMTP ports: 587 (TLS), 465 (SSL), 25 (Non-secure)
SMTP_USER = "it@clarksresortnepal.com"
SMTP_PASS = "Dd9824204425@123"

# Email Configuration
SENDER_EMAIL = "it@clarksresortnepal.com"
RECIPIENT_EMAIL = "rootuserdj@gmail.com"
SUBJECT = "Receved Photos "
BODY = "Attached is the myphotos.zip file."

# File to attach
FILE_PATH = "myphotos.zip"

# Create Email Message
msg = EmailMessage()
msg["From"] = SENDER_EMAIL
msg["To"] = RECIPIENT_EMAIL
msg["Subject"] = SUBJECT
msg.set_content(BODY)

# Attach File
if os.path.exists(FILE_PATH):
    with open(FILE_PATH, "rb") as f:
        file_data = f.read()
        file_name = os.path.basename(FILE_PATH)
        msg.add_attachment(file_data, maintype="application", subtype="zip", filename=file_name)
else:
    print("Error: File not found.")
    exit()

# Send Email
try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()  # Secure the connection
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
    print("Email sent successfully!")
except Exception as e:
    print(f"Error sending email: {e}")
