from django.shortcuts import render, HttpResponse
# Authenticate
from django.contrib.auth import authenticate, login, logout
# Import Messages
from django.contrib import messages
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
# Check Is SuperUser
from django.contrib.auth.decorators import user_passes_test
# Import User Model
from django.contrib.auth.models import User
from django.db.models import Sum, Count

from Apps.SiteSettings_Apps__Ak.SiteSettings.models import BrandPhotoModel
from Apps.Product_Apps__Ak.models import Cart, Brand_Model, Home_Slider
from Apps.SiteSettings_Apps__Ak.SiteSettings.models import SiteSettings
from Apps.AdminSite__Ak.AdminPanel.models import Email_Management
from Apps.AdminSite__Ak.AdminPanel.forms.email_management import Email_Management_Form, remove_mail_form
from Apps.AdminSite__Ak.AdminPanel.forms.product_form import deleted_product_form
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.template.loader import get_template
from Arzan_Kala import settings
from django.utils import timezone


# Render Partial Admin Header
def admin_header_view(request, *args, **kwargs):
    return render(request, 'AdminPanel/Component/Header/Header.html', {})


# home view for posts. Posts are displayed in a list
@user_passes_test(lambda user: user.is_superuser, login_url="AdminSite__Ak:AdminAuth")
def IndexView(request, *args, **kwargs):
    Member_Count = Profile.objects.filter(user__is_active=True).count()
    total_sale = Post_Products.objects.filter(cart_item__cart__active=False).aggregate(Sum("cart_item__total"))
    total_product_count = Post_Products.objects.filter(cart_item__cart__active=False).aggregate(
        Count("cart_item__count"))
    active_cart_count = Cart.objects.filter(active=True).count()

    last_sales = Cart.objects.filter(active=False).order_by("-id")[0:8]
    context = {
        "Member_Count": Member_Count,
        "total_sale": total_sale["cart_item__total__sum"] if total_sale.get(
            "cart_item__total__sum") is not None else None,
        "total_product_count": total_product_count["cart_item__count__count"] if total_product_count.get(
            "cart_item__count__count") is not None else None,
        "active_cart_count": active_cart_count,
        "last_sales": last_sales,
    }
    return render(request, template_name='AdminPanel/dashboard.html', context=context)


from Apps.GateWay__Ak.Py_Ir_GateWay.Wallet import WALLET
from Arzan_Kala.settings import LOGIN_PAY_PHONE_NUMBER, LOGIN_PAY_PASSWORD


@user_passes_test(lambda user: user.is_superuser, login_url="AdminSite__Ak:AdminAuth")
def WALLET_VIEW(request):
    if not request.is_ajax():
        return redirect('AdminSite__Ak:dashboard')
    Wallet_Obj = WALLET(LOGIN_PAY_PHONE_NUMBER, LOGIN_PAY_PASSWORD)
    return render(request, "AdminPanel/Wallet-Card/Card.html", {
        "Wallet_List": Wallet_Obj.GET_WALLET_LIST(),
    })


@user_passes_test(lambda user: user.is_superuser, login_url="AdminSite__Ak:AdminAuth")
def invoice_display(request, id):
    invoice = get_object_or_404(Cart, id=id)
    site_contact_info = SiteSettings.objects.first()
    context = {
        "invoice": invoice,
        "site_contact_info": site_contact_info
    }
    return render(request, "AdminPanel/Products/page-invoice.html", context)


@user_passes_test(lambda user: user.is_superuser, login_url="AdminSite__Ak:AdminAuth")
def email_management(request):
    if request.is_ajax() and request.GET and request.GET.get("email_id"):
        Email_msg = Email_Management.objects.filter(id=int(request.GET.get("email_id"))).first()
        if Email_msg:
            context = {
                "Email_Msg": Email_msg
            }
            return render(request, "AdminPanel/Email-Management/mail-msg.html", context)
    Email_qs = Email_Management.objects.all().order_by("-id", "-send_date")
    context = {
        "Email_Obj": Email_qs,
    }
    return render(request, "AdminPanel/Email-Management/app-email.html", context)


