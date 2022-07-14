"""imports for functionality"""
from django.shortcuts import render, redirect, reverse
from django.contrib import messages


def contact(request):
    """
    view for contact page (doesn't send)
    """
    if request.method == "POST":

        messages.success(request, 'Message sent! We will be in touch soon!')
        return redirect(reverse('home'))

    return render(request, 'contact/contact.html')
