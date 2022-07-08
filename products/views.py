"""
imports for functionality
"""
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Product, Category, SubCat
from .forms import ProductForm


def all_products(request):
    """
    View all products
    """
    products = Product.objects.all()
    search_term = None
    category = None
    sort = None
    direction = None

    if request.GET:
        # sorting functionality
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)
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
                messages.error(request, f'No search term entered.')
                return redirect(reverse('home'))

            results = Q(
                name__icontains=search_term) | Q(
                    description__icontains=search_term)
            products = products.filter(results)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': search_term,
        'category': category,
        'subcat': category,
        'current_sorting': current_sorting,
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


def sale(request):
    """
    Filter by sale products
    """
    products = Product.objects.all().filter(on_offer=True)
    context = {
        'products': products,
    }
    return render(request, 'products/products.html', context)


def admin_add_product(request):
    """
    allow superusers to add products
    """
    form = ProductForm()
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
