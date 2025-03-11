from django.urls import path
from Grocery.views import (index, product_list_view, category_list_view, category_product_list_view,
                           vendors_list_view, vendor_detail_list_view, product_detail_view,tags_list_view
                           ,add_review_form, search_view)

from django.conf import settings
from django.conf.urls.static import static



app_name = 'Grocery'
urlpatterns = [

    #Home page
    path("", index,name= "index"),
    path("products/", product_list_view, name="product-list"),
    path("product/<pid>/", product_detail_view, name="product-details-list"),

    #category
    path("category/", category_list_view, name="category-list"),
    path("category/<cid>/", category_product_list_view, name="category-product-list"),

    #Vendors
    path("vendors/", vendors_list_view,name = "vendors_list"),
    path("vendor/<vid>/", vendor_detail_list_view,name = "vendor_detail_list"),

    #tags
    path("products/tag/<slug:tag_slug>/", tags_list_view, name="tags-list"),

    #reviews
    path("add_review_form/<int:pid>/", add_review_form, name="add_review_form"),

    #search
    path("search/", search_view, name="search"),

]
urlpatterns += static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)

