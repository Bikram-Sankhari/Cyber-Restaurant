from django.urls import path
from . import views

urlpatterns = [
    path('Dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('profile/', views.customer_profile, name='customer_profile'),
]