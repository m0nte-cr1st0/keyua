# Django imports
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import logout, get_user_model
from django.http import Http404
from django.views.generic import RedirectView, TemplateView
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect

# Project imports
from project.inauth.models import ConfirmationAccountRequest, PasswordResetRequest
from project.utils.mixins import RedirectIfAuthorizedMixin, LandingJSContextMixin
from project.utils import enums
from project.utils import notifications

User = get_user_model()

# TODO: RedirectIfAuthorizedMixin
class LandingView(LandingJSContextMixin, TemplateView):
    template_name = 'landing.html'


class RegistrationFromInviteView(TemplateView):
    template_name = 'inauth/registration_from_invite.html'
    target_page = reverse_lazy('landing')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(self.target_page)

        invite_key = request.GET.get('key')
        invite = Invite.objects.filter(key=invite_key).first()

        if not invite:
            return redirect(self.target_page)

        return super(RegistrationFromInviteView, self).dispatch(
                request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(RegistrationFromInviteView, self).get_context_data(*args, **kwargs)
        invite_key = self.request.GET.get('key')
        invite = Invite.objects.filter(key=invite_key).first()

        context['bad_invite'] = User.objects.filter(email=invite.email).exists() or \
                                    invite.status != enums.ReferralStatuses.PENDING
        context['invite'] = invite
        return context


class ResetPasswordView(TemplateView):
    template_name = 'inauth/reset_password.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ResetPasswordView, self).get_context_data(*args, **kwargs)
        reset_key = self.request.GET.get('key')

        if not PasswordResetRequest.objects.filter(key=reset_key, used=False).exists():
            raise Http404

        context['reset_key'] = reset_key
        return context


class ReferralLinkView(RedirectView):

    def dispatch(self, *args, **kwargs):
        referral = self.request.GET.get(settings.SESSION_REFERRAL_NAME)
        if referral:
            self.request.session[settings.SESSION_REFERRAL_NAME] = referral
            self.request.session.modified = True
        return redirect(reverse('landing'))


class ConfirmationAccountRequestView(RedirectView):

    def dispatch(self, *args, **kwargs):
        key = self.request.GET.get('key')
        if key:
            confirmation_request = ConfirmationAccountRequest.objects.filter(
                key=key).first()
            if confirmation_request:
                confirmation_request.mark_as_confirmed()
                if self.request.user.is_authenticated():
                    messages.success(self.request, notifications.USER_CONFIRMED_ACCOUNT)
                else:
                    url = '{}?message={}'.format(
                            reverse('message-page'),
                            notifications.USER_CONFIRMED_ACCOUNT
                        )
                    return redirect(url)
        return redirect(reverse('landing'))


class MessagePageView(TemplateView):
    template_name = 'inauth/message_page.html'

    def get_context_data(self, *args, **kwargs):
        context = super(MessagePageView, self).get_context_data(*args, **kwargs)
        message = self.request.GET.get('message', 'Opps, no updates for you :)')
        context['message'] = message
        return context


class LogoutView(RedirectView):

    def dispatch(self, *args, **kwargs):
        logout(self.request)
        return redirect(reverse('landing'))
