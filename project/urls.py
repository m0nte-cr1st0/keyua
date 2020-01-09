"""IncheckSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from project.landing.views import GoogleSiteVerificationView


urlpatterns = [
    # WYSIWYG HTML editor
    url(r'^tinymce/', include('tinymce.urls')),
    url('keyua-admin/filebrowser/', admin.site.urls),
    url('grappelli/', include('grappelli.urls')),

    # API
    url(r'^api/', include('project.api.urls')),

    # Blog
    url(r'^blog/', include('project.blog.urls')),

    # admin side
    url(r'^keyua-admin/', admin.site.urls),

    #Other files
    url(r'^googlef65a9f395670d60e.html/$', GoogleSiteVerificationView.as_view(), name='google-file'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# It's important to hold it on this place
urlpatterns += [
    url(r'^', include('project.landing.urls')),
]