@user_passes_test(lambda user: user.is_superuser, login_url="AdminSite__Ak:AdminAuth")
def creating_sending_mail(request):
    Email_Management__Form = Email_Management_Form(request.POST or None)
    if Email_Management__Form.is_valid():
        mail_subject = Email_Management__Form.cleaned_data.get("subject")
        context = {
            'Subject': mail_subject,
            'Content': Email_Management__Form.cleaned_data.get("html_content")
        }
        htmly = get_template('AdminPanel/Email-Management/template-user-mail.html')
        html_content = htmly.render(context)
        email = EmailMessage(
            mail_subject, html_content, settings.EMAIL_HOST_USER,
            to=[user.email for user in Email_Management__Form.cleaned_data.get("user").all()]
        )
        email.send()
        Email_qs = Email_Management__Form.save()
        Email_qs.send_date = timezone.now()
        Email_qs.save()
        return redirect("AdminSite__Ak:email_management_view")
    context = {
        "Email_Management__Form": Email_Management__Form,
        "User_Obj": User.objects.filter(is_active=True)
    }
    return render(request, 'AdminPanel/Email-Management/creating-sending-mail.html', context)


@user_passes_test(lambda user: user.is_superuser, login_url="AdminSite__Ak:AdminAuth")
def remove_mail(request):
    remove_mail__form = remove_mail_form(request.POST or None)
    if remove_mail__form.is_valid():
        Email_obj = get_object_or_404(Email_Management, id=remove_mail__form.cleaned_data.get("removed_mail_id"))
        for Email_id in remove_mail__form.cleaned_data.get("removed_mail_id").split(","):
            if str(Email_id).isdigit():
                Email_qs = Email_Management.objects.filter(id=Email_id)
                Email_qs.delete()
                return JsonResponse({
                    "status": 200,
                    "message": "ایمیل انتخاب شده با موفقیت حذف شد."
                })
            else:
                return JsonResponse({
                    "status": 203,
                    "message": "اطلاعات ایمیل انتخاب شده به سرور ارسال شده صحیح نبوده است سرور در تلاش بود که آن را پیدا و حذف کند"
                })
        Email_obj.delete()
    return render(request, "AdminPanel/Email-Management/removed-mail-form.html", context={
        "remove_mail__form": remove_mail__form
    })


# Login To Panel
def LoginAdmin(request, *args, **kwargs):
    from .forms.authentication_form import AdminAuthLoginForm
    from Apps.Usrs_Apps__Ak.Ak_User_Account.Validation_User_Input.FormValidation import RecaptchaValidation
    """
    -Ver: 1 Stable
    -Last Update: 24 January 2021
    -View Base: FBV

    How is Worked View?
    1) If Super User Is Logged In System Redirect To Ak Dashboard
    2) If Not Valid Information SuperUser Show Message Error
    3) Check Robot Spamming
    """
    login_form = AdminAuthLoginForm(request.POST or None)
    if login_form.is_valid():
        if RecaptchaValidation(request.POST.get('g-recaptcha-response')):
            bool_accounts = authenticate(
                request,
                username=login_form.cleaned_data.get("email"),
                password=login_form.cleaned_data.get("password")
            )
            if bool_accounts is not None:
                login(request, bool_accounts)
                return redirect("AdminSite__Ak:dashboard")
            else:
                messages.error(request, "کاربری با این مشخصات در سیستم مدیر ها یافت نشد.")
        else:
            messages.error(request, 'لطفا تیک من ربات نیستم را بزنید')
    else:
        redirect("AdminSite__Ak:AdminAuth")
    return render(request=request, template_name='AdminPanel/Auth/login.html', context={"form": login_form})


@user_passes_test(lambda user: user.is_superuser and user.is_active and user.is_authenticated,
                  login_url="AdminSite__Ak:AdminAuth")
def LogOut_Admin_View(request):
    if request.user.is_authenticated and request.user.is_superuser:
        logout(request)
        return redirect('AdminSite__Ak:dashboard')


import json
# Edit a post
from Apps.AdminSite__Ak.AdminPanel.forms.user_information_change_form import (
    default_user_edit_form,
    user_information_editing_form,
)
from django.http import JsonResponse


@user_passes_test(lambda user: user.is_superuser, login_url="AdminSite__Ak:AdminAuth")
def edit_user_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    default__user_edit_form = default_user_edit_form(
        request.POST or None,
        instance=user
    )
    if default__user_edit_form.is_valid():
        default__user_edit_form.save()
        return JsonResponse({
            'bool': True,
            'text': 'تغییرات با موفقیت اعمال شد',
        })
    elif default__user_edit_form.errors:
        return JsonResponse(
            default__user_edit_form.errors,
            safe=False
        )

    context = {
        'default__user_edit_form': default__user_edit_form,
        'edit_user': user
    }
    return render(request, 'AdminPanel/Users/user-edit.html', context)


