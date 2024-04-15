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

        common_attrs = {'class': 'form-control',}

        category_attrs = common_attrs.copy()
        common_attrs['autofocus'] = 'True'
        
        price_attrs = common_attrs.copy()
        price_attrs['style'] = 'width:20vw'

        image_attrs = common_attrs.copy()
        image_attrs['style'] = 'font-size:0.8rem;width:20vw'

        widgets = {
            'category': forms.Select(attrs=category_attrs,),
            'food_title': forms.TextInput(attrs=common_attrs),
            'price': forms.NumberInput(attrs=price_attrs),
            'description': forms.Textarea(attrs=common_attrs),
            'image': forms.FileInput(attrs=image_attrs),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
