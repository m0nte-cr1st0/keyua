# Django imports
from django.contrib.auth import get_user_model

# Project imports
from project.inauth.models import ConfirmationAccountRequest

User = get_user_model()


def create_user(email, password, request, **kwargs):
    user = User.objects.create_user(email, email, password)

    first_name = kwargs.get('name')
    if first_name:
        user.first_name = first_name

    # Save additional changes
    user.save()

    # Check referral in session.
    user.check_referral(request.session)

    # Create confirmation request.
    ConfirmationAccountRequest.create_request(user=user)

    return user
