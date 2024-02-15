from django.contrib import admin
from .models import Cart
# Register your models here.


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'food_item', 'quantity',
                    'delivery_status', 'updated_at')


admin.site.register(Cart, CartAdmin)
