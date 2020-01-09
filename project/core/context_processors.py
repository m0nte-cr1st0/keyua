# Python imports
import json
import time

# Django imports
from django.utils.safestring import mark_safe
from django.conf import settings

# Project imports
from project.core.js_urls import PROJECT_URLS


def core_context(request):
    """
    Returns basics data for core functionality
    """
    context_dict = {
        'PROJECT_URLS': mark_safe(json.dumps(PROJECT_URLS)),
        'JS_TIMESTAMP': time.time()
    }

    variables = ('DEBUG',)
    for variable in variables:
        context_dict[variable] = getattr(settings, variable, None)

    return context_dict