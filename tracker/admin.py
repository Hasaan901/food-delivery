from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Order, Restaurant, FoodItem

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'phone', 'role', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone', 'role')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Order)
admin.site.register(Restaurant)
admin.site.register(FoodItem)
