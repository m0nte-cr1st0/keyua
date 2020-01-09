# Rest imports
from rest_framework import serializers

# Project imports
from project.mailing.models import MessageNotification


class MessageNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageNotification
        fields = ('pk', 'message', 'read')