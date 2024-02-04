from marketplace.models import Cart
from datetime import datetime

def get_order_details(request):
    cart_items = Cart.objects.filter(user=request.user)
    result = {}
    for item in cart_items:
        result[item.food_item.id] = {'quantity': item.quantity,
                                     'rate': item.food_item.price,
                                     'total': item.food_item.price * item.quantity,}
        
    return result


def generate_order_id(request):
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    order_id = f"{request.user.id}-{now}"
    return order_id