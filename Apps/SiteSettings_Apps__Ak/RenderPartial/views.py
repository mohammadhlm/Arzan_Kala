from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
# Site Settings Model
from Apps.SiteSettings_Apps__Ak.SiteSettings.models import SiteSettings
from Apps.Product_Apps__Ak.models import Post_Products, Category_Product
from Apps.Ak__Main__.forms import Product_Add_To_Cart
from Apps.Product_Apps__Ak.models import Cart_Item, Cart


def Footer(request, *args, **kwargs):
    ObjSiteSettings = SiteSettings.objects.first()
    FooterContext = {
        'ObjSiteSettings': ObjSiteSettings
    }
    return render(
        request=request,
        template_name='All_Template_Main/Footer/Footer_Black_Main.html',
        context=FooterContext
    )


def header_one(request):
    contact_info = SiteSettings.objects.first()
    group_category = Category_Product.objects.all()[0:3]
    context = {
        "contact_info": contact_info,
        'group_category': group_category,
        "COOKIES": False if request.user.is_authenticated else True if not request.user.is_authenticated and request.COOKIES.get(
            "products") is None or request.COOKIES.get(
            "products") == "" else False
    }
    if request.user.is_authenticated:
        Cart_qs = Cart.objects.filter(user=request.user,active=True)
        if Cart_qs.exists():
            print(Cart_qs)
            context["total_product_price"] = Cart_qs.first().total_product_price
        else:
            context["total_product_price"] = 0
    if not request.user.is_authenticated and request.COOKIES.get("products") is not None or "":
        Product_Cookies = request.COOKIES.get("products")
        txt = re.search("([\d\-]+)", Product_Cookies).group() if re.search("([\d\-]+)",
                                                                           Product_Cookies) is not None else f"{Product_Cookies}" if str(
            Product_Cookies).isdigit() else ""
        txt = txt.split("-") if "-" in txt else [txt] if txt.isdigit() else []
        Product_Qs_Unk_User = None
        cart_total_price = 0
        if txt:
            for index, Product_id in enumerate(txt):
                if index == 0:
                    Product_Qs_Unk_User = Post_Products.objects.filter(id=int(Product_id))
                else:
                    Product_Qs_Unk_User = Product_Qs_Unk_User | Post_Products.objects.filter(id=int(Product_id))
            for product in Product_Qs_Unk_User:
                cart_total_price += product.discounted_price if product.discounted_price else product.final_price

            context["Product_Qs_Unk_User"] = Product_Qs_Unk_User
            context["cart_item_count"] = Product_Qs_Unk_User.count()
            context["total_product_price"] = cart_total_price
            context["Product_Qs_Unk_User"] = Product_Qs_Unk_User.all()
    return render(request, 'All_Template_Main/Header_Main/Header_1/header-one.html', context)


import re


def header_two(request):
    contact_info = SiteSettings.objects.first()
    context = {
        "list_category": Category_Product.objects.all()[0:7],
        "contact_info": contact_info,
        "COOKIES": False if request.user.is_authenticated else True if not request.user.is_authenticated and request.COOKIES.get(
            "products") is None or request.COOKIES.get(
            "products") == "" else False
    }
    if request.user.is_authenticated:
        Cart_qs = Cart.objects.filter(user=request.user,active=True)
        if Cart_qs.exists():
            context["total_product_price"] = Cart_qs.first().total_product_price
        else:
            context["total_product_price"] = 0
    if not request.user.is_authenticated and request.COOKIES.get("products") is not None or "":
        Product_Cookies = request.COOKIES.get("products")
        txt = re.search("([\d\-]+)", Product_Cookies).group() if re.search("([\d\-]+)",
                                                                           Product_Cookies) is not None else f"{Product_Cookies}" if str(
            Product_Cookies).isdigit() else ""
        txt = txt.split("-") if "-" in txt else [txt] if txt.isdigit() else []
        Product_Qs_Unk_User = None
        cart_total_price = 0
        if txt:
            for index, Product_id in enumerate(txt):
                if index == 0:
                    Product_Qs_Unk_User = Post_Products.objects.filter(id=int(Product_id))
                else:
                    Product_Qs_Unk_User = Product_Qs_Unk_User | Post_Products.objects.filter(id=int(Product_id))
            for product in Product_Qs_Unk_User:
                cart_total_price += product.discounted_price if product.discounted_price else product.final_price

            context["Product_Qs_Unk_User"] = Product_Qs_Unk_User
            context["cart_item_count"] = Product_Qs_Unk_User.count()
            context["total_product_price"] = cart_total_price
            context["Product_Qs_Unk_User"] = Product_Qs_Unk_User.all()
    return render(request, "All_Template_Main/Header_Main/Header_1/header-two.html", context)


