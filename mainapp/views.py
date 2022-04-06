import json
from django.shortcuts import render

from mainapp.models import ProductCategory, Product
# Create your views here.


def index(request):
    content = {
        "title": "GeekShop"
    }
    return render(request, 'mainapp/index.html', content)


def products_view(request):

    content = {
        "title": "GeekShop - Каталог",
        "categories": ProductCategory.objects.all(),
        "products": Product.objects.all()

    }
    return render(request, 'mainapp/products.html', content)
