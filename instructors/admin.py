from django.contrib import admin
from .models import Instructor


class InstructorAdmin(admin.ModelAdmin):
    """Edit Class for Admin pages"""

    list_display = (
        "friendly_name",
        "display_on_site",
    )

    ordering = ("friendly_name",)


admin.site.register(Instructor, InstructorAdmin)
