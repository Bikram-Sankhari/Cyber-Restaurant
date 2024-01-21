from django.contrib import admin

from menu.models import Category, FoodItem

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name','id', 'vendor', 'updated_at')
    search_fields = ('category_name', 'vendor__vendor_name')

class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('food_title', 'id', 'category', 'vendor', 'price', 'is_available', 'updated_at')
    list_filter = ('is_available',)
    search_fields = ('food_title', 'category__category_name', 'vendor__vendor_name', 'price')
    prepopulated_fields = {'slug': ('food_title',)}
    list_editable = ('price', 'is_available')
    list_per_page = 10

# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(FoodItem, FoodItemAdmin)