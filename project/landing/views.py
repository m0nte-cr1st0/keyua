# Django imports
from django.conf import settings
from django.views.generic import TemplateView
from django.template.loader import render_to_string
from django.http import Http404, JsonResponse
from django.shortcuts import redirect
from django.db.models import Q
from django.urls import reverse

# REST imports
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.views import APIView

# Project imports
from project.blog.models import Category, Article
from project.cms.models import (
    Page,
    JsCode,
    BlogComponent,
    RobotsFile,
    RedirectSettings
)
from project.mailing.models import ContactForm
from project.mailing.forms import ContactFormForm
from project.utils.utils import send_contact_us_notification
from project.content.models import Review


def is_normal_slash_count(url):
    temp_url = url
    slash_count = 0
    while temp_url.endswith('/'):
        slash_count += 1
        temp_url = temp_url[:-1]
    return (slash_count == 1, slash_count)


def replace_bad_slash(url, slash_count):
    if slash_count == 2:
        return url.replace('//', '/')
    return url.replace('/'*(slash_count-1), '')


def normalize_url(url):
    if len(url) > 1:
        if not url.endswith('/'):
            return url + '/'
        # replace the url like /contacts//// to /contacts/
        good_slash, slash_count = is_normal_slash_count(url)
        if not good_slash:
            url = replace_bad_slash(url, slash_count)
    return url


def is_bad_url(url):
    if len(url) > 1:
        good_slash, slash_count = is_normal_slash_count(url)
        if not good_slash:
            return True
    return False


class RedirectMixinView:

    def dispatch(self, *args, **kwargs):
        url = self.request.path

        redirect_setting = RedirectSettings.objects.filter(url_from=url).first()
        if redirect_setting:
            return redirect(redirect_setting.url_to, permanent=True)

        if is_bad_url(url):
            return redirect(normalize_url(url), permanent=True)
        return super(RedirectMixinView, self).dispatch(*args, **kwargs)


