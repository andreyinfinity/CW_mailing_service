from django.db import models


class User(models.Model):
    """Пользователь"""
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    last_name = models.CharField(max_length=20, null=True, blank=True, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='e-mail')

    def __str__(self):
        return f'{self.last_name}{self.first_name}: {self.email}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
