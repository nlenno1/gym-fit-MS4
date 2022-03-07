from django import forms
from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    """ Class for Form to create a Review """
    class Meta:
        """ Update Class Meta Data """
        model = ContactMessage
        exclude = ['message_from',]

    def __init__(self, *args, **kwargs):
        """ Add  classes and set autofocus on first field """
        super().__init__(*args, **kwargs)
        self.fields['message_subject'].widget.attrs['autofocus'] = True
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
