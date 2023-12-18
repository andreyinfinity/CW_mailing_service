from django import forms
from django.contrib.auth.forms import UserCreationForm
from user.models import User


class UserLoginForm(forms.Form):
    """Форма входа в систему"""
    username = forms.CharField(
                     max_length=30,
                     widget=forms.TextInput(attrs={
                         'class': 'form-control',
                         'placeholder': 'Имя пользователя'}))
    password = forms.CharField(
                      max_length=30,
                      widget=forms.PasswordInput(attrs={
                          'class': 'form-control',
                          'placeholder': 'Пароль'}))


class UserRegistrationForm(UserCreationForm):
    """Форма регистрации нового пользователя"""
    username = forms.CharField(max_length=30,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Введите Имя'}))
    email = forms.CharField(max_length=75,
                            widget=forms.EmailInput(attrs={
                                'class': 'form-control',
                                'placeholder': 'Введите адрес электронной почты'}))
    password1 = forms.CharField(label="Пароль", max_length=100,
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(label="Подтверждение пароля", max_length=100,
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Повторите пароль'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        """Проверка адреса электронной почты на уникальность"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже зарегистрирован.")
        return email
