from django.shortcuts import render
from app_product.models import Product
from app_category.models import Category
from app_banner.models import Banner

def home_view(request):
    # دریافت پارامترها
    query = request.GET.get('q')
    category_id = request.GET.get('category')

    # پایه: فقط محصولات فعال
    products = Product.objects.filter(is_active=True)

    # فیلتر بر اساس جستجو
    if query:
        products = products.filter(name__icontains=query)

    # فیلتر بر اساس دسته‌بندی
    if category_id:
        products = products.filter(category_id=category_id)

    # پرفروش‌ها (فقط اگر فیلتر نشده باشن)
    if not query and not category_id:
        bestsellers = products.filter(sold_count__gt=0).order_by('-sold_count')[:10]
        if not bestsellers:
            bestsellers = products.order_by('-created_at')[:10]
        
        # پیشنهاد ویژه (تخفیف ≥ 20%)
        special_offers = products.filter(discount_percent__gte=20)
    else:
        bestsellers = []
        special_offers = []

    categories = Category.objects.all()
    banners = Banner.objects.all().order_by('position')

    return render(request, 'home.html', {
        'banners': banners,
        'products': products,
        'bestsellers': bestsellers,
        'special_offers': special_offers,  # ← این خط اضافه شد
        'categories': categories,
        'query': query,
        'selected_category': category_id,
    })