"""
imports for functionality
"""
from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def bag_contents(request):
    """
    get bag contents, calculate delivery total and grand total
    """
    bag_items = []
    total = 0
    no_of_products = 0
    bag = request.session.get('bag', {})

    for item_id, quantity in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        if product.on_offer:
            total += quantity * product.offer_price
        else:
            total += quantity * product.price

        no_of_products += quantity
        bag_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
        })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY / 100)
        free_delivery_in = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_in = 0

    grand_total = delivery + total

    context = {
        'bag_items': bag_items,
        'total': total,
        'no_of_products': no_of_products,
        'delivery': delivery,
        'free_delivery_in': free_delivery_in,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total
    }

    return context
