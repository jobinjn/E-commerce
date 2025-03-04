from itertools import product

from django.contrib import admin
from Grocery.models import Product, Category, Vendor, CartOrder, ProductImages, CartOrderItems, ProductReview, Wishlist, ADDRESS

# Register your models here.
class ProductImagesAdmin(admin.TabularInline):  # Use admin.StackedInline for a different layout
    model = ProductImages
    extra = 3

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'image', 'category','vendor', 'status', 'featured', 'pid']
    inlines = [ProductImagesAdmin]

class CategoryAdmin(admin.ModelAdmin):
    list_display = [ 'title', 'category_image']

class VendorAdmin(admin.ModelAdmin):
    list_display = [ 'title', 'vendor_image', 'address', 'contact']

class CartOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'price', 'paid_track', 'date', 'product_status']  # Replace with valid fields or methods

class CartOrderItemAdmin(admin.ModelAdmin):
    list_display = [ 'get_user', 'invoice_no', 'items', 'image', 'quantity', 'price', 'total']

    def get_user(self, obj):
        return obj.order.user  # Fetch user from related CartOrder

    get_user.short_description = 'User'  # Rename column in admin panel

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = [ 'user', 'product', 'review', 'ratings', 'date']

class WishlistAdmin(admin.ModelAdmin):
    list_display = [ 'user', 'product', 'date']

class AddressAdmin(admin.ModelAdmin):
    list_display = [ 'user', 'address', 'status']

admin.site.register(Product, ProductAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Vendor,VendorAdmin)
admin.site.register(CartOrder,CartOrderAdmin)
admin.site.register(CartOrderItems,CartOrderItemAdmin)
admin.site.register(ProductReview,ProductReviewAdmin)
admin.site.register(Wishlist,WishlistAdmin)
admin.site.register(ADDRESS,AddressAdmin)