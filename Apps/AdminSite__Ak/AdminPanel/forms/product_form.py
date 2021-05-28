from django import forms
from Apps.Product_Apps__Ak.models import Post_Products, Product_Tags, Category_Product, Brand_Model, Home_Slider
from ckeditor.widgets import CKEditorWidget

from ckeditor.fields import RichTextField


class product_creation_form(forms.ModelForm):
    class Meta:
        model = Post_Products
        fields = (
            "photo", "name", "status", "slug", "tag", "category", "short_description", "further_details",
            "discounted_price",
            "final_price", "inventory", "sold", "publication_date", "attributes")
        widgets = {
            'photo': forms.FileInput(attrs={
                'style': 'display:none !important'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': "custom-select",
                'id': "customSelect"
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'tag': forms.SelectMultiple(attrs={
                'class': "d-none",
            }),
            'category': forms.SelectMultiple(attrs={
                'class': 'select2 form-control',
                'multiple': 'multiple',
            }),
            'short_description': CKEditorWidget(),
            'further_details': CKEditorWidget(attrs={
            }),
            'discounted_price': forms.TextInput(attrs={
                'class': 'touchspin',
                'data-bts-step': '0.5',
                'data-bts-decimals': '3',
            }),
            'final_price': forms.TextInput(attrs={
                'class': 'touchspin',
                'data-bts-step': '0.5',
                'data-bts-decimals': '3',

            }),
            'inventory': forms.TextInput(attrs={
                'class': 'touchspin',
                'data-bts-step': '5',
            }),
            'sold': forms.TextInput(attrs={
                'class': 'touchspin',
            }),
            'publication_date': forms.TextInput(attrs={
                'class': 'd-none'
            })
        }
        error_messages = {
            'photo': {
                'required': "وارد کردن عکس محصول اجباری است",
            },
            'name': {
                'required': "وارد کردن نام محصول اجباری است",
            },
            'status': {
                'required': "وارد کردن وضعیت محصول اجباری است",
            },
            'tag': {
                'invalid': 'لطفا برچسبی برای محصول انتخاب نمایید',
            },
            'category': {
                'invalid': "وارد کردن دسته بندی محصول اجباری است",
            },
            'short_description': {
                'required': "وارد کردن توضیحات کوتاه محصول اجباری است",
            },
            'further_details': {
                'required': "وارد کردن توضیحات کامل محصول اجباری است",
            },
            'final_price': {
                'required': "وارد کردن قیمت محصول اجباری است",
            },
            'inventory': {
                'required': "وارد کردن تعداد محصول اجباری است",
            },
            'publication_date': {
                'required': "وارد کردن زمان انتشار محصول اجباری است",
            },
        }


class tag_creation_form(forms.ModelForm):
    class Meta:
        model = Product_Tags
        fields = '__all__'
        widgets = {'tag_name': forms.TextInput(attrs={
            'class': 'form-control',
            'data-validation-regex-regex': '^[-a-zA-Z_\d\u0621-\u0628\u062A-\u063A\u0641-\u0642\u0644-\u0648\u064E-\u0651\u0655\u067E\u0686\u0698\u06A9\u06AF\u06BE\u06CC]+$',
            'data-validation-regex-message': 'نویسه ها باید شامل حروف الفبا یا اعداد و زیر خط,خط تیره باشند.',
            'placeholder': 'لطفا نام برچسب را وارد نمایید',
            'aria-invalid': 'false'
        })}


class category_creation_form(forms.ModelForm):
    class Meta:
        model = Category_Product
        fields = '__all__'
        widgets = {
            'category_photo': forms.FileInput(attrs={
                'style': 'display:none !important'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'لطفا آدرس اینترنتی دسته بندی را وارد کنید',
            }),
            'category_name': forms.TextInput(attrs={
                'class': 'form-control',
                'data-validation-regex-regex': '^[-a-zA-Z_\d\u0621-\u0628\u062A-\u063A\u0641-\u0642\u0644-\u0648\u064E-\u0651\u0655\u067E\u0686\u0698\u06A9\u06AF\u06BE\u06CC]+$',
                'data-validation-regex-message': 'نویسه ها باید شامل حروف الفبا یا اعداد و زیر خط,خط تیره باشند.',
                'placeholder': 'لطفا نام دسته بندی را وارد نمایید',
                'aria-invalid': 'false'
            })
        }


class brand_creation_form(forms.ModelForm):
    class Meta:
        model = Brand_Model
        fields = "__all__"
        widgets = {
            'photo': forms.FileInput(attrs={
                'style': 'display:none !important'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'لطفا نام برند را وارد کنید',
            }),
        }


class slider_creation_form(forms.ModelForm):
    class Meta:
        model = Home_Slider
        fields = "__all__"
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'لطفا عنوان اسلایدر را وارد کنید',
            }),
            'text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'لطفا توضیحات اسلایدر را وارد کنید',
            }),
        }


class advanced_product_filter_form(forms.ModelForm):
    class Meta:
        model = Post_Products
        fields = ('status',)
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-control'
            })
        }


from Apps.Product_Apps__Ak.models import More_Product_Photos


class upload_multi_img_form(forms.Form):
    photo = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'd-none'
    }))
    product = forms.CharField(widget=forms.NumberInput(attrs={
        'class': 'd-none'
    }))


class deleted_product_form(forms.Form):
    deleted_product_id = forms.CharField()


class Search_Object_Form(forms.Form):
    object_id = forms.IntegerField()


class Search_Object_W_Contains_Form(forms.Form):
    text = forms.CharField()
