from django.urls import path

from blog import views
from blog.apps import BlogConfig

app_name = BlogConfig.name

urlpatterns = [
    path('', views.PostListView.as_view(), name='blog'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post'),
]