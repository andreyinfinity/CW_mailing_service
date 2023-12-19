from django.urls import path

from mailing.apps import MailingConfig
from mailing import views

app_name = MailingConfig.name

urlpatterns = [
    path('mails/', views.MailView.as_view(), name='mails'),
    path('mails/create/', views.MailCreateView.as_view(), name='create'),
    path('mails/edit/<int:pk>', views.MailUpdateView.as_view(), name='edit'),
    path('mails/delete/<int:pk>', views.MailDeleteView.as_view(), name='delete'),
]