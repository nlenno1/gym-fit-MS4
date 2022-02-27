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
        'stripe_public_key': 'pk_test_51KXTSbCu2tiFYO49Y8LdZAtdhoxIZM1PWn6cOnx4hGJ4idl8KlUQvqjXDouuwnnCFH6l1rWOyjyjSVXB5p7MfUeu00k5OPvskJ',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)
