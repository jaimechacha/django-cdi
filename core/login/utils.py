import smtplib
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.template.loader import render_to_string

from config import settings


def send_email_util(subject, user_email, template, parameters):

    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = settings.EMAIL_HOST_USER
    message['To'] = user_email

    html = render_to_string(template, parameters)
    content = MIMEText(html, 'html')
    message.attach(content)
    server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    server.starttls()
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    server.sendmail(
        settings.EMAIL_HOST_USER, user_email, message.as_string()
    )
    server.quit()


def send_mail_thread(subject, user_email, template, parameters):
    thread = threading.Thread(target=send_email_util, args=(subject, user_email, template, parameters))
    thread.start()
