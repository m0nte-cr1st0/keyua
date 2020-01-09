# Django imports
from django.contrib import admin

# Project imports
from project.blog.models import *

class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_url', 'is_optimized', 'preview')
    list_filter = ('is_optimized',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('title',)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')
    list_filter = ('category',)


class VoteAdmin(admin.ModelAdmin):
    list_display = ('ip', 'rating', 'article')


admin.site.register(Image, ImageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Vote, VoteAdmin)