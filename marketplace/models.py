from django.db import models
from accounts.models import User
from menu.models import FoodItem
from orders.models import Order


ORDER_STATUS_CHOICES = (
    ('Ordered', 'Ordered'),
    ('Payment Pending', 'Payment Pending'),
    ('Unordered', 'Unordered'),
)

# Create your models here.
class Cart(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order_status = models.CharField(max_length=15, choices=ORDER_STATUS_CHOICES, default='Unordered')

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Cart'

    def __unicode__(self):
        return self.user

    def total_price(self):
        return self.quantity * self.food_item.price