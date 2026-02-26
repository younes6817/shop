from django.conf import settings

from app_category.models import Category


def shop_info(request):
    return {
        "SHOP_NAME": getattr(settings, "SHOP_NAME", "SHOP_NAME"),
        "categories": Category.objects.filter(product__is_active=True).distinct().only("id", "name"),
        "search_query": request.GET.get("q", ""),
        "APP_VERSION": getattr(settings, "APP_VERSION", "normal"),
        "PREMIUM_FEATURES": getattr(settings, "PREMIUM_FEATURES", False),
        "SUPER_FEATURES": getattr(settings, "SUPER_FEATURES", False),
    }
