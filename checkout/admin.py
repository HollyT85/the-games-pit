"""
imports for functionality
"""
from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    """
    Make OrderLineItem available in Order
    """
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    """
    Order Admin
    """
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = (
        'order_number', 'date', 'delivery_cost', 'sub_total', 'grand_total')

    fields = (
        'order_number', 'date', 'full_name', 'email', 'phone', 'address_line1',
        'address_line2', 'town_city', 'county', 'post_code', 'country',
        'delivery_cost', 'sub_total', 'grand_total'
    )

    list_display = (
        'order_number', 'date', 'full_name', 'sub_total', 'delivery_cost',
        'grand_total'
    )

    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
