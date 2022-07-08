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

        c_friendly_name = [(c.id, c.get_friendly_name()) for c in categories]
        sc_friendly_name = [(sc.id, sc.get_friendly_name()) for sc in sub_cats]

        self.fields['category'].choices = c_friendly_name
        self.fields['sub_cat'].choices = sc_friendly_name

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'custom-form'
