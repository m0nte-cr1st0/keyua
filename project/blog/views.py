# Django imports
from django.views.generic import ListView, DetailView
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.http import JsonResponse

# Project imports
from project.blog.models import Category, Article, Vote
from project.landing.views import RedirectMixinView
from project.cms.models import Page


ITEMS_ON_PAGE = 10


class BlogViewMixin(ListView):
    queryset = Article.objects.all()
    context_object_name = 'articles'
    category = None

    def get_queryset(self, *args, **kwargs):
        queryset = super(BlogViewMixin, self).get_queryset(*args, **kwargs)

        if (self.kwargs.get('page')) == '1':
            raise Http404

        page = self.kwargs.get('page', 1)
        category = self.kwargs.get('category', None)

        if category:
            category = get_object_or_404(Category, url=category)
            queryset = queryset.filter(category=category)
            self.category = category

        paginator = Paginator(queryset, ITEMS_ON_PAGE)

        try:
            queryset = paginator.page(page)
        except EmptyPage:
            raise Http404

        return queryset

    def get_context_data(self, **kwargs):
        context = super(BlogViewMixin, self).get_context_data(**kwargs)
        context['current_page'] = self.kwargs.get('page', None)
        if context['current_page']:
            context['current_page'] = int(context['current_page'])

        context['current_category'] = self.category
        context['categories'] = Category.objects.exclude(is_green_button=True)
        context['marked_category'] = Category.objects.filter(is_green_button=True).first()
        context['SITE_URL'] = settings.SITE_URL
        context['pages'] = Page.objects.filter(show_on_main_menu=True, is_draft=False).order_by('order')
        return context


class BlogView(BlogViewMixin):
    template_name = 'blog/index.html'


class CategoryView(BlogViewMixin):
    template_name = 'blog/category.html'


class ArticleView(RedirectMixinView, DetailView):
    template_name = 'blog/article.html'
    context_object_name = 'article'
    queryset = Article.objects.all()

    def get_object(self, *args, **kwargs):
        article = get_object_or_404(Article, url=self.kwargs['article'])
        return article

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleView, self).get_context_data(*args, **kwargs)
        article = self.get_object()
        context['SITE_URL'] = settings.SITE_URL
        context['pages'] = Page.objects.filter(show_on_main_menu=True, is_draft=False).order_by('order')
        return context

    def get(self, *args, **kwargs):
        article = self.get_object()
        if self.request.is_ajax():
            article = self.get_object()
            return JsonResponse(
                article.vote_status(article.get_client_ip(self.request))
            )
        return super(ArticleView, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        # take request with article's "rating"
        if self.request.is_ajax():
            rating = self.request.POST.get('rating')
            article = self.get_object()
            ip = article.get_client_ip(self.request)
            article.voting(ip, rating)
            return JsonResponse(
                article.vote_status(ip)
            )
        return super(ArticleView, self).get(*args, **kwargs)