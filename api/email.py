import smtplib
import getpass
import os
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()


def email(employee_email):
    password = os.environ["EMAIL_HOST_PASSWORD"]
    reciever = employee_email
    sender = os.environ["EMAIL_HOST_USER"]

    msg = MIMEMultipart()
    msg["To"] = reciever
    msg["From"] = sender
    msg["Subject"] = "Qr code"
    msg_ready = MIMEText(
        "Hello, there is a qr code in the message with the contact details of the retail object: "
    )
    image = MIMEImage(
        open("api/static/qr_code.png", "rb").read(), "png", name="QR_CODE"
    )

    msg.attach(msg_ready)
    msg.attach(image)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as mail:
        mail.login(sender, password)
        mail.sendmail(sender, reciever, msg.as_string())
    return True
