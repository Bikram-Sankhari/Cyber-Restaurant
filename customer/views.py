from django.shortcuts import redirect, render
from accounts.utils import validate_customer
from django.contrib.auth.decorators import user_passes_test, login_required
from .utils import get_user_profile
from .forms import CustomerUserForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from django.contrib import messages

# Create your views here.


@login_required(login_url='login')
@user_passes_test(validate_customer)
def customer_dashboard(request):
    return render(request, 'customer/dashboard.html')


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
                user_form.cleaned_data['username'] = username
                messages.info(request, 'Username cannot be changed')
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
