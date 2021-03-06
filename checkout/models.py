import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings

from django_countries.fields import CountryField

from products.models import ClassAccessPackage
from classes.models import SingleExerciseClass
from profiles.models import UserProfile


class Order(models.Model):
    """Model for any Order created"""

    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label="Country *", null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    original_bag = models.TextField(null=False, blank=False, default="")
    stripe_pid = models.CharField(
        max_length=254, null=False, blank=False, default=""
    )

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        self.order_total = (
            self.lineitems.aggregate(Sum("lineitem_total"))[
                "lineitem_total__sum"
            ]
            or 0
        )
        self.grand_total = self.order_total
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    """Model for individual items in an order"""

    order = models.ForeignKey(
        Order,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="lineitems",
    )
    exercise_class = models.ForeignKey(
        SingleExerciseClass, on_delete=models.CASCADE, null=True, blank=True,
    )
    access_package = models.ForeignKey(
        ClassAccessPackage, on_delete=models.CASCADE, null=True, blank=True,
    )
    item_name = models.CharField(
        max_length=100, null=True, blank=True
    )
    lineitem_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, blank=False, editable=False
    )

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        if self.exercise_class:
            self.lineitem_total = self.exercise_class.price
            self.item_name = self.exercise_class.info()
        elif self.access_package:
            self.lineitem_total = self.access_package.price
            self.item_name = self.access_package.friendly_name
        super().save(*args, **kwargs)

    def __str__(self):
        if self.exercise_class:
            description = f"{self.exercise_class.category} \
                on {self.exercise_class.class_date.strftime('%d/%b/%Y')} \
                    at {self.exercise_class.start_time.strftime('%H:%M')}"
            return f"{description} on order \
                {self.order.order_number}"
        elif self.access_package:
            return f"{self.access_package} on order \
                {self.order.order_number}"
