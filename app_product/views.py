from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import Product


@ensure_csrf_cookie
def product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product_spec = product.specifications.all()

    initial_color = None
    if product.has_colors:
        initial_color = (
            product.colors.filter(is_default=True, stock__gt=0).first()
            or product.colors.filter(stock__gt=0).first()
            or product.colors.filter(is_default=True).first()
            or product.colors.first()
        )

    return render(
        request,
        "product_detail.html",
        {
            "product": product,
            "product_spec": product_spec,
            "initial_color_id": initial_color.id if initial_color else "",
            "initial_color_in_stock": bool(initial_color and initial_color.stock > 0),
        },
    )
