from accounts.models import UserProfile
from django.shortcuts import get_object_or_404

def get_user_profile(request):
    if request.user.is_authenticated:
        return get_object_or_404(UserProfile, user=request.user)
    return None
