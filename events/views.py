"""
imports for functionality
"""
from django.shortcuts import render, get_object_or_404
from .models import Events


def all_events(request):
    
    return render(request, 'events/events.html')


def special_events(request):
    """
    special event details
    """
    events = Events.objects.all()

    context = {
        'events': events,
    }

    return render(request, 'events/special-events.html', context)

