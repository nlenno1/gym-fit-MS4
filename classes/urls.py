from django.urls import path
from . import views

urlpatterns = [
     path('classes/our_classes/', views.view_class_categories,
          name='view_class_categories'),

     path('classes/class_bookings/', views.view_all_single_classes,
          name='view_all_single_classes'),

     # path('classes/class_bookings/filtered/<category_id>', views.filter_single_classes,
     #      name='filter_single_classes'),
     path('classes/class_bookings/filtered/', views.filter_single_classes,
          name='filter_single_classes'),

     path('classes/class_category/<category_id>',
          views.view_single_class_category, name='view_single_class_category'),
]
