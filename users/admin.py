from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Отображение списка клиентов"""
    list_display = ('pk', 'email', 'username', 'first_name', 'last_name')
