import os
from datetime import date

# Django imports
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.files import File
from django.db.models.signals import post_save
from django.db.models import Avg, Count
from django.utils.safestring import mark_safe

# Third parts
from tinymce.models import HTMLField
import tinify

# Project imports
from project.core.mixins import (
    TitleMixin,
    OrderingMixin,
    ComponentDescriptionMixin,
    ComponentButtonMixin,
    ComponentBackgroundMixin
)
from project.content.models import ListItem
from project.cms.models import SEO


tinify.key = settings.TINYPNG_API_KEY


class Image(TitleMixin):
    """
    Class stores all images on project.
    """
    image = models.ImageField(upload_to="blog_images/")
    #: Is optimized flag
    is_optimized = models.BooleanField(default=False)

    def get_optimized_image_name(self):
        img_name, img_format = os.path.basename(self.image.name).split('.')
        return '{0}_optimized.{1}'.format(img_name, img_format)

    def original_image_name(self):
        return os.path.basename(self.image.name)

    def get_url(self):
        image_url = self.image.url

        if self.is_optimized:
            optimized_name = self.get_optimized_image_name()
            original_name = self.original_image_name()
            image_url = image_url.replace(original_name, optimized_name)

        return '{0}{1}'.format(
            settings.SITE_URL,
            image_url
        )

    def preview(self):
        """
        Preview of image.
        """
        return mark_safe('<img src="{0}" width="200">'.format(self.get_url()))


class Category(TitleMixin, SEO):
    """
    Class stores all categories on project.
    """
    #: Related url address
    url = models.CharField(max_length=255, blank=True, null=True, help_text="Just text, without '/'")
    #: Related JS code
    js_code = models.TextField(blank=True, null=True)
    #: Is green button?
    is_green_button = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Categories"

    def get_url(self):
        return reverse('blog-category', args=[self.url])


class Author(ComponentDescriptionMixin, ComponentBackgroundMixin):
    """
    Class stores all authors on system.
    """
    #: Related properties.
    properties = models.ManyToManyField(ListItem)
    #: LinkedIn profile
    linkedin_url = models.CharField(max_length=200, blank=True, null=True)


class Article(TitleMixin, SEO):
    """
    Class stores all articles on system.
    """
    #: Related url address
    url = models.CharField(max_length=255, blank=True, null=True, help_text="Just text, without '/'")
    #: Hide link?
    hidden_link = models.BooleanField(default=False)
    #: Related JS code
    js_code = models.TextField(blank=True, null=True)
    #: Custom header background.
    header_background = models.ImageField(upload_to="article_bg/", blank=True, null=True)
    #: Related category.
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    #: Related image.
    small_image = models.ImageField(upload_to="articles/", blank=True, null=True)
    #: Related title.
    title = models.CharField(max_length=255)
    #: Related date.
    date = models.DateField(
        'Publication date',
        default=date.today,
        blank=True, null=True)
    #: Related author.
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    #: Intro for article
    intro = HTMLField(blank=True, null=True)
    #: Related content.
    contents = HTMLField(blank=True)
    #: Related articles.
    related_articles = models.ManyToManyField('self', blank=True)
    #: Last modification date
    last_mod = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "-id"]

    def get_url(self):
        return reverse('blog-article', args=[self.url])

    def voting(self, ip, rating):
        """
        Method for voting, if this IP is not voted
        
        Parameters
        -------
        ip: str 
            User's IP.
        rating: int
            User's rating for current article.
        
        Return:
        -------
        obj
            create vote object.
        """
        print(Vote.objects.filter(article=self, ip=ip).exists())
        #print(Vote.objects.filter(article=self, ip=ip).first())
        if not Vote.objects.filter(article=self, ip=ip).exists():
            print('it was created')
            Vote.objects.create(article=self, ip=ip, rating=rating)
            print('it was created')


    def vote_status(self, ip):
        """
        Method for returning voting data
        
        Parameters
        -------
        ip: str 
            User's IP.
        
        Return:
        -------
        voted: (bool or int)
            did user vote for this article or not:
                if he voted return his rating(int)
                if he didn't return False(bool)
        vote_count: (int)
            count of votings
        avg_rating: (float)
            average rating
        """
        voted = Vote.objects.filter(article=self, ip=ip).first()
        votings = Vote.objects.filter(article=self).aggregate(
                avg_rating=Avg('rating'),
                count_votes=Count('id')
            )
        return {
            'pk': self.id,
            'voted': voted.rating if voted else False,
            'vote_count': votings.get('count_votes'),
            'avg_rating': round(votings.get('avg_rating')) if votings.get('avg_rating') else 0
        }

    @staticmethod
    def get_client_ip(request):
        """
        Takes user's IP from request
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


##################
##### Vote #######
##################


class Vote(models.Model):
    """
    Class for users voting to article.
    """
    #: Related Article
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE
    )
    #: User's IP
    ip = models.CharField(max_length=20, blank=True)
    #: User's rating for article
    rating = models.PositiveSmallIntegerField()


##################
#### Signals #####
##################


def save_image(sender, instance, created, **kwargs):
    if created or not instance.is_optimized:
        image_location = '{0}{1}{2}'.format(
            settings.MEDIA_ROOT,
            '/blog_images/',
            os.path.basename(instance.image.name)
        )
        new_filename = instance.get_optimized_image_name()

        new_image_location = '{0}{1}{2}'.format(
            settings.MEDIA_ROOT,
            '/blog_images/',
            new_filename
        )

        source = tinify.from_file(image_location)
        source.to_file(new_image_location)

        instance.is_optimized = True
        instance.save()

post_save.connect(save_image, sender=Image)