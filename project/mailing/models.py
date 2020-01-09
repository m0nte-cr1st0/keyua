# Python import
import os
import uuid

# Django imports
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Project imports
from project.utils import models as base_models
from project.mailing import consts
from project.mailing.mailing import send_email

User = get_user_model()


def get_upload_path(instance, file):
    return 'contactact_form/{0}_{1}'.format(instance.name, file)


class ContactForm(base_models.ModelWithTimestamp):
    """
    Class for storing all form requests.
    """
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=255, blank=True, null=True)
    text = models.TextField()
    file = models.FileField(upload_to=get_upload_path, blank=True,
                            null=True)
    nda = models.BooleanField(default=False)


class EmailNotification(base_models.ModelWithTimestamp):
    """
    A model stores all email notifications in system.
    """
    #: Target email or emails separated by comma.
    target = models.CharField(max_length=255)
    #: Email subject.
    subject = models.CharField(max_length=255)
    #: From name value.
    name = models.CharField(max_length=255)
    #: Content of email.
    content = models.TextField()
    #: Event related current email notification.
    event = models.PositiveSmallIntegerField(choices=consts.EVENT_LIST)
    #: Object type related current email notification.
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )
    #: Object ID related current 
    object_id = models.PositiveIntegerField()
    #: Object related current email notification.
    content_object = GenericForeignKey('content_type', 'object_id')
    #: Key related current email notification.
    key = models.UUIDField(default=uuid.uuid4, editable=False)

    @classmethod
    def create_notification(cls, target, subject, name, content,
            event, obj):
        """
        Creates new email notification.

        :rtype: :class:`project.mailing.models.Notification`
        """
        return cls.objects.create(
            target=target,
            subject=subject,
            name=name,
            content=content,
            event=event,
            object_id=obj.id,
            content_type=ContentType.objects.get_for_model(obj)
        )

    @classmethod
    def get_uuid(cls):
        uuid_ = uuid.uuid4()
        return uuid_

    def send_notification(self):
        extra_data = {}

        send_email.delay(
            subject=self.subject,
            html_content=self.content,
            from_email=self.name or self.get_settings.get('FROM'),
            to=self.target,
            **extra_data
        )


class MessageNotification(base_models.ModelWithTimestamp):
    """
    A model represents all message notifications in system.
    """
    #: Related User
    recipient = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    #: Content of the message
    message = models.TextField()
    #: Already read or not
    read = models.BooleanField(default=False)
