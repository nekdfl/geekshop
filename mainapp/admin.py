from django.contrib import admin

# Register your models here.
from mainapp.models import Product, ProductCategory

admin.site.register(ProductCategory)
admin.site.register(Product)