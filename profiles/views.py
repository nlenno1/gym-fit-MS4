from datetime import date

from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User

from checkout.models import Order
from .models import UserProfile

from .forms import UserProfileForm, UserForm


def profile(request):
    """ Display User Profile """

    profile_object = get_object_or_404(UserProfile, user=request.user)
    user_object = get_object_or_404(User, id=request.user.id)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile_object)
        user_form = UserForm(request.POST, instance=user_object)
        if form.is_valid() and user_form.is_valid():
            form.save()
            user_form.save()
            messages.success(request, "Profile updated successfully")

    form = UserProfileForm(instance=profile_object)
    user_form = UserForm(instance=user_object)
    orders = profile_object.orders.all().order_by('-order_date')

    upcoming_classes = []
    previous_classes = []
    for item in profile_object.classes.order_by("-date"):
        if item.date < date.today():
            previous_classes.append(item)
        else:
            upcoming_classes.append(item)

    template = "profiles/profile.html"
    context = {
        'form': form,
        'user_form': user_form,
        'orders': orders,
        'on_profile_page': True,
        'profile': profile_object,
        'upcoming_classes': upcoming_classes,
        'previous_classes': previous_classes,
    }

    return render(request, template, context)


def order_history(request, order_number):
    """ Display Previous Orders """
    order = get_object_or_404(Order, order_number=order_number)  # Find the order
    # Message to tell user that this is a previous order
    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))
    # store required data and render
    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)
