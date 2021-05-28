from django import forms
from Apps.Usrs_Apps__Ak.Ak_User_Account.models import Contact
from Apps.Product_Apps__Ak.models import Comment, Rating


class Contact_Form(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"
        widgets = {
            'user': forms.TextInput(attrs={
                "class": "d-none"
            }),
            'subject': forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "موضوع را وارد کنید *",
            }),
            "msg": forms.Textarea(attrs={
                "rows": 4,
                "class": "form-control",
                'placeholder': "پیام *",
                'style': "resize:none"
            })

        }


class form_advanced_filter_shop(forms.Form):
    ORDER_CHOICES = [
        ("de", "مرتب سازی پیش فرض"),
        ("popularity", "مرتب سازی بر اساس محبوبیت"),
        ("date", "مرتب سازی بر اساس جدید"),
        ("price", "مرتب سازی بر اساس قیمت: پایین تا بالا"),
        ("price-desc", "مرتب سازی بر اساس قیمت: بالا تا پایین"),
    ]
    order = forms.ChoiceField(choices=ORDER_CHOICES, widget=forms.Select(attrs={
        "class": "form-control form-control-sm"
    }))
    category_id = forms.CharField(widget=forms.NumberInput(attrs={
        "class": "d-none"
    }))
    brand_id = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class": "d-none"
    }))
    price_filter = forms.CharField(widget=forms.TextInput(attrs={
        "class": "d-none"
    }))


class Comment_Form(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("user", "product", "body",)
        widgets = {
            "body": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "پیام شما*"
            }),
            "user": forms.EmailInput(attrs={
                "class": "d-none"
            }),
            "product": forms.NumberInput(attrs={
                "class": "d-none"
            })
        }


class Rating_Form(forms.ModelForm):
    class Meta:
        model = Rating
        fields = (
            "product",
            "user",
            "star",
        )
        widgets = {
            "product": forms.Select(attrs={
                "class": "d-none",
            }),
            "user": forms.NumberInput(attrs={
                "class": "d-none",
            }),
            "star": forms.NumberInput(attrs={
                "class": "d-none",
            })
        }


class Product_Add_To_Cart(forms.Form):
    product_id = forms.IntegerField()


class Completion_User_Information(forms.Form):
    first_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "نام*"
    }))

    last_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "نام خانوادگی*"
    }))

    postal_code = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'class': "form-control",
        "placeholder": "کدپستی*"
    }))

    location_first = forms.CharField(max_length=250, widget=forms.TextInput(attrs={
        'class': "form-control",
        "placeholder": "آدرس شما*"
    }))
    phone_number = forms.CharField(max_length=11, widget=forms.TextInput(attrs={
        'class': 'form-control',
        "placeholder": "تلفن همراه*"
    }))
    select_city = forms.CharField(widget=forms.Select(attrs={
        "class": "form-control js-data-city-to-ajax"
    }))

    def clean_phone_number(self):
        if re.search('(^0?[\d]{10}$)', str(self.cleaned_data.get("phone_number")).strip()) is None:
            raise forms.ValidationError('فرمت شماره تلفن صحیح نمیباشد شماره تلفن شامل 11 رقم و میتواند شامل 0 نباشد')
        else:
            return self.cleaned_data.get("phone_number")

    def clean_postal_code(self):
        if re.search("(^[\d]{5}[\-]?[\d]{5}$)", str(self.cleaned_data.get("postal_code"))) is None:
            raise forms.ValidationError('فرمت کد پستی صحیح نمیباشد لطفا از راهنمای این فیلد کمک بگیرید')
        else:
            return self.cleaned_data.get("postal_code")
