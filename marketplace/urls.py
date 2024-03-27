from django.urls import path
from . import views

urlpatterns = [
    path('', views.marketplace, name='marketplace'),

    # Url for Cart
    path('cart/', views.cart, name='cart'),

    # Url for Vendor Details Page
    path('<slug:vendor_slug>/', views.vendor_detail, name='vendor_detail'),

    path('add_to_cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    path('decrease_item/<int:food_id>/', views.decrease_cart, name='decrease_cart'),
    path('delete_cart/<int:food_id>/', views.delete_cart, name='delete_cart'),
]