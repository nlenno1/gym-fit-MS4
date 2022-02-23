from django.urls import path
from . import views

urlpatterns = [
     path('our_classes/', views.view_class_categories,
          name='view_class_categories'),

     path('single_classes/', views.filter_single_classes,
          name='filter_single_classes'),

     path('classes_this_week/', views.classes_this_week,
          name='classes_this_week'),

     path('class_category/<category_id>',
          views.view_single_class_category, name='view_single_class_category'),
]