@user_passes_test(lambda user: user.is_superuser, login_url="AdminSite__Ak:AdminAuth")
def save_information_edit_user(request, pk):
    if not request.is_ajax():
        return redirect("AdminSite__Ak:list_users_view")
    user = get_object_or_404(User, pk=pk)
    user__information_editing_form = user_information_editing_form(request.POST or None, request.FILES or None,
                                                                   instance=user.profile)
    if user__information_editing_form.is_valid():
        if user__information_editing_form.cleaned_data.get("delete_profile_checkbox"):
            user.profile.user_profile = "/media/images/User/UserProfile/icon-avatar-default.png"
            user.profile.save()
            return JsonResponse({
                'bool': True,
                'src': user.profile.user_profile.url,
                'text': 'نمایه کاربر با موفقیت حذف شد',
            })
        user__information_editing_form.save()
        return JsonResponse({
            'bool': True,
            'src': user.profile.user_profile.url,
            'text': 'تغییرات با موفقیت اعمال شد',
        })
    context = {"user__information_editing_form": user__information_editing_form}
    return render(request, "AdminPanel/Users/save_information_edit_user.html", context)


# ------------User List User View--------------

from Apps.AdminSite__Ak.AdminPanel.forms.user_information_change_form import (
    default_user_form,
    user_information_form,
)


@user_passes_test(lambda user: user.is_superuser, login_url="AdminSite__Ak:AdminAuth")
def list_user_view(request):
    from django.core.paginator import Paginator
    if request.GET.get('update') == 'true':
        pass
    contact_list = User.objects.all()
    paginator = Paginator(contact_list, 4)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'list_users': page_obj,
    }
    return render(request, 'AdminPanel/Users/users-list.html', context)


# Ajax Form
@user_passes_test(lambda user: user.is_superuser, login_url="AdminSite__Ak:AdminAuth")
def default_user_form_view(request):
    default__user_form = default_user_form(request.POST or None)
    if not request.is_ajax():
        return redirect('AdminSite__Ak:list_users_view')
    if default__user_form.is_valid():
        user = default__user_form.save(commit=False)
        user.set_password(default__user_form.cleaned_data.get("password"))
        user.save()
        return JsonResponse({
            'created': True,
            'pk': User.objects.get(username=default__user_form.cleaned_data.get("email")).pk,
            'msg_text': 'ثبت نام کاربر با موفقیت انجام شد'
        })
    return render(request, 'AdminPanel/Users/html-form/default__user_form.html',
                  context={'default__user_form': default__user_form})


# Ajax Form
@user_passes_test(lambda user: user.is_superuser, login_url="AdminSite__Ak:AdminAuth")
def user_information_form_view(request, pk):
    user = User.objects.get(pk=pk)
    user__information_form = user_information_form(request.POST or None, request.FILES or None, instance=user.profile)
    if not request.is_ajax():
        return redirect('AdminSite__Ak:list_users_view')
    if user__information_form.is_valid():
        user__information_form.save()
        return JsonResponse({
            'created': True,
            'msg_text': 'ثبت نام کاربر با موفقیت انجام شد'
        })
    return render(request, 'AdminPanel/Users/html-form/user__information_form.html',
                  {'user__information_form': user__information_form})


# Ajax Form
from .forms.user_information_change_form import delete_user_form


@user_passes_test(lambda user: user.is_superuser, login_url="AdminSite__Ak:AdminAuth")
def delete_user_view(request):
    delete_users_form = delete_user_form(request.POST or None)
    if not request.is_ajax():
        redirect('AdminSite__Ak:list_users_view')
    if delete_users_form.is_valid():
        list_user_id = delete_users_form.cleaned_data.get('user_id').split(',')
        try:
            for user_id in list_user_id:
                User.objects.filter(pk=int(user_id)).first().delete()
            return JsonResponse({'status': 200})
        except:
            pass
    return render(request, 'AdminPanel/Users/user-delete.html', {'delete_users_form': delete_users_form})


