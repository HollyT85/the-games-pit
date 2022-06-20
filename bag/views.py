"""
imports for functionality
"""
from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import messages
from products.models import Product


def view_bag(request):
    """
    Shopping Bag View
    """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """
    Add quantity to bag of product
    """
    product = Product.objects.get(pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity
        messages.success(request, f'Added {product.name} to your bag!')

    request.session['bag'] = bag

    return redirect(redirect_url)


def update_bag(request, item_id):
    """
    update quantity of item in bag
    """
    quantity = int(request.POST.get('quantity'))
    bag = request.session.get('bag', {})

    if quantity > 0:
        bag[item_id] = quantity

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def delete_item(request, item_id):
    """
    delete item in bag
    """
    bag = request.session.get('bag', {})
    bag.pop(item_id)

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))

