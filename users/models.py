from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    """Пользователь"""
    image = models.ImageField(upload_to='users/pk', verbose_name='аватар', **NULLABLE)
    username = None
    email = models.EmailField(verbose_name='e-mail', unique=True)
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='страна', **NULLABLE)
    uuid = models.CharField(max_length=32, verbose_name='uuid-hex', **NULLABLE)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []