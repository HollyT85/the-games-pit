from django.contrib import admin
from .models import Category, Product, SubCat


class ProductsAdmin(admin.ModelAdmin):
    """
    Display of products
    """
    list_display = (
        'category',
        'sub_cat',
        'extra_cat',
        'name',
        'description',
        'in_stock',
        'on_offer',
        'offer_price',
        'rrp',
        'price',
        'image',
        'created'
    )


class CategoryAdmin(admin.ModelAdmin):
    """
    Display of category
    """
    list_display = (
        'main_cat',
    )


class SubCatAdmin(admin.ModelAdmin):
    """
    Display of sub-category
    """
    list_display = (
        'main_cat',
        'sub_cat'
    )


admin.site.register(Product, ProductsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCat, SubCatAdmin)
