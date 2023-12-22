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
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('validate_forgot_password/<uidb64>/<token>', views.validate_forgot_password, name='validate_forgot_password'),
    path('reset_password/', views.reset_password, name='reset_password'),
]
