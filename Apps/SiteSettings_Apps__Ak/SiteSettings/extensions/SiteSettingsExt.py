# Error Module
from django.core.validators import ValidationError
# Import Random
from random import choice as random_choice
# String ascii Letters
from string import ascii_letters as string_ascii_letters
# Import Re
import re
# import Os
import os


# Logo Validator
def CheckLogo(Logo):
    def CheckFileSize(Logo):
        MaxLogoSize = 0.7
        return True if Logo.file.size < MaxLogoSize * 1024 * 1024 else False

    def CheckHeightAndWidth(Logo):
        return True if Logo.width <= 182 and Logo.height <= 47 else False

    if CheckFileSize(Logo) is False:
        raise ValidationError("حجم فایل لوگو شما نمیتواند بیشتر از (0.7) مگابایت باشد.")
    elif CheckHeightAndWidth(Logo) is False:
        raise ValidationError("اندازه ابعاد تصویر شما باید (عرض: 182 پیکسل × ارتفاع: 47 پیکسل باشد.)")


# Brand Photo Validator
def CheckBrandPhoto(Photo):
    def CheckFileSize(Photo):
        MaxLogoSize = 0.1
        return True if Photo.file.size < MaxLogoSize * 1024 * 1024 else False

    def CheckHeightAndWidth(Photo):
        return True if Photo.width <= 163 and Photo.height <= 85 else False

    if CheckFileSize(Photo) is False:
        raise ValidationError("حجم فایل عکس شما نمیتواند بیشتر از (0.1) مگابایت باشد.")
    elif CheckHeightAndWidth(Photo) is False:
        raise ValidationError("اندازه ابعاد تصویر شما باید (عرض: ۱۶۳ پیکسل × ارتفاع: ۸۵ پیکسل باشد.)")


def CheckThePreCodeContactPhone(Phone):
    if re.search("(^0[0-9]{2}-?[0-9]{8}$)", Phone) is None:
        raise ValidationError("فرمت شماره تلفن همراه شما صحیح نمی باشد.")


def CheckInstagramUrl(Url):
    if re.search('(^(http[s]?:\/\/www\.|http[s]?:\/\/|www\.)instagram.com\/[\S]+$)', str(Url).strip()) is None:
        raise ValidationError("آدرس اینستاگرام شما صحیح نمی باشد.")


def CheckYoutubeUrl(Url):
    if re.search("(^(http[s]?:\/\/www\.|http[s]?:\/\/|www\.)youtube\.com\/[\S]+$)", str(Url).strip()) is None:
        raise ValidationError("آدرس کانال یوتیوب شما صحیح نمی باشد.")


def CheckTelegramUrl(Url):
    if re.search('((^http[s]?:\/\/www\.|http[s]?:\/\/|www\.)?(telegram.com|[Tt]\.me)\/[\S]+$)',
                 str(Url).strip()) is None:
        raise ValidationError("آدرس تلگرام شما صحیح نمی باشد.")


def CheckFacebookUrl(Url):
    if re.search("(^(http[s]?:\/\/www\.|http[s]?:\/\/|www\.)facebook\.com\/[\S]+$)", str(Url).strip()) is None:
        raise ValidationError("آدرس فیسبوک شما صحیح نمی باشد.")


def CheckTwitterUrl(Url):
    if re.search('(^(http[s]?:\/\/www\.|http[s]?:\/\/|www\.)twitter\.com\/[\S]+$)', str(Url).strip()) is None:
        raise ValidationError("آدرس توییتر شما صحیح نمی باشد.")


def RenameTheLogoIcon(instance, filename):
    def GetNamePhoto(FilePath):
        GetFileName = os.path.basename(FilePath)
        Name, Ext = os.path.splitext(GetFileName)
        return Name, Ext

    Name, Ext = GetNamePhoto(filename)
    FinallyName = f"{str(instance) + ''.join(random_choice(string_ascii_letters.lower()) for i in range(3))}{Ext}"
    return f"images/SiteSettings/LogoIcon/{FinallyName}"


def RenameTheBrandPhoto(instance, filename, **kwargs):
    def GetNamePhoto(FilePath):
        GetFileName = os.path.basename(FilePath)
        Name, Ext = os.path.splitext(GetFileName)
        return Name, Ext

    Name, Ext = GetNamePhoto(filename)
    FinallyName = f"{str(instance)}-{''.join(random_choice(string_ascii_letters.lower()) for i in range(3))}-{Ext}"
    return f"images/SiteSettings/BrandPhoto/{FinallyName}"
