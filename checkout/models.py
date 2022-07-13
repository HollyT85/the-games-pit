"""
generate order number
"""
import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings

from products.models import Product
from profiles.models import UserProfile


class Order(models.Model):
    """
    Order details
    """
    order_number = models.CharField(
        max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='orders')
    full_name = models.CharField(max_length=60)
    email = models.EmailField(max_length=254)
    phone = models.CharField(
        max_length=12, blank=True, null=True)
    address_line1 = models.CharField(max_length=80)
    address_line2 = models.CharField(
        max_length=80, blank=True, null=True)
    town_city = models.CharField(max_length=80)
    county = models.CharField(max_length=80)
    post_code = models.CharField(max_length=8)
    country = models.CharField(
        max_length=30, blank=False, null=False, default='GB')
    date = models.DateTimeField(auto_now_add=True)
    sub_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    delivery_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    original_bag = models.TextField(default='')
    stripe_pid = models.CharField(max_length=254, default='')

    def _generate_order_number(self):
        """
        generate random, unique order number
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        update total with each new line of items added
        """
        self.sub_total = self.lineitems.aggregate(
            Sum('lineitem_total'))['lineitem_total__sum'] or 0

        if self.sub_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = self.sub_total * settings.STANDARD_DELIVERY / 100
        else:
            self.delivery_cost = 0
        self.grand_total = self.sub_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """
        override default save method so an order number can be set
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, *kwargs)

        def __str__(self):
            return self.order_number


class OrderLineItem(models.Model):
    """
    order line item details - for each individual product
    """
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(
        Product, null=False, blank=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    lineitem_total = models.DecimalField(
        max_digits=8, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        """
        Override save to update lineitem and subtotals
        """
        if self.product.on_offer:
            self.lineitem_total = self.product.offer_price * self.quantity
        else:
            self.lineitem_total = self.product.price * self.quantity
        super().save(*args, *kwargs)

        def __str__(self):
            return f'{self.product.name} on order {self.order.order_number}'
