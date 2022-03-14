from django import forms
from profiles.forms import DateInput, TimePickerInput
from .models import ClassCategory, SingleExerciseClass


class ClassCategoryForm(forms.ModelForm):
    """Class for Form to create Class Access Packages"""

    class Meta:
        """Update Class Meta Data"""

        model = ClassCategory
        exclude = [
            "name",
        ]

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
                self.fields[field].label += " "
                placeholder = f"{self.fields[field].label} *"
            else:
                placeholder = self.fields[field].label
            self.fields[field].widget.attrs["placeholder"] = placeholder
            self.fields[field].widget.attrs["class"] = "stripe-style-input"


class SingleExerciseClassForm(forms.ModelForm):
    """Class for Form to create Class Access Packages"""

    weekly_class = forms.BooleanField(required=False)
    weekly_classes_until = forms.DateField(widget=DateInput(), required=False)

    class Meta:
        """Update Class Meta Data"""

        widgets = {
            "class_date": DateInput(),
            "start_time": TimePickerInput(),
            "end_time": TimePickerInput(),
        }
        model = SingleExerciseClass
        exclude = [
            "remaining_spaces",
            "participants",
            "end_time",
        ]

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super(SingleExerciseClassForm, self).__init__(*args, **kwargs)
        labels = {
            "duration": "Duration (mins) *",
        }
        
        self.fields["category"].widget.attrs["autofocus"] = True
        for field in labels:
            self.fields[field].label = labels[field]
        for field in self.fields:
            if self.fields[field].required:
                self.fields[field].label += " "
                placeholder = f"{self.fields[field].label} *"
            else:
                placeholder = self.fields[field].label
            self.fields[field].widget.attrs["placeholder"] = placeholder
            self.fields[field].widget.attrs["class"] = "stripe-style-input"
