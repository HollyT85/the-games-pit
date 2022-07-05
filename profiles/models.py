"""
imports for functionality
"""
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    user profile; see previous orders
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone = models.CharField(
        max_length=12, blank=True, null=True)
    default_address_line1 = models.CharField(
        max_length=80, blank=True, null=True)
    default_address_line2 = models.CharField(
        max_length=80, blank=True, null=True)
    default_town_city = models.CharField(
        max_length=80, blank=True, null=True)
    default_county = models.CharField(
        max_length=80, blank=True, null=True)
    default_post_code = models.CharField(
        max_length=8, blank=True, null=True)
    default_country = models.CharField(
        max_length=30, blank=True, null=True, default='GB')

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_update_profile(sender, instance, created, **kwargs):
    """
    create / update user's profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    # if already exists, just update it
    instance.userprofile.save()
