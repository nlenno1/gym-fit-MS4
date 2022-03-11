from django.contrib import admin
from .models import ContactMessage


class ContactMessageAdmin(admin.ModelAdmin):
    """Edit Class for Admin pages"""

    list_display = (
        "message_from",
        "message_subject",
        "message_text",
        "message_sent",
    )

    ordering = ("-message_sent",)


admin.site.register(ContactMessage, ContactMessageAdmin)
