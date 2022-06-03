from django.conf import settings
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, TemplateView, ListView

from common.mixins import BaseClassContextMixin
from mainapp.models import ProductCategory, Product


def get_link_category():
    if settings.LOW_CACHE:
        key = 'link_category'
        link_category = cache.get(key)
        if link_category is None:
            link_category = ProductCategory.objects.all()
            cache.set(key, link_category)
        return link_category
    else:
        return ProductCategory.objects.all()


def get_product(category, page):
    # fix me : how to use it?
    # queryset = get_product(id_category, self.page)
    if category:
        if settings.LOW_CACHE:
            key = f'link_product{category}{page}'
            link_product = cache.get(key)
            if link_product is None:
                link_product = Product.objects.filter(category_id=category).select_related('category')
                cache.set(key, link_product)
            return link_product
        else:
            return Product.objects.filter(category_id=category).select_related('category')
    else:
        if settings.LOW_CACHE:
            key = 'link_product'
            link_product = cache.get(key)
            if link_product is None:
                link_product = Product.objects.all().select_related('category')
                cache.set(key, link_product)
            return link_product
        else:
            return Product.objects.all().select_related('category')


def get_product_(pk):
    if settings.LOW_CACHE:
        key = f'product{pk}'
        product = cache.get(key)
        if product is None:
            product = Product.objects.get(id=pk)
            cache.set(key, product)
        return product
    else:
        return Product.objects.get(id=pk)


# Create your views here.
@method_decorator(cache_page(60 * 60), name='get')
class IndexTemplateView(TemplateView, BaseClassContextMixin):
    template_name = 'mainapp/index.html'
    title = "GeekShop"


@method_decorator(cache_page(60 * 60), name='get')
class ProductListView(ListView, BaseClassContextMixin):
    model = Product
    context_object_name = 'products'
    template_name = 'mainapp/products.html'
    paginate_by = 6

    def get_queryset(self):
        id_category = self.kwargs.get('id_category')

        if id_category:
            queryset = Product.objects.filter(category_id=id_category).select_related()
            # fix me : how to use it?
            # queryset = get_product(id_category, self.page)
        else:
            queryset = Product.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['categories'] = get_link_category()
        current_page = self.kwargs.get('page')
        context['current_page'] = current_page

        # try:
        #     products_pagination = pagination.page(page)
        # except PageNotAnInteger:
        #     products_pagination = pagination.page(1)
        # except EmptyPage:
        #     products_pagination = pagination.page(pagination.num_pages)
        return context

class ProductDetail(DetailView):
    model = Product
    template_name = "mainapp/detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data()
        context['product'] = get_product_(self.kwargs.get('pk'))
        return context
