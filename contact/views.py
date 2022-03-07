from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import ContactMessageForm


def send_contact_message(request):
    """ View to allow users to create a review """

    form = ContactMessageForm()

    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.message_from = request.user
            new_message.save()
            messages.success(request, "Message sent to Admin")
        else:
            messages.error(request, "Unable to send message. Please check \
                that the form is valid")

        return redirect(reverse('send_contact_message'))

    context = {
        'form': form
    }

    return render(request, 'contact/contact.html', context)
