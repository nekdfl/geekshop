from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
from django.urls import reverse

from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from basketapp.models import Basket


def login(request):

    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(username=username, password=password)
            if user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                print('Пользователь не активный')
        else:
            print(form.errors)

    else:
       form = UserLoginForm()
    context = {
        'title' : 'Gekshop | Авторизация',
        'form': form
    }
    return render(request,'authapp/login.html',context)

def register(request):

    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
                form.save()
                messages.success(request, 'Регистрация успешно завершена')
                return HttpResponseRedirect(reverse('authapp:login'))
        else:
            print(form.errors)
            messages.error(request, form.errors)
    else:
        form = UserRegisterForm()

    context = {
        'title': 'Gekshop | Регистрация',
        'form':form
    }
    return render(request, 'authapp/register.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            messages.success(request, 'Изменения сохранены')
            form.save()
        else:
            print(form.errors)
            messages.error(request, form.errors)

    user_select = request.user

    context = {
        'title' : 'Gekshop | Профиль пользователя',
        'form' : UserProfileForm(instance=request.user),
        'baskets' : Basket.objects.filter(user=user_select)
    }

    return render(request, 'authapp/profile.html', context)

def logout(request):
    auth.logout(request)
    return render(request,'mainapp/index.html')
