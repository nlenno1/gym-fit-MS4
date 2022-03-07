import uuid
from django.db import models

from classes.models import ClassCategory


class Instructor(models.Model):
    """ Class for a Review """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=254, null=False, blank=False)
    friendly_name = models.CharField(max_length=254, null=False, blank=False)
    description = models.TextField(max_length=255, null=False, blank=False)
    can_lead_classes = models.ManyToManyField(ClassCategory, blank=False)
    image = models.ImageField(null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    display_on_site = models.BooleanField(default=False)
