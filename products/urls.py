from django.urls import path
from . import views

urlpatterns = [
    path('products/class_access_packages/', views.view_class_access_packages,
         name='view_class_access_packages'),
]
