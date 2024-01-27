from django.db import models
from django.utils import timezone
from customer.models import Customer
from users.models import User, NULLABLE

PERIOD_CHOICES = (
    ('onetime', 'один раз'),
    ('daily', 'ежедневно'),
    ('weekly', 'еженедельно'),
    ('monthly', 'ежемесячно'),
)
STATUS_CHOICES = (
    ('created', 'created'),
    ('in progress', 'in progress'),
    ('sending', 'sending'),
    ('stopped', 'stopped'),
    ('completed', 'completed')
)


class Mail(models.Model):
    """Письмо"""
    title = models.CharField(max_length=200, verbose_name='тема письма')
    body = models.TextField(verbose_name='текст письма')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')

    class Meta:
        verbose_name = 'письмо'
        verbose_name_plural = 'письма'
        ordering = ('-pk',)

    def __str__(self):
        return self.title


class Mailing(models.Model):
    """Рассылка"""
    name = models.CharField(max_length=50, verbose_name='название', default='рассылка')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    send_date = models.DateTimeField(default=timezone.now, verbose_name='дата начала рассылки')
    next_date = models.DateTimeField(verbose_name='дата следующего отправления', **NULLABLE)
    period = models.CharField(max_length=50, choices=PERIOD_CHOICES, default='none', verbose_name='периодичность')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='created', verbose_name='статус')
    customers = models.ManyToManyField(Customer, verbose_name='клиенты пользователя')
    mail = models.ForeignKey(Mail, on_delete=models.CASCADE, verbose_name='письмо')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        ordering = ('-pk',)
        permissions = [
            ('set_mailing_status', 'изменение статуса рассылки'),
            ('view_all_mailings', 'просмотр рассылок всех пользователей')
        ]

    def __str__(self):
        return f'{self.mail}, {self.send_date}'


class Logs(models.Model):
    """Статистика рассылки"""
    last_attempt_time = models.DateTimeField(verbose_name='Последняя отправка', auto_now=True)
    status = models.CharField(max_length=20, verbose_name='Статус отправки')
    mailing_pk = models.IntegerField(verbose_name='id рассылки')
    mailing_name = models.CharField(max_length=50, verbose_name='название рассылки', **NULLABLE)
    user_pk = models.IntegerField(verbose_name='id пользователя')
    error_message = models.TextField(verbose_name='Сообщение об ошибке', **NULLABLE)

    def __str__(self):
        return (f'{self.last_attempt_time} '
                f'{self.status} '
                f'{self.mailing_pk} '
                f'{self.user_pk} '
                f'{self.error_message}')

    class Meta:
        verbose_name = 'Лог рассылки'
        verbose_name_plural = 'Логи рассылки'
