# app_product/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Product, ProductSpec, ProductImage, ProductColor

class ProductColorInline(admin.TabularInline):
    model = ProductColor
    extra = 1
    fields = ('color', 'color_name', 'stock', 'is_default')
    show_change_link = True

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductSpecInline(admin.TabularInline):
    model = ProductSpec
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount_percent', 'stock', 'colors_count', 'is_active')
    list_filter = ('is_active', 'category', 'discount_percent')
    search_fields = ('name', 'description')
    inlines = [ProductColorInline, ProductImageInline, ProductSpecInline]
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('name', 'description', 'category', 'is_active')
        }),
        ('قیمت و موجودی', {
            'fields': ('price', 'discount_percent', 'stock')
        }),
    )
    
    def colors_count(self, obj):
        """تعداد رنگ‌های محصول"""
        return obj.colors.count()
    colors_count.short_description = 'تعداد رنگ'

@admin.register(ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    list_display = ('product', 'color_name', 'color_preview', 'stock', 'is_default')
    list_filter = ('product', 'is_default')
    
    def color_preview(self, obj):
        if obj.color:
            return format_html(
                '<span style="display:inline-block;width:20px;height:20px;background:{};border-radius:50%;border:1px solid #ddd;"></span>',
                obj.color
            )
        return '-'
    color_preview.short_description = 'رنگ'