from django.urls import path
from . import views

urlpatterns = [
    path(  # view all class categories
        "our_classes/",
        views.view_class_categories,
        name="view_class_categories",
    ),
    path(  # view class category details
        "class_category/<int:category_id>",
        views.view_single_class_category,
        name="view_single_class_category",
    ),
    # class category CRD
    path(
        "class_category/add",
        views.add_class_category,
        name="add_class_category",
    ),
    path(
        "class_category/<int:category_id>/edit",
        views.edit_class_category,
        name="edit_class_category",
    ),
    path(
        "class_category/<int:category_id>/delete",
        views.delete_class_category,
        name="delete_class_category",
    ),
    # Class Category Favourites List Control
    path(
        "class_category/favourites/<category_id>/add",
        views.add_category_to_favs,
        name="add_category_to_favs",
    ),
    path(
        "class_category/favourites/<category_id>/remove",
        views.remove_category_from_favs,
        name="remove_category_from_favs",
    ),
    path(  # view classes this week
        "classes_this_week/", views.classes_this_week, name="classes_this_week"
    ),
    path(  # view classes by day
        "classes_by_day/",
        views.filter_single_classes,
        name="filter_single_classes",
    ),
    # Single Exercise Class CRD
    path(
        "single_class/add",
        views.add_single_exercise_class,
        name="add_single_exercise_class",
    ),
    path(
        "single_class/<class_id>/edit",
        views.edit_single_exercise_class,
        name="edit_single_exercise_class",
    ),
    path(
        "single_class/<class_id>/delete",
        views.delete_single_exercise_class,
        name="delete_single_exercise_class",
    ),
    # Book and Cancel Single Exercise Classes
    path(
        "single_class/<class_id>/book",
        views.book_with_package,
        name="book_with_package",
    ),
    path(
        "single_class/<class_id>/cancel",
        views.cancel_class_booking,
        name="cancel_class_booking",
    ),
]
