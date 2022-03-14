from django.db import models
from django.contrib.auth.models import User

from django.core.validators import MaxValueValidator

from instructors.models import Instructor
from reviews.models import ClassCategoryReview


ABILITY_CHOICES = [
    ("BEG", "Beginner"),
    ("INT", "Intermediate"),
    ("ADV", "Advanced"),
]


class ClassCategory(models.Model):
    """Class for the Categories of Exercise Classes Available"""

    class Meta:
        """Update Meta data for model"""

        verbose_name_plural = "Class Categories"
        ordering = ["friendly_name"]

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    equipment_required = models.CharField(
        max_length=254, null=True, blank=True
    )
    image = models.ImageField(null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)

    def __str__(self):
        """Return name string"""
        return self.friendly_name

    def generate_average_rating(self):
        """Function to return number of reviews and average rating"""
        reviews = ClassCategoryReview.objects.filter(review_subject=self)
        numb_of_reviews = 0
        rating_total = 0
        review_average_rating = 0
        for review in reviews:
            numb_of_reviews += 1
            rating_total += review.review_rating
        if numb_of_reviews != 0:
            review_average_rating = rating_total / numb_of_reviews
        return review_average_rating, numb_of_reviews


class SingleExerciseClass(models.Model):
    """Class for the Categories of Exercise Classes Available"""

    class Meta:
        """Update Meta data for model"""

        verbose_name_plural = "Single Exercise Classes"
        ordering = ["class_date", "start_time"]

    category = models.ForeignKey(
        ClassCategory, null=True, blank=True, on_delete=models.CASCADE
    )
    class_date = models.DateField(auto_now=False, auto_now_add=False)
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    end_time = models.TimeField(
        auto_now=False, auto_now_add=False
    )  # generated in view
    duration = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(120)], null=True, blank=True
    )
    location = models.CharField(max_length=100)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    token_cost = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(30)]
    )
    max_capacity = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(150)]
    )
    remaining_spaces = models.PositiveSmallIntegerField(  # generated in view
        validators=[MaxValueValidator(150)], null=True, blank=True
    )
    participants = models.ManyToManyField(
        User, blank=True
    )  # generated in view
    ability_level = models.CharField(
        max_length=30, choices=ABILITY_CHOICES, null=True, blank=True
    )
    additional_notes = models.TextField(null=True, blank=True)

    def __str__(self):
        """Return name string"""
        return self.info()

    def info(self):
        """return string of class info"""
        category = self.category.friendly_name
        class_date = self.class_date.strftime("%d/%m/%Y")
        start_time = self.start_time.strftime("%H:%M")
        return f"{category} at {start_time} on the \
            {class_date}"
