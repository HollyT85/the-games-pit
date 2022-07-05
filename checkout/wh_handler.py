"""
imports for functionality
"""
import json
import time

from django.http import HttpResponse

from products.models import Product
from .models import Order, OrderLineItem


class StripeWHHandler:
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
        piid = intent.id
        bag = intent.metadata.bag
        save_order = intent.metadata.save_order

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        # blank data if empty
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        order_exists = False
        # try 5 times
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    address_line1__iexact=shipping_details.address.line1,
                    address_line2__iexact=shipping_details.address.line2,
                    town_city__iexact=shipping_details.address.city,
                    county__iexact=shipping_details.address.state,
                    post_code__iexact=shipping_details.address.postal_code,
                    country__iexact=shipping_details.address.country,
                    grand_total=grand_total,
                    original_bag=bag,
                    stripe_piid=piid,
                )
                order_exists = True
                break

            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Order already in DB',
                status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    address_line1__iexact=shipping_details.address.line1,
                    address_line2__iexact=shipping_details.address.line2,
                    town_city__iexact=shipping_details.address.city,
                    county__iexact=shipping_details.address.state,
                    post_code__iexact=shipping_details.address.postal_code,
                    country__iexact=shipping_details.address.country,
                    original_bag=bag,
                    stripe_piid=piid,
                )
                for item_id, item_data in json.loads(bag).items():
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()

            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)

        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Order created',
            status=200)

    def handle_failed_payment_intent(self, event):
        """
        handle failed payment intent
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )
