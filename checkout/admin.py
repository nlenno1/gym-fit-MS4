from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    """Class to allow admin to add a new order line item"""

    model = OrderLineItem
    readonly_fields = ("lineitem_total", "item_name")


class OrderAdmin(admin.ModelAdmin):
    """Class to allow admin to view orders"""

    inlines = (OrderLineItemAdminInline,)
    readonly_fields = (
        "order_number",
        "order_date",
        "grand_total",
        "original_bag",
        "stripe_pid",
    )

    fields = (
        "order_number",
        "user_profile",
        "order_date",
        "full_name",
        "email",
        "phone_number",
        "country",
        "postcode",
        "town_or_city",
        "street_address1",
        "street_address2",
        "county",
        "grand_total",
        "original_bag",
        "stripe_pid",
    )

    list_display = (
        "order_number",
        "order_date",
        "full_name",
        "grand_total",
    )

    ordering = ("-order_date",)


admin.site.register(Order, OrderAdmin)
