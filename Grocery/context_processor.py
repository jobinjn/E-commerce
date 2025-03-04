from Grocery.models import Product, Category, Vendor, CartOrder, ProductImages, CartOrderItems, ProductReview, Wishlist, ADDRESS
from django.shortcuts import render
from unicodedata import category


def default(request):
    categories = Category.objects.all()
    address = None  # Default value in case of anonymous user

    if request.user.is_authenticated:  # Ensure user is logged in
        address = ADDRESS.objects.filter(user=request.user)

    return {
        "categories": categories,
        "address": address,
    }
