from django.urls import path
from . import views

urlpatterns = [
    path('classes/our_classes/', views.view_class_categories,
         name='view_class_categories'),
    path('classes/class_bookings/', views.view_all_single_classes,
         name='view_all_single_classes'),
]
