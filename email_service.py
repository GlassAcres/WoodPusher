from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import os


conf = ConnectionConfig(
    MAIL_USERNAME=os.environ["EMAIL_USER"],
    MAIL_PASSWORD=os.environ["EMAIL_PASSWORD"],
    MAIL_FROM=os.environ["EMAIL_USER"],  # Now guaranteed to not be None
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