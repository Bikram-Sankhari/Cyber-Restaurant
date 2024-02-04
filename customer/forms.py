from accounts.models import User
from django import forms

class CustomerUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email']

        widgets = {
            'username': forms.TextInput(attrs={'readonly': True}),
        }