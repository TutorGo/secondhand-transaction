import time

from celery.task import task
from django.core.mail import EmailMessage
from django.utils import timezone
from config.celery import app
# from config.celery import app
# from config.celery import app


@app.task
def email_send(subject, message, toemail):
    email = EmailMessage(subject, message, to=[toemail])
    email.send()
