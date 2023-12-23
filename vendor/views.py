from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test, login_required
from accounts.views import validate_vendor
# Create your views here.

@login_required(login_url='login')
@user_passes_test(validate_vendor)
def vendor_profile(request):
    return render(request, 'vendor/vendor_profile.html')