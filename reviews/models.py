from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator


class ClassCategoryReview(models.Model):
    """ Class for the Review of Class Categories """

    class Meta:
        """ Update Meta data for model """
        verbose_name_plural = "Class Category Reviews"
        verbose_name = "Class Category Reviews"

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    review_subject_id = models.CharField(max_length=254, null=False,
                                         blank=False)
    review_text = models.TextField(null=False, blank=False)
    review_rating = models.IntegerField(validators=[MaxValueValidator(5)],
                                        null=False, blank=False,)
    created_on = models.DateTimeField(auto_now_add=True, null=False,
                                      blank=False, editable=False)
