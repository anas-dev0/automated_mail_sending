import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

from email.mime.base import MIMEBase
from email import encoders



load_dotenv()  # Load environment variables from .env file




def send_email(subject,body,recepient):
    # --- Config ---
    EMAIL = os.getenv("email")
    PASSWORD = os.getenv("password")
    TO = recepient

    # --- Build the email ---
    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = TO
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))  # use "html" for HTML emails


    with open("Cv_anas_aouini.pdf", "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment; filename=Cv_anas_aouini.pdf")
        msg.attach(part)

    # --- Send it ---
    with smtplib.SMTP("smtp.office365.com", 587) as server:
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)
        print("Email sent successfully!")

