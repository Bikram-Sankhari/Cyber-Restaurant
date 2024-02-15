from django.db import models
from accounts.models import User
from menu.models import FoodItem


ORDER_STATUS_CHOICES = (
    ('Ordered', 'Ordered'),
    ('Payment Pending', 'Payment Pending'),
    ('Unordered', 'Unordered'),
)

DELIVERY_STATUS_CHOICES = (
    ('Unconfirmed', 'Unconfirmed'),
    ('Preparing', 'Preparing'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
)

# Create your models here.c
class Cart(models.Model):
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, null=True, related_name='cart_item')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order_status = models.CharField(max_length=15, choices=ORDER_STATUS_CHOICES, default='Unordered')
    delivery_status = models.CharField(max_length=15, choices=DELIVERY_STATUS_CHOICES, default='Unconfirmed')

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Cart'

    def __unicode__(self):
        return self.user

    def total_price(self):
        return self.quantity * self.food_item.price