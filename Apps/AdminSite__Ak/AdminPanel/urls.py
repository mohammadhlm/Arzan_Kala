from django.urls import path, include, reverse_lazy
from .views import (
    # -- User Apps
    list_user_view,
    edit_user_view,
    show_user_view,
    delete_user_view,
    advanced_user_filter_view,

    # Products App
    products_list_view,
    create_product_view,
    add_more_img_product,
    create_tag_view,
    create_category_view,
    search_tag_view,
    search_category_view,
    search_brand_view,
    advanced_product_filter,
    invoice_display,
    deleted_product_view,
    search_slider_view,
    create_brand_view,
    create_slider_view,

    # Site Settings
    view_settings,
    customizer_theme,

    # Email Management
    email_management,
    creating_sending_mail,
    remove_mail,

    # Edit User
    save_information_edit_user,

    # Create User
    default_user_form_view,
    user_information_form_view,

    LoginAdmin,
    LogOut_Admin_View,
    IndexView,

    # Wallet
    WALLET_VIEW,
)
from django.contrib.auth import views as auth_views

app_name = 'AdminSite__Ak'
urlpatterns = [
    # Users Page App
    path('user/users-list', list_user_view, name='list_users_view'),
    path('user/edit-user/<int:pk>', edit_user_view, name='edit_user_view'),
    path('user/save-information/<int:pk>', save_information_edit_user, name='save_information_edit_user_view'),
    path('user/view-user/<int:pk>', show_user_view, name='show_user_view'),
    path('user/user-info-form/<int:pk>', user_information_form_view, name='user_information_form_view'),
    path('user/default-user-form/', default_user_form_view, name='default_user_form_view'),
    path('user/delete-user/', delete_user_view, name='delete_user_form_view'),
    path('user/advanced-user-filter/', advanced_user_filter_view, name='advanced_user_filter'),
    # --------------------------------------------------------------------
    # Products Page App
    path('products/products-list/', products_list_view, name='products_list_view'),
    path('product/create-product/', create_product_view, name='create_product_view'),
    path('product/add-more-pr-img/', add_more_img_product, name='add_more_img_product_view'),
    path('product/create-tag/', create_tag_view, name='create_tag_view'),
    path('product/create-category/', create_category_view, name='create_category_view'),
    path('product/create-brand/', create_brand_view, name='create_brand_view'),
    path('product/create-slider/', create_slider_view, name='create_slider_view'),
    path('search-tag/', search_tag_view, name='search_tag_view'),
    path('search-category/', search_category_view, name='search_category_view'),
    path('search-live-brand/', search_brand_view, name='search_brand_view'),
    path('search-live-slider/', search_slider_view, name='search_slider_view'),
    path('advanced-product-filter/', advanced_product_filter, name="advanced-product-filter-view"),
    path('product/invoice/<int:id>', invoice_display, name="product_invoice_display"),
    path('deleted-product/', deleted_product_view, name="deleted_product_view"),
    # --------------------------------------------------------------------
    # Site Settings App
    path('settings/', view_settings, name='settings_view'),
    path('customize/', customizer_theme, name='customize_theme'),
    # --------------------------------------------------------------------
    # Email Management
    path('email-management/', email_management, name="email_management_view"),
    path('send-mail/', creating_sending_mail, name="creating_sending_mail_view"),
    path("removed-mail/", remove_mail, name="removed_mail_view"),

    # Wallet View
    path("wallet/", WALLET_VIEW, name="wallet_view"),

    path('', IndexView, name='dashboard'),
    path('login/', LoginAdmin, name='AdminAuth'),
    path('logout/', LogOut_Admin_View, name='admin_logout'),
]

from .forms.authentication_form import ResetPasswordAdmin, SetNewAdminPassword

urlpatterns += [
    # ...
    # Forget Password
    path('reset-password/',
         auth_views.PasswordResetView.as_view(
             template_name='AdminPanel/Auth/password_reset_form.html',
             subject_template_name='AdminPanel/Auth/password_reset_subject.txt',
             email_template_name='AdminPanel/Auth/password_reset_email.html',
             form_class=ResetPasswordAdmin,
             success_url=reverse_lazy('AdminSite__Ak:password_reset_done'),
         ),
         name='password_reset'
         ),

    path('manager/password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='AdminPanel/Auth/password_reset_done.html'
         ),

         name='password_reset_done'),
    path('manager/password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='AdminPanel/Auth/password_reset_confirm.html',
             form_class=SetNewAdminPassword,
             success_url=reverse_lazy('AdminSite__Ak:password_reset_complete')

         ),

         name='password_reset_confirm'),
    path('manager/password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='AdminPanel/Auth/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]
