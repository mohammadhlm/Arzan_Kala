from django import forms

# Form Auth
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User


class AdminAuthLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "id": "user-name",
                "placeholder": "نام کاربری",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-password",
                "placeholder": "کلمه عبور",
            }
        )
    )


class ResetPasswordAdmin(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'id': 'email-account',
                'placeholder': 'لطفا ایمیل حساب کاربری خود را وارد نمایید...'
            }
        )
    )


class SetNewAdminPassword(SetPasswordForm):
    new_password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "new-password",
                "placeholder": "لطفا رمز عبور جدید را وارد نمایید...",
            }
        )
    )
    new_password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "confirm-new-password",
                "placeholder": "لطفا رمز عبور جدید را مجدد وارد نمایید...",
            }
        )
    )

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")
        if new_password1 != new_password2:
            raise forms.ValidationError("رمز های عبور همسان نیستند!")
        else:
            return new_password2
