from django.urls import path
from . import views

urlpatterns = [
     path('<int:category_id>/add/', views.create_a_category_review,
          name='create_a_category_review'),
     path('<review_id>/delete/', views.delete_category_review,
          name='delete_category_review'),
]
