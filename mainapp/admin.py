from django.contrib import admin

# Register your models here.
from mainapp.models import Product, ProductCategory

admin.site.register(ProductCategory)


# admin.site.register(Product)

@admin.register(Product)
class Product(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantily', 'category',)
    fields = ('name', 'image', 'description', ('price', 'quantily'), 'category',)
    readonly_fields = ('description',)
    ordering = ('name', 'price',)
    search_fields = ('name',)
