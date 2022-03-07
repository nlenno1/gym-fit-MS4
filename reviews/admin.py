from django.contrib import admin
from .models import ClassCategoryReview


class ClassCategoryReviewAdmin(admin.ModelAdmin):
    """ Edit Class for Admin pages """

    list_display = (
            'created_on',
            'author',
            'review_subject',
            'review_rating',
        )

    ordering = ('-created_on',)


admin.site.register(ClassCategoryReview, ClassCategoryReviewAdmin)
