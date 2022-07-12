"""
imports for functionality
"""
from django.shortcuts import render
from .models import Events


def all_events(request):
    """
    view for generic event page
    """
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
