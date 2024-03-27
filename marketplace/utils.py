from .models import Cart

GST_PERCENTAGE = 18

def get_amounts(request):
    subtotal = 0
    gst = 0
    total = 0
    if request.user.is_authenticated:
        cart_items = get_cart_items(request)

        # Calculate Subtotal
        for cart_item in cart_items:
            subtotal += (cart_item.quantity * cart_item.food_item.price)
        
        # Calculate GST
        gst = float(subtotal) * GST_PERCENTAGE / 100

        # Calculate Total
        total = float(subtotal) + gst

        # Format Results
        gst = format(gst, ".2f")
        subtotal = format(subtotal, ".2f")
        total = format(total, ".2f")
        
    return {'subtotal': subtotal, 'gst': gst, 'total': total}

def get_cart_items(request):
    return Cart.objects.filter(user=request.user, order_status='Unordered')

def get_food_item_in_cart(request, food_item):
    return Cart.objects.get(user=request.user, food_item=food_item, order_status='Unordered')

def get_cart_context(request):
    cart_items = get_cart_items(request)
    amounts = get_amounts(request)
    context = {
        'cart_items': cart_items,
        'subtotal': amounts['subtotal'],
        'gst': amounts['gst'],
        'total': amounts['total'],
    }

    return context