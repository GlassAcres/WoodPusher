from aiosmtpd.controller import Controller
from aiosmtpd.handlers import Message
from email import message_from_bytes
from email.policy import default

class EmailHandler:
    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        envelope.rcpt_tos.append(address)
        return '250 OK'

    async def handle_DATA(self, server, session, envelope):
        message = message_from_bytes(envelope.content, policy=default)
        subject = message['subject']
        from_email = message['from']
        body = message.get_body(preferencelist=('plain', 'html')).get_content()

        # TODO: Process the received email and generate AI response

        return '250 OK'

async def start_email_receiver():
    handler = EmailHandler()
    controller = Controller(handler, hostname='0.0.0.0', port=8025)
    controller.start()