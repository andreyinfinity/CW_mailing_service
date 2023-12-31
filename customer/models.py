from django.db import models
from users.models import User


class Customer(models.Model):
    """Модель Клиент"""
    first_name = models.CharField(max_length=20, null=True, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=20, null=True, blank=True, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='e-mail')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mailing_count = models.IntegerField(default=0, verbose_name='счетчик рассылок')
    is_subscribe = models.BooleanField(default=True, verbose_name='подписан')

    def __str__(self):
        return f'{self.last_name} {self.first_name}: {self.email}'

    class Meta:
        unique_together = [['email', 'user']]
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
        ordering = ('-pk',)
