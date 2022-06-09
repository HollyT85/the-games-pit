from decimal import Decimal
from django.conf import settings

def bag_contents(request):

    bag_items = []
    total = 0
    no_of_products = 0

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY)
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