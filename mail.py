import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
import os

load_dotenv()


def send_email(subject, body, recepient):
    email_address = os.getenv("EMAIL_ADDRESS")
    email_password = os.getenv("EMAIL_APP_PASSWORD")
    candidate_name = os.getenv("CANDIDATE_NAME")
    cv_file = os.getenv("CV_FILE", "cv.pdf")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.office365.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))

    if not email_address or not email_password:
        raise RuntimeError(
            "EMAIL_ADDRESS and EMAIL_APP_PASSWORD must be set in your .env file."
        )

    msg = MIMEMultipart()
    msg["From"] = f"{candidate_name} <{email_address}>" if candidate_name else email_address
    msg["To"] = recepient
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    if not os.path.exists(cv_file):
        raise FileNotFoundError(
            f"CV file '{cv_file}' not found. Set CV_FILE in your .env to point to your CV PDF."
        )
    with open(cv_file, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(cv_file)}")
        msg.attach(part)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(email_address, email_password)
        server.send_message(msg)
        print("Email sent successfully!")
