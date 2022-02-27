from django.http import HttpResponse


def StripeWH_Handler:
    """ Handle Stripe Webhooks """

    def __init__(self, request):
        self.request = request
    
    def handle_event(self, event):
        """ Handle a generic or unexpected webhook event """
        return HttpResponse(
            content=f"Webhook recieved: {event['type']}",
            status=200
        )