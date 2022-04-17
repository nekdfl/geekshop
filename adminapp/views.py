# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, DeleteView, TemplateView, CreateView

from adminapp.forms import UserAdminRegisterForm, AdminUserProfileForm, AdminCategoryAddForm, AdminCategoryUpdateForm, \
    AdminProductAddForm, AdminProductUpdateForm
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

class CategoryListView(ListView, BaseClassContextMixin, SuperUserDispatchMixin, UserDispatchMixin):
    model = ProductCategory
    title = 'Админка | Категории товаров',
    template_name = 'adminapp/admin-categories-read.html'
    context_object_name = 'categories'


class CategoryCreateView(CreateView, BaseClassContextMixin, SuperUserDispatchMixin, UserDispatchMixin):
    model = ProductCategory
    title = 'Админка | Добавить категорию товаров'
    template_name = 'adminapp/admin-categories-create.html'
    form_class = AdminCategoryAddForm
    success_url = reverse_lazy('adminapp:admin_categories')

    def form_valid(self, form):
        messages.success(self.request, f'Категория {form.clean()["name"]} успешно добавлена')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)


class CategoryUpdateView(UpdateView, BaseClassContextMixin, SuperUserDispatchMixin, UserDispatchMixin):
    model = ProductCategory
    title = 'Админка | Редактировать категорию товаров'
    template_name = 'adminapp/admin-categories-update-delete.html'
    form_class = AdminCategoryUpdateForm
    success_url = reverse_lazy('adminapp:admin_categories')

    def form_valid(self, form):
        messages.success(self.request, f'Изменения в категорию {form.clean()["name"]} успешно внесены')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)


class CategoryDeleteView(DeleteView, SuperUserDispatchMixin, UserDispatchMixin):
    model = ProductCategory
    template_name = 'adminapp/admin-categories-update-delete.html'
    form_class = AdminCategoryUpdateForm
    success_url = reverse_lazy('adminapp:admin_categories')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())


#########################

class ProductListView(ListView, BaseClassContextMixin, SuperUserDispatchMixin, UserDispatchMixin):
    model = Product
    template_name = 'adminapp/admin-products-read.html'
    title = 'Админка | Категории товаров',
    context_object_name = 'products'


class ProductCreateView(CreateView, BaseClassContextMixin, SuperUserDispatchMixin, UserDispatchMixin):
    model = Product
    template_name = 'adminapp/admin-products-create.html'
    title = 'Админка | Добавление товара'
    success_url = reverse_lazy('adminapp:admin_products')
    form_class = AdminProductAddForm

    def form_valid(self, form):
        messages.success(self.request, f'Товар {form.clean()["name"]} успешно добавлен')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)


class ProductUpdateView(UpdateView, BaseClassContextMixin, SuperUserDispatchMixin, UserDispatchMixin):
    model = Product
    template_name = 'adminapp/admin-products-update-delete.html'
    title = 'Админка | Обновление информации о товаре'
    form_class = AdminProductUpdateForm
    success_url = reverse_lazy('adminapp:admin_products')

    def form_valid(self, form):
        messages.success(self.request, f'Товар {form.clean()["name"]} успешно обновлен')
        return super(ProductUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super(ProductUpdateView, self).form_invalid(form)


class ProductDeleteView(DeleteView, SuperUserDispatchMixin, UserDispatchMixin):
    model = Product
    template_name = 'adminapp/admin-products-update-delete.html'
    form_class = AdminProductUpdateForm
    success_url = reverse_lazy('adminapp:admin_products')

    def get(self, request, *args, **kwargs):
        pass
        self.object = self.get_object()
        obj_name = self.object.name
        self.object.delete()
        messages.success(self.request, f'Товар {obj_name} успешно удален')
        return HttpResponseRedirect(self.success_url)

