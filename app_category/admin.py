from django.contrib import admin
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']  # ستون‌های نمایشی در لیست
    search_fields = ['name']       # امکان جستجو بر اساس نام
    ordering = ['name']            # مرتب‌سازی بر اساس نام
