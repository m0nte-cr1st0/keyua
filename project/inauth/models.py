# Python imports
import uuid
import datetime

# Django imports
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F
from django.urls import reverse

# Third apps imports
from enumfields import EnumIntegerField
from rest_framework.authtoken.models import Token

# Project imports
from project.utils import (
    enums,
    consts,
    models as base_models
)
from project.utils.utils import get_username_from_email
from project.mailing.consts import (
    ACCOUNT_CONFIRMATION,
    PASSWORD_RESET,
    PASSWORD_RESET_SUCCESS
)


class User(AbstractUser, base_models.ModelWithTimestamp):
    """
    User model for the project.
    """
    #: User who invited current user to the system.
    referral = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    @property
    def api_token(self):
        """
        Returns token API key.

        :rtype: str
        """
        token, created = Token.objects.get_or_create(user=self)
        return token.key

    @property
    def firstname(self):
        """
        Returns first name if exists, otherwise get a username from email.

        :rtype: str
        """
        return self.first_name or get_username_from_email(self.email)

    @property
    def balance(self):
        from project.transaction.models import Transaction
        return '{:,.2f}'.format(Transaction.get_user_balance(self))

    def get_referral_link(self):
        """
        Returns referral link for current user.

        :rtype: str
        """
        return '{domain}{url}?{key}={user_id}'.format(
            domain=settings.SITE_URL,
            url=reverse('invite_from_link'),
            key=settings.SESSION_REFERRAL_NAME,
            user_id=self.id
        )

    def check_referral(self, session):
        """
        Checks referral into session and apply to user if exists.

        :rtype: class
        """
        if settings.SESSION_REFERRAL_NAME in session:
            referral_pk = session.get(settings.SESSION_REFERRAL_NAME)
            if referral_pk:
                referral = User.objects.filter(pk=referral_pk).first()
                if referral and not self.referral:
                    self.referral = referral
                    self.save()
        return self


class PasswordResetRequest(base_models.ModelWithTimestamp):
    """
    Model which stores all requests for resetting password.
    """
    #: Email which needs resetting.
    email = models.EmailField()
    #: Key for this request.
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    #: Status of using.
    used = models.BooleanField(default=False)

    @classmethod
    def generate_request(cls, email):
        """
        Generates new request if not exists, otherwise uses existing.
        """
        reset_request = cls.objects.filter(email=email, used=False).first()
        if not reset_request:
            reset_request = cls.objects.create(email=email)
        # send email with request.
        from project.mailing.tasks import apply_notification
        user = User.objects.get(email=email)
        apply_notification(reset_request, PASSWORD_RESET, **{'user': user})
        return reset_request

    def get_reset_password_url(self):
        """
        Returns an absolute url for reset password request.

        :rtype: str
        """
        return '{domain}{url}?key={key}'.format(
                domain=settings.SITE_URL,
                url=reverse('reset_password'),
                key=self.key
            )

    def mark_as_used(self):
        """
        Closed request.
        """
        self.used = True
        self.save()
        # TODO: add this behavior
        # send email with request.
        # user = User.objects.get(email=self.email)
        # apply_notification(self, PASSWORD_RESET_SUCCESS, **{'user': user})
        return self


class ConfirmationAccountRequest(base_models.ModelWithTimestamp):
    """
    Model which stores all confirmation requests.
    """
    #: Related user
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    #: Unique key for this request.
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    #: Current status of request.
    confirmed = models.BooleanField(default=False)
    #: Count of sending to user.
    send_count = models.PositiveSmallIntegerField(default=0)

    @classmethod
    def create_request(cls, user):
        """
        Creates a new confirmation request.
        """
        confirmation_request = cls.objects.create(user=user)
        confirmation_request.send_confirmation_email()
        return confirmation_request

    def get_confirmation_url(self):
        """
        Returns an absolute url for confirmation request.

        :rtype: str
        """
        return '{domain}{url}?key={key}'.format(
                domain=settings.SITE_URL,
                url=reverse('account-confirmation'),
                key=self.key
            )

    def send_confirmation_email(self):
        from project.mailing.tasks import apply_notification
        apply_notification(self, ACCOUNT_CONFIRMATION, **{'user': self.user})
        self.send_count = F('send_count') + 1
        self.save()
        return self

    def mark_as_confirmed(self):
        """
        Mark status of request as confirmed.
        """
        self.confirmed = True
        self.save()

        from project.referral.models import Invite
        # Search intivations and award it.
        invite = Invite.pending.filter(email=self.user.email).first()
        if invite:
            invite.apply_awarding(self.user)

            # Mark all other invitations as deprecated.
            for bad_invite in Invite.pending.filter(
                    email=self.user.email).exclude(pk=invite.pk):
                bad_invite.mark_as_registered_by_other()

        return self
