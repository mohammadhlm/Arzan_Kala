from django.urls import path
# View Function Base
from .views import home_page, contact_us, product_detail, category_detail, shop_page, product_ajax_filter, \
    comment_for_product, rating_for_product, checkout, about_us, Send_Payment_Gateway_Request, Verify_Gate_Way_Request
from Apps.SiteSettings_Apps__Ak.RenderPartial.views import remove_product_from_cart

app_name = "Ak_Main"
urlpatterns = [
    path('', home_page, name="Home_Page"),
    path('contact-us/', contact_us, name="contact-us"),
    path('product/<slug:slug>', product_detail, name="product-detail"),
    path('category/<slug:slug>', category_detail, name="category-detail"),
    path('shop/', shop_page, name="shop_page"),
    path('ajax-filter/', product_ajax_filter, name="product_ajax_filter"),
    path('send-comment/<slug:slug>', comment_for_product, name="product_comment"),
    path('send-rating/<slug:slug>', rating_for_product, name="product_rating"),
    path('remove-product-from-cart', remove_product_from_cart, name="remove_product_from_cart"),
    path('checkout', checkout, name="checkout"),
    path('about-us/', about_us, name="about_us"),
    # ----Gateway----
    path('send-request/', Send_Payment_Gateway_Request, name="send_gate_way_request"),
    path('verify/', Verify_Gate_Way_Request, name="verify_gate_way_request"),

]
