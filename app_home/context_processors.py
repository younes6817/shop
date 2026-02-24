from app_category.models import Category
from shop.settings import base as settings


def shop_info(request):
    return {
        "SHOP_NAME": getattr(settings, "SHOP_NAME", "SHOP_NAME"),
        "categories": Category.objects.filter(product__is_active=True).distinct().only("id", "name"),
        "search_query": request.GET.get("q", ""),
    }

