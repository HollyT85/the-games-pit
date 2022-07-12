"""
imports for functionality
"""
from django.shortcuts import (
    render, redirect, reverse, HttpResponse, get_object_or_404)
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
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
        messages.success(
            request, f'You now have {bag[item_id]} {product.name} \
                in your bag!')
    else:
        bag[item_id] = quantity
        messages.success(request, f'Added {product.name} to your bag!')

    request.session['bag'] = bag

    return redirect(redirect_url)


def update_bag(request, item_id):
    """
    update quantity of item in bag
    """
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    bag = request.session.get('bag', {})

    if quantity > 0:
        bag[item_id] = quantity
        messages.success(
            request, f'You now have {bag[item_id]} {product.name} \
                in your bag!')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def delete_item(request, item_id):
    """
    delete item in bag
    """

    try:
        product = get_object_or_404(Product, pk=item_id)
        bag = request.session.get('bag', {})

        bag.pop(item_id)
        messages.success(request, f'Removed {product.name} from your bag!')

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Something has gone wrong removing {e}.')
        return HttpResponse(status=500)
