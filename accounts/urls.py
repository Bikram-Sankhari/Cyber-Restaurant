from django.urls import path
from . import views

urlpatterns = [
    path('registerUser/', views.register_user, name='register_user'),
    path('registerVendor/', views.register_vendor, name='register_vendor'),
    path('login/', views.login,  name='login'),
    path('logout/', views.logout, name='logout'),
    path('myAccount/', views.my_account, name='my_account'),
    path('vendorDashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('customerDashboard/', views.customer_dashboard, name='customer_dashboard'),
]
