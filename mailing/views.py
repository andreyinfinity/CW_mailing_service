from django.urls import reverse_lazy
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

    def form_valid(self, form):
        """Добавление текущего пользователя в форму"""
        form.instance.user = self.request.user
        form.save()
        customers = Customer.objects.filter(user=self.request.user).filter(is_subscribe=True)
        form.instance.customers.set(customers)
        return super().form_valid(form)


class MailingUpdateView(generic.UpdateView):
    """Редактирование рассылки"""
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailings')


class MailingDeleteView(generic.DeleteView):
    """Удаление рассылки"""
    model = Mailing
    success_url = reverse_lazy('mailing:mailings')

