from django.contrib import admin
from .models import *

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ('image',)  # alt_text پنهان است

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'discount_percent', 'stock', 'is_active']
    list_filter = ['is_active', 'category']
    search_fields = ['name']
    list_editable = ['price', 'stock', 'is_active']
    exclude = ('sold_count',)
    inlines = [ProductImageInline]  # ← این خط ضروری بود!

@admin.register(ProductSpec)
class ProductSpecAdmin(admin.ModelAdmin):
    list_display = ['product', 'key', 'value']
    search_fields = ['product__name', 'key', 'value']