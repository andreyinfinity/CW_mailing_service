from django.contrib import admin
from django.utils.safestring import mark_safe

from blog.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'viewed', 'create_date', 'is_published']
    list_editable = ['is_published']
    list_filter = ['is_published', 'create_date']
    ordering = ['-create_date']
    search_fields = ['title', 'body']
    fields = ['title', 'body', ('image', 'get_image'), ('viewed', 'create_date')]
    readonly_fields = ['viewed', 'create_date', 'get_image']

    def get_image(self, object):
        """Метод для показа изображения"""
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=300>")

    get_image.short_description = "изображение"
