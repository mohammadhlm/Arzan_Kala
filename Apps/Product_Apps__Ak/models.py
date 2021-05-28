from django.db import models
from ckeditor.fields import RichTextField
from django.db.models import Q, Avg, Count
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
import emoji
from django.utils.text import slugify
from .Extension import Calculate__Postage
from Arzan_Kala.Extentions import Jalali_date_converter


# from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
def calculator_discount(price, discount):
    discount = str(discount)
    if price == 0:
        return price
    elif discount == "100":
        return 0
    else:
        finally_price = price * (1.0 - float(f"0.{discount}"))
        return finally_price


class Custom_manager_pr_category(models.Manager):
    def search_cat_pr_add(self, search):
        qs_cat = self.get_queryset().filter(category_name__icontains=search)
        list_cat = [{cat.pk: cat.category_name} for cat in qs_cat]
        if len(list_cat) > 0:
            return list_cat

    def show_cat_shop(self):
        qs_cat = self.get_queryset().all().order_by("-id")
        if len(qs_cat) > 0:
            return qs_cat


class Category_Product(models.Model):
    category_name = models.CharField(max_length=40, verbose_name="نام دسته بندی")
    slug = models.SlugField(default=None, allow_unicode=True)
    category_photo = models.ImageField(verbose_name='تصویر دسته بندی', upload_to="images/Product-Category/",
                                       default=None, blank=True)
    category_making_time = models.DateTimeField(auto_now_add=True)
    objects = Custom_manager_pr_category()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.slug)
        return super(Category_Product, self).save(*args, **kwargs)

    @property
    def get_product_related(self):
        return self.post_products_set.all()

    def get_product_header(self):
        return self.post_products_set.all()

    @property
    def get_absolute_url(self):
        return reverse("Ak_Main:category-detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.category_name


class Custom_Manager_Pr_tag(models.Manager):
    def search_tag_pr_add(self, sr_qs):
        qs_tg = self.get_queryset().filter(
            Q(tag_name__istartswith=sr_qs) | Q(tag_name__icontains=sr_qs) | Q(tag_name__iendswith=sr_qs) | Q(
                tag_name__in=sr_qs)).distinct()
        return qs_tg


class Product_Tags(models.Model):
    tag_name = models.CharField(max_length=35, verbose_name="نام برچسب")
    tag_making_time = models.DateTimeField(auto_now_add=True)
    objects = Custom_Manager_Pr_tag()

    def __str__(self):
        return self.tag_name


class Brand_Model(models.Model):
    photo = models.ImageField(upload_to="images/Product-Brand/")
    name = models.CharField(max_length=70)
    created_time = models.DateTimeField(auto_now_add=True)


class Custom_manager_product(models.Manager):
    def get_pr_status(self, status):
        qs = self.get_queryset().filter(status__exact=status)
        if len(qs) > 0:
            return qs

    def get_new_product(self):
        return self.get_queryset().filter(status__exact="PB", inventory__gt=0).order_by("-id")[0:7]

    def get_the_most_product_sold(self):
        return self.get_queryset().filter(status__exact="PB", inventory__gt=0).order_by("-sold")[0:7]

    def get_discounted_products(self):
        return self.get_queryset().filter(status__exact="PB", discounted_price__isnull=True).order_by(
            "-production_date")[0:4]

    def get_special_offer_products(self):
        return self.get_queryset().filter(status__exact="PB", special_offer=True)[0:7]

    def get_the_best_rated_product(self):
        return self.get_queryset().filter(status="PB").annotate(avg_rate=Avg("rating__star")).order_by("-avg_rate")[0:5]

    def advanced_filter_product_shop(self, **kwargs):

        category_id = kwargs.get("category_id")
        price_gte, price_lte = str(kwargs.get("price_filter")).split("-")
        brand_id = kwargs.get("brand_id")
        order_by = kwargs.get("order")
        qs = None
        for index, cat_id in enumerate(category_id.split(",")):
            if index == 0:
                qs = self.get_queryset().filter(
                    Q(category__id=int(cat_id)) &
                    Q(final_price__gte=price_gte) &
                    Q(final_price__lte=price_lte) &
                    Q(brand__id=brand_id)
                )
            else:
                qs.union(self.get_queryset().filter(
                    Q(category__id=int(cat_id)) &
                    Q(final_price__gte=price_gte) &
                    Q(final_price__lte=price_lte) &
                    Q(brand__id=brand_id)
                ))
            if order_by == "popularity":
                qs.annotate(rate_avg=Avg("rating__star")).order_by("-rate_avg")
            else:
                ordering = "-id" if order_by == "de" else "-date" if order_by == "date" else "price" if order_by == "price" else "-price" if order_by == "price-desc" else "-id"
                qs.order_by(ordering)
            return qs

    def get_the_most_visited_product(self):
        return self.get_queryset().annotate(visit_count=Count("product_visit_counter")).order_by("-visit_count")


class Home_Slider(models.Model):
    title = models.CharField(max_length=40)
    text = models.CharField(max_length=25)

    @property
    def get_photo(self):
        return Post_Products.objects.filter(slider=self).prefetch_related('slider')


class Post_Products(models.Model):
    STATUS = [
        ('NS', '-------'),
        ('PB', 'انتشار'),
        ('AC', 'بایگانی')
    ]
    slug = models.SlugField(default=None, verbose_name="نشانی اینترنتی")
    photo = models.ImageField(verbose_name="تصویر محصول", upload_to="images/Product-Photos/")
    name = models.CharField(verbose_name="نام محصول", max_length=200)
    short_description = RichTextField(verbose_name="توضیحات کوتاه محصول", max_length=300,
                                      config_name='Product_title_configuration')
    further_details = RichTextField(verbose_name="توضیحات کامل محصول", max_length=3000, config_name='default')
    attributes = models.JSONField(verbose_name="ویژگی های محصول", default=dict)
    tag = models.ManyToManyField(Product_Tags, verbose_name="انتخاب برچسب های محصول")
    brand = models.ForeignKey(Brand_Model, on_delete=models.SET_NULL, null=True)
    category = models.ManyToManyField(Category_Product, verbose_name="انتخاب دسته بندی محصول",
                                      help_text="لطفا حداقل 5 دسته بندی برای محصول خود انتخاب کنید")
    discounted_price = models.FloatField(verbose_name="قیمت با تخفیف محصول", blank=True, default=None)
    discount_percent = models.IntegerField(verbose_name="درصد تخفیف", blank=True, null=True)
    final_price = models.FloatField(verbose_name="قیمت نهایی محصول")
    publication_date = models.DateTimeField(verbose_name="تاریخ انتشار", default=timezone.now)
    production_date = models.DateTimeField(verbose_name="تاریخ ایجاد محصول", auto_now_add=True)
    update_date = models.DateTimeField(verbose_name="تاریخ بروزرسانی", auto_now=True)
    inventory = models.IntegerField(verbose_name="تعداد موجود")
    special_offer = models.BooleanField(verbose_name="پیشنهاد ویژه", default=False, blank=True)
    sold = models.IntegerField(verbose_name="تعداد فروخته شده", default=0, blank=True)
    status = models.CharField(verbose_name="وضعیت انتشار", choices=STATUS, max_length=2, default='NS')
    slider = models.ForeignKey(Home_Slider, on_delete=models.SET_NULL, null=True, blank=True)
    objects = Custom_manager_product()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.slug)
        if self.discount_percent is not None and self.discount_percent != 0:
            self.discounted_price = calculator_discount(self.final_price, self.discount_percent)
            return super(Post_Products, self).save(*args, **kwargs)
        else:
            return super(Post_Products, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class META:
        ordering = ["id"]

    @property
    def get_avg_rate(self):
        sum_rate = 0
        rate_qs = Rating.objects.filter(product_id=self.id)
        for obj in rate_qs:
            sum_rate += obj.star
        if len(rate_qs) > 0:
            return sum_rate / len(rate_qs)

    @property
    def rate_count(self):
        return len(Rating.objects.filter(product=self))

    @property
    def tag_count(self):
        return Product_Tags.objects.filter(post_products=self).count()

    @property
    def category_count(self):
        return Category_Product.objects.filter(post_products=self).count()

    @property
    def jalali_time_publication_date(self):
        return Jalali_date_converter(self.publication_date)

    @property
    def jalali_update_date(self):
        return Jalali_date_converter(self.update_date)

    @property
    def jalali_production_date(self):
        return Jalali_date_converter(self.production_date)

    def get_tag(self):
        return Product_Tags.objects.filter(post_products=self).prefetch_related("post_products_set")

    def get_category(self):
        return Category_Product.objects.filter(post_products=self).prefetch_related("post_products_set")

    def get_photo(self):
        return More_Product_Photos.objects.select_related("Product_Photos").filter(Product_Photos=self)

    @property
    def get_count_comment(self):
        return Comment.objects.select_related("product").filter(product=self, approved=True).count()

    @property
    def get_absolute_url(self):
        return reverse("Ak_Main:product-detail", kwargs={"slug": self.slug})


class Slider_Information(models.Model):
    product = models.OneToOneField(Post_Products, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="images/Slider-Photos/")

    def __str__(self):
        return self.product.name


class Product_Color(models.Model):
    color_code = models.CharField(max_length=20)
    color_name = models.CharField(max_length=50)
    product = models.ForeignKey(Post_Products, on_delete=models.CASCADE)

    def __str__(self):
        return self.color_name


class More_Product_Photos(models.Model):
    photo = models.ImageField(verbose_name="تصویر های بیشتر محصول", upload_to="images/More-Product-Photos/")
    product = models.ForeignKey(Post_Products, on_delete=models.CASCADE)


class Rating(models.Model):
    product = models.ForeignKey(Post_Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name="زمان ارسال نظر", auto_now_add=True, null=True)
    star = models.IntegerField(
        verbose_name="امتیاز محصول",
        default=None,
        choices=[(1, emoji.emojize(":star:")),
                 (2, emoji.emojize(":star: :star:")),
                 (3, emoji.emojize(":star: :star: :star:")),
                 (4, emoji.emojize(":star: :star: :star: :star:")),
                 (5, emoji.emojize(":star: :star: :star: :star: :star:")),
                 ])

    def __str__(self):
        return f"{self.product.name} {self.user.get_full_name()}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Post_Products, on_delete=models.CASCADE)
    body = models.TextField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.product.name + f"({self.user.get_full_name()})"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    pay_time = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=False)
    Postage = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name()

    def save(self, *args, **kwargs):
        if self.active:
            self.pay_time = timezone.now()
        return super(Cart, self).save(*args, **kwargs)

    @property
    def get_absolute_url(self):
        return reverse("AdminSite__Ak:product_invoice_display", kwargs={"id": self.id})

    @property
    def total_product_price(self):
        total = 0
        for item in self.cart_item_set.all():
            total += item.total
        return total

    @property
    def jalali_created_time(self):
        return Jalali_date_converter(self.created_time)

    @property
    def jalali_pay_time(self):
        return Jalali_date_converter(self.pay_time)

    @property
    def jalali_pay_time(self):
        return Jalali_date_converter(self.pay_time)

    def Calculate_Postage(self, from_city, to_city, post_method):
        total_wright = 0
        for item in self.cart_item_set.all():
            if item.product.attributes.get("weight"):
                total_wright += item.product.attributes.get("weight")
        product__total_price = self.total_product_price
        Postage = Calculate__Postage(from_city, to_city, product__total_price, total_wright, post_method)
        if Postage:
            return Postage


class Cart_Item(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Post_Products, on_delete=models.CASCADE)
    count = models.IntegerField()
    total = models.FloatField(blank=True)

    def __str__(self):
        return self.product.name

    def save(self, *args, **kwargs):
        self.total = self.product.discounted_price * self.count if self.product.discounted_price is not None else self.product.final_price * self.count
        return super(Cart_Item, self).save(*args, **kwargs)


class Product_Visit_Counter(models.Model):
    product = models.ForeignKey(Post_Products, on_delete=models.SET_NULL, null=True)
    ip = models.GenericIPAddressField()
    visit_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.visit_date
