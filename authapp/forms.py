import hashlib
import random

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm

from authapp.models import User, UserProfile
from authapp.validators import validate_username


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self,*args,**kwargs):
        super(UserLoginForm, self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['password'].widget.attrs['placeholder'] = 'Введите пароль'
        self.fields['username'].required = True
        for filed_name , field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(validators=[validate_username])
    # username = forms.CharField(widget=forms.TextInput(), validators=[validate_username])

    class Meta:
        model = User
        fields = ('username','password1','password2','last_name','first_name','email')

    def __init__(self,*args,**kwargs):
        super(UserRegisterForm, self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['password1'].widget.attrs['placeholder'] = 'Введите пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Повторите пароль'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Ведите фамилию'
        self.fields['last_name'].required = True
        self.fields['first_name'].widget.attrs['placeholder'] = 'Введите имя'
        self.fields['email'].widget.attrs['placeholder'] = 'Введите email'

        for filed_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'

    def save(self):
        user = super(UserRegisterForm, self).save()
        user.is_active = False
        salt = hashlib.sha1(str(random.Random).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1(str(user.email + salt).encode('utf8')).hexdigest()
        user.save()
        return user


class UserForm(UserChangeForm):
    image = forms.ImageField(widget=forms.FileInput, required=False)
    age = forms.IntegerField(widget=forms.NumberInput, required=False, min_value=1)

    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'email', 'image', 'age')

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True

        for filed_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-2'

        self.fields['image'].widget.attrs['class'] = 'custom-file-input'


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for filed_name, field in self.fields.items():
            if filed_name != 'gender':
                field.widget.attrs['class'] = 'form-control py-4'
            else:
                field.widget.attrs['class'] = 'form-control'
