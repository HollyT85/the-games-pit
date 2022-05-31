from django.db import models


class Category(models.Model):
    main_cat = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.main_cat


class SubCat(models.Model):
    main_cat = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    sub_cat = models.CharField(max_length=255)

    def __str__(self):
        return self.sub_cat


class Products(models.Model):
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    sub_cat = models.ForeignKey(
        'SubCat', null=True, blank=True, on_delete=models.SET_NULL)
    extra_cat = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    in_stock = models.BooleanField(default=True)
    rrp = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(upload_to='images/')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.name
