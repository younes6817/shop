# your_app/admin.py (یا همون فایل بالا)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # فیلدهایی که در لیست کاربران نمایش داده می‌شن
    list_display = ['phone', 'email', 'role', 'point', 'is_staff']
    list_filter = ['role', 'is_staff', 'is_superuser']
    search_fields = ['phone', 'email']
    
    # فیلدهایی که در فرم ویرایش نمایش داده می‌شن
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('اطلاعات شخصی', {'fields': ('email', 'first_name', 'last_name')}),
        ('دسترسی‌ها', {'fields': ('role', 'point', 'is_active', 'is_staff', 'is_superuser')}),
    )
    
    # فیلدهایی که هنگام ساخت کاربر نمایش داده می‌شن
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'email', 'password1', 'password2'),
        }),
    )
    
    ordering = ['phone']