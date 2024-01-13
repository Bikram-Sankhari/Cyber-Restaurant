from django import forms
from .models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_name', 'description',)
        widgets = {
            'category_name': forms.TextInput(attrs={'class': 'form-control mb-3', 'autofocus': 'True'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
