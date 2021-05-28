from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
# Create User Functional for Register Page
from .extensions.RegisterPageExt import RegisterUser
# Register Form
from .forms import RegisterForm, LoginForm
# Send Email
from django.core.mail import send_mail
from django.conf import settings
# Signal
from .signal.register_signal import Send_Mail_Registration_Successful
from django.db.models.signals import post_save
from django.dispatch import receiver
# Form Validation
from .Validation_User_Input.FormValidation import RecaptchaValidation
# Decrator
from django.contrib.auth.decorators import login_required
# Token Generator
from .utils import account_activation_token


def register_page(request, *args, **kwargs):
    register_form = RegisterForm(request.POST or None)
    if request.user.is_authenticated:
        return redirect("Ak_Main:Home_Page")
    if register_form.is_valid():
        if RecaptchaValidation(request.POST.get('g-recaptcha-response')):
            RegisterUser(request, register_form)
            return redirect("Ak_Main:Home_Page")
        else:
            messages.error(request, "×لطفا تیک من ربات نیستم را بزنید.")
            redirect("Ak_User_Account:Register")
    else:
        redirect("Ak_User_Account:Register")
    context = {
        "RegisterForm": register_form,
    }
    return render(request=request, template_name="User_Apps/Ak_User_Account/register.html", context=context)


def login_page(request, *args, **kwargs):
    login_form = LoginForm(request.POST or None)
    if request.user.is_authenticated:
        return redirect("Ak_Main:Home_Page")
    elif login_form.is_valid():
        if RecaptchaValidation(request.POST.get('g-recaptcha-response')):
            bool_accounts = authenticate(
                request,
                username=login_form.cleaned_data.get("email"),
                password=login_form.cleaned_data.get("password")
            )
            if bool_accounts:
                login(request, bool_accounts)
                return redirect("Ak_Main:Home_Page")
        else:
            messages.error(request, "×لطفا تیک من ربات نیستم را بزنید.")
            redirect("Ak_User_Account:Register")
    else:
        redirect("Ak_User_Account:Login")
    context = {
        "LoginForm": login_form
    }
    return render(request=request, template_name="User_Apps/Ak_User_Account/login.html", context=context)


from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.template.loader import get_template


def Send_account_activation_link(request):
    us = User.objects.get(email='mohammadds@gmail.com')
    current_site = get_current_site(request)
    mail_subject = 'فعالسازی حساب کاربری'
    context = {
        'user': us,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(us.id)),
        'token': account_activation_token.make_token(us),
    }
    htmly = get_template('Email_Html/email.html')
    to_email = "arzankala.ir@gmail.com"
    html_content = htmly.render(context)
    email = EmailMessage(
        mail_subject, html_content, settings.EMAIL_HOST_USER, to=[to_email]
    )
    email.send()
    return HttpResponse("Sent")


def activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('Ak_Main:Home_Page')
    else:
        return HttpResponse('Error')
