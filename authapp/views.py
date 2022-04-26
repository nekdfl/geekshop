from django.conf import settings
from django.contrib import messages, auth
from django.contrib.auth.views import LogoutView, LoginView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
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

    def post(self, request, *args, **kwargs):
        register_form = UserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            user = register_form.save()
            if self.send_verify_mail(user):
                print(f'email активации пользователя {user.username} отправлен')
                messages.success(request=request,
                                 message=f'Инструкция по завершению регистрация отправлена на почту {user.email}')
                return HttpResponseRedirect(reverse('authapp:login'))
            else:
                messages.error(request=request, message=f'Не удалось отправить письмо по адресу {user.email}')
                print(f'ошибка отправки сообщения активакции пользователю {user.username} на почту {user.email}')
        else:
            messages.error(request=request, message=f'{register_form.errors}')
        context = {'form': register_form}
        return render(request, self.template_name, context)

    def send_verify_mail(self, user):
        verify_link = reverse('authapp:verify', args=[user.email, user.activation_key])
        title = f'Активация учетной записи {user.username}'
        message = f'Для подтверждения учетной записи {user.username} на сайте ' \
                  f'{settings.DOMAIN_NAME} перейдите по ссылке: \n' \
                  f'{settings.DOMAIN_NAME}{verify_link}'
        return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

    def verify(self, email, activate_key):
        try:
            user = User.objects.get(email=email)
            if user and user.activation_key == activate_key and not user.is_activation_key_expired():
                user.activation_key = ''
                user.activation_key_ = None
                user.is_active = True
                user.save()
                auth.login(self, user)
            return render(self, template_name='authapp/verification.html')
        except Exception as e:
            return HttpResponseRedirect(reverse('index'))

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
