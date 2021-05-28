from django.contrib import admin

# Register your models here.
from Apps.Product_Apps__Ak.models import Product_Tags
from .models import Customize_Theme,Email_Management

admin.site.register(Product_Tags)
admin.site.register(Customize_Theme)
admin.site.register(Email_Management)
