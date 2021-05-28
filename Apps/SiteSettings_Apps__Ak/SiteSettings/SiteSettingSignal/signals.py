# Signal
from django.db.models.signals import post_save
from django.dispatch import receiver
# Mdoel Site Settings
from Apps.SiteSettings_Apps__Ak.SiteSettings.models import SiteSettings
# Model Select Site Setting
from Apps.SiteSettings_Apps__Ak.SiteSettings.models import SelectSiteSetting


@receiver(post_save, sender=SiteSettings)
def CreateObjectBrandPhoto(sender, instance, created, **kwargs):
    if created:
        ObjectBrandPhoto = SelectSiteSetting.objects.create(SelectBox=instance)
        ObjectBrandPhoto.save()
