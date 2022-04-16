from django.urls import path

from adminapp.views import CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView
from adminapp.views import IndexTemplateView, UserListView, UserCreateView, UserUpdateView, UserDeleteView
from adminapp.views import ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView

app_name = "adminapp"
urlpatterns = [
    path('', IndexTemplateView.as_view(), name="index"),
    path('users/', UserListView.as_view(), name='admin_users'),
    path('user-create/', UserCreateView.as_view(), name='admin_user_create'),
    path('user-update/<int:pk>/', UserUpdateView.as_view(), name='admin_user_update'),
    path('user-delete/<int:pk>/', UserDeleteView.as_view(), name='admin_user_delete'),
    path('categories/', CategoryListView.as_view(), name='admin_categories'),
    path('category-add/', CategoryCreateView.as_view(), name='admin_category_add'),
    path('category-update/<int:pk>/', CategoryUpdateView.as_view(), name='admin_category_update'),
    path('category-delete/<int:pk>/', CategoryDeleteView.as_view(), name='admin_category_delete'),
    path('products/', ProductListView.as_view(), name='admin_products'),
    path('product-add/', ProductCreateView.as_view(), name='admin_product_add'),
    path('product-update/<int:pk>/', ProductUpdateView.as_view(), name='admin_product_update'),
    path('product-delete/<int:pk>/', ProductDeleteView.as_view(), name='admin_product_delete'),

]
