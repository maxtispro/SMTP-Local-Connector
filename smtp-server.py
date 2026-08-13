from aiosmtpd.smtp import SMTP as Server, Envelope, Session
from aiosmtpd.controller import Controller
import smtplib
import asyncio
from connectors import Connector
from threading import Event

from config import config


def relay_message(envelope: Envelope):
    connector = Connector(envelope)
    return connector.sendmail()


class MessageHandler:

    async def handle_DATA(self,
        server: Server,
        session: Session,
        envelope: Envelope
    ):
        try:
            refused = await asyncio.to_thread(relay_message, envelope)

            if refused:
                print("Refused, Send errors:", refused)
                return "451 4.3.0 Some recipients were refused"

            return "250 2.0.0 Message relayed"

        except smtplib.SMTPAuthenticationError as error:
            print("Authentication failed: ", error)
            return "451 4.7.0 Upstream authentication failed"

        except smtplib.SMTPException as error:
            print("SMTP failure", error)
            return "451 4.3.0 Upstream SMTP failure"


if __name__ == "__main__":

    controller = Controller(
        MessageHandler(),
        config.local.hostname,
        config.local.port
    )

    try:
        print("Starting SMTP Server")
        controller.start()
        Event().wait()

    except KeyboardInterrupt:
        print("\nStopping Server")

    finally:
        controller.stop()