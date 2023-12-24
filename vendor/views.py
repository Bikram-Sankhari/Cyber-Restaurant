from django.shortcuts import redirect, render
from django.contrib.auth.decorators import user_passes_test, login_required
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from accounts.views import validate_vendor
from .models import Vendor
from .forms import VendorForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
# Create your views here.


@login_required(login_url='login')
@user_passes_test(validate_vendor)
def vendor_profile(request):
    vendor = get_object_or_404(Vendor, user=request.user)
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        user_profile_form = UserProfileForm(
            request.POST, request.FILES, instance=profile)

        if vendor_form.is_valid() and user_profile_form.is_valid():
            vendor_form.save()
            user_profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('vendor_profile')
        else:
            print(vendor_form.errors)
            print(user_profile_form.errors)

            context = {
                'vendor_form': vendor_form,
                'user_profile_form': user_profile_form,
                'profile': profile,
                'vendor': vendor,
            }

            return render(request, 'vendor/vendor_profile.html', context)
    else:
        vendor_form = VendorForm(instance=vendor)
        user_profile_form = UserProfileForm(instance=profile)
        context = {
            'vendor_form': vendor_form,
            'user_profile_form': user_profile_form,
            'profile': profile,
            'vendor': vendor,
        }
        return render(request, 'vendor/vendor_profile.html', context)
