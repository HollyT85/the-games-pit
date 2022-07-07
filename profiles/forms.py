"""
imports for functionality
"""
from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    """
    user profile form model
    """
    class Meta:
        """
        fields in order form
        """
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        iterate through fields starting at full name and remove labels
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone': 'Phone Number',
            'default_address_line1': 'Address 1',
            'default_address_line2': 'Address 2(optional)',
            'default_town_city': 'Town / City',
            'default_county': 'County',
            'default_post_code': 'Postcode',
            'default_country': 'Country',
        }

        self.fields['default_phone'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'custom-form'
            self.fields[field].label = False
