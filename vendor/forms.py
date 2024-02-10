from django import forms
from .models import Vendor, OpeningHours, DAY_CHOICES, get_time_choices
from django.utils.translation import gettext_lazy as _


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license']
        widgets = {
            'vendor_name': forms.TextInput(attrs={'placeholder': 'Name of your Organisation e.g. - Punjabi Dhaba', 'class': 'login-credential',}),
        }


COLUMN_CLASS = 'col-6 col-sm-3'

class OpeningHoursForm(forms.Form):
    day = forms.ChoiceField(label='Day of Week:', widget=forms.Select(attrs={'class': COLUMN_CLASS}), choices=DAY_CHOICES, )
    open= forms.ChoiceField(label='Opening Time:', widget=forms.Select(attrs={'class': COLUMN_CLASS}), choices=get_time_choices(), )
    close= forms.ChoiceField(label='Closing Time:', widget=forms.Select(attrs={'class': COLUMN_CLASS}), choices=get_time_choices(), )
    is_closed = forms.BooleanField(label='Is Holiday:', widget=forms.CheckboxInput(attrs={'class': COLUMN_CLASS, 'style': 'width: 0.8rem;'}), required=False)