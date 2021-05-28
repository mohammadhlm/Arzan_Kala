from django.urls import path
# Views
from .views import Dashboard, change_user_information, logout_user

app_name = 'Ak_User_Account_Dashboard'
urlpatterns = [
    path('user/dashboard/', Dashboard, name="User_Dashboard"),
    path('user/change_user_information/', change_user_information,name="changer_user_information"),
    path("user/logout/", logout_user, name="logout_user"),
]
