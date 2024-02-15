from django.shortcuts import redirect, render
from accounts.utils import validate_customer
from django.contrib.auth.decorators import user_passes_test, login_required
from marketplace.models import Cart
from .utils import get_user_profile
from .forms import CustomerUserForm, ChangePasswordForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from django.contrib import messages
from orders.models import Order
from orders.utils import get_orders
from django.contrib import auth


# Dashhoard
@login_required(login_url='login')
@user_passes_test(validate_customer)
def customer_dashboard(request):
    orders = get_orders(request)
    recent_orders = orders[:5]

    context = {
        'order_count': orders.count(),
        'orders': recent_orders,
    }

    return render(request, 'customer/dashboard.html', context)


# My Orders
@login_required(login_url='login')
@user_passes_test(validate_customer)
def my_orders(request):
    orders = get_orders(request)

    context = {
        'orders': orders,
    }

    return render(request, 'customer/my_orders.html', context)


# Delivery Status
@login_required(login_url='login')
def delivery_status(request, order_id):
    try:
        order = Order.objects.get(order_id=order_id, user=request.user)

    except Order.DoesNotExist:
        messages.error(request, 'Invalid Order ID!')
        return redirect('my_orders')

    else:
        cart_items = Cart.objects.filter(order=order)
        context = {
            'order': order,
            'cart_items': cart_items,
        }

        return render(request, 'customer/delivery_status.html', context)


# Profile Settings
@login_required(login_url='login')
@user_passes_test(validate_customer)
def customer_profile(request):
    if request.method == 'POST':
        user_form = CustomerUserForm(request.POST, instance=request.user)
        username = request.user.username
        
        profile_form = UserProfileForm(request.POST, request.FILES, instance=get_user_profile(request))
        if user_form.is_valid() and profile_form.is_valid():
            # Check for username changing attempt
            if user_form.cleaned_data['username'] != username:
                user = user_form.save(commit=False)
                user.username = username
                user.save()
                user_form = CustomerUserForm(instance=user)
                messages.info(request, 'Username cannot be changed')

            else:
                user_form.save()

            profile_form.save()
        
            messages.success(request, 'Profile updated successfully')
    else:
        user_form = CustomerUserForm(instance=request.user)
        profile_form = UserProfileForm(instance=get_user_profile(request))

    context = {
        'user_form': user_form,
        'user_profile_form': profile_form,
    }

    return render(request, 'customer/profile.html', context)


# Change Password
@login_required(login_url='login')
@user_passes_test(validate_customer)
def change_customer_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        user = auth.authenticate(username=request.user.username, password=request.POST['old_password'])

        if user:
            if form.is_valid():
                request.user.set_password(form.cleaned_data['new_password'])
                request.user.save()
                auth.logout(request)
                messages.success(request, 'Password changed successfully')
                return redirect('login')
            
        else:
            messages.error(request, 'Invalid Current Password')
            return redirect('change_customer_password')
    else:
        form = ChangePasswordForm()

    context = {
        'form': form,
    }
    print(form.errors)
    return render(request, 'customer/change_customer_password.html', context)