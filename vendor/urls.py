from django.urls import path
from . import views

urlpatterns = [
    path('Dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('profile/', views.vendor_profile, name='vendor_profile'),
    path('menu-builder/', views.menu_builder, name='menu_builder'),
    path('menu-builder/category/<int:pk>/', views.fooditems_by_category, name='fooditems_by_category'),

    # Category CRUD URLs
    path('menu-builder/category/add', views.add_category, name='add_category'),
    path('menu-builder/category/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('menu-builder/category/delete/<int:pk>/', views.delete_category, name='delete_category'),

    # Food Item CRUD URLs
    path('menu-builder/food/add', views.add_food, name='add_food'),
    path('menu-builder/food/edit/<int:pk>/', views.edit_food, name='edit_food'),
    path('menu-builder/food/delete/<int:pk>/', views.delete_food, name='delete_food'),

    path('opening-hours/', views.opening_hours, name='opening_hours'),

    # Opening Hours CRUD URLs
    path('opening-hours/add', views.add_opening_hours, name='add_opening_hours'),
    path('opening-hours/remove/<int:pk>/', views.remove_opening_hours, name='remove_opening_hours'),

    # Orders URLs
    path('orders/', views.orders, name='vendor_orders'),
    path('orders/status/<str:order_id>', views.order_status, name='vendor_order_status'),
    path('send-out-for-delivery/<str:id>', views.send_out_for_delivery, name='send_out_for_delivery'),

    # Change Password
    path('change-password/', views.change_password, name='change_vendor_password'),
]
