from django.db import models


class ModelWithTimestamp(models.Model):
    """
    A model abstraction to support timestamp fields.
    """
    #: The date of creation.
    created_at = models.DateTimeField(auto_now_add=True)
    #: The date the resource was last modified.
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ModelWithOrder(models.Model):
    """
    A model abstraction to support order field.
    """
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ["order"]