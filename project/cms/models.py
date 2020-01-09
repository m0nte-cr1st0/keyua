# Django imports
from django.db import models
from django.utils.safestring import mark_safe

# Project imports
from project.core.mixins import (
    TitleMixin,
    OrderingMixin,
    ComponentDescriptionMixin,
    ComponentButtonMixin,
    ComponentBackgroundMixin
)
from project.content.models import (
    Technology,
    Column,
    City,
    CustomerLogo,
    Project,
    TeamMember,
    ColumnImage,
    TextImage,
    ColumnImageWithList,
    ListItem,
    Review,
    IconLink
)


HEADER_STYLES = (
    (1, 'As on main page'),
    (6, 'As on main page with white links'),
    (2, 'With white menu links'),
    (3, 'With black menu links'),
    (4, 'With contact form'),
    (5, 'Without uppercase')
)

HEADER_TITLE_STYLES = (
    ('h-green-title', 'Green color'),
    ('h-grey-title', 'Grey color'),
    ('h-black-title', 'Dark color'),
    ('h-white-title', 'White color')
)


class SEO(models.Model):
    """
    Class stores SEO specifications for object.
    """
    #: Meta title for page.
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    #: Meta description for page.
    meta_description = models.TextField(blank=True, null=True)
    #: Meta keywords for page.
    meta_keywords = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True


class Component(object):
    """
    Class represents custom component methods.
    """

    @property
    def unique_id(self):
        return '{}-{}'.format(
            self.__class__.__name__.lower(),
            self.id
        )

    def get_component_title(self):
        """
        Return the full title of component.
        """
        return '{component_name}: {component_title}'.format(
                component_name=self.__class__.__name__,
                component_title=self.title
            )

    def get_model_for_instance(self):
        """
        Return unique string for current instance,
        contained from application name, model name, instance ID.
        """
        return '{app_name}|{model_name}|{id}'.format(
                app_name='cms',
                model_name=self.__class__.__name__,
                id=self.id
            )


class HeaderComponent(TitleMixin, ComponentBackgroundMixin, Component):
    """
    Class stores all headers for pages on system.
    """
    #: What CSS style use for this page?
    css_style = models.PositiveSmallIntegerField(choices=HEADER_STYLES)
    #: CSS class for title
    css_title_style = models.CharField(
        choices=HEADER_TITLE_STYLES,
        max_length=100,
        blank=True,
        null=True
    )
    #: CSS class for sub title
    css_subtitle_style = models.CharField(
        choices=HEADER_TITLE_STYLES,
        max_length=100,
        blank=True,
        null=True
    )
    #: Subtitle for header.
    sub_title = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    #: Title for top button.
    top_button_title = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    #: URL for top button.
    top_button_url = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    #: White button title.
    white_button_title = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    #: White button url.
    white_button_url = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    #: Green button title.
    green_button_title = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    #: Green button url.
    green_button_url = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )


class TechnologyComponent(ComponentDescriptionMixin, ComponentButtonMixin, Component):
    """
    Class stores all technology components.
    """
    background = models.ImageField(
        upload_to="tech_backgrounds/",
        help_text="Background or some image",
        blank=True,
        null=True
    )
    #: Related techonologies for current component.
    technologies = models.ManyToManyField(Technology)


class FourColumnComponent(ComponentDescriptionMixin, ComponentBackgroundMixin, ComponentButtonMixin, Component):
    """
    Class stores all four columns components on system.
    """
    CSS_CHOICES = (
        ('default', 'default'),
        ('grey', 'grey')
    )
    COLUMNS_CHOICES = (
        ('col-md-3 col-sm-6 col-xs-12', 'Four columns'),
        ('col-md-4 col-sm-6 col-xs-12', 'Tree columns'),
    )
    #: The columns count
    columns_count = models.CharField(
        choices=COLUMNS_CHOICES,
        max_length=50,
        default='col-md-3 col-sm-6 col-xs-12'
    )
    #: CSS style
    css_style = models.CharField(choices=CSS_CHOICES, max_length=50, blank=True, null=True)
    #: All related columns for this component.
    columns = models.ManyToManyField(Column)


class CityComponent(TitleMixin, Component):
    """
    Class stores all four columns components on system.
    """
    #: All related columns for this component.
    cities = models.ManyToManyField(City)
    description = models.TextField(blank=True)


class BottomComponent(TitleMixin, ComponentButtonMixin, Component):
    """
    Class stores green bottom component.
    """
    DEFAULT = 1
    BIG_SIZE = 2
    FIXED = 3
    VIEW_TYPES = (
        (DEFAULT, 'Default'),
        (BIG_SIZE, 'Big size'),
        (FIXED, 'Fixed on the bottom')
    )
    #: View type
    view_type = models.PositiveSmallIntegerField(
        choices=VIEW_TYPES, default=DEFAULT)


