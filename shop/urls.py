from . import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('account/', include('app_user.urls')),
    path('', include('app_home.urls')),
    path('cart/', include('app_cart.urls')),
    path('product/', include('app_product.urls')),
    path('payment/', include('payments.urls')),
    path('orders/', include('app_order.urls')),
    path('address/', include('app_address.urls')),
    path('panel/', include('dashboard.urls')),
]


if settings.base.DEBUG:
    urlpatterns += static(settings.base.MEDIA_URL, document_root=settings.base.MEDIA_ROOT)


