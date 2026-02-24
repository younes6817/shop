from django import forms
from django.core.exceptions import ValidationError

from .models import User


class RegisterForm(forms.ModelForm):
    # فیلد رمز جداست تا تکرار رمز را بررسی کنیم و رمز را هش ذخیره کنیم.
    password = forms.CharField(widget=forms.PasswordInput, label="رمز عبور")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="تکرار رمز عبور")

    class Meta:
        model = User
        # طبق درخواست: نام کاربر نخواهیم. فقط راه ارتباطی + رمز.
        fields = ["phone", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # برای ثبت‌نام، هر دو فیلد ایمیل و موبایل اختیاری‌اند؛
        # اما در clean بررسی می‌کنیم حداقل یکی پر شده باشد.
        self.fields["phone"].required = False
        self.fields["email"].required = False

        common_class = "w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none"
        for field in self.fields.values():
            field.widget.attrs["class"] = common_class
        self.fields["password"].widget.attrs["class"] = common_class
        self.fields["password_confirm"].widget.attrs["class"] = common_class

        self.fields["phone"].widget.attrs["placeholder"] = "مثال: 09123456789"
        self.fields["email"].widget.attrs["placeholder"] = "example@mail.com"

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get("phone")
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        # شرط اصلی: حداقل یکی از ایمیل یا موبایل باید پر شود.
        if not phone and not email:
            raise ValidationError("حداقل یکی از ایمیل یا شماره تلفن را وارد کنید.")

        if password and password_confirm and password != password_confirm:
            raise ValidationError("رمز عبور و تکرار آن یکسان نیست.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    # کاربر می‌تواند با موبایل یا ایمیل وارد شود.
    identifier = forms.CharField(label="موبایل یا ایمیل")
    password = forms.CharField(widget=forms.PasswordInput, label="رمز عبور")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        common_class = "w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none"
        self.fields["identifier"].widget.attrs["class"] = common_class
        self.fields["password"].widget.attrs["class"] = common_class
