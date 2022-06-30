from django.http import HttpResponse

from .models import Order, OrderLineItem
from products.models import Product

import json
import time


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
        piid = intent.id
        bag = intent.metadata.bag
        save_order = intent.metadata.save_order

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.data.charges[0].amount / 100, 2)

        # blank data if empty
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=shipping_details.email,
                    phone__iexact=shipping_details.phone,
                    address_line1__iexact=shipping_details.line1,
                    address_line2__iexact=shipping_details.line2,
                    town_city__iexact=shipping_details.city,
                    county__iexact=shipping_details.state,
                    post_code__iexact=shipping_details.postal_code,
                    country__iexact=shipping_details.country,
                    grand_total=grand_total,
                    original_bag=bag,
                    stripe_piid=piid
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
                    full_name=shipping_details.name,
                    email=shipping_details.email,
                    phone=shipping_details.phone,
                    address_line1=shipping_details.line1,
                    address_line2=shipping_details.line2,
                    town_city=shipping_details.city,
                    county=shipping_details.state,
                    post_code=shipping_details.postal_code,
                    country=shipping_details.country,
                    original_bag=bag,
                    stripe_piid=piid
                )
                product = Product.objects.get(id=item_id)
                for item_id, item_data in json.loads(bag).items():
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
