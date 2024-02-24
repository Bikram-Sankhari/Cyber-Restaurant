from marketplace.models import Cart
from datetime import datetime
from marketplace.utils import get_cart_items
from .models import Order
from decouple import config
import requests
from hashlib import sha256
import django.dispatch
from django.dispatch import receiver


payment_done_singal = django.dispatch.Signal()
items_ordered_singal = django.dispatch.Signal()

def generate_order_id(request):
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    order_id = f"{request.user.id}-{now}"
    return order_id


PHONEPE_MERCHANT_ID = config('PHONEPE_MERCHANT_ID')
PHONEPE_SALT_KEY = config('PHONEPE_SALT_KEY')
PHONEPE_SALT_INDEX = config('PHONEPE_SALT_INDEX')

def call_phonepe_order_status_api(request, order):
    x_verify_hash = sha256(f"/pg/v1/status/{PHONEPE_MERCHANT_ID}/{order.order_id}{PHONEPE_SALT_KEY}".encode()).hexdigest()

    headers = {
        'Content-Type': 'application/json',
        'X-VERIFY': f"{x_verify_hash}###{PHONEPE_SALT_INDEX}",
        'X-MERCHANT-ID': PHONEPE_MERCHANT_ID,
    }

    parameters = {
        'merchantId': PHONEPE_MERCHANT_ID,
        'merchantTransactionId': order.order_id,
    }

    url = f"https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/status/{PHONEPE_MERCHANT_ID}/{order.order_id}"
    try:
        response = requests.get(url, headers=headers, params=parameters)
    except Exception as e:
        print(e)
        return False

    order.transaction_details = response.json()


    if 'data' in response.json():
        if response.json()['data']['state'] == 'COMPLETED':
            payment_done_singal.send(sender=None, order=order, request=request)
            order.status = 'Completed'
        elif response.json()['data']['state'] == 'FAILED':
            order.status = 'Failed'
        elif response.json()['data']['state'] == 'PENDING':
            order.status = 'Pending'
            # Here need to call another application by it's API to keep checking for the update an display that to the user

    order.save()

    # Update Food Items status in the Order
    food_items_in_order = Cart.objects.filter(order=order)
    if order.status == 'Completed':
        for item in food_items_in_order:
            item.order_status = 'Ordered'
            item.delivery_status = 'Preparing'
            item.save()
            
        items_ordered_singal.send(sender=None, order=order, request=request)

    elif order.status == 'Pending':
        for item in food_items_in_order:
            item.order_status = 'Payment Pending'
            item.save()    

    return True

def get_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-updated_at')
    return orders
