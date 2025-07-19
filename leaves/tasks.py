from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_leave_email(subject, plain_message, from_email, recipient_list, html_message=None):
    send_mail(
        subject,
        plain_message,
        from_email,
        recipient_list,
        html_message=html_message,
        fail_silently=False,
    )