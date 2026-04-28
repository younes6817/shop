from django.contrib.auth.signals import user_logged_in
from .models import Cart, CartItem

def merge_guest_cart(sender, request, user, **kwargs):
    guest_cart_id = request.session.get('guest_cart_id')
    if not guest_cart_id:
        return

    guest_cart = Cart.objects.filter(id=guest_cart_id, user__isnull=True).first()
    if not guest_cart:
        request.session.pop('guest_cart_id', None)
        return

    user_cart, _ = Cart.objects.get_or_create(user=user, is_active=True)

    for item in guest_cart.items.all():
        existing_item = user_cart.items.filter(
            product=item.product,
            selected_color=item.selected_color
        ).first()

        if existing_item:
            max_stock = item.selected_color.stock if item.selected_color else item.product.total_stock
            new_qty = existing_item.quantity + item.quantity
            if new_qty > max_stock:
                new_qty = max_stock
            existing_item.quantity = new_qty
            existing_item.save()
            item.delete()
        else:
            item.cart = user_cart
            item.save()

    guest_cart.delete()
    request.session.pop('guest_cart_id', None)
    request.session.modified = True

user_logged_in.connect(merge_guest_cart)