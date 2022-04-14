# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from adminapp.forms import UserAdminRegisterForm, AdminUserProfileForm
from authapp.models import User


@user_passes_test(lambda u: u.is_superuser)
def index(request):
    context = {
        'title': 'Админка | Пользователи'
    }
    return render(request, 'adminapp/admin.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_users(request):
    context = {
        'title': 'Админка | Пользователи',
        'users': User.objects.all()
    }
    return render(request, 'adminapp/admin-users-read.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_user_create(request):
    if request.method == 'POST':
        form = UserAdminRegisterForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация успешно завершена')
            return HttpResponseRedirect(reverse('adminapp:admin_users'))
        else:
            messages.error(request, form.errors)
            print(form.errors)
    else:
        form = UserAdminRegisterForm
    context = {
        'title': 'Админка | Регистрация пользователи',
        'form': form
    }
    return render(request, 'adminapp/admin-users-create.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_user_update(request, id):
    pass
    user_select = User.objects.get(id=id)
    if request.method == "POST":
        form = AdminUserProfileForm(data=request.POST, instance=user_select, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:admin_users'))
    else:
        form = AdminUserProfileForm(instance=user_select)

    context = {
        'title': 'Админка | Обновление пользователи',
        'form': form,
        'user_select': user_select
    }
    return render(request, 'adminapp/admin-users-update-delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_user_delete(request, id):
    # user_select = User.objects.get(id=id).delete()
    user_select = User.objects.get(id=id)
    user_select.is_active = False
    user_select.save()
    return HttpResponseRedirect(reverse('adminapp:admin_users'))
