"""Imports for functionality"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home")
]
