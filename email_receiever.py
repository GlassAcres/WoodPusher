from aiosmtpd.controller import Controller
from email import message_from_bytes
from email.policy import default
import os
import asyncio
from anthropic import AsyncAnthropic
import imaplib
import email

# Assuming send_email is defined in email_service.py and correctly imported here
from email_service import send_email

class EmailHandler:
    def __init__(self):
        self.async_client = AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        self.imap_user = os.environ["EMAIL_USER"]
        self.imap_password = os.environ["EMAIL_PASSWORD"]

    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        envelope.rcpt_tos.append(address)
        return '250 OK'

    async def handle_DATA(self, server, session, envelope):
        msg = message_from_bytes(envelope.content, policy=default)
        body = msg.get_body(preferencelist=('plain', 'html')).get_content()

        # Extract the thread ID or subject to use as a conversation identifier
        thread_id = msg['Message-ID']

        # Fetch conversation context using IMAP
        conversation_context = self.fetch_conversation_context(thread_id)

        # Generate AI response with conversation context
        ai_response = await self.generate_ai_response(body + "\n\n" + conversation_context)

        from_email = msg['from']  # Sender's email address
        await send_email("AI Response", from_email, ai_response)

        return '250 OK'

    def fetch_conversation_context(self, thread_id):
        # Connect to Gmail's IMAP server and authenticate
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(self.imap_user, self.imap_password)
        mail.select('inbox')

        # Assuming thread_id is used to search for related emails
        # This is a placeholder for actual search logic based on thread_id or another identifier
        status, data = mail.search(None, 'ALL')
        all_emails = []
        for num in data[0].split():
            status, data = mail.fetch(num, '(RFC822)')
            email_msg = email.message_from_bytes(data[0][1])
            all_emails.append(email_msg.get_payload())

        # Logout and return concatenated emails as context
        mail.logout()
        return "\n\n".join(all_emails)

    async def generate_ai_response(self, user_message):
        response = await self.async_client.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": user_message,
                }
            ],
            model="claude-3-opus-20240229",
        )
        return response.content[0].text

async def start_email_receiver():
    handler = EmailHandler()
    controller = Controller(handler, hostname='0.0.0.0', port=8025)
    controller.start()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_email_receiver())