class ProjectComponent(TitleMixin, ComponentButtonMixin, Component):
    """
    Class stores all project components on system.
    """
    BIG_SMALL = 1
    DEFAULT = 2
    VIEW_TYPES = (
        (BIG_SMALL, 'Big-Small'),
        (DEFAULT, 'Default')
    )
    #: View type
    view_type = models.PositiveSmallIntegerField(choices=VIEW_TYPES, default=VIEW_TYPES)
    #: Relates projects.
    projects = models.ManyToManyField(Project)
    description = models.TextField(blank=True)


class CustomerLogoComponent(ComponentDescriptionMixin, Component):
    """
    Class stores all customer logos components.
    """
    #: Relates customer logos.
    logos = models.ManyToManyField(CustomerLogo)


class OfficeSpaceComponent(ComponentDescriptionMixin, Component):
    """
    Class stores all office spaces on system.
    """
    pass


class TileComponent(ComponentDescriptionMixin, Component):
    """
    Class stores all tiles components on system.
    """
    THIN = 1
    FAT = 2
    ICON_CENTERED = 3
    CSS_CHOICES = (
        (THIN, 'Thin'),
        (FAT, 'Fat'),
        (ICON_CENTERED, 'Icons centered')

    )
    COLS_CHOICES = (
        ('col-md-3 col-sm-6 col-xs-12', 'Four columns'),
        ('col-sm-4 col-xs-12', 'Three columns'),
        ('col-md-6 col-sm-6 col-xs-12', 'Two columns')
    )
    #: Css type.
    css_style = models.PositiveSmallIntegerField(choices=CSS_CHOICES, default=THIN)
    #: Columns view
    column_count = models.CharField(choices=COLS_CHOICES, max_length=50, default='col-xs-4')
    #: Related columns
    columns = models.ManyToManyField(Column, through='TileColumnComponent')


class TileColumnComponent(models.Model):
    """
    Class represents columns for tile with ordering.
    """
    #: Current Page.
    tile_component = models.ForeignKey(TileComponent, on_delete=models.CASCADE)
    #: Related component.
    column = models.ForeignKey(Column, on_delete=models.CASCADE)
    #: Position ordering for component on page.
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]


class TeamComponent(ComponentDescriptionMixin, Component):
    """
    Class stores all tiles components on system.
    """
    #: Related members
    members = models.ManyToManyField(TeamMember)


class ColumnImageComponent(ComponentDescriptionMixin, Component):
    """
    Class stores all column images components on system.
    """
    COLUMNS_CHOICES = (
        ('col-md-6', 'Two columns'),
        ('col-md-4 col-sm-6 col-xs-12', 'Tree columns'),
        ('col-md-3 col-sm-6 col-xs-12', 'Four columns'),
    )

    #: The columns count
    columns_count = models.CharField(
        choices=COLUMNS_CHOICES,
        max_length=50,
        default='col-md-6 col-sm-6'
    )
    #: Related columns
    columns = models.ManyToManyField(ColumnImage)


class GalleryComponent(TitleMixin, Component):
    """
    Class stores all text images components on system.
    """
    #: Related galleries
    galleries = models.ManyToManyField(TextImage)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)


class ColumnImageWithListComponent(TitleMixin, Component):
    """
    Class stores all column image lists components on system.
    """
    NORMAL = 1
    IMAGE_LEFT = 2
    STYLES = (
        (NORMAL, 'Image as background'),
        (IMAGE_LEFT, 'Image left')
    )
    COLUMNS_CHOICES = (
        ('col-md-6', 'Two columns'),
        ('col-md-4 col-sm-6 col-xs-12', 'Tree columns'),
        ('col-md-3 col-sm-6 col-xs-12', 'Four columns'),
    )
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    #: The columns count
    columns_count = models.CharField(
        choices=COLUMNS_CHOICES,
        max_length=50,
        default='col-md-6 col-sm-6'
    )
    #: Related items
    items = models.ManyToManyField(ColumnImageWithList)
    #: Css styles
    css_style = models.PositiveSmallIntegerField(choices=STYLES, default=NORMAL)


class TextWithBigBackgroundComponent(ComponentDescriptionMixin, ComponentBackgroundMixin, ComponentButtonMixin, Component):
    """
    Class which stores all texts with big backgrounds on system.
    """
    WHITE = 1
    GREEN = 2
    GREEN_WITH_ICO = 3
    CSS_STYLES = (
        (WHITE, 'White title'),
        (GREEN, 'Green title'),
        (GREEN_WITH_ICO, 'With ico buttons')
    )
    #: Related CSS style 
    css_style = models.PositiveSmallIntegerField(choices=CSS_STYLES, default=WHITE)


class BlogComponent(TitleMixin, Component):
    """
    Class which stores all blog components on system.
    """
    pass


