# from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

from django.core.validators import MaxValueValidator

# from instructors.models import Instructor


class ClassCategory(models.Model):
    """ Class for the Categories of Exercise Classes Available """

    class Meta:
        """ Update Meta data for model """
        verbose_name_plural = "Class Categories"

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    equipment_required = models.CharField(max_length=254, null=True,
                                          blank=True)
    image = models.ImageField(null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)

    def __str__(self):
        """ Return name string"""
        return self.name

    def get_friendly_name(self):
        """ Return friendly_name string"""
        return self.friendly_name


class SingleExerciseClass(models.Model):
    """ Class for the Categories of Exercise Classes Available """

    class Meta:
        """ Update Meta data for model """
        verbose_name_plural = "Single Exercise Classes"

    category = models.ForeignKey(ClassCategory, null=True, blank=True,
                                 on_delete=models.CASCADE)
    class_date = models.DateField(auto_now=False, auto_now_add=False)
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    end_time = models.TimeField(auto_now=False, auto_now_add=False)
    duration = models.PositiveSmallIntegerField(
               validators=[MaxValueValidator(120)], null=True, blank=True)  # Calculated in function below
    location = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100)  # Will become ForeignKey
    # instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    token_cost = models.PositiveSmallIntegerField(
                validators=[MaxValueValidator(30)])
    max_capacity = models.PositiveSmallIntegerField(
                validators=[MaxValueValidator(150)])
    ability_level = models.CharField(
                    max_length=30, choices=[
                        ('BEG', 'Beginner'),
                        ('INT', 'Intermediate'),
                        ('ADV', 'Advanced')],
                        null=True, blank=True)
    additional_notes = models.TextField(null=True, blank=True)

    # To be filled
    participants = models.ManyToManyField(User, blank=True)
    remaining_spaces = models.PositiveSmallIntegerField(
                       validators=[MaxValueValidator(150)],
                       null=True, blank=True)

    def __init__(self, *args, **kwargs):
        """ Set remaining spaces variable """
        super().__init__(*args, **kwargs)
        self.remaining_spaces = self.max_capacity
    #     if self.duration:
    #         self.duration = datetime.combine(date.today(), self.end_time) - datetime.combine(date.today(),self.start_time)
