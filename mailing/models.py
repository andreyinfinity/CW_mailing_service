# from django.db import models
#
#
# PERIOD_CHOICES = (
#     ('none', 'не повторять'),
#     ('daily', 'ежедневно'),
#     ('weekly', 'еженедельно'),
#     ('monthly', 'ежемесячно')
# )
# STATUS_CHOICES = ('created', 'begin', 'end')
#
#
# class Mail(models.Model):
#     """Письмо"""
#     title = models.CharField(max_length=200, verbose_name='тема письма')
#     body = models.TextField(verbose_name='текст письма')
#
#
# class User(models.Model):
#     """Пользователь"""
#     first_name = models.CharField(max_length=20, verbose_name='Имя')
#     last_name = models.CharField(max_length=20, verbose_name='Фамилия')
#     email = models.EmailField(verbose_name='e-mail')
#
#
# class Customers:
#     """Клиенты пользователя"""
#     first_name = models.CharField(max_length=20, verbose_name='Имя')
#     last_name = models.CharField(max_length=20, verbose_name='Фамилия')
#     email = models.EmailField(verbose_name='e-mail')
#
#
# class Mailing(models.Model):
#     """Рассылка"""
#     name = models.CharField(max_length=50, verbose_name='название', default='рассылка')
#     create_date = models.DateField(auto_now_add=True, verbose_name='дата создания')
#     send_date = models.DateField(verbose_name='дата отправления')
#     time = models.TimeField(verbose_name='время')
#     period = models.CharField(max_length=50, choices=PERIOD_CHOICES, default='none', verbose_name='периодичность')
#     repetitions = models.SmallIntegerField(verbose_name='количество повторений', default=1)
#     status = models.CharField(max_length=50, default='created', verbose_name='статус')
#     customers = models.ManyToManyField(Customers, verbose_name='клиенты пользователя')
#     mail = models.ForeignKey(Mail, on_delete=models.CASCADE, verbose_name='письмо')
#     user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
#
#     class Meta:
#         verbose_name = 'рассылка'
#         verbose_name_plural = 'рассылки'
#         ordering = ('-pk',)
#
#     def __str__(self):
#         return f'{self.mail}, {self.send_date}'