class ContactFormComponent(ComponentDescriptionMixin, Component):
    """
    Presents all contanct forms components in system.
    """
    pass


class ReviewsComponent(ComponentButtonMixin, Component):
    """
    Represents reviews block in the system.
    """
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)

    review_list = models.ManyToManyField(Review)

    def __str__(self):
        return self.title or self.description


class IconComponent(ComponentButtonMixin, ComponentBackgroundMixin, Component):
    """
    Represents the set of icons.
    """
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    css_class = models.CharField(max_length=70, default="col-sm-2")
    icon_list = models.ManyToManyField(IconLink)

    def __str__(self):
        return (
            self.title or
            self.description or
            ', '.join(self.icon_list.values_list('title', flat=True))
        )


class ProjectPageComponent(TitleMixin, ComponentBackgroundMixin, Component):
    """
    Represents all project pages in system.
    """
    #: Related project.
    project = models.ForeignKey(
        Project,
        null=True,
        on_delete=models.SET_NULL
    )
    #: Project url.
    project_url = models.CharField(max_length=250)
    projects_page_url = models.CharField(max_length=200, default="/projects/")
    #: Short description on header.
    header_text = models.TextField()
    #: Project location.
    location_text = models.CharField(max_length=50)
    #: Project industry.
    industry_text = models.CharField(max_length=50)
    #: Project team size.
    team_size_text = models.CharField(max_length=50)
    #: Project period text.
    period_text = models.CharField(max_length=50)
    #: List of project achievements.
    achievements = models.ManyToManyField(ListItem)
    #: List of related technologies
    technology_component = models.ForeignKey(
        TechnologyComponent,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    #: List of project facts.
    facts = models.ManyToManyField(Column, blank=True)


class ComponentUnit(TitleMixin):
    #: Related component.
    component = models.CharField(max_length=255, blank=True, null=True)

    def get_component_model(self):
        app_name, model_name, pk = self.component.split('|')
        from django.apps import apps
        component_model = apps.get_model(app_name, model_name)
        return component_model

    def get_component_template(self):
        app_name, model_name, pk = self.component.split('|')
        return 'components/{}.html'.format(model_name)

    def get_component_instance(self):
        app_name, model_name, pk = self.component.split('|')
        return self.get_component_model().objects.get(pk=pk)


class Page(TitleMixin, OrderingMixin, SEO):
    """
    Class stores all unique pages on system.
    """
    #: Parent page.
    parent = models.ForeignKey(
        'self',
        models.SET_NULL,
        blank=True,
        null=True,
    )
    #: Unique url address.
    url = models.CharField(max_length=255, unique=True)
    #: Show breadcrumbs?
    show_breadcrumbs = models.BooleanField(default=False)
    #: Is page located on main menu?
    show_on_main_menu = models.BooleanField(default=False)
    #: Is page index?
    is_index = models.BooleanField(default=False)
    #: Is draft?
    is_draft = models.BooleanField(default=False)
    #: Show on sitemap?
    show_on_sitemap = models.BooleanField(default=True)
    #: Related components
    components = models.ManyToManyField(ComponentUnit, through='PageComponent')
    #: Custom CSS for page
    custom_css = models.TextField(blank=True)
    #: Last modification date
    last_mod = models.DateTimeField(auto_now=True)

    def get_breadcrumbs(self):
        """
        Returns breadcrumbs for current page.
        """
        page = self
        breadcrumbs = []
        while page:
            breadcrumbs.append('<span>/</span><a href="{}">{}</a>'.format(
                page.url, page.title))
            page = page.parent
        breadcrumbs.append('<a href="/">KeyUa</a>')
        return ''.join(breadcrumbs[::-1])

    def show_preview(self):
        """
        Returns link for draft page.
        """
        return mark_safe('<a href="{}?test=test" target="_blank">Preview</a>'.format(self.url))


class JsCode(models.Model):
    """
    Class stores all js codes for pages.
    """
    #: Related js title
    title = models.CharField(max_length=255, blank=True, null=True)
    #: Related page
    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    #: Related JS code
    js_code = models.TextField()

    def __str__(self):
        return "For page: {}".format(
            self.page.title if self.page else 'All pages')


class PageComponent(models.Model):
    """
    Class represents bridge with component and page.
    """
    #: Current Page.
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    #: Related component.
    component = models.ForeignKey(ComponentUnit, on_delete=models.CASCADE)
    #: Position ordering for component on page.
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]


class RobotsFile(models.Model):
    """
    Class represents content for robots file.
    """
    content = models.TextField(blank=True, null=True)


class RedirectSettings(models.Model):
    """
    Stores all redirects on platform.
    """
    url_from = models.CharField(max_length=255, help_text="Example, /url-from/")
    url_to = models.CharField(max_length=255, help_text="Example, /url-to/")

    class Meta:
        verbose_name_plural = "Redirect Settings"

