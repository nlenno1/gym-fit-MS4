from django.shortcuts import render

from .forms import ContactMessageForm

def send_contact_message(request):
    """ View to allow users to create a review """

    form = ContactMessageForm()

    context = {
        'form': form
    }

    return render(request, 'contact/contact.html', context)
