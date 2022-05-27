from django.views.generic import DetailView, TemplateView, ListView

from common.mixins import BaseClassContextMixin
from mainapp.models import ProductCategory, Product


# Create your views here.

class IndexTemplateView(TemplateView, BaseClassContextMixin):
    template_name = 'mainapp/index.html'
    title = "GeekShop"


class ProductListView(ListView, BaseClassContextMixin):
    model = Product
    context_object_name = 'products'
    template_name = 'mainapp/products.html'
    paginate_by = 6

    def get_queryset(self):
        id_category = self.kwargs.get('id_category')

        if id_category:
            queryset = Product.objects.filter(category_id=id_category)
        else:
            queryset = Product.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.all()
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
