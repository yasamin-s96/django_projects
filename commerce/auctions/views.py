from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from .models import *

class ListingForm(forms.ModelForm):
    image_url = forms.URLField(required=False)
    class Meta:
        model = Listing
        fields = ["title", "description", "starting_bid","categories", "image_url"]
    def __init__(self, *args, **kwargs):
        super(ListingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


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
    return HttpResponseRedirect(reverse("index"))


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            new_listing = Listing()
            new_listing.creator = request.user
            new_listing.title = form.cleaned_data["title"]
            new_listing.description = form.cleaned_data["description"]
            new_listing.starting_bid = form.cleaned_data["starting_bid"]
            new_listing.save()
            # new_listing.categories.add(form.cleaned_data["category"])
            new_listing.image_url = form.cleaned_data["image_url"]
            
            return render(request, "auctions/create_listing.html", {"form": ListingForm(), "status":True})

        else:
            return render(request, "auctions/create_listing.html", {"form": form, "status":False})
    else:      
        return render(request, "auctions/create_listing.html", {"form": ListingForm(), "status": None})
