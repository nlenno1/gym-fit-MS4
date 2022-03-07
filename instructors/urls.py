from django.urls import path
from . import views

urlpatterns = [
     path('add/', views.add_an_instructor, name='add_an_instructor'),
]
