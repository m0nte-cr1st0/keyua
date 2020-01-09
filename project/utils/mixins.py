# Python imports
import json

# Django imports
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _l
from django.utils.safestring import mark_safe

# Project imports
from project.core.rates import RATES


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            data = {
                'status': 'error',
                'errors': form.errors
            }
            return JsonResponse(data)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'status': 'ok',
                'pk': self.object.pk if self.object else None,
            }
            return JsonResponse(data)
        else:
            return response


class RedirectIfAuthorizedMixin(object):
    # TODO: Change to needed view
    target_page = reverse_lazy('landing')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.target_page)
        return super(RedirectIfAuthorizedMixin, self).dispatch(
                request, *args, **kwargs)


class OnlyAuthorizedMixin(object):
    target_page = reverse_lazy('landing')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.target_page)
        return super(OnlyAuthorizedMixin, self).dispatch(
                request, *args, **kwargs)


class LandingJSContextMixin(object):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['LANDING_APP'] = mark_safe({
            # All texts related components
            'components': {
                # Texts related with `authorization.vue.js` components.
                'authorization': {
                    'firstName': str(_l('First Name')),
                    'email': str(_l('E-mail')),
                    'password': str(_l('Password')),
                    'send': str(_l('Send')),
                    'forgotPassword': str(_l('forgot password')),
                    'login': str(_l('login')),
                    'registration': str(_l('registration')),
                },
                # Texts related with `common/calculator.vue.js` components.
                'calculator': {
                    'investment': str(_l('Investment')),
                    'proposal': str(_l('Proposal')),
                    'minimumDeposit': str(_l('Minimum deposit')),
                    'montlyReturn': str(_l('Montly Return')),
                    'profitPerDay': str(_l('Profit per day')),
                    'profitWholePeriod': str(_l('Profit for the whole period')),
                    'totalIncome': str(_l('Total income (deposit + profit)')),
                    'yourInvestments': str(_l('Your investments')),
                    'difficultRate': str(_l('Difficult rate')),
                    'investmentTerm': str(_l('Investment term')),
                    'months': str(_l('months')),
                    'investWithUs': str(_l('Invest with us')),
                },
            },
            # All texts related applications
            'applications': {
                # Texts related with `authorization.vue.js` application.
                'authorization': {
                    'login': str(_l('login')),
                    'registration': str(_l('registration')),
                },
            },
            # All texts for errors.
            'errors': {
                'requiredField': str(_l('Field is required')),
                'invalidEmail': str(_l('Enter a valid email')),
                'invalidURL': str(_l('Enter a valid URL address')),
                'shortLength': str(_l('The value is too short')),
            },

        })
        # All contansts for landing application.
        context['LANDING_CONSTS'] = mark_safe(
            json.dumps({
                'rates': RATES
            })
        )
        return context

