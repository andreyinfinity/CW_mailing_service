from django.urls import path
from customer.apps import CustomerConfig
from customer import views

app_name = CustomerConfig.name

urlpatterns = [
    path('', views.CustomerView.as_view(), name='customers'),
    path('create/', views.CustomerCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.CustomerUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.CustomerDeleteView.as_view(), name='delete'),
    path('<int:pk>', views.toggle_subscribe, name='toggle_subscribe')
]