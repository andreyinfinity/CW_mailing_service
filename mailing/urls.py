from django.urls import path
from mailing.apps import MailingConfig
from mailing import views

app_name = MailingConfig.name

urlpatterns = [
    path('mails/', views.MailView.as_view(), name='mails'),
    path('mails/create/', views.MailCreateView.as_view(), name='create'),
    path('mails/<int:pk>/edit/', views.MailUpdateView.as_view(), name='edit'),
    path('mails/<int:pk>/delete/', views.MailDeleteView.as_view(), name='delete'),
    path('mailings/', views.MailingView.as_view(), name='mailings'),
    path('mailings/create/', views.MailingCreateView.as_view(), name='create_mailing'),
    path('mailings/<int:pk>/edit/', views.MailingUpdateView.as_view(), name='edit_mailing'),
    path('mailings/<int:pk>/delete/', views.MailingDeleteView.as_view(), name='delete_mailing'),
]