from django.contrib.auth.views import LogoutView
from django.urls import path

from users.apps import UserConfig
from users.views import LoginUser, UserRegistration, UserUpdateView, activate, UserListView, toggle_active

app_name = UserConfig.name

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', UserRegistration.as_view(), name='registration'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('users/', UserListView.as_view(), name='users'),
    path('activate/<str:code>', activate, name='activate'),
    path('toggle_active/<int:pk>', toggle_active, name='toggle_active'),
]