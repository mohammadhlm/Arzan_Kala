from django import forms

# Form Auth
from django.contrib.auth.models import User
from Apps.Usrs_Apps__Ak.Ak_User_Account.models import Profile


# Edit User
class default_user_edit_form(forms.ModelForm):
    class Meta:
        fields = ('first_name', 'last_name', 'username', 'is_active', 'is_superuser', 'is_staff')
        model = User
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'نام',
                    'data-validation-required-message': "لطفا این فیلد را پر کنید این فیلد الزامی است"
                }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام',
                'data-validation-required-message': "لطفا این فیلد را پر کنید این فیلد الزامی است"
            }),
            'username': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام کاربری',
                'data-validation-required-message': "لطفا این فیلد را پر کنید این فیلد الزامی است"
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'custom-control-input',
            }),
            'is_superuser': forms.CheckboxInput(attrs={
                'class': 'custom-control-input',
            }),
            'is_staff': forms.CheckboxInput(attrs={
                'class': 'custom-control-input',
            })
        }


class user_information_editing_form(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'phone_number',
            'postal_code',
            'location_first',
            'gender_selection',
            'user_profile',
            'delete_profile_checkbox',
        )
        widgets = {
            'phone_number': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'تلفن همراه را وارد نمایید...',
                }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'کد پستی را وارد نمایید...'
            }),
            'location_first': forms.Textarea(attrs={
                'rows': 1,
                'style': 'resize:none;height:2.7125rem',
                'class': 'form-control',
                'placeholder': 'آدرس خود را وارد نمایید...'
            }),
            'gender_selection': forms.Select(attrs={
                'class': 'form-control'
            }), 'user_profile': forms.FileInput(attrs={
                'style': 'display:none;'
            }),
            'delete_profile_checkbox': forms.CheckboxInput(attrs={
                'style': 'display:none;'
            })
        }


# Create User
class default_user_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'is_active', 'is_superuser', 'is_staff',)
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام خانوادگی'
            }),
            'username': forms.TextInput(attrs={
                'style': 'display:none'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ایمیل را وارد نمایید...'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'پسورد را وارد نمایید...'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'custom-control-input'
            }),
            'is_superuser': forms.CheckboxInput(attrs={
                'class': 'custom-control-input'
            }),
            'is_staff': forms.CheckboxInput(attrs={
                'class': 'custom-control-input'
            })
        }


class user_information_form(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('user_profile', 'gender_selection', 'location_first', 'phone_number', 'postal_code',)
        widgets = {
            'user_profile': forms.FileInput(attrs={
                'style': 'display:none;opacity:0'
            }),
            'gender_selection': forms.Select(
                attrs={
                    'class': 'form-control'
                },
            ),
            'location_first': forms.Textarea(attrs={
                'rows': 1,
                'style': 'resize:none;height:2.7125rem',
                'class': 'form-control',
                'placeholder': 'آدرس خود را وارد نمایید...'
            }),
            'phone_number': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'تلفن همراه را وارد نمایید...',
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'کد پستی را وارد نمایید...'
            }),
        }

        # User View Form


class user_profile_account_deletion_form(forms.Form):
    user_id = forms.IntegerField(widget=forms.HiddenInput())


# Delete User
class delete_user_form(forms.Form):
    user_id = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'style': 'display:none'
        }))
