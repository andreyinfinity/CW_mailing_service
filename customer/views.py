from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from customer.forms import CustomerForm
from customer.models import Customer


class CustomerView(LoginRequiredMixin, generic.ListView):
    """Контроллер списка клиентов. Если пользователь не авторизован,
    то переход на страницу авторизации."""
    login_url = 'user:login'

    def get_queryset(self):
        """Метод для вывода клиентов текущего пользователя"""
        return Customer.objects.filter(user=self.request.user.pk)

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['username'] = self.request.user.first_name
    #     return context


class CustomerCreateView(LoginRequiredMixin, generic.CreateView):
    """Контроллер создания нового клиента для текущего пользователя"""
    login_url = 'user:login'
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy('customer:customers')

    def get_form_kwargs(self):
        """Запись user_id в kwargs для передачи в форму"""
        kwargs = super(CustomerCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Добавление user_id после валидации формы"""
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return redirect(self.success_url)


class CustomerUpdateView(LoginRequiredMixin, generic.UpdateView):
    """Контроллер редактирования клиента"""
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy('customer:customers')

    def get_form_kwargs(self):
        """Запись user_id в kwargs для передачи в форму"""
        kwargs = super(CustomerUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class CustomerDeleteView(LoginRequiredMixin, generic.DeleteView):
    """Контроллер удаления клиента"""
    model = Customer
    success_url = reverse_lazy('customer:customers')


def toggle_subscribe(request, pk):
    """Контроллер изменения состояния подписчика"""
    customer = get_object_or_404(Customer, pk=pk)
    if customer.is_subscribe:
        customer.is_subscribe = False
    else:
        customer.is_subscribe = True
    customer.save()
    return redirect(reverse_lazy('customer:customers'))
