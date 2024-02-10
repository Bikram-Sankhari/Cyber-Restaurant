from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from accounts.models import User
# Create your models here.

STATUS_CHOICES = (
    ('Initiated', 'Initiated'),
    ('Completed', 'Completed'),
    ("Pending", 'Pending'),
    ('Failed', 'Failed'),
)

class Order(models.Model):
    order_id = models.CharField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_first_name = models.CharField(max_length=50)
    delivery_last_name = models.CharField(max_length=50)
    delivery_email = models.EmailField(max_length=120)
    delivery_phone_number = models.CharField(max_length=12)
    delivery_address = models.CharField(max_length=500)
    delivery_country = models.CharField(max_length=15)
    delivery_state = models.CharField(max_length=15)
    delivery_city = models.CharField(max_length=15)
    delivery_pin_code = models.CharField(max_length=6)
    price_details = models.JSONField(encoder=DjangoJSONEncoder)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    transaction_details = models.JSONField(encoder=DjangoJSONEncoder, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.delivery_first_name} {self.delivery_last_name} - Order ID: {self.order_id}'
