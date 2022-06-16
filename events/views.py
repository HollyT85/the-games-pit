"""
imports for functionality
"""
from django.shortcuts import render
from .models import Events


def all_events(request):
    """
    retrieve all events 
    """
    events = Events.objects.all()
    context = {
        'events': events,
    }
    return render(request, 'events/events.html', context)
