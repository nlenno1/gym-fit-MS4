import uuid
from django.db import models

import classes.models  # used for calling ClassCategory


class Instructor(models.Model):
    """Class for a Review"""

    class Meta:
        ordering = ["friendly_name"]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=254, null=False, blank=False)
    friendly_name = models.CharField(max_length=254, null=False, blank=False)
    description = models.TextField(max_length=255, null=True, blank=True)
    can_lead_classes = models.ManyToManyField(
        "classes.ClassCategory", blank=False
    )
    image = models.ImageField(null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    display_on_site = models.BooleanField(default=False)

    def __str__(self):
        """Return name string"""
        return self.friendly_name
