from django.urls import path
from mainapp.views import products_view

app_name = "mainapp"

urlpatterns = [
    path('', products_view, name='product')
]
