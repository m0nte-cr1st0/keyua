# Python imports
import json

# Django imports
from django.core.mail import EmailMessage
from django.conf import settings

# Others imports
from celery import task

# Project imports
from project.mailing.mandrill import mandrill_sent_letter


@task
def send_email(subject, html_content, from_email, to, **kwargs):
    """
    Sending email.
    """
    if not isinstance(to, list):
        to = [to]

    is_mandrill = True  # not settings.DEBUG

    if is_mandrill:
        email_dict = {
            "key": settings.MANDRILL_API_KEY,
            "message": {
                "html": html_content,
                "text": "%s" % subject,
                "subject": "%s" % subject,
                "from_email": settings.DEFAULT_FROM_EMAIL,
                "from_name": settings.DEFAULT_FROM_NAME,
                "to": [
                    {
                        "email": "%s" % to[0],
                        "type": "to"
                    }
                ],
                "attachments": []
            },
        }
        # if attachments
        if kwargs.get('attachments'):
            email_dict['message']['attachments'] = [
                {
                    "type": kwargs.get('type'),
                    "name": kwargs.get('name'),
                    "content": kwargs.get('content')
                }
            ]
        body = json.dumps(email_dict)
        answer = mandrill_sent_letter(body)
    else: 
        msg = EmailMessage(subject, html_content, from_email, to)
        # Main content is now text/html
        msg.content_subtype = "html"
        msg.send()

    return True
