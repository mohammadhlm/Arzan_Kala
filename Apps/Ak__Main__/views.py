from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from Apps.GateWay__Ak.models import Trans_Verify
from Apps.GateWay__Ak.Py_Ir_GateWay.Client import Py_Ir
# Create your views here.
from Apps.Product_Apps__Ak.models import Comment, Rating
from .forms import Comment_Form, Rating_Form
from Apps.Product_Apps__Ak.models import Home_Slider, Cart, Cart_Item

# GetWay Api
from Arzan_Kala.settings import gate_way_api_key
from django.utils import timezone


def grouped_object(list_obj):
    list_grouped = []
    range_number = int(len(list_obj) / 3) + 1 if type(len(list_obj) / 3) == float else int(len(list_obj) / 3)
    for _ in range(range_number):
        list_grouped.append(
            [list_obj.pop(len(list_obj) - 1) for _ in range(3 if len(list_obj) >= 3 else len(list_obj))])
    return list_grouped


def home_page(request, *args, **kwargs):
    Home__Slider = Home_Slider.objects.first()
    new_product = Post_Products.objects.get_new_product()
    best_sellers_product = Post_Products.objects.get_the_most_product_sold()
    discounted_products = Post_Products.objects.get_discounted_products()
    special_offer_products = Post_Products.objects.get_special_offer_products()

    best_sellers_product_2 = Post_Products.objects.get_the_most_product_sold()[0:5]
    best_rated_product = Post_Products.objects.get_the_best_rated_product()

    context = {
        "list_new_product": new_product,
        "list_best_sellers_product": best_sellers_product,
        "list_discounted_products": discounted_products,
        'list_special_offer_products': special_offer_products,
        #     End Show
        "list_best_sellers_product_2": grouped_object(list(best_sellers_product_2)),
        'list_best_rated_product': grouped_object(list(best_rated_product)),
        "list_most_visited": Post_Products.objects.get_the_most_visited_product()[0:7],
        'Home__Slider': Home__Slider,
    }
    response = render(request, "index.html", context)
    return response


from Apps.SiteSettings_Apps__Ak.SiteSettings.models import SiteSettings
from .forms import Contact_Form
from Apps.Usrs_Apps__Ak.Ak_User_Account.Validation_User_Input.FormValidation import RecaptchaValidation
from django.contrib import messages


def contact_us(request):
    Contact__Form = Contact_Form(request.POST or None, initial={
        "user": request.user.id
    })

    if Contact__Form.is_valid():
        if RecaptchaValidation(request.POST.get("g-recaptcha-response")):
            Contact__Form.save()
            return redirect("Ak_Main:contact-us")
        else:
            messages.error(request, "×لطفا تیک من ربات نیستم را بزنید.")
            redirect("Ak_Main:contact-us")
    contact_info = SiteSettings.objects.first()
    context = {
        "Contact__Form": Contact__Form,
        'contact_info': contact_info
    }
    return render(request, "contact-us.html", context)


def product_detail(request, slug):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    Product_Visit_Counter.objects.get_or_create(ip=ip, product__slug=slug)

    product_qs = get_object_or_404(Post_Products, slug=slug)
    related_product = Post_Products.objects.filter(status="PB", category=product_qs.category.first()).order_by("-id")[
                      0:7]
    context = {
        "product": product_qs,
        'related_product': related_product
    }
    return render(request, "product-detail.html", context)


def category_detail(request, slug):
    return render(request, "", {})


from Apps.Product_Apps__Ak.models import Post_Products, Category_Product, Brand_Model, Product_Visit_Counter
from .forms import form_advanced_filter_shop


def shop_page(request):
    form__advanced_filter_shop = form_advanced_filter_shop(request.GET or None)
    category_qs = Category_Product.objects.show_cat_shop()
    context = {
        'form__advanced_filter_shop': form__advanced_filter_shop,
        "list_category": category_qs,
        "list_brand": Brand_Model.objects.all()[0:5]
    }
    return render(request, "shop.html", context)


