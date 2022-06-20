from django import template

register = template.Library()

@register.filter(name='item_total')
def item_total(price, quantity):
    return price * quantity


@register.filter(name='offer_total')
def offer_total(offer_price, quantity):
    return offer_price * quantity
