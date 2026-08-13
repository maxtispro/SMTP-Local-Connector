from smtplib import SMTP as Client
from email.message import EmailMessage

from config import config


if __name__ == "__main__":

    message = EmailMessage()
    message["From"] = f"Test <{config.remote.from_email}>"
    message["To"] = config.test.to_email
    message["Subject"] = "SMTP Local Connector Success"
    message.set_content("You have successfully configured SMTP Local Connector xD")

    client = Client(config.local.hostname, config.local.port)
    client.send_message(message, "user@example.com", [config.test.to_email])