def product_ajax_filter(request):
    form__advanced_filter_shop = form_advanced_filter_shop(request.GET or None)
    product_qs = Post_Products.objects.all()
    if form__advanced_filter_shop.is_valid():
        product_qs = Post_Products.objects.advanced_filter_product_shop(
            order=form__advanced_filter_shop.cleaned_data.get("order"),
            brand_id=form__advanced_filter_shop.cleaned_data.get("brand_id"),
            category_id=form__advanced_filter_shop.cleaned_data.get("category_id"),
            price_filter=form__advanced_filter_shop.cleaned_data.get("price_filter")
        )
    paginator = Paginator(product_qs, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj
    }
    return render(request, "product_ajax_filter.html", context)


def comment_for_product(request, slug):
    product_qs = get_object_or_404(Post_Products, slug=slug)
    if not request.is_ajax():
        return redirect("Ak_Main:shop_page")
    if len(Comment.objects.filter(user_id=request.user.id, product_id=product_qs.id)) == 0:
        Comment__Form = Comment_Form(request.POST or None, initial={"user": request.user.id, "product": product_qs.id})
        if Comment__Form.is_valid():
            Comment___Form = Comment__Form.save(commit=False)
            Comment___Form.user = request.user
            Comment___Form.save()
            return JsonResponse({
                "status": 200,
                "msg": "نظر شما با موفقیت ثبت شد پس از بررسی ناظر در قسمت نظر ها قرار خواهد گرفت"
            })
        context = {
            "Comment__Form": Comment__Form
        }
        return render(request, "comment-form.html", context)
    else:
        return JsonResponse({
            "status": 205,
            "msg": "شما از قبل دیدگاهی برای این محصول ثبت کرده اید"
        })


def rating_for_product(request, slug):
    product_qs = get_object_or_404(Post_Products, slug=slug)
    if not request.is_ajax():
        return redirect("Ak_Main:shop_page")
    if len(Rating.objects.filter(user_id=request.user.id, product_id=product_qs.id)) == 0:
        Rating__Form = Rating_Form(request.POST or None, initial={"user": request.user, "product": product_qs})
        if Rating__Form.is_valid():
            Rating___Form = Rating__Form.save(commit=False)
            Rating___Form.user = request.user
            Rating___Form.save()
            return JsonResponse({
                "status": 200,
                "msg": "امتیاز شما با موفقیت ثبت شد "
            })
        context = {
            "Rating__Form": Rating__Form
        }
        return render(request, "rating-form.html", context)
    else:
        return JsonResponse({
            "status": 205,
            "msg": "شما از قبل به این محصول امتیاز داده اید"
        })


from .forms import Completion_User_Information
from Apps.Product_Apps__Ak.Extension import Calculate__Postage


