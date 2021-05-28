from django.urls import path, include
from .views import login_page, register_page
from django.conf import urls

from .views import activate, Send_account_activation_link
from django.conf.urls import url

app_name = "Ak_User_Account"
urlpatterns = [
    path('user/login/', login_page, name="Login"),
    path('user/register/', register_page, name='Register'),
    path('user/reset-password/', Send_account_activation_link),
    path('user/activate/<slug:uidb64>/<slug:token>/', activate, name='activate')

]
