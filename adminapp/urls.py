from django.urls import path

from adminapp.views import IndexTemplateView, UserListView, UserCreateView, UserUpdateView, UserDeleteView
from adminapp.views import admin_categories, admin_category_add, admin_category_update, admin_category_delete
from adminapp.views import admin_products, admin_product_add, admin_product_update, admin_product_delete

app_name = "adminapp"
urlpatterns = [
    path('', IndexTemplateView.as_view(), name="index"),
    path('users/', UserListView.as_view(), name='admin_users'),
    path('user-create/', UserCreateView.as_view(), name='admin_user_create'),
    path('user-update/<int:pk>/', UserUpdateView.as_view(), name='admin_user_update'),
    path('user-delete/<int:pk>/', UserDeleteView.as_view(), name='admin_user_delete'),
    path('categories/', admin_categories, name='admin_categories'),
    path('category-add/', admin_category_add, name='admin_category_add'),
    path('category-update/<int:pk>/', admin_category_update, name='admin_category_update'),
    path('category-delete/<int:id>/', admin_category_delete, name='admin_category_delete'),
    path('products/', admin_products, name='admin_products'),
    path('product-add/', admin_product_add, name='admin_product_add'),
    path('product-update/<int:id>/', admin_product_update, name='admin_product_update'),
    path('product-delete/<int:id>/', admin_product_delete, name='admin_product_delete'),

]
