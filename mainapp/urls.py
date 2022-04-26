from django.urls import path

from mainapp.views import ProductListView, ProductDetail

app_name = "mainapp"

urlpatterns = [
    path('', ProductListView.as_view(), name='product'),
    path('category/<int:id_category>/', ProductListView.as_view(), name='category'),
    path('page/<int:page>/', ProductListView.as_view(), name='category_page'),
    path('detail/<int:pk>/', ProductDetail.as_view(), name='product_detail')
]
