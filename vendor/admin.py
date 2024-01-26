from django.contrib import admin
from .models import Vendor, OpeningHours

# Register your models here.


class VendorAdmin(admin.ModelAdmin):
    list_display = ('vendor_name', 'id', 'user', 'is_approved', 'created_at', 'modified_at')
    list_display_links = ('user', 'vendor_name')
    ordering = ('-created_at',)
    list_editable = ('is_approved',)

class OpeningHoursAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'day', 'open', 'close', 'is_closed')
    list_editable = ('is_closed',)
    list_filter = ('day', 'is_closed')
    list_per_page = 10
    list_max_show_all = 100

admin.site.register(Vendor, VendorAdmin)
admin.site.register(OpeningHours, OpeningHoursAdmin)
