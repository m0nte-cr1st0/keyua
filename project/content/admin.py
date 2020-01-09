# Django imports
from django.contrib import admin

# Project
from project.content.models import *


class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)


class CityAdmin(admin.ModelAdmin):
    list_display = ('title',)


class ColumnAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


class CustomerLogoAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)


class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)


class ColumnImageAdmin(admin.ModelAdmin):
    list_display = ('title',)


class TextImageAdmin(admin.ModelAdmin):
    list_display = ('title',)


class ListItemAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


class ColumnImageWithListAdmin(admin.ModelAdmin):
    list_display = ('title',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'position', 'text')


class IconLinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'link')


admin.site.register(City, CityAdmin)
admin.site.register(Column, ColumnAdmin)
admin.site.register(Technology, TechnologyAdmin)
admin.site.register(CustomerLogo, CustomerLogoAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(TeamMember, TeamMemberAdmin)
admin.site.register(ColumnImage, ColumnImageAdmin)
admin.site.register(TextImage, TextImageAdmin)
admin.site.register(ListItem, ListItemAdmin)
admin.site.register(ColumnImageWithList, ColumnImageWithListAdmin)

admin.site.register(Review, ReviewAdmin)
admin.site.register(IconLink, IconLinkAdmin)
