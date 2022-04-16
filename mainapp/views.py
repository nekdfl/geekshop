from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.views.generic import DetailView

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

    pagination = Paginator(products, per_page=2)

    try:
        products_pagination = pagination.page(page)
    except PageNotAnInteger:
        products_pagination = pagination.page(1)
    except EmptyPage:
        products_pagination = pagination.page(pagination.num_pages)

    content = {
        "title": "GeekShop - Каталог",
        "categories": ProductCategory.objects.all(),
        "products": products_pagination,
        'current_page': page
    }
    return render(request, 'mainapp/products.html', content)


class ProductDetail(DetailView):
    model = Product
    template_name = "mainapp/detail.html"
