from .models import Vendor
import datetime
from .models import OpeningHours

def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor