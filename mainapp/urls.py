from django.urls import path

from mainapp.views import products, ProductDetail

app_name = "mainapp"

urlpatterns = [
    path('', products, name='product'),
    path('category/<int:id_category>/', products, name='category'),
    path('page/<int:page>/', products, name='category_page'),
    path('detail/<int:pk>/', ProductDetail.as_view(), name='product_detail')
]
