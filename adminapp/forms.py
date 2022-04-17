from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from authapp.models import User
from mainapp.models import ProductCategory, Product


class UserAdminRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'last_name', 'first_name', 'email', 'image', 'age')

    def __init__(self, *args, **kwargs):
        super(UserAdminRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['password1'].widget.attrs['placeholder'] = 'Введите пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Повторите пароль'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Ведите фамилию'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Введите имя'
        self.fields['email'].widget.attrs['placeholder'] = 'Введите email'
        self.fields['image'].widget.attrs['placeholder'] = 'Загрузить фото'
        self.fields['age'].widget.attrs['placeholder'] = 'Возраст'

        for filed_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'

        self.fields['image'].widget.attrs['class'] = 'custom-file-input'


class AdminUserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'email', 'image', 'age')

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True

        for filed_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'

        self.fields['image'].widget.attrs['class'] = 'custom-file-input'


############################
class AdminCategoryAddForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ('name', 'description')

    def __init__(self, *args, **kwargs):
        super(AdminCategoryAddForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Введите имя категории'
        self.fields['description'].widget.attrs['placeholder'] = 'Введите описание...'

        for filed_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'


class AdminCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ('name', 'description')

    def __init__(self, *args, **kwargs):
        super(AdminCategoryUpdateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Введите имя категории'
        self.fields['description'].widget.attrs['placeholder'] = 'Введите описание...'

        for filed_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'


############################
class AdminProductAddForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'image', 'description', 'price', 'quantity', 'category')

    def __init__(self, *args, **kwargs):
        super(AdminProductAddForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Введите наименование товара'
        self.fields['image'].widget.attrs['placeholder'] = 'Загрузить фото'
        self.fields['description'].widget.attrs['placeholder'] = 'Введите описание'
        self.fields['price'].widget.attrs['placeholder'] = 'Укажите цену'
        self.fields['quantity'].widget.attrs['placeholder'] = 'Укажите колличество на складе'
        self.fields['category'].widget.attrs['placeholder'] = 'Выбирите категорию'

        for filed_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-2'

        self.fields['image'].widget.attrs['class'] = 'custom-file-input'


class AdminProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'image', 'description', 'price', 'quantity', 'category')

    def __init__(self, *args, **kwargs):
        super(AdminProductUpdateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Введите наименование товара'
        # self.fields['image'].widget.attrs['placeholder'] = 'Загрузить фото'
        self.fields['description'].widget.attrs['placeholder'] = 'Введите описание'
        self.fields['price'].widget.attrs['placeholder'] = 'Укажите цену'
        self.fields['quantity'].widget.attrs['placeholder'] = 'Укажите колличество на складе'
        self.fields['category'].widget.attrs['placeholder'] = 'Выбирите категорию'

        for filed_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-2'

        # self.fields['image'].widget.attrs['class'] = 'custom-file-input'
