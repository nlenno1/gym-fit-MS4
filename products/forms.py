from django import forms
from .models import ClassAccessPackage


class ClassAccessPackageForm(forms.ModelForm):
    """ Class for Form to create Class Access Packages """
    class Meta:
        """ Update Class Meta Data """
        model = ClassAccessPackage
        fields = ('friendly_name', 'type', 'description',
                  'price', 'duration',
                  'amount_of_tokens', 'image',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'friendly_name': 'Package Name',
            'type': 'Package Type',
            'description': 'Package Description',
            'price': 'Price',
            'duration': 'Duration (days)',
            'amount_of_tokens': 'Amount Of Tokens in Package',
            'image': 'Image Upload',
        }

        self.fields['friendly_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
