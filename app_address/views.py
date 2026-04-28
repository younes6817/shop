from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import *

@login_required
def addresses_view(request):
    addresses = Address.objects.filter(user=request.user, hidden="False")

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "add":
            title = (request.POST.get("title") or "").strip()
            full_name = (request.POST.get("full_name") or "").strip()
            province = (request.POST.get("province") or "").strip()
            city = (request.POST.get("city") or "").strip()
            minimal_address = (request.POST.get("minimal_address") or "").strip()
            building_no = (request.POST.get("building_no") or "").strip()
            postal_code = (request.POST.get("postal_code") or "").strip()
            if title and full_name and province and city and minimal_address and building_no and postal_code:
                Address.objects.create(
                    user=request.user,
                    title=title,
                    full_name=full_name,
                    province=province,
                    city=city,
                    minimal_address=minimal_address,
                    building_no=building_no,
                    postal_code=postal_code
                )
                request.session.modified = True
                messages.success(request, "آدرس جدید ذخیره شد.")
            else:
                messages.error(request, "کل لیست الزامی است")

        if action == "delete":
            address_id = request.POST.get("address_id")
            if address_id:
                address = get_object_or_404(Address, id=address_id, user=request.user)
                address.delete()
                messages.success(request, "آدرس حذف شد.")

        return redirect("address:address")

    return render(request, "addresses.html", {"addresses": addresses})
