from django.db import models
from django.contrib.auth.models import User
# EXT
# Rename User Photo
from django.db.models import Q, Sum

from .extensions.ProfileModelExt import RenameUserPhoto
# Image Size Validators
from .extensions.ProfileModelExt import ImageSizaValidators
# Postal Code Validator
from .extensions.ProfileModelExt import postal_code_validator
# Phone Number Validator
from .extensions.ProfileModelExt import phone_number_validator
# Url
from django.urls import reverse_lazy
from django.urls import reverse_lazy, reverse


# Custom Profile Model Manager


class CustomModelManagerProfile(models.Manager):

    def Get_All_Information(self, user_id):
        user_profile = self.get_queryset().filter(user=user_id)
        return user_profile.first()

    def advanced_admin_user_list_filter(self, **kwargs):
        filters = {}
        for key, val in kwargs.get("value_list").items():
            if val is not None:
                filters[key] = val
        user_qs = self.get_queryset().filter(**filters)
        return user_qs


# Create your models here.
gender_selection_choices = [
    ('MS', 'زن'),
    ('MR', 'مرد'),
    ('TG', 'دیگر'),
]


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    user_profile = models.ImageField(
        verbose_name="پروفایل",
        upload_to=RenameUserPhoto,
        validators=[ImageSizaValidators],
        default='images/User/UserProfile/icon-avatar-default.png',
        blank=True
    )
    delete_profile_checkbox = models.BooleanField(
        verbose_name='حذف عکس کاربر',
        default=False,
        blank=True
    )
    gender_selection = models.CharField(
        verbose_name='انتخاب جنسیت',
        max_length=2,
        blank=True,
        choices=gender_selection_choices,
    )
    postal_code = models.CharField(
        verbose_name='کد پستی',
        max_length=20,
        validators=[postal_code_validator],
        blank=True,
        help_text='کد پستی 10 رقمی میتواند شامل خط تیره (-) یا نباشد',
    )
    phone_number = models.CharField(
        max_length=11,
        verbose_name='شماره تماس',
        help_text='شماره تماس باید 11 رقمی باشد و میتواند شامل صفر در ابتدای شماره نباشد',
        blank=True,
        validators=[phone_number_validator],
    )
    location_first = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="آدرس (1)"
    )
    NumberOfEmailsSentActivationLink = models.IntegerField(
        blank=True,
        default=0,
        verbose_name="تعداد ایمیل ارسالی فعالسازی حساب کاربری"
    )
    NumberOfEmailsSentToTheUser = models.IntegerField(
        blank=True,
        default=0,
        verbose_name="تعداد ایمیل های ارسال شده برای کاربر"
    )

    objects = CustomModelManagerProfile()

    @property
    def get_cart_item_count(self):
        Cart_qs = self.user.cart_set.filter(active=True)
        if Cart_qs.exists():
            Cart_Item_Qs = Cart_qs.first().cart_item_set.all()
            if Cart_Item_Qs.exists() and Cart_Item_Qs.count() > 0:
                return Cart_Item_Qs.count()
            else:
                return 0

    @property
    def get_cart_item(self):
        return self.user.cart_set.filter(active=True).first().cart_item_set.all()

    @property
    def total_user_purchases(self):
        qs = self.user.cart_set.filter(active=False)
        total = 0
        if qs:
            for cart in qs:
                total += cart.total_product_price
            return total

    def get_total_last_sale(self):
        qs = self.user.cart_set.filter(active=False)
        if qs:
            return qs.last().total_product_price

    def get_absolute_url_user_display(self):
        return reverse_lazy('AdminSite__Ak:show_user_view', kwargs={
            'pk': self.user.pk
        })

    def number_of_cards_paid_by_the_user(self):
        return self.user.cart_set.filter(active=False).count()

    def get_absolute_url_user_edit(self):
        return reverse_lazy('AdminSite__Ak:edit_user_view', kwargs={
            'pk': self.user.pk
        })

    def __str__(self):
        return self.user.get_full_name()

    class META:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
        ordering = ["id"]


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    msg = models.TextField(max_length=1500)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name() + f"({self.msg[0:20]}...)"
