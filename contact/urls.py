from django.urls import path
from . import views

urlpatterns = [
    path("", views.send_contact_message, name="send_contact_message"),
    path(
        "<message_id>/delete",
        views.delete_contact_message,
        name="delete_contact_message",
    ),
]
