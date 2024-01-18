from .models import Cart


def get_food_count(request):
    if request.user.is_authenticated:
        food_items_in_cart = Cart.objects.filter(user=request.user)
        total_qty = 0
        for food_item in food_items_in_cart:
            total_qty += food_item.quantity
        return dict(food_count=total_qty)
    return dict(food_count=0)