from django.urls import path
from . import views

urlpatterns = [
     path('our_classes/', views.view_class_categories,
          name='view_class_categories'),
     path('class_category/<int:category_id>',
          views.view_single_class_category, name='view_single_class_category'),
     path('class_category/add',
          views.add_class_category, name='add_class_category'),
     path('class_category/<category_id>/edit',
          views.edit_class_category, name='edit_class_category'),
     path('class_category/<category_id>/delete',
          views.delete_class_category, name='delete_class_category'),

     path('classes_this_week/', views.classes_this_week,
          name='classes_this_week'),


     path('single_classes/', views.filter_single_classes,
          name='filter_single_classes'),

     path('single_class/add',
          views.add_single_exercise_class, name='add_single_exercise_class'),
     # path('single_class/<class_id>/edit',
     #      views.edit_single_exercise_class, name='edit_single_exercise_class'),
     # path('single_class/<class_id>/delete',
     #      views.delete_single_exercise_class, name='delete_single_exercise_class'),
]
