from django.contrib import admin
from .models import ClassAccessPackage

class ClassAccessPackageAdmin(admin.ModelAdmin):
    """ Edit Class for Admin pages """
    list_display = (
            'friendly_name',
            'type',
            'price',
            'duration',
        )

    ordering = ('type', 'friendly_name')


admin.site.register(ClassAccessPackage, ClassAccessPackageAdmin)
