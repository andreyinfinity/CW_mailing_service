from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.datetime_safe import datetime
from django.views import generic
from customer.models import Customer
from mailing.forms import MailingForm, MailForm
from mailing.models import Mail, Mailing


class MailView(generic.ListView):
    """Вывод списка писем пользователя"""
    model = Mail

    def get_queryset(self):
        """Метод для вывода писем текущего пользователя"""
        return Mail.objects.filter(user=self.request.user.pk)


class MailCreateView(generic.CreateView):
    """Создание письма"""
    model = Mail
    form_class = MailForm
    success_url = reverse_lazy('mailing:mails')

    def form_valid(self, form):
        """Добавление текущего пользователя в форму"""
        form.instance.user = self.request.user
        return super().form_valid(form)


class MailUpdateView(generic.UpdateView):
    """Редактирование письма"""
    model = Mail
    form_class = MailForm
    success_url = reverse_lazy('mailing:mails')


class MailDeleteView(generic.DeleteView):
    """Удаление письма"""
    model = Mail
    success_url = reverse_lazy('mailing:mails')


class MailingView(generic.ListView):
    """Вывод списка писем пользователя"""
    model = Mailing

    def get_queryset(self):
        """Метод для вывода рассылок текущего пользователя"""
        return Mailing.objects.filter(user=self.request.user.pk)


class MailingCreateView(generic.CreateView):
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
        form.instance.user = self.request.user
        form.instance.next_date = form.cleaned_data.get('send_date')
        form.save()
        customers = Customer.objects.filter(user=self.request.user).filter(is_subscribe=True)
        form.instance.customers.set(customers)
        return super().form_valid(form)


class MailingUpdateView(generic.UpdateView):
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
        form.instance.next_date = form.cleaned_data.get('send_date')
        form.save()
        customers = Customer.objects.filter(user=self.request.user).filter(is_subscribe=True)
        form.instance.customers.set(customers)
        return super().form_valid(form)


class MailingDeleteView(generic.DeleteView):
    """Удаление рассылки"""
    model = Mailing
    success_url = reverse_lazy('mailing:mailings')


def toggle_status(request, pk):
    """Контроллер изменения состояния рассылки"""
    mailing = get_object_or_404(Mailing, pk=pk)
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
