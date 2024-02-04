from accounts.models import UserProfile
from vendor.models import Vendor
from django.conf import settings
from django.shortcuts import get_object_or_404


def get_vendor(request):
    if request.user.is_authenticated and request.user.get_role() == 'vendor':
        vendor = Vendor.objects.get(user=request.user)
    else:
        vendor = None
    return dict(vendor=vendor)

def get_google_api_key(request):
    return {'GOOGLE_API_KEY': settings.GOOGLE_API_KEY}

def get_user_profile(request):
    if request.user.is_authenticated:
        user_profile = get_object_or_404(UserProfile, user=request.user)
    else:
        user_profile = None
    return dict(user_profile=user_profile)
