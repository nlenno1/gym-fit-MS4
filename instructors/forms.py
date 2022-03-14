from django import forms
from .models import Instructor
from django.forms import CheckboxSelectMultiple


class InstructorForm(forms.ModelForm):
    """Class for Form to create a Review"""

    class Meta:
        """Update Class Meta Data"""

        model = Instructor
        exclude = [
            "name",
        ]
        widgets = {
            "can_lead_classes": CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        """Add  classes and set autofocus on first field"""
        super().__init__(*args, **kwargs)
        labels = {
            "friendly_name": "Name",
        }

        self.fields["friendly_name"].widget.attrs["autofocus"] = True
        for field in labels:
            self.fields[field].label = labels[field]
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f"{self.fields[field].label} *"
                self.fields[field].label += " "
            else:
                placeholder = self.fields[field].label
            self.fields[field].widget.attrs["placeholder"] = placeholder
            self.fields[field].widget.attrs["class"] = "stripe-style-input"
