from datetime import date

from django import forms
from .models import ClassCategoryReview


class ClassCategoryReviewForm(forms.ModelForm):
    """ Class for Form to create Class Access Packages """
    class Meta:
        """ Update Class Meta Data """
        model = ClassCategoryReview
        fields = ['review_text',  'review_rating', ]
        labels = {
            'review_rating': 'Review Rating (out of 5)',
        }

    def __init__(self, *args, **kwargs):
        """ Add  classes and set autofocus on first field """
        super().__init__(*args, **kwargs)
        self.fields['review_text'].widget.attrs['autofocus'] = True
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
