# Django imports
from django.conf.urls import url
from django.views.i18n import set_language
from django.views.i18n import JavaScriptCatalog

# Project imports
from project.inauth.views import *


urlpatterns = [
    url(r'^$', LandingView.as_view(), name='landing'),
    url(r'^registration-from-invite/$', RegistrationFromInviteView.as_view(), name='registration_from_invite'),
    url(r'^reset-password/$', ResetPasswordView.as_view(), name='reset_password'),
    url(r'^i/$', ReferralLinkView.as_view(), name='invite_from_link'),
    url(r'^confirm/account/$', ConfirmationAccountRequestView.as_view(), name='account-confirmation'),
    url(r'^message-page/$', MessagePageView.as_view(), name='message-page'),
    url(r'^logout/$', LogoutView.as_view(), name='inauth-logout'),

    # TODO: move to core urls
    url(r'^setlang/$', set_language, name='set_language'),
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]