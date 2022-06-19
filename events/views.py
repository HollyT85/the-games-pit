"""
imports for functionality
"""
from django.shortcuts import render, get_object_or_404
from .models import Events


def all_events(request, event_id):
    """
    Individual product details
    """
    event = get_object_or_404(Events, pk=event_id)

    context = {
        'event': event,
    }

    return render(request, 'events/events.html', context)
