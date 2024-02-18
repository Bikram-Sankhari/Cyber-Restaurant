from django.shortcuts import render, redirect
from vendor.models import Vendor
from . utils import get_location, set_location
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from django.contrib import messages


def home(request):
    if get_location(request):
        longitude = request.session['longitude']
        latitude = request.session['latitude']
        current_point = GEOSGeometry(
            f"POINT({longitude} {latitude})", srid=4326)
        vendors = Vendor.objects.filter(
            is_approved=True,
            user__is_active=True,
            user_profile__location__distance_lte=(
                current_point, D(km=50))
        ).annotate(distance=Distance("user_profile__location", current_point)
                   ).order_by("distance")
        for vendor in vendors:
            vendor.distance = round(vendor.distance.km, 2)
    else:
        vendors = Vendor.objects.filter(
            is_approved=True, user__is_active=True)[:8]
        print(vendors)
    context = {
        'vendors': vendors,
    }
    return render(request, 'index.html', context)


def location_accessed(request):
    current_url = set_location(
        request, request.GET['longitude'], request.GET['latitude'], request.GET['current_url'])
    messages.success(request, 'Your location has been updated')
    return redirect(current_url)
