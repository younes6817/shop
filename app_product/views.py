from django.shortcuts import get_object_or_404, render
from .models import Product, ProductSpec

def product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product_spec = product.specifications.all()
    return render(request, 'product_detail.html', {
        'product': product,
        'product_spec': product_spec
    })