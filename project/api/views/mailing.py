# Rest imports
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.routers import SimpleRouter, Route

# Project imports
from project.mailing.models import MessageNotification
from project.api.serializers.mailing import MessageNotificationSerializer


class NotificationRouter(SimpleRouter):

    routes = [
        Route(
            url=r'notification-list/$',
            mapping={
                'get': 'notification_list'
            },
            name='{basename}-list',
            initkwargs={}
        ),
        Route(
            url=r'notification-close/$',
            mapping={
                'post': 'notification_close'
            },
            name='{basename}-close',
            initkwargs={}
        ),
    ]


class NotificationViewSet(viewsets.ViewSet):
    """
    Base api class for Mailing app.
    """

    def notification_list(self, request, **kwargs):
        """
        Returns list of unread notifications for current user.
        """
        queryset = MessageNotification.objects.filter(recipient=request.user, read=False)
        serializer = MessageNotificationSerializer(
            queryset,
            many=True,
        )
        return Response(serializer.data)

    def notification_close(self, request, **kwargs):
        """
        Marks notification as read.
        """
        pk = request.data.get('pk')
        MessageNotification.objects.filter(recipient=request.user, pk=pk, read=False).update(read=True)
        return self.notification_list(request, **kwargs)
