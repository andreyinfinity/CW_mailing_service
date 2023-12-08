from django.db import models


class Tag(models.Model):
    tag = models.CharField(max_length=100, verbose_name='заметка')


class Customer(models.Model):
    """Клиент"""
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    last_name = models.CharField(max_length=20, null=True, blank=True, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='e-mail')
    tag = models.ForeignKey(Tag, null=True, blank=True, on_delete=models.CASCADE)
    mailing_count = models.IntegerField(default=0, verbose_name='счетчик рассылок')
    is_active = models.BooleanField(default=True, verbose_name='флаг активности')

    def __str__(self):
        return f'{self.last_name}{self.first_name}: {self.email}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
