from django.db import models
from ckeditor.fields import RichTextField, CKEditorWidget
from django.contrib.auth.models import User
from Arzan_Kala.Extentions import Jalali_date_converter


class Customize_Theme(models.Model):
    CHOICES_COLOR = [
        ('PR', 'بنفش'),
        ('GR', 'سبز'),
        ('RD', 'قرمز'),
        ('BL', 'آبی'),
        ('OG', 'نارنجی'),
        ('BC', 'مشکی'),
    ]
    CHOICES_THEME = [
        ('LT', 'روشن'),
        ('DK', 'تاریک'),
        ('ST', 'نیمه روشن'),
    ]
    CHOICES_MENU_MODE = [
        ('CD', 'بسته'),
        ('ON', 'باز'),
    ]
    CHOICES_COLOR_HEADER = [
        ('WT', 'سفید'),
        ('PR', 'بنفش'),
        ('GR', 'سبز'),
        ('RD', 'قرمز'),
        ('BL', 'آبی'),
        ('OG', 'نارنجی'),
        ('BC', 'مشکی'),
    ]
    CHOICES_HEADER_MODE = [
        ('HN', 'مخفی'),
        ('FD', 'ثابت'),
        ('SG', 'چسبیده'),
        ('FG', 'شناور'),
    ]
    CHOICES_FOOTER_MODE = [
        ('HN', 'مخفی'),
        ('FD', 'ثابت'),
        ('SG', 'چسبیده'),
    ]
    menu_color = models.CharField(verbose_name="رنگ منو", choices=CHOICES_COLOR, default='BL', max_length=2)
    theme_color = models.CharField(verbose_name='رنگ تم', choices=CHOICES_THEME, default='LT', max_length=2)
    menu_mode = models.BooleanField(verbose_name='حالت منو', default=False)
    header_color = models.CharField(verbose_name='رنگ سربرگ', choices=CHOICES_COLOR_HEADER, default='WT', max_length=2)
    header_mode = models.CharField(verbose_name='حالت سربرگ', choices=CHOICES_HEADER_MODE, default='FG', max_length=2)
    footer_mode = models.CharField(verbose_name='حالت پاورقی', choices=CHOICES_FOOTER_MODE, default='FD', max_length=2)
    flash_navigation_mode = models.BooleanField(verbose_name='حالت فلش پیمایش صفحه', default=True)


class Email_Management(models.Model):
    user = models.ManyToManyField(User)
    subject = models.CharField(max_length=200)
    html_content = RichTextField(config_name='Email_Management_Config', max_length=2800)
    send_date = models.DateTimeField(null=True, blank=True)
    number_of_submissions = models.BigIntegerField(blank=True, null=True)

    @property
    def Jalali_send_date(self):
        return Jalali_date_converter(self.send_date)

    def save(self, *args, **kwargs):
        return super(Email_Management, self).save(*args, **kwargs)


from .signals import edit_email_management_field