# Advanced User Filter
from Apps.Usrs_Apps__Ak.Ak_User_Account.models import Profile
from django.core.paginator import Paginator


@user_passes_test(lambda user: user.is_superuser, login_url="AdminSite__Ak:AdminAuth")
def advanced_user_filter_view(request):
    GENDER = json.loads(request.GET.get("gender")) if request.GET.get("gender") == 'null' else request.GET.get("gender")
    Para_qs = {
        'user__is_active': json.loads(request.GET.get("status")),
        'user__is_superuser': json.loads(request.GET.get("role")),
        'gender_selection': GENDER
    }
    User_qs = Profile.objects.advanced_admin_user_list_filter(value_list=Para_qs)
    paginator = Paginator(User_qs, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'AdminPanel/Users/user-list-filter.html', {'list_users': page_obj})


# Show User View
from .forms.user_information_change_form import user_profile_account_deletion_form


@user_passes_test(lambda user: user.is_superuser, login_url="AdminSite__Ak:AdminAuth")
def show_user_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    user__profile_account_deletion_form = user_profile_account_deletion_form(request.POST or None,
                                                                             initial={'user_id': pk})
    if user__profile_account_deletion_form.is_valid():
        user.delete()
        return redirect('AdminSite__Ak:list_users_view')
    context = {
        'user_view': user,
        'user__profile_account_deletion_form': user__profile_account_deletion_form
    }
    return render(request, 'AdminPanel/Users/user-view.html', context)


from django.core.paginator import Paginator
from Apps.Product_Apps__Ak.models import Post_Products


@user_passes_test(lambda user: user.is_superuser, login_url="AdminSite__Ak:AdminAuth")
def products_list_view(request):
    paginator = Paginator(Post_Products.objects.all(), 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'products_list': page_obj,
    }
    return render(request, 'AdminPanel/Products/products-list.html', context)


# Advanced Filter Product
from .forms.product_form import advanced_product_filter_form


@user_passes_test(lambda user: user.is_superuser, login_url="AdminSite__Ak:AdminAuth")
def advanced_product_filter(request):
    advanced_product_filter__form = advanced_product_filter_form(request.GET)
    if not request.is_ajax():
        return redirect("AdminSite__Ak:products_list_view")
    if advanced_product_filter__form.is_valid():
        status = advanced_product_filter__form.cleaned_data.get("status")
        qs_product = Post_Products.objects.get_pr_status(status=status)
        if qs_product is not None:
            paginator = Paginator(qs_product, 4)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context = {
                'products_list': page_obj,
            }
            return render(request, 'AdminPanel/Products/product-list-filter.html', context)
        else:
            return render(request, 'AdminPanel/Products/product-list-filter.html')
    return render(request, 'AdminPanel/Products/product-form/advanced-filter-product_list.html',
                  {"advanced_filter_form": advanced_product_filter__form})


def deleted_product_view(request):
    deleted_product__form = deleted_product_form(request.POST or None)
    if deleted_product__form.is_valid():
        for pr__id in deleted_product__form.cleaned_data.get("deleted_product_id").split(","):
            if str(pr__id).isdigit():
                pr_qs = Post_Products.objects.filter(id=pr__id)
                if pr_qs:
                    delete_product_id = pr__id
                    pr_qs.first().delete()
                    return JsonResponse({"delete_product_id": delete_product_id})
                else:
                    return JsonResponse({
                        "status": 203,
                        'message': "محصول انتخاب شده در لیست محصولات یافت نشد."
                    })
            else:
                return JsonResponse({
                    "status": 203,
                    "message": "اطلاعات ارسال شده صحیح نبوده است...\n سرور متاسفانه نتوانست درخواست شما را پردازش کند..."
                })

    return render(request, "AdminPanel/Products/product-form/deleted_product_form.html", context={
        "deleted_product__form": deleted_product__form,
    })


from django.forms import formset_factory
from .forms.product_form import upload_multi_img_form
from Apps.Product_Apps__Ak.models import More_Product_Photos


