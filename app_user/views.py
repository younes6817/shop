from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import LoginForm, RegisterForm
from .models import User


def register_view(request):
    if request.user.is_authenticated:
        return redirect("user:profile")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user:login")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("user:profile")

    error_message = None

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data["identifier"].strip()
            password = form.cleaned_data["password"]

            if "@" in identifier:
                user = User.objects.filter(email__iexact=identifier).first()
            else:
                user = User.objects.filter(phone=identifier).first()

            if user and user.check_password(password) and user.is_active:
                login(request, user)
                next_url = request.POST.get("next") or request.GET.get("next")
                return redirect(next_url or "user:profile")

            error_message = "اطلاعات ورود نامعتبر است."
    else:
        form = LoginForm()

    return render(
        request,
        "login.html",
        {
            "form": form,
            "error_message": error_message,
            "next": request.GET.get("next", ""),
        },
    )


def main_view(request):
    profile_options = [
        {"title": "تنظیمات حساب", "subtitle": "ویرایش اطلاعات شخصی", "href": "#"},
        {"title": "سفارش‌ها", "subtitle": "مشاهده تاریخچه خرید", "href": "#"},
        {"title": "آدرس‌ها", "subtitle": "مدیریت آدرس‌های ارسال", "href": "#"},
        {"title": "امنیت", "subtitle": "رمز عبور و امنیت حساب", "href": "#"},
    ]
    return render(request, "main.html", {"profile_options": profile_options})


@require_POST
def logout_view(request):
    logout(request)
    return redirect("home:home")


@require_POST
@login_required
def delete_account_view(request):
    user_to_delete = request.user
    logout(request)
    user_to_delete.delete()
    return redirect("home:home")

