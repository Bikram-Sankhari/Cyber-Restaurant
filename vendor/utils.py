from orders.models import Order
from .models import Vendor
from django.shortcuts import get_list_or_404
from marketplace.models import Cart
from django.db.models import Prefetch, Q
from django.core.paginator import Paginator


# Not used in orders.models due to circularimport error
def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor


def get_all_orders_for_vendor(request):
    all_orders = Order.objects.filter(
        cart_item__food_item__vendor=get_vendor(request), cart_item__order_status='Ordered').order_by('-updated_at').distinct().prefetch_related(
            Prefetch(
                'cart_item',
                queryset=Cart.objects.filter(
                    Q(food_item__vendor=get_vendor(request))
                )
            )
    )

    return all_orders


def paginate(request, obj, orders_per_page):
    paginator = Paginator(obj, orders_per_page)

    try:
        page_number = request.GET.get("page")
    except:
        page_number = 1

    page_obj = paginator.get_page(page_number)

    return page_obj
