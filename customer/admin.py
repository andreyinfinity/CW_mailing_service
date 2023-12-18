from django.contrib import admin
from customer.models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Отображение списка клиентов"""
    list_display = ('email', 'first_name', 'last_name', 'user')
