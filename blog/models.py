from django.db import models
from users.models import NULLABLE


class Post(models.Model):
    """Публикация"""
    title = models.CharField(max_length=200, verbose_name='заголовок')
    body = models.TextField(verbose_name='содержимое статьи')
    image = models.ImageField(upload_to='blog/', verbose_name='изображение', **NULLABLE)
    viewed = models.IntegerField(default=0, verbose_name='количество просмотров')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='дата публикации')
    is_published = models.BooleanField(default=True, verbose_name='опубликована')

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'публикации'
        ordering = ('-pk',)

    def __str__(self):
        return self.title
