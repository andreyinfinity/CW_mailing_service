from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import DatabaseError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from customer.forms import CustomerForm
from customer.models import Customer
from customer.permissions import OwnerPermissionsMixin


class CustomerView(LoginRequiredMixin, generic.ListView):
    """Контроллер списка клиентов. Если пользователь не авторизован,
    то переход на страницу авторизации."""
    login_url = 'users:login'
    model = Customer

    def get_queryset(self):
        """Метод для вывода клиентов только текущего пользователя"""
        return super().get_queryset().filter(user=self.request.user)


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
            except DatabaseError:
                messages.warning(request=self.request,
                                 message=f"Пользователь с таким e-mail уже существует")
                return redirect(reverse_lazy('customer:create'))
            messages.success(request=self.request,
                             message=f'{instance.email} успешно добавлен')
            return redirect(self.success_url)
        return super().form_valid(form)


class CustomerUpdateView(LoginRequiredMixin, OwnerPermissionsMixin, generic.UpdateView):
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
            except DatabaseError:
                messages.warning(request=self.request,
                                 message=f"Пользователь с таким e-mail уже существует")
                return redirect(reverse_lazy('customer:edit', args=[self.object.pk]))
            messages.success(request=self.request,
                             message=f'{instance.email} успешно обновлен')
            return redirect(self.success_url)
        return super().form_valid(form)


class CustomerDeleteView(LoginRequiredMixin, OwnerPermissionsMixin, generic.DeleteView):
    """Контроллер удаления клиента"""
    model = Customer
    success_url = reverse_lazy('customer:customers')

    def get_success_url(self):
        """Вывод сообщения при успешном удалении"""
        messages.warning(request=self.request,
                         message=f'Клиент "{self.object.email}" удален')
        return super().get_success_url()


@login_required
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
