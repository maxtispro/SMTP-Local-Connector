from smtplib import SMTP as Client
from aiosmtpd.smtp import Envelope
import ssl

from config import config


class Connector:

    def __init__(self, envelope: Envelope):
        if not envelope.content:
            raise ValueError("Invalid envelope")
        
        self.from_addr: str = config.remote.from_email
        self.to_addrs: list[str] = envelope.rcpt_tos
        self.message: bytes | str = envelope.content

    def sendmail(self):
        ssl_context = ssl.create_default_context()
        
        with Client(config.remote.hostname, config.remote.port, timeout=30) as client:
            client.ehlo()
            client.starttls(context=ssl_context)
            client.ehlo()
            client.login(config.remote.user, config.remote.secret)

            return client.sendmail(self.from_addr, self.to_addrs, self.message)