def checkout(request):
    context = {}
    if request.user.is_authenticated and request.COOKIES.get(
            "products") is None:
        initial_form_value = {}
        for form_field in Completion_User_Information.__dict__.get("declared_fields"):
            if form_field != "first_name" and form_field != "last_name" and form_field != "select_city":
                if hasattr(request.user.profile, form_field) and getattr(request.user.profile,
                                                                         form_field) != "":
                    initial_form_value[form_field] = getattr(request.user.profile, form_field)
            elif form_field != "select_city":
                if hasattr(request.user, form_field) and getattr(request.user, form_field) != "":
                    initial_form_value[form_field] = getattr(request.user, form_field)

        Completion_User__Information = Completion_User_Information(request.POST or None, initial=initial_form_value)
        context["Completion_User__Information"] = Completion_User__Information
        if Completion_User__Information.is_valid():
            for key, value in Completion_User__Information.cleaned_data.items():
                try:
                    if key != "first_name" and key != "last_name" and key != "select_city" and hasattr(
                            request.user.profile, key):
                        setattr(request.user.profile, key, value)
                        request.user.profile.save()
                    elif key == "first_name" or key == "last_name" and key != "select_city" and hasattr(request.user,
                                                                                                        key):
                        setattr(request.user, key, value)
                        request.user.save()

                    elif key == "select_post_method":
                        Cart_Qs = request.user.cart_set.filter(active=True)
                        if Cart_Qs:
                            Calc_Postage = Cart_Qs.first().Calculate_Postage(
                                from_city="3208",
                                to_city=Completion_User__Information.cleaned_data.get("select_city"),
                                post_method=Completion_User__Information.cleaned_data.get("select_post_method"),
                            )
                            Cart_Qs_Obj = Cart_Qs.first()
                            Cart_Qs_Obj.to_city_code = Completion_User__Information.cleaned_data.get("select_city")
                            Cart_Qs_Obj.posting_method = Completion_User__Information.cleaned_data.get(
                                "select_post_method")
                            Cart_Qs_Obj.save()
                except:
                    Completion_User__Information.add_error(key, "مقدار وارد شده صحیح نمیباشد")
                    return JsonResponse(Completion_User__Information.errors, safe=False)

            return JsonResponse({
                "status_code": 200,
                "Calc_Postage": Calc_Postage,
            })
        elif Completion_User__Information.errors:
            return JsonResponse(Completion_User__Information.errors, safe=False)
    elif request.user.is_authenticated and request.COOKIES.get(
            "products") is not None:
        COOKIE = request.COOKIES.get("products")
        txt = re.search("([\d\-]+)", COOKIE).group() if re.search("([\d\-]+)",
                                                                  COOKIE) is not None else f"{COOKIE}" if str(
            COOKIE).isdigit() else ""
        txt = txt.split("-") if "-" in txt else [txt] if txt.isdigit() else []
        if len(txt) != 0:
            Cart_Obj = Cart.objects.filter(user_id=request.user.id, active=True)
            if Cart_Obj.exists():
                for Product_Id in txt:
                    Product_Obj = Post_Products.objects.filter(id=Product_Id)
                    if Product_Obj.exists():
                        Cart_Item.objects.create(cart=Cart_Obj.first(), product=Product_Obj.first(), count=1)
            else:
                Cart_Obj = Cart.objects.create(user_id=request.user.id, active=True)
                for Product_Id in txt:
                    Product_Obj = Post_Products.objects.filter(id=Product_Id)
                    if Product_Obj.exists():
                        Cart_Item.objects.create(cart=Cart_Obj.first(), product=Product_Obj.first(), count=1)
    return render(request, "checkout.html", context)


from .models import About_Us


def about_us(request):
    About_Us_Qs = About_Us.objects.first()
    context = {
        "About_Us_Qs": About_Us_Qs
    }
    return render(request, "about-us.html", context)


# @login_required(login_url=reverse("Ak_User_Account:Login"))
def Send_Payment_Gateway_Request(request):
    Cart_Qs = get_object_or_404(Cart, active=True, user=request.user)
    if Cart_Qs:
        Calc_Postage = Cart_Qs.Calculate_Postage(
            from_city="3208",
            to_city=str(Cart_Qs.to_city_code),
            post_method=str(Cart_Qs.posting_method),
        )
        Cart_Qs.Postage = Calc_Postage.get("Postal_Cost")
        Cart_Qs.save()
        Amount = Calc_Postage.get("Total_Cost")
        Client_Req_Obj = Py_Ir(Api_Key=gate_way_api_key)
        Pay_Response = Client_Req_Obj.request_payment_link(amount=Amount,
                                                           redirect_url=f"{request.META['HTTP_HOST']}/verify")
        return redirect(Pay_Response.get("payment_url"))


@login_required()
def Verify_Gate_Way_Request(request, *args, **kwargs):
    Client_Req_Obj = Py_Ir(Api_Key=gate_way_api_key)
    Response = Client_Req_Obj.bank_transaction_verification(
        Request_Object=request,
        status=request.GET.get("status"),
        token=request.GET.get("token"),
        request_user_id=request.user.id
    )

    if Response["status"] == 1:
        Cart_Object = Cart.objects.filter(user_id=request.user.id, active=True)
        if Cart_Object:
            Cart_Object = Cart_Object.first()
            Cart_Object.active = False
            Cart_Object.pay_time = timezone.now()
            Cart_Object.save()

            for Cart_Item_Obj in Cart_Object.cart_item_set.all():
                Product = Post_Products.objects.filter(id=Cart_Item_Obj.product_id).first()
                Product.inventory -= 1
                Product.sold += 1
                Product.save()
    context = {
        "Response": Response,
    }
    return render(request, "order-completed.html", context)
