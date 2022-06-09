from django.shortcuts import render


def view_bag(request):
    """
    Shopping Bag View
    """
    return render(request, 'bag/bag.html')
