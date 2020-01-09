# Django imports
from django.db import models


class TitleMixin(models.Model):
    """
    Class stores title of object.
    """
    #: Title value of any object.
    title = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return '{}'.format(self.title)


class OrderingMixin(models.Model):
    """
    Class stores ordering value for any object.
    """
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ['order']


class ComponentDescriptionMixin(TitleMixin):
    """
    Class represents component with description section.
    """
    #: Description value of any object.
    description = models.TextField(blank=True)

    class Meta:
        abstract = True


class ComponentButtonMixin(models.Model):
    """
    Class represents component with button section.
    """
    #: Title for button.
    button_title = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    #: URL for button.
    button_url = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    class Meta:
        abstract = True


class ComponentBackgroundMixin(models.Model):
    """
    Class represents component with background.
    """
    #: Background or image raleted it.
    background = models.ImageField(upload_to="backgrounds/", help_text="Background or some image", blank=True)

    class Meta:
        abstract = True
