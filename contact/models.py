import uuid
from django.db import models
from django.contrib.auth.models import User


class ContactMessage(models.Model):
    """ Class for a Message from Signed In User """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message_from = models.CharField(max_length=100, null=False, blank=False)
    reply_email = models.EmailField(null=False, blank=False)
    message_subject = models.CharField(max_length=200, null=False, blank=False)
    message_text = models.TextField(null=False, blank=False)
    message_sent = models.DateTimeField(auto_now_add=True, null=False,
                                        blank=False, editable=False)
