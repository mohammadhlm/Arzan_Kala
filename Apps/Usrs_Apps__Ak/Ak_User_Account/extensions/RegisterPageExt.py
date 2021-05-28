# User Model
from django.contrib.auth.models import User
# Redirect
from django.shortcuts import redirect


def RegisterUser(request, FormData, *args, **kwargs):
    FullName = FormData.cleaned_data.get("full_name")
    Email = FormData.cleaned_data.get("email")
    Password = FormData.cleaned_data.get("password")
    NewUser = User.objects.create_user(
        username=Email,
        email=Email,
        password=Password,
        first_name=FullName,
    )
    NewUser.is_active = False
    NewUser.save()
