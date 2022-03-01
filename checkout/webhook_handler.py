import json
import time

from django.http import HttpResponse

from products.models import ClassAccessPackage
from classes.models import SingleExerciseClass
from .models import Order, OrderLineItem


class StripeWebhookHandler:
    """ Handle Stripe Webhooks """

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """ Handle a generic or unexpected webhook event """
        return HttpResponse(
            content=f"Unhandled webhook recieved: {event['type']}",
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """ Handle the paymnet_intent.succeeded webhook event """
        # retrieve and store data from the Stripe returned intent object

        intent = event.data.object
        print(intent)

        pid = intent.id
        original_bag = intent.metadata.bag
        save_info = intent.metadata.save_info
        package_data = intent.metadata.package_data
        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        # Clean data in the shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        order_exists = False  # assuming the order doesn't exist
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(  # find an order with exactly the same details
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    grand_total=grand_total,
                    original_bag=original_bag,
                    stripe_pid=pid,
                )
                order_exists = True
                print("ORDER EXISTS IN DATABASE")
                break
            except Order.DoesNotExist:
                print("ORDER NOT FOUND ATTEMPT " + str(attempt))
                attempt += 1
                time.sleep(2)
        if order_exists:
            return HttpResponse(
                    content=f"Webhook recieved: {event['type']} | SUCCESS: Verified the order already exists in the database",
                    status=200
                )
        else:
            order = None
            try:  # generate new order from information in Stripe webhook
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    original_bag=original_bag,
                    stripe_pid=pid,
                )
                bag = json.loads(original_bag)
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
            except Exception as err:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {err}',
                    status=500)
        return HttpResponse(
            content=f"Webhook recieved: {event['type']} | Success: Created order in webhook",
            status=200
        )

    def handle_payment_intent_payment_failed(self, event):
        """ Handle the paymnet_intent.payment_failed webhook event """
        return HttpResponse(
            content=f"Webhook recieved: {event['type']}",
            status=200
        )
