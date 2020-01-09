# Django imports
from django.conf import settings

# Project imports
from project.mailing.models import EmailNotification, MessageNotification
from project.mailing import consts
from project.mailing.utils import generate_html


def apply_notification(obj, notification_id, **kwargs):

    template = consts.EVENT_SETTINGS[notification_id]['TEMPLATE'] or kwargs.get('template')
    subject = consts.EVENT_SETTINGS[notification_id]['SUBJECT']
    from_name = consts.EVENT_SETTINGS[notification_id]['FROM_EMAIL']
    uuid_ = EmailNotification.get_uuid()

    message_notification = consts.MESSAGE_NOTIFICATION_SETTINGS.get(notification_id)

    if notification_id == consts.USER_REGISTRATION:
        # obj == User
        user = obj

        data = {
            'name': user.firstname
        }
        html = generate_html(data, template)
        email_notification = EmailNotification.create_notification(
            target=user.email,
            subject=subject,
            name=from_name,
            content=html,
            event=notification_id,
            obj=user
        )
        email_notification.send_notification()
    if notification_id == consts.PASSWORD_RESET:
        # obj == PasswordResetRequest
        password_reset_request = obj
        user = kwargs.get('user')

        data = {
            'name': user.firstname,
            'reset_password_link': password_reset_request.get_reset_password_url()
        }
        html = generate_html(data, template)
        email_notification = EmailNotification.create_notification(
            target=user.email,
            subject=subject,
            name=from_name,
            content=html,
            event=notification_id,
            obj=user
        )
        email_notification.send_notification()
    if notification_id == consts.ACCOUNT_CONFIRMATION:
        # obj == ConfirmAccountRequest
        confirmation_account = obj

        data = {
            'name': confirmation_account.user.firstname,
            'confirmation_link': confirmation_account.get_confirmation_url()
        }
        html = generate_html(data, template)
        email_notification = EmailNotification.create_notification(
            target=confirmation_account.user.email,
            subject=subject,
            name=from_name,
            content=html,
            event=notification_id,
            obj=confirmation_account
        )
        email_notification.send_notification()

    # Add message notification
    if message_notification:
        user = kwargs.get('user')
        if user:
            message_notification = message_notification.get('TEXT')
            MessageNotification.objects.create(
                recipient=user,
                message=message_notification)
