from django import forms
from .models import User, UserProfile
from django.core.exceptions import ValidationError


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': '******************',
            'class': 'login-credential',
        }
    ))
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': '******************',
            'class': 'login-credential',
        }
    ))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Your First Name e.g. - John', 'class': 'login-credential',}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Your Last Name e.g. - Doe','class': 'login-credential',}),
            'username': forms.TextInput(attrs={'placeholder': 'An Unique Username e.g. - johndoe@1997','class': 'login-credential',}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Business Email e.g. - johndoe1997@email.com','class': 'login-credential',}),
        }

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError(
                'Password and Confirm Password do not match')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'cover_photo', 'address', 'phone_number',
                  'country', 'state', 'city', 'pin_code', 'latitude', 'longitude']
        labels = {
            'profile_picture': 'Update Profile Picture',
            'cover_photo': 'Update Cover Photo',
            'address': 'Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'state': 'State',
            'city': 'City',
            'pin_code': 'Pin Code',
            'latitude': 'Latitude',
            'longitude': 'Longitude',
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['latitude'].widget.attrs['readonly'] = True
        self.fields['longitude'].widget.attrs['readonly'] = True
