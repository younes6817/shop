from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from app_product.models import Product, ProductColor, ProductImage
from app_user.models import User

from .models import Cart, CartItem


def _to_persian_num(num):
    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    return "".join(persian_digits[int(d)] if d.isdigit() else d for d in str(num))


def _get_or_create_guest_user(request):
    guest_user_id = request.session.get("guest_user_id")
    if guest_user_id:
        guest_user = User.objects.filter(id=guest_user_id).first()
        if guest_user:
            return guest_user

    guest_user = User.objects.create(
        first_name="مهمان",
        role="customer",
        is_active=False,
    )
    guest_user.set_unusable_password()
    guest_user.save(update_fields=["password"])
    request.session["guest_user_id"] = guest_user.id
    request.session.modified = True
    return guest_user


def _get_cart_owner(request):
    if request.user.is_authenticated:
        return request.user
    return _get_or_create_guest_user(request)


def _get_or_create_cart(request):
    owner = _get_cart_owner(request)
    cart, _ = Cart.objects.get_or_create(user=owner, is_active=True)
    return cart


def cart_view(request):
    cart = _get_or_create_cart(request)

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
    total_price_persian = _to_persian_num("{:,}".format(int(total_price)))

    return render(
        request,
        "cart_detail.html",
        {
            "cart": cart,
            "cart_items": cart_items,
            "total_items": total_items,
            "total_price": total_price_persian,
            "is_guest_cart": not request.user.is_authenticated,
        },
    )


def checkout_view(request):
    cart = _get_or_create_cart(request)
    cart_items = list(
        cart.items.select_related("product", "selected_color")
        .prefetch_related(
            Prefetch(
                "product__images",
                queryset=ProductImage.objects.only("id", "product_id", "image"),
            )
        )
        .all()
    )

    if not cart_items:
        return redirect("cart:cart_view")

    subtotal = sum(item.total_price for item in cart_items)
    shipping_cost = 0 if subtotal >= 3_000_000 else 60_000
    total_payable = subtotal + shipping_cost

    addresses = request.session.get("account_addresses", []) if request.user.is_authenticated else []
    address_text = ""
    form_errors = []
    payment_success = False
    selected_address_index = ""

    profile_name = ""
    if request.user.is_authenticated:
        profile_name = f"{request.user.first_name or ''} {request.user.last_name or ''}".strip()
    need_full_name = not profile_name

    form_data = {
        "full_name": "",
        "province": "",
        "city": "",
        "postal_code": "",
        "building_no": "",
        "unit_no": "",
        "minimal_address": "",
        "phone": "",
    }

    if request.method == "POST":
        form_data = {
            "full_name": (request.POST.get("full_name") or "").strip(),
            "province": (request.POST.get("province") or "").strip(),
            "city": (request.POST.get("city") or "").strip(),
            "postal_code": (request.POST.get("postal_code") or "").strip(),
            "building_no": (request.POST.get("building_no") or "").strip(),
            "unit_no": (request.POST.get("unit_no") or "").strip(),
            "minimal_address": (request.POST.get("minimal_address") or "").strip(),
            "phone": (request.POST.get("phone") or "").strip(),
        }
        selected_address_index = (request.POST.get("address_index") or "").strip()

        if selected_address_index.isdigit():
            idx = int(selected_address_index)
            if 0 <= idx < len(addresses):
                address_text = addresses[idx].get("address", "").strip()

        if not address_text:
            final_name = form_data["full_name"] if need_full_name else profile_name

            if need_full_name and not final_name:
                form_errors.append("نام تحویل‌گیرنده الزامی است.")

            if not form_data["province"]:
                form_errors.append("استان الزامی است.")
            if not form_data["city"]:
                form_errors.append("شهر الزامی است.")
            if not form_data["minimal_address"]:
                form_errors.append("آدرس الزامی است.")
            if not form_data["building_no"]:
                form_errors.append("پلاک الزامی است.")

            postal_code = form_data["postal_code"]
            if not postal_code:
                form_errors.append("کد پستی الزامی است.")
            elif not postal_code.isdigit() or len(postal_code) != 10:
                form_errors.append("کد پستی باید ۱۰ رقم باشد.")

            phone = form_data["phone"]
            if not phone:
                form_errors.append("شماره تماس الزامی است.")
            elif not phone.isdigit() or len(phone) != 11 or not phone.startswith("09"):
                form_errors.append("شماره تماس معتبر نیست.")

            if not form_errors:
                address_parts = [
                    f"تحویل‌گیرنده: {final_name}",
                    f"استان: {form_data['province']}",
                    f"شهر: {form_data['city']}",
                    f"آدرس: {form_data['minimal_address']}",
                    f"پلاک: {form_data['building_no']}",
                ]
                if form_data["unit_no"]:
                    address_parts.append(f"واحد: {form_data['unit_no']}")
                address_parts.extend(
                    [
                        f"کدپستی: {form_data['postal_code']}",
                        f"تماس: {form_data['phone']}",
                    ]
                )
                address_text = " | ".join(address_parts)

        if address_text and not form_errors:
            payment_success = True

    return render(
        request,
        "checkout.html",
        {
            "cart_items": cart_items,
            "addresses": addresses,
            "subtotal": _to_persian_num("{:,}".format(int(subtotal))),
            "shipping_cost": _to_persian_num("{:,}".format(int(shipping_cost))),
            "total_payable": _to_persian_num("{:,}".format(int(total_payable))),
            "form_errors": form_errors,
            "selected_address_text": address_text,
            "selected_address_index": selected_address_index,
            "need_full_name": need_full_name,
            "profile_name": profile_name,
            "form_data": form_data,
            "payment_success": payment_success,
            "is_guest_cart": not request.user.is_authenticated,
        },
    )


