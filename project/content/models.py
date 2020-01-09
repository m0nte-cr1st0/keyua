# Django imports
from django.db import models

# Project imports
from project.core.mixins import (
    TitleMixin,
    OrderingMixin,
    ComponentDescriptionMixin,
    ComponentButtonMixin,
    ComponentBackgroundMixin
)


class Technology(TitleMixin, OrderingMixin):
    """
    Class stores all techologies on system.
    """
    #: Logo of technologe.
    logo = models.ImageField(upload_to="technology_logos/")

    class Meta:
        verbose_name_plural = "Technologies"


class Column(ComponentDescriptionMixin, OrderingMixin):
    """
    Class stores all columns content on system.
    """
    ICONS_CHOICES = (
        ('development', 'development'),
        ('high-load', 'high-load'),
        ('security', 'security'),
        ('mach-learning', 'mach-learning'),
        ('dev-ops', 'dev-ops'),
        ('real-time', 'real-time'),
        ('back-end', 'back-end'),
        ('front-end', 'front-end'),
        ('devops', 'devops'),
        ('qa', 'qa'),
        ('ux', 'ux'),
        ('intergations', 'intergations'),
        ('ico manufacturing', 'ico manufacturing'),
        ('ico oli & gas', 'ico oli & gas'),
        ('ico real', 'ico real estate'),
        ('ico jems', 'ico jems'),
        ('ico chemical', 'ico chemical'),
        ('ico agriculture', 'ico agriculture'),
    )
    #: Related icon.
    css_icon = models.CharField(choices=ICONS_CHOICES, blank=True, null=True, max_length=255)
    #: Related hover background.
    hover_background = models.ImageField(upload_to="hover-bg/", blank=True, null=True)
    #: Related url address.
    url = models.CharField(max_length=255, blank=True, null=True)


class City(ComponentDescriptionMixin, ComponentBackgroundMixin, OrderingMixin):
    """
    Class stores all cities content on system.
    """
    more_text = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Cities"


class CustomerLogo(TitleMixin, OrderingMixin):
    """
    Class stores all customer logos on system.
    """
    #: Logo file.
    logo = models.ImageField(upload_to="customer_logos/")
    #: The url to customer
    url = models.CharField(max_length=200, blank=True, null=True)


class Project(
        ComponentDescriptionMixin,
        ComponentBackgroundMixin,
        ComponentButtonMixin,
        OrderingMixin
    ):
    """
    Class stores all projects on system.
    """
    #: Logo for project.
    logo = models.ImageField(upload_to="project_logos/", null=True, blank=True)
    #: Short description.
    short_description = models.TextField(null=True, blank=True)
    #: Is nofollow link?
    nofollow_link = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']


class TeamMember(ComponentDescriptionMixin, OrderingMixin):
    """
    Class stores all members on system.
    """
    #: Related photo
    photo = models.ImageField(upload_to="team_photos/")
    #: Related position
    position = models.CharField(max_length=50)
    #: Link to LinkedIn profile url
    linkedin_url = models.CharField(max_length=255, blank=True, null=True)


class ColumnImage(ComponentDescriptionMixin, ComponentBackgroundMixin, ComponentButtonMixin):
    """
    Class which stores all column images on system.
    """
    pass


class TextImage(ComponentDescriptionMixin, ComponentBackgroundMixin):
    """
    Class which stores all column images on system.
    """
    pass


class ListItem(TitleMixin):
    """
    Class stores all list items on system.
    """
    pass

class ColumnImageWithList(ComponentDescriptionMixin, ComponentBackgroundMixin, ComponentButtonMixin):
    """
    Class which stores column images with list on system.
    """
    #: List items title
    items_title = models.CharField(max_length=200, blank=True, null=True)
    #: Related items
    items = models.ManyToManyField(ListItem)


class Review(models.Model):
    """
    Class to present user reviews.
    """
    #: Working position of reviwer
    position = models.CharField(max_length=100)
    #: The reviewer name
    name = models.CharField(max_length=100, blank=True)
    #: The background of slide
    background_color = models.CharField(max_length=50, default="#fff")
    #: Reviewer photo
    photo = models.ImageField(
        upload_to="review_user/",
        blank=True, 
        null=True
    )
    #: The text of review.
    text = models.TextField()

    def __str__(self):
        return '{}: {}'.format(self.position, self.text)


class IconLink(models.Model):
    """
    Class to present set of icons with title and link.
    """
    #: The title of the icon.
    title = models.CharField(max_length=50)
    #: The image of icon.
    icon = models.ImageField(
        upload_to="icons_set/",
        blank=True, 
        null=True
    )
    #: The redirect link for icon.
    link = models.CharField(max_length=200)

    def __str__(self):
        return self.title
