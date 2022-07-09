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
        sub_cats = SubCat.objects.all()

        self.fields['category'].choices = categories
        self.fields['sub_cat'].choices = sub_cats

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = ''
