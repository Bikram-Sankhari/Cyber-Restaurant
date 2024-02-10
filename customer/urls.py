from django.urls import path
from . import views

urlpatterns = [
    path('Dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('profile/', views.customer_profile, name='customer_profile'),
    path('change-customer-password', views.change_customer_password, name='change_customer_password'),
]