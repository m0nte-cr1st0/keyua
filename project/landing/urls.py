# Django imports
from django.conf.urls import url
from django.views.i18n import set_language
from django.views.i18n import JavaScriptCatalog

# Project imports
from project.landing.views import *


urlpatterns = [
    # TODO: move to core urls
    url(r'^setlang/$', set_language, name='set_language'),
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),

    # Sitemap
    url(r'^sitemap.xml$', SiteMapView.as_view(), name='site-map'),
    url(r'^robots.txt$', RobotsView.as_view(), name='robots'),

    # Other files
    url(r'^yandex_50e2da9c0795e223.html$', YandexFileView.as_view(), name='yandex-file'),

    # It's important to hold it on this place
    url(r'^simple-api/$', APISimpleView.as_view(), name='simple-api'),
    url(r'^', LandingView.as_view(), name='landing'),
]