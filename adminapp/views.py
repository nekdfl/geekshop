# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, DeleteView, TemplateView, CreateView

from adminapp.forms import UserAdminRegisterForm, AdminUserProfileForm, AdminCategoryAdd, AdminCategoryUpdate, \
    AdminProductAdd, AdminProductUpdate
from adminapp.mixins import BaseClassContextMixin, SuperUserDispatchMixin, UserDispatchMixin
from authapp.models import User
from mainapp.models import ProductCategory, Product


# пример function based view с декоратором
# @user_passes_test(lambda u: u.is_superuser)
# def index(request):
#     context = {
#         'title': 'Админка | Пользователи'
#     }
#     return render(request, 'adminapp/admin.html', context)

# прмиер class based view и работа с конектостом через переделение встроенных методгов
class IndexTemplateView(TemplateView):
    template_name = 'adminapp/admin.html'

    # применение декоратора как FBV index выше
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(IndexTemplateView, self).dispatch(request, *args, **kwargs)

    # работа с конекстом
    def get_context_data(self, **kwargs):
        context = super(IndexTemplateView, self).get_context_data(**kwargs)
        context['title'] = 'Главная'
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def admin_users(request):
#     context = {
#         'title': 'Админка | Пользователи',
#         'users': User.objects.all()
#     }
#     return render(request, 'adminapp/admin-users-read.html', context)

# прмиер CBV с использованием миксинов
class UserListView(ListView, BaseClassContextMixin, SuperUserDispatchMixin):
    model = User
    template_name = 'adminapp/admin-users-read.html'
    title = 'Админка | Пользователи'
    context_object_name = 'users'


# @user_passes_test(lambda u: u.is_superuser)
# def admin_user_create(request):
#     if request.method == 'POST':
#         form = UserAdminRegisterForm(data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Регистрация успешно завершена')
#             return HttpResponseRedirect(reverse('adminapp:admin_users'))
#         else:
#             messages.error(request, form.errors)
#             print(form.errors)
#     else:
#         form = UserAdminRegisterForm
#     context = {
#         'title': 'Админка | Регистрация пользователи',
#         'form': form
#     }
#     return render(request, 'adminapp/admin-users-create.html', context)

class UserCreateView(CreateView, BaseClassContextMixin, SuperUserDispatchMixin, UserDispatchMixin):
    model = User
    title = 'Админка | Регистрация пользователи'
    template_name = 'adminapp/admin-users-create.html'
    form_class = UserAdminRegisterForm
    success_url = reverse_lazy('adminapp:admin_users')

    def form_valid(self, form):
        messages.success(self.request, f'Пользователь {form.clean()["username"]} успешно зарегистрирован')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)


class UserUpdateView(UpdateView, BaseClassContextMixin, SuperUserDispatchMixin, UserDispatchMixin):
    model = User
    title = 'Админка | Редактирование пользователи'
    template_name = 'adminapp/admin-users-update-delete.html'
    form_class = AdminUserProfileForm
    success_url = reverse_lazy('adminapp:admin_users')

    def form_valid(self, form):
        messages.success(self.request, f'Пользователь {form.clean()["username"]} успешно обновлен')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)


# Пример удаления через DeleteView
class UserDeleteView(DeleteView, SuperUserDispatchMixin, UserDispatchMixin):
    model = User
    template_name = 'adminapp/admin-users-update-delete.html'
    form_class = AdminUserProfileForm
    success_url = reverse_lazy('adminapp:admin_users')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


# Пример удаления через FBV
# @user_passes_test(lambda u: u.is_superuser)
# def admin_user_delete(request, id):
#     user_select = User.objects.get(id=id).delete()
#     # user_select = User.objects.get(id=id)
#     # user_select.is_active = False
#     # user_select.save()
#     return HttpResponseRedirect(reverse('adminapp:admin_users'))


#########################
@user_passes_test(lambda u: u.is_superuser)
def admin_categories(request):
    context = {
        'title': 'Админка | Пользователи',
        'categories': ProductCategory.objects.all()
    }
    return render(request, 'adminapp/admin-categories-read.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_category_add(request):
    if request.method == 'POST':
        form = AdminCategoryAdd(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Категория успешно добавлена')
            return HttpResponseRedirect(reverse('adminapp:admin_categories'))
        else:
            messages.error(request, form.errors)
            print(form.errors)
    else:
        form = AdminCategoryAdd
    context = {
        'title': 'Админка | Добавить категорию',
        'form': form
    }
    return render(request, 'adminapp/admin-categories-create.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_category_update(request, pk):
    category_select = ProductCategory.objects.get(id=pk)
    if request.method == "POST":
        form = AdminCategoryUpdate(data=request.POST, instance=category_select)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:admin_categories'))
    else:
        form = AdminCategoryUpdate(instance=category_select)

    context = {
        'title': 'Админка | Обновление категории',
        'form': form,
        'category_select': category_select
    }
    return render(request, 'adminapp/admin-categories-update-delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_category_delete(request, pk):
    ProductCategory.objects.get(id=pk).delete()
    return HttpResponseRedirect(reverse('adminapp:admin_categories'))


#########################

@user_passes_test(lambda u: u.is_superuser)
def admin_products(request):
    context = {
        'title': 'Админка | Товары',
        'products': Product.objects.all()
    }
    return render(request, 'adminapp/admin-products-read.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_product_add(request):
    if request.method == 'POST':
        form = AdminProductAdd(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Товар успешно добавлен')
            return HttpResponseRedirect(reverse('adminapp:admin_products'))
        else:
            messages.error(request, form.errors)
            print(form.errors)
    else:
        form = AdminProductAdd()
    context = {
        'title': 'Админка | Создание товара',
        'form': form
    }
    return render(request, 'adminapp/admin-products-create.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_product_update(request, id):
    product_select = Product.objects.get(id=id)
    if request.method == "POST":
        form = AdminProductUpdate(data=request.POST, instance=product_select, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:admin_products'))
    else:
        form = AdminProductUpdate(instance=product_select)

    context = {
        'title': 'Админка | Обновление информации о товаре',
        'form': form,
        'product_select': product_select
    }
    return render(request, 'adminapp/admin-products-update-delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_product_delete(request, id):
    Product.objects.get(id=id).delete()

    return HttpResponseRedirect(reverse('adminapp:admin_products'))
