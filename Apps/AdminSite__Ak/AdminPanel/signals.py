from django.db.models.signals import post_save
from .models import Email_Management
from django.dispatch import receiver
from django.shortcuts import get_object_or_404


@receiver(post_save, sender=Email_Management)
def edit_email_management_field(sender, instance, created, **kwargs):
    if created:
        email_qs = Email_Management.objects.filter(id=instance.id).first()
        email_qs.number_of_submissions = email_qs.user.all().count()
        email_qs.save()
