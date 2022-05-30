from django.contrib import admin
from .models import Category, Products, SubCat


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


admin.site.register(Products, ProductsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCat, SubCatAdmin)
