from django.db.models import F
from django.http import Http404
from django.views import generic
from blog.models import Post


class PostListView(generic.ListView):
    """Список статей блога"""
    model = Post

    def get_queryset(self):
        """Показ только опубликованных статей"""
        return super().get_queryset().filter(is_published=True)


class PostDetailView(generic.DetailView):
    """Просмотр статьи блога"""
    model = Post

    def get_object(self, queryset=None):
        """Запрет на показ неопубликованной статьи и счетчик просмотров"""
        post = super().get_object(queryset)
        if not post.is_published:
            raise Http404
        post.viewed += 1
        post.save()
        return post
