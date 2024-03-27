def get_location(request):
    if 'longitude' in request.session and 'latitude' in request.session:
        return True
    else:
        return False
    
def set_location(request, longitude, latitude, current_url):
    request.session['longitude'] = longitude
    request.session['latitude'] = latitude
    request.session['current_url'] = current_url
    return request.GET['current_url']