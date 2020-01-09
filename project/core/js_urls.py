# Django imports
from django.urls import reverse_lazy


PROJECT_URLS = {
    'languages': {
        'setLanguage': str(reverse_lazy('set_language')),
    },
    'landing': {
        'index': str(reverse_lazy('landing')),
    },
    'authentication': {
        'login': str(reverse_lazy('inauth-login')),
        'registration': str(reverse_lazy('inauth-login')),  # It's not a typo
        'restorePassword': str(reverse_lazy('inauth-forgot-password')),
    },
}