from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone', 'address_line1',
                  'address_line2', 'town_city', 'post_code', 'county',
                  'country')

    def __init__(self, *args, **kwargs):
        """
        iterate through fields starting at full name and remove labels
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone': 'Phone Number',
            'address_line1': 'Address 1',
            'address_line2': 'Address 2(optional)',
            'town_city': 'Town / City',
            'county': 'County',
            'post_code': 'Postcode',
            'country': 'Country',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field] * }'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
