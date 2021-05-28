import os
import re
from random import randint as Gen_Number

# Validation Error Module
from django.core.validators import ValidationError


# Rename User Photo
def RenameUserPhoto(instance, filename):
    def GetNamePhoto(FilePath):
        GetFileName = os.path.basename(FilePath)
        Name, Ext = os.path.splitext(GetFileName)
        return Name, Ext

    Name, Ext = GetNamePhoto(filename)
    FinallyName = f"{instance.user.id}-{str(instance.user.username).replace(' ', '-')}{Ext}" if instance.user.id and instance.user.username is not None else f"{Gen_Number(1, 10)}-{str(instance.user.get_full_name()).replace(' ', '-')}{Ext}"
    return f"images/User/UserProfile/{FinallyName}"


# Image Size Validators
def ImageSizaValidators(Image):
    MaxSizeImage = 2.0
    if Image.file.size > MaxSizeImage * 1024 * 1024:
        raise ValidationError("حجم فایل نمایه کاربر نمیتواند بیشتر از 4 مگابایت باشد!")


# Postal Code Validator
def postal_code_validator(code):
    if re.search("(^[\d]{5}[\-]?[\d]{5}$)", str(code).strip()) is None:
        raise ValidationError('فرمت کد پستی صحیح نمیباشد لطفا از راهنمای این فیلد کمک بگیرید')


def phone_number_validator(phone):
    if re.search('(^0?[\d]{10}$)', str(phone).strip()) is None:
        raise ValidationError('فرمت شماره تلفن صحیح نمیباشد شماره تلفن شامل 11 رقم و میتواند شامل 0 نباشد')
