from .models import Cart

GST_PERCENTAGE = 18

def get_amounts(request):
    subtotal = 0
    gst = 0
    total = 0
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)

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