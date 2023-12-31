from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from customer.forms import StyleFormMixin
from users.models import User


class UserLoginForm(StyleFormMixin, AuthenticationForm):
    """Форма авторизации пользователя"""
    class Meta:
        model = User
        fields = ['email', 'password']


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """Форма регистрации пользователя"""
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']


class UserProfileForm(StyleFormMixin, UserChangeForm):
    """Форма профиля пользователя"""
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'phone', 'country', 'image']

    def __init__(self, *args, **kwargs):
        """Скрытие поля пароль в шаблоне"""
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class RecoveryForm(StyleFormMixin, forms.BaseForm):
    """Форма запроса на восстановление пароля по email"""
    class Meta:
        model = User
        fields = ['email']
