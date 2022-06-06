from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Product


def all_products(request):
    """
    Products page view
    """
    products = Product.objects.all()
    search_term = None

    if request.GET:
        if 'search' in request.GET:
            search_term = request.GET['search']
            if not search_term:
                messages.error(request, "Your search string was blank")
                return redirect(reverse('products'))
            
            results = Q(name__icontains=input) | Q(description__icontains=search_term)
            products = products.filter(results)

    context = {
        'products': products,
        'search_term': search_term,
    }

    return render(request, 'products/products.html', context)


def product_info(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product-info.html', context)

