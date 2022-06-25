"""
imports for functionality
"""
from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    """
    checkout view
    """
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, 'Bag is empty')
        return redirect(reverse('home'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form
    }

    return render(request, template, context)
