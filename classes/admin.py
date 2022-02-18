from django.contrib import admin
from .models import ClassCategory, SingleExerciseClass


class ClassCategoryAdmin(admin.ModelAdmin):
    """ Edit Class for Admin pages """
    list_display = (
        'friendly_name',
    )


class SingleExerciseClassAdmin(admin.ModelAdmin):
    """ Edit Class for Admin pages """
    list_display = (
            'date',
            'start_time',
            'duration',
            'category',
            'instructor',
            'price',
            'max_capacity',
            'ability_level',
        )

    ordering = ('-date', '-start_time')


admin.site.register(ClassCategory, ClassCategoryAdmin)
admin.site.register(SingleExerciseClass, SingleExerciseClassAdmin)
