
def get_or_set_location(request):
    if 'longitude' in request.session and 'latitude' in request.session:
        return True
    elif 'longitude' in request.GET and 'latitude' in request.GET:
        longitude = request.GET['longitude']
        latitude = request.GET['latitude']
        request.session['longitude'] = longitude
        request.session['latitude'] = latitude
        return True
    else:
        return False