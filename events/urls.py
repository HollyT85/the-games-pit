"""
imports for functionality
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_events, name="all_events"),
    path('special_events/', views.special_events, name="special_events"),
    
]
