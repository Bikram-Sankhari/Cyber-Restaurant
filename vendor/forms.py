from django import forms
from .models import Vendor, OpeningHours
from django.utils.translation import gettext_lazy as _


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license']
        widgets = {
            'vendor_name': forms.TextInput(attrs={'placeholder': 'Name of your Organisation e.g. - Punjabi Dhaba'}),
        }


COLUMN_CLASS = 'col-6 col-sm-3'
class OpeningHoursForm(forms.ModelForm):
    class Meta:
        global column_class
        model = OpeningHours
        fields = ['day', 'open', 'close']
        labels = {
            'day': _('Day:'),
            'open': _('Open:'),
            'close': _('Close:'),
        }
        widgets = {
            'day': forms.Select(attrs={'class': COLUMN_CLASS, 'style': 'font-size: small'}),
            'open': forms.Select(attrs={'class': COLUMN_CLASS, 'style': 'font-size: small'}),
            'close': forms.Select(attrs={'class': COLUMN_CLASS, 'style': 'font-size: small'}),
        }