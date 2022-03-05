from datetime import date

from django import forms
from profiles.forms import DateInput, TimePickerInput
from .models import ClassCategory, SingleExerciseClass


class ClassCategoryForm(forms.ModelForm):
    """ Class for Form to create Class Access Packages """
    class Meta:
        """ Update Class Meta Data """
        model = ClassCategory
        fields = ('__all__')

    def __init__(self, *args, **kwargs):
        """
        Add  classes and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'


class SingleExerciseClassForm(forms.ModelForm):
    """ Class for Form to create Class Access Packages """
    class Meta:
        """ Update Class Meta Data """
        widgets = {'date': DateInput(),
                   'start_time': TimePickerInput(),
                   'end_time': TimePickerInput(), }
        model = SingleExerciseClass
        exclude = ['remaining_spaces', 'participants', ]
        labels = {
            'duration': 'Duration (mins)*',
        }

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super(SingleExerciseClassForm, self).__init__(*args, **kwargs)

        self.fields['category'].widget.attrs['autofocus'] = True
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
