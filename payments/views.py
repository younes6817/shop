from django.shortcuts import get_object_or_404, redirect, render
from app_cart.views import _get_or_create_cart
from app_product.models import Product
from .services import ZarinpalPaymentService
from app_order.models import *
from app_address.models import Address
from app_cart.views import checkout_view
from django.urls import reverse

def start_payment(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    address = Address.objects.get(
        id=request.session.get("checkout_address_id"),
        user=request.user
    )
    
    amount_rial = product.price * 10

    callback_url = request.build_absolute_uri(reverse('payment:verify_payment'))
    service = ZarinpalPaymentService(
        amount=amount_rial,
        description=f"خرید {product.name}",
        callback_url=callback_url
    )

    print("Callback URL:", callback_url)
    payment = service.request_payment()
    
    if payment:
        return redirect(payment["url"])
    
    return redirect("home")

def verify_payment(request):
    authority = request.GET.get("Authority")
    status = request.GET.get("Status")
    order_id = request.session.get("pending_order_id")
    order = Order.objects.filter(id=order_id, user=request.user).first()
    
    if not order:
        return render(request, "error.html", {"message": "سفارش یافت نشد"})
    
    if status == "OK" and authority:
        amount = request.session.get("payment_amount", 0)

        if amount == 0:
            order.status = "error_pay"
            order.save()
            return render(request, "error.html", {
                "message": "مبلغ پرداخت یافت نشد"
            })
        
        amount_rial = amount * 10
        
        service = ZarinpalPaymentService(
            amount=amount_rial,
            description="",
            callback_url=""
        )
        
        result = service.verify_payment(authority)

        print(f"Verify result: {result}")
        
        if result["success"]:
            request.session.pop("payment_amount", None)
            request.session.pop("address_text", None)

            cart = _get_or_create_cart(request)
            cart.items.all().delete()

            order.status = "paid"
            order.save()

            for item in order.orderitem_set.all():
                if item.selected_color:
                    product = item.product
                    color = item.selected_color
                    product.sold_count += item.quantity
                    color.stock -= item.quantity
                    if color.stock < 0:
                        color.stock = 0
                    product.save()
                    color.save()

            return render(request, "success.html", {
                "ref_id": result["ref_id"]
            })
    
    order.status = "error_pay"
    return render(request, "error.html", {
        "message": "پرداخت ناموفق"
    })
