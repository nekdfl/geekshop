from django.contrib import messages
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import reverse_lazy
from django.views.generic import UpdateView, FormView

from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from authapp.models import User
from common.mixins import IsUserAuthorizedMixin, BaseClassContextMixin


class LoginTemplateView(LoginView, BaseClassContextMixin):
    title = 'Geekshop | Авторизация'
    form_class = UserLoginForm
    template_name = 'authapp/login.html'


class RegisterUser(FormView, BaseClassContextMixin):
    title = 'Geekshop | Регистрация'
    template_name = 'authapp/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('authapp:login')
    Model = User

    def form_valid(self, form):
        form.save()  # добавление пользователя
        messages.success(self.request, 'Регистрация успешно завершена')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)


class Profile(UpdateView, BaseClassContextMixin, IsUserAuthorizedMixin):
    template_name = 'authapp/profile.html'
    form_class = UserProfileForm
    title = 'Geekshop | Профиль пользователя'
    success_url = reverse_lazy('authapp:profile')

    def get_object(self, queryset=None):
        return User.objects.get(id=self.request.user.pk)

    def form_valid(self, form):
        messages.success(self.request, 'Изменения сохранены')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)


class Logout(LogoutView, IsUserAuthorizedMixin):
    template_name = 'mainapp/index.html'
