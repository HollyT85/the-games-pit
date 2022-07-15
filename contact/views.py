"""imports for functionality"""
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.core.mail import send_mail

from django.conf import settings


def contact(request):
    """
    view for contact page (doesn't send)
    """
    if request.method == "POST":

        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        sender_email = settings.EMAIL_HOST_USER

        data = {
            'name': name,
            'email': email,
            'subect': subject,
            'message': message,
        }

        """code from https://www.youtube.com/watch?v=1DcySa35fXw&t=1s"""

        message = '''
        New message: {}

        From: {}
        '''.format(data['message'], data['email'])
        send_mail(data['subject'], message, '', [sender_email])

        messages.success(request, 'Message sent! We will be in touch soon!')
        return redirect(reverse('home'))

    return render(request, 'contact/contact.html')
