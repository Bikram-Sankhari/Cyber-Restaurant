from django.db import models
from django.core.serializers.json import DjangoJSONEncoder

# Create your models here.

STATUS_CHOICES = (
    ('Completed', 'Completed'),
    ("Pending", 'Pending'),
    ('Cancelled', 'Cancelled'),
)

class Order(models.Model):
    order_id = models.CharField(primary_key=True)
    delivery_first_name = models.CharField(max_length=50)
    delivery_last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=80)
    delivery_email = models.EmailField(max_length=120)
    delivery_phone_number = models.CharField(max_length=12)
    delivery_address = models.CharField(max_length=500)
    delivery_country = models.CharField(max_length=15)
    delivery_state = models.CharField(max_length=15)
    delivery_city = models.CharField(max_length=15)
    delivery_pin_code = models.CharField(max_length=6)
    order_details = models.JSONField(encoder=DjangoJSONEncoder)
    price_details = models.JSONField(encoder=DjangoJSONEncoder)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.delivery_first_name} {self.delivery_last_name} - Order ID: {self.order_id}'
