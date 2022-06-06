"""
imports for functionality
"""
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category, SubCat


def all_products(request):
    """
    View all products
    """
    products = Product.objects.all()
    search_term = None
    category = None

    if request.GET:
        # filter functionality - main category
        if 'category' in request.GET:
            category = request.GET['category'].split(',')
            products = products.filter(category__main_cat__in=category)
            category = Category.objects.filter(main_cat__in=category)
        # filter functionality - sub-category
        if 'sub_cat' in request.GET:
            category = request.GET['sub_cat'].split(',')
            products = products.filter(sub_cat__sub_cat__in=category)
            category = SubCat.objects.filter(sub_cat__in=category)
        # Search functionality
        if 'search' in request.GET:
            search_term = request.GET['search']
            if not search_term:
                messages.error(request, "Your search string was blank")
                return redirect(reverse('products'))

            results = Q(
                name__icontains=input) | Q(description__icontains=search_term)
            products = products.filter(results)

    context = {
        'products': products,
        'search_term': search_term,
        'category': category,
        'subcat': category,
    }

    return render(request, 'products/products.html', context)


def product_info(request, product_id):
    """
    Individual product details
    """
    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product-info.html', context)
