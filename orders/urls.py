from django.urls import path
from . import views

urlpatterns = [
    path('review-order/', views.review_order, name='review_order'),
    path('check_phonepe_order_status/<str:order_id>', views.check_phonepe_order_status, name='check_phonepe_order_status'),
    path('order-status/<str:order_id>', views.order_status, name='order_status'),
]