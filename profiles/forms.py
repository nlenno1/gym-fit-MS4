from django import forms
from django.contrib.auth.models import User

from .models import UserProfile


class DateInput(forms.DateInput):
    """Add date picker widget to date field"""
    # Date Widget From Youtube Tutorial
    # (https://www.youtube.com/watch?v=I2-JYxnSiB0)

    input_type = "date"


class TimePickerInput(forms.TimeInput):
    """Add time picker widget to time field"""
    # Time Widget From Nancy Lin's Blog
    # (For link see README Credits)
    input_type = "time"


class UserForm(forms.ModelForm):
    """Class for all User Profiles"""

    class Meta:
        """Update Class Meta Data"""

        model = User
        fields = ("username", "first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        labels = {
            "username": "Username",
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "Email",
        }

        for field in self.fields:
            self.fields[field].label = labels[field] + " "
            if self.fields[field].required:
                placeholder = f"{labels[field]} *"
            else:
                placeholder = labels[field]
            self.fields[field].widget.attrs["placeholder"] = placeholder
            self.fields[field].widget.attrs["placeholder"] = placeholder
            self.fields[field].widget.attrs["class"] = "stripe-style-input"


class UserProfileForm(forms.ModelForm):
    """Class for all User Profiles"""

    class Meta:
        """Update Class Meta Data"""

        widgets = {"dob": DateInput()}
        model = UserProfile
        fields = (
            "default_phone_number",
            "default_street_address1",
            "default_street_address2",
            "default_town_or_city",
            "default_county",
            "default_postcode",
            "default_country",
            "dob",
            "health_conditions",
        )

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        labels = {
            "default_phone_number": "Phone Number",
            "default_postcode": "Postal Code",
            "default_town_or_city": "Town or City",
            "default_street_address1": "Street Address 1",
            "default_street_address2": "Street Address 2",
            "default_county": "County",
            "health_conditions": "Medical Conditions",
        }

        self.fields["default_phone_number"].widget.attrs["autofocus"] = True
        for field in self.fields:
            if field != "default_country" and field != "dob":
                self.fields[field].label = labels[field] + " "
                if self.fields[field].required:
                    placeholder = f"{labels[field]} *"
                else:
                    placeholder = labels[field]
                self.fields[field].widget.attrs["placeholder"] = placeholder
                self.fields[field].label = placeholder
            self.fields[field].widget.attrs["class"] = "stripe-style-input"
        self.fields["dob"].label = "Date of Birth"
        self.fields["default_country"].label = "Country"
