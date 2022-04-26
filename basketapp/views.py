from django.http import HttpResponseRedirect, JsonResponse
# Create your views here.
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import CreateView, DeleteView, UpdateView

from basketapp.models import Basket
from common.mixins import IsUserAuthorizedMixin
from mainapp.models import Product


class BasketCreateView(CreateView, IsUserAuthorizedMixin):

    def get(self, request, *args, **kwargs):
        if request.is_ajax:
            product_id = self.kwargs.get('product_id')
            user_select = self.request.user
            product = get_object_or_404(Product, id=product_id)
            baskets = Basket.objects.filter(user=user_select, product=product)
            if baskets:
                basket = baskets.first()
                basket.quantity += 1
                basket.save()
            else:
                Basket.objects.create(user=user_select, product=product, quantity=1)

        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class BasketRemoveView(DeleteView, IsUserAuthorizedMixin):

    def get(self, request, *args, **kwargs):
        basket_id = self.kwargs.get('basket_id')
        get_object_or_404(Basket, id=basket_id).delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class BasketUpdateView(UpdateView, IsUserAuthorizedMixin):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            quantity = self.kwargs.get('quantity')
            basket_id = self.kwargs.get('basket_id')
            basket = get_object_or_404(Basket, id=basket_id)

            if quantity > 0:
                basket.quantity = quantity
                basket.save()
            else:
                basket.delete()

            baskets = Basket.objects.filter(user=request.user)
            context = {"baskets": baskets}
            result = render_to_string('basketapp/basket.html', context)
        return JsonResponse({'result': result})
