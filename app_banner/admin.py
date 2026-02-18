from django.contrib import admin
from .models import Banner

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'position', 'has_external_link', 'has_product_link']
    list_editable = ['position']
    ordering = ['position']

    fieldsets = (
        ('اطلاعات بنر', {
            'fields': ('title', 'position')
        }),
        ('عکس بنر', {
            'fields': ('image_url', 'image_upload'),
            'description': "⚠️ فقط یکی از این دو گزینه را پر کنید."
        }),
        ('لینک مقصد', {
            'fields': ('link_to', 'product_to'),
            'description': (
                "⚠️ <strong>اگر تبلیغ خارج از سایت است، لینک را در «لینک» قرار دهید.</strong><br>"
                "⚠️ <strong>اگر تبلیغ داخلی است، محصول را در «محصول» انتخاب کنید.</strong>"
            )
        }),
    )

    def has_external_link(self, obj):
        return bool(obj.link_to)
    has_external_link.boolean = True
    has_external_link.short_description = "لینک خارجی"

    def has_product_link(self, obj):
        return bool(obj.product_to)
    has_product_link.boolean = True
    has_product_link.short_description = "لینک به محصول"