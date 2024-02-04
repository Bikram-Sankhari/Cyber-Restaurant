from django.urls import path
from . import views

urlpatterns = [
    path('review-order/', views.review_order, name='review_order'),
]