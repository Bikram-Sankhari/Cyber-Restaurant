from django import forms
from .models import Category, FoodItem
from django.utils.translation import gettext_lazy as _


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_name', 'description',)
        widgets = {
            'category_name': forms.TextInput(attrs={'class': 'form-control mb-3', 'autofocus': 'True'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ('category', 'food_title', 'price', 'image', 'is_available', 'description',)
        labels={
            "category": _("Category *"),
            "food_title": _("Food Title *"),
            "price": _("Price *"),
            "description": _("Description"),
            "image": _("Image"),
            "is_available": _("Is Available"),
        }

        widgets = {
            'category': forms.Select(attrs={'class': 'form-control mb-3'},),
            'food_title': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'price': forms.NumberInput(attrs={'class': 'form-control mb-3', 'style': 'width:20vw'}),
            'description': forms.Textarea(attrs={'class': 'form-control mb-3'}),
            'image': forms.FileInput(attrs={'class': 'form-control mb-3', 'style': 'font-size:0.8rem;width:20vw'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input mb-3'}),
        }
        
