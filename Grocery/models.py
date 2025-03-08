from random import choices
from sys import prefix
from django.utils.html import mark_safe
from django.db import models
from django.template.defaultfilters import length
from django.utils.regex_helper import Choice
from shortuuid.django_fields import ShortUUIDField
from userauths.models import User
from taggit.managers import TaggableManager

STATUS_CHOICE = (
    ("process","processing"),
    ("shipped","shipped"),
    ("delivered","Delivered"),
)

STATUS= (
    ("draft","Draft"),
    ("disabled","Disabled"),
    ("rejected","Rejected"),
    ("in_review","In Review"),
    ("Published","Published"),
)
RATING= (
    ("1","★☆☆☆☆"),
    ("2","★★☆☆☆"),
    ("3","★★★☆☆"),
    ("4","★★★★☆"),
    ("5","★★★★★"),
)

def user_directory_path(instance,filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

# Create your models here.
class Category(models.Model):
    cid = ShortUUIDField(unique=True, length = 10, max_length=20, prefix= 'cat', alphabet="abcdefgh123456")
    title = models.CharField(max_length=100, default="food")
    image = models.ImageField(upload_to="category",default= "category.jpg")

    class Meta:
        verbose_name_plural = "categories"

    def category_image(self):
        return mark_safe('<img src="%s width="50" height="50"/>'% (self.image.url))
    def __str__(self):
        return self.title

class Tags(models.Model):
    pass

class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=20, prefix='ven', alphabet="abcdefgh123456")
    title = models.CharField(max_length=100, default="nestify")
    image = models.ImageField(upload_to=user_directory_path, default='vendor.jpg')
    cover_image = models.ImageField(upload_to=user_directory_path, default='vendor.jpg')
    description = models.TextField(null=True, blank=True, default="i am an vendor")
    address = models.CharField(max_length=100,default="arumanai")
    contact = models.CharField(max_length=100, default='+91 8547371755')
    chat_resp_time = models.CharField(max_length=100,default='100')
    shipping_time = models.CharField(max_length=100,default='100')
    authentic_rating = models.CharField(max_length=100,default='100')
    days_return = models.CharField(max_length=100,default='100')
    warranty_period = models.CharField(max_length=100,default='100')
    date = models.DateTimeField(auto_now_add=True,null=True, blank=True)



    user = models.ForeignKey(User, on_delete=models.SET, null=True)

    class Meta:
        verbose_name_plural = "Vendors"

    def vendor_image(self):
        return mark_safe('<img src="%s width="50" height="50"/>'% (self.image.url))
    def __str__(self):
        return self.title


class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=20, prefix='ven', alphabet="abcdefgh123456")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="user_products")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="category")
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name="products_vendor")
    title = models.CharField(max_length=100, default="fresh pear")
    image = models.ImageField(upload_to=user_directory_path, default='product.jpg')
    description = models.TextField(null=True, blank=True, default="this is the product")
    price = models.DecimalField(max_digits=10, decimal_places=2, default="1.99")
    old_price = models.DecimalField(max_digits=10, decimal_places=2, default="2.99")
    Specification = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=100, default="organic", null=True, blank=True)
    stock_count = models.CharField(max_length=100, default="10", null=True, blank=True)
    mfd = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    life = models.CharField(max_length=100, default="100 days", null=True, blank=True)
    tags = TaggableManager( blank=True)
    #tags = models.ForeignKey('Tags', on_delete=models.SET_NULL, null=True)
    product_status = models.CharField(choices=STATUS, max_length=10, default="in_review")
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)
    sku = ShortUUIDField(unique=True, length=4, max_length=20, prefix='sku', alphabet="1234567890")
    date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Products"

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title

    def get_percentage(self):
        if self.old_price and self.price:
            return ((self.old_price - self.price) / self.old_price) * 100
            return 0


# class ProductImages(models.Model):
#     image = models.ImageField(upload_to="Product-Images", default='product.jpg')
#     product = models.ForeignKey(Product, on_delete=models.SET, null=True)
#     date = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         verbose_name_plural = "Products-Images"


class ProductImages(models.Model):
    image = models.ImageField(upload_to="Product-Images", default='product.jpg')
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True, related_name='p_images')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Products-Images"

    def __str__(self):
        return f"Image for {self.product.title if self.product else 'No Product'}"



#************************************** cart, order, order items and address **********************************

class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=9999999999999999, decimal_places=2,default="1.99")
    paid_track = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices = STATUS_CHOICE, max_length=10, default="processing")

    class Meta:
        verbose_name_plural = "Carts order"

    def paid_status(self):
        return "Paid" if self.paid_track else "Unpaid"

    def order_rate(self):
        # Example of logic
        return self.price * 0.1

class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.SET_NULL, null=True)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    items = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=9999999999999999, decimal_places=2,default="1.99")
    total = models.DecimalField(max_digits=9999999999999999, decimal_places=2,default="1.99")


    class Meta:
        verbose_name_plural = "Carts order"

    def product_image(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />'% (self.image.url))

#************************************** product review, wishlist, address **********************************

class ProductReview(models.Model):
    RATING = [
        (1, "⭐"),
        (2, "⭐⭐"),
        (3, "⭐⭐⭐"),
        (4, "⭐⭐⭐⭐"),
        (5, "⭐⭐⭐⭐⭐"),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="reviews")
    review = models.TextField()
    ratings = models.IntegerField(choices=RATING, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "product reviews"

    def __str__(self):
        return self.product.title if self.product else "No Product"

    def get_rating(self):
        return dict(self.RATING).get(self.ratings, "No Rating")


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "wishlist "

    def __str__(self):
        return self.product.title

class ADDRESS(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Address "