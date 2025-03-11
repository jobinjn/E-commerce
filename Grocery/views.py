from http.client import HTTPResponse
from lib2to3.fixes.fix_input import context

from taggit.models import Tag
from django.db.models import Avg
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from Grocery.models import Product, Category, Vendor, CartOrder, ProductImages, CartOrderItems, ProductReview, Wishlist, ADDRESS
from pyexpat import features
from Grocery.forms import ProductReviewForm
from unicodedata import category


# This is home apge
def index(request):
    # products = Product.objects.all
    products = Product.objects.filter(product_status= "Published", featured = True)
    context = {
        "products": products
    }
    return render(request,'Grocery/index.html', context)

#This is for products list
def product_list_view(request):
    # products = Product.objects.all
    products = Product.objects.filter(product_status= "Published")
    context = {
        "products": products
    }
    return render(request,'Grocery/product-list.html', context)

def category_list_view(request):
    categories = Category.objects.all

    context = {
        "categories": categories
    }
    return render(request,'Grocery/category-list.html', context)

def category_product_list_view(request, cid):
    # Fetch single category safely
    category = get_object_or_404(Category, cid=cid)
    products = Product.objects.filter(product_status= "Published", category=category)


    context = {
        "category": category,
        "products": products,
    }
    return render(request, 'Grocery/category-product-list.html', context)



def vendors_list_view(request):

    vendors = Vendor.objects.all()


    context = {
        "vendors": vendors,
    }
    return render(request, 'Grocery/vendors-list.html', context)

def vendor_detail_list_view(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(product_status= "Published", vendor=vendor)

    context = {
        "vendor": vendor,
        "products": products,
    }
    return render(request, 'Grocery/vendor-detail-list.html', context)



def product_detail_view(request, pid):
    product = Product.objects.get(pid=pid)
    products = Product.objects.filter(category= product.category).exclude(pid=pid)
    p_image = product.p_images.all()

    #getting all review
    reviews  =  ProductReview.objects.filter(product=product).order_by("-date")

    #review form
    review_form = ProductReviewForm()

    make_review = True
    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user = request.user,product=product).count()

        if user_review_count > 0:
            make_review = False

    #getting average
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating = Avg('ratings'))
    context ={
        "product":product,
        "p_image":p_image,
        "products":products,
        "make_review" : make_review,
        "reviews": reviews,
        "review_form":review_form,
        "average_rating":average_rating,
    }
    return render(request, 'Grocery/product-details.html', context)




def tags_list_view(request, tag_slug=None):
    product =Product.objects.filter(product_status= "Published").order_by("-id")

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug = tag_slug)
        products = product.filter(tags__in=[tag])

        context ={
            "products" : products,
            "tag" : tag,
        }
        return render(request, 'Grocery/tags-list.html', context)

def add_review_form(request, pid):
    product = Product.objects.get(pk=pid)
    user = request.user

    review = ProductReview.objects.create(
        user=user,
        product=product,
        review=request.POST['review'],
        ratings=request.POST['ratings'],  # Ensure integer
    )

    context = {
        'user': user.username,
        'review': request.POST['review'],
        'ratings': request.POST['ratings'],  # Ensure integer
    }

    # Compute average rating
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('ratings'))

    return JsonResponse({
        'bool': True,
        'context': context,  # ✅ Use "context" instead of "avg"
        'average_rating': average_rating,
    })


def search_view(request):
    query = request.GET.get("q")

    products =  Product.objects.filter(title__icontains=query).order_by("-date")

    context = {
        "products":products,
        "query":query,
    }
    return render(request,"Grocery/search.html", context)