class LandingView(TemplateView):
    template_name = 'base.html'

    def get(self, *args, **kwargs):
        page = Page.objects.filter(url=self.request.path).first()
        # Show 404 page
        if not page:
            raise Http404
        return super(LandingView, self).get(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(LandingView, self).get_context_data(*args, **kwargs)

        test = self.request.GET.get('test')
        pages = Page.objects.order_by('order')
        if test is None:
            pages = pages.exclude(is_draft=True)

        page = pages.filter(url=normalize_url(self.request.path)).first()

        context['canonical'] = '{}{}'.format(settings.SITE_URL, self.request.path)
        context['page'] = page
        context['js_common'] = JsCode.objects.filter(page__isnull=True)
        context['js_page'] = page.jscode_set.all()
        content = ''

        if pages and page:
            for component in page.components.order_by('pagecomponent__order'):
                content += render_to_string(
                    component.get_component_template(),
                    {
                        'component': component.get_component_instance(),
                        'pages': pages.filter(show_on_main_menu=True),
                        'current_page': page,
                        'contact_form': ContactFormForm()
                    },
                    request=self.request
                )
        context['content'] = content
        return context

    def post(self, request, *args, **kwargs):
        contact_form = ContactFormForm(request.POST, request.FILES)
        if contact_form.is_valid():
            contact_form = contact_form.save()
            if contact_form.file:
                file = settings.MEDIA_URL[1:] + str(contact_form.file)
            else:
                file = ''
            send_contact_us_notification(
                file=file,
                name=contact_form.name,
                email=contact_form.email,
                body=contact_form.text,
                phone=contact_form.phone,
                nda=contact_form.nda
            )
            return JsonResponse({})
        else:
            response = {}
            for k in contact_form.errors:
                if contact_form.errors[k][0] == 'This field is required.':
                    response[k] = 'Share details, please.'
                else:
                    response[k] = contact_form.errors[k][0]
            return JsonResponse({"response": response, 'result': 'error'})


class SiteMapView(TemplateView):
    content_type = 'application/xml'
    template_name = 'sitemap.xml'

    def get_context_data(self, *args, **kwargs):
        context = super(SiteMapView, self).get_context_data(*args, **kwargs)
        context['pages'] = (Page.objects
                             .order_by('order')
                             .exclude(Q(is_draft=True) | Q(show_on_sitemap=False)))
        context['articles'] = Article.objects.all()
        context['last_blog_mod'] = max(Article.objects.values_list('last_mod', flat=True))
        context['domain'] = settings.SITE_URL
        return context


class RobotsView(TemplateView):
    content_type = 'text/plain'
    template_name = 'robots.txt'

    def get_context_data(self, *args, **kwargs):
        context = super(RobotsView, self).get_context_data(*args, **kwargs)
        context['content'] = RobotsFile.objects.first()
        return context


class YandexFileView(TemplateView):
    template_name = 'yandex_50e2da9c0795e223.html'


class GoogleSiteVerificationView(TemplateView):
    template_name = 'googlef65a9f395670d60e.html'


############################
## Simple API for project ##
############################


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for user reviews.
    """

    class Meta:
        model = Review
        fields = '__all__'


class LogoSerializer(serializers.Serializer):
    """
    Serializer for customer logos.
    """
    title = serializers.CharField()
    logo = serializers.CharField()
    url = serializers.CharField()


class GallerySerializer(serializers.Serializer):
    """
    Serializer for gallery.
    """
    title = serializers.CharField()
    description = serializers.CharField()
    background = serializers.CharField()


class BlogSerializer(serializers.Serializer):
    """
    Serializer for blog.
    """
    title = serializers.CharField()
    author = serializers.CharField()
    small_image = serializers.CharField()
    url = serializers.SerializerMethodField()
    date = serializers.CharField()

    def get_url(self, obj):
        return obj.get_url()


class ContactFormSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactForm
        fields = '__all__'


class APISimpleView(APIView):

    def get(self, *args, **kwargs):
        component_id = self.request.GET.get('component')
        page_id = self.request.GET.get('page')
        category_id = self.request.GET.get('category')

        if page_id:
            page = Page.objects.filter(id=page_id).first()
            # Data for customer logos component
            if component_id == 'logo':
                component = page.components.filter(
                    component__icontains='cms|CustomerLogoComponent').first()
                if component:
                    component_data = component.get_component_instance()
                    serializer = LogoSerializer(
                        component_data.logos.all(),
                        many=True,
                    )
                    return Response(serializer.data)
            elif component_id == 'gallery':
                component = page.components.filter(
                    component__icontains='cms|GalleryComponent').first()
                if component:
                    component_data = component.get_component_instance()
                    serializer = GallerySerializer(
                        component_data.galleries.all(),
                        many=True
                    )
                    return Response(serializer.data)

            elif component_id == 'reviews':
                component = page.components.filter(
                    component__icontains='cms|ReviewsComponent').first()
                if component:
                    component_data = component.get_component_instance()
                    serializer = ReviewSerializer(
                        component_data.review_list.all(),
                        many=True
                    )
                    return Response(serializer.data)

        # Blog area
        if component_id == 'blog':
            articles =  Article.objects.filter(category_id=category_id) if category_id else Article.objects.all()
            serializer = BlogSerializer(
                articles,
                many=True
            )
            return Response(serializer.data)

    def post(self, *args, **kwargs):
        data = self.request.data

        contact_form = ContactFormSerializer(data=data)
        if contact_form.is_valid():
            contact_form = contact_form.save()

            # Send email notification
            send_contact_us_notification(
                name=contact_form.name,
                email=contact_form.email,
                body=contact_form.text,
                phone=contact_form.phone,
                file=contact_form.file,
                nda=contact_form.nda
            )
            return Response({'success': True})

        return Response({
            'success': False,
            'errors': contact_form.errors
        })