import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from menu.models import Category, FoodItem
from vendor.models import Vendor, OpeningHours
from django.db.models import Prefetch
from .models import Cart
from .context_processors import get_food_count
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages
from django.db.models import Q
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from Restaurant.utils import get_or_set_location


# Create your views here.

def get_subtotal(request):
    subtotal = 0
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        for cart_item in cart_items:
            subtotal += (cart_item.quantity * cart_item.food_item.price)
    return format(subtotal, ".2f")


def marketplace(request):
    try:
        radius = int(request.GET['radius'])
    except MultiValueDictKeyError:
        vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    except ValueError:
        messages.error(request, 'Invalid Input')
        return redirect('home')

    # for searching the marketplace
    else:
        try:
            latitude = float(request.GET['lat'])
            longitude = float(request.GET['long'])

        except ValueError:
            if get_or_set_location(request):
                latitude = request.session['latitude']
                longitude = request.session['longitude']
            
            else:
                latitude = longitude = None

        if latitude and longitude:
            if radius < 5:
                messages.error(request, 'Minimum Radius should be 5 KM')
                return redirect('home')
            elif radius > 50:
                messages.error(request, 'Maximum Radius should be 50 KM')
                return redirect('home')

            current_point = GEOSGeometry(
                f"POINT({longitude} {latitude})", srid=4326)
            keywords = request.GET['keywords']
            if keywords:
                # Fetch the IDs of vendors by Searching FoodItems for the keywords
                id_of_food_items = FoodItem.objects.filter(
                    food_title__icontains=keywords, is_available=True).values_list('vendor', flat=True)

                # Fetch IDs of vendors by searching Categories for the keywords
                id_of_food_categories = Category.objects.filter(
                    category_name__icontains=keywords).values_list('vendor', flat=True)

                vendors = Vendor.objects.filter(Q(id__in=id_of_food_categories) |
                                                Q(id__in=id_of_food_items) |
                                                Q(vendor_name__icontains=keywords),
                                                Q(is_approved=True,
                                                user__is_active=True),
                                                user_profile__location__distance_lte=(
                                                    current_point, D(km=radius))
                                                ).annotate(distance=Distance("user_profile__location", current_point)
                                                        ).order_by("distance")

            else:
                vendors = Vendor.objects.filter(
                    is_approved=True,
                    user__is_active=True,
                    user_profile__location__distance_lte=(
                        current_point, D(km=radius))
                ).annotate(distance=Distance("user_profile__location", current_point)
                        ).order_by("distance")
                
            for vendor in vendors:
                vendor.distance = round(vendor.distance.km, 2)
        else:
            messages.error(request, 'Please enable Location Services')
            return redirect('home')


    context = {
        'vendors': vendors,
        'vendor_count': vendors.count(),
    }

    return render(request, 'marketplace/listing.html', context)


def vendor_detail(request, vendor_slug):
    food_items_in_cart = None
    if request.user.is_authenticated:
        food_items_in_cart = Cart.objects.filter(user=request.user)

    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    vendor_open = OpeningHours.objects.filter(vendor=vendor).order_by('day', 'open')
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
        'open_hours': vendor_open,
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
                    return JsonResponse({'status': 'Success',
                                         'message': f'{food_item} Added to Cart',
                                         'code': 200, 'quantity': 1,
                                         'total_quantity': get_food_count(request),
                                         'subtotal': get_subtotal(request)})

                else:
                    fooditem_from_cart.quantity += 1
                    fooditem_from_cart.save()
                    return JsonResponse({'status': 'Success',
                                         'message': f'Quantity Increased Successfully for {food_item}',
                                         'code': 200, 'quantity': fooditem_from_cart.quantity,
                                         'total_quantity': get_food_count(request),
                                         'subtotal': get_subtotal(request)})

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
                    fooditem_from_cart = Cart.objects.get(
                        user=request.user, food_item=food_item)
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'This Item is not in your Cart', 'code': 405})

                else:
                    if fooditem_from_cart.quantity > 1:
                        fooditem_from_cart.quantity -= 1
                        fooditem_from_cart.save()
                        return JsonResponse({'status': 'Success',
                                             'message': f'Quantity Decreased Successfully for {food_item}',
                                             'code': 200,
                                             'quantity': fooditem_from_cart.quantity,
                                             'total_quantity': get_food_count(request),
                                             'subtotal': get_subtotal(request)})

                    else:
                        return JsonResponse({'status': 'Success',
                                             'message': f'{food_item} will be Removed from Cart',
                                             'code': 201,
                                             'quantity': 0,
                                             'total_quantity': get_food_count(request)})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid Request', 'code': 408})

    else:
        return JsonResponse({'status': 'Failed', 'message': 'Please Login to Your Account', 'code': 400})


@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    subtotal = get_subtotal(request)
    gst = format(float(subtotal) * 18 / 100, ".2f")
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'gst': gst,
        'total': format(float(subtotal) + (float(subtotal) * 18 / 100), ".2f"),
    }
    return render(request, 'marketplace/cart.html', context)


@login_required(login_url='login')
def delete_cart(request, food_id):
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
                    return JsonResponse({'status': 'Failed', 'message': 'This Item is not in your Cart', 'code': 405})

                else:
                    fooditem_from_cart.delete()
                    return JsonResponse({'status': 'Success',
                                         'message': f'{food_item} Removed from Cart',
                                         'code': 200,
                                         'total_quantity': get_food_count(request),
                                         'subtotal': get_subtotal(request)})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid Request', 'code': 408})
