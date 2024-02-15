from orders.models import Order
from .models import Vendor
import datetime
from .models import OpeningHours


def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor


def get_all_orders(request):
    all_orders = Order.objects.filter(
        cart_item__food_item__vendor=get_vendor(request), cart_item__order_status='Ordered').distinct()
    
    return all_orders
