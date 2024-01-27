import smtplib
import uuid
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import HttpResponseRedirect, get_object_or_404, redirect
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
            try:
                email = EmailMessage(subject=mail_subject, body=message, to=[to_email], from_email=EMAIL_HOST_USER)
                email.send()
                messages.success(request=self.request,
                                 message='Вы успешно зарегистрировались. '
                                         'На ваш email выслана ссылка для активации аккаунта.')
            except smtplib.SMTPException as error:
                error_message = str(error)
                messages.warning(request=self.request,
                                 message=f'{error_message}'
                                         f'Произошла ошибка при отправки на ваш email ссылки для активации аккаунта.')
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
                         message='Ваш аккаунт успешно активирован. Вы можете войти, '
                                 'используя логи и пароль, указанный при регистрации')
        return HttpResponseRedirect(reverse_lazy('users:login'))
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.warning(request=request,
                         message='Неверная ссылка активации')
        return HttpResponseRedirect(reverse_lazy('users:login'))


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    """Контроллер редактирования профиля пользователя"""
    model = User
    success_url = reverse_lazy('users:profile')
    form_class = UserProfileForm

    def get_object(self, queryset=None):
        """Получение объекта текущего пользователя"""
        return self.request.user


class UserListView(PermissionRequiredMixin, generic.ListView):
    model = User
    permission_required = 'users.view_all_users'

    def get_queryset(self):
        """Метод для вывода пользователей исключая себя"""
        return super().get_queryset().exclude(pk=self.request.user.pk)


@permission_required(perm='users.set_user_active')
def toggle_active(request, pk):
    """Контроллер изменения состояния клиента сервиса"""
    user = get_object_or_404(User, pk=pk)
    if user.is_active:
        user.is_active = False
        messages.warning(request=request,
                         message=f'{user.email} заблокирован в сервисе')
    else:
        user.is_active = True
        messages.success(request=request,
                         message=f'{user.email} восстановлен в сервисе')
    user.save()
    return redirect(reverse_lazy('users:users'))
