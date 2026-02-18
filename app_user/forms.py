from django import forms
from django.core.exceptions import ValidationError
from .models import User

# app_user/forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="رمز عبور")
    password_a = forms.CharField(widget=forms.PasswordInput, label="تکرار رمز عبور")

    class Meta:
        model = User
        fields = ['email', 'password']  # ← username رو حذف کن!

    def clean_password_a(self):
        password = self.cleaned_data.get('password')
        password_a = self.cleaned_data.get('password_a')
        if password and password_a and password != password_a:
            raise ValidationError("رمزهای عبور یکسان نیستند.")
        return password_a

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # ← اینجا هم تغییر کرد
        if commit:
            user.save()
        return user
    
class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")