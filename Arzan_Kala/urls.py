"""Arzan_Kala URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Module Static Files
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # Include Urls
    path('', include("Apps.Ak__Main__.urls", namespace="Ak_Main")),
    # Include Admin Panel Url
    path('manager/', include("Apps.AdminSite__Ak.AdminPanel.urls", namespace='AdminSite__Ak')),
    # Include User Apps Url
    path('', include("Apps.Usrs_Apps__Ak.Ak_User_Account.urls", namespace="Ak_User_Account")),
    path('', include("Apps.Usrs_Apps__Ak.Ak_User_Account_Dashboard.urls", namespace="Ak_User_Account_Dashboard")),
    # Include Product Apps Url
    path('', include('Apps.Product_Apps__Ak.urls', namespace="Ak_Product_Apps")),
    # Django Social Auth
    path('', include('social_django.urls', namespace='social')),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
