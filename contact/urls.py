from django.urls import path
from . import views

urlpatterns = [
     path('', views.send_contact_message, name='send_contact_message'),
]
