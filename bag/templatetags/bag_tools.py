from django import template

register = template.Library()


def item_total(price, quantity):
    return price * quantity


def offer_price(offer_price, quantity):
    return offer_price * quantity
