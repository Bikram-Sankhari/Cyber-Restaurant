from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from accounts.models import User
from marketplace.models import Cart
from vendor.models import Vendor
from marketplace.utils import GST_PERCENTAGE

# Create your models here.

STATUS_CHOICES = (
    ('Initiated', 'Initiated'),
    ('Completed', 'Completed'),
    ("Pending", 'Pending'),
    ('Failed', 'Failed'),
)

request_from_middleware = None


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
    transaction_details = models.JSONField(
        encoder=DjangoJSONEncoder, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.delivery_first_name} {self.delivery_last_name} - Order ID: {self.order_id}'

    def check_status_for_customer(self, status):
        cart_items = Cart.objects.filter(order=self)
        for item in cart_items:
            if item.delivery_status != status:
                return False

        return True

    def is_fully_delivered_for_customer(self):
        return self.check_status_for_customer('Delivered')

    def is_fully_preparing_for_customer(self):
        return self.check_status_for_customer('Preparing')

    def is_fully_on_the_way_for_customer(self):
        return self.check_status_for_customer('On The Way')

    def get_current_vendor(self):
        vendor = Vendor.objects.get(user=request_from_middleware.user)
        return vendor
    
    def get_all_vendors(self):
        all_cart_items = Cart.objects.filter(order=self)
        vendors = set()
        for item in all_cart_items:
            if item.food_item.vendor not in vendors:
                vendors.add(item.food_item.vendor)

        return vendors        
    
    def get_cart_items_by_vendor(self):
        vendor = self.get_current_vendor()
        cart_items = Cart.objects.filter(
            order=self, food_item__vendor=vendor, order_status='Ordered')

        return cart_items

    def get_vendor_price_details(self):
        cart_items = self.get_cart_items_by_vendor()

        subtotal = 0
        for item in cart_items:
            subtotal += item.food_item.price * item.quantity

        tax = subtotal * GST_PERCENTAGE / 100
        total = subtotal + tax

        return {'subtotal': subtotal, 'tax': tax, 'total': total}

    def check_status_by_vendor(self, status: str):
        cart_items = self.get_cart_items_by_vendor()

        for item in cart_items:
            if item.delivery_status != status:
                return False

        return True

    def is_fully_delivered_by_vendor(self):
        return self.check_status_by_vendor('Delivered')

    def is_fully_preparing_by_vendor(self):
        return self.check_status_by_vendor('Preparing')

    def is_fully_on_the_way_by_vendor(self):
        return self.check_status_by_vendor('On The Way')
