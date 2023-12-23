from vendor.models import Vendor

def get_vendor(request):
    if request.user.is_authenticated and request.user.get_role() == 'vendor':
        vendor = Vendor.objects.get(user=request.user)
    else:
        vendor = None
    return dict(vendor=vendor)