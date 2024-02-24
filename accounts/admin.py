from django.contrib import admin
from .models import User, UserProfile
from django.contrib.auth.admin import UserAdmin
from django.contrib.gis import admin
# Register your models here.


class UserManager(UserAdmin):
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    list_display = ('first_name', 'last_name', 'id', 'email',
                    'username', 'role', 'is_active',)
    ordering = ('-date_joined',)
    list_editable = ('is_active',)

class UserProfileAdmin(admin.GISModelAdmin):
    default_zoom = 4
    point_zoom = 12
    list_display = ('user', 'address','state', 'country',  'latitude', 'longitude')


admin.site.register(User, UserManager)
admin.site.register(UserProfile, UserProfileAdmin)