def remove_product_from_cart(request):
    Product__Add_To_Cart = Product_Add_To_Cart(request.POST or None)

    # "This section is about adding or removing a product from the user's shopping cart"
    if Product__Add_To_Cart.is_valid() and request.user.is_authenticated:
        get_object_or_404(Post_Products, id=Product__Add_To_Cart.cleaned_data.get("product_id"))
        Cart_qs = Cart.objects.filter(user_id=request.user.id, active=True)

        # "This section is for the logged in user who has an active purchase card"
        if Cart_qs.exists():

            # "This section is for the logged in user whose product is already in the cart and the selected product will be removed from the cart"
            if len(Cart_Item.objects.filter(cart_id=Cart_qs.first().id,
                                            product_id=Product__Add_To_Cart.cleaned_data.get("product_id"))) > 0:
                cart_item = Cart_Item.objects.filter(cart_id=Cart_qs.first().id,
                                                     product_id=Product__Add_To_Cart.cleaned_data.get(
                                                         "product_id")).first()
                delete_product_id = cart_item.product.id
                cart_item.delete()
                return JsonResponse({
                    "status_code": 200,
                    "status": 700,
                    "delete_product_id": delete_product_id,
                    "total_product_price": Cart_qs.first().total_product_price,
                    "msg": "محصول از لیست سبد خرید شما با موفقیت حذف شد"
                })

            # "This section is for the logged in user whose selected product is not in the cart and a new item is added to the cart"
            else:
                new_cart_item = Cart_Item.objects.create(cart_id=Cart_qs.first().id,
                                                         product_id=Product__Add_To_Cart.cleaned_data.get("product_id"),
                                                         count=1)
                return JsonResponse({
                    "status_code": 200,
                    "status": 800,
                    "product_id": new_cart_item.product.id,
                    "item_product_photo_url": new_cart_item.product.photo.url,
                    "product_name": new_cart_item.product.name,
                    'item_count': new_cart_item.count,
                    "item_total": new_cart_item.total,
                    "get_absolute_url": new_cart_item.product.get_absolute_url,
                    'total_product_price': new_cart_item.cart.total_product_price,
                    "msg": "محصول با موفقیت به سبد خرید شما افزوده شد"
                })

        # "This section is for the logged in user who does not have an active purchase card and the purchase card is made for it and the product is added to the item of the purchase card.
        else:
            Cart_q = Cart.objects.create(user_id=request.user.id, active=True)
            Cart_Item.objects.create(cart_id=Cart_q.id, product_id=Product__Add_To_Cart.cleaned_data.get("product_id"),
                                     count=1)
            return JsonResponse({
                "status_code": 200,
                "status": 800,
                "product_id": Cart_Item.product.id,
                "item_product_photo_url": Cart_Item.product.photo.url,
                "product_name": Cart_Item.product.name,
                'item_count': Cart_Item.count,
                "item_total": Cart_Item.total,
                "get_absolute_url": Cart_Item.product.get_absolute_url,
                'total_product_price': Cart_Item.cart.total_product_price,
                "msg": "محصول با موفقیت به لیست سبد خرید شما افزوده شد"
            })

    # "This section is for a user who is not logged in and the product cookie is available in the user's browser"
    elif Product__Add_To_Cart.is_valid() and not request.user.is_authenticated and request.COOKIES.get(
            "products") is not None:
        product_qs = get_object_or_404(Post_Products, id=Product__Add_To_Cart.cleaned_data.get("product_id"))
        COOKIE = request.COOKIES.get("products")
        txt = re.search("([\d\-]+)", COOKIE).group() if re.search("([\d\-]+)",
                                                                  COOKIE) is not None else f"{COOKIE}" if str(
            COOKIE).isdigit() else ""
        txt = txt.split("-") if "-" in txt else [txt] if txt.isdigit() else []

        # "This section is for a user who is not logged in to the system and there is a product in its cookie and the product is removed from the user's shopping cart."
        if len(txt) != 0 and str(Product__Add_To_Cart.cleaned_data.get("product_id")) in txt:
            txt.remove(str(Product__Add_To_Cart.cleaned_data.get("product_id")))
            total_product_price = 0
            for pr_id in txt:
                Pr_qs = Post_Products.objects.filter(id=int(pr_id))
                if Pr_qs.exists():
                    total_product_price += Pr_qs.first().discounted_price if Pr_qs.first().discounted_price else Pr_qs.first().final_price
            txt = '-'.join(str(product_id) for product_id in txt)
            response = JsonResponse({
                'status_code': 200,
                'status': 700,
                "delete_product_id": Product__Add_To_Cart.cleaned_data.get("product_id"),
                'total_product_price': total_product_price,
                "msg": "محصول با موفقیت از لیست سبد خرید شما حذف شد"
            })
            response.set_cookie('products', txt, max_age=None)
            return response

        # "This section is for a user who is not logged in and the product is not in the cookie and the product is added to the user cart"
        else:
            txt.append(str(Product__Add_To_Cart.cleaned_data.get("product_id")))
            total_product_price = 0
            for pr_id in txt:
                Pr_qs = Post_Products.objects.filter(id=int(pr_id))
                if Pr_qs.exists():
                    total_product_price += Pr_qs.first().discounted_price if Pr_qs.first().discounted_price else Pr_qs.first().final_price
            txt = '-'.join(str(product_id) for product_id in txt)
            response = JsonResponse({
                'status_code': 200,
                'status': 800,
                "product_id": product_qs.id,
                "item_product_photo_url": product_qs.photo.url,
                "product_name": product_qs.name,
                'item_count': 1,
                "item_total": product_qs.discounted_price if product_qs.discounted_price else product_qs.final_price,
                "get_absolute_url": product_qs.get_absolute_url,
                'total_product_price': total_product_price,
                "msg": "محصول با موفقیت به لیست سبد خرید شما افزوده شد"
            })
            response.set_cookie('products', txt, max_age=None)
            return response

    # "This part is related to the user who is not logged in and the product cookie is not found in its browser or the product is not available in it, in this part the product cookie is made for it again and the product is added to the user's shopping cart list."
    elif Product__Add_To_Cart.is_valid() and not request.user.is_authenticated and request.COOKIES.get(
            "products") is None or "":
        product_qs = Post_Products.objects.filter(id=Product__Add_To_Cart.cleaned_data.get("product_id"))
        if product_qs.exists():
            product_qs = product_qs.first()
            response = JsonResponse({
                'status_code': 200,
                'status': 800,
                "product_id": product_qs.id,
                "item_product_photo_url": product_qs.photo.url,
                "product_name": product_qs.name,
                'item_count': 1,
                "item_total": product_qs.discounted_price if product_qs.discounted_price else product_qs.final_price,
                "get_absolute_url": product_qs.get_absolute_url,
                'total_product_price': product_qs.discounted_price if product_qs.discounted_price else product_qs.final_price,
                "msg": "محصول با موفقیت به لیست سبد خرید شما افزوده شد"
            })
            response.set_cookie('products', str(Product__Add_To_Cart.cleaned_data.get("product_id")), max_age=None)
            return response
    context = {
        'Product__Add_To_Cart': Product__Add_To_Cart
    }
    return render(request, 'remove-product-from-cart.html', context)
