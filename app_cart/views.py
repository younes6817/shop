from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from math import atan2, cos, radians, sin, sqrt
from django.conf import settings
from app_product.models import Product, ProductColor, ProductImage
from app_user.models import User
from .models import Cart, CartItem
from app_address.models import Address
from app_order.models import Order, OrderItem
from django.urls import reverse


def _to_persian_num(num):
    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    return "".join(persian_digits[int(d)] if d.isdigit() else d for d in str(num))

def calculate_shipping_price(total_weight_grams):
    """
    محاسبه قیمت پست بر اساس وزن (به گرم)
    """
    weight_kg = total_weight_grams / 1000
    
    if weight_kg <= 1:
        return 50_000
    elif weight_kg <= 2:
        return 70_000
    elif weight_kg <= 5:
        return 100_000
    elif weight_kg <= 10:
        return 150_000
    elif weight_kg <= 20:
        return 220_000
    else:
        return 300_000

def _haversine_km(lat1, lng1, lat2, lng2):
    earth_radius_km = 6371.0

    d_lat = radians(lat2 - lat1)
    d_lng = radians(lng2 - lng1)
    a = (
        sin(d_lat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lng / 2) ** 2
    )
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return earth_radius_km * c


def _shipping_price_by_distance(distance_km):
    if distance_km <= 5:
        return 40_000  # ۴۰ هزار تومان
    if distance_km <= 15:
        return 70_000  # ۷۰ هزار تومان
    if distance_km <= 30:
        return 100_000  # ۱۰۰ هزار تومان
    return 150_000  # بیش از ۳۰ کیلومتر


def _get_or_create_cart(request):
    if not request.user.is_authenticated:
        guest_cart_id = request.session.get('guest_cart_id')
        if guest_cart_id:
            cart = Cart.objects.filter(id=guest_cart_id, user__isnull=True).first()
            if cart:
                return cart

        cart= Cart.objects.create(user=None, is_active=True)
        request.session['guest_cart_id'] = cart.id
        request.session.modified = True
        return cart
    else:
        cart, _ = Cart.objects.get_or_create(user = request.user, is_active=True)
        return cart

def cart_view(request):
    cart = _get_or_create_cart(request)
    require_login = not request.user.is_authenticated

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

    items_out_of_stock = []
    for item in cart_items:
        if item.selected_color:
            if item.selected_color.stock <= 0:
                items_out_of_stock.append(item.id)
        else:
            if item.product.total_stock <= 0:
                items_out_of_stock.append(item.id)
    has_out_of_stock = len(items_out_of_stock) > 0

    total_items = sum(item.quantity for item in cart_items)
    total_price = sum(item.total_price for item in cart_items)
    total_price_persian = _to_persian_num("{:,}".format(int(total_price)))

    print("Cart items:", [(item.id, item.product.name, item.selected_color.stock if item.selected_color else 'no-color') for item in cart_items])

    return render(
        request,
        "cart_detail.html",
        {
            "cart": cart,
            "cart_items": cart_items,
            "total_items": total_items,
            "total_price": total_price_persian,
            "is_guest_cart": not request.user.is_authenticated,
            "items_out_of_stock": items_out_of_stock,   
            "has_out_of_stock": has_out_of_stock,
            "require_login": require_login,
        },
    )


