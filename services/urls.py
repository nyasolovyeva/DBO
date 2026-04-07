from django.urls import path
from . import views

urlpatterns = [
    path('', views.bank_list, name='bank_list'),
    path('service/<int:pk>/', views.service_detail, name='service_detail'),
    path('compare/', views.compare_services, name='compare_services'),
]