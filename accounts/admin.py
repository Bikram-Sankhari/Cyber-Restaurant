from django.contrib import admin
from .models import User, UserProfile
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class UserManager(UserAdmin):
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    list_display = ('first_name', 'last_name', 'email',
                    'username', 'role', 'is_active')
    ordering = ('-date_joined',)


admin.site.register(User, UserManager)
admin.site.register(UserProfile)
