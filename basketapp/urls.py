

from django.urls import path

from basketapp.views import BasketCreateView, BasketRemoveView, BasketUpdateView

app_name = "basketapp"
urlpatterns = [
    path('add/<int:product_id>', BasketCreateView.as_view(), name="basket_add"),
    path('remove/<int:basket_id>', BasketRemoveView.as_view(), name="basket_remove"),
    path('edit/<int:basket_id>/<int:quantity>', BasketUpdateView.as_view(), name="basket_edit"),
]
