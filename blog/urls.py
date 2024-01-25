from django.urls import path
from django.views.decorators.cache import cache_page

from blog import views
from blog.apps import BlogConfig

app_name = BlogConfig.name

urlpatterns = [
    path('', views.PostListView.as_view(), name='blog'),
    path('<int:pk>/', cache_page(60 * 30)(views.PostDetailView.as_view()), name='post'),
]
