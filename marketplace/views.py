from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from menu.models import Category, FoodItem
from vendor.models import Vendor
from django.db.models import Prefetch
from .models import Cart
from .context_processors import get_food_count
from django.contrib.auth.decorators import login_required


# Create your views here.


def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    context = {
        'vendors': vendors
    }
    return render(request, 'marketplace/listing.html', context)


def vendor_detail(request, vendor_slug):
    food_items_in_cart = None
    if request.user.is_authenticated:
        food_items_in_cart = Cart.objects.filter(user=request.user)

    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'food_items',
            queryset=FoodItem.objects.filter(is_available=True)
        )
    )

    context = {
        'vendor': vendor,
        'categories': categories,
        'food_items_in_cart': food_items_in_cart,
    }

    if food_items_in_cart:
        foods_in_cart = [
            food_item_in_cart.food_item for food_item_in_cart in food_items_in_cart]
        context['foods_in_cart'] = foods_in_cart

    return render(request, 'marketplace/vendor_detail.html', context)


def add_to_cart(request, food_id=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                food_item = FoodItem.objects.get(id=food_id)
            except:
                return JsonResponse({'status': 'Failed', 'message': 'No Food Item Found with this ID', 'code': 404})
            else:
                try:
                    fooditem_from_cart = Cart.objects.get(
                        user=request.user, food_item=food_item)
                except:
                    new_cart_item = Cart.objects.create(
                        user=request.user, food_item=food_item, quantity=1)
                    new_cart_item.save()
                    return JsonResponse({'status': 'Success', 'message': f'{food_item} Added to Cart', 'code': 200, 'quantity': 1, 'total_quantity': get_food_count(request)})

                else:
                    fooditem_from_cart.quantity += 1
                    fooditem_from_cart.save()
                    return JsonResponse({'status': 'Success', 'message': f'Quantity Increased Successfully for {food_item}', 'code': 200, 'quantity': fooditem_from_cart.quantity, 'total_quantity': get_food_count(request)})

        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid Request', 'code': 408})

    else:
        return JsonResponse({'status': 'Failed', 'message': 'Please Login to Your Account', 'code': 400})


def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                food_item = FoodItem.objects.get(id=food_id)
            except:
                return JsonResponse({'status': 'Failed', 'message': 'No Food Item Found with this ID', 'code': 404})
            else:
                try:
                    fooditem_from_cart = Cart.objects.get(user=request.user, food_item=food_item)
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'This Item is not in your Cart', 'code': 405})

                else:
                    if fooditem_from_cart.quantity > 1:
                        fooditem_from_cart.quantity -= 1
                        fooditem_from_cart.save()
                        return JsonResponse({'status': 'Success', 'message': f'Quantity Decreased Successfully for {food_item}', 'code': 200, 'quantity': fooditem_from_cart.quantity, 'total_quantity': get_food_count(request)})

                    else:
                        fooditem_from_cart.delete()
                        return JsonResponse({'status': 'Success', 'message': f'{food_item} Removed from Cart', 'code': 201, 'quantity': 0, 'total_quantity': get_food_count(request)})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid Request', 'code': 408})
        
    else:
        return JsonResponse({'status': 'Failed', 'message': 'Please Login to Your Account', 'code': 400})


@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/cart.html', context)


def delete_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                food_item = FoodItem.objects.get(id=food_id)
            except:
                return JsonResponse({'status': 'Failed', 'message': 'No Food Item Found with this ID', 'code': 404})
            else:
                try:
                    fooditem_from_cart = Cart.objects.get(user=request.user, food_item=food_item)
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'This Item is not in your Cart', 'code': 405})

                else:
                    fooditem_from_cart.delete()
                    return JsonResponse({'status': 'Success', 'message': f'{food_item} Removed from Cart', 'code': 201, 'total_quantity': get_food_count(request)})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid Request', 'code': 408})