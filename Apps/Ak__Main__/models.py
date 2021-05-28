from django.db import models


# Create your models here.
# About Us Model
class About_Us(models.Model):
    who_are_we_img = models.ImageField(upload_to="images/About-Us", verbose_name="تصویر ما کی هستیم؟")
    who_are_we_title = models.CharField(max_length=30, verbose_name='عنوان ما کی هستیم؟')
    who_are_we = models.TextField(max_length=1000, verbose_name="متن ما کی هستیم؟")
    why_us_title = models.CharField(max_length=45,verbose_name="عنوان چرا ما؟")
    why_us_text = models.TextField(max_length=150, verbose_name="متن چرا ما؟")
    info_card_one_title = models.CharField(max_length=25, verbose_name="عنوان کارت اطلاعات 1")
    info_card_one = models.CharField(max_length=160, verbose_name="متن کارت اطلاعات 1")
    info_card_two_title = models.CharField(max_length=25, verbose_name="عنوان کارت اطلاعات 2")
    info_card_two = models.CharField(max_length=160, verbose_name="متن کارت اطلاعات 2")
    info_card_three_title = models.CharField(max_length=25, verbose_name="عنوان کارت اطلاعات 3")
    info_card_three = models.CharField(max_length=160, verbose_name="متن کارت اطلاعات 3")
    store_services_title_one = models.CharField(max_length=30, verbose_name="عنوان کارت اطلاعات خدمات فروشگاه 1")
    store_services_text_one = models.CharField(max_length=70, verbose_name="متن کارت اطلاعات خدمات فروشگاه 1")
    store_services_title_two = models.CharField(max_length=30, verbose_name="عنوان کارت اطلاعات خدمات فروشگاه 2")
    store_services_text_two = models.CharField(max_length=70, verbose_name="عنوان کارت اطلاعات خدمات فروشگاه 2")
    store_services_title_three = models.CharField(max_length=30, verbose_name="عنوان کارت اطلاعات خدمات فروشگاه 3")
    store_services_text_three = models.CharField(max_length=70, verbose_name="عنوان کارت اطلاعات خدمات فروشگاه 3")

    def __str__(self):
        return f"{self.id} تنظیمات سایت "
