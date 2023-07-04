from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView
from .models import *
from .forms import *



def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return redirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)

        # Create a watchlist for newly created user
        new_watchlist = Watchlist.objects.create()
        user.watchlist = new_watchlist
        user.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            new_listing = form.save(commit=False)
            new_listing.creator = request.user
            new_listing.save()
            form.save_m2m()
            return HttpResponseRedirect(reverse("index"))

        else:
            messages.error(request, "Failed. Please fill the form correctly.")
    else:
        form = ListingForm()
    return render(request, "auctions/create_listing.html", {"form":form })

class ActiveListingsView(ListView):
    model = Listing
    template_name = "auctions/index.html"
    context_object_name = "listings"
    ordering = ["-created_at"]

def listing_details(request, listing_id):
    user = request.user
    listing = Listing.objects.get(pk=listing_id)
    context = {"listing":listing, "categories":listing.categories.all()}
    comment_form = CommentForm()
    bid_form = BidForm(listing_id=listing_id)
    context["comment_form"] = comment_form
    context["bid_form"] = bid_form
    # check if the listing already exists on user's watchlist:
    if user.watchlist.listings.filter(pk=listing_id).exists():
        context["listing_exists"] = True

    if request.method == "GET":
        return render(request, "auctions/listing_details.html", context)

    else:
        if request.POST.get("place_bid"):
            bid_form = BidForm(request.POST, listing_id=listing_id)
            if bid_form.is_valid():
                bid = bid_form.save(commit=False)
                bid.maker = user
                bid.listing = listing
                bid_form.save()
            else:
                context["bid"] = bid_form
                return render(request, "auctions/listing_details.html", context)

        if request.POST.get("close_auction"):
            listing.closed = True
            bids = listing.bids.all()
            maximum = 0
            for bid in bids:
                if bid.amount > maximum:
                    maximum = bid.amount
                    winning_bid = bid
                    
            listing.winner = winning_bid.maker
            listing.closed = True
            listing.save()

        if request.POST.get("add_to_watchlist"):
            user.watchlist.listings.add(listing)
            user.save()
            messages.success(request, "Successfully added to watchlist!")
             
        if request.POST.get("remove_from_watchlist"):
            user.watchlist.listings.remove(listing)
            messages.success(request, "Successfully removed from watchlist!")

        if request.POST.get("post_comment"):
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.user = user
                new_comment.listing = listing
                comment_form.save()

        return redirect(reverse("listing details", kwargs={"listing_id":listing_id}))



        















