from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from app_product.models import Product, ProductColor, ProductImage

from .models import Cart, CartItem


@login_required
def cart_view(request):
    cart = Cart.objects.filter(user=request.user, is_active=True).first()
    if not cart:
        cart = Cart.objects.create(user=request.user)

    cart_items = (
        cart.items.select_related("product", "selected_color")
        .prefetch_related(
            Prefetch(
                "product__images",
                queryset=ProductImage.objects.only("id", "product_id", "image"),
            )
        )
        .all()
    )
    total_items = sum(item.quantity for item in cart_items)
    total_price = sum(item.total_price for item in cart_items)

    def to_persian_num(num):
        persian_digits = "۰۱۲۳۴۵۶۷۸۹"
        return "".join(persian_digits[int(d)] if d.isdigit() else d for d in str(num))

    total_price_persian = to_persian_num("{:,}".format(int(total_price)))

    return render(
        request,
        "cart_detail.html",
        {
            "cart": cart,
            "cart_items": cart_items,
            "total_items": total_items,
            "total_price": total_price_persian,
        },
    )


@require_POST
@login_required
def add_to_cart(request):
    try:
        product_id = request.POST.get("product_id")
        color_id = request.POST.get("color_id")

        if not product_id:
            return JsonResponse({"success": False, "message": "invalid product"}, status=400)

        product = get_object_or_404(Product, pk=product_id)

        selected_color = None
        if color_id:
            selected_color = get_object_or_404(ProductColor, pk=color_id, product=product)
        else:
            # If product has color variants but no color was sent, use default/first color.
            selected_color = (
                product.colors.filter(is_default=True).first()
                or product.colors.first()
            )

        cart, _ = Cart.objects.get_or_create(user=request.user, is_active=True)

        cart_item = CartItem.objects.filter(
            cart=cart,
            product=product,
            selected_color=selected_color,
        ).first()

        if cart_item:
            cart_item.quantity += 1
            cart_item.save()
            message = "cart item quantity increased"
        else:
            cart_item = CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=1,
                selected_color=selected_color,
            )
            message = "product added to cart"

        return JsonResponse(
            {
                "success": True,
                "message": message,
                "item_id": cart_item.id,
                "quantity": cart_item.quantity,
            }
        )
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@require_POST
@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    cart_item.delete()
    return JsonResponse({"success": True, "message": "item removed"})


@require_POST
@login_required
def update_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    try:
        new_quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        return JsonResponse({"success": False, "message": "invalid quantity"}, status=400)

    if new_quantity <= 0:
        cart_item.delete()
        return JsonResponse({"success": True, "action": "deleted"})

    cart_item.quantity = new_quantity
    cart_item.save()
    return JsonResponse({"success": True, "new_quantity": new_quantity})
