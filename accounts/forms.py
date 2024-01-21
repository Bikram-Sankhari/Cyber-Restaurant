from django import forms
from .models import User, UserProfile
from django.core.exceptions import ValidationError


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': '******************',
        }
    ))
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': '******************',
        }
    ))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Your First Name e.g. - John'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Your Last Name e.g. - Doe'}),
            'username': forms.TextInput(attrs={'placeholder': 'An Unique Username e.g. - johndoe@1997'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Business Email e.g. - johndoe1997@email.com'}),
        }

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                'Password and Confirm Password do not match')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'cover_photo', 'address',
                   'country', 'state', 'city', 'pin_code', 'latitude', 'longitude']
        
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['latitude'].widget.attrs['readonly'] = True
        self.fields['longitude'].widget.attrs['readonly'] = True
