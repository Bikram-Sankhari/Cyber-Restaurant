from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.vendor_profile, name='vendor_profile'),
]
