from django import forms
from django.contrib.auth import get_user_model
# Import Validation
from .models import Contact
from .Validation_User_Input.FormValidation import EmailValidation, FullnameValidation, PasswordValidation


# Register Forms
class RegisterForm(forms.Form):
    full_name = forms.CharField(
        min_length=6,
        max_length=40,
        error_messages={
            'required': 'لطفا نام و نام خانوادگی خود را وارد نمایید(این فیلد الزامی است.)',
            'invalid': 'مقادیر وارد شده اشتباه است (نام خانوادگی باید شامل حروف باشد.)',
            'min_length': 'نام و نام خانوادگی شما باید خداقل ۶ حرف باشد.',
            'max_length': 'نام و نام خانوادگی شما نمی تواند بیشتر از ۴۰ حرف باشد.'
        },
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": 'نام و نام خانوادگی خود را وارد کنید',
                "type": "text",
            }
        ),
    )
    email = forms.EmailField(
        min_length=12,
        max_length=80,
        error_messages={
            'required': 'لطفا ایمیل خود را وارد نمایید(این فیلد الزامی است.)',
            'invalid': 'ایمیل وارد شده اشتباه است (ایمیل فقط شامل حروف و اعداد انگلیسی میتواند باشد.)',
            'min_length': 'ایمیل شما باید خداقل ۱۲ حرف باشد.',
            'max_length': 'ایمیل شما نمی تواند بیشتر از ۸۰ حرف باشد.'
        },
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": 'ایمیل خود را وارد کنید',
                "type": "email",
            }
        ),
    )
    password = forms.CharField(
        min_length=8,
        max_length=40,
        error_messages={
            'required': 'لطفا پسورد خود را وارد نمایید(این فیلد الزامی است.)',
            'invalid': 'پسورد وارد شده اشتباه است (پسورد فقط شامل حروف و اعداد انگلیسی میتواند باشد.)',
            'min_length': 'پسورد شما باید خداقل ۸ حرف باشد.',
            'max_length': 'پسورد شما نمی تواند بیشتر از ۴۰ حرف باشد.'
        },
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": 'کلمه عبور',
                "type": "password",
            }
        ),
    )
    confirm_password = forms.CharField(
        error_messages={
            'required': 'لطفا پسورد خود را مجدد وارد نمایید(این فیلد الزامی است.)',
            'invalid': 'پسورد وارد شده اشتباه است (پسورد فقط شامل حروف و اعداد انگلیسی میتواند باشد.)',
        },
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": 'کلمه عبور',
                "type": "password",
            }
        ),
    )
    checkbox_rules = forms.BooleanField(
        error_messages={
            'required': 'لطفا قوانین و مقررات را تایید کنید(در غیر این صورت نمیتوانید ثبت نام کنید)',
        },
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
                "id": "exampleCheckbox2",
            }
        ),
        required=True
    )

    def clean_full_name(self):
        if FullnameValidation(self.cleaned_data.get("full_name")) is False:
            raise forms.ValidationError("نام و نام خانوادگی شما نمیتواند شامل اعداد و کارکتر های اجمالی باشد!")
        else:
            return self.cleaned_data.get("full_name")

    def clean_email(self):
        User = get_user_model()
        if User.objects.filter(username=self.cleaned_data.get("email")).exists():
            raise forms.ValidationError(
                "کاربری با این مشخصات داخل سایت وجود دارد اگر این حساب کاربری متعلق به شماست از طریق دکمه ورود اقدام کنید.")
        elif EmailValidation(self.cleaned_data.get("email")) is False:
            raise forms.ValidationError(
                "فرمت ایمیل وارد شده جزو ایمیل های استاندارد نیست(لطفا از ایمیل دیگری استفاده نمایید)")
        else:
            return self.cleaned_data.get("email")

    def clean_password(self):
        if PasswordValidation(self.cleaned_data.get("password")) is False:
            raise forms.ValidationError(
                "رمز عبور شما دارای ایمنی پایینی است لطفا رمز عبور قوی تری وارد نمایید(رمز عبور باید شامل اعداد و حروف باشد)")
        else:
            return self.cleaned_data.get("password")

    def clean_confirm_password(self):
        if self.cleaned_data.get("password") != self.cleaned_data.get("confirm_password"):
            raise forms.ValidationError("پسورد های شما همسان نیستند!(لطفا با دقت وارد نمایید)")
        else:
            return self.cleaned_data.get("confirm_password")


# Login Form
class LoginForm(forms.Form):
    email = forms.EmailField(
        error_messages={
            'required': 'لطفا ایمیل خود را وارد نمایید(این فیلد الزامی است.)',
            'invalid': 'ایمیل وارد شده اشتباه است (ایمیل فقط شامل حروف و اعداد انگلیسی میتواند باشد.)',
        },
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": 'ایمیل خود را وارد کنید',
                "type": "email",
            }
        ),
    )
    password = forms.CharField(
        error_messages={
            'required': 'لطفا کلمه عبور خود را وارد نمایید(این فیلد الزامی است.)',
            'invalid': 'کلمه عبور وارد شده اشتباه است (کلمه عبور فقط شامل حروف و اعداد انگلیسی میتواند باشد.)',
        },
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": 'کلمه عبور',
                "type": "password",
            }
        ),
    )

    def clean_email(self):
        User = get_user_model()
        if not User.objects.filter(username=self.cleaned_data.get("email")).exists():
            raise forms.ValidationError("کاربری با این مشخصات یافت نشد")
        else:
            return self.cleaned_data.get("email")
