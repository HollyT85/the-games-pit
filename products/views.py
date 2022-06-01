from django.shortcuts import render
from .models import Products


def products(request):
    """
    Products page view
    """
    products = Products.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)

