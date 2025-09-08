    # your_app/tasks.py
from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

@shared_task
def send_templated_email_task(template_name, context, subject, recipient_list, from_email=None):
    """
    Celery task to send a templated email.
    """
    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL

    html_content = render_to_string(template_name, context)
    msg = EmailMessage(subject, html_content, from_email, recipient_list)
    msg.content_subtype = "html"  # Main content is now HTML
    msg.send()