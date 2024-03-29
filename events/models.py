"""
import db for functionality
"""
from django.db import models


class Events(models.Model):
    """
    category model
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    class Meta:
        """
        correct incorrect spelling of events
        """
        verbose_name_plural = 'Events'

    def __str__(self):
        return self.name
