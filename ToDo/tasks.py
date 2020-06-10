from __future__ import absolute_import, unicode_literals
from django.core.mail import send_mail
from celery import shared_task
from ToDo import settings

@shared_task
def send_email(message, to_email, from_email=settings.EMAIL_HOST_USER, subject='TODO', ):
    send_mail(subject=subject,
              message=message,
              from_email=from_email,
              recipient_list=[to_email,],
              fail_silently=False,
              )
