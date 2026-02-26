from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

from app_banner.models import Banner
from app_product.models import Product


@ensure_csrf_cookie
def home_view(request):
    query = (request.GET.get("q") or "").strip()
    category_id = (request.GET.get("category") or "").strip()

    products = Product.objects.filter(is_active=True)

    if query:
        products = products.filter(name__icontains=query)

    if category_id.isdigit():
        products = products.filter(category_id=int(category_id))
    else:
        category_id = ""

    show_home_extras = not query and not category_id

    if show_home_extras:
        bestsellers = products.filter(sold_count__gt=0).order_by("-sold_count")[:10]
        if not bestsellers:
            bestsellers = products.order_by("-created_at")[:10]
        special_offers = products.filter(discount_percent__gte=20)
        banners = Banner.objects.all().order_by("position")
    else:
        bestsellers = Product.objects.none()
        special_offers = Product.objects.none()
        banners = []

    return render(
        request,
        "home.html",
        {
            "banners": banners,
            "products": products,
            "bestsellers": bestsellers,
            "special_offers": special_offers,
            "query": query,
            "selected_category": category_id,
            "show_home_extras": show_home_extras,
        },
    )
