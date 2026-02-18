from shop import settings

def shop_info(request):
    return {
        'SHOP_NAME': getattr(settings, 'SHOP_NAME', 'SHOP_NAME')
    }