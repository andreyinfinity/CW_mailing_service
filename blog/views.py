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
        """Запрет на показ неопубликованной статьи"""
        self.object = super().get_object(queryset)
        if not self.object.is_published:
            raise Http404
        return self.object
