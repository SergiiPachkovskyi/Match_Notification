import smtplib
import ssl
from email.message import EmailMessage
from django.conf import settings


def send(user_email, text, subject):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.ukr.net", port=465, context=context) as server:
        server.login("saintdaemon@ukr.net", settings.EMAIL_PASSWORD)
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = 'saintdaemon@ukr.net'
        msg['To'] = user_email
        server.sendmail(from_addr="saintdaemon@ukr.net", to_addrs=user_email, msg=str(msg) + text)
        server.quit()
