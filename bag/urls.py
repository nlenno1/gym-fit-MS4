from django.urls import path
from . import views

urlpatterns = [
    path("", views.view_bag, name="view_bag"),
    path(
        "add/package/<item_id>",
        views.add_package_to_bag,
        name="add_package_to_bag",
    ),
    path(
        "add/single_class/<item_id>",
        views.add_single_class_to_bag,
        name="add_single_class_to_bag",
    ),
    path(
        "remove/<product_type>/<item_id>",
        views.remove_from_bag,
        name="remove_from_bag",
    ),
]
