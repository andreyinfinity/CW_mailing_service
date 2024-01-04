import uuid
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from config.settings import EMAIL_HOST_USER
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from users.models import User


class LoginUser(LoginView):
    """Авторизация пользователя"""
    form_class = UserLoginForm
    template_name = 'users/login.html'
    success_url = 'users:profile'
    extra_context = {'title': "Авторизация"}


class UserRegistration(generic.CreateView):
    """Регистрация пользователя с активацией аккаунта по email"""
    form_class = UserRegisterForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        if form.is_valid():
            user = form.save(commit=False)
            # деактивируем пользователя
            user.is_active = False
            # создаем и записываем код верификации
            verification_code = uuid.uuid4().hex
            user.uuid = verification_code
            user.save()
            # получаем домен сайта
            current_site = get_current_site(self.request)
            # создаем и отправляем письмо со ссылкой на активацию
            mail_subject = 'Ссылка для активации вашего аккаунта'
            message = (f"Для активации вашего аккаунта перейдите по ссылке:\n"
                       f"http://{current_site}{reverse_lazy('users:activate', args=[verification_code])}")
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(subject=mail_subject, body=message, to=[to_email], from_email=EMAIL_HOST_USER)
            email.send()
            messages.success(request=self.request,
                             message='Вы успешно зарегистрировались. '
                                     'На ваш email выслана ссылка для активации аккаунта.')
            return HttpResponseRedirect(reverse_lazy('users:login'))
        return super().form_valid(form)


def activate(request, code):
    """Контроллер активации пользователя при переходе по ссылке из письма"""
    try:
        # поиск пользователя по uuid
        user = User.objects.get(uuid=code)
        # активация пользователя
        user.is_active = True
        user.uuid = None
        user.save()
        # при успешной активации редирект на страницу входа
        messages.success(request=request,
                         message='Ваш аккаунт успешно активирован.')
        return HttpResponseRedirect(reverse_lazy('users:login'))
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.warning(request=request,
                         message='Неверная ссылка активации')
        return HttpResponseRedirect(reverse_lazy('users:login'))


class UserUpdateView(generic.UpdateView):
    model = User
    success_url = reverse_lazy('users:profile')
    form_class = UserProfileForm

    def get_object(self, queryset=None):
        return self.request.user
