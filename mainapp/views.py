from django.shortcuts import render

from mainapp.models import ProductCategory, Product


# Create your views here.


def index(request):
    content = {
        "title": "GeekShop"
    }
    return render(request, 'mainapp/index.html', content)


def products(request, id_category=None, page=1):
    if id_category:
        products = Product.objects.filter(category=id_category)
    else:
        products = Product.objects.all()

    content = {
        "title": "GeekShop - Каталог",
        "categories": ProductCategory.objects.all(),
        "products": products

    }
    return render(request, 'mainapp/products.html', content)
