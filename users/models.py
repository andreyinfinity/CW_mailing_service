from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}


def user_directory_path(instance, filename):
    # Файл будет загружен в MEDIA_ROOT/user_<id>/<filename>
    return "user_{0}/{1}".format(instance.id, filename)


class User(AbstractUser):
    """Пользователь"""
    image = models.ImageField(upload_to=user_directory_path, verbose_name='аватар', **NULLABLE)
    username = None
    email = models.EmailField(verbose_name='e-mail', unique=True)
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='страна', **NULLABLE)
    uuid = models.CharField(max_length=32, verbose_name='uuid-hex', **NULLABLE)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

