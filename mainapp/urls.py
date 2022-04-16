from django.urls import path

from mainapp.views import products

app_name = "mainapp"

urlpatterns = [
    path('', products, name='product'),
    path('category/<int:id_category>/', products, name='category'),
    path('category/<int:id_category>/', products, name='category')
]
