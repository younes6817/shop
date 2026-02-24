from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['phone', 'email', 'role', 'point', 'is_staff']
    list_filter = ['role', 'is_staff', 'is_superuser']
    search_fields = ['phone', 'email']
    
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('اطلاعات شخصی', {'fields': ('email', 'first_name', 'last_name')}),
        ('دسترسی‌ها', {'fields': ('role', 'point', 'is_active', 'is_staff', 'is_superuser')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'email', 'password1', 'password2'),
        }),
    )
    
    ordering = ['phone']
