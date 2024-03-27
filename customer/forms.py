from accounts.models import User
from django import forms
from django.core.exceptions import ValidationError


class CustomerUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email']

        widgets = {
            'username': forms.TextInput(attrs={'readonly': True}),
        }

class ChangePasswordForm(forms.Form):
    input_field_attrs = {'class': "form-control form-control-sm change-password-input ps-2 pe-0", 'style': "border: solid 1px #c33332;",}

    old_password = forms.CharField(label='Current Password :', widget=forms.PasswordInput(attrs=input_field_attrs))
    new_password = forms.CharField(label='New Password :', widget=forms.PasswordInput(attrs=input_field_attrs))
    confirm_password = forms.CharField(label='Confirm New Password :', widget=forms.PasswordInput(attrs=input_field_attrs))

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password != confirm_password:
            raise ValidationError(
                '* Password and Confirm Password do not match')