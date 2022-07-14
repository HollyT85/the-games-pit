"""imports for functionality"""
from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('', views.checkout, name="checkout"),
    path(
        'checkout_success/<order_number>/',
        views.checkout_success, name="checkout_success"),
    path(
        'cache_checkout_info/',
        views.cache_checkout_info, name='cache_checkout_info'),
    path('wh', webhook, name='webhook'),
]
