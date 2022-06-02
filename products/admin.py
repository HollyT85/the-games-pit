from django.contrib import admin
from .models import Category, Product, SubCat


class ProductsAdmin(admin.ModelAdmin):
    list_display = (
        'category',
        'sub_cat',
        'extra_cat',
        'name',
        'description',
        'in_stock',
        'rrp',
        'price',
        'on_offer',
        'offer_price',
        'image',
        'created'
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'main_cat',
    )


class SubCatAdmin(admin.ModelAdmin):
    list_display = (
        'main_cat',
        'sub_cat'
    )


admin.site.register(Product, ProductsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCat, SubCatAdmin)
