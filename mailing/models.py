from django.db import models


class Mailing(models.Model):
    """Рассылка"""
    PERIOD_CHOICES = (
        ('none', 'не повторять'),
        ('daily', 'ежедневно'),
        ('weekly', 'еженедельно'),
        ('monthly', 'ежемесячно')
    )
    STATUS_CHOICES = ('created', 'begin', 'end')

    name = models.CharField(max_length=50, verbose_name='название')
    time = models.TimeField(verbose_name='время')
    period = models.CharField(max_length=50, choices=PERIOD_CHOICES, default='none', verbose_name='периодичность')
    repetitions = models.SmallIntegerField(verbose_name='количество повторений')
    status = models.CharField(max_length=50, default='created', verbose_name='статус')
    mail = models.ForeignKey('Mail', on_delete=models.CASCADE, verbose_name='письмо')
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='клиент')


class Mail(models.Model):
    """Письмо"""
    emails = models.ForeignKey('Emails', on_delete=models.CASCADE, verbose_name='список адресов')
    title = models.CharField(max_length=200, verbose_name='тема письма')
    message = models.TextField(verbose_name='текст письма')
