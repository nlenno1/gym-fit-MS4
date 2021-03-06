from django.urls import path
from . import views

urlpatterns = [
    path(
        "class_access_packages/",
        views.view_class_access_packages,
        name="view_class_access_packages",
    ),
    path(
        "class_access_package/add/",
        views.add_class_access_package,
        name="add_class_access_package",
    ),
    path(
        "class_access_package/<package_id>/edit/",
        views.edit_class_access_package,
        name="edit_class_access_package",
    ),
    path(
        "class_access_package/<package_id>/delete/",
        views.delete_class_access_package,
        name="delete_class_access_package",
    ),
]
