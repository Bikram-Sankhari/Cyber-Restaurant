from django.contrib import admin
from .models import Order

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'status', 'updated_at')

admin.site.register(Order, OrderAdmin)
