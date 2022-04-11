from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
# Create your views here.
from django.template.loader import render_to_string

from basketapp.models import Basket
from mainapp.models import Product


def basket_add(request, id):
    user_select = request.user
    product = Product.objects.get(id=id)
    baskets = Basket.objects.filter(user=user_select, product=product)

    if baskets:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    else:
        Basket.objects.create(user=user_select, product=product, quantity=1)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# def basket_add(request, id):
#
#     if request.is_ajax():
#         user_select = request.user
#         product = Product.objects.get(id=id)
#         baskets = Basket.objects.filter(user=user_select, product=product)
#
#         if baskets:
#             basket = baskets.first()
#             basket.quantity +=1
#             basket.save()
#         else:
#             Basket.objects.create(user=user_select, product=product, quantity=1)
#
#         products = Product.objects.all()
#         context = {"baskets": products}
#         result = render_to_string('mainapp/include/product_card.html', context)
#         return JsonResponse({'result': result})


@login_required
def basket_remove(request, basket_id):
    Basket.objects.get(id=basket_id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, basket_id, quantity):
    pass
    if request.is_ajax():
        pass
        basket = Basket.objects.get(id=basket_id)
        if quantity > 0:
            basket.quantity = quantity
            basket.save()
        else:
            basket.delete()

        baskets = Basket.objects.filter(user=request.user)
        context = {"baskets": baskets}
        result = render_to_string('basketapp/basket.html', context)
        return JsonResponse({'result': result})
