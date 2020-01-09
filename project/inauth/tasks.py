# Django imports
from django.contrib.auth import get_user_model

# Third part imports
from celery import task

# Project imports
from project.inauth.models import ConfirmationAccountRequest


User = get_user_model()


@task
def confirm_account_reminder():
    for user in User.objects.all():
        confirmation_request = ConfirmationAccountRequest.objects.filter(user=user)
        if not confirmation_request.exists():
            ConfirmationAccountRequest.create_request(user=user)
        else:
            confirmation_request = confirmation_request.first()
            if confirmation_request.send_count < 4:
                confirmation_request.send_confirmation_email()
            
