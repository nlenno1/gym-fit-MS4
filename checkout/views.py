from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    """ A view to render the checkout page """
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "You can't checkout as there is nothing in your shopping bag")
        return redirect(reverse('view_bag'))

    order_form = OrderForm()
    template = "checkout/checkout.html"
    context = {
        'order_form': order_form,
    }

    return render(request, template, context)
