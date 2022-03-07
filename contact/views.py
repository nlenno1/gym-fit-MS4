from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import ContactMessageForm
from .models import ContactMessage


def send_contact_message(request):
    """ View to allow users to send a message to admin """

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


@login_required
def delete_contact_message(request, message_id):
    """ View to allow admin to delete a message """

    if not request.user.is_superuser:
        messages.error(request, "Sorry, only Admin allowed")
        return redirect(reverse('home'))

    message = None
    message = ContactMessage.objects.get(id=message_id)
    if message:
        message.delete()
        messages.success(request, "Message Deleted")
    else:
        messages.error(request, "Could not Delete the Message")

    return redirect(reverse('profile'))
