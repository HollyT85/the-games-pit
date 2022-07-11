"""
imports for functionality
"""
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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


@login_required
def admin_add_product(request):
    """
    allow superusers to add products
    """
    if not request.user.is_superuser:
        messages.error(request, 'You are not authorised to do this.')
        return redirect(reverse('home'))
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            form.save()
            messages.success(request, 'Product successfully added')
            return redirect(reverse('product_info', args=[product.id]))
        else:
            messages.error(request, 'Product not added; try again')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required()
def admin_edit_product(request, product_id):
    """
    allow superusers to edit a product
    """
    if not request.user.is_superuser:
        messages.error(request, 'You are not authorised to do this.')
        return redirect(reverse('home'))
    
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product successfully edited')
            return redirect(reverse('product_info', args=[product.id]))
        else:
            messages.error(request, 'Product not edited; try again')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product
    }

    return render(request, template, context)


@login_required
def admin_delete_product(request, product_id):
    """
    allow superuser to delete product
    """
    if not request.user.is_superuser:
        messages.error(request, 'You are not authorised to do this.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product successfully deleted')
    return redirect(reverse('home'))