@user_passes_test(lambda user: user.is_superuser, login_url="AdminSite__Ak:AdminAuth")
def add_more_img_product(request):
    form_all = formset_factory(upload_multi_img_form, extra=5)
    pr_img_form_set = form_all(request.POST or None, request.FILES or None)
    if pr_img_form_set.is_valid():
        for form in pr_img_form_set:
            owner = get_object_or_404(Post_Products, id=form.cleaned_data.get("product"))
            file = form.cleaned_data.get('photo')
            More_Product_Photos.objects.create(Product_Photos=owner, photo=file)
        return JsonResponse({'status': 200})
    return render(request, 'AdminPanel/Products/product-form/add-img-product.html', {'form': pr_img_form_set})


from .forms.product_form import product_creation_form


@user_passes_test(lambda user: user.is_superuser, login_url="AdminSite__Ak:AdminAuth")
def create_product_view(request):
    product_creation__form = product_creation_form(request.POST or None, request.FILES or None)
    if product_creation__form.errors:
        return JsonResponse(product_creation__form.errors, safe=False)
    if product_creation__form.is_valid():
        product_creation__form.save()
        return JsonResponse({'status': 200})

    return render(
        request,
        'AdminPanel/Products/product-add.html',
        {'product_creation__form': product_creation__form, 'upload_img': ''}
    )


# Search Tag View Ajax
from Apps.Product_Apps__Ak.models import Product_Tags, Category_Product
from .forms.product_form import Search_Object_Form, Search_Object_W_Contains_Form


