import datetime
from dateutil.relativedelta import relativedelta

from django import forms
from django.contrib.auth.models import User

from .models import UserProfile


class DateInput(forms.DateInput):
    """Add date picker widget to date field """
    input_type = 'date'


class TimePickerInput(forms.TimeInput):
    """Add time picker widget to time field """
    input_type = 'time'



class UserForm(forms.ModelForm):
    """ Class for all User Profiles """
    class Meta:
        """ Update Class Meta Data """
        model = User
        fields = ('username', 'first_name',
                  'last_name', 'email')

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
        }

        self.fields['username'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False


class UserProfileForm(forms.ModelForm):
    """ Class for all User Profiles """
    class Meta:
        """ Update Class Meta Data """
        widgets = {'dob': DateInput()}
        model = UserProfile
        fields = ('default_phone_number',
                  'default_street_address1', 'default_street_address2',
                  'default_town_or_city',
                  'default_county', 'default_postcode',
                  'default_country', 'dob', 'health_conditions')

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_county': 'County',
            'dob': 'Date Of Birth',
            'health_conditions': 'Medical Conditions',
        }

        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
