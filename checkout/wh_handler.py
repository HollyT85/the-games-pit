"""
imports for functionality
"""
import json
import time

from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from products.models import Product
from profiles.models import UserProfile
from .models import Order, OrderLineItem


class StripeWH_Handler:
    """
    stripe webhooks
    """
    def __init__(self, request):
        self.request = request

    def _send_order_conf_email(self, order):
        """
        send customer an order confirmation email
        """
        customer_email = order.email
        email_subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order}
        )
        email_body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL}
        )

        send_mail(
            email_subject,
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            [customer_email]
        )

    def handle_event(self, event):
        """
        Handle an unknown / unusual webhook event
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def handle_successful_payment_intent(self, event):
        """
        handle successful payment intent
        """
        intent = event.data.object
        print(intent.metadata)
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        # blank data if empty
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # update profile if save order checked
        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)
            if save_info:
                profile.default_phone = shipping_details.phone,
                profile.default_address_line1 = shipping_details.address.line1,
                profile.default_address_line2 = shipping_details.address.line2,
                profile.default_town_city = shipping_details.address.city,
                profile.default_county = shipping_details.address.state,
                profile.default_post_code = shipping_details.address.postal_code,
                profile.default_country = shipping_details.address.country,
                profile.save()

        order_exists = False
        # try 5 times
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone__iexact=shipping_details.phone,
                    address_line1__iexact=shipping_details.address.line1,
                    address_line2__iexact=shipping_details.address.line2,
                    town_city__iexact=shipping_details.address.city,
                    county__iexact=shipping_details.address.state,
                    post_code__iexact=shipping_details.address.postal_code,
                    country__iexact=shipping_details.address.country,
                    grand_total=grand_total,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                order_exists = True
                break

            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)

        if order_exists:
            self._send_order_conf_email(order)
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: \
                    Order already in DB',
                status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    user_profile=profile,
                    email=billing_details.email,
                    phone=shipping_details.phone,
                    address_line1=shipping_details.address.line1,
                    address_line2=shipping_details.address.line2,
                    town_city=shipping_details.address.city,
                    county=shipping_details.address.state,
                    post_code=shipping_details.address.postal_code,
                    country=shipping_details.address.country,
                    original_bag=bag,
                    stripe_pid=pid,
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
        self._send_order_conf_email(order)

        return HttpResponse(
            content=f'Webhook received: {event["type"]} | \
                SUCCESS: Order created',
            status=200)

    def handle_failed_payment_intent(self, event):
        """
        handle failed payment intent
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )
