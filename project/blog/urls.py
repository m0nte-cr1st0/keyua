# Django imports
from django.conf.urls import url

# Project imports
from project.blog.views import *


urlpatterns = [
    url(r'^$', BlogView.as_view(), name='blog'),
    url(r'^(?P<page>\d+)/$', BlogView.as_view(), name='blog'),

    url(r'^category/(?P<category>[-\w]+)/$', CategoryView.as_view(), name='blog-category'),
    url(r'^category/(?P<category>[-\w]+)/(?P<page>\d+)/$', CategoryView.as_view(), name='blog-category'),

    url(r'^(?P<article>[-\w]+)/$', ArticleView.as_view(), name='blog-article'),
]