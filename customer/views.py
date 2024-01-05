from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from customer.forms import CustomerForm
from customer.models import Customer


class CustomerView(LoginRequiredMixin, generic.ListView):
    """Контроллер списка клиентов. Если пользователь не авторизован,
    то переход на страницу авторизации."""
    login_url = 'users:login'

    def get_queryset(self):
        """Метод для вывода клиентов текущего пользователя"""
        return Customer.objects.filter(user=self.request.user.pk)


class CustomerCreateView(LoginRequiredMixin, generic.CreateView):
    """Контроллер создания нового клиента для текущего пользователя"""
    login_url = 'users:login'
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy('customer:create')

    def form_valid(self, form):
        """Добавление user_id после валидации формы
        и проверка уникальности email"""
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = self.request.user
            try:
                instance.save()
            except IntegrityError:
                messages.warning(request=self.request,
                                 message=f"Пользователь с таким e-mail уже существует")
                return redirect(reverse_lazy('customer:create'))
            messages.success(request=self.request,
                             message=f'{instance.email} успешно добавлен')
            return redirect(self.success_url)

        return super().form_valid(form)


class CustomerUpdateView(LoginRequiredMixin, generic.UpdateView):
    """Контроллер редактирования клиента"""
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy('customer:customers')

    def form_valid(self, form):
        """Проверка уникальности email после валидации формы"""
        if form.is_valid():
            instance = form.save(commit=False)
            try:
                instance.save()
            except IntegrityError:
                messages.warning(request=self.request,
                                 message=f"Пользователь с таким e-mail уже существует")
                return redirect(reverse_lazy('customer:create'))
            messages.success(request=self.request,
                             message=f'{instance.email} успешно обновлен')
            return redirect(self.success_url)
        return super().form_valid(form)


class CustomerDeleteView(LoginRequiredMixin, generic.DeleteView):
    """Контроллер удаления клиента"""
    model = Customer
    success_url = reverse_lazy('customer:customers')


def toggle_subscribe(request, pk):
    """Контроллер изменения состояния подписчика"""
    customer = get_object_or_404(Customer, pk=pk)
    if customer.is_subscribe:
        customer.is_subscribe = False
        messages.warning(request=request,
                         message=f'{customer.email} отписан от рассылок')
    else:
        customer.is_subscribe = True
        messages.success(request=request,
                         message=f'{customer.email} подписан на рассылки')
    customer.save()
    return redirect(reverse_lazy('customer:customers'))