@user_passes_test(lambda user: user.is_superuser, login_url="AdminSite__Ak:AdminAuth")
def search_tag_view(request):
    Search_Object_W_Contains__Form = Search_Object_W_Contains_Form(request.GET or None)
    if Search_Object_W_Contains__Form.is_valid():
        Search_Text = Search_Object_W_Contains__Form.cleaned_data.get("text")
        Tag_qs = Product_Tags.objects.search_tag_pr_add(sr_qs=Search_Text)
        Json_Response = {"results": []}
        if Tag_qs:
            for Tag_Obj in Tag_qs:
                Item_Added = {"text": f"{Tag_Obj.tag_name}", "id": f"{Tag_Obj.id}"}
                Json_Response.get("results").append(Item_Added)
                return JsonResponse(Json_Response, charset="UTF-8", json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse(Json_Response)


# Search Live Category Ajax
@user_passes_test(lambda user: user.is_superuser, login_url="AdminSite__Ak:AdminAuth")
def search_category_view(request):
    Search_Object_W_Contains__Form = Search_Object_W_Contains_Form(request.GET or None)
    if Search_Object_W_Contains__Form.is_valid():
        Search_Text = Search_Object_W_Contains__Form.cleaned_data.get("text")
        Category_qs = Category_Product.objects.filter(category_name__icontains=Search_Text)
        Json_Response = {"results": []}
        if Category_qs:
            for Cat_Obj in Category_qs:
                Item_Added = {"text": f"{Cat_Obj.category_name}", "id": f"{Cat_Obj.id}"}
                Json_Response.get("results").append(Item_Added)
                return JsonResponse(Json_Response, charset="UTF-8", json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse(Json_Response)


# Search Live Brand
@user_passes_test(lambda user: user.is_superuser, login_url="AdminSite__Ak:AdminAuth")
def search_brand_view(request):
    Search_Object_W_Contains__Form = Search_Object_W_Contains_Form(request.GET or None)
    if Search_Object_W_Contains__Form.is_valid():
        Search_Text = Search_Object_W_Contains__Form.cleaned_data.get("text")
        Brand_qs = Brand_Model.objects.filter(name__icontains=Search_Text)
        Json_Response = {"results": []}
        if Brand_qs:
            for Brand_Obj in Brand_qs:
                Item_Added = {"text": f"{Brand_Obj.name}", "id": f"{Brand_Obj.id}"}
                Json_Response.get("results").append(Item_Added)
                return JsonResponse(Json_Response, charset="UTF-8", json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse(Json_Response)


# Search Live Slider
@user_passes_test(lambda user: user.is_superuser, login_url="AdminSite__Ak:AdminAuth")
def search_slider_view(request):
    Search_Object_W_Contains__Form = Search_Object_W_Contains_Form(request.GET or None)
    if Search_Object_W_Contains__Form.is_valid():
        Search_Text = Search_Object_W_Contains__Form.cleaned_data.get("text")
        Slider_qs = Home_Slider.objects.filter(text__icontains=Search_Text)
        Json_Response = {"results": []}
        if Slider_qs:
            for Slider_Obj in Slider_qs:
                Item_Added = {"text": f"{Slider_Obj.title}", "id": f"{Slider_Obj.id}"}
                Json_Response.get("results").append(Item_Added)
                return JsonResponse(Json_Response, charset="UTF-8", json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse(Json_Response)


@user_passes_test(lambda user: user.is_superuser, login_url="AdminSite__Ak:AdminAuth")
def create_tag_view(request):
    from .forms.product_form import tag_creation_form
    if not request.is_ajax():
        return redirect('AdminSite__Ak:create_product_view')
    tag__creation_form = tag_creation_form(request.POST or None)
    if tag__creation_form.is_valid():
        tag__creation_form.save()
        return JsonResponse({
            'status': 200,
            'message': 'برچسب محصول با موفقیت ساخته شد.'
        })
    elif tag__creation_form.errors:
        return JsonResponse(
            tag__creation_form.errors, safe=False
        )
    return render(request, 'AdminPanel/Products/Tags/tag-add.html', {'tag_creation_form': tag__creation_form})


@user_passes_test(lambda user: user.is_superuser, login_url="AdminSite__Ak:AdminAuth")
def create_category_view(request):
    from .forms.product_form import category_creation_form
    if not request.is_ajax():
        return redirect('AdminSite__Ak:create_product_view')
    category__creation_form = category_creation_form(request.POST or None, request.FILES or None)
    if category__creation_form.is_valid():
        category__creation_form.save()
        return JsonResponse({
            "status": 200,
            "message": "دسته بندی محصول با موفقیت ایجاد شد."
        })
    elif category__creation_form.errors:
        return JsonResponse(category__creation_form.errors, safe=False)
    return render(request, 'AdminPanel/Products/category/category-add.html',
                  {'category_creation_form': category_creation_form})


from .forms.product_form import brand_creation_form, slider_creation_form


@user_passes_test(lambda user: user.is_superuser, login_url="AdminSite__Ak:AdminAuth")
def create_brand_view(request):
    if not request.is_ajax():
        return redirect("AdminSite__Ak:products_list_view")
    brand_creation__form = brand_creation_form(request.POST or None, request.FILES or None)
    if brand_creation__form.is_valid():
        brand_creation__form.save()
        return JsonResponse({
            "status": 200,
            "message": "برند با موفقیت ایجاد شد"
        })
    elif brand_creation__form.errors:
        return JsonResponse(brand_creation__form.errors, safe=False)
    return render(request, "AdminPanel/Products/Brand-Form/brand-form.html", context={
        "brand_creation__form": brand_creation__form
    })


@user_passes_test(lambda user: user.is_superuser, login_url="AdminSite__Ak:AdminAuth")
def create_slider_view(request):
    if not request.is_ajax():
        return redirect("AdminSite__Ak:products_list_view")
    slider_creation__form = slider_creation_form(request.POST or None)
    if slider_creation__form.errors:
        pass
    if slider_creation__form.is_valid():
        slider_creation__form.save()
        return JsonResponse({
            "status": 200,
            "message": "اسلایدر با موفقیت ایجاد شد"
        })
    elif slider_creation__form.errors:
        return JsonResponse(slider_creation__form.errors, safe=False)
    return render(request, "AdminPanel/Products/slider-form/slider-form.html", context={
        "slider_creation__form": slider_creation__form
    })


# ------------------------------------
# ----------- Site Settings-----------
@user_passes_test(lambda user: user.is_superuser, login_url="AdminSite__Ak:AdminAuth")
def view_settings(request):
    return render(request, 'AdminPanel/Settings/view-settings.html', {
    })


from .models import Customize_Theme
from .forms.customizer_theme_form import customizer_theme_form


@user_passes_test(lambda user: user.is_superuser, login_url="AdminSite__Ak:AdminAuth")
def customizer_theme(request):
    print(request.POST)
    customize_obj = Customize_Theme.objects.first()
    customizer__theme__form = customizer_theme_form(request.POST or None, instance=customize_obj)
    if customizer__theme__form.is_valid():
        customizer__theme__form.save()
        return JsonResponse({
            "status": 200,
            "messages": "تغییرات حالت ظاهری پنل ادمین با موفقیت ذخیره شد..."
        })
    return render(request, "AdminPanel/__Main__/Customizer__Main__.html",
                  {'customizer__theme__form': customizer__theme__form, 'customize_obj': customize_obj})
