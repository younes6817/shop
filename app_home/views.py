from django.shortcuts import render
from app_product.models import Product
from app_category.models import Category

def home_view(request):
    # همه محصولات فعال
    all_products = Product.objects.filter(is_active=True)

    # بخش‌بندی‌ها
    latest = all_products.order_by('-created_at')[:10]          # جدیدترین‌ها
    bestsellers = all_products.order_by('-sold_count')[:10]     # پرفروش‌ها
    special_offers = all_products.filter(discount_percent__gte=20)  # پیشنهاد ویژه
    all_list = all_products                                     # همه محصولات

    # لیست دسته‌بندی‌ها (برای منوی موبایل)
    categories = Category.objects.all()

    return render(request, 'home.html', {
        'latest': latest,
        'bestsellers': bestsellers,
        'special_offers': special_offers,
        'all_products': all_list,
        'categories': categories,  # ← این خط ضروری بود!
    })