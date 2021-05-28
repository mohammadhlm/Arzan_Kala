from django.db import models

# Logo Validators
from .extensions.SiteSettingsExt import CheckLogo
# Email Validator
from Apps.Usrs_Apps__Ak.Ak_User_Account.Validation_User_Input.FormValidation import EmailValidation
# Validator
from .extensions.SiteSettingsExt import (
    # Site Settings Validator
    CheckThePreCodeContactPhone,
    CheckYoutubeUrl,
    CheckInstagramUrl,
    CheckTwitterUrl,
    CheckTelegramUrl,
    CheckFacebookUrl,
    # Brand Photo Validator
    CheckBrandPhoto,
)

# Rename Logo Icon
from .extensions.SiteSettingsExt import RenameTheLogoIcon
# Rename Brand Photo
from .extensions.SiteSettingsExt import RenameTheBrandPhoto


# Create your models here.
class SiteSettings(models.Model):
    SiteSettingName = models.CharField(max_length=35)
    BlackLogoSiteHeader = models.ImageField(
        verbose_name="لوگو هدر سایت",
        upload_to=RenameTheLogoIcon,
        validators=[CheckLogo],
    )
    WhiteLogoSiteFooter = models.ImageField(
        verbose_name="لوگو فوتر سایت",
        upload_to=RenameTheLogoIcon,
        validators=[CheckLogo],
    )
    CopyrightText = models.CharField(
        verbose_name="متن کپی رایت",
        max_length=70,
    )
    CompanyAddress = models.CharField(
        verbose_name='آدرس شرکت',
        max_length=60,
    )
    EmailSupportSite = models.EmailField(
        verbose_name="آدرس ایمیل پشتیبانی سایت",
        max_length=40,
        validators=[EmailValidation],
    )
    SiteSupportContactNumber = models.CharField(
        verbose_name="شماره تلفن پشتیبانی سایت",
        max_length=15,
        validators=[CheckThePreCodeContactPhone],
    )
    ShortDescriptionFooter = models.CharField(
        verbose_name='توضیحات کوتاه سایت در پاورقی',
        max_length=100,
    )
    InstagramSite = models.URLField(
        verbose_name="آدرس اینستاگرام سایت",
        validators=[CheckInstagramUrl],
    )
    YoutubeSite = models.URLField(
        verbose_name='آدرس کانال یوتیوب سایت',
        validators=[CheckYoutubeUrl],
    )
    TelegramSite = models.URLField(
        verbose_name='آدرس کانال تلگرام سایت',
        validators=[CheckTelegramUrl],
    )
    FacebookSite = models.URLField(
        verbose_name="آدرس فیسبوک سایت",
        validators=[CheckFacebookUrl],
    )
    TwitterSite = models.URLField(
        verbose_name='آدرس توییتر سایت',
        validators=[CheckTwitterUrl],
    )

    def __str__(self):
        return self.SiteSettingName


# Brand Photo Model (Relational Site Settings)
class BrandPhotoModel(models.Model):
    BrandName = models.CharField(max_length=35, unique=True)
    BrandPhoto = models.ImageField(
        upload_to=RenameTheBrandPhoto,
        validators=[CheckBrandPhoto],
    )
    SiteSetting = models.ForeignKey(SiteSettings, on_delete=models.CASCADE)

    def __str__(self):
        return self.BrandName


class SelectSiteSetting(models.Model):
    SelectBox = models.OneToOneField(
        SiteSettings,
        on_delete=models.CASCADE,
        verbose_name="انتخاب تنظمیات سایت",

    )

    def __str__(self):
        return self.SelectBox.SiteSettingName


# Signal Select Site Setting
from .SiteSettingSignal.signals import CreateObjectBrandPhoto
