from django import forms
from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    """ Class for Form for User to send a Message """
    class Meta:
        """ Update Class Meta Data """
        model = ContactMessage
        exclude = ['message_from', 'reply_email',]
        labels = {
            'message_subject': 'Message Subject',
            'message_text': 'Message'
        }

    def __init__(self, *args, **kwargs):
        """ Add  classes and set autofocus on first field """
        super().__init__(*args, **kwargs)
        self.fields['message_subject'].widget.attrs['autofocus'] = True
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'


class GuestContactMessageForm(forms.ModelForm):
    """ Class for Form for Guest to send a Message """
    class Meta:
        """ Update Class Meta Data """
        model = ContactMessage
        fields = ('__all__')
        labels = {
            'message_from': 'Full Name',
            'reply_email': 'Email',
            'message_subject': 'Message Subject',
            'message_text': 'Message',
        }

    def __init__(self, *args, **kwargs):
        """ Add  classes and set autofocus on first field """
        super().__init__(*args, **kwargs)
        self.fields['message_from'].widget.attrs['autofocus'] = True
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
