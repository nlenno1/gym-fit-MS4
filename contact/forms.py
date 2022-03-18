from django import forms
from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    """Class for Form for User to send a Message"""

    class Meta:
        """Update Class Meta Data"""

        model = ContactMessage
        exclude = [
            "message_from",
            "reply_email",
        ]

    def __init__(self, *args, **kwargs):
        """Add  classes and set autofocus on first field"""
        super().__init__(*args, **kwargs)
        labels = {
            "message_subject": "Message Subject",
            "message_text": "Message",
        }

        self.fields["message_subject"].widget.attrs["autofocus"] = True
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


class GuestContactMessageForm(forms.ModelForm):
    """Class for Form for Guest to send a Message"""

    class Meta:
        """Update Class Meta Data"""

        model = ContactMessage
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        """Add  classes and set autofocus on first field"""
        super().__init__(*args, **kwargs)
        labels = {
            "message_from": "Full Name",
            "reply_email": "Email",
            "message_subject": "Message Subject",
            "message_text": "Message",
        }

        self.fields["message_from"].widget.attrs["autofocus"] = True
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
