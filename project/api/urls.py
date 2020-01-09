# Django imports
from django.conf.urls import url, include

# Project imports
from project.api.views import (
    inauth,
    mailing
)

router_inauth = inauth.InauthRouter()
router_inauth.register('inauth', inauth.InauthViewSet, base_name="inauth")

router_notification = mailing.NotificationRouter()
router_notification.register('mailing', mailing.NotificationViewSet, base_name="notification")


urlpatterns = [
    url(r'^inauth/', include(router_inauth.urls)),
    url(r'^notification/', include(router_notification.urls)),
]