from django.db import models
from django.core.validators import MaxValueValidator


class ClassAccessPackage(models.Model):
    """Class for the Class Access Package Product"""

    class Meta:
        """Update Meta data for model"""

        verbose_name_plural = "Class Access Packages"

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    sku = models.CharField(max_length=254, null=True, blank=True)
    type = models.CharField(
        max_length=30,
        choices=[("UU", "Unlimited Use"), ("TK", "Token Package")],
        null=True,
        blank=True,
    )
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    duration = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(365)]
    )
    amount_of_tokens = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(50)], null=True, blank=True
    )
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        """Return name string"""
        return self.name

    def get_friendly_name(self):
        """Return friendly_name string"""
        return self.friendly_name
