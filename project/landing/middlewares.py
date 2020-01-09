import requests, re

from django.shortcuts import redirect
from django.urls import resolve
from django.http import Http404, HttpResponsePermanentRedirect

from django.core.paginator import Paginator
from project.blog.models import Article
from project.cms.models import Page


class RedirectMiddleware(object):
    response_redirect_class = HttpResponsePermanentRedirect

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        path = re.sub("/+", "/", request.path)

        if response.status_code == 404:
            if not path.endswith('/'):
                request.path = path
            else:
                request.path = path[:-1]
            if path.startswith('/blog/'):
                result = re.match(r'\/blog\/[0-9]+', request.path)
                try:
                    if result.start() == 0 and result.end() >= 7:
                        queryset = Article.objects.all()
                        paginator = Paginator(queryset, 10)
                        if int(request.path.split('/')[-1]) > paginator.num_pages:
                            raise Http404
                except AttributeError:
                    raise Http404
            try:
                full_path = request.get_full_path(force_append_slash=True) # add the slash, keeping query parameters
                if full_path in Page.objects.values_list('url', flat=True):
                    return redirect(full_path)
                r = resolve(full_path)
                response = r.func(request, args=r.args, kwargs=r.kwargs)
                if response.status_code == 200:
                    return redirect(full_path)
            except:
            #     if requests.get(request.build_absolute_uri() + '/').status_code == 200:
            #         return redirect(full_path)
                pass  # this will fall through to `return response`

        # Add the Content-Length header to non-streaming responses if not
        # already set.
        if not response.streaming and not response.has_header('Content-Length'):
            response['Content-Length'] = str(len(response.content))
        return response