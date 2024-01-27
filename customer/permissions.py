from django.contrib.auth.mixins import PermissionRequiredMixin


class OwnerPermissionsMixin(PermissionRequiredMixin):
    """Миксин для проверки является ли пользователь владельцем"""
    def has_permission(self):
        """Метод для сравнения текущего пользователя с владельцем объекта"""
        return self.get_object().user == self.request.user
