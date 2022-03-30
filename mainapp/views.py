import json
from unicodedata import category
from django.shortcuts import render

# Create your views here.


def index(request):
    content = {
        "title": "GeekShop"
    }
    return render(request, 'mainapp/index.html', content)


def products_view(request):

    categories = []
    products = []

    with open("mainapp/fixtures/categories.json") as f:
        categories = json.load(f)

    with open("mainapp/fixtures/products.json") as f:
        products = json.load(f)

    content = {
        "title": "GeekShop - Каталог",
        "categories": categories["category_list"],
        "products": products["goods"]

    }
    return render(request, 'mainapp/products.html', content)
