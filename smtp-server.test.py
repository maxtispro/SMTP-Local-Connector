from smtplib import SMTP as Client
from email.message import EmailMessage

from config import config


if __name__ == "__main__":

    with Client(config.local.hostname, config.local.port) as client:
        client.set_debuglevel(1)
        client.ehlo()

        print("Advertised features:", client.esmtp_features)

        client.login(config.local.user, config.local.password)

        print("Authentication succeeded")

        message = EmailMessage()
        message["From"] = f"Test <{config.remote.from_email}>"
        message["To"] = config.test.to_email
        message["Subject"] = "SMTP Local Connector Success"
        message.set_content("You have successfully configured SMTP Local Connector xD")

        client.send_message(message, "user@example.com", [config.test.to_email])