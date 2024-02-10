from marketplace.models import Cart
from datetime import datetime
from marketplace.utils import get_cart_items
from .models import Order
from decouple import config
import requests
from hashlib import sha256
from decouple import config


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
    response = requests.get(url, headers=headers, params=parameters)

    order.transaction_details = response.json()


    if 'data' in response.json():
        if response.json()['data']['state'] == 'COMPLETED':
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
            item.save()

    elif order.status == 'Pending':
        for item in food_items_in_order:
            item.order_status = 'Payment Pending'
            item.save()    