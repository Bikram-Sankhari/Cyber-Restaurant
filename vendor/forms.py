from django import forms
from .models import Vendor

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license']
        widgets = {
            'vendor_name': forms.TextInput(attrs={'placeholder': 'Name of your Organisation e.g. - Punjabi Dhaba'}),
        }