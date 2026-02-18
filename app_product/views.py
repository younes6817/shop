from django.shortcuts import get_object_or_404, render
from .models import Product

def product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})