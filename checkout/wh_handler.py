from django.http import HttpResponse


class StripeWH_Handler:
    """
    stripe webhooks
    """
    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        handle unexpected / unknown event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200
        )

    def handle_successful_payment_intent(self, event):
        """
        handle successful payment intent
        """

        intent = event.data.object
        print(intent)

        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )

    def handle_failed_payment_intent(self, event):
        """
        handle failed payment intent
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )
