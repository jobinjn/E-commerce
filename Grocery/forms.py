from django import forms
from Grocery.models import ProductReview

class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder' :"write review"}))

    class Meta:
        model = ProductReview
        fields =['review', 'ratings']