from django.contrib import admin
from .models import Post_Products, Category_Product, Rating, Comment, Brand_Model, Product_Color, Cart, Cart_Item, \
    More_Product_Photos, Home_Slider,Slider_Information

# Register your models here.
admin.site.register(Post_Products)
admin.site.register(Category_Product)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(Brand_Model)
admin.site.register(Product_Color)
admin.site.register(Cart)
admin.site.register(Cart_Item)
admin.site.register(More_Product_Photos)
admin.site.register(Home_Slider)
admin.site.register(Slider_Information)
