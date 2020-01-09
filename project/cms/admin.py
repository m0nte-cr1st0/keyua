# Django imports
from django.contrib import admin
from django import forms

# Project imports
from project.cms.models import *


##### Admin forms ######
def get_component_unit_choices():
    ALL_COMPONENTS = (
        HeaderComponent,
        TechnologyComponent,
        FourColumnComponent,
        BottomComponent,
        CityComponent,
        CustomerLogoComponent,
        ProjectComponent,
        OfficeSpaceComponent,
        TileComponent,
        TeamComponent,
        ColumnImageComponent,
        GalleryComponent,
        ColumnImageWithListComponent,
        TextWithBigBackgroundComponent,
        ContactFormComponent,
        ProjectPageComponent,
        ReviewsComponent,
        IconComponent
    )
    PAGE_COMPONENT_CHOICES = []
    for component in ALL_COMPONENTS:
        for obj in component.objects.all():
            PAGE_COMPONENT_CHOICES.append((obj.get_model_for_instance(), obj.get_component_title()))

    return PAGE_COMPONENT_CHOICES


class ComponentUnitAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ComponentUnitAdminForm, self).__init__(*args, **kwargs)
        self.fields['component'] = forms.ChoiceField(
            choices=get_component_unit_choices()
        )

    class Meta:
        model = ComponentUnit
        fields = '__all__'
########################


class PageComponentInline(admin.TabularInline):
    model = PageComponent


class ComponentUnitAdmin(admin.ModelAdmin):
    list_display = ('title',)
    form = ComponentUnitAdminForm


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'show_preview', 'url', 'show_on_main_menu', 'order',
                    'is_index', 'is_draft', 'show_breadcrumbs', 'show_on_sitemap')
    list_editable = ('show_on_main_menu', 'order',
                    'is_index', 'is_draft', 'show_breadcrumbs', 'show_on_sitemap')
    list_filter = ('show_on_main_menu', 'show_breadcrumbs',
                   'is_index', 'is_draft', 'show_on_sitemap')
    inlines = [
        PageComponentInline
    ]


class HeaderComponentAdmin(admin.ModelAdmin):
    list_display = ('title',)


class BottomComponentAdmin(admin.ModelAdmin):
    list_display = ('title',)


class TechnologiesInline(admin.TabularInline):
    model = TechnologyComponent.technologies.through


class TechnologyComponentAdmin(admin.ModelAdmin):
    inlines = [
        TechnologiesInline
    ]
    exclude = ('technologies',)


class ColumnsInline(admin.TabularInline):
    model = FourColumnComponent.columns.through


class FourColumnComponentAdmin(admin.ModelAdmin):
    inlines = [
        ColumnsInline
    ]
    exclude = ('columns',)


class CitiesInline(admin.TabularInline):
    model = CityComponent.cities.through


class CityComponentAdmin(admin.ModelAdmin):
    inlines = [
        CitiesInline
    ]
    exclude = ('cities',)


class CustomerLogoInline(admin.TabularInline):
    model = CustomerLogoComponent.logos.through


class CustomerLogoComponentAdmin(admin.ModelAdmin):
    inlines = [
        CustomerLogoInline
    ]
    exclude = ('logos',)


class ProjectInline(admin.TabularInline):
    model = ProjectComponent.projects.through


class ProjectComponentAdmin(admin.ModelAdmin):
    inlines = [
        ProjectInline
    ]
    exclude = ('projects',)


class OfficeSpaceComponentAdmin(admin.ModelAdmin):
    list_display = ('title',)


class TileColumnComponentInline(admin.TabularInline):
    model = TileColumnComponent


class TileComponentAdmin(admin.ModelAdmin):
    list_display = ('title', 'column_count')
    list_editable = ('column_count',)
    list_filter = ('column_count',)

    inlines = [
        TileColumnComponentInline
    ]


class TeamComponentAdmin(admin.ModelAdmin):
    list_display = ('title',)


class ColumnImageComponentAdmin(admin.ModelAdmin):
    list_display = ('title',)


class GalleryComponentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)


class ColumnImageWithListComponentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)


class TextWithBigBackgroundComponentAdmin(admin.ModelAdmin):
    list_display = ('title',)


class ContactFormComponentAdmin(admin.ModelAdmin):
    list_display = ('__str__',)


class JsCodeAdmin(admin.ModelAdmin):
    list_display = ('title', '__str__', 'page')
    list_filter = ('page',)


class ProjectPageComponentAdmin(admin.ModelAdmin):
    list_display = ('project', 'project_url', 'header_text')


class RobotsFileAdmin(admin.ModelAdmin):
    list_display = ('content',)


class RedirectSettingsAdmin(admin.ModelAdmin):
    list_display = ('url_from', 'url_to')


class ReviewsComponentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')


class IconComponentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')


admin.site.register(ComponentUnit, ComponentUnitAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(HeaderComponent, HeaderComponentAdmin)
admin.site.register(BottomComponent, BottomComponentAdmin)
admin.site.register(TechnologyComponent, TechnologyComponentAdmin)
admin.site.register(FourColumnComponent, FourColumnComponentAdmin)
admin.site.register(CityComponent, CityComponentAdmin)
admin.site.register(CustomerLogoComponent, CustomerLogoComponentAdmin)
admin.site.register(ProjectComponent, ProjectComponentAdmin)
admin.site.register(OfficeSpaceComponent, OfficeSpaceComponentAdmin)
admin.site.register(TileComponent, TileComponentAdmin)
admin.site.register(TeamComponent, TeamComponentAdmin)
admin.site.register(ColumnImageComponent, ColumnImageComponentAdmin)
admin.site.register(GalleryComponent, GalleryComponentAdmin)
admin.site.register(ColumnImageWithListComponent, ColumnImageWithListComponentAdmin)
admin.site.register(TextWithBigBackgroundComponent, TextWithBigBackgroundComponentAdmin)
admin.site.register(ContactFormComponent, ContactFormComponentAdmin)
admin.site.register(ProjectPageComponent, ProjectPageComponentAdmin)
admin.site.register(JsCode, JsCodeAdmin)
admin.site.register(RobotsFile, RobotsFileAdmin)
admin.site.register(RedirectSettings, RedirectSettingsAdmin)
admin.site.register(ReviewsComponent, ReviewsComponentAdmin)
admin.site.register(IconComponent, IconComponentAdmin)
