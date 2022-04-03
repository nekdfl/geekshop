from itertools import product
from django.contrib import admin

from mainapp.models import Product, ProductCategory
from authapp.models import User

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(User)
