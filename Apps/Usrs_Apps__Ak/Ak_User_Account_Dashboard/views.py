from django.shortcuts import render, reverse, redirect
from django.http import JsonResponse
from .forms import Activation_link_submission_form
# Dectrators Login Requierd
from django.contrib.auth.decorators import login_required
# User Model
from django.contrib.auth.models import User
from .forms import Change_User_Information
from Apps.Usrs_Apps__Ak.Ak_User_Account.models import Profile
from django.contrib.auth import logout

# Create your views here.

from Apps.Usrs_Apps__Ak.Ak_User_Account.views import Send_account_activation_link


@login_required()
def Dashboard(request, *args, **kwargs):
    context = {

    }
    return render(request=request, template_name='User_Apps/Ak_User_Account_Dashboard/dashboard.html', context=context)


@login_required()
def change_user_information(request):
    if not request.is_ajax():
        return redirect("Ak_Main:Home_Page")
    Change__User__Information = Change_User_Information(request.POST or None, request.FILES or None, initial={
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "user_profile": request.user.profile.user_profile,
        "gender_selection": request.user.profile.gender_selection,
        "postal_code": request.user.profile.postal_code,
        "phone_number": request.user.profile.phone_number,
        "location_first": request.user.profile.location_first,
    })

    if Change__User__Information.is_valid():
        try:
            request.user.first_name = Change__User__Information.cleaned_data.get("first_name")
            request.user.last_name = Change__User__Information.cleaned_data.get("last_name")
            request.user.profile.user_profile = Change__User__Information.cleaned_data.get("user_profile")
            request.user.profile.gender_selection = Change__User__Information.cleaned_data.get("gender_selection")
            request.user.profile.postal_code = Change__User__Information.cleaned_data.get("postal_code")
            request.user.profile.phone_number = Change__User__Information.cleaned_data.get("gender_selection")
            request.user.profile.location_first = Change__User__Information.cleaned_data.get("location_first")
            request.user.save()
            request.user.profile.save()
        except Exception as Err:
            return JsonResponse({
                "status": 203,
                "message": "لطفا فیلد هارا با دقت چک کنید و راهنمای آنهارا بررسی کنید..."
            })
        return JsonResponse({
            "status": 200,
            "message": "اطلاعات شما با موفقیت بروزرسانی شد"
        })
    elif Change__User__Information.errors:
        return JsonResponse(Change__User__Information.errors, safe=False)
    return render(request, "User_Apps/Ak_User_Account_Dashboard/change-user-information-form.html", context={
        "Change__User__Information": Change__User__Information
    })


@login_required()
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('Ak_Main:Home_Page')
