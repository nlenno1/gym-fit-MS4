import json
from datetime import date, timedelta

from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

import stripe

from bag.contexts import bag_contents
from products.models import ClassAccessPackage
from classes.models import SingleExerciseClass
from .forms import OrderForm
from .models import OrderLineItem, Order


@require_POST
def cache_checkout_data(request):
    """ View to temp save checkout data """
    try:
        #  check if the order includes a class access package
        package_data = {}
        current_bag = bag_contents(request)
        package = current_bag['bag_items']['class_access_package']
        if package:  # add required data to dict
            package_data['type'] = package.type
            package_data['unlimited_tokens'] = package.unlimited_tokens
            package_data['amount_of_tokens'] = package.amount_of_tokens
            package_data['expiry_date'] = (date.today() + timedelta(days=package.duration)).strftime("%d/%m/%Y")
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
            'package_data': json.dumps(package_data),
        })
        return HttpResponse(status=200)
    except Exception as err:
        messages.error(request, "Sorry, your payment can't be processed \
            right now. Please try again later.")
        return HttpResponse(content=err, status=400)

def checkout(request):
    """ A view to render the checkout page """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == "POST":
        bag = request.session.get('bag', {})

        form_data = {  # gather data from POST method
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():  # save order_form if valid
            order = order_form.save()

            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            order.save()

            if bag['class_access_package']:
                try:
                    package = ClassAccessPackage.objects.get(id=bag['class_access_package'])
                    order_line_item = OrderLineItem(
                            order=order,
                            access_package=package,
                        )
                    order_line_item.save()
                except package.DoesNotExist:
                    messages.error(request, (
                        "The Class Access Package in your bag wasn't found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_bag'))

            print(bag['single_classes'])
            for item_id in bag['single_classes']:
                try:
                    exercise_class = SingleExerciseClass.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                            order=order,
                            exercise_class=exercise_class,
                        )
                    order_line_item.save()
                except exercise_class.DoesNotExist:
                    messages.error(request, (
                        "One of the Exercise Classes in your bag wasn't found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_bag'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')

    else:
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


def checkout_success(request, order_number):
    """ Handle sucessful checkouts"""
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f"Order sucessfully processed! {chr(10)}\
        Your order number is {order_number}.{chr(10)}A confirmation email will be sent \
            to {order.email}.")

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order
    }

    return render(request, template, context)
