import secrets

from aiosmtpd.smtp import SMTP as Server, Envelope, Session, AuthResult, LoginPassword
from aiosmtpd.controller import Controller
import smtplib
import asyncio
from connectors import Connector
from threading import Event

from config import config


def relay_message(envelope: Envelope):
    connector = Connector(envelope)
    return connector.sendmail()


def authenticate(
    server: Server,
    session: Session,
    envelope: Envelope,
    mechanism: str,
    auth_data: LoginPassword
) -> AuthResult:
    
    if mechanism not in {"LOGIN", "PLAIN"}:
        return AuthResult(success=False, handled=False)

    username_valid = secrets.compare_digest(auth_data.login, config.local.user.encode())

    password_valid = secrets.compare_digest(auth_data.password, config.local.password.encode())

    if username_valid and password_valid:
        return AuthResult(success=True)

    return AuthResult(success=False, handled=False, message="535 5.7.8 Authentication credentials invalid")


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
        config.local.port,
        authenticator=authenticate,
        auth_require_tls=False,
        decode_data=False
    )

    try:
        print("Starting SMTP Server")
        controller.start()
        Event().wait()

    except KeyboardInterrupt:
        print("\nStopping Server")

    finally:
        controller.stop()