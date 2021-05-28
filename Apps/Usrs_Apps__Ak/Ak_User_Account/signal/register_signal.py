from django.contrib.auth.models import User

# Signal
from django.db.models.signals import post_save
from django.dispatch import receiver

# Profile
from Apps.Usrs_Apps__Ak.Ak_User_Account.models import Profile


@receiver(post_save, sender=User)
def Send_Mail_Registration_Successful(sender, instance, created, **kwargs):
    if created:
        instance.username = instance.email
        instance.save()
        Profile.objects.create(user=instance)
        instance.profile.save()
