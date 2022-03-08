from django.urls import path
from . import views

urlpatterns = [
     path('instructor_management/', views.instructor_management,
          name='instructor_management'),
     path('instructor_management/add/', views.add_an_instructor,
          name='add_an_instructor'),
     path('instructor_management/<instructor_id>/edit/', views.edit_instructor,
          name='edit_instructor'),
     path('instructor_management/<instructor_id>/delete/',
          views.delete_instructor, name='delete_instructor'),
]
