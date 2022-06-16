from django.contrib import admin
from .models import Events


class EventsAdmin(admin.ModelAdmin):
    """
    Display of event categories
    """
    list_display = (
        'name',
        'description',
        'date',
        'time',
    )