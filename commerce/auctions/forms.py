from django import forms
from .models import Category, Listing, Bid, Comment
from django.core.exceptions import ValidationError


class ListingForm(forms.ModelForm):
    image_url = forms.URLField(required=False)
    categories = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
     choices=Category.objects.all().values_list("id", "title"))
    class Meta:
        model = Listing
        fields = ["title", "description", "starting_bid","categories", "image_url"]

class BidForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        current_listing_id = kwargs.pop("listing_id", None)
        super().__init__(*args, **kwargs)
        self.current_listing_id = current_listing_id
    class Meta:
        model = Bid
        fields = ["amount"]
    
    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        current_listing = Listing.objects.get(pk=self.current_listing_id)
        if amount < current_listing.starting_bid:
            raise ValidationError(f"The bid must be at least ${current_listing.starting_bid}")

        if Bid.objects.exists():
            current_listing_bids = Bid.objects.filter(listing = Listing.objects.get(pk=self.current_listing_id))
            if current_listing_bids.exists():
                for bid in current_listing_bids:
                    if amount <= bid.amount:
                        raise ValidationError("Your bid must be greater than any other bids that have been placed.")
        
        return amount

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]

