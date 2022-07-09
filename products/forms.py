from django import forms
from .models import Category, SubCat, Product


class ProductForm(forms.ModelForm):
    """
    form for products for super users
    """
    class Meta:
        """
        all fields from product model required
        """
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = ''
