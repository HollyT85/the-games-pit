from django.db import models

from products.models import Product


class Order(models.Model):
    """
    Order details
    """
    order_number = models.CharField(
        max_length=32, nnull=False, editable=False)
    full_name = models.CharField(max_length=60)
    email = models.EmailField(max_length=254)
    phone = models.IntegerField(
        max_length=12, blank=True, null=True)
    address_line1 = models.CharField(max_length=80)
    address_line2 = models.CharField(
        max_length=80, blank=True, null=True)
    town_city = models.CharField(max_length=80)
    county = models.CharField(max_lenth=80)
    post_code = models.CharField(max_length=8)
    country = models.CharField(
        max_length=30, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    sub_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    delivery_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)


class OrderLineItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    lineitem_total = models.DecimalField(
        max_digits=8, decimal_places=2, editable=False)