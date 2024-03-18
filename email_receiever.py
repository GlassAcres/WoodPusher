from aiosmtpd.controller import Controller
from email import message_from_bytes
from email.policy import default
import os
import asyncio
from anthropic import AsyncAnthropic

class EmailHandler:
    def __init__(self):
        self.async_client = AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        envelope.rcpt_tos.append(address)
        return '250 OK'

    async def handle_DATA(self, server, session, envelope):
        message = message_from_bytes(envelope.content, policy=default)
        body = message.get_body(preferencelist=('plain', 'html')).get_content()

        ai_response = await self.generate_ai_response(body)

        # Assuming `send_email` is your function to send emails
        from_email = message['from']  # Sender's email address
        await send_email("AI Response", from_email, ai_response)

        return '250 OK'

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

# This ensures that the async event loop is correctly managed
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_email_receiver())
