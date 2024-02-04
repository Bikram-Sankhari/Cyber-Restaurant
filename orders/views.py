import base64
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from Restaurant.utils import get_location
from marketplace.utils import get_cart_context, get_amounts
from django.contrib import messages
from .utils import generate_order_id, get_order_details
from .forms import OrderForm
from accounts.models import UserProfile
import requests
from django.conf import settings
import requests
from hashlib import sha256
import json

# Create your views here.


@login_required(login_url='login')
def review_order(request):
    context = get_cart_context(request)
    if not context['cart_items']:
        messages.info(request, 'Please add Items to your Cart to Checkout !')
        return redirect('marketplace')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.username = request.user.username
            obj.order_details = get_order_details(request)
            obj.price_details = get_amounts(request)
            obj.order_id = generate_order_id(request)
            obj.save()
            
            # Phone Pe call
            salt_key = "099eb0cd-02cf-4e2a-8aca-3e6c6aff0399"
            salt_index = "1"
            url = "https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/pay"
            headers = {
                "Content-Type" : "application/json",
            }

            payload = {
                "merchantId": "PGTESTPAYUAT",
                "merchantTransactionId": str(obj.order_id),
                "amount": int(float(obj.price_details['total']) * 100),
                "merchantUserId": str(obj.username),
                "redirectUrl": 'https://www.google.com',
                "redirectMode": "REDIRECT",
                "callbackUrl": 'https://www.google.com',
                "paymentInstrument": {"type": "PAY_PAGE"},
            }

            base64_encoded_payload = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
            hash_obj = sha256((base64_encoded_payload + "/pg/v1/pay" + salt_key).encode())
            final_hash = hash_obj.hexdigest()
            headers["X-VERIFY"] = final_hash + '###' + salt_index

            parameters = {
                "request": base64_encoded_payload,
            }

            response = requests.post(url, headers=headers, json=parameters)
            redirect_url = response.json()['data']['instrumentResponse']['redirectInfo']['url']

            return redirect(redirect_url)


    else:
        profile = UserProfile.objects.get(user=request.user)
        initial_values = {
            'delivery_first_name': request.user.first_name,
            'delivery_last_name': request.user.last_name,
            'delivery_email': request.user.email,
            'delivery_phone_number': profile.phone_number,
        }

        # Get the current Location First
        if get_location(request):
            reverse_geocoding_url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={request.session['latitude']},{request.session['longitude']}&key={settings.GOOGLE_API_KEY}"
            response = requests.get(reverse_geocoding_url).json()
            if response['status'] == 'OK':
                address_components = response['results'][0]['address_components']
                for address_component in address_components:
                    if 'administrative_area_level_1' in address_component['types']:
                        initial_values['delivery_state'] = address_component['long_name']
                    elif 'country' in address_component['types']:
                        initial_values['delivery_country'] = address_component['long_name']
                    elif 'postal_code' in address_component['types']:
                        initial_values['delivery_pin_code'] = address_component['long_name']
                    elif 'locality' in address_component['types']:
                        initial_values['delivery_city'] = address_component['long_name']
                initial_values['delivery_address'] = response['results'][0]['formatted_address']

        # If not get the User's Location from profile
        else:
            initial_values['delivery_address'] = profile.address
            initial_values['delivery_city'] = profile.city
            initial_values['delivery_state'] = profile.state
            initial_values['delivery_country'] = profile.country
            initial_values['delivery_pin_code'] = profile.pin_code

        form = OrderForm(initial=initial_values)
    context['form'] = form
    
    return render(request, 'orders/review_order.html', context)
