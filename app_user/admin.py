from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib.admin.sites import NotRegistered

from .models import User

admin.site.site_header = "مدیریت فروشگاه یونس"
admin.site.site_title = "پنل مدیریت فروشگاه یونس"
admin.site.index_title = "مدیریت ساده فروشگاه"

try:
    admin.site.unregister(Group)
except NotRegistered:
    pass

try:
    from admin_interface.models import Theme

    admin.site.unregister(Theme)
except (ImportError, NotRegistered):
    pass


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['phone', 'email', 'role', 'point', 'is_staff']
    list_filter = ['role', 'is_staff', 'is_superuser']
    search_fields = ['phone', 'email']
    
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('اطلاعات شخصی', {'fields': ('email', 'first_name', 'last_name')}),
        ('دسترسی‌ها', {'fields': ('role', 'point', 'is_active', 'is_staff', 'is_superuser')}),
        ('زمان‌های مهم', {'fields': ('last_login',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'email', 'password1', 'password2'),
        }),
    )
    
    ordering = ['phone']
