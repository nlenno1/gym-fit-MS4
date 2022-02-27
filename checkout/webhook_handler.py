from django.http import HttpResponse


class StripeWH_Handler:
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
        return HttpResponse(
            content=f"Webhook recieved: {event['type']}",
            status=200
        )

    def handle_payment_intent_payment_failed(self, event):
        """ Handle the paymnet_intent.payment_failed webhook event """
        return HttpResponse(
            content=f"Webhook recieved: {event['type']}",
            status=200
        )
