from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import DatabaseError
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.datetime_safe import datetime
from django.views import generic
from customer.models import Customer
from customer.permissions import OwnerPermissionsMixin
from mailing.forms import MailingForm, MailForm
from mailing.models import Mail, Mailing, Logs


class MailView(LoginRequiredMixin, generic.ListView):
    """Вывод списка писем пользователя"""
    model = Mail

    def get_queryset(self):
        """Метод для вывода писем только текущего пользователя"""
        return super().get_queryset().filter(user=self.request.user)


class MailCreateView(LoginRequiredMixin, generic.CreateView):
    """Создание письма"""
    model = Mail
    form_class = MailForm
    success_url = reverse_lazy('mailing:mails')

    def form_valid(self, form):
        """Добавление текущего пользователя в форму"""
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = self.request.user
            try:
                instance.save()
            except DatabaseError:
                messages.warning(request=self.request,
                                 message=f"Ошибка сохранения письма")
                return redirect(reverse_lazy('mailing:create'))
            messages.success(request=self.request,
                             message=f'Письмо "{instance.title}" успешно сохранено')
            return redirect(self.success_url)
        return super().form_valid(form)


class MailUpdateView(LoginRequiredMixin, OwnerPermissionsMixin, generic.UpdateView):
    """Редактирование письма"""
    model = Mail
    form_class = MailForm
    success_url = reverse_lazy('mailing:mails')

    def get_success_url(self):
        messages.success(request=self.request,
                         message=f'Письмо "{self.object.title}" успешно обновлено')
        return super().get_success_url()


class MailDeleteView(LoginRequiredMixin, OwnerPermissionsMixin, generic.DeleteView):
    """Удаление письма"""
    model = Mail
    success_url = reverse_lazy('mailing:mails')

    def get_success_url(self):
        """Вывод сообщения при успешном удалении"""
        messages.warning(request=self.request,
                         message=f'Письмо "{self.object.title}" удалено')
        return super().get_success_url()


class MailingView(LoginRequiredMixin, generic.ListView):
    """Вывод списка писем пользователя"""
    model = Mailing

    def get_queryset(self):
        """Метод для вывода рассылок только текущего пользователя и
        показа рассылок всех пользователей для модератора"""
        if self.request.user.has_perm('mailing.view_all_mailings'):
            return super().get_queryset().all().exclude(status='completed').order_by('next_date')
        return super().get_queryset().filter(user=self.request.user)


class MailingCreateView(LoginRequiredMixin, generic.CreateView):
    """Создание рассылки"""
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailings')

    def get_form_kwargs(self):
        """Передача текущего пользователя в kwargs для использования в форме"""
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """Добавление пользователя и списка активных
        клиентов пользователя в рассылку"""
        if form.is_valid():
            customers = Customer.objects.filter(user=self.request.user).filter(is_subscribe=True)
            if customers:
                instance = form.save(commit=False)
                instance.user = self.request.user
                instance.next_date = form.cleaned_data.get('send_date')
                try:
                    instance.save()
                    instance.customers.set(customers)
                    customers.update(mailing_count=F('mailing_count') + 1)
                except DatabaseError:
                    messages.warning(request=self.request,
                                     message=f"Ошибка создания рассылки")
                    return redirect(reverse_lazy('mailing:mailings'))
                messages.success(request=self.request,
                                 message=f'{instance.name} успешно создана')
                return redirect(self.success_url)
            messages.warning(request=self.request,
                             message=f'Должен быть хотя бы 1 клиент для рассылки')
            return redirect(reverse_lazy('customer:customers'))
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, OwnerPermissionsMixin, generic.UpdateView):
    """Редактирование рассылки"""
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailings')

    def get_form_kwargs(self):
        """Передача текущего пользователя в kwargs для использования в форме"""
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """Добавление списка активных
        клиентов пользователя в рассылку"""
        if form.is_valid():
            customers = Customer.objects.filter(user=self.request.user).filter(is_subscribe=True)
            if customers:
                instance = form.save(commit=False)
                instance.next_date = form.cleaned_data.get('send_date')
                try:
                    instance.save()
                    instance.customers.set(customers)
                except DatabaseError:
                    messages.warning(request=self.request,
                                     message=f"Ошибка обновления рассылки")
                    return redirect(reverse_lazy('mailing:mailings'))
                messages.success(request=self.request,
                                 message=f'{instance.name} успешно обновлена')
                return redirect(self.success_url)
            messages.warning(request=self.request,
                             message=f'Должен быть хотя бы 1 клиент для рассылки')
            return redirect(reverse_lazy('customer:customers'))
        return super().form_valid(form)


class MailingDeleteView(LoginRequiredMixin, OwnerPermissionsMixin, generic.DeleteView):
    """Удаление рассылки"""
    model = Mailing
    success_url = reverse_lazy('mailing:mailings')

    def get_success_url(self):
        """Вывод сообщения при успешном удалении"""
        messages.warning(request=self.request,
                         message=f'Рассылка "{self.object.name}" удалена')
        return super().get_success_url()


@login_required
def toggle_status(request, pk):
    """Контроллер изменения состояния рассылки"""
    mailing = get_object_or_404(Mailing, pk=pk)
    if request.user.has_perm('mailing.set_mailing_status') or request.user == mailing.user:
        if mailing.status in ['in progress', 'created']:
            mailing.status = 'stopped'
            messages.warning(request=request,
                             message=f'Рассылка {mailing.name} прекращена')
        elif mailing.status == 'stopped':
            mailing.status = 'in progress'
            if mailing.next_date < datetime.now(timezone.utc):
                mailing.next_date = datetime.now(timezone.utc)
            messages.success(request=request,
                             message=f'Рассылка {mailing.name} продолжит свою работу')
        elif mailing.status == 'completed':
            mailing.status = 'created'
            mailing.next_date = datetime.now(timezone.utc)
            messages.success(request=request,
                             message=f'Рассылка {mailing.name} будет разослана повторно')
        mailing.save()
    return redirect(reverse_lazy('mailing:mailings'))


class LogsView(LoginRequiredMixin, generic.ListView):
    """Вывод списка логов рассылок пользователя"""
    model = Logs

    def get_queryset(self):
        """Метод для вывода логов только текущего пользователя"""
        return super().get_queryset().filter(user=self.request.user)
