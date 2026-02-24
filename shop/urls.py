from . import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('app_user.urls')),
    path('', include('app_home.urls')),
    path('cart/', include('app_cart.urls')),
    path('product/', include('app_product.urls'))
]


if settings.base.DEBUG:
    urlpatterns += static(settings.base.MEDIA_URL, document_root=settings.base.MEDIA_ROOT)


