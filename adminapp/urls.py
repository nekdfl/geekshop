from django.urls import path

from adminapp.views import admin_categories, admin_category_add, admin_category_update, admin_category_delete
from adminapp.views import admin_products, admin_product_add, admin_product_update, admin_product_delete
from adminapp.views import index, admin_users, admin_user_create, admin_user_delete, admin_user_update

app_name = "adminapp"
urlpatterns = [
    path('', index, name="index"),
    path('users/', admin_users, name='admin_users'),
    path('user-create/', admin_user_create, name='admin_user_create'),
    path('user-update/<int:id>/', admin_user_update, name='admin_user_update'),
    path('user-delete/<int:id>/', admin_user_delete, name='admin_user_delete'),
    path('categories/', admin_categories, name='admin_categories'),
    path('category-add/', admin_category_add, name='admin_category_add'),
    path('category-update/<int:id>/', admin_category_update, name='admin_category_update'),
    path('category-delete/<int:id>/', admin_category_delete, name='admin_category_delete'),
    path('products/', admin_products, name='admin_products'),
    path('product-add/', admin_product_add, name='admin_product_add'),
    path('product-update/<int:id>/', admin_product_update, name='admin_product_update'),
    path('product-delete/<int:id>/', admin_product_delete, name='admin_product_delete'),

]