def checkout_view(request):
    if not request.user.is_authenticated:
        return redirect('user:login')
    
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
    shipping_cost = 50_000
    total_payable = subtotal + shipping_cost
    
    addresses = Address.objects.filter(user=request.user, hidden=False) if request.user.is_authenticated else []
    address_text = ""
    address_hidden = None
    address = None
    selected_address = None
    form_errors = []
    payment_success = False
    distance_km = None
    profile_name = ""
    
    if request.user.is_authenticated:
        profile_name = f"{request.user.first_name or ''} {request.user.last_name or ''}".strip()
    
    need_full_name = True
    
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
        
        # 🔹 Action: ذخیره آدرس جدید
        if request.POST.get("action") == "save_address":
            title = request.POST.get("title", "").strip()
            full_name = request.POST.get("full_name", "").strip()
            province = request.POST.get("province", "").strip()
            city = request.POST.get("city", "").strip()
            minimal_address = request.POST.get("minimal_address", "").strip()
            building_no = request.POST.get("building_no", "").strip()
            postal_code = request.POST.get("postal_code", "").strip()
            phone = request.POST.get("phone", "").strip()
            
            if not province:
                return JsonResponse({"success": False, "error": "استان الزامی است"})
            if not city:
                return JsonResponse({"success": False, "error": "شهر الزامی است"})
            if not minimal_address:
                return JsonResponse({"success": False, "error": "آدرس الزامی است"})
            if not building_no:
                return JsonResponse({"success": False, "error": "پلاک الزامی است"})
            if not postal_code:
                return JsonResponse({"success": False, "error": "کد پستی الزامی است"})
            
            try:
                address = Address.objects.create(
                    user=request.user,
                    title=title,
                    full_name=full_name or "تحویل‌گیرنده",
                    province=province,
                    city=city,
                    minimal_address=minimal_address,
                    building_no=int(building_no),
                    postal_code=postal_code,
                )
                return JsonResponse({"success": True, "address_id": address.id})
            except Exception as e:
                return JsonResponse({"success": False, "error": str(e)})
        
        # 🔹 Action: پردازش پرداخت (ادامه POST عادی)
        selected_address_id = request.POST.get("address_id")
        
        if selected_address_id:
            selected_address = addresses.filter(id=selected_address_id).first()
            if selected_address:
                address_text = f"{selected_address.full_name} - {selected_address.city} - {selected_address.minimal_address}"
        
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
                address_hidden = Address.objects.create(
                    user=request.user,
                    full_name=form_data["full_name"],
                    province=form_data["province"],
                    city=form_data["city"],
                    minimal_address=form_data["minimal_address"],
                    building_no=int(form_data["building_no"]),
                    postal_code=form_data["postal_code"],
                    hidden=True
                )
        
        # تعیین آدرس نهایی
        if selected_address:
            address_final = selected_address
        elif address_hidden:
            address_final = address_hidden
        else:
            address_final = None
        
        if address_final:
            request.session["checkout_address_id"] = address_final.id

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            total_price=total_payable,
            address=address_final,
            status="pending"
        )
        request.session["pending_order_id"] = order.id
    
        MAX_AMOUNT_RIAL = 2_000_000_000
        MAX_AMOUNT_TOMAN = MAX_AMOUNT_RIAL // 10
        
        # 🔹 اگر خطایی نبود، به درگاه پرداخت برو
        if not form_errors and address_final:
            from payments.services import ZarinpalPaymentService
            if total_payable > MAX_AMOUNT_TOMAN:
                form_errors.append("مبلغ سفارش بیش از حد مجاز است")
            else:
                request.session["payment_amount"] = int(total_payable)
                amount_in_rial = int(total_payable) * 10

                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price_at_buy=item.product.price,
                        selected_color=item.selected_color,
                    )
                
                callback_url = request.build_absolute_uri(reverse('payment:verify_payment'))
                service = ZarinpalPaymentService(
                    amount=amount_in_rial,
                    description="خرید از فروشگاه",
                    callback_url=callback_url
                )
                payment = service.request_payment()
                
                if payment:
                    return redirect(payment["url"])
                else:
                    form_errors.append("خطا در اتصال به درگاه پرداخت")
        
        return render(
            request,
            "checkout.html",
            {
                "cart_items": cart_items,
                "addresses": addresses,  # ✅ همیشه QuerySet
                "subtotal": _to_persian_num("{:,}".format(int(subtotal))),
                "shipping_cost": _to_persian_num("{:,}".format(int(shipping_cost))),
                "total_payable": _to_persian_num("{:,}".format(int(total_payable))),
                "distance_km": f"{distance_km:.2f}" if distance_km is not None else "",
                "shop_lat": settings.SHOP_LAT,
                "shop_lng": settings.SHOP_LNG,
                "form_errors": form_errors,
                "selected_address": selected_address,
                "need_full_name": need_full_name,
                "profile_name": profile_name,
                "form_data": form_data,
                "payment_success": payment_success,
                "is_guest_cart": not request.user.is_authenticated,
            },
        )
    
    # ✅ درخواست GET - نمایش اولیه فرم
    return render(
        request,
        "checkout.html",
        {
            "cart_items": cart_items,
            "addresses": addresses,
            "subtotal": _to_persian_num("{:,}".format(int(subtotal))),
            "shipping_cost": _to_persian_num("{:,}".format(int(shipping_cost))),
            "total_payable": _to_persian_num("{:,}".format(int(total_payable))),
            "distance_km": f"{distance_km:.2f}" if distance_km is not None else "",
            "shop_lat": settings.SHOP_LAT,
            "shop_lng": settings.SHOP_LNG,
            "form_errors": form_errors,
            "selected_address": selected_address,
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
        if product.total_stock <= 0:
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
        max_stock = selected_color.stock if selected_color else product.total_stock
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

    max_stock = cart_item.selected_color.stock if cart_item.selected_color else cart_item.product.total_stock
    if new_quantity > max_stock:
        return JsonResponse({"success": False, "message": "موجودی کافی نیست."}, status=400)

    cart_item.quantity = new_quantity
    cart_item.save(update_fields=["quantity"])
    return JsonResponse({"success": True, "new_quantity": new_quantity})
