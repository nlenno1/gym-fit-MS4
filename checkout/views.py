from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

import stripe

from bag.contexts import bag_contents
from .forms import OrderForm


def checkout(request):
    """ A view to render the checkout page """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "You can't checkout as there is nothing in your shopping bag")
        return redirect(reverse('view_bag'))

    current_bag = bag_contents(request)
    grand_total = current_bag['total']
    stripe_total = round(grand_total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY
    )

    order_form = OrderForm()

    if not stripe_public_key:
        message.warning(request, "Stripe Public Key is missing. Please set it \
            and try again")
    template = "checkout/checkout.html"
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)
