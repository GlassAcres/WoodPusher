from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
if EMAIL_USER is None:
    raise ValueError("EMAIL_USER environment variable is not set")

conf = ConnectionConfig(
    MAIL_USERNAME=EMAIL_USER,
    MAIL_PASSWORD=os.environ["EMAIL_PASSWORD"],
    MAIL_FROM=EMAIL_USER,  # Now guaranteed to not be None
    MAIL_PORT= int(os.environ["EMAIL_PORT"]),  # Ensure MAIL_PORT is cast to an integer in the next step
    MAIL_SERVER=os.environ["EMAIL_HOST"],
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)

async def send_email(subject: str, recipient: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=[recipient],
        body=body,
        subtype="html",
    )

    fm = FastMail(conf)
    await fm.send_message(message)