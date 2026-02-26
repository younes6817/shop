from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import User


def _to_persian_password_errors(messages):
    translated = []
    for message in messages:
        text = str(message)
        lowered = text.lower()

        if "at least" in lowered and "characters" in lowered:
            translated.append("رمز عبور باید حداقل ۸ کاراکتر باشد.")
        elif "too common" in lowered:
            translated.append("این رمز عبور خیلی رایج است.")
        elif "entirely numeric" in lowered:
            translated.append("رمز عبور نمی‌تواند فقط عدد باشد.")
        elif "too similar" in lowered:
            translated.append("رمز عبور با اطلاعات حساب شما شباهت زیادی دارد.")
        else:
            translated.append(text)

    return translated


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="رمز عبور")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="تکرار رمز عبور")

    class Meta:
        model = User
        fields = ["phone", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["phone"].required = False
        self.fields["email"].required = False

        common_class = "w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none"
        for field in self.fields.values():
            field.widget.attrs["class"] = common_class
        self.fields["password"].widget.attrs["class"] = common_class
        self.fields["password_confirm"].widget.attrs["class"] = common_class

        self.fields["phone"].widget.attrs["placeholder"] = "مثال: 09123456789"
        self.fields["email"].widget.attrs["placeholder"] = "example@mail.com"

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not password:
            return password

        candidate_user = User(
            phone=self.cleaned_data.get("phone"),
            email=self.cleaned_data.get("email"),
        )

        try:
            validate_password(password, user=candidate_user)
        except ValidationError as exc:
            raise ValidationError(_to_persian_password_errors(exc.messages))

        return password

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get("phone")
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if not phone and not email:
            raise ValidationError("حداقل یکی از ایمیل یا شماره تلفن را وارد کنید.")

        if phone and User.objects.filter(phone=phone).exists():
            self.add_error("phone", "این شماره تلفن قبلاً ثبت شده است.")

        if email and User.objects.filter(email__iexact=email).exists():
            self.add_error("email", "این ایمیل قبلاً ثبت شده است.")

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
    identifier = forms.CharField(label="موبایل یا ایمیل")
    password = forms.CharField(widget=forms.PasswordInput, label="رمز عبور")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        common_class = "w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none"
        self.fields["identifier"].widget.attrs["class"] = common_class
        self.fields["password"].widget.attrs["class"] = common_class


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        common_class = "w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none"
        for field in self.fields.values():
            field.widget.attrs["class"] = common_class

        self.fields["phone"].required = False
        self.fields["email"].required = False

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get("phone")
        email = cleaned_data.get("email")

        if not phone and not email:
            raise ValidationError("حداقل یکی از ایمیل یا شماره تلفن را وارد کنید.")

        if phone and User.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
            self.add_error("phone", "این شماره تلفن قبلاً ثبت شده است.")

        if email and User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            self.add_error("email", "این ایمیل قبلاً ثبت شده است.")

        return cleaned_data


class SecurityPasswordChangeForm(PasswordChangeForm):
    error_messages = {
        **PasswordChangeForm.error_messages,
        "password_incorrect": "رمز عبور فعلی نادرست است.",
        "password_mismatch": "رمز عبور جدید و تکرار آن یکسان نیست.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].label = "رمز عبور فعلی"
        self.fields["new_password1"].label = "رمز عبور جدید"
        self.fields["new_password2"].label = "تکرار رمز عبور جدید"

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError(self.error_messages["password_mismatch"])

        if password2:
            try:
                validate_password(password2, user=self.user)
            except ValidationError as exc:
                raise ValidationError(_to_persian_password_errors(exc.messages))

        return password2
