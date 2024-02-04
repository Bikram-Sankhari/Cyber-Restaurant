from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_first_name', 'delivery_last_name', 'delivery_email', 'delivery_phone_number', 'delivery_address',
                  'delivery_country', 'delivery_state', 'delivery_city', 'delivery_pin_code',
                  ]
        labels = {
            'delivery_first_name': 'First Name',
            'delivery_last_name': 'Last Name',
            'delivery_email': 'Email',
            'delivery_phone_number': 'Phone Number',
            'delivery_address': 'Address',
            'delivery_country': 'Country',
            'delivery_state': 'State',
            'delivery_city': 'City',
            'delivery_pin_code': 'Pin Code',
        }

        widgets = {
            'delivery_first_name': forms.TextInput(attrs={'id': 'id_first_name', 'class': 'mb-3'}),
            'delivery_last_name': forms.TextInput(attrs={'id': 'id_last_name', 'class': 'mb-3'}),
            'delivery_email': forms.TextInput(attrs={'id': 'id_email', 'class': 'mb-3'}),
            'delivery_phone_number': forms.TextInput(attrs={'id': 'id_phone_number', 'class': 'mb-3'}),
            'delivery_address': forms.TextInput(attrs={'id': 'id_address', 'class': 'mb-3'}),
            'delivery_country': forms.TextInput(attrs={'id': 'id_country', 'class': 'mb-3'}),
            'delivery_state': forms.TextInput(attrs={'id': 'id_state', 'class': 'mb-3'}),
            'delivery_city': forms.TextInput(attrs={'id': 'id_city', 'class': 'mb-3'}),
            'delivery_pin_code': forms.TextInput(attrs={'id': 'id_pin_code', 'class': 'mb-3'}),
        }