@require_POST
def add_to_cart(request):
    try:
        product_id = request.POST.get("product_id")
        color_id = request.POST.get("color_id")

        if not product_id:
            return JsonResponse({"success": False, "message": "شناسه محصول نامعتبر است."}, status=400)

        product = get_object_or_404(Product, pk=product_id)
        if product.stock <= 0:
            return JsonResponse({"success": False, "message": "این محصول ناموجود است."}, status=400)

        selected_color = None
        if product.has_colors:
            if color_id:
                selected_color = get_object_or_404(ProductColor, pk=color_id, product=product)
            else:
                selected_color = (
                    product.colors.filter(is_default=True, stock__gt=0).first()
                    or product.colors.filter(stock__gt=0).first()
                )

            if not selected_color:
                return JsonResponse({"success": False, "message": "برای این محصول رنگ موجودی ثبت نشده است."}, status=400)

            if selected_color.stock <= 0:
                return JsonResponse({"success": False, "message": "رنگ انتخاب‌شده ناموجود است."}, status=400)

        cart = _get_or_create_cart(request)

        cart_item = CartItem.objects.filter(
            cart=cart,
            product=product,
            selected_color=selected_color,
        ).first()

        new_quantity = (cart_item.quantity + 1) if cart_item else 1
        max_stock = selected_color.stock if selected_color else product.stock
        if new_quantity > max_stock:
            return JsonResponse({"success": False, "message": "موجودی کافی نیست."}, status=400)

        if cart_item:
            cart_item.quantity = new_quantity
            cart_item.save(update_fields=["quantity"])
            message = "تعداد این کالا در سبد بیشتر شد."
        else:
            cart_item = CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=1,
                selected_color=selected_color,
            )
            message = "محصول به سبد خرید اضافه شد."

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
def remove_from_cart(request, item_id):
    cart = _get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    cart_item.delete()
    return JsonResponse({"success": True, "message": "item removed"})


@require_POST
def update_quantity(request, item_id):
    cart = _get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, pk=item_id, cart=cart)

    try:
        new_quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        return JsonResponse({"success": False, "message": "invalid quantity"}, status=400)

    if new_quantity <= 0:
        cart_item.delete()
        return JsonResponse({"success": True, "action": "deleted"})

    max_stock = cart_item.selected_color.stock if cart_item.selected_color else cart_item.product.stock
    if new_quantity > max_stock:
        return JsonResponse({"success": False, "message": "موجودی کافی نیست."}, status=400)

    cart_item.quantity = new_quantity
    cart_item.save(update_fields=["quantity"])
    return JsonResponse({"success": True, "new_quantity": new_quantity})
