"""
imports for functionality
"""
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from bag.contexts import bag_contents
from .forms import OrderForm

import stripe


def checkout(request):
    """
    checkout view
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, 'Bag is empty')
        return redirect(reverse('home'))

    current_order = bag_contents(request)
    total = current_order['grand_total']
    stripe_total = round(total*100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY
    )

    if not stripe_public_key:
        messages.warning(request, 'No public key for stripe')

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret
    }

    return render(request, template, context)
