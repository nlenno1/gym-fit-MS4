import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

import classes.models  # used for import of ClassCategory


class ClassCategoryReview(models.Model):
    """Class for a Review"""

    class Meta:
        """Update Meta data for model"""

        verbose_name_plural = "Class Category Reviews"
        verbose_name = "Class Category Review"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    review_subject = models.ForeignKey(
        "classes.ClassCategory", on_delete=models.CASCADE, null=False
    )
    review_text = models.TextField(null=False, blank=False)
    review_rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],
        validators=[MaxValueValidator(5)],
        null=False,
        blank=False,
    )
    created_on = models.DateTimeField(
        auto_now_add=True, null=False, blank=False, editable=False
    )
