from django.contrib import auth
from django.contrib.auth.views import LoginView
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from users.models import User


class LoginUser(LoginView):
    """Авторизация пользователя"""
    form_class = UserLoginForm
    template_name = 'users/login.html'
    success_url = 'home:index'
    extra_context = {'title': "Авторизация"}


class UserRegistration(generic.CreateView):
    """Регистрация пользователя"""
    form_class = UserRegisterForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')


class UserUpdateView(generic.UpdateView):
    model = User
    success_url = reverse_lazy('users:profile')
    form_class = UserProfileForm

    def get_object(self, queryset=None):
        return self.request.user
