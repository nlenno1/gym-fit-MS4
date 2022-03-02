from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from .models import UserProfile
from .forms import UserProfileForm

from checkout.models import Order

def profile(request):
    """ Display User Profile """

    profile_object = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile_object)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")

    form = UserProfileForm(instance=profile_object)
    orders = profile_object.orders.all()

    template = "profiles/profile.html"
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True,
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
