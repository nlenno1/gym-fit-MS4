import uuid
from datetime import date
from django.contrib import messages
from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_countries.fields import CountryField

from classes.models import SingleExerciseClass, ClassCategory

class UserProfile(models.Model):
    """
    A user profile model for maintaining default
    delivery information and order history
    """
    class Meta:
        """ Define Class Spefic Data """
        verbose_name_plural = 'User Profiles'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone_number = models.CharField(max_length=20, null=True, blank=True)
    default_street_address1 = models.CharField(max_length=80, null=True, blank=True)
    default_street_address2 = models.CharField(max_length=80, null=True, blank=True)
    default_town_or_city = models.CharField(max_length=40, null=True, blank=True)
    default_county = models.CharField(max_length=80, null=True, blank=True)
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_country = CountryField(blank_label='Country', null=True, blank=True)

    dob = models.DateField(null=True, blank=True)
    health_conditions = models.TextField(null=True, blank=True)

    fav_class_categories = models.ManyToManyField(ClassCategory, blank=True)
    classes = models.ManyToManyField(SingleExerciseClass, blank=True)

    active_class_package = models.BooleanField(default=False)
    package_name = models.CharField(max_length=30, null=True, blank=True)
    class_package_type = models.CharField(max_length=30, null=True, blank=True)
    class_tokens = models.IntegerField(null=True, blank=True)
    package_expiry = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    def check_package_expired(self):
        """ Check if package assigned to profile has expired """
        if self.active_class_package:
            if date.today() > self.package_expiry:
                self.active_class_package = False
                self.package_name = None
                self.class_package_type = None
                self.class_tokens = None
                self.save()


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.userprofile.save()
