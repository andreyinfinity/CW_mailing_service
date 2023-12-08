from django.urls import path

from home.apps import HomeConfig
from home.views import IndexView

app_name = HomeConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]