from django.urls import path
from . import views

urlpatterns = [
    path("", views.view_bag, name="view_bag"),
    path(  # add package to bag
        "package/<item_id>/add",
        views.add_package_to_bag,
        name="add_package_to_bag",
    ),
    path(  # add single class to bag
        "single_class/<item_id>/add",
        views.add_single_class_to_bag,
        name="add_single_class_to_bag",
    ),
    path(  # remove product from bag
        "<product_type>/<item_id>/remove",
        views.remove_from_bag,
        name="remove_from_bag",
    ),
]
