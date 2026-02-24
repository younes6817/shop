from app_category.models import Category
from shop.settings import base as settings


def shop_info(request):
    # داده‌های مشترک برای تمام صفحات (چون base.html در همه جا استفاده می‌شود)
    return {
        "SHOP_NAME": getattr(settings, "SHOP_NAME", "SHOP_NAME"),
        # فقط دسته‌هایی نمایش داده شوند که محصول فعال دارند.
        "categories": Category.objects.filter(product__is_active=True).distinct().only("id", "name"),
        "search_query": request.GET.get("q", ""),
    